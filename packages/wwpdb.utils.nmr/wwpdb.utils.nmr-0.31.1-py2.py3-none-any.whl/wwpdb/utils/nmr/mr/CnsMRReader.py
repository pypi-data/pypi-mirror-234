##
# CnsMRReader.py
#
# Update:
##
""" A collection of classes for parsing CNS MR files.
"""
import sys
import os

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, PredictionMode

try:
    from wwpdb.utils.nmr.mr.LexerErrorListener import LexerErrorListener
    from wwpdb.utils.nmr.mr.ParserErrorListener import ParserErrorListener
    from wwpdb.utils.nmr.mr.CnsMRLexer import CnsMRLexer
    from wwpdb.utils.nmr.mr.CnsMRParser import CnsMRParser
    from wwpdb.utils.nmr.mr.CnsMRParserListener import CnsMRParserListener
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
    from nmr.mr.CnsMRLexer import CnsMRLexer
    from nmr.mr.CnsMRParser import CnsMRParser
    from nmr.mr.CnsMRParserListener import CnsMRParserListener
    from nmr.mr.ParserListenerUtil import (coordAssemblyChecker,
                                           MAX_ERROR_REPORT,
                                           REPRESENTATIVE_MODEL_ID)
    from nmr.io.CifReader import CifReader
    from nmr.ChemCompUtil import ChemCompUtil
    from nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from nmr.NEFTranslator.NEFTranslator import NEFTranslator


class CnsMRReader:
    """ Accessor methods for parsing CNS MR files.
    """

    def __init__(self, verbose=True, log=sys.stdout,
                 representativeModelId=REPRESENTATIVE_MODEL_ID,
                 mrAtomNameMapping=None,
                 cR=None, caC=None, ccU=None, csStat=None, nefT=None,
                 reasons=None):
        self.__verbose = verbose
        self.__lfh = log
        self.__debug = False
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

    def setLexerMaxErrorReport(self, maxErrReport):
        self.__maxLexerErrorReport = maxErrReport

    def setParserMaxErrorReport(self, maxErrReport):
        self.__maxParserErrorReport = maxErrReport

    def setSllPredMode(self, ssl_pred):
        self.__sll_pred = ssl_pred

    def parse(self, mrFilePath, cifFilePath=None, isFilePath=True,
              createSfDict=False, originalFileName=None, listIdCounter=None, entryId=None):
        """ Parse CNS MR file.
            @return: CnsMRParserListener for success or None otherwise, ParserErrorListener, LexerErrorListener.
        """

        ifh = None

        try:

            if isFilePath:
                mrString = None

                if not os.access(mrFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"CnsMRReader.parse() {mrFilePath} is not accessible.\n")
                    return None, None, None

                ifh = open(mrFilePath, 'r')  # pylint: disable=consider-using-with
                input = InputStream(ifh.read())

            else:
                mrFilePath, mrString = None, mrFilePath

                if mrString is None or len(mrString) == 0:
                    if self.__verbose:
                        self.__lfh.write("CnsMRReader.parse() Empty string.\n")
                    return None, None, None

                input = InputStream(mrString)

            if cifFilePath is not None:
                if not os.access(cifFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"CnsMRReader.parse() {cifFilePath} is not accessible.\n")
                    return None, None, None

                if self.__cR is None:
                    self.__cR = CifReader(self.__verbose, self.__lfh)
                    if not self.__cR.parse(cifFilePath):
                        return None, None, None

            lexer = CnsMRLexer(input)
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
            parser = CnsMRParser(stream)
            if not isFilePath or self.__sll_pred:
                parser._interp.predictionMode = PredictionMode.SLL  # pylint: disable=protected-access
            parser.removeErrorListeners()
            parser_error_listener = ParserErrorListener(mrFilePath, maxErrorReport=self.__maxParserErrorReport)
            parser.addErrorListener(parser_error_listener)
            tree = parser.cns_mr()

            walker = ParseTreeWalker()
            listener = CnsMRParserListener(self.__verbose, self.__lfh,
                                           self.__representativeModelId,
                                           self.__mrAtomNameMapping,
                                           self.__cR, self.__caC,
                                           self.__ccU, self.__csStat, self.__nefT,
                                           self.__reasons)
            listener.setDebugMode(self.__debug)
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
                self.__lfh.write(f"+CnsMRReader.parse() ++ Error - {str(e)}\n")
            return None, None, None
            # pylint: disable=unreachable
            """ debug code
        except Exception as e:
            if self.__verbose and isFilePath:
                self.__lfh.write(f"+CnsMRReader.parse() ++ Error - {mrFilePath!r} - {str(e)}\n")
            return None, None, None
            """
        finally:
            if isFilePath and ifh is not None:
                ifh.close()


if __name__ == "__main__":
    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2mlb/test.mr',
                 '../../tests-nmr/mock-data-remediation/2mlb/2mlb.cif')

    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2ltq/2ltq-corrected-div_src.mr',
                 '../../tests-nmr/mock-data-remediation/2ltq/2ltq.cif')

    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-combine-at-upload/bmr36473/data/D_1300028046_mr-upload_P2.cns.V1',
                 '../../tests-nmr/mock-data-combine-at-upload/bmr36473/data/D_1300028046_model-annotate_P1.cif.V2')

    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2mf8/2mf8-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/2mf8/2mf8.cif')

    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7969/dna2_used.tbl',
                 '../../tests-nmr/mock-data-daother-7969/D_800478_model_P1.cif.V3')

    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/6ijw/D_1300008256_mr_P1.cyana.V1-corrected',
                 '../../tests-nmr/mock-data-remediation/6ijw/6ijw.cif')

    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/6uck/noe.tbl-corrected',
                 '../../tests-nmr/mock-data-remediation/6uck/6uck.cif')

    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2m10/2m10-trimmed.mr',
                 '../../tests-nmr/mock-data-remediation/2m10/2m10.cif')

    reader = CnsMRReader(False)
    reader.setDebugMode(False)
    reader_listener, _, _ =\
        reader.parse('../../tests-nmr/mock-data-remediation/1iio/1iio-trimmed.mr',
                     '../../tests-nmr/mock-data-remediation/1iio/1iio.cif')
    reader = CnsMRReader(True, reasons=reader_listener.getReasonsForReparsing())
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/1iio/1iio-trimmed.mr',
                 '../../tests-nmr/mock-data-remediation/1iio/1iio.cif')

    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2jrl/2jrl-corrected-div_dst-div_src.mr',
                 '../../tests-nmr/mock-data-remediation/2jrl/2jrl.cif')

    reader = CnsMRReader(False)
    reader.setDebugMode(False)
    reader_listener, _, _ =\
        reader.parse('../../tests-nmr/mock-data-remediation/2b87/2b87-corrected.mr',
                     '../../tests-nmr/mock-data-remediation/2b87/2b87.cif')
    reader = CnsMRReader(True, reasons=reader_listener.getReasonsForReparsing())
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2b87/2b87-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/2b87/2b87.cif')

    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2lhz/2lhz-corrected.mr',
                 '../../tests-nmr/mock-data-remediation/2lhz/2lhz.cif')

    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/6th8/hbond_patches.tbl',
                 '../../tests-nmr/mock-data-remediation/6th8/6th8.cif')

    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/4by9/4by9-trimmed.mr',
                 '../../tests-nmr/mock-data-remediation/4by9/4by9.cif')

    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/D_1300022442_mr-upload_P1.cns.V1',
                 '../../tests-nmr/mock-data-daother-7690/D_1300022442_model-annotate_P1.cif.V1')

    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/D_1300019843_mr-upload_P1.cns.V1',
                 '../../tests-nmr/mock-data-daother-7690/D_1300019843_model-annotate_P1.cif.V1')

    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-pdbstat/D_1000243168_mr-upload_P8.xplor-nih.V1',
                 '../../tests-nmr/mock-data-pdbstat/6pvr.cif')

    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-pdbstat/D_1000243168_mr-upload_P2.xplor-nih.V1',
                 '../../tests-nmr/mock-data-pdbstat/6pvr.cif')

    reader = CnsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-pdbstat/atom_sel_expr_example.txt',
                 '../../tests-nmr/mock-data-pdbstat/6pvr.cif')
