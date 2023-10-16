##
# AmberPTReader.py
#
# Update:
##
""" A collection of classes for parsing AMBER PT files.
"""
import sys
import os

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, PredictionMode

try:
    from wwpdb.utils.nmr.mr.LexerErrorListener import LexerErrorListener
    from wwpdb.utils.nmr.mr.ParserErrorListener import ParserErrorListener
    from wwpdb.utils.nmr.mr.AmberPTLexer import AmberPTLexer
    from wwpdb.utils.nmr.mr.AmberPTParser import AmberPTParser
    from wwpdb.utils.nmr.mr.AmberPTParserListener import AmberPTParserListener
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
    from nmr.mr.AmberPTLexer import AmberPTLexer
    from nmr.mr.AmberPTParser import AmberPTParser
    from nmr.mr.AmberPTParserListener import AmberPTParserListener
    from nmr.mr.ParserListenerUtil import (coordAssemblyChecker,
                                           MAX_ERROR_REPORT,
                                           REPRESENTATIVE_MODEL_ID)
    from nmr.io.CifReader import CifReader
    from nmr.ChemCompUtil import ChemCompUtil
    from nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from nmr.NEFTranslator.NEFTranslator import NEFTranslator


class AmberPTReader:
    """ Accessor methods for parsing AMBER PT files.
    """

    def __init__(self, verbose=True, log=sys.stdout,
                 representativeModelId=REPRESENTATIVE_MODEL_ID,
                 mrAtomNameMapping=None,
                 cR=None, caC=None, ccU=None, csStat=None, nefT=None):
        self.__verbose = verbose
        self.__lfh = log

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

    def setLexerMaxErrorReport(self, maxErrReport):
        self.__maxLexerErrorReport = maxErrReport

    def setParserMaxErrorReport(self, maxErrReport):
        self.__maxParserErrorReport = maxErrReport

    def parse(self, ptFilePath, cifFilePath=None, isFilePath=True):
        """ Parse AMBER PT file.
            @return: AmberPTParserListener for success or None otherwise, ParserErrorListener, LexerErrorListener.
        """

        ifh = None

        try:

            if isFilePath:
                ptString = None

                if not os.access(ptFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"AmberPTReader.parse() {ptFilePath} is not accessible.\n")
                    return None, None, None

                ifh = open(ptFilePath, 'r')  # pylint: disable=consider-using-with
                input = InputStream(ifh.read())

            else:
                ptFilePath, ptString = None, ptFilePath

                if ptString is None or len(ptString) == 0:
                    if self.__verbose:
                        self.__lfh.write("AmberPTReader.parse() Empty string.\n")
                    return None, None, None

                input = InputStream(ptString)

            if cifFilePath is not None:
                if not os.access(cifFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"AmberPTReader.parse() {cifFilePath} is not accessible.\n")
                    return None, None, None

                if self.__cR is None:
                    self.__cR = CifReader(self.__verbose, self.__lfh)
                    if not self.__cR.parse(cifFilePath):
                        return None, None, None

            lexer = AmberPTLexer(input)
            lexer.removeErrorListeners()

            lexer_error_listener = LexerErrorListener(ptFilePath, maxErrorReport=self.__maxLexerErrorReport)
            lexer.addErrorListener(lexer_error_listener)

            messageList = lexer_error_listener.getMessageList()

            if messageList is not None and self.__verbose:
                for description in messageList:
                    self.__lfh.write(f"[Syntax error] line {description['line_number']}:{description['column_position']} {description['message']}\n")
                    if 'input' in description:
                        self.__lfh.write(f"{description['input']}\n")
                        self.__lfh.write(f"{description['marker']}\n")

            stream = CommonTokenStream(lexer)
            parser = AmberPTParser(stream)
            # try with simpler/faster SLL prediction mode
            parser._interp.predictionMode = PredictionMode.SLL  # pylint: disable=protected-access
            parser.removeErrorListeners()
            parser_error_listener = ParserErrorListener(ptFilePath, maxErrorReport=self.__maxParserErrorReport)
            parser.addErrorListener(parser_error_listener)
            tree = parser.amber_pt()

            walker = ParseTreeWalker()
            listener = AmberPTParserListener(self.__verbose, self.__lfh,
                                             self.__representativeModelId,
                                             self.__mrAtomNameMapping,
                                             self.__cR, self.__caC,
                                             self.__ccU, self.__csStat, self.__nefT)
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
                self.__lfh.write(f"+AmberPTReader.parse() ++ Error - {str(e)}\n")
            return None, None, None
            # pylint: disable=unreachable
            """ debug code
        except Exception as e:
            if self.__verbose and isFilePath:
                self.__lfh.write(f"+AmberPTReader.parse() ++ Error - {ptFilePath!r} - {str(e)}\n")
            return None, None, None
            """
        finally:
            if isFilePath and ifh is not None:
                ifh.close()


if __name__ == "__main__":
    reader = AmberPTReader(True)
    reader.parse('../../tests-nmr/mock-data-daother-8685/FANA3_0M_ZDNAminwat.prmtop',
                 '../../tests-nmr/mock-data-daother-8685/D_800590_model_P1.cif.V4')

    reader = AmberPTReader(True)
    reader.parse('../../tests-nmr/mock-data-remediation/7b72/ds.prmtop',
                 '../../tests-nmr/mock-data-remediation/7b72/7b72.cif')

    reader = AmberPTReader(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/D_1300028390_mr-upload_P1.dat.V1',
                 '../../tests-nmr/mock-data-daother-7690/D_1300028390_model-annotate_P1.cif.V2')

    reader = AmberPTReader(True)
    reader.parse('../../tests-nmr/mock-data-daother-7421/D_1292118884_mr-upload_P1.dat.V1',
                 '../../tests-nmr/mock-data-daother-7421/D_800450_model_P1.cif.V1')
