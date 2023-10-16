##
# CyanaMRReader.py
#
# Update:
##
""" A collection of classes for parsing CYANA MR files.
"""
import sys
import os

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, PredictionMode

try:
    from wwpdb.utils.nmr.mr.LexerErrorListener import LexerErrorListener
    from wwpdb.utils.nmr.mr.ParserErrorListener import ParserErrorListener
    from wwpdb.utils.nmr.mr.CyanaMRLexer import CyanaMRLexer
    from wwpdb.utils.nmr.mr.CyanaMRParser import CyanaMRParser
    from wwpdb.utils.nmr.mr.CyanaMRParserListener import CyanaMRParserListener
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (coordAssemblyChecker,
                                                       MAX_ERROR_REPORT,
                                                       REPRESENTATIVE_MODEL_ID)
    from wwpdb.utils.nmr.io.CifReader import CifReader
    from wwpdb.utils.nmr.ChemCompUtil import ChemCompUtil
    from wwpdb.utils.nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from wwpdb.utils.nmr.NEFTranslator.NEFTranslator import NEFTranslator
except ImportError:
    from nmr.mr.LexerErrorListener import LexerErrorListener
    from nmr.mr.ParserErrorListener import ParserErrorListener
    from nmr.mr.CyanaMRLexer import CyanaMRLexer
    from nmr.mr.CyanaMRParser import CyanaMRParser
    from nmr.mr.CyanaMRParserListener import CyanaMRParserListener
    from nmr.mr.ParserListenerUtil import (coordAssemblyChecker,
                                           MAX_ERROR_REPORT,
                                           REPRESENTATIVE_MODEL_ID)
    from nmr.io.CifReader import CifReader
    from nmr.ChemCompUtil import ChemCompUtil
    from nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from nmr.NEFTranslator.NEFTranslator import NEFTranslator


class CyanaMRReader:
    """ Accessor methods for parsing CYANA MR files.
    """

    def __init__(self, verbose=True, log=sys.stdout,
                 representativeModelId=REPRESENTATIVE_MODEL_ID,
                 mrAtomNameMapping=None,
                 cR=None, caC=None, ccU=None, csStat=None, nefT=None,
                 reasons=None, upl_or_lol=None, file_ext=None):
        self.__verbose = verbose
        self.__lfh = log
        self.__debug = False
        self.__remediate = False
        self.__sll_pred = False

        self.__maxLexerErrorReport = MAX_ERROR_REPORT
        self.__maxParserErrorReport = MAX_ERROR_REPORT

        self.__representativeModelId = representativeModelId
        self.__mrAtomNameMapping = mrAtomNameMapping

        if cR is not None and caC is None:
            caC = coordAssemblyChecker(verbose, log, representativeModelId, cR, None, None, fullCheck=False)

        self.__cR = cR
        self.__caC = caC

        # CCD accessing utility
        self.__ccU = ChemCompUtil(verbose, log) if ccU is None else ccU

        # BMRB chemical shift statistics
        self.__csStat = BMRBChemShiftStat(verbose, log, self.__ccU) if csStat is None else csStat

        # NEFTranslator
        self.__nefT = NEFTranslator(verbose, log, self.__ccU, self.__csStat) if nefT is None else nefT

        # reasons for re-parsing request from the previous trial
        self.__reasons = reasons

        self.__upl_or_lol = upl_or_lol

        self.__file_ext = file_ext

    def setDebugMode(self, debug):
        self.__debug = debug

    def setRemediateMode(self, remediate):
        self.__remediate = remediate

    def setLexerMaxErrorReport(self, maxErrReport):
        self.__maxLexerErrorReport = maxErrReport

    def setParserMaxErrorReport(self, maxErrReport):
        self.__maxParserErrorReport = maxErrReport

    def setSllPredMode(self, ssl_pred):
        self.__sll_pred = ssl_pred

    def parse(self, mrFilePath, cifFilePath=None, isFilePath=True,
              createSfDict=False, originalFileName=None, listIdCounter=None, entryId=None):
        """ Parse CYANA MR file.
            @return: CyanaMRParserListener for success or None otherwise, ParserErrorListener, LexerErrorListener.
        """

        ifh = None

        try:

            if isFilePath:
                mrString = None

                if not os.access(mrFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"CyanaMRReader.parse() {mrFilePath} is not accessible.\n")
                    return None, None, None

                ifh = open(mrFilePath, 'r')  # pylint: disable=consider-using-with
                input = InputStream(ifh.read())

            else:
                mrFilePath, mrString = None, mrFilePath

                if mrString is None or len(mrString) == 0:
                    if self.__verbose:
                        self.__lfh.write("CyanaMRReader.parse() Empty string.\n")
                    return None, None, None

                input = InputStream(mrString)

            if cifFilePath is not None:
                if not os.access(cifFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"CyanaMRReader.parse() {cifFilePath} is not accessible.\n")
                    return None, None, None

                if self.__cR is None:
                    self.__cR = CifReader(self.__verbose, self.__lfh)
                    if not self.__cR.parse(cifFilePath):
                        return None, None, None

            lexer = CyanaMRLexer(input)
            lexer.removeErrorListeners()

            lexer_error_listener = LexerErrorListener(mrFilePath, maxErrorReport=self.__maxLexerErrorReport)
            lexer.addErrorListener(lexer_error_listener)

            messageList = lexer_error_listener.getMessageList()

            if messageList is not None and self.__verbose:
                for description in messageList:
                    self.__lfh.write(f"[Syntax error] line {description['line_number']}:{description['column_position']} {description['message']}\n")
                    if 'input' in description:
                        self.__lfh.write(f"{description['input']}\n")
                        self.__lfh.write(f"{description['marker']}\n")

            stream = CommonTokenStream(lexer)
            parser = CyanaMRParser(stream)
            if not isFilePath or self.__sll_pred:
                parser._interp.predictionMode = PredictionMode.SLL  # pylint: disable=protected-access
            parser.removeErrorListeners()
            parser_error_listener = ParserErrorListener(mrFilePath, maxErrorReport=self.__maxParserErrorReport)
            parser.addErrorListener(parser_error_listener)
            tree = parser.cyana_mr()

            walker = ParseTreeWalker()
            listener = CyanaMRParserListener(self.__verbose, self.__lfh,
                                             self.__representativeModelId,
                                             self.__mrAtomNameMapping,
                                             self.__cR, self.__caC,
                                             self.__ccU, self.__csStat, self.__nefT,
                                             self.__reasons, self.__upl_or_lol, self.__file_ext)
            listener.setDebugMode(self.__debug)
            listener.setRemediateMode(self.__remediate)
            listener.createSfDict(createSfDict)
            if createSfDict:
                if originalFileName is not None:
                    listener.setOriginaFileName(originalFileName)
                if listIdCounter is not None:
                    listener.setListIdCounter(listIdCounter)
                if entryId is not None:
                    listener.setEntryId(entryId)
            walker.walk(listener, tree)

            messageList = parser_error_listener.getMessageList()

            if messageList is not None and self.__verbose:
                for description in messageList:
                    self.__lfh.write(f"[Syntax error] line {description['line_number']}:{description['column_position']} {description['message']}\n")
                    if 'input' in description:
                        self.__lfh.write(f"{description['input']}\n")
                        self.__lfh.write(f"{description['marker']}\n")

            if self.__verbose:
                if listener.warningMessage is not None and len(listener.warningMessage) > 0:
                    print('\n'.join(listener.warningMessage))
                if isFilePath:
                    print(listener.getContentSubtype())

            return listener, parser_error_listener, lexer_error_listener

        except IOError as e:
            if self.__verbose:
                self.__lfh.write(f"+CyanaMRReader.parse() ++ Error - {str(e)}\n")
            return None, None, None
            # pylint: disable=unreachable
            """ debug code
        except Exception as e:
            if self.__verbose and isFilePath:
                self.__lfh.write(f"+CyanaMRReader.parse() ++ Error - {mrFilePath!r} - {str(e)}\n")
            return None, None, None
            """
        finally:
            if isFilePath and ifh is not None:
                ifh.close()


if __name__ == "__main__":
    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2lk5/test.mr',
                 '../../tests-nmr/mock-data-remediation/2lk5/2lk5.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2m6i/2m6i-corrected-div_dst-div_dst-div_dst-div_dst.mr',
                 '../../tests-nmr/mock-data-remediation/2m6i/2m6i.cif')

    reader = CyanaMRReader(False)
    reader.setDebugMode(False)
    reader_listener, _, _ =\
        reader.parse('../../tests-nmr/mock-data-remediation/2lrr/2lrr-trimmed.mr',
                     '../../tests-nmr/mock-data-remediation/2lrr/2lrr.cif')
    reader = CyanaMRReader(True, reasons=reader_listener.getReasonsForReparsing())
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2lrr/2lrr-trimmed.mr',
                 '../../tests-nmr/mock-data-remediation/2lrr/2lrr.cif')
    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2kym/2kym-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/2kym/2kym.cif')

    reader = CyanaMRReader(True, file_ext='upv')
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5mcs/omcf_omcf320R.upv',
                 '../../tests-nmr/mock-data-remediation/5mcs/5mcs.cif', originalFileName='omcf_omcf320R.upv')

    reader = CyanaMRReader(True, file_ext='upl')
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5ue2/pro_csp_28dec16.upl',
                 '../../tests-nmr/mock-data-remediation/5ue2/5ue2.cif', originalFileName='pro_csp_28dec16.upl')

    reader = CyanaMRReader(True, file_ext='upl')
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5ue2/pro_mutations_28dec16.upl',
                 '../../tests-nmr/mock-data-remediation/5ue2/5ue2.cif', originalFileName='pro_mutations_28dec16.upl')

    reader = CyanaMRReader(True, file_ext='upl')
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5ue2/methyl_NOEs.upl',
                 '../../tests-nmr/mock-data-remediation/5ue2/5ue2.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5ue2/2_dp8_dihre.aco-corrected',
                 '../../tests-nmr/mock-data-remediation/5ue2/5ue2.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2rrn/2rrn-trimmed-div_src.mr',
                 '../../tests-nmr/mock-data-remediation/2rrn/2rrn.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/6cgh/deposit.rdc',
                 '../../tests-nmr/mock-data-remediation/6cgh/6cgh.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2m5b/2m5b-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/2m5b/2m5b.cif')

    reader = CyanaMRReader(False)
    reader.setDebugMode(False)
    reader_listener, _, _ = reader.parse('../../tests-nmr/mock-data-remediation/5ue2/pro_protect_28dec16.upl',
                                         '../../tests-nmr/mock-data-remediation/5ue2/5ue2.cif')
    reader = CyanaMRReader(True, reasons=reader_listener.getReasonsForReparsing())
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5ue2/pro_protect_28dec16.upl',
                 '../../tests-nmr/mock-data-remediation/5ue2/5ue2.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2lxn/test.mr',
                 '../../tests-nmr/mock-data-remediation/2lxn/2lxn.cif')

    reader = CyanaMRReader(False)
    reader.setDebugMode(False)
    reader_listener, _, _ =\
        reader.parse('../../tests-nmr/mock-data-remediation/7sa5/D_1000259911_mr_P4.cyana.V1',
                     '../../tests-nmr/mock-data-remediation/7sa5/7sa5.cif')
    reader = CyanaMRReader(True, reasons=reader_listener.getReasonsForReparsing())
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/7sa5/D_1000259911_mr_P4.cyana.V1',
                 '../../tests-nmr/mock-data-remediation/7sa5/7sa5.cif')

    reader = CyanaMRReader(False)
    reader.setDebugMode(False)
    reader_listener, _, _ =\
        reader.parse('../../tests-nmr/mock-data-remediation/2lum/2lum-corrected.mr',
                     '../../tests-nmr/mock-data-remediation/2lum/2lum.cif')
    reader = CyanaMRReader(True, reasons=reader_listener.getReasonsForReparsing())
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2lum/2lum-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/2lum/2lum.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/7en4/deposit.rdc',
                 '../../tests-nmr/mock-data-remediation/7en4/7en4.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5knw/hbond_nmrstar.txt-corrected',
                 '../../tests-nmr/mock-data-remediation/5knw/5knw.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2mls/2mls-corrected-div_dst-div_dst.mr',
                 '../../tests-nmr/mock-data-remediation/2mls/2mls.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/7f7n/dis.upl_map',
                 '../../tests-nmr/mock-data-remediation/7f7n/7f7n.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2jrl/2jrl-corrected-div_src.mr',
                 '../../tests-nmr/mock-data-remediation/2jrl/2jrl.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2m5v/test_concat.mr',
                 '../../tests-nmr/mock-data-remediation/2m5v/2m5v.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2llp/test_multichain_noe.mr',
                 '../../tests-nmr/mock-data-remediation/2llp/2llp.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5ujn/K27_both_RDC_for_armor_b72_edited.txt-corrected',
                 '../../tests-nmr/mock-data-remediation/5ujn/5ujn.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/6kh9/18hrs_revised_4.dist.upl-corrected',
                 '../../tests-nmr/mock-data-remediation/6kh9/6kh9.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2lj5/2lj5-trimmed.mr',
                 '../../tests-nmr/mock-data-remediation/2lj5/2lj5.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2mk3/rdc_test.mr',
                 '../../tests-nmr/mock-data-remediation/2mk3/2mk3.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/7acb/7acb-trimmed.mr',
                 '../../tests-nmr/mock-data-remediation/7acb/7acb.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/D_1300028390_mr-upload_P1.cyana.V1',
                 '../../tests-nmr/mock-data-daother-7690/D_1300028390_model-annotate_P1.cif.V2')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/D_1300022821_mr-upload_P2.cyana.V1',
                 '../../tests-nmr/mock-data-daother-7690/D_1300022821_model-annotate_P1.cif.V1')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/D_1300024364_mr-upload_P1.cyana.V2',
                 '../../tests-nmr/mock-data-daother-7690/D_1300024364_model-release_P1.cif.V1')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-6830/2nd_test/cyana_rdc_restraints_exmaple',
                 '../../tests-nmr/mock-data-daother-6830/2nd_test/D_800411_model_P1.cif.V1')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-6830/2nd_test/cyana_dihed_restraints_exmaple',
                 '../../tests-nmr/mock-data-daother-6830/2nd_test/D_800411_model_P1.cif.V1')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-5829/D_1000249951_mr-upload_P1.cyana.V1',
                 '../../tests-nmr/mock-data-daother-5829/D_800467_model_P1.cif.V3')
