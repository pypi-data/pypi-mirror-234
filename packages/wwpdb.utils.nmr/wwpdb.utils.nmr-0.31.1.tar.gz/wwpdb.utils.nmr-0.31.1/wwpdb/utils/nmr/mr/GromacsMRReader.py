##
# GromacsMRReader.py
#
# Update:
##
""" A collection of classes for parsing GROMACS MR files.
"""
import sys
import os

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, PredictionMode

try:
    from wwpdb.utils.nmr.mr.LexerErrorListener import LexerErrorListener
    from wwpdb.utils.nmr.mr.ParserErrorListener import ParserErrorListener
    from wwpdb.utils.nmr.mr.GromacsMRLexer import GromacsMRLexer
    from wwpdb.utils.nmr.mr.GromacsMRParser import GromacsMRParser
    from wwpdb.utils.nmr.mr.GromacsMRParserListener import GromacsMRParserListener
    from wwpdb.utils.nmr.mr.GromacsPTReader import GromacsPTReader
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
    from nmr.mr.GromacsMRLexer import GromacsMRLexer
    from nmr.mr.GromacsMRParser import GromacsMRParser
    from nmr.mr.GromacsMRParserListener import GromacsMRParserListener
    from nmr.mr.GromacsPTReader import GromacsPTReader
    from nmr.mr.ParserListenerUtil import (coordAssemblyChecker,
                                           MAX_ERROR_REPORT,
                                           REPRESENTATIVE_MODEL_ID)
    from nmr.io.CifReader import CifReader
    from nmr.ChemCompUtil import ChemCompUtil
    from nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from nmr.NEFTranslator.NEFTranslator import NEFTranslator


class GromacsMRReader:
    """ Accessor methods for parsing GROMACS MR files.
    """

    def __init__(self, verbose=True, log=sys.stdout,
                 representativeModelId=REPRESENTATIVE_MODEL_ID,
                 mrAtomNameMapping=None,
                 cR=None, caC=None, ccU=None, csStat=None, nefT=None,
                 atomNumberDict=None):
        self.__verbose = verbose
        self.__lfh = log
        self.__debug = False

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

        # GromacsPTParserListener.getAtomNumberDict()
        self.__atomNumberDict = atomNumberDict

    def setDebugMode(self, debug):
        self.__debug = debug

    def setLexerMaxErrorReport(self, maxErrReport):
        self.__maxLexerErrorReport = maxErrReport

    def setParserMaxErrorReport(self, maxErrReport):
        self.__maxParserErrorReport = maxErrReport

    def parse(self, mrFilePath, cifFilePath=None, ptFilePath=None, isFilePath=True,
              createSfDict=False, originalFileName=None, listIdCounter=None, entryId=None):
        """ Parse GROMACS MR file.
            @return: GromacsMRParserListener for success or None otherwise, ParserErrorListener, LexerErrorListener.
        """

        ifh = None

        try:

            if isFilePath:
                mrString = None

                if not os.access(mrFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"GromacsMRReader.parse() {mrFilePath} is not accessible.\n")
                    return None, None, None

            else:
                mrFilePath, mrString = None, mrFilePath

                if mrString is None or len(mrString) == 0:
                    if self.__verbose:
                        self.__lfh.write("GromacsMRReader.parse() Empty string.\n")
                    return None, None, None

            if cifFilePath is not None:
                if not os.access(cifFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"GromacsMRReader.parse() {cifFilePath} is not accessible.\n")
                    return None, None, None

                if self.__cR is None:
                    self.__cR = CifReader(self.__verbose, self.__lfh)
                    if not self.__cR.parse(cifFilePath):
                        return None, None, None

            if ptFilePath is not None and self.__atomNumberDict is None:
                ptR = GromacsPTReader(self.__verbose, self.__lfh,
                                      self.__representativeModelId,
                                      self.__mrAtomNameMapping,
                                      self.__cR, self.__caC,
                                      self.__ccU, self.__csStat, self.__nefT)
                ptPL, _, _ = ptR.parse(ptFilePath, cifFilePath)
                if ptPL is not None:
                    self.__atomNumberDict = ptPL.getAtomNumberDict()

            if isFilePath:
                ifh = open(mrFilePath, 'r')  # pylint: disable=consider-using-with
                input = InputStream(ifh.read())
            else:
                input = InputStream(mrString)

            lexer = GromacsMRLexer(input)
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
            parser = GromacsMRParser(stream)
            # try with simpler/faster SLL prediction mode
            parser._interp.predictionMode = PredictionMode.SLL  # pylint: disable=protected-access
            parser.removeErrorListeners()
            parser_error_listener = ParserErrorListener(mrFilePath, maxErrorReport=self.__maxParserErrorReport)
            parser.addErrorListener(parser_error_listener)
            tree = parser.gromacs_mr()

            walker = ParseTreeWalker()
            listener = GromacsMRParserListener(self.__verbose, self.__lfh,
                                               self.__representativeModelId,
                                               self.__mrAtomNameMapping,
                                               self.__cR, self.__caC,
                                               self.__ccU, self.__csStat, self.__nefT,
                                               self.__atomNumberDict)
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

            if isFilePath and ifh is not None:
                ifh.close()

            return listener, parser_error_listener, lexer_error_listener

        except IOError as e:
            if self.__verbose:
                self.__lfh.write(f"+GromacsMRReader.parse() ++ Error - {str(e)}\n")
            return None, None, None
            # pylint: disable=unreachable
            """ debug code
        except Exception as e:
            if self.__verbose and isFilePath:
                self.__lfh.write(f"+GromacsMRReader.parse() ++ Error - {mrFilePath!r} - {str(e)}\n")
            return None, None, None
            """
        finally:
            if isFilePath and ifh is not None:
                ifh.close()


if __name__ == "__main__":
    reader = GromacsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2mzi/2mzi-trimmed-div_src.mr',
                 '../../tests-nmr/mock-data-remediation/2mzi/2mzi.cif',
                 '../../tests-nmr/mock-data-remediation/2mzi/2mzi-trimmed-div_dst.mr')

    reader = GromacsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/6v5d/gromacs_orientation_restraints.itp',
                 '../../tests-nmr/mock-data-remediation/6v5d/6v5d.cif')

    reader = GromacsMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2mzh/2mzh.rst',
                 '../../tests-nmr/mock-data-remediation/2mzh/2mzh.cif',
                 '../../tests-nmr/mock-data-remediation/2mzh/2mzh.top')
