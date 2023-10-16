##
# XplorMRReader.py
#
# Update:
##
""" A collection of classes for parsing XPLOR-NIH MR files.
"""
import sys
import os

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, PredictionMode

try:
    from wwpdb.utils.nmr.mr.LexerErrorListener import LexerErrorListener
    from wwpdb.utils.nmr.mr.ParserErrorListener import ParserErrorListener
    from wwpdb.utils.nmr.mr.XplorMRLexer import XplorMRLexer
    from wwpdb.utils.nmr.mr.XplorMRParser import XplorMRParser
    from wwpdb.utils.nmr.mr.XplorMRParserListener import XplorMRParserListener
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
    from nmr.mr.XplorMRLexer import XplorMRLexer
    from nmr.mr.XplorMRParser import XplorMRParser
    from nmr.mr.XplorMRParserListener import XplorMRParserListener
    from nmr.mr.ParserListenerUtil import (coordAssemblyChecker,
                                           MAX_ERROR_REPORT,
                                           REPRESENTATIVE_MODEL_ID)
    from nmr.io.CifReader import CifReader
    from nmr.ChemCompUtil import ChemCompUtil
    from nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from nmr.NEFTranslator.NEFTranslator import NEFTranslator


class XplorMRReader:
    """ Accessor methods for parsing XPLOR-NIH MR files.
    """

    def __init__(self, verbose=True, log=sys.stdout,
                 representativeModelId=REPRESENTATIVE_MODEL_ID,
                 mrAtomNameMapping=None,
                 cR=None, caC=None, ccU=None, csStat=None, nefT=None,
                 reasons=None):
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
        """ Parse XPLOR-NIH MR file.
            @return: XplorMRParserListener for success or None otherwise, ParserErrorListener, LexerErrorListener.
        """

        ifh = None

        try:

            if isFilePath:
                mrString = None

                if not os.access(mrFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"XplorMRReader.parse() {mrFilePath} is not accessible.\n")
                    return None, None, None

                ifh = open(mrFilePath, 'r')  # pylint: disable=consider-using-with
                input = InputStream(ifh.read())

            else:
                mrFilePath, mrString = None, mrFilePath

                if mrString is None or len(mrString) == 0:
                    if self.__verbose:
                        self.__lfh.write("XplorMRReader.parse() Empty string.\n")
                    return None, None, None

                input = InputStream(mrString)

            if cifFilePath is not None:
                if not os.access(cifFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"XplorMRReader.parse() {cifFilePath} is not accessible.\n")
                    return None, None, None

                if self.__cR is None:
                    self.__cR = CifReader(self.__verbose, self.__lfh)
                    if not self.__cR.parse(cifFilePath):
                        return None, None, None

            lexer = XplorMRLexer(input)
            lexer.removeErrorListeners()

            lexer_error_listener = LexerErrorListener(mrFilePath, inputString=mrString, maxErrorReport=self.__maxLexerErrorReport)
            lexer.addErrorListener(lexer_error_listener)

            messageList = lexer_error_listener.getMessageList()

            if messageList is not None and self.__verbose:
                for description in messageList:
                    self.__lfh.write(f"[Syntax error] line {description['line_number']}:{description['column_position']} {description['message']}\n")
                    if 'input' in description:
                        self.__lfh.write(f"{description['input']}\n")
                        self.__lfh.write(f"{description['marker']}\n")

            stream = CommonTokenStream(lexer)
            parser = XplorMRParser(stream)
            if not isFilePath or self.__sll_pred:
                parser._interp.predictionMode = PredictionMode.SLL  # pylint: disable=protected-access
            parser.removeErrorListeners()
            parser_error_listener = ParserErrorListener(mrFilePath, inputString=mrString, maxErrorReport=self.__maxParserErrorReport)
            parser.addErrorListener(parser_error_listener)
            tree = parser.xplor_nih_mr()

            walker = ParseTreeWalker()
            listener = XplorMRParserListener(self.__verbose, self.__lfh,
                                             self.__representativeModelId,
                                             self.__mrAtomNameMapping,
                                             self.__cR, self.__caC,
                                             self.__ccU, self.__csStat, self.__nefT,
                                             self.__reasons)
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
                self.__lfh.write(f"+XplorMRReader.parse() ++ Error - {str(e)}\n")
            return None, None, None
            # pylint: disable=unreachable
            """ debug code
        except Exception as e:
            if self.__verbose and isFilePath:
                self.__lfh.write(f"+XplorMRReader.parse() ++ Error - {mrFilePath!r} - {str(e)}\n")
            return None, None, None
            """
        finally:
            if isFilePath and ifh is not None:
                ifh.close()


if __name__ == "__main__":
    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-combine-at-upload/bmr21102/sms21102/AmBErg_CC_restraints_PAR12p6ms.tbl',
                 '../../tests-nmr/mock-data-combine-at-upload/bmr21102/sms21102/sms21102.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-combine-at-upload/bmr21100/sms21100/Ambig.tbl',
                 '../../tests-nmr/mock-data-combine-at-upload/bmr21100/sms21100/sms21100.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader_listener, _, _ =\
        reader.parse('../../tests-nmr/mock-data-daother-8580/newupload_2/D_1000274286_mr_P3.xplor-nih.V1',
                     '../../tests-nmr/mock-data-daother-8580/newupload_2/D_1000274286_model_P1.cif.V1')
    reader = XplorMRReader(True, reasons=reader_listener.getReasonsForReparsing())
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-8580/newupload_2/D_1000274286_mr_P3.xplor-nih.V1',
                 '../../tests-nmr/mock-data-daother-8580/newupload_2/D_1000274286_model_P1.cif.V1')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2mjb/2mjb-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/2mjb/2mjb.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2l94/2l94-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/2l94/2l94.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5t1o/PCS_HN_EIN.tbl-corrected',
                 '../../tests-nmr/mock-data-remediation/5t1o/5t1o.cif')

    reader = XplorMRReader(False)
    reader.setDebugMode(False)
    reader_listener, _, _ =\
        reader.parse('../../tests-nmr/mock-data-remediation/2n8l/2n8l-corrected.mr',
                     '../../tests-nmr/mock-data-remediation/2n8l/2n8l.cif')
    reader = XplorMRReader(True, reasons=reader_listener.getReasonsForReparsing())
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2n8l/2n8l-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/2n8l/2n8l.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/6th8/allnoe.tbl-corrected',
                 '../../tests-nmr/mock-data-remediation/6th8/6th8.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2mjk/2mjk-trimmed.mr',
                 '../../tests-nmr/mock-data-remediation/2mjk/2mjk.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/6cch/6cch-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/6cch/6cch.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2lrk/2lrk-corrected-div_src.mr',
                 '../../tests-nmr/mock-data-remediation/2lrk/2lrk.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2mk3/2mk3-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/2mk3/2mk3.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5xbo/Tb_UBA1_PCS_correct_50p.tbl-corrected',
                 '../../tests-nmr/mock-data-remediation/5xbo/5xbo.cif')

    reader = XplorMRReader(False)
    reader.setDebugMode(False)
    reader_listener, _, _ =\
        reader.parse('../../tests-nmr/mock-data-remediation/2k31/2k31-corrected.mr',
                     '../../tests-nmr/mock-data-remediation/2k31/2k31.cif')

    reader = XplorMRReader(True, reasons=reader_listener.getReasonsForReparsing())
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2k31/2k31-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/2k31/2k31.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2lrk/2lrk-corrected-div_src.mr',
                 '../../tests-nmr/mock-data-remediation/2lrk/2lrk.cif')

    reader = XplorMRReader(False)
    reader.setDebugMode(False)
    reader_listener, _, _ =\
        reader.parse('../../tests-nmr/mock-data-remediation/1iio/1iio-trimmed.mr',
                     '../../tests-nmr/mock-data-remediation/1iio/1iio.cif')
    reader = XplorMRReader(True, reasons=reader_listener.getReasonsForReparsing())
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/1iio/1iio-trimmed.mr',
                 '../../tests-nmr/mock-data-remediation/1iio/1iio.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2m3g/2m3g-trimmed.mr',
                 '../../tests-nmr/mock-data-remediation/2m3g/2m3g.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/7n7e/distance.xplor',
                 '../../tests-nmr/mock-data-remediation/7n7e/7n7e.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2ju5/2ju5-trimmed-div_src.mr-corrected',
                 '../../tests-nmr/mock-data-remediation/2ju5/2ju5.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/6x63/deposit_All_Unamb_MD_xplorFormat_fixNomen.txt',
                 '../../tests-nmr/mock-data-remediation/6x63/6x63.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2laj/2laj-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/2laj/2laj.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5kqj/ANT2_hbond_restraint.tbl',
                 '../../tests-nmr/mock-data-remediation/5kqj/5kqj.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2l1v/2l1v-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/2l1v/2l1v.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2mcc/2mcc-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/2mcc/2mcc.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/6d53/dangleT.tbl-corrected',
                 '../../tests-nmr/mock-data-remediation/6d53/6d53.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2k2a/2k2a-corrected-div_src.mr',
                 '../../tests-nmr/mock-data-remediation/2k2a/2k2a.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5w3n/fus_CC_RDC.tbl-corrected',
                 '../../tests-nmr/mock-data-remediation/5w3n/5w3n.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5w3n/fus_CO_RDC.tbl-corrected',
                 '../../tests-nmr/mock-data-remediation/5w3n/5w3n.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/6var/HBVe_sPRE.tab-corrected',
                 '../../tests-nmr/mock-data-remediation/6var/6var.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/6l92/G4II_planarity.txt',
                 '../../tests-nmr/mock-data-remediation/6l92/6l92.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5t1o/RDC_NPr.tbl-corrected',
                 '../../tests-nmr/mock-data-remediation/5t1o/5t1o.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/6ud0/pcs_hn_dist_tm_tsg_tsap.tbl-corrected',
                 '../../tests-nmr/mock-data-remediation/6ud0/6ud0.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2l3b/cacb_shift.mr',
                 '../../tests-nmr/mock-data-remediation/2l3b/2l3b.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2kw8/2kw8-trimmed-div_dst-div_src.mr',
                 '../../tests-nmr/mock-data-remediation/2kw8/2kw8.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2bjc/test_no_eff.mr',
                 '../../tests-nmr/mock-data-remediation/2bjc/2bjc.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2bgo/test.mr',
                 '../../tests-nmr/mock-data-remediation/2bgo/2bgo.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5ks5/vean.test',
                 '../../tests-nmr/mock-data-remediation/5ks5/5ks5.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2bjc/test.mr',
                 '../../tests-nmr/mock-data-remediation/2bjc/2bjc.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/4by9/4by9-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/4by9/4by9.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7871/wsh2090_ambig_rev.tbl',
                 '../../tests-nmr/mock-data-daother-7871/D_800473_model_P1.cif.V3')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2n55/test.mr',
                 '../../tests-nmr/mock-data-remediation/2n55/2n55.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2m54/2m54-trimmed.mr',
                 '../../tests-nmr/mock-data-remediation/2m54/2m54.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2n21/2n21-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/2n21/2n21.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/6p6c/pea-15erk2c13shifts_ded.tbl',
                 '../../tests-nmr/mock-data-remediation/6p6c/6p6c.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/6jcd/submit-plane.tbl',
                 '../../tests-nmr/mock-data-remediation/6jcd/6jcd.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/D_1300020446_mr-upload_P5.xplor-nih.V1',
                 '../../tests-nmr/mock-data-daother-7690/D_1300020446_model-release_P1.cif.V2')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/D_1300020646_mr-upload_P1.xplor-nih.V2',
                 '../../tests-nmr/mock-data-daother-7690/D_1300020646_model-annotate_P1.cif.V2')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-pdbstat/D_1000243168_mr-upload_P8.xplor-nih.V1',
                 '../../tests-nmr/mock-data-pdbstat/6pvr.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-pdbstat/D_1000243168_mr-upload_P2.xplor-nih.V1',
                 '../../tests-nmr/mock-data-pdbstat/6pvr.cif')

    reader = XplorMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-pdbstat/atom_sel_expr_example.txt',
                 '../../tests-nmr/mock-data-pdbstat/6pvr.cif')
