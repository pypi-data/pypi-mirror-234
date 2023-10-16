##
# RosettaMRReader.py
#
# Update:
##
""" A collection of classes for parsing ROSETTA MR files.
"""
import sys
import os

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, PredictionMode

try:
    from wwpdb.utils.nmr.mr.LexerErrorListener import LexerErrorListener
    from wwpdb.utils.nmr.mr.ParserErrorListener import ParserErrorListener
    from wwpdb.utils.nmr.mr.RosettaMRLexer import RosettaMRLexer
    from wwpdb.utils.nmr.mr.RosettaMRParser import RosettaMRParser
    from wwpdb.utils.nmr.mr.RosettaMRParserListener import RosettaMRParserListener
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
    from nmr.mr.RosettaMRLexer import RosettaMRLexer
    from nmr.mr.RosettaMRParser import RosettaMRParser
    from nmr.mr.RosettaMRParserListener import RosettaMRParserListener
    from nmr.mr.ParserListenerUtil import (coordAssemblyChecker,
                                           MAX_ERROR_REPORT,
                                           REPRESENTATIVE_MODEL_ID)
    from nmr.io.CifReader import CifReader
    from nmr.ChemCompUtil import ChemCompUtil
    from nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from nmr.NEFTranslator.NEFTranslator import NEFTranslator


class RosettaMRReader:
    """ Accessor methods for parsing ROSETTA MR files.
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

    def parse(self, mrFilePath, cifFilePath=None, isFilePath=True,
              createSfDict=False, originalFileName=None, listIdCounter=None, entryId=None):
        """ Parse ROSETTA MR file.
            @return: RosettaMRParserListener for success or None otherwise, ParserErrorListener, LexerErrorListener.
        """

        ifh = None

        try:

            if isFilePath:
                mrString = None

                if not os.access(mrFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"RosettaMRReader.parse() {mrFilePath} is not accessible.\n")
                    return None, None, None

                ifh = open(mrFilePath, 'r')  # pylint: disable=consider-using-with
                input = InputStream(ifh.read())

            else:
                mrFilePath, mrString = None, mrFilePath

                if mrString is None or len(mrString) == 0:
                    if self.__verbose:
                        self.__lfh.write("RosettaMRReader.parse() Empty string.\n")
                    return None, None, None

                input = InputStream(mrString)

            if cifFilePath is not None:
                if not os.access(cifFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"RosettaMRReader.parse() {cifFilePath} is not accessible.\n")
                    return None, None, None

                if self.__cR is None:
                    self.__cR = CifReader(self.__verbose, self.__lfh)
                    if not self.__cR.parse(cifFilePath):
                        return None, None, None

            lexer = RosettaMRLexer(input)
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
            parser = RosettaMRParser(stream)
            # try with simpler/faster SLL prediction mode
            parser._interp.predictionMode = PredictionMode.SLL  # pylint: disable=protected-access
            parser.removeErrorListeners()
            parser_error_listener = ParserErrorListener(mrFilePath, maxErrorReport=self.__maxParserErrorReport)
            parser.addErrorListener(parser_error_listener)
            tree = parser.rosetta_mr()

            walker = ParseTreeWalker()
            listener = RosettaMRParserListener(self.__verbose, self.__lfh,
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
                self.__lfh.write(f"+RosettaMRReader.parse() ++ Error - {str(e)}\n")
            return None, None, None
            # pylint: disable=unreachable
            """ debug code
        except Exception as e:
            if self.__verbose and isFilePath:
                self.__lfh.write(f"+RosettaMRReader.parse() ++ Error - {mrFilePath!r} - {str(e)}\n")
            return None, None, None
            """
        finally:
            if isFilePath and ifh is not None:
                ifh.close()


if __name__ == "__main__":
    reader = RosettaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-D_80002121177/D_1300034625_mr-upload_P1.rosetta.V1',
                 '../../tests-nmr/mock-data-D_80002121177/D_800517_model_P1.cif.V3')

    reader = RosettaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2m9v/2m9v-trimmed-div_dst.mr',
                 '../../tests-nmr/mock-data-remediation/2m9v/2m9v.cif')

    reader = RosettaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2mme/2mme-trimmed.mr',
                 '../../tests-nmr/mock-data-remediation/2mme/2mme.cif')

    reader = RosettaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/6u3s/NOES_PRES.cst',
                 '../../tests-nmr/mock-data-remediation/6u3s/6u3s.cif')

    reader = RosettaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/rosetta_rdc.test',
                 '../../tests-nmr/mock-data-daother-7690/D_800470_model_P1.cif.V4')

    reader = RosettaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/rosetta_angle.test',
                 '../../tests-nmr/mock-data-daother-7690/D_800470_model_P1.cif.V4')

    reader = RosettaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/rosetta_dist.test',
                 '../../tests-nmr/mock-data-daother-7690/D_800470_model_P1.cif.V4')
