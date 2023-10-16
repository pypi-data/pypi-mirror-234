##
# File: CharmmMRParserListener.py
# Date: 21-Sep-2022
#
# Updates:
""" ParserLister class for CHARMM MR files.
    @author: Masashi Yokochi
"""
import sys
import re
import itertools
import copy
import numpy

from antlr4 import ParseTreeListener
from rmsd.calculate_rmsd import (int_atom, ELEMENT_WEIGHTS)  # noqa: F401 pylint: disable=no-name-in-module, import-error
from operator import itemgetter

try:
    from wwpdb.utils.align.alignlib import PairwiseAlign  # pylint: disable=no-name-in-module
    from wwpdb.utils.nmr.mr.CharmmMRParser import CharmmMRParser
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (toRegEx, toNefEx,
                                                       coordAssemblyChecker,
                                                       extendCoordChainsForExactNoes,
                                                       translateToStdResName,
                                                       translateToStdAtomName,
                                                       isIdenticalRestraint,
                                                       hasInterChainRestraint,
                                                       isAmbigAtomSelection,
                                                       getAltProtonIdInBondConstraint,
                                                       getTypeOfDihedralRestraint,
                                                       isLikePheOrTyr,
                                                       isCyclicPolymer,
                                                       getRestraintName,
                                                       contentSubtypeOf,
                                                       incListIdCounter,
                                                       decListIdCounter,
                                                       getSaveframe,
                                                       getLoop,
                                                       getRow,
                                                       getDistConstraintType,
                                                       getPotentialType,
                                                       REPRESENTATIVE_MODEL_ID,
                                                       MAX_PREF_LABEL_SCHEME_COUNT,
                                                       THRESHHOLD_FOR_CIRCULAR_SHIFT,
                                                       DIST_RESTRAINT_RANGE,
                                                       DIST_RESTRAINT_ERROR,
                                                       ANGLE_RESTRAINT_RANGE,
                                                       ANGLE_RESTRAINT_ERROR,
                                                       DIST_AMBIG_LOW,
                                                       DIST_AMBIG_UP,
                                                       DIST_AMBIG_MED,
                                                       DIST_AMBIG_UNCERT,
                                                       CARTN_DATA_ITEMS,
                                                       AUTH_ATOM_DATA_ITEMS,
                                                       ATOM_NAME_DATA_ITEMS,
                                                       AUTH_ATOM_CARTN_DATA_ITEMS,
                                                       PTNR1_AUTH_ATOM_DATA_ITEMS,
                                                       PTNR2_AUTH_ATOM_DATA_ITEMS)
    from wwpdb.utils.nmr.ChemCompUtil import ChemCompUtil
    from wwpdb.utils.nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from wwpdb.utils.nmr.NEFTranslator.NEFTranslator import NEFTranslator
    from wwpdb.utils.nmr.AlignUtil import (LEN_LARGE_ASYM_ID,
                                           LARGE_ASYM_ID,
                                           monDict3,
                                           protonBeginCode,
                                           aminoProtonCode,
                                           updatePolySeqRst,
                                           sortPolySeqRst,
                                           alignPolymerSequence,
                                           assignPolymerSequence,
                                           trimSequenceAlignment,
                                           retrieveAtomIdentFromMRMap,
                                           retrieveAtomIdFromMRMap,
                                           retrieveRemappedSeqId,
                                           splitPolySeqRstForMultimers,
                                           splitPolySeqRstForExactNoes,
                                           retrieveRemappedChainId,
                                           splitPolySeqRstForNonPoly,
                                           retrieveRemappedNonPoly,
                                           splitPolySeqRstForBranched,
                                           retrieveOriginalSeqIdFromMRMap)
    from wwpdb.utils.nmr.NmrVrptUtility import (to_np_array, distance, dist_error,
                                                angle_target_values, dihedral_angle, angle_error)
except ImportError:
    from nmr.align.alignlib import PairwiseAlign  # pylint: disable=no-name-in-module
    from nmr.mr.CharmmMRParser import CharmmMRParser
    from nmr.mr.ParserListenerUtil import (toRegEx, toNefEx,
                                           coordAssemblyChecker,
                                           extendCoordChainsForExactNoes,
                                           translateToStdResName,
                                           translateToStdAtomName,
                                           isIdenticalRestraint,
                                           hasInterChainRestraint,
                                           isAmbigAtomSelection,
                                           getAltProtonIdInBondConstraint,
                                           getTypeOfDihedralRestraint,
                                           isLikePheOrTyr,
                                           getRestraintName,
                                           isCyclicPolymer,
                                           contentSubtypeOf,
                                           incListIdCounter,
                                           decListIdCounter,
                                           getSaveframe,
                                           getLoop,
                                           getRow,
                                           getDistConstraintType,
                                           getPotentialType,
                                           REPRESENTATIVE_MODEL_ID,
                                           MAX_PREF_LABEL_SCHEME_COUNT,
                                           THRESHHOLD_FOR_CIRCULAR_SHIFT,
                                           DIST_RESTRAINT_RANGE,
                                           DIST_RESTRAINT_ERROR,
                                           ANGLE_RESTRAINT_RANGE,
                                           ANGLE_RESTRAINT_ERROR,
                                           DIST_AMBIG_LOW,
                                           DIST_AMBIG_UP,
                                           DIST_AMBIG_MED,
                                           DIST_AMBIG_UNCERT,
                                           CARTN_DATA_ITEMS,
                                           AUTH_ATOM_DATA_ITEMS,
                                           ATOM_NAME_DATA_ITEMS,
                                           AUTH_ATOM_CARTN_DATA_ITEMS,
                                           PTNR1_AUTH_ATOM_DATA_ITEMS,
                                           PTNR2_AUTH_ATOM_DATA_ITEMS)
    from nmr.ChemCompUtil import ChemCompUtil
    from nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from nmr.NEFTranslator.NEFTranslator import NEFTranslator
    from nmr.AlignUtil import (LEN_LARGE_ASYM_ID,
                               LARGE_ASYM_ID,
                               monDict3,
                               protonBeginCode,
                               aminoProtonCode,
                               updatePolySeqRst,
                               sortPolySeqRst,
                               alignPolymerSequence,
                               assignPolymerSequence,
                               trimSequenceAlignment,
                               retrieveAtomIdentFromMRMap,
                               retrieveAtomIdFromMRMap,
                               retrieveRemappedSeqId,
                               splitPolySeqRstForMultimers,
                               splitPolySeqRstForExactNoes,
                               retrieveRemappedChainId,
                               splitPolySeqRstForNonPoly,
                               retrieveRemappedNonPoly,
                               splitPolySeqRstForBranched,
                               retrieveOriginalSeqIdFromMRMap)
    from nmr.NmrVrptUtility import (to_np_array, distance, dist_error,
                                    angle_target_values, dihedral_angle, angle_error)


DIST_RANGE_MIN = DIST_RESTRAINT_RANGE['min_inclusive']
DIST_RANGE_MAX = DIST_RESTRAINT_RANGE['max_inclusive']

DIST_ERROR_MIN = DIST_RESTRAINT_ERROR['min_exclusive']
DIST_ERROR_MAX = DIST_RESTRAINT_ERROR['max_exclusive']


ANGLE_RANGE_MIN = ANGLE_RESTRAINT_RANGE['min_inclusive']
ANGLE_RANGE_MAX = ANGLE_RESTRAINT_RANGE['max_inclusive']

ANGLE_ERROR_MIN = ANGLE_RESTRAINT_ERROR['min_exclusive']
ANGLE_ERROR_MAX = ANGLE_RESTRAINT_ERROR['max_exclusive']


# This class defines a complete listener for a parse tree produced by CharmmMRParser.
class CharmmMRParserListener(ParseTreeListener):

    __file_type = 'nm-res-cha'

    __verbose = None
    __lfh = None
    __debug = False
    __sel_expr_debug = False

    __createSfDict = False
    __omitDistLimitOutlier = True
    __allowZeroUpperLimit = False
    __correctCircularShift = True

    # @see: https://bmrb.io/ref_info/atom_nom.tbl
    # @see: https://bmrb.io/macro/files/xplor_to_iupac.Nov140620
    # whether to trust the ref_info or the macro for atom nomenclature of ASN/GLN amino group
    __trust_bmrb_ref_info = True

    # atom name mapping of public MR file between the archive coordinates and submitted ones
    __mrAtomNameMapping = None

    # CCD accessing utility
    __ccU = None

    # BMRB chemical shift statistics
    __csStat = None

    # NEFTranslator
    __nefT = None

    # Pairwise align
    __pA = None

    # reasons for re-parsing request from the previous trial
    __reasons = None

    # CIF reader
    __cR = None
    __hasCoord = False

    # experimental method
    __exptlMethod = ''
    # whether solid-state NMR is applied to symmetric samples such as fibrils
    __symmetric = 'no'

    # data item name for model ID in 'atom_site' category
    __modelNumName = None

    # data item names for auth_asym_id, auth_seq_id, auth_atom_id in 'atom_site' category
    __authAsymId = None
    __authSeqId = None
    __authAtomId = None

    # coordinates information generated by ParserListenerUtil.coordAssemblyChecker()
    __polySeq = None
    __altPolySeq = None
    __nonPoly = None
    __branched = None
    __nonPolySeq = None
    __coordAtomSite = None
    __coordUnobsRes = None
    __labelToAuthSeq = None
    __authToLabelSeq = None
    __authToStarSeq = None
    __authToInsCode = None

    __offsetHolder = None

    __representativeModelId = REPRESENTATIVE_MODEL_ID
    __hasPolySeq = False
    __hasNonPoly = False
    __hasBranched = False
    __hasNonPolySeq = False
    __preferAuthSeq = True

    # large model
    __largeModel = False
    __representativeAsymId = 'A'

    # polymer sequence of MR file
    __polySeqRst = None

    __seqAlign = None
    __chainAssign = None

    # current restraint subtype
    __cur_subtype = ''
    __cur_auth_atom_id = ''

    # last comment
    lastComment = None

    # vector statement
    __cur_vector_mode = ''
    __cur_vector_atom_prop_type = ''

    # evaluate statement
    __cur_symbol_name = ''
    __cur_vflc_op_code = ''

    # union expression
    __cur_union_expr = False
    __con_union_expr = False
    __top_union_expr = False

    depth = 0

    stackSelections = None  # stack of selection
    stackTerms = None  # stack of term
    stackFactors = None  # stack of factor
    stackVflc = None  # stack of Vflc

    factor = None
    unionFactor = None

    # distance
    noeAverage = 'r-6'
    squareExponent = 1.0
    rSwitch = None
    scale = 1.0
    kMin = 0.0
    kMax = 0.0
    rMin = 0.0
    rMax = None
    fMax = None
    # tCon = 0.0
    rExp = -1.0 / 6.0

    # dihedral angle
    force = None
    min = None
    width = None
    period = 0

    # generic statements
    classification = None
    coefficients = None

    # collection of atom selection
    atomSelectionSet = []

    # collection of number selection
    numberSelection = []

    # collection of number selection in factor
    numberFSelection = []

    # evaluate
    evaluate = {}

    __f = __g = None
    warningMessage = None

    reasonsForReParsing = {}

    __cachedDictForAtomIdList = {}
    __cachedDictForFactor = {}

    # original source MR file name
    __originalFileName = '.'

    # list id counter
    __listIdCounter = {}

    # entry ID
    __entryId = '.'

    # dictionary of pynmrstar saveframes
    sfDict = {}

    # last edited pynmrstar saveframe
    __lastSfDict = {}

    def __init__(self, verbose=True, log=sys.stdout,
                 representativeModelId=REPRESENTATIVE_MODEL_ID,
                 mrAtomNameMapping=None,
                 cR=None, caC=None, ccU=None, csStat=None, nefT=None,
                 reasons=None):
        self.__verbose = verbose
        self.__lfh = log

        self.__representativeModelId = representativeModelId
        self.__mrAtomNameMapping = None if mrAtomNameMapping is None or len(mrAtomNameMapping) == 0 else mrAtomNameMapping

        self.__cR = cR
        self.__hasCoord = cR is not None

        if self.__hasCoord:
            ret = coordAssemblyChecker(verbose, log, representativeModelId, cR, caC)
            self.__modelNumName = ret['model_num_name']
            self.__authAsymId = ret['auth_asym_id']
            self.__authSeqId = ret['auth_seq_id']
            self.__authAtomId = ret['auth_atom_id']
            self.__polySeq = ret['polymer_sequence']
            self.__altPolySeq = ret['alt_polymer_sequence']
            self.__nonPoly = ret['non_polymer']
            self.__branched = ret['branched']
            self.__coordAtomSite = ret['coord_atom_site']
            self.__coordUnobsRes = ret['coord_unobs_res']
            self.__labelToAuthSeq = ret['label_to_auth_seq']
            self.__authToLabelSeq = ret['auth_to_label_seq']
            self.__authToStarSeq = ret['auth_to_star_seq']
            self.__authToInsCode = ret['auth_to_ins_code']

        self.__offsetHolder = {}

        self.__hasPolySeq = self.__polySeq is not None and len(self.__polySeq) > 0
        self.__hasNonPoly = self.__nonPoly is not None and len(self.__nonPoly) > 0
        self.__hasBranched = self.__branched is not None and len(self.__branched) > 0
        if self.__hasNonPoly or self.__hasBranched:
            self.__hasNonPolySeq = True
            if self.__hasNonPoly and self.__hasBranched:
                self.__nonPolySeq = self.__nonPoly
                self.__nonPolySeq.extend(self.__branched)
            elif self.__hasNonPoly:
                self.__nonPolySeq = self.__nonPoly
            else:
                self.__nonPolySeq = self.__branched

        self.__largeModel = self.__hasPolySeq and len(self.__polySeq) > LEN_LARGE_ASYM_ID
        if self.__largeModel:
            self.__representativeAsymId = next(c for c in LARGE_ASYM_ID if any(ps for ps in self.__polySeq if ps['auth_chain_id'] == c))

        # CCD accessing utility
        self.__ccU = ChemCompUtil(verbose, log) if ccU is None else ccU

        # BMRB chemical shift statistics
        self.__csStat = BMRBChemShiftStat(verbose, log, self.__ccU) if csStat is None else csStat

        # NEFTranslator
        self.__nefT = NEFTranslator(verbose, log, self.__ccU, self.__csStat) if nefT is None else nefT

        # Pairwise align
        if self.__hasPolySeq:
            self.__pA = PairwiseAlign()
            self.__pA.setVerbose(verbose)

        if reasons is not None and 'model_chain_id_ext' in reasons:
            self.__polySeq, self.__altPolySeq, self.__coordAtomSite, self.__coordUnobsRes,\
                self.__labelToAuthSeq, self.__authToLabelSeq, self.__authToStarSeq =\
                extendCoordChainsForExactNoes(reasons['model_chain_id_ext'],
                                              self.__polySeq, self.__altPolySeq,
                                              self.__coordAtomSite, self.__coordUnobsRes,
                                              self.__authToLabelSeq, self.__authToStarSeq)

        # reasons for re-parsing request from the previous trial
        self.__reasons = reasons
        self.__preferLabelSeqCount = 0

        self.reasonsForReParsing = {}  # reset to prevent interference from the previous run

        self.__cachedDictForAtomIdList = {}
        self.__cachedDictForFactor = {}

        self.distRestraints = 0      # CHARMM: Distance restraints
        self.dihedRestraints = 0     # CHARMM: Dihedral angle restraints
        self.geoRestraints = 0       # CHARMM: Harmonic coordinate/NCS restraints

        self.dist_comment_pat = re.compile('.*:'
                                           r'([A-Za-z]+)(\d+):(\S+)-'
                                           r'([A-Za-z]+)(\d+):(\S+).*')
        self.dist_comment_pat2 = re.compile('.*:'
                                            r'([A-Z]+):([A-Za-z]+)(\d+):(\S+)-'
                                            r'([A-Z]+):([A-Za-z]+)(\d+):(\S+).*')

        self.dihed_comment_pat = re.compile('.*:'
                                            r'([A-Za-z]+)(\d+):(\S+)-'
                                            r'([A-Za-z]+)(\d+):(\S+)-'
                                            r'([A-Za-z]+)(\d+):(\S+)-'
                                            r'([A-Za-z]+)(\d+):(\S+).*')

        self.sfDict = {}

    def setDebugMode(self, debug):
        self.__debug = debug

    def createSfDict(self, createSfDict):
        self.__createSfDict = createSfDict

    def setOriginaFileName(self, originalFileName):
        self.__originalFileName = originalFileName

    def setListIdCounter(self, listIdCounter):
        self.__listIdCounter = listIdCounter

    def setEntryId(self, entryId):
        self.__entryId = entryId

    # Enter a parse tree produced by CharmmMRParser#charmm_mr.
    def enterCharmm_mr(self, ctx: CharmmMRParser.Charmm_mrContext):  # pylint: disable=unused-argument
        self.__polySeqRst = []
        self.__f = []
        self.__g = []

    # Exit a parse tree produced by CharmmMRParser#charmm_mr.
    def exitCharmm_mr(self, ctx: CharmmMRParser.Charmm_mrContext):  # pylint: disable=unused-argument

        try:

            if self.__hasPolySeq and self.__polySeqRst is not None:
                sortPolySeqRst(self.__polySeqRst,
                               None if self.__reasons is None or 'non_poly_remap' not in self.__reasons else self.__reasons['non_poly_remap'])

                self.__seqAlign, _ = alignPolymerSequence(self.__pA, self.__polySeq, self.__polySeqRst,
                                                          resolvedMultimer=self.__reasons is not None)
                self.__chainAssign, message = assignPolymerSequence(self.__pA, self.__ccU, self.__file_type, self.__polySeq, self.__polySeqRst, self.__seqAlign)

                if len(message) > 0:
                    self.__f.extend(message)

                if self.__chainAssign is not None:

                    if len(self.__polySeq) == len(self.__polySeqRst):

                        chain_mapping = {}

                        for ca in self.__chainAssign:
                            ref_chain_id = ca['ref_chain_id']
                            test_chain_id = ca['test_chain_id']

                            if ref_chain_id != test_chain_id:
                                chain_mapping[test_chain_id] = ref_chain_id

                        if len(chain_mapping) == len(self.__polySeq):

                            for ps in self.__polySeqRst:
                                if ps['chain_id'] in chain_mapping:
                                    ps['chain_id'] = chain_mapping[ps['chain_id']]

                            self.__seqAlign, _ = alignPolymerSequence(self.__pA, self.__polySeq, self.__polySeqRst,
                                                                      resolvedMultimer=self.__reasons is not None)
                            self.__chainAssign, _ = assignPolymerSequence(self.__pA, self.__ccU, self.__file_type, self.__polySeq, self.__polySeqRst, self.__seqAlign)

                    trimSequenceAlignment(self.__seqAlign, self.__chainAssign)

                    if self.__reasons is None and any(f for f in self.__f if 'Atom not found' in f):

                        seqIdRemap = []

                        cyclicPolymer = {}

                        for ca in self.__chainAssign:
                            ref_chain_id = ca['ref_chain_id']
                            test_chain_id = ca['test_chain_id']

                            sa = next(sa for sa in self.__seqAlign
                                      if sa['ref_chain_id'] == ref_chain_id
                                      and sa['test_chain_id'] == test_chain_id)

                            poly_seq_model = next(ps for ps in self.__polySeq
                                                  if ps['auth_chain_id'] == ref_chain_id)
                            poly_seq_rst = next(ps for ps in self.__polySeqRst
                                                if ps['chain_id'] == test_chain_id)

                            seq_id_mapping = {}
                            for ref_seq_id, mid_code, test_seq_id in zip(sa['ref_seq_id'], sa['mid_code'], sa['test_seq_id']):
                                if mid_code == '|':
                                    try:
                                        seq_id_mapping[test_seq_id] = next(auth_seq_id for auth_seq_id, seq_id
                                                                           in zip(poly_seq_model['auth_seq_id'], poly_seq_model['seq_id'])
                                                                           if seq_id == ref_seq_id)
                                    except StopIteration:
                                        pass

                            if ref_chain_id not in cyclicPolymer:
                                cyclicPolymer[ref_chain_id] =\
                                    isCyclicPolymer(self.__cR, self.__polySeq, ref_chain_id, self.__representativeModelId, self.__modelNumName)

                            if cyclicPolymer[ref_chain_id]:

                                poly_seq_model = next(ps for ps in self.__polySeq
                                                      if ps['auth_chain_id'] == ref_chain_id)

                                offset = None
                                for seq_id, comp_id in zip(poly_seq_rst['seq_id'], poly_seq_rst['comp_id']):
                                    if seq_id not in seq_id_mapping:
                                        _seq_id = next((_seq_id for _seq_id, _comp_id in zip(poly_seq_model['seq_id'], poly_seq_model['comp_id'])
                                                        if _seq_id not in seq_id_mapping.values() and _comp_id == comp_id), None)
                                        if _seq_id is not None:
                                            offset = seq_id - _seq_id
                                            break

                                if offset is not None:
                                    for seq_id in poly_seq_rst['seq_id']:
                                        if seq_id not in seq_id_mapping:
                                            seq_id_mapping[seq_id] = seq_id - offset

                            if any(k for k, v in seq_id_mapping.items() if k != v)\
                               and not any(k for k, v in seq_id_mapping.items()
                                           if v in poly_seq_model['seq_id']
                                           and k == poly_seq_model['auth_seq_id'][poly_seq_model['seq_id'].index(v)]):
                                seqIdRemap.append({'chain_id': test_chain_id, 'seq_id_dict': seq_id_mapping})

                        if len(seqIdRemap) > 0:
                            if 'seq_id_remap' not in self.reasonsForReParsing:
                                self.reasonsForReParsing['seq_id_remap'] = seqIdRemap

                        if any(ps for ps in self.__polySeq if 'identical_chain_id' in ps):
                            polySeqRst, chainIdMapping = splitPolySeqRstForMultimers(self.__pA, self.__polySeq, self.__polySeqRst, self.__chainAssign)

                            if polySeqRst is not None:
                                self.__polySeqRst = polySeqRst
                                if 'chain_id_remap' not in self.reasonsForReParsing:
                                    self.reasonsForReParsing['chain_id_remap'] = chainIdMapping

                        if len(self.__polySeq) == 1 and len(self.__polySeqRst) == 1:
                            polySeqRst, chainIdMapping, modelChainIdExt =\
                                splitPolySeqRstForExactNoes(self.__pA, self.__polySeq, self.__polySeqRst, self.__chainAssign)

                            if polySeqRst is not None:
                                self.__polySeqRst = polySeqRst
                                if 'chain_id_clone' not in self.reasonsForReParsing:
                                    self.reasonsForReParsing['chain_id_clone'] = chainIdMapping
                                if 'model_chain_id_ext' not in self.reasonsForReParsing:
                                    self.reasonsForReParsing['model_chain_id_ext'] = modelChainIdExt

                        if self.__hasNonPoly:
                            polySeqRst, nonPolyMapping = splitPolySeqRstForNonPoly(self.__ccU, self.__nonPoly, self.__polySeqRst,
                                                                                   self.__seqAlign, self.__chainAssign)

                            if polySeqRst is not None:
                                self.__polySeqRst = polySeqRst
                                if 'non_poly_remap' not in self.reasonsForReParsing:
                                    self.reasonsForReParsing['non_poly_remap'] = nonPolyMapping

                        if self.__hasBranched:
                            polySeqRst, branchedMapping = splitPolySeqRstForBranched(self.__pA, self.__polySeq, self.__branched, self.__polySeqRst,
                                                                                     self.__chainAssign)

                            if polySeqRst is not None:
                                self.__polySeqRst = polySeqRst
                                if 'branched_remap' not in self.reasonsForReParsing:
                                    self.reasonsForReParsing['branched_remap'] = branchedMapping

            # """
            # if 'label_seq_scheme' in self.reasonsForReParsing and self.reasonsForReParsing['label_seq_scheme']:
            #     if 'non_poly_remap' in self.reasonsForReParsing:
            #         self.reasonsForReParsing['label_seq_scheme'] = False
            #     if 'seq_id_remap' in self.reasonsForReParsing:
            #         del self.reasonsForReParsing['seq_id_remap']
            # """
            if 'local_seq_scheme' in self.reasonsForReParsing:
                if 'non_poly_remap' in self.reasonsForReParsing or 'branched_remap' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['local_seq_scheme']
                if 'seq_id_remap' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['seq_id_remap']

            if 'seq_id_remap' in self.reasonsForReParsing and 'non_poly_remap' in self.reasonsForReParsing:
                del self.reasonsForReParsing['seq_id_remap']

        finally:
            self.warningMessage = sorted(list(set(self.__f)), key=self.__f.index)

    # Enter a parse tree produced by CharmmMRParser#comment.
    def enterComment(self, ctx: CharmmMRParser.CommentContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#comment.
    def exitComment(self, ctx: CharmmMRParser.CommentContext):
        comment = []
        for col in range(20):
            if ctx.Any_name(col):
                text = str(ctx.Any_name(col))
                if text[0] in ('#', '!'):
                    break
                comment.append(str(ctx.Any_name(col)))
            else:
                break
        self.lastComment = None if len(comment) == 0 else ' '.join(comment)

    # Enter a parse tree produced by CharmmMRParser#distance_restraint.
    def enterDistance_restraint(self, ctx: CharmmMRParser.Distance_restraintContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist'

        self.noeAverage = 'r-6'  # default averaging method
        self.squareExponent = 1.0
        self.rSwitch = None
        self.scale = 1.0
        self.kMin = 0.0
        self.kMax = 0.0
        self.rMin = 0.0
        self.rMax = None
        self.fMax = None
        # self.tCon = 0.0
        self.rExp = -1.0 / 6.0

        if self.__createSfDict:
            self.__addSf()

    # Exit a parse tree produced by CharmmMRParser#distance_restraint.
    def exitDistance_restraint(self, ctx: CharmmMRParser.Distance_restraintContext):  # pylint: disable=unused-argument

        try:

            target_value = None
            lower_limit = self.rMin
            upper_limit = self.rMax
            lower_linear_limit = None
            upper_linear_limit = None

            if self.fMax is not None and self.fMax > 0.0 and self.kMax > 0.0:
                upper_linear_limit = self.rMax + self.fMax / self.kMax
            if self.rSwitch is not None:
                upper_linear_limit = self.rMax + self.rSwitch

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            self.__allowZeroUpperLimit = False
            if self.__reasons is not None and 'model_chain_id_ext' in self.__reasons\
               and len(self.atomSelectionSet[0]) > 0\
               and len(self.atomSelectionSet[0]) == len(self.atomSelectionSet[1]):
                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                if chain_id_1 != chain_id_2 and seq_id_1 == seq_id_2 and atom_id_1 == atom_id_2\
                   and ((chain_id_1 in self.__reasons['model_chain_id_ext'] and chain_id_2 in self.__reasons['model_chain_id_ext'][chain_id_1])
                        or (chain_id_2 in self.__reasons['model_chain_id_ext'] and chain_id_1 in self.__reasons['model_chain_id_ext'][chain_id_2])):
                    self.__allowZeroUpperLimit = True
            self.__allowZeroUpperLimit |= hasInterChainRestraint(self.atomSelectionSet)

            dstFunc = self.validateDistanceRange(self.scale, self.squareExponent if self.rSwitch is not None else 1.0,
                                                 target_value, lower_limit, upper_limit,
                                                 lower_linear_limit, upper_linear_limit)

            if dstFunc is None:
                return

            if len(self.atomSelectionSet[0]) == 0 or len(self.atomSelectionSet[1]) == 0:
                if len(self.__g) > 0:
                    self.__f.extend(self.__g)
                return

            memberId = '.'
            if self.__createSfDict:
                sf = self.__getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                       self.__csStat, self.__originalFileName),
                                  potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                sf['id'] += 1
                memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'
                if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                   and (isAmbigAtomSelection(self.atomSelectionSet[0], self.__csStat)
                        or isAmbigAtomSelection(self.atomSelectionSet[1], self.__csStat)):
                    memberId = 0
                    _atom1 = _atom2 = None

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if isIdenticalRestraint([atom1, atom2]):
                    continue
                if self.__createSfDict and memberLogicCode == '.':
                    altAtomId1, altAtomId2 = getAltProtonIdInBondConstraint([atom1, atom2], self.__csStat)
                    if altAtomId1 is not None or altAtomId2 is not None:
                        atom1, atom2 =\
                            self.selectRealisticBondConstraint(atom1, atom2,
                                                               altAtomId1, altAtomId2,
                                                               dstFunc)
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (NOE) id={self.distRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    if isinstance(memberId, int):
                        if _atom1 is None or isAmbigAtomSelection([_atom1, atom1], self.__csStat)\
                           or isAmbigAtomSelection([_atom2, atom2], self.__csStat):
                            memberId += 1
                            _atom1, _atom2 = atom1, atom2
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', memberId, memberLogicCode,
                                 sf['list_id'], self.__entryId, dstFunc,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom1, atom2)
                    sf['loop'].add_data(row)

                    if sf['constraint_subsubtype'] == 'ambi':
                        continue

                    if memberLogicCode == 'OR'\
                       and (isAmbigAtomSelection(self.atomSelectionSet[0], self.__csStat)
                            or isAmbigAtomSelection(self.atomSelectionSet[1], self.__csStat)):
                        sf['constraint_subsubtype'] = 'ambi'
                    if 'upper_limit' in dstFunc and dstFunc['upper_limit'] is not None:
                        upperLimit = float(dstFunc['upper_limit'])
                        if upperLimit <= DIST_AMBIG_LOW or upperLimit >= DIST_AMBIG_UP:
                            sf['constraint_subsubtype'] = 'ambi'

        finally:
            self.numberSelection.clear()

            if self.__createSfDict:
                self.__trimSfWoLp()

    # Enter a parse tree produced by CharmmMRParser#point_distance_restraint.
    def enterPoint_distance_restraint(self, ctx: CharmmMRParser.Point_distance_restraintContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#point_distance_restraint.
    def exitPoint_distance_restraint(self, ctx: CharmmMRParser.Point_distance_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#dihedral_angle_restraint.
    def enterDihedral_angle_restraint(self, ctx: CharmmMRParser.Dihedral_angle_restraintContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dihed'

        if self.__createSfDict:
            self.__addSf()

    # Exit a parse tree produced by CharmmMRParser#dihedral_angle_restraint.
    def exitDihedral_angle_restraint(self, ctx: CharmmMRParser.Dihedral_angle_restraintContext):  # pylint: disable=unused-argument

        try:

            target_value = self.min
            lower_limit = None
            upper_limit = None
            lower_linear_limit = None
            upper_linear_limit = None

            dstFunc = self.validateAngleRange(1.0, {'force': self.force, 'period': self.period},
                                              target_value, lower_limit, upper_limit,
                                              lower_linear_limit, upper_linear_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            if len(self.atomSelectionSet) != 4:
                return

            if not self.areUniqueCoordAtoms('a dihedral angle (DIHE)'):
                if len(self.__g) > 0:
                    self.__f.extend(self.__g)
                return

            if self.__createSfDict:
                sf = self.__getSf(potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))

            compId = self.atomSelectionSet[0][0]['comp_id']
            peptide, nucleotide, carbohydrate = self.__csStat.getTypeOfCompId(compId)

            first_item = True

            for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                self.atomSelectionSet[1],
                                                                self.atomSelectionSet[2],
                                                                self.atomSelectionSet[3]):
                angleName = getTypeOfDihedralRestraint(peptide, nucleotide, carbohydrate,
                                                       [atom1, atom2, atom3, atom4])
                if angleName is None:
                    continue
                if peptide and angleName == 'CHI2' and atom4['atom_id'] == 'CD1' and isLikePheOrTyr(atom2['comp_id'], self.__ccU):
                    dstFunc = self.selectRealisticChi2AngleConstraint(atom1, atom2, atom3, atom4,
                                                                      dstFunc)
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (DIHE) id={self.dihedRestraints} angleName={angleName} "
                          f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    if first_item:
                        sf['id'] += 1
                        first_item = False
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, angleName,
                                 sf['list_id'], self.__entryId, dstFunc,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom1, atom2, atom3, atom4)
                    sf['loop'].add_data(row)

        finally:
            self.numberSelection.clear()

            if self.__createSfDict:
                self.__trimSfWoLp()

    # Enter a parse tree produced by CharmmMRParser#harmonic_restraint.
    def enterHarmonic_restraint(self, ctx: CharmmMRParser.Harmonic_restraintContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#harmonic_restraint.
    def exitHarmonic_restraint(self, ctx: CharmmMRParser.Harmonic_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#manipulate_internal_coordinate.
    def enterManipulate_internal_coordinate(self, ctx: CharmmMRParser.Manipulate_internal_coordinateContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#manipulate_internal_coordinate.
    def exitManipulate_internal_coordinate(self, ctx: CharmmMRParser.Manipulate_internal_coordinateContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#droplet_potential.
    def enterDroplet_potential(self, ctx: CharmmMRParser.Droplet_potentialContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#droplet_potential.
    def exitDroplet_potential(self, ctx: CharmmMRParser.Droplet_potentialContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#fix_atom_constraint.
    def enterFix_atom_constraint(self, ctx: CharmmMRParser.Fix_atom_constraintContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#fix_atom_constraint.
    def exitFix_atom_constraint(self, ctx: CharmmMRParser.Fix_atom_constraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#center_of_mass_constraint.
    def enterCenter_of_mass_constraint(self, ctx: CharmmMRParser.Center_of_mass_constraintContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#center_of_mass_constraint.
    def exitCenter_of_mass_constraint(self, ctx: CharmmMRParser.Center_of_mass_constraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#fix_bond_or_angle_constraint.
    def enterFix_bond_or_angle_constraint(self, ctx: CharmmMRParser.Fix_bond_or_angle_constraintContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#fix_bond_or_angle_constraint.
    def exitFix_bond_or_angle_constraint(self, ctx: CharmmMRParser.Fix_bond_or_angle_constraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#restrained_distance.
    def enterRestrained_distance(self, ctx: CharmmMRParser.Restrained_distanceContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#restrained_distance.
    def exitRestrained_distance(self, ctx: CharmmMRParser.Restrained_distanceContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#external_force.
    def enterExternal_force(self, ctx: CharmmMRParser.External_forceContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#external_force.
    def exitExternal_force(self, ctx: CharmmMRParser.External_forceContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#rmsd_restraint.
    def enterRmsd_restraint(self, ctx: CharmmMRParser.Rmsd_restraintContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#rmsd_restraint.
    def exitRmsd_restraint(self, ctx: CharmmMRParser.Rmsd_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#gyration_restraint.
    def enterGyration_restraint(self, ctx: CharmmMRParser.Gyration_restraintContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#gyration_restraint.
    def exitGyration_restraint(self, ctx: CharmmMRParser.Gyration_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#distance_matrix_restraint.
    def enterDistance_matrix_restraint(self, ctx: CharmmMRParser.Distance_matrix_restraintContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#distance_matrix_restraint.
    def exitDistance_matrix_restraint(self, ctx: CharmmMRParser.Distance_matrix_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#noe_statement.
    def enterNoe_statement(self, ctx: CharmmMRParser.Noe_statementContext):
        if ctx.MinDist():
            self.noeAverage = 'min'

        elif ctx.SumR():
            self.noeAverage = 'sum'

        elif ctx.SExp():
            self.squareExponent = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.squareExponent, str):
                if self.squareExponent in self.evaluate:
                    self.squareExponent = self.evaluate[self.squareExponent]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.squareExponent!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.squareExponent = 1.0
            if self.squareExponent is None or self.squareExponent <= 0.0:
                self.__f.append("[Invalid data] "
                                "The exponent value of square-well or soft-square function "
                                f"'NOE {str(ctx.SExp())} {self.squareExponent} END' must be a positive value.")

        elif ctx.RSwi():
            self.rSwitch = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.rSwitch, str):
                if self.rSwitch in self.evaluate:
                    self.rSwitch = self.evaluate[self.rSwitch]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.rSwitch!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.rSwitch = 1.0
            if self.rSwitch is None or self.rSwitch < 0.0:
                self.__f.append("[Invalid data] "
                                "The smoothing parameter of soft-square function "
                                f"'NOE {str(ctx.RSwi())} {self.rSwitch} END' must not be a negative value.")

        elif ctx.Scale():
            self.scale = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.scale, str):
                if self.scale in self.evaluate:
                    self.scale = self.evaluate[self.scale]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.scale!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.scale = 1.0
            if self.scale is None or self.scale == 0.0:
                self.__f.append("[Range value warning] "
                                f"The scale value 'NOE {str(ctx.Scale())} {self.scale} END' should be a positive value.")
            elif self.scale < 0.0:
                self.__f.append("[Invalid data] "
                                f"The scale value 'NOE {str(ctx.Scale())} {self.scale} END' must not be a negative value.")

        elif ctx.KMin():
            self.kMin = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.kMin, str):
                if self.kMin in self.evaluate:
                    self.kMin = self.evaluate[self.kMin]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.kMin!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.kMin = 0.0
            if self.kMin is None or self.kMin < 0.0:
                self.__f.append("[Invalid data] "
                                "The kinetic parameter of soft-square function "
                                f"'NOE {str(ctx.KMin())} {self.kMin} END' must not be a negative value.")

        elif ctx.KMax():
            self.kMax = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.kMax, str):
                if self.kMax in self.evaluate:
                    self.kMax = self.evaluate[self.kMax]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.kMax!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.kMax = 0.0
            if self.kMax is None or self.kMax < 0.0:
                self.__f.append("[Invalid data] "
                                "The kinetic parameter of soft-square function "
                                f"'NOE {str(ctx.KMax())} {self.kMax} END' must not be a negative value.")

        elif ctx.RMin():
            self.rMin = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.rMin, str):
                if self.rMin in self.evaluate:
                    self.rMin = self.evaluate[self.rMin]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.rMin!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.rMin = 0.0
            if self.rMin is None or self.rMin < 0.0:
                self.__f.append("[Invalid data] "
                                "The lower limit of distance restraint "
                                f"'NOE {str(ctx.RMin())} {self.rMin} END' must not be a negative value.")

        elif ctx.RMax():
            self.rMax = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.rMax, str):
                if self.rMax in self.evaluate:
                    self.rMax = self.evaluate[self.rMax]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.rMax!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.rMax = None
            if self.rMax is not None and self.rMax < 0.0:
                self.__f.append("[Invalid data] "
                                "The upper limit of distance restraint "
                                f"'NOE {str(ctx.RMax())} {self.rMax} END' must not be a negative value.")

        elif ctx.FMax():
            self.fMax = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.fMax, str):
                if self.fMax in self.evaluate:
                    self.fMax = self.evaluate[self.fMax]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.fMax!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.fMax = None
            if self.fMax is not None and self.fMax < 0.0:
                self.__f.append("[Invalid data] "
                                "The kinetic parameter of smoothing function "
                                f"'NOE {str(ctx.FMax())} {self.fMax} END' must not be a negative value.")

        elif ctx.RExp():
            self.rExp = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.rExp, str):
                if self.rExp in self.evaluate:
                    self.rExp = self.evaluate[self.rExp]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.rExp!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.rExp = -1.0 / 6.0
            if abs(self.rExp + 1.0 / 6.0) < 0.001 or abs(self.rExp - 6.0) < 0.001:
                self.noeAverage = 'r-6'
            elif abs(self.rExp - 3.0) < 0.001:
                self.noeAverage = 'r-3'
            elif abs(self.rExp - 1.0) < 0.001:
                self.noeAverage = 'center'

        elif ctx.Reset():
            self.noeAverage = 'r-6'
            self.squareExponent = 1.0
            self.rSwitch = None
            self.scale = 1.0
            self.kMin = 0.0
            self.kMax = 0.0
            self.rMin = 0.0
            self.rMax = None
            self.fMax = None
            # self.tCon = 0.0
            self.rExp = -1.0 / 6.0

    # Exit a parse tree produced by CharmmMRParser#noe_statement.
    def exitNoe_statement(self, ctx: CharmmMRParser.Noe_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#noe_assign.
    def enterNoe_assign(self, ctx: CharmmMRParser.Noe_assignContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by CharmmMRParser#noe_assign.
    def exitNoe_assign(self, ctx: CharmmMRParser.Noe_assignContext):  # pylint: disable=unused-argument
        pass

    def validateDistanceRange(self, weight, squareExponent,
                              target_value, lower_limit, upper_limit,
                              lower_linear_limit, upper_linear_limit):
        """ Validate distance value range.
        """

        validRange = True
        dstFunc = {'weight': weight, 'average': self.noeAverage, 'exponent_over_upper_limit': squareExponent}

        if target_value is not None and upper_limit is not None and lower_limit is not None\
           and abs(target_value - lower_limit) <= DIST_AMBIG_UNCERT\
           and abs(target_value - upper_limit) <= DIST_AMBIG_UNCERT:
            if target_value >= DIST_AMBIG_MED:
                lower_limit = lower_linear_limit = None
            elif target_value <= DIST_AMBIG_LOW:
                upper_limit = upper_linear_limit = None

        if target_value is not None:
            if DIST_ERROR_MIN < target_value < DIST_ERROR_MAX or (target_value == 0.0 and self.__allowZeroUpperLimit):
                dstFunc['target_value'] = f"{target_value}" if target_value > 0.0 else "0.0"
            else:
                if target_value <= DIST_ERROR_MIN and self.__omitDistLimitOutlier:
                    self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                    f"The target value='{target_value}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                    target_value = None
                else:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The target value='{target_value}' must be within range {DIST_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if DIST_ERROR_MIN <= lower_limit < DIST_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.3f}" if lower_limit > 0.0 else "0.0"
            else:
                if lower_limit <= DIST_ERROR_MIN and self.__omitDistLimitOutlier:
                    self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                    lower_limit = None
                else:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if DIST_ERROR_MIN < upper_limit <= DIST_ERROR_MAX or (upper_limit == 0.0 and self.__allowZeroUpperLimit):
                dstFunc['upper_limit'] = f"{upper_limit:.3f}" if upper_limit > 0.0 else "0.0"
            else:
                if (upper_limit <= DIST_ERROR_MIN or upper_limit > DIST_ERROR_MAX) and self.__omitDistLimitOutlier:
                    self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                    upper_limit = None
                else:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if lower_linear_limit is not None:
            if DIST_ERROR_MIN <= lower_linear_limit < DIST_ERROR_MAX:
                dstFunc['lower_linear_limit'] = f"{lower_linear_limit:.3f}" if lower_linear_limit > 0.0 else "0.0"
            else:
                if lower_linear_limit <= DIST_ERROR_MIN and self.__omitDistLimitOutlier:
                    self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                    lower_linear_limit = None
                else:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if upper_linear_limit is not None:
            if DIST_ERROR_MIN < upper_linear_limit <= DIST_ERROR_MAX or (upper_linear_limit == 0.0 and self.__allowZeroUpperLimit):
                dstFunc['upper_linear_limit'] = f"{upper_linear_limit:.3f}" if upper_linear_limit > 0.0 else "0.0"
            else:
                if (upper_linear_limit <= DIST_ERROR_MIN or upper_linear_limit > DIST_ERROR_MAX) and self.__omitDistLimitOutlier:
                    self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                    f"The upper linear limit value='{upper_linear_limit:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                    upper_linear_limit = None
                else:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper linear limit value='{upper_linear_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.3f}' must be less than the target value '{target_value}'. "
                                    "It indicates that a negative value was unexpectedly set: "
                                    f"d={target_value}, dminus={self.numberSelection[1]}, dplus={self.numberSelection[2]}.")

            if lower_linear_limit is not None:
                if lower_linear_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.3f}' must be less than the target value '{target_value}'. "
                                    "It indicates that a negative value was unexpectedly set: "
                                    f"d={target_value}, dminus={self.numberSelection[1]}, dplus={self.numberSelection[2]}.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.3f}' must be greater than the target value '{target_value}'. "
                                    "It indicates that a negative value was unexpectedly set: "
                                    f"d={target_value}, dminus={self.numberSelection[1]}, dplus={self.numberSelection[2]}.")

            if upper_linear_limit is not None:
                if upper_linear_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper linear limit value='{upper_linear_limit:.3f}' must be greater than the target value '{target_value}'. "
                                    "It indicates that a negative value was unexpectedly set: "
                                    f"d={target_value}, dminus={self.numberSelection[1]}, dplus={self.numberSelection[2]}.")

        else:

            if lower_limit is not None and upper_limit is not None:
                if lower_limit > upper_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.3f}' must be less than the upper limit value '{upper_limit:.3f}'.")
            if lower_linear_limit is not None and upper_limit is not None:
                if lower_linear_limit > upper_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.3f}' must be less than the upper limit value '{upper_limit:.3f}'.")

            if lower_limit is not None and upper_linear_limit is not None:
                if lower_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.3f}' must be less than the upper limit value '{upper_linear_limit:.3f}'.")

            if lower_linear_limit is not None and upper_linear_limit is not None:
                if lower_linear_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.3f}' must be less than the upper limit value '{upper_linear_limit:.3f}'.")

            if lower_limit is not None and lower_linear_limit is not None:
                if lower_linear_limit > lower_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.3f}' must be less than the lower limit value '{lower_limit:.3f}'.")

            if upper_limit is not None and upper_linear_limit is not None:
                if upper_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.3f}' must be less than the upper linear limit value '{upper_linear_limit:.3f}'.")

        if not validRange:
            return None

        if target_value is not None:
            if DIST_RANGE_MIN <= target_value <= DIST_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value}' should be within range {DIST_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if DIST_RANGE_MIN <= lower_limit <= DIST_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit:.3f}' should be within range {DIST_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if DIST_RANGE_MIN <= upper_limit <= DIST_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit:.3f}' should be within range {DIST_RESTRAINT_RANGE}.")

        if lower_linear_limit is not None:
            if DIST_RANGE_MIN <= lower_linear_limit <= DIST_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower linear limit value='{lower_linear_limit:.3f}' should be within range {DIST_RESTRAINT_RANGE}.")

        if upper_linear_limit is not None:
            if DIST_RANGE_MIN <= upper_linear_limit <= DIST_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper linear limit value='{upper_linear_limit:.3f}' should be within range {DIST_RESTRAINT_RANGE}.")

        return dstFunc

    # Enter a parse tree produced by CharmmMRParser#pnoe_statement.
    def enterPnoe_statement(self, ctx: CharmmMRParser.Pnoe_statementContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#pnoe_statement.
    def exitPnoe_statement(self, ctx: CharmmMRParser.Pnoe_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#pnoe_assign.
    def enterPnoe_assign(self, ctx: CharmmMRParser.Pnoe_assignContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by CharmmMRParser#pnoe_assign.
    def exitPnoe_assign(self, ctx: CharmmMRParser.Pnoe_assignContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#dihedral_statement.
    def enterDihedral_statement(self, ctx: CharmmMRParser.Dihedral_statementContext):  # pylint: disable=unused-argument
        if ctx.Force():
            self.force = float(str(ctx.Force()))

        elif ctx.Min():
            self.min = float(str(ctx.Min()))

        elif ctx.Width():
            self.width = float(str(ctx.Width()))

        elif ctx.Period():
            self.period = int(str(ctx.Period()))

    # Exit a parse tree produced by CharmmMRParser#dihedral_statement.
    def exitDihedral_statement(self, ctx: CharmmMRParser.Dihedral_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#dihedral_assign.
    def enterDihedral_assign(self, ctx: CharmmMRParser.Dihedral_assignContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by CharmmMRParser#dihedral_assign.
    def exitDihedral_assign(self, ctx: CharmmMRParser.Dihedral_assignContext):  # pylint: disable=unused-argument
        if ctx.selection(0):
            pass

        elif ctx.ByNumber():
            self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                            "The 'bynumber' clause has no effect "
                            "because the internal atom number is not included in the coordinate file.")

        elif ctx.Simple_name(0) and ctx.Integer(0):
            if ctx.Simple_name(4):
                for col in range(4):
                    self.factor = {'chain_id': [str(ctx.Simple_name(col * 2))],
                                   'seq_id': [int(str(ctx.Integer(col)))],
                                   'atom_id': [str(ctx.Simple_name(col * 2 + 1))]}
                    self.factor = self.__consumeFactor_expressions(self.factor, 'atom-spec', True)
                    atomSelection = self.factor['atom_selection'] if 'atom_selection' in self.factor else []
                    self.atomSelectionSet.append(atomSelection)
            else:
                for col in range(4):
                    self.factor = {'seq_id': [int(str(ctx.Integer(col)))],
                                   'atom_id': [str(ctx.Simple_name(col))]}
                    atomSelection = self.factor['atom_selection'] if 'atom_selection' in self.factor else []
                    self.atomSelectionSet.append(atomSelection)

    def validateAngleRange(self, weight, misc_dict,
                           target_value, lower_limit, upper_limit,
                           lower_linear_limit=None, upper_linear_limit=None):
        """ Validate angle value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if self.__correctCircularShift:
            _array = numpy.array([target_value, lower_limit, upper_limit, lower_linear_limit, upper_linear_limit],
                                 dtype=float)

            shift = None
            if numpy.nanmin(_array) >= THRESHHOLD_FOR_CIRCULAR_SHIFT:
                shift = -(numpy.nanmax(_array) // 360) * 360
            elif numpy.nanmax(_array) <= -THRESHHOLD_FOR_CIRCULAR_SHIFT:
                shift = -(numpy.nanmin(_array) // 360) * 360
            if shift is not None:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                "The target/limit values for an angle restraint have been circularly shifted "
                                f"to fit within range {ANGLE_RESTRAINT_ERROR}.")
                if target_value is not None:
                    target_value += shift
                if lower_limit is not None:
                    lower_limit += shift
                if upper_limit is not None:
                    upper_limit += shift
                if lower_linear_limit is not None:
                    upper_linear_limit += shift
                if upper_linear_limit is not None:
                    upper_linear_limit += shift

        if isinstance(misc_dict, dict):
            for k, v in misc_dict.items():
                dstFunc[k] = v

        if target_value is not None:
            if ANGLE_ERROR_MIN < target_value < ANGLE_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if ANGLE_ERROR_MIN <= lower_limit < ANGLE_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.3f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if ANGLE_ERROR_MIN < upper_limit <= ANGLE_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.3f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if lower_linear_limit is not None:
            if ANGLE_ERROR_MIN <= lower_linear_limit < ANGLE_ERROR_MAX:
                dstFunc['lower_linear_limit'] = f"{lower_linear_limit:.3f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The lower linear limit value='{lower_linear_limit:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if upper_linear_limit is not None:
            if ANGLE_ERROR_MIN < upper_linear_limit <= ANGLE_ERROR_MAX:
                dstFunc['upper_linear_limit'] = f"{upper_linear_limit:.3f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The upper linear limit value='{upper_linear_limit:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if lower_limit is not None and lower_linear_limit is not None:
            if lower_linear_limit > lower_limit:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The lower linear limit value='{lower_linear_limit:.3f}' must be less than the lower limit value '{lower_limit:.3f}'.")

        if upper_limit is not None and upper_linear_limit is not None:
            if upper_limit > upper_linear_limit:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit:.3f}' must be less than the upper linear limit value '{upper_linear_limit:.3f}'.")

        if not validRange:
            return None

        if target_value is not None:
            if ANGLE_RANGE_MIN <= target_value <= ANGLE_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if ANGLE_RANGE_MIN <= lower_limit <= ANGLE_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if ANGLE_RANGE_MIN <= upper_limit <= ANGLE_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if lower_linear_limit is not None:
            if ANGLE_RANGE_MIN <= lower_linear_limit <= ANGLE_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower linear limit value='{lower_linear_limit:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if upper_linear_limit is not None:
            if ANGLE_RANGE_MIN <= upper_linear_limit <= ANGLE_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper linear limit value='{upper_linear_limit:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        return dstFunc

    def areUniqueCoordAtoms(self, subtype_name, skip_col=None):
        """ Check whether atom selection sets are uniquely assigned.
        """

        for col, _atomSelectionSet in enumerate(self.atomSelectionSet):
            _lenAtomSelectionSet = len(_atomSelectionSet)

            if _lenAtomSelectionSet == 0:
                if skip_col is not None and col in skip_col:
                    continue
                return False  # raised error already

            if _lenAtomSelectionSet == 1:
                continue

            for (atom1, atom2) in itertools.combinations(_atomSelectionSet, 2):
                if atom1['chain_id'] != atom2['chain_id']:
                    continue
                if atom1['seq_id'] != atom2['seq_id']:
                    continue
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"Ambiguous atom selection '{atom1['chain_id']}:{atom1['seq_id']}:{atom1['comp_id']}:{atom1['atom_id']} or "
                                f"{atom2['atom_id']}' is not allowed as {subtype_name} restraint.")
                return False

        return True

    # Enter a parse tree produced by CharmmMRParser#harmonic_statement.
    def enterHarmonic_statement(self, ctx: CharmmMRParser.Harmonic_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by CharmmMRParser#harmonic_statement.
    def exitHarmonic_statement(self, ctx: CharmmMRParser.Harmonic_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#absolute_spec.
    def enterAbsolute_spec(self, ctx: CharmmMRParser.Absolute_specContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#absolute_spec.
    def exitAbsolute_spec(self, ctx: CharmmMRParser.Absolute_specContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#force_const_spec.
    def enterForce_const_spec(self, ctx: CharmmMRParser.Force_const_specContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#force_const_spec.
    def exitForce_const_spec(self, ctx: CharmmMRParser.Force_const_specContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#bestfit_spec.
    def enterBestfit_spec(self, ctx: CharmmMRParser.Bestfit_specContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#bestfit_spec.
    def exitBestfit_spec(self, ctx: CharmmMRParser.Bestfit_specContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#coordinate_spec.
    def enterCoordinate_spec(self, ctx: CharmmMRParser.Coordinate_specContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#coordinate_spec.
    def exitCoordinate_spec(self, ctx: CharmmMRParser.Coordinate_specContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#ic_statement.
    def enterIc_statement(self, ctx: CharmmMRParser.Ic_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by CharmmMRParser#ic_statement.
    def exitIc_statement(self, ctx: CharmmMRParser.Ic_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#droplet_statement.
    def enterDroplet_statement(self, ctx: CharmmMRParser.Droplet_statementContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#droplet_statement.
    def exitDroplet_statement(self, ctx: CharmmMRParser.Droplet_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#fix_atom_statement.
    def enterFix_atom_statement(self, ctx: CharmmMRParser.Fix_atom_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by CharmmMRParser#fix_atom_statement.
    def exitFix_atom_statement(self, ctx: CharmmMRParser.Fix_atom_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#center_of_mass_statement.
    def enterCenter_of_mass_statement(self, ctx: CharmmMRParser.Center_of_mass_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by CharmmMRParser#center_of_mass_statement.
    def exitCenter_of_mass_statement(self, ctx: CharmmMRParser.Center_of_mass_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#fix_bond_or_angle_statement.
    def enterFix_bond_or_angle_statement(self, ctx: CharmmMRParser.Fix_bond_or_angle_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by CharmmMRParser#fix_bond_or_angle_statement.
    def exitFix_bond_or_angle_statement(self, ctx: CharmmMRParser.Fix_bond_or_angle_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#shake_opt.
    def enterShake_opt(self, ctx: CharmmMRParser.Shake_optContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#shake_opt.
    def exitShake_opt(self, ctx: CharmmMRParser.Shake_optContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#fast_opt.
    def enterFast_opt(self, ctx: CharmmMRParser.Fast_optContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#fast_opt.
    def exitFast_opt(self, ctx: CharmmMRParser.Fast_optContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#restrained_distance_statement.
    def enterRestrained_distance_statement(self, ctx: CharmmMRParser.Restrained_distance_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by CharmmMRParser#restrained_distance_statement.
    def exitRestrained_distance_statement(self, ctx: CharmmMRParser.Restrained_distance_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#external_force_statement.
    def enterExternal_force_statement(self, ctx: CharmmMRParser.External_force_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by CharmmMRParser#external_force_statement.
    def exitExternal_force_statement(self, ctx: CharmmMRParser.External_force_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#rmsd_statement.
    def enterRmsd_statement(self, ctx: CharmmMRParser.Rmsd_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by CharmmMRParser#rmsd_statement.
    def exitRmsd_statement(self, ctx: CharmmMRParser.Rmsd_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#rmsd_orient_spec.
    def enterRmsd_orient_spec(self, ctx: CharmmMRParser.Rmsd_orient_specContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#rmsd_orient_spec.
    def exitRmsd_orient_spec(self, ctx: CharmmMRParser.Rmsd_orient_specContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#rmsd_force_const_spec.
    def enterRmsd_force_const_spec(self, ctx: CharmmMRParser.Rmsd_force_const_specContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#rmsd_force_const_spec.
    def exitRmsd_force_const_spec(self, ctx: CharmmMRParser.Rmsd_force_const_specContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#rmsd_coordinate_spec.
    def enterRmsd_coordinate_spec(self, ctx: CharmmMRParser.Rmsd_coordinate_specContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#rmsd_coordinate_spec.
    def exitRmsd_coordinate_spec(self, ctx: CharmmMRParser.Rmsd_coordinate_specContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#gyration_statement.
    def enterGyration_statement(self, ctx: CharmmMRParser.Gyration_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by CharmmMRParser#gyration_statement.
    def exitGyration_statement(self, ctx: CharmmMRParser.Gyration_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#distance_matrix_statement.
    def enterDistance_matrix_statement(self, ctx: CharmmMRParser.Distance_matrix_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by CharmmMRParser#distance_matrix_statement.
    def exitDistance_matrix_statement(self, ctx: CharmmMRParser.Distance_matrix_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#selection.
    def enterSelection(self, ctx: CharmmMRParser.SelectionContext):  # pylint: disable=unused-argument
        if self.__sel_expr_debug:
            print("  " * self.depth + "enter_selection")

        if self.depth == 0:
            self.stackSelections = []
            self.stackTerms = []
            self.factor = {}

    # Exit a parse tree produced by CharmmMRParser#selection.
    def exitSelection(self, ctx: CharmmMRParser.SelectionContext):  # pylint: disable=unused-argument
        if self.__sel_expr_debug:
            print("  " * self.depth + "exit_selection")

        if 'or' in self.stackSelections:
            top_union_exprs = self.stackSelections.count('or')

            unionSelections = []
            unionSelections.append(None)
            unionId = 0

            for _selection in self.stackSelections:

                if _selection is None:
                    continue

                if isinstance(_selection, str) and _selection == 'or':

                    if unionId == top_union_exprs - 1:
                        break

                    unionSelections.append(None)
                    unionId += 1

                    continue

                if unionSelections[unionId] is None:
                    unionSelections[unionId] = []

                unionSelections[unionId].append(_selection)

            self.stackSelections.clear()

            unionAtomSelection = []

            for stackSelections in unionSelections:

                if stackSelections is None:
                    continue

                if 'and' not in stackSelections:

                    atomSelection = stackSelections.pop() if stackSelections else []

                    while stackSelections:
                        _selection = stackSelections.pop()
                        if _selection is not None:
                            atomSelection = self.__intersectionAtom_selections(_selection, atomSelection)

                else:

                    blockSelections = []
                    blockSelections.append(None)
                    blockId = 0

                    for _selection in stackSelections:

                        if _selection is None:
                            continue

                        if isinstance(_selection, str) and _selection == 'and':
                            blockSelections.append(None)
                            blockId += 1
                            continue

                        if blockSelections[blockId] is None:
                            blockSelections[blockId] = _selection

                        else:
                            for _atom in _selection:
                                if _atom not in blockSelections[blockId]:
                                    blockSelections[blockId].append(_atom)

                    stackSelections.clear()

                    atomSelection = blockSelections.pop()

                    while blockSelections:
                        atomSelection = self.__intersectionAtom_selections(blockSelections.pop(), atomSelection)

                if len(atomSelection) > 0:
                    unionAtomSelection.extend(atomSelection)

            atomSelection = unionAtomSelection

            if '*' in atomSelection:
                atomSelection.remove('*')

            if self.__createSfDict:
                atomSelection = sorted(atomSelection, key=itemgetter('chain_id', 'seq_id', 'atom_id'))

            if self.__sel_expr_debug:
                print("  " * self.depth + f"atom selection: {atomSelection}")

            self.atomSelectionSet.append(atomSelection)

            return

        if 'and' not in self.stackSelections:

            atomSelection = self.stackSelections.pop() if self.stackSelections else []

            while self.stackSelections:
                _selection = self.stackSelections.pop()
                if _selection is not None:
                    if self.__con_union_expr:
                        for _atom in _selection:
                            if _atom not in atomSelection:
                                atomSelection.append(_atom)
                    else:
                        atomSelection = self.__intersectionAtom_selections(_selection, atomSelection)

        else:

            blockSelections = []
            blockSelections.append(None)
            blockId = 0

            for _selection in self.stackSelections:

                if _selection is None:
                    continue

                if isinstance(_selection, str) and _selection == 'and':
                    blockSelections.append(None)
                    blockId += 1
                    continue

                if blockSelections[blockId] is None:
                    blockSelections[blockId] = _selection

                else:
                    for _atom in _selection:
                        if _atom not in blockSelections[blockId]:
                            blockSelections[blockId].append(_atom)

            self.stackSelections.clear()

            atomSelection = blockSelections.pop()

            while blockSelections:
                atomSelection = self.__intersectionAtom_selections(blockSelections.pop(), atomSelection)

        while self.stackSelections:
            _selection = self.stackSelections.pop()
            if _selection is not None:
                for _atom in _selection:
                    if _atom not in atomSelection:
                        atomSelection.append(_atom)

        if '*' in atomSelection:
            atomSelection.remove('*')

        if self.__createSfDict:
            atomSelection = sorted(atomSelection, key=itemgetter('chain_id', 'seq_id', 'atom_id'))

        if self.__sel_expr_debug:
            print("  " * self.depth + f"atom selection: {atomSelection}")

        self.atomSelectionSet.append(atomSelection)

    # Enter a parse tree produced by CharmmMRParser#selection_expression.
    def enterSelection_expression(self, ctx: CharmmMRParser.Selection_expressionContext):
        self.__cur_union_expr = self.__con_union_expr = bool(ctx.Or_op(0))
        if self.depth == 0:
            self.__top_union_expr = self.__cur_union_expr

        if self.depth > 0 and self.__cur_union_expr:
            self.unionFactor = {}

        if self.__sel_expr_debug:
            print("  " * self.depth + f"enter_sel_expr, union: {self.__cur_union_expr}")

        if self.depth > 0 and len(self.factor) > 0:
            if 'atom_selection' not in self.factor:
                self.consumeFactor_expressions(cifCheck=True)
            if 'atom_selection' in self.factor:
                self.stackSelections.append(self.factor['atom_selection'])
                self.stackSelections.append('and')  # intersection

        self.depth += 1

    # Exit a parse tree produced by CharmmMRParser#selection_expression.
    def exitSelection_expression(self, ctx: CharmmMRParser.Selection_expressionContext):  # pylint: disable=unused-argument
        self.depth -= 1
        if self.__sel_expr_debug:
            print("  " * self.depth + "exit_sel_expr")

        _atomSelection = []
        while self.stackTerms:
            _term = self.stackTerms.pop()
            if _term is not None:
                _atomSelection.extend(_term)

        atomSelection = [dict(s) for s in set(frozenset(atom.items()) for atom in _atomSelection)] if len(_atomSelection) > 1 else _atomSelection

        if len(atomSelection) > 0:
            self.stackSelections.append(atomSelection)

        if self.depth == 0 or not self.__top_union_expr:
            self.factor = {}

        if self.__cur_union_expr:
            self.__cur_union_expr = False
        if self.__con_union_expr and self.depth == 0:
            self.__con_union_expr = False
            self.unionFactor = None

    # Enter a parse tree produced by CharmmMRParser#term.
    def enterTerm(self, ctx: CharmmMRParser.TermContext):
        if self.__sel_expr_debug:
            print("  " * self.depth + f"enter_term, intersection: {bool(ctx.And_op(0))}")

        self.stackFactors = []
        self.factor = {}

        self.depth += 1

    # Exit a parse tree produced by CharmmMRParser#term.
    def exitTerm(self, ctx: CharmmMRParser.TermContext):  # pylint: disable=unused-argument
        self.depth -= 1
        if self.__sel_expr_debug:
            print("  " * self.depth + "exit_term")

        if self.depth == 1 and self.__top_union_expr:

            if self.stackFactors:
                while self.stackFactors:
                    _factor = self.__consumeFactor_expressions(self.stackFactors.pop(), cifCheck=True)
                    self.factor = self.__intersectionFactor_expressions(self.factor,
                                                                        None if 'atom_selection' not in _factor
                                                                        or isinstance(_factor['atom_selection'], str)
                                                                        else _factor['atom_selection'])
            else:
                self.factor = self.__consumeFactor_expressions(self.factor, cifCheck=True)

            if 'atom_selection' in self.factor:
                self.stackTerms.append(self.factor['atom_selection'])

            _atomSelection = []
            while self.stackTerms:
                _term = self.stackTerms.pop()
                if _term is not None and not isinstance(_term, str):
                    _atomSelection.extend(_term)

            atomSelection = [dict(s) for s in set(frozenset(atom.items()) for atom in _atomSelection)] if len(_atomSelection) > 1 else _atomSelection

            if len(atomSelection) > 0:
                self.stackSelections.append(atomSelection)

            self.stackSelections.append('or')  # union

            self.stackTerms = []
            self.stackFactors = []
            self.factor = {}

            return

        if self.depth == 1 or not self.__top_union_expr:
            while self.stackFactors:
                _factor = self.__consumeFactor_expressions(self.stackFactors.pop(), cifCheck=True)
                self.factor = self.__intersectionFactor_expressions(self.factor, None if 'atom_selection' not in _factor else _factor['atom_selection'])

        if self.unionFactor is not None and len(self.unionFactor) > 0:
            if 'atom_selection' not in self.unionFactor:
                self.unionFactor = self.__consumeFactor_expressions(self.unionFactor, cifCheck=True)
            if 'atom_selection' in self.unionFactor:
                _atomSelection = self.unionFactor['atom_selection']
                del self.unionFactor['atom_selection']
                __factor = self.__consumeFactor_expressions(self.unionFactor, cifCheck=True)
                if 'atom_selection' in __factor:
                    for _atom in __factor['atom_selection']:
                        if _atom not in _atomSelection:
                            _atomSelection.append(_atom)
                if len(_atomSelection) > 0:
                    self.factor['atom_selection'] = _atomSelection
            self.unionFactor = None

        if 'atom_selection' in self.factor and not isinstance(self.factor['atom_selection'], str):
            self.stackTerms.append(self.factor['atom_selection'])

    def consumeFactor_expressions(self, clauseName='atom selection expression', cifCheck=True):
        """ Consume factor expressions as atom selection if possible.
        """

        if self.stackFactors:
            self.stackFactors.pop()

        self.factor = self.__consumeFactor_expressions(self.factor, clauseName, cifCheck)

    def __consumeFactor_expressions(self, _factor, clauseName='atom selection expression', cifCheck=True):
        """ Consume factor expressions as atom selection if possible.
        """
        if not self.__hasPolySeq and not self.__hasNonPolySeq:
            return _factor

        if not self.__hasCoord:
            cifCheck = False

        if 'atom_num' in _factor and 'atom_id' not in _factor:
            g = None
            if self.lastComment is not None:
                if self.__cur_subtype == 'dist':
                    if self.dist_comment_pat.match(self.lastComment):
                        g = self.dist_comment_pat.search(self.lastComment).groups()
                        offset = len(self.atomSelectionSet) * 3
                        # _factor['comp_id'] = [g[offset]]
                        _factor['seq_id'] = [int(g[offset + 1])]
                        _factor['atom_id'] = [g[offset + 2]]
                        _factor['chain_id'] = [ps['auth_chain_id'] for ps in self.__polySeq if _factor['seq_id'][0] in ps['seq_id']]
                        if self.__hasNonPolySeq:
                            for np in self.__nonPolySeq:
                                _chainId = np['auth_chain_id']
                                if _chainId not in _factor['chain_id'] and _factor['seq_id'][0] in np['seq_id']:
                                    _factor['chain_id'].append(_chainId)
                        if len(_factor['chain_id']) == 0:
                            del _factor['chain_id']
                    elif self.dist_comment_pat2.match(self.lastComment):
                        g = self.dist_comment_pat2.search(self.lastComment).groups()
                        offset = len(self.atomSelectionSet) * 4
                        _factor['chain_id'] = [g[offset]]
                        # _factor['comp_id'] = [g[offset + 1]]
                        _factor['seq_id'] = [int(g[offset + 2])]
                        _factor['atom_id'] = [g[offset + 3]]
                elif self.__cur_subtype == 'dihed':
                    if self.dihed_comment_pat.match(self.lastComment):
                        g = self.dihed_comment_pat.search(self.lastComment).groups()
                        offset = len(self.atomSelectionSet) * 3
                        # _factor['comp_id'] = [g[offset]]
                        _factor['seq_id'] = [int(g[offset + 1])]
                        _factor['atom_id'] = [g[offset + 2]]
                        _factor['chain_id'] = [ps['auth_chain_id'] for ps in self.__polySeq if _factor['seq_id'][0] in ps['seq_id']]
                        if self.__hasNonPolySeq:
                            for np in self.__nonPolySeq:
                                _chainId = np['auth_chain_id']
                                if _chainId not in _factor['chain_id'] and _factor['seq_id'][0] in np['seq_id']:
                                    _factor['chain_id'].append(_chainId)
                        if len(_factor['chain_id']) == 0:
                            del _factor['chain_id']
            if g is None:
                _factor['atom_id'] = [None]
                if 'chain_id' in _factor:
                    del _factor['chain_id']
                if 'seq_id' in _factor:
                    del _factor['seq_id']

                self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                "The 'bynumber' clause has no effect "
                                "because the internal atom number is not included in the coordinate file.")

                return _factor

        if ('atom_id' in _factor and _factor['atom_id'][0] is None)\
           or ('atom_selection' in _factor and (_factor['atom_selection'] is None or len(_factor['atom_selection']) == 0)):
            return {'atom_selection': []}

        if not any(key for key in _factor if not (key == 'atom_selection' or key.startswith('auth'))):
            return _factor

        if 'alt_chain_id' in _factor:
            len_factor = len(_factor)

            if len_factor == 2 and 'chain_id' in _factor and len(_factor['chain_id']) == 0:
                if self.__largeModel:
                    _factor['chain_id'] = [self.__representativeAsymId]
                else:
                    _factor['atom_selection'] = ['*']
                    del _factor['chain_id']
                    return _factor

            elif len_factor == 1:
                _factor['atom_selection'] = ['*']
                return _factor

        if len(self.atomSelectionSet) == 0:
            self.__retrieveLocalSeqScheme()

        if 'atom_id' in _factor and len(_factor['atom_id']) == 1:
            self.__cur_auth_atom_id = _factor['atom_id'][0]
        elif 'atom_ids' in _factor and len(_factor['atom_ids']) == 1:
            self.__cur_auth_atom_id = _factor['atom_ids'][0]
        else:
            self.__cur_auth_atom_id = ''

        ambigAtomSelect = False
        if 'atom_id' not in _factor and 'atom_ids' not in _factor\
           and 'type_symbol' not in _factor and 'type_symbols' not in _factor:
            _factor['atom_not_specified'] = True
            if 'atom_selection' not in _factor:
                ambigAtomSelect = True

        elif 'chain_id' not in _factor and 'seq_id' not in _factor and 'seq_ids' not in _factor:
            if 'atom_selection' not in _factor:
                ambigAtomSelect = True

        if 'seq_id' not in _factor and 'seq_ids' not in _factor:
            _factor['seq_not_specified'] = True

        key = str(_factor)
        if key in self.__cachedDictForFactor:
            return copy.deepcopy(self.__cachedDictForFactor[key])

        len_warn_msg = len(self.__f)

        if 'chain_id' not in _factor or len(_factor['chain_id']) == 0:
            if self.__largeModel:
                _factor['chain_id'] = [self.__representativeAsymId]
            else:
                _factor['chain_id'] = [ps['auth_chain_id'] for ps in self.__polySeq]
                if self.__hasNonPolySeq:
                    for np in self.__nonPolySeq:
                        _chainId = np['auth_chain_id']
                        if _chainId not in _factor['chain_id']:
                            _factor['chain_id'].append(_chainId)

        if 'seq_id' not in _factor and 'seq_ids' not in _factor:
            if 'comp_ids' in _factor and len(_factor['comp_ids']) > 0\
               and ('comp_id' not in _factor or len(_factor['comp_id']) == 0):
                lenCompIds = len(_factor['comp_ids'])
                _compIdSelect = set()
                for chainId in _factor['chain_id']:
                    ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                    if ps is not None:
                        for realSeqId in ps['auth_seq_id']:
                            idx = ps['auth_seq_id'].index(realSeqId)
                            realCompId = ps['comp_id'][idx]
                            origCompId = ps['auth_comp_id'][idx]
                            if (lenCompIds == 1
                                and (re.match(toRegEx(translateToStdResName(_factor['comp_ids'][0], self.__ccU)), realCompId)
                                     or re.match(toRegEx(translateToStdResName(_factor['comp_ids'][0], self.__ccU)), origCompId)))\
                               or (lenCompIds == 2
                                   and (translateToStdResName(_factor['comp_ids'][0], self.__ccU) <= realCompId
                                        <= translateToStdResName(_factor['comp_ids'][1], self.__ccU)
                                        or translateToStdResName(_factor['comp_ids'][0], self.__ccU) <= origCompId
                                        <= translateToStdResName(_factor['comp_ids'][1], self.__ccU))):
                                _compIdSelect.add(realCompId)
                if self.__hasNonPolySeq:
                    for chainId in _factor['chain_id']:
                        npList = [np for np in self.__nonPolySeq if np['auth_chain_id'] == chainId]
                        for np in npList:
                            for realSeqId in np['auth_seq_id']:
                                idx = np['auth_seq_id'].index(realSeqId)
                                realCompId = np['comp_id'][idx]
                                origCompId = np['auth_comp_id'][idx]
                                if (lenCompIds == 1
                                    and (re.match(toRegEx(translateToStdResName(_factor['comp_ids'][0], self.__ccU)), realCompId)
                                         or re.match(toRegEx(translateToStdResName(_factor['comp_ids'][0], self.__ccU)), origCompId)))\
                                   or (lenCompIds == 2
                                       and (translateToStdResName(_factor['comp_ids'][0], self.__ccU) <= realCompId
                                            <= translateToStdResName(_factor['comp_ids'][1], self.__ccU)
                                            or translateToStdResName(_factor['comp_ids'][0], self.__ccU) <= origCompId
                                            <= translateToStdResName(_factor['comp_ids'][1], self.__ccU))):
                                    _compIdSelect.add(realCompId)
                _factor['comp_id'] = list(_compIdSelect)
                del _factor['comp_ids']

        if 'seq_ids' in _factor and len(_factor['seq_ids']) > 0\
           and ('seq_id' not in _factor or len(_factor['seq_id']) == 0):
            seqId = _factor['seq_ids'][0]
            _seqId = toRegEx(seqId)
            seqIds = []
            for chainId in _factor['chain_id']:
                ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                if ps is not None:
                    found = False
                    for realSeqId in ps['auth_seq_id']:
                        if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                            idx = ps['auth_seq_id'].index(realSeqId)
                            realCompId = ps['comp_id'][idx]
                            origCompId = ps['auth_comp_id'][idx]
                            _compIdList = [translateToStdResName(_compId, self.__ccU) for _compId in _factor['comp_id']]
                            if realCompId not in _compIdList and origCompId not in _compIdList:
                                continue
                        if re.match(_seqId, str(realSeqId)):
                            seqIds.append(realSeqId)
                            found = True
                    if not found:
                        for realSeqId in ps['auth_seq_id']:
                            if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                idx = ps['auth_seq_id'].index(realSeqId)
                                realCompId = ps['comp_id'][idx]
                                origCompId = ps['auth_comp_id'][idx]
                                _compIdList = [translateToStdResName(_compId, self.__ccU) for _compId in _factor['comp_id']]
                                if realCompId not in _compIdList and origCompId not in _compIdList:
                                    continue
                            seqKey = (chainId, realSeqId)
                            if seqKey in self.__authToLabelSeq:
                                _, realSeqId = self.__authToLabelSeq[seqKey]
                                if re.match(_seqId, str(realSeqId)):
                                    seqIds.append(realSeqId)
            if self.__hasNonPolySeq:
                for chainId in _factor['chain_id']:
                    npList = [np for np in self.__nonPolySeq if np['auth_chain_id'] == chainId]
                    for np in npList:
                        found = False
                        for realSeqId in np['auth_seq_id']:
                            if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                idx = np['auth_seq_id'].index(realSeqId)
                                realCompId = np['comp_id'][idx]
                                origCompId = np['auth_comp_id'][idx]
                                _compIdList = [translateToStdResName(_compId, self.__ccU) for _compId in _factor['comp_id']]
                                if realCompId not in _compIdList and origCompId not in _compIdList:
                                    continue
                            if re.match(_seqId, str(realSeqId)):
                                seqIds.append(realSeqId)
                                found = True
                        if not found:
                            for realSeqId in np['auth_seq_id']:
                                if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                    idx = np['auth_seq_id'].index(realSeqId)
                                    realCompId = np['comp_id'][idx]
                                    origCompId = np['auth_comp_id'][idx]
                                    _compIdList = [translateToStdResName(_compId, self.__ccU) for _compId in _factor['comp_id']]
                                    if realCompId not in _compIdList and origCompId not in _compIdList:
                                        continue
                                seqKey = (chainId, realSeqId)
                                if seqKey in self.__authToLabelSeq:
                                    _, realSeqId = self.__authToLabelSeq[seqKey]
                                    if re.match(_seqId, str(realSeqId)):
                                        seqIds.append(realSeqId)
            _factor['seq_id'] = list(set(seqIds))
            del _factor['seq_ids']

        if 'seq_id' not in _factor or len(_factor['seq_id']) == 0:
            seqIds = []
            for chainId in _factor['chain_id']:
                ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                if ps is not None:
                    for realSeqId in ps['auth_seq_id']:
                        if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                            idx = ps['auth_seq_id'].index(realSeqId)
                            realCompId = ps['comp_id'][idx]
                            origCompId = ps['auth_comp_id'][idx]
                            _compIdList = [translateToStdResName(_compId, self.__ccU) for _compId in _factor['comp_id']]
                            if realCompId not in _compIdList and origCompId not in _compIdList:
                                continue
                        seqIds.append(realSeqId)
            if self.__hasNonPolySeq:
                for chainId in _factor['chain_id']:
                    npList = [np for np in self.__nonPolySeq if np['auth_chain_id'] == chainId]
                    for np in npList:
                        for realSeqId in np['auth_seq_id']:
                            if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                idx = np['auth_seq_id'].index(realSeqId)
                                realCompId = np['comp_id'][idx]
                                origCompId = np['auth_comp_id'][idx]
                                _compIdList = [translateToStdResName(_compId, self.__ccU) for _compId in _factor['comp_id']]
                                if realCompId not in _compIdList and origCompId not in _compIdList:
                                    continue
                            seqIds.append(realSeqId)
            _factor['seq_id'] = list(set(seqIds))

        if 'atom_id' not in _factor and 'atom_ids' not in _factor:
            if 'type_symbols' in _factor and len(_factor['type_symbols']) > 0\
               and ('type_symbol' not in _factor or len(_factor['type_symbol']) == 0):
                lenTypeSymbols = len(_factor['type_symbols'])
                _typeSymbolSelect = set()
                _compIdSelect = set()
                for chainId in _factor['chain_id']:
                    ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                    if ps is not None:
                        _compIdSelect |= set(ps['comp_id'])
                if self.__hasNonPolySeq:
                    for chainId in _factor['chain_id']:
                        npList = [np for np in self.__nonPolySeq if np['auth_chain_id'] == chainId]
                        for np in npList:
                            _compIdSelect |= set(np['comp_id'])
                for compId in _compIdSelect:
                    if self.__ccU.updateChemCompDict(compId):
                        for cca in self.__ccU.lastAtomList:
                            realTypeSymbol = cca[self.__ccU.ccaTypeSymbol]
                            if (lenTypeSymbols == 1 and re.match(toRegEx(_factor['type_symbols'][0]), realTypeSymbol))\
                               or (lenTypeSymbols == 2 and _factor['type_symbols'][0] <= realTypeSymbol <= _factor['type_symbols'][1]):
                                _typeSymbolSelect.add(realTypeSymbol)
                _factor['type_symbol'] = list(_typeSymbolSelect)
                if len(_factor['type_symbol']) == 0:
                    _factor['atom_id'] = [None]
                del _factor['type_symbols']

            if 'type_symbol' in _factor:
                _atomIdSelect = set()
                _compIdSelect = set()
                for chainId in _factor['chain_id']:
                    ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                    if ps is not None:
                        _compIdSelect |= set(ps['comp_id'])
                if self.__hasNonPolySeq:
                    for chainId in _factor['chain_id']:
                        npList = [np for np in self.__nonPolySeq if np['auth_chain_id'] == chainId]
                        for np in npList:
                            _compIdSelect |= set(np['comp_id'])
                for compId in _compIdSelect:
                    if self.__ccU.updateChemCompDict(compId):
                        for cca in self.__ccU.lastAtomList:
                            if cca[self.__ccU.ccaTypeSymbol] in _factor['type_symbol']\
                               and cca[self.__ccU.ccaLeavingAtomFlag] != 'Y':
                                _atomIdSelect.add(cca[self.__ccU.ccaAtomId])
                _factor['atom_id'] = list(_atomIdSelect)
                if len(_factor['atom_id']) == 0:
                    _factor['atom_id'] = [None]

        if 'atom_ids' in _factor and len(_factor['atom_ids']) > 0\
           and ('atom_id' not in _factor or len(_factor['atom_id']) == 0):
            lenAtomIds = len(_factor['atom_ids'])
            _compIdSelect = set()
            for chainId in _factor['chain_id']:
                ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                if ps is not None:
                    for realSeqId in ps['auth_seq_id']:
                        if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                            if self.getOrigSeqId(ps, realSeqId) not in _factor['seq_id']:
                                continue
                        idx = ps['auth_seq_id'].index(realSeqId)
                        realCompId = ps['comp_id'][idx]
                        if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                            origCompId = ps['auth_comp_id'][idx]
                            _compIdList = [translateToStdResName(_compId, self.__ccU) for _compId in _factor['comp_id']]
                            if realCompId not in _compIdList and origCompId not in _compIdList:
                                continue
                        _compIdSelect.add(realCompId)
            if self.__hasNonPolySeq:
                for chainId in _factor['chain_id']:
                    npList = [np for np in self.__nonPolySeq if np['auth_chain_id'] == chainId]
                    for np in npList:
                        for realSeqId in np['auth_seq_id']:
                            if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                if self.getOrigSeqId(np, realSeqId, False) not in _factor['seq_id']:
                                    continue
                            idx = np['auth_seq_id'].index(realSeqId)
                            realCompId = np['comp_id'][idx]
                            if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                origCompId = np['auth_comp_id'][idx]
                                _compIdList = [translateToStdResName(_compId, self.__ccU) for _compId in _factor['comp_id']]
                                if realCompId not in _compIdList and origCompId not in _compIdList:
                                    continue
                            _compIdSelect.add(realCompId)

            _atomIdSelect = set()
            for compId in _compIdSelect:
                if self.__ccU.updateChemCompDict(compId):
                    refAtomIdList = [cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList]
                    for cca in self.__ccU.lastAtomList:
                        if cca[self.__ccU.ccaLeavingAtomFlag] != 'Y':
                            realAtomId = cca[self.__ccU.ccaAtomId]
                            if lenAtomIds == 1:
                                atomId = translateToStdAtomName(_factor['atom_ids'][0], compId, refAtomIdList, ccU=self.__ccU)
                                _, _, details = self.__nefT.get_valid_star_atom(compId, atomId, leave_unmatched=True)
                                if details is not None:
                                    _, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId, leave_unmatched=True)
                                    if details is None and atomId.rfind('1') != -1:
                                        idx = atomId.rindex('1')
                                        atomId = atomId[0:idx] + '3' + atomId[idx + 1:]
                                _atomId = toNefEx(toRegEx(atomId))
                                if re.match(_atomId, realAtomId):
                                    _atomIdSelect.add(realAtomId)
                                    _factor['alt_atom_id'] = _factor['atom_ids'][0]
                            elif lenAtomIds == 2:
                                atomId1 = translateToStdAtomName(_factor['atom_ids'][0], compId, refAtomIdList, ccU=self.__ccU)
                                atomId2 = translateToStdAtomName(_factor['atom_ids'][1], compId, refAtomIdList, ccU=self.__ccU)
                                _, _, details = self.__nefT.get_valid_star_atom(compId, atomId1, leave_unmatched=True)
                                if details is not None:
                                    _, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId1, leave_unmatched=True)
                                    if details is None and atomId1.rfind('1') != -1:
                                        idx = atomId1.rindex('1')
                                        atomId1 = atomId1[0:idx] + '3' + atomId1[idx + 1:]
                                _, _, details = self.__nefT.get_valid_star_atom(compId, atomId2, leave_unmatched=True)
                                if details is not None:
                                    _, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId2, leave_unmatched=True)
                                    if details is None and atomId2.rfind('1') != -1:
                                        idx = atomId2.rindex('1')
                                        atomId2 = atomId2[0:idx] + '3' + atomId2[idx + 1:]
                                if (atomId1 < atomId2 and atomId1 <= realAtomId <= atomId2)\
                                   or (atomId1 > atomId2 and atomId2 <= realAtomId <= atomId1):
                                    _atomIdSelect.add(realAtomId)
            _factor['atom_id'] = list(_atomIdSelect)

            if len(_factor['atom_id']) == 0:
                self.__preferAuthSeq = not self.__preferAuthSeq

                _compIdSelect = set()
                for chainId in _factor['chain_id']:
                    ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                    if ps is not None:
                        for realSeqId in ps['auth_seq_id']:
                            if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                if self.getOrigSeqId(ps, realSeqId) not in _factor['seq_id']:
                                    continue
                            idx = ps['auth_seq_id'].index(realSeqId)
                            realCompId = ps['comp_id'][idx]
                            if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                origCompId = ps['auth_comp_id'][idx]
                                _compIdList = [translateToStdResName(_compId, self.__ccU) for _compId in _factor['comp_id']]
                                if realCompId not in _compIdList and origCompId not in _compIdList:
                                    continue
                            _compIdSelect.add(realCompId)
                if self.__hasNonPolySeq:
                    for chainId in _factor['chain_id']:
                        npList = [np for np in self.__nonPolySeq if np['auth_chain_id'] == chainId]
                        for np in npList:
                            for realSeqId in np['auth_seq_id']:
                                if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                    if self.getOrigSeqId(np, realSeqId, False) not in _factor['seq_id']:
                                        continue
                                idx = np['auth_seq_id'].index(realSeqId)
                                realCompId = np['comp_id'][idx]
                                if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                    origCompId = np['auth_comp_id'][idx]
                                    _compIdList = [translateToStdResName(_compId, self.__ccU) for _compId in _factor['comp_id']]
                                    if realCompId not in _compIdList and origCompId not in _compIdList:
                                        continue
                                _compIdSelect.add(realCompId)

                _atomIdSelect = set()
                for compId in _compIdSelect:
                    if self.__ccU.updateChemCompDict(compId):
                        refAtomIdList = [cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList]
                        for cca in self.__ccU.lastAtomList:
                            if cca[self.__ccU.ccaLeavingAtomFlag] != 'Y':
                                realAtomId = cca[self.__ccU.ccaAtomId]
                                if lenAtomIds == 1:
                                    atomId = translateToStdAtomName(_factor['atom_ids'][0], compId, refAtomIdList, ccU=self.__ccU)
                                    _, _, details = self.__nefT.get_valid_star_atom(compId, atomId, leave_unmatched=True)
                                    if details is not None:
                                        _, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId, leave_unmatched=True)
                                        if details is None and atomId.rfind('1') != -1:
                                            idx = atomId.rindex('1')
                                            atomId = atomId[0:idx] + '3' + atomId[idx + 1:]
                                    _atomId = toNefEx(toRegEx(atomId))
                                    if re.match(_atomId, realAtomId):
                                        _atomIdSelect.add(realAtomId)
                                        _factor['alt_atom_id'] = _factor['atom_ids'][0]
                                elif lenAtomIds == 2:
                                    atomId1 = translateToStdAtomName(_factor['atom_ids'][0], compId, refAtomIdList, ccU=self.__ccU)
                                    atomId2 = translateToStdAtomName(_factor['atom_ids'][1], compId, refAtomIdList, ccU=self.__ccU)
                                    _, _, details = self.__nefT.get_valid_star_atom(compId, atomId1, leave_unmatched=True)
                                    if details is not None:
                                        _, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId1, leave_unmatched=True)
                                        if details is None and atomId1.rfind('1') != -1:
                                            idx = atomId1.rindex('1')
                                            atomId1 = atomId1[0:idx] + '3' + atomId1[idx + 1:]
                                    _, _, details = self.__nefT.get_valid_star_atom(compId, atomId2, leave_unmatched=True)
                                    if details is not None:
                                        _, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId2, leave_unmatched=True)
                                        if details is None and atomId2.rfind('1') != -1:
                                            idx = atomId2.rindex('1')
                                            atomId2 = atomId2[0:idx] + '3' + atomId2[idx + 1:]
                                    if (atomId1 < atomId2 and atomId1 <= realAtomId <= atomId2)\
                                       or (atomId1 > atomId2 and atomId2 <= realAtomId <= atomId1):
                                        _atomIdSelect.add(realAtomId)
                _factor['atom_id'] = list(_atomIdSelect)

                if len(_factor['atom_id']) > 0:
                    self.__authSeqId = 'auth_seq_id' if self.__preferAuthSeq else 'label_seq_id'
                    if len(self.atomSelectionSet) > 0:
                        self.__setLocalSeqScheme()
                else:
                    self.__preferAuthSeq = not self.__preferAuthSeq

                if len(_factor['atom_id']) == 0:
                    _factor['atom_id'] = [None]
                    _factor['alt_atom_id'] = _factor['atom_ids']
            # del _factor['atom_ids']

        if 'atom_id' not in _factor or len(_factor['atom_id']) == 0:
            _compIdSelect = set()
            _nonPolyCompIdSelect = []
            for chainId in _factor['chain_id']:
                ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                if ps is not None:
                    for realSeqId in ps['auth_seq_id']:
                        if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                            if self.getOrigSeqId(ps, realSeqId) not in _factor['seq_id']:
                                continue
                        idx = ps['auth_seq_id'].index(realSeqId)
                        realCompId = ps['comp_id'][idx]
                        if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                            origCompId = ps['auth_comp_id'][idx]
                            _compIdList = [translateToStdResName(_compId, self.__ccU) for _compId in _factor['comp_id']]
                            if realCompId not in _compIdList and origCompId not in _compIdList:
                                continue
                        _compIdSelect.add(realCompId)
            if self.__hasNonPolySeq:
                for chainId in _factor['chain_id']:
                    npList = [np for np in self.__nonPolySeq if np['auth_chain_id'] == chainId]
                    for np in npList:
                        for realSeqId in np['auth_seq_id']:
                            if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                if self.getOrigSeqId(np, realSeqId, False) not in _factor['seq_id']:
                                    continue
                            idx = np['auth_seq_id'].index(realSeqId)
                            realCompId = np['comp_id'][idx]
                            if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                origCompId = np['auth_comp_id'][idx]
                                _compIdList = [translateToStdResName(_compId, self.__ccU) for _compId in _factor['comp_id']]
                                if realCompId not in _compIdList and origCompId not in _compIdList:
                                    continue
                            _nonPolyCompIdSelect.append({'chain_id': chainId,
                                                         'seq_id': realSeqId,
                                                         'comp_id': realCompId})

            _atomIdSelect = set()
            for compId in _compIdSelect:
                if self.__ccU.updateChemCompDict(compId):
                    for cca in self.__ccU.lastAtomList:
                        if cca[self.__ccU.ccaLeavingAtomFlag] != 'Y':
                            realAtomId = cca[self.__ccU.ccaAtomId]
                            _atomIdSelect.add(realAtomId)

            for nonPolyCompId in _nonPolyCompIdSelect:
                _, coordAtomSite = self.getCoordAtomSiteOf(nonPolyCompId['chain_id'], nonPolyCompId['seq_id'], cifCheck)
                if coordAtomSite is not None:
                    for realAtomId in coordAtomSite['atom_id']:
                        _atomIdSelect.add(realAtomId)

            _factor['atom_id'] = list(_atomIdSelect)

            if len(_factor['atom_id']) == 0:
                self.__preferAuthSeq = not self.__preferAuthSeq

                _compIdSelect = set()
                _nonPolyCompIdSelect = []
                for chainId in _factor['chain_id']:
                    ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                    if ps is not None:
                        for realSeqId in ps['auth_seq_id']:
                            if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                if self.getOrigSeqId(ps, realSeqId) not in _factor['seq_id']:
                                    continue
                            idx = ps['auth_seq_id'].index(realSeqId)
                            realCompId = ps['comp_id'][idx]
                            if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                origCompId = ps['auth_comp_id'][idx]
                                _compIdList = [translateToStdResName(_compId, self.__ccU) for _compId in _factor['comp_id']]
                                if realCompId not in _compIdList and origCompId not in _compIdList:
                                    continue
                            _compIdSelect.add(realCompId)
                if self.__hasNonPolySeq:
                    for chainId in _factor['chain_id']:
                        npList = [np for np in self.__nonPolySeq if np['auth_chain_id'] == chainId]
                        for np in npList:
                            for realSeqId in np['auth_seq_id']:
                                if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                    if self.getOrigSeqId(np, realSeqId, False) not in _factor['seq_id']:
                                        continue
                                idx = np['auth_seq_id'].index(realSeqId)
                                realCompId = np['comp_id'][idx]
                                if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                    origCompId = np['auth_comp_id'][idx]
                                    _compIdList = [translateToStdResName(_compId, self.__ccU) for _compId in _factor['comp_id']]
                                    if realCompId not in _compIdList and origCompId not in _compIdList:
                                        continue
                                _nonPolyCompIdSelect.append({'chain_id': chainId,
                                                             'seq_id': realSeqId,
                                                             'comp_id': realCompId})

                _atomIdSelect = set()
                for compId in _compIdSelect:
                    if self.__ccU.updateChemCompDict(compId):
                        for cca in self.__ccU.lastAtomList:
                            if cca[self.__ccU.ccaLeavingAtomFlag] != 'Y':
                                realAtomId = cca[self.__ccU.ccaAtomId]
                                _atomIdSelect.add(realAtomId)

                for nonPolyCompId in _nonPolyCompIdSelect:
                    _, coordAtomSite = self.getCoordAtomSiteOf(nonPolyCompId['chain_id'], nonPolyCompId['seq_id'], cifCheck)
                    if coordAtomSite is not None:
                        for realAtomId in coordAtomSite['atom_id']:
                            _atomIdSelect.add(realAtomId)

                _factor['atom_id'] = list(_atomIdSelect)

                if len(_factor['atom_id']) > 0:
                    self.__authSeqId = 'auth_seq_id' if self.__preferAuthSeq else 'label_seq_id'
                    if len(self.atomSelectionSet) > 0:
                        self.__setLocalSeqScheme()
                else:
                    self.__preferAuthSeq = not self.__preferAuthSeq

                if len(_factor['atom_id']) == 0:
                    _factor['atom_id'] = [None]

        _atomSelection = []

        if _factor['atom_id'][0] is not None:
            foundCompId = self.__consumeFactor_expressions__(_factor, cifCheck, _atomSelection, isPolySeq=True, isChainSpecified=True)
            if self.__hasNonPolySeq:
                foundCompId |= self.__consumeFactor_expressions__(_factor, cifCheck, _atomSelection, isPolySeq=False, isChainSpecified=True, altPolySeq=self.__nonPolySeq)

            if not foundCompId and len(_factor['chain_id']) == 1 and len(self.__polySeq) > 1:
                self.__consumeFactor_expressions__(_factor, cifCheck, _atomSelection, isPolySeq=True, isChainSpecified=False)
                if self.__hasNonPolySeq:
                    self.__consumeFactor_expressions__(_factor, cifCheck, _atomSelection, isPolySeq=False, isChainSpecified=False, altPolySeq=self.__nonPolySeq)

        if 'atom_ids' in _factor:
            del _factor['atom_ids']
        if 'atom_not_specified' in _factor:
            del _factor['atom_not_specified']
        if 'seq_not_specified' in _factor:
            del _factor['seq_not_specified']

        atomSelection = [dict(s) for s in set(frozenset(atom.items()) for atom in _atomSelection)]

        valid = len(self.__f) == len_warn_msg

        if 'alt_chain_id' in _factor:
            for _atom in atomSelection:
                self.updateSegmentIdDict(_factor, _atom['chain_id'], valid)

        if 'atom_selection' not in _factor:
            _factor['atom_selection'] = atomSelection
        else:
            _atomSelection = []
            for _atom in _factor['atom_selection']:
                if _atom in atomSelection:
                    _atomSelection.append(_atom)
            _factor['atom_selection'] = _atomSelection

        if len(_factor['atom_selection']) == 0:
            __factor = copy.copy(_factor)
            del __factor['atom_selection']
            if _factor['atom_id'][0] is not None:
                error_type = "Insufficient atom selection" if 'atom_num' not in __factor else 'Atom not found'
                if self.__cur_subtype != 'plane':
                    if cifCheck:
                        if self.__cur_union_expr:
                            self.__g.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                            f"The {clauseName} has no effect for a factor {__factor}.")
                        else:
                            self.__f.append(f"[{error_type}] {self.__getCurrentRestraint()}"
                                            f"The {clauseName} has no effect for a factor {__factor}.")
                            self.__preferAuthSeq = not self.__preferAuthSeq
                            self.__authSeqId = 'auth_seq_id' if self.__preferAuthSeq else 'label_seq_id'
                            self.__setLocalSeqScheme()
                            # """
                            # if 'atom_id' in __factor and __factor['atom_id'][0] is None:
                            #     if 'label_seq_scheme' not in self.reasonsForReParsing:
                            #         self.reasonsForReParsing['label_seq_scheme'] = True
                            # """
                    else:
                        self.__g.append(f"[{error_type}] {self.__getCurrentRestraint()}"
                                        f"The {clauseName} has no effect for a factor {__factor}. "
                                        "Please update the sequence in the Macromolecules page.")
                else:
                    hint = f" Please verify that the planarity restraints match with the residue {_factor['comp_id'][0]!r}"\
                        if 'comp_id' in _factor and len(_factor['comp_id']) == 1 else ''
                    self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                    f"The {clauseName} has no effect for a factor {__factor}.{hint}")

        if 'chain_id' in _factor:
            del _factor['chain_id']
        if 'comp_id' in _factor:
            del _factor['comp_id']
        if 'seq_id' in _factor:
            del _factor['seq_id']
        if 'type_symbol' in _factor:
            del _factor['type_symbol']
        if 'atom_id' in _factor:
            del _factor['atom_id']
        if 'alt_chain_id' in _factor:
            del _factor['alt_chain_id']
        if 'alt_atom_id' in _factor:
            del _factor['alt_atom_id']

        if ambigAtomSelect or valid:
            self.__cachedDictForFactor[key] = copy.deepcopy(_factor)

        return _factor

    def __consumeFactor_expressions__(self, _factor, cifCheck, _atomSelection, isPolySeq=True, isChainSpecified=True, altPolySeq=None):
        atomSpecified = True
        if 'atom_not_specified' in _factor:
            atomSpecified = not _factor['atom_not_specified']
        seqSpecified = True
        if 'seq_not_specified' in _factor:
            seqSpecified = not _factor['seq_not_specified']
        foundCompId = False

        for chainId in (_factor['chain_id'] if isChainSpecified else [ps['auth_chain_id'] for ps in (self.__polySeq if isPolySeq else altPolySeq)]):
            psList = [ps for ps in (self.__polySeq if isPolySeq else altPolySeq) if ps['auth_chain_id'] == chainId]

            if len(psList) == 0:
                continue

            for ps in psList:

                for seqId in _factor['seq_id']:
                    _seqId_ = seqId
                    seqId = self.getRealSeqId(ps, seqId, isPolySeq)

                    if self.__reasons is not None:
                        if 'branched_remap' in self.__reasons and seqId in self.__reasons['branched_remap']:
                            fixedChainId, seqId = retrieveRemappedChainId(self.__reasons['branched_remap'], seqId)
                            if fixedChainId != chainId:
                                continue
                        if 'chain_id_remap' in self.__reasons and seqId in self.__reasons['chain_id_remap']:
                            fixedChainId, seqId = retrieveRemappedChainId(self.__reasons['chain_id_remap'], seqId)
                            if fixedChainId != chainId:
                                continue
                        elif 'chain_id_clone' in self.__reasons and seqId in self.__reasons['chain_id_clone']:
                            fixedChainId, seqId = retrieveRemappedChainId(self.__reasons['chain_id_clone'], seqId)
                            if fixedChainId != chainId:
                                continue
                        elif 'seq_id_remap' in self.__reasons:
                            _, seqId = retrieveRemappedSeqId(self.__reasons['seq_id_remap'], chainId, seqId)

                    if ps is not None and seqId in ps['auth_seq_id']:
                        compId = ps['comp_id'][ps['auth_seq_id'].index(seqId)]
                    elif 'gap_in_auth_seq' in ps and seqId is not None:
                        compId = None
                        min_auth_seq_id = ps['auth_seq_id'][0]
                        max_auth_seq_id = ps['auth_seq_id'][-1]
                        if min_auth_seq_id <= seqId <= max_auth_seq_id:
                            _seqId_ = seqId + 1
                            while _seqId_ <= max_auth_seq_id:
                                if _seqId_ in ps['auth_seq_id']:
                                    break
                                _seqId_ += 1
                            if _seqId_ not in ps['auth_seq_id']:
                                _seqId_ = seqId - 1
                                while _seqId_ >= min_auth_seq_id:
                                    if _seqId_ in ps['auth_seq_id']:
                                        break
                                    _seqId_ -= 1
                            if _seqId_ in ps['auth_seq_id']:
                                idx = ps['auth_seq_id'].index(_seqId_) - _seqId_ - seqId
                                try:
                                    seqId = ps['auth_seq_id'][idx]
                                    compId = ps['comp_id'][idx]
                                except IndexError:
                                    pass
                    else:
                        compId = None

                    if not isPolySeq and compId is None:
                        if 'alt_auth_seq_id' in ps and seqId in ps['alt_auth_seq_id']:
                            idx = ps['alt_auth_seq_id'].index(seqId)
                            seqId = ps['seq_id'][idx]
                            compId = ps['comp_id'][idx]
                        elif seqId in ps['seq_id']:
                            idx = ps['seq_id'].index(seqId)
                            compId = ps['comp_id'][idx]
                            _seqId_ = ps['auth_seq_id'][idx]

                    seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCheck)

                    if compId is None and seqKey in self.__authToLabelSeq:
                        _, seqId = self.__authToLabelSeq[seqKey]
                        if ps is not None and seqId in ps['auth_seq_id']:
                            compId = ps['comp_id'][ps['auth_seq_id'].index(seqId)]
                            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCheck)

                    if compId is None and coordAtomSite is not None and ps is not None and seqKey[1] in ps['auth_seq_id']:
                        compId = ps['comp_id'][ps['auth_seq_id'].index(seqKey[1])]

                    if coordAtomSite is None and not isPolySeq:
                        try:
                            idx = ps['auth_seq_id'].index(seqId)
                            seqId = ps['seq_id'][idx]
                            compId = ps['comp_id'][idx]
                            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCheck)
                        except ValueError:
                            pass

                    if compId is None:
                        continue

                    if self.__reasons is not None:
                        if 'non_poly_remap' in self.__reasons and compId in self.__reasons['non_poly_remap']\
                           and seqId in self.__reasons['non_poly_remap'][compId]:
                            fixedChainId, seqId = retrieveRemappedNonPoly(self.__reasons['non_poly_remap'], chainId, seqId, compId)
                            if fixedChainId != chainId:
                                continue

                    _seqId = seqId
                    if not isPolySeq and 'alt_auth_seq_id' in ps and seqId in ps['auth_seq_id'] and seqId not in ps['alt_auth_seq_id']:
                        seqId = next(_altSeqId for _seqId, _altSeqId in zip(ps['auth_seq_id'], ps['alt_auth_seq_id']) if _seqId == seqId)
                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCheck)

                    if not isPolySeq and isChainSpecified and self.doesNonPolySeqIdMatchWithPolySeqUnobs(_factor['chain_id'][0], _seqId_):
                        continue

                    foundCompId = True

                    updatePolySeqRst(self.__polySeqRst, chainId, seqId, compId)

                    atomSiteAtomId = None if coordAtomSite is None else coordAtomSite['atom_id']

                    for atomId in _factor['atom_id']:
                        origAtomId = _factor['atom_id'] if 'alt_atom_id' not in _factor else _factor['alt_atom_id']

                        atomId = atomId.upper()

                        if compId not in monDict3 and self.__mrAtomNameMapping is not None and (_seqId in ps['auth_seq_id'] or _seqId_ in ps['auth_seq_id']):
                            if _seqId in ps['auth_seq_id']:
                                authCompId = ps['auth_comp_id'][ps['auth_seq_id'].index(_seqId)]
                            else:
                                authCompId = ps['auth_comp_id'][ps['auth_seq_id'].index(_seqId_)]
                            atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, _seqId, authCompId, atomId, coordAtomSite)
                            if coordAtomSite is not None and atomId not in atomSiteAtomId:
                                if self.__reasons is not None and 'branched_remap' in self.__reasons:
                                    _seqId_ = retrieveOriginalSeqIdFromMRMap(self.__reasons['branched_remap'], chainId, seqId)
                                    if _seqId_ != seqId:
                                        _, _, atomId = retrieveAtomIdentFromMRMap(self.__mrAtomNameMapping, _seqId_, authCompId, atomId, coordAtomSite)
                                elif seqId != _seqId:
                                    atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, authCompId, atomId, coordAtomSite)

                        atomIds = self.getAtomIdList(_factor, compId, atomId)

                        # @see: https://bmrb.io/ref_info/atom_nom.tbl
                        if self.__trust_bmrb_ref_info:
                            pass

                        # @see: https://bmrb.io/macro/files/xplor_to_iupac.Nov140620
                        else:
                            if compId == 'ASN':
                                if atomId == 'HD21':
                                    _atomId = atomId[:-1] + '2'
                                    if self.__nefT.validate_comp_atom(compId, _atomId):
                                        atomIds = self.__nefT.get_valid_star_atom(compId, _atomId)[0]
                                elif atomId == 'HD22':
                                    _atomId = atomId[:-1] + '1'
                                    if self.__nefT.validate_comp_atom(compId, _atomId):
                                        atomIds = self.__nefT.get_valid_star_atom(compId, _atomId)[0]
                            elif compId == 'GLN':
                                if atomId == 'HE21':
                                    _atomId = atomId[:-1] + '2'
                                    if self.__nefT.validate_comp_atom(compId, _atomId):
                                        atomIds = self.__nefT.get_valid_star_atom(compId, _atomId)[0]
                                elif atomId == 'HE22':
                                    _atomId = atomId[:-1] + '1'
                                    if self.__nefT.validate_comp_atom(compId, _atomId):
                                        atomIds = self.__nefT.get_valid_star_atom(compId, _atomId)[0]

                        if coordAtomSite is not None\
                           and not any(_atomId for _atomId in atomIds if _atomId in atomSiteAtomId):
                            if atomId in atomSiteAtomId:
                                atomIds = [atomId]
                            elif 'alt_atom_id' in _factor:
                                _atomId_ = toNefEx(toRegEx(_factor['alt_atom_id']))
                                _atomIds_ = [_atomId for _atomId in atomSiteAtomId if re.match(_atomId_, _atomId)]
                                if len(_atomIds_) > 0:
                                    atomIds = _atomIds_

                        for _atomId in atomIds:
                            ccdCheck = not cifCheck

                            if cifCheck:
                                _atom = None
                                if coordAtomSite is not None:
                                    if _atomId in atomSiteAtomId:
                                        _atom = {}
                                        _atom['comp_id'] = coordAtomSite['comp_id']
                                        _atom['type_symbol'] = coordAtomSite['type_symbol'][atomSiteAtomId.index(_atomId)]
                                    elif 'alt_atom_id' in coordAtomSite and _atomId in coordAtomSite['alt_atom_id']:
                                        _atom = {}
                                        _atom['comp_id'] = coordAtomSite['comp_id']
                                        _atom['type_symbol'] = coordAtomSite['type_symbol'][coordAtomSite['alt_atom_id'].index(_atomId)]
                                        self.__authAtomId = 'auth_atom_id'
                                    elif self.__preferAuthSeq and atomSpecified:
                                        _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCheck, asis=False)
                                        if _coordAtomSite is not None:
                                            _compId = _coordAtomSite['comp_id']
                                            _atomId = self.getAtomIdList(_factor, _compId, atomId)[0]
                                            if _atomId in _coordAtomSite['atom_id']:
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['atom_id'].index(_atomId)]
                                                if self.__ccU.updateChemCompDict(compId):
                                                    cca = next((cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == _atomId), None)
                                                    if cca is None or (cca is not None and cca[self.__ccU.ccaLeavingAtomFlag] == 'Y'):
                                                        if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                            self.reasonsForReParsing['label_seq_scheme'] = True
                                                """
                                                self.__preferAuthSeq = False
                                                self.__authSeqId = 'label_seq_id'
                                                seqKey = _seqKey
                                                chainId, seqId = seqKey
                                                if len(self.atomSelectionSet) > 0:
                                                    self.__setLocalSeqScheme()
                                                """
                                            elif 'alt_atom_id' in _coordAtomSite and _atomId in _coordAtomSite['alt_atom_id']:
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['alt_atom_id'].index(_atomId)]
                                                if self.__ccU.updateChemCompDict(compId):
                                                    cca = next((cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == _atomId), None)
                                                    if cca is None or (cca is not None and cca[self.__ccU.ccaLeavingAtomFlag] == 'Y'):
                                                        if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                            self.reasonsForReParsing['label_seq_scheme'] = True
                                                """
                                                self.__preferAuthSeq = False
                                                self.__authSeqId = 'label_seq_id'
                                                self.__authAtomId = 'auth_atom_id'
                                                seqKey = _seqKey
                                                chainId, seqId = seqKey
                                                if len(self.atomSelectionSet) > 0:
                                                    self.__setLocalSeqScheme()
                                                """
                                    elif _seqId_ in ps['auth_seq_id'] and atomSpecified:
                                        self.__preferAuthSeq = True
                                        _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId_, cifCheck)
                                        if _coordAtomSite is not None:
                                            _compId = _coordAtomSite['comp_id']
                                            _atomId = self.getAtomIdList(_factor, _compId, atomId)[0]
                                            if _atomId in _coordAtomSite['atom_id']:
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['atom_id'].index(_atomId)]
                                                self.__authSeqId = 'auth_seq_id'
                                                seqKey = _seqKey
                                                chainId, seqId = seqKey
                                                if len(self.atomSelectionSet) > 0:
                                                    self.__setLocalSeqScheme()
                                            elif 'alt_atom_id' in _coordAtomSite and _atomId in _coordAtomSite['alt_atom_id']:
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['alt_atom_id'].index(_atomId)]
                                                self.__authSeqId = 'auth_seq_id'
                                                self.__authAtomId = 'auth_atom_id'
                                                seqKey = _seqKey
                                                chainId, seqId = seqKey
                                                if len(self.atomSelectionSet) > 0:
                                                    self.__setLocalSeqScheme()
                                            else:
                                                self.__preferAuthSeq = False
                                        else:
                                            self.__preferAuthSeq = False

                                elif self.__preferAuthSeq and atomSpecified:
                                    if len(self.atomSelectionSet) == 0:
                                        _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCheck, asis=False)
                                        if _coordAtomSite is not None:
                                            _compId = _coordAtomSite['comp_id']
                                            _atomId = self.getAtomIdList(_factor, _compId, atomId)[0]
                                            if _atomId in _coordAtomSite['atom_id']:
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['atom_id'].index(_atomId)]
                                                if self.__ccU.updateChemCompDict(compId):
                                                    cca = next((cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == _atomId), None)
                                                    if cca is None or (cca is not None and cca[self.__ccU.ccaLeavingAtomFlag] == 'Y'):
                                                        if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                            self.reasonsForReParsing['label_seq_scheme'] = True
                                                """
                                                self.__preferAuthSeq = False
                                                self.__authSeqId = 'label_seq_id'
                                                seqKey = _seqKey
                                                chainId, seqId = seqKey
                                                if len(self.atomSelectionSet) > 0:
                                                    self.__setLocalSeqScheme()
                                                """
                                            elif 'alt_atom_id' in _coordAtomSite and _atomId in _coordAtomSite['alt_atom_id']:
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['alt_atom_id'].index(_atomId)]
                                                if self.__ccU.updateChemCompDict(compId):
                                                    cca = next((cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == _atomId), None)
                                                    if cca is None or (cca is not None and cca[self.__ccU.ccaLeavingAtomFlag] == 'Y'):
                                                        if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                            self.reasonsForReParsing['label_seq_scheme'] = True
                                                """
                                                self.__preferAuthSeq = False
                                                self.__authSeqId = 'label_seq_id'
                                                self.__authAtomId = 'auth_atom_id'
                                                seqKey = _seqKey
                                                chainId, seqId = seqKey
                                                if len(self.atomSelectionSet) > 0:
                                                    self.__setLocalSeqScheme()
                                                """
                                elif _seqId_ in ps['auth_seq_id'] and atomSpecified:
                                    if len(self.atomSelectionSet) == 0:
                                        self.__preferAuthSeq = True
                                        _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId_, cifCheck)
                                        if _coordAtomSite is not None:
                                            _compId = _coordAtomSite['comp_id']
                                            _atomId = self.getAtomIdList(_factor, _compId, atomId)[0]
                                            if _atomId in _coordAtomSite['atom_id']:
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['atom_id'].index(_atomId)]
                                                self.__authSeqId = 'auth_seq_id'
                                                seqKey = _seqKey
                                                chainId, seqId = seqKey
                                                if len(self.atomSelectionSet) > 0:
                                                    self.__setLocalSeqScheme()
                                            elif 'alt_atom_id' in _coordAtomSite and _atomId in _coordAtomSite['alt_atom_id']:
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['alt_atom_id'].index(_atomId)]
                                                self.__authSeqId = 'auth_seq_id'
                                                self.__authAtomId = 'auth_atom_id'
                                                seqKey = _seqKey
                                                chainId, seqId = seqKey
                                                if len(self.atomSelectionSet) > 0:
                                                    self.__setLocalSeqScheme()
                                            else:
                                                self.__preferAuthSeq = False
                                        else:
                                            self.__preferAuthSeq = False

                                if _atom is not None:
                                    _compIdList = None if 'comp_id' not in _factor else [translateToStdResName(_compId, self.__ccU) for _compId in _factor['comp_id']]
                                    if ('comp_id' not in _factor or _atom['comp_id'] in _compIdList)\
                                       and ('type_symbol' not in _factor or _atom['type_symbol'] in _factor['type_symbol']):
                                        selection = {'chain_id': chainId, 'seq_id': seqId, 'comp_id': _atom['comp_id'], 'atom_id': _atomId}
                                        if len(self.__cur_auth_atom_id) > 0:
                                            selection['auth_atom_id'] = self.__cur_auth_atom_id
                                        if not atomSpecified or not seqSpecified:
                                            if self.__ccU.updateChemCompDict(compId):
                                                cca = next((cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == _atomId), None)
                                                if cca is None or (cca is not None and cca[self.__ccU.ccaLeavingAtomFlag] == 'Y'):
                                                    continue
                                        _atomSelection.append(selection)
                                else:
                                    ccdCheck = True

                            if (len(_factor['chain_id']) > 1 or len(_factor['seq_id']) > 1) and not atomSpecified:
                                continue

                            if isPolySeq and 'ambig_auth_seq_id' in ps and _seqId in ps['ambig_auth_seq_id']:
                                continue

                            if not isPolySeq and 'alt_auth_seq_id' in ps and _seqId in ps['auth_seq_id'] and _seqId not in ps['alt_auth_seq_id']:
                                continue

                            if isinstance(origAtomId, str) and origAtomId.startswith('*'):
                                continue

                            if ccdCheck and compId is not None:
                                _compIdList = None if 'comp_id' not in _factor else [translateToStdResName(_compId, self.__ccU) for _compId in _factor['comp_id']]
                                if self.__ccU.updateChemCompDict(compId) and ('comp_id' not in _factor or compId in _compIdList):
                                    if len(origAtomId) > 1:
                                        typeSymbols = set()
                                        for _atomId_ in origAtomId:
                                            typeSymbol = next((cca[self.__ccU.ccaTypeSymbol] for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == _atomId_), None)
                                            if typeSymbol is not None:
                                                typeSymbols.add(typeSymbol)
                                                if len(typeSymbols) > 1:
                                                    break
                                        if len(typeSymbols) > 1:
                                            continue
                                    cca = next((cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == _atomId), None)
                                    if cca is not None and cca[self.__ccU.ccaLeavingAtomFlag] == 'Y' and (not atomSpecified or not seqSpecified):
                                        continue
                                    if cca is not None and ('type_symbol' not in _factor or cca[self.__ccU.ccaTypeSymbol] in _factor['type_symbol']):
                                        selection = {'chain_id': chainId, 'seq_id': seqId, 'comp_id': compId, 'atom_id': _atomId}
                                        if len(self.__cur_auth_atom_id) > 0:
                                            selection['auth_atom_id'] = self.__cur_auth_atom_id
                                        if _atomId.startswith('HOP') and isinstance(origAtomId, str) and '*' in origAtomId:
                                            continue
                                        if not seqSpecified:
                                            continue
                                        _atomSelection.append(selection)
                                        if cifCheck and seqKey not in self.__coordUnobsRes and self.__ccU.lastChemCompDict['_chem_comp.pdbx_release_status'] == 'REL':
                                            if self.__cur_subtype != 'plane' and coordAtomSite is not None:
                                                checked = False
                                                if seqId == 1 or (chainId, seqId - 1) in self.__coordUnobsRes or seqId == ps['auth_seq_id'][0]:
                                                    if coordAtomSite is not None and ((_atomId in aminoProtonCode and 'H1' in atomSiteAtomId)
                                                                                      or _atomId == 'P' or _atomId.startswith('HOP')):
                                                        checked = True
                                                if _atomId[0] in protonBeginCode:
                                                    bondedTo = self.__ccU.getBondedAtoms(compId, _atomId)
                                                    if len(bondedTo) > 0:
                                                        if coordAtomSite is not None and bondedTo[0] in atomSiteAtomId and cca[self.__ccU.ccaLeavingAtomFlag] != 'Y':
                                                            checked = True
                                                            if len(origAtomId) == 1:
                                                                _atomSelection[-1]['hydrogen_not_instantiated'] = True
                                                                self.__f.append(f"[Hydrogen not instantiated] {self.__getCurrentRestraint()}"
                                                                                f"{chainId}:{seqId}:{compId}:{origAtomId} is not properly instantiated in the coordinates. "
                                                                                "Please re-upload the model file.")
                                                if not checked and not self.__cur_union_expr:
                                                    if chainId in LARGE_ASYM_ID:
                                                        if isPolySeq and not self.__preferAuthSeq\
                                                           and ('label_seq_offset' not in self.reasonsForReParsing
                                                                or chainId not in self.reasonsForReParsing['label_seq_offset']):
                                                            if 'label_seq_offset' not in self.reasonsForReParsing:
                                                                self.reasonsForReParsing['label_seq_offset'] = {}
                                                            offset = self.getLabelSeqOffsetDueToUnobs(ps)
                                                            self.reasonsForReParsing['label_seq_offset'][chainId] = offset
                                                            if offset != 0:
                                                                self.reasonsForReParsing['label_seq_scheme'] = True
                                                        if seqId < 1 and len(self.__polySeq) == 1:
                                                            self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                                                            f"{chainId}:{seqId}:{compId}:{origAtomId} is not present in the coordinates. "
                                                                            f"The residue number '{seqId}' is not present "
                                                                            f"in polymer sequence of chain {chainId} of the coordinates. "
                                                                            "Please update the sequence in the Macromolecules page.")
                                                        else:
                                                            self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                                                            f"{chainId}:{seqId}:{compId}:{origAtomId} is not present in the coordinates.")
                                    elif cca is None and 'type_symbol' not in _factor and 'atom_ids' not in _factor:
                                        if seqId == 1 or (chainId, seqId - 1) in self.__coordUnobsRes or seqId == ps['auth_seq_id'][0]:
                                            if coordAtomSite is not None and ((_atomId in aminoProtonCode and 'H1' in atomSiteAtomId)
                                                                              or _atomId == 'P' or _atomId.startswith('HOP')):
                                                continue
                                        # """
                                        # if self.__reasons is None and seqKey in self.__authToLabelSeq:
                                        #     _, _seqId = self.__authToLabelSeq[seqKey]
                                        #     if ps is not None and _seqId in ps['auth_seq_id']:
                                        #         _compId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                                        #         if self.__ccU.updateChemCompDict(_compId):
                                        #             cca = next((cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == _atomId), None)
                                        #             if cca is not None:
                                        #                 if 'label_seq_scheme' not in self.reasonsForReParsing:
                                        #                     self.reasonsForReParsing['label_seq_scheme'] = True
                                        # """
                                        if cifCheck and self.__cur_subtype != 'plane'\
                                           and 'seq_id' in _factor and len(_factor['seq_id']) == 1\
                                           and (self.__reasons is None or 'non_poly_remap' not in self.__reasons)\
                                           and not self.__cur_union_expr:
                                            if chainId in LARGE_ASYM_ID:
                                                if seqId < 1 and len(self.__polySeq) == 1:
                                                    self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                                                    f"{chainId}:{seqId}:{compId}:{origAtomId} is not present in the coordinates. "
                                                                    f"The residue number '{seqId}' is not present in polymer sequence of chain {chainId} of the coordinates. "
                                                                    "Please update the sequence in the Macromolecules page.")
                                                elif seqSpecified:
                                                    self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                                                    f"{chainId}:{seqId}:{compId}:{origAtomId} is not present in the coordinates.")

        return foundCompId

    def getOrigSeqId(self, ps, seqId, isPolySeq=True):
        # if self.__reasons is not None and 'label_seq_scheme' in self.__reasons and self.__reasons['label_seq_scheme'] or not self.__preferAuthSeq:
        if not self.__preferAuthSeq:
            chainId = ps['chain_id']
            offset = 0
            if isPolySeq and self.__reasons is not None and 'label_seq_offset' in self.__reasons and chainId in self.__reasons['label_seq_offset']:
                offset = self.__reasons['label_seq_offset'][chainId]
            seqKey = (ps['chain_id' if isPolySeq else 'auth_chain_id'], seqId)
            if seqKey in self.__authToLabelSeq:
                _chainId, _seqId = self.__authToLabelSeq[seqKey]
                if _seqId in ps['seq_id']:
                    return _seqId + offset
        if seqId in ps['auth_seq_id']:
            return seqId
        # if seqId in ps['seq_id']:
        #     return ps['auth_seq_id'][ps['seq_id'].index(seqId)]
        return seqId

    def getRealSeqId(self, ps, seqId, isPolySeq=True):
        # if self.__reasons is not None and 'label_seq_scheme' in self.__reasons and self.__reasons['label_seq_scheme'] or not self.__preferAuthSeq:
        if not self.__preferAuthSeq:
            chainId = ps['chain_id']
            offset = 0
            if isPolySeq and self.__reasons is not None and 'label_seq_offset' in self.__reasons and chainId in self.__reasons['label_seq_offset']:
                offset = self.__reasons['label_seq_offset'][chainId]
            seqKey = (ps['chain_id' if isPolySeq else 'auth_chain_id'], seqId + offset)
            if seqKey in self.__labelToAuthSeq:
                _chainId, _seqId = self.__labelToAuthSeq[seqKey]
                if _seqId in ps['auth_seq_id']:
                    return _seqId
        if seqId in ps['auth_seq_id']:
            return seqId
        # if seqId in ps['seq_id']:
        #     return ps['auth_seq_id'][ps['seq_id'].index(seqId)]
        return seqId

    def getRealChainId(self, chainId):
        if self.__reasons is not None and 'segment_id_mismatch' in self.__reasons and chainId in self.__reasons['segment_id_mismatch']:
            _chainId = self.__reasons['segment_id_mismatch'][chainId]
            if _chainId is not None:
                chainId = _chainId
        return chainId

    def updateSegmentIdDict(self, factor, chainId, valid):
        if self.__reasons is not None or 'alt_chain_id' not in factor\
           or len(self.reasonsForReParsing) == 0 or 'segment_id_mismatch' not in self.reasonsForReParsing:
            return
        altChainId = factor['alt_chain_id']
        if altChainId not in self.reasonsForReParsing['segment_id_mismatch']:
            return
        if chainId not in self.reasonsForReParsing['segment_id_match_stats'][altChainId]:
            self.reasonsForReParsing['segment_id_match_stats'][altChainId][chainId] = 0
        if valid:
            self.reasonsForReParsing['segment_id_match_stats'][altChainId][chainId] += 1
        stats = self.reasonsForReParsing['segment_id_match_stats'][altChainId]
        _chainId = max(stats, key=lambda key: stats[key])[0]
        self.reasonsForReParsing['segment_id_mismatch'][altChainId] = _chainId
        # try to avoid multiple segment_id assignments
        for k, _stats in self.reasonsForReParsing['segment_id_match_stats'].items():
            if k == altChainId:
                continue
            if chainId in _stats:
                _stats[chainId] -= 1

    def getCoordAtomSiteOf(self, chainId, seqId, cifCheck=True, asis=True):
        seqKey = (chainId, seqId)
        if asis:
            return seqKey, self.__coordAtomSite[seqKey] if cifCheck and seqKey in self.__coordAtomSite else None
        if seqKey in self.__labelToAuthSeq:
            seqKey = self.__labelToAuthSeq[seqKey]
            return seqKey, self.__coordAtomSite[seqKey] if cifCheck and seqKey in self.__coordAtomSite else None
        return seqKey, None

    def getAtomIdList(self, factor, compId, atomId):
        key = (compId, atomId, 'alt_atom_id' in factor)
        if key in self.__cachedDictForAtomIdList:
            return copy.copy(self.__cachedDictForAtomIdList[key])
        atomIds, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId, leave_unmatched=True)
        if 'alt_atom_id' in factor and details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
            atomIds, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)
            if atomId[-1].isdigit() and int(atomId[-1]) <= len(atomIds):
                atomIds = [atomIds[int(atomId[-1]) - 1]]

        if details is not None:
            _atomId = toNefEx(translateToStdAtomName(atomId, compId, ccU=self.__ccU))
            if _atomId != atomId:
                if atomId.startswith('HT') and len(_atomId) == 2:
                    _atomId = 'H'
                atomIds = self.__nefT.get_valid_star_atom_in_xplor(compId, _atomId)[0]
        self.__cachedDictForAtomIdList[key] = atomIds
        return atomIds

    def getLabelSeqOffsetDueToUnobs(self, ps):
        authChainId = ps['auth_chain_id']
        for labelSeqId, authSeqId in zip(ps['seq_id'], ps['auth_seq_id']):
            seqKey = (authChainId, authSeqId)
            if seqKey not in self.__coordUnobsRes:
                return labelSeqId - 1
        return ps['seq_id'][-1] - 1

    def doesNonPolySeqIdMatchWithPolySeqUnobs(self, chainId, seqId):
        _ps_ = next((_ps_ for _ps_ in self.__polySeq if _ps_['auth_chain_id'] == chainId), None)
        if _ps_ is not None:
            _chainId_ = _ps_['chain_id']
            _seqKey_ = (_chainId_, seqId)
            if _seqKey_ in self.__labelToAuthSeq:
                if self.__labelToAuthSeq[_seqKey_] != _seqKey_:
                    if self.__labelToAuthSeq[_seqKey_] in self.__coordUnobsRes:
                        return True
                else:
                    max_label_seq_id = _ps_['seq_id'][-1]
                    _seqId_ = seqId + 1
                    while _seqId_ <= max_label_seq_id:
                        if _seqId_ in _ps_['seq_id']:
                            _seqKey_ = (_chainId_, _seqId_)
                            if _seqKey_ in self.__labelToAuthSeq and self.__labelToAuthSeq[_seqKey_] != _seqKey_:
                                break
                        _seqId_ += 1
                    if _seqId_ not in _ps_['seq_id']:
                        min_label_seq_id = _ps_['seq_id'][0]
                        _seqId_ = seqId - 1
                        while _seqId_ >= min_label_seq_id:
                            if _seqId_ in _ps_['seq_id']:
                                _seqKey_ = (_chainId_, _seqId_)
                                if _seqKey_ in self.__labelToAuthSeq and self.__labelToAuthSeq[_seqKey_] != _seqKey_:
                                    break
                            _seqId_ -= 1
                    if _seqId_ in _ps_['seq_id']:
                        _seqKey_ = (_chainId_, _seqId_)
                        if _seqKey_ in self.__labelToAuthSeq and self.__labelToAuthSeq[_seqKey_] != _seqKey_:
                            __chainId__, __seqId__ = self.__labelToAuthSeq[_seqKey_]
                            __seqKey__ = (__chainId__, __seqId__ - (_seqId_ - seqId))
                            if __seqKey__ in self.__coordUnobsRes:
                                return True
        return False

    def intersectionFactor_expressions(self, atomSelection=None):
        self.consumeFactor_expressions(cifCheck=False)

        self.factor = self.__intersectionFactor_expressions(self.factor, atomSelection)

    def __intersectionFactor_expressions(self, _factor, atomSelection=None):  # pylint: disable=no-self-use
        if 'atom_selection' not in _factor:
            _factor['atom_selection'] = atomSelection
            return _factor

        if atomSelection is None or len(atomSelection) == 0:
            _factor['atom_selection'] = []

        elif isinstance(atomSelection[0], str) and atomSelection[0] == '*':
            return _factor

        _atomSelection = []
        for _atom in _factor['atom_selection']:
            if isinstance(_atom, str) and _atom == '*':
                _factor['atom_selection'] = atomSelection
                return _factor
            if _atom in atomSelection:
                _atomSelection.append(_atom)
            elif 'hydrogen_not_instantiated' in _atom and _atom['hydrogen_not_instantiated']:
                chain_id = _atom['chain_id']
                seq_id = _atom['seq_id']
                if any(_atom2 for _atom2 in atomSelection if _atom2['chain_id'] == chain_id and _atom2['seq_id'] == seq_id):
                    _atomSelection.append(_atom)

        _factor['atom_selection'] = _atomSelection

        return _factor

    def __intersectionAtom_selections(self, _selection1, _selection2):  # pylint: disable=no-self-use
        if _selection1 is None or len(_selection1) == 0 or _selection2 is None or len(_selection2) == 0:
            return []

        if isinstance(_selection2[0], str) and _selection2[0] == '*':
            return _selection1

        hasAuthSeqId1 = any(_atom for _atom in _selection1 if 'auth_atom_id' in _atom)
        hasAuthSeqId2 = any(_atom for _atom in _selection2 if 'auth_atom_id' in _atom)

        _atomSelection = []

        if not hasAuthSeqId1 and not hasAuthSeqId2:
            for _atom in _selection1:
                if isinstance(_atom, str) and _atom == '*':
                    return _selection2
                if _atom in _selection2:
                    _atomSelection.append(_atom)
                elif 'hydrogen_not_instantiated' in _atom and _atom['hydrogen_not_instantiated']:
                    chain_id = _atom['chain_id']
                    seq_id = _atom['seq_id']
                    if any(_atom2 for _atom2 in _selection2 if _atom2['chain_id'] == chain_id and _atom2['seq_id'] == seq_id):
                        _atomSelection.append(_atom)

        elif hasAuthSeqId1 and not hasAuthSeqId2:
            __selection1 = copy.deepcopy(_selection1)
            for _atom in __selection1:
                if 'auth_atom_id' in _atom:
                    _atom.pop('auth_atom_id')
            for idx, _atom in enumerate(__selection1):
                if isinstance(_atom, str) and _atom == '*':
                    return _selection2
                if _atom in _selection2:
                    _atomSelection.append(_selection1[idx])
                elif 'hydrogen_not_instantiated' in _atom and _atom['hydrogen_not_instantiated']:
                    chain_id = _atom['chain_id']
                    seq_id = _atom['seq_id']
                    if any(_atom2 for _atom2 in _selection2 if _atom2['chain_id'] == chain_id and _atom2['seq_id'] == seq_id):
                        _atomSelection.append(_selection1[idx])

        elif not hasAuthSeqId1 and hasAuthSeqId2:
            __selection2 = copy.deepcopy(_selection2)
            for idx, _atom in enumerate(__selection2):
                if 'auth_atom_id' in _atom:
                    _atom.pop('auth_atom_id')
            for idx, _atom in enumerate(__selection2):
                if isinstance(_atom, str) and _atom == '*':
                    return _selection1
                if _atom in _selection1:
                    _atomSelection.append(_selection2[idx])
                elif 'hydrogen_not_instantiated' in _atom and _atom['hydrogen_not_instantiated']:
                    chain_id = _atom['chain_id']
                    seq_id = _atom['seq_id']
                    if any(_atom1 for _atom1 in _selection1 if _atom1['chain_id'] == chain_id and _atom1['seq_id'] == seq_id):
                        _atomSelection.append(_selection2[idx])

        else:
            __selection1 = copy.deepcopy(_selection1)
            for _atom in __selection1:
                if 'auth_atom_id' in _atom:
                    _atom.pop('auth_atom_id')
            __selection2 = copy.deepcopy(_selection2)
            for _atom in __selection2:
                if 'auth_atom_id' in _atom:
                    _atom.pop('auth_atom_id')
            for idx, _atom in enumerate(__selection1):
                if isinstance(_atom, str) and _atom == '*':
                    return _selection2
                if _atom in __selection2:
                    _atomSelection.append(_selection1[idx])
                elif 'hydrogen_not_instantiated' in _atom and _atom['hydrogen_not_instantiated']:
                    chain_id = _atom['chain_id']
                    seq_id = _atom['seq_id']
                    if any(_atom2 for _atom2 in __selection2 if _atom2['chain_id'] == chain_id and _atom2['seq_id'] == seq_id):
                        _atomSelection.append(_selection1[idx])

        return _atomSelection

    # Enter a parse tree produced by CharmmMRParser#factor.
    def enterFactor(self, ctx: CharmmMRParser.FactorContext):
        if self.__sel_expr_debug:
            print("  " * self.depth + f"enter_factor, concatenation: {bool(ctx.factor())}")

        self.depth += 1

    # Exit a parse tree produced by CharmmMRParser#factor.
    def exitFactor(self, ctx: CharmmMRParser.FactorContext):
        self.depth -= 1
        if self.__sel_expr_debug:
            print("  " * self.depth + "exit_factor")

        try:

            # concatenation
            if ctx.factor() and self.stackSelections:
                if self.__con_union_expr and not self.__cur_union_expr and ctx.Not_op():
                    if len(self.stackFactors) > 0:
                        self.stackFactors.pop()
                        self.factor['atom_selection'] = self.stackSelections[-1]
                        self.stackSelections.append('and')  # intersection

                elif not self.__top_union_expr:
                    if len(self.stackFactors) > 0:
                        self.stackFactors.pop()
                        self.factor = {'atom_selection': self.stackSelections.pop()}

            if ctx.All() or ctx.Initial():
                clauseName = 'all' if ctx.All() else 'initial'
                if self.__sel_expr_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.__hasCoord:
                    return
                try:

                    atomSelection =\
                        self.__cR.getDictListWithFilter('atom_site',
                                                        AUTH_ATOM_DATA_ITEMS,
                                                        [{'name': self.__modelNumName, 'type': 'int',
                                                          'value': self.__representativeModelId},
                                                         {'name': 'label_alt_id', 'type': 'enum',
                                                          'enum': ('A')}
                                                         ])

                    self.intersectionFactor_expressions(atomSelection)

                    if len(self.factor['atom_selection']) == 0:
                        self.factor['atom_id'] = [None]
                        self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                        f"The {clauseName!r} clause has no effect.")

                    else:
                        if 'chain_id' in self.factor:
                            del self.factor['chain_id']
                        if 'comp_id' in self.factor:
                            del self.factor['comp_id']
                        if 'seq_id' in self.factor:
                            del self.factor['seq_id']
                        if 'type_symbol' in self.factor:
                            del self.factor['type_symbol']
                        if 'atom_id' in self.factor:
                            del self.factor['atom_id']
                        if 'comp_ids' in self.factor:
                            del self.factor['comp_ids']
                        if 'seq_ids' in self.factor:
                            del self.factor['seq_ids']
                        if 'type_symbols' in self.factor:
                            del self.factor['type_symbols']
                        if 'atom_ids' in self.factor:
                            del self.factor['atom_ids']
                        if 'alt_chain_id' in self.factor:
                            del self.factor['alt_chain_id']
                        if 'alt_atom_id' in self.factor:
                            del self.factor['alt_atom_id']

                except Exception as e:
                    if self.__verbose:
                        self.__lfh.write(f"+CharmmMRParserListener.exitFactor() ++ Error  - {str(e)}")

            elif ctx.Around():
                clauseName = 'around'
                if self.__sel_expr_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.__hasCoord:
                    return
                if len(self.numberFSelection) == 0 or None in self.numberFSelection:
                    return
                around = self.numberFSelection[0]
                _atomSelection = []

                self.consumeFactor_expressions(f"atom selection expression before the {clauseName!r} clause")

                if 'atom_selection' in self.factor:

                    for _atom in self.factor['atom_selection']:

                        try:

                            _origin =\
                                self.__cR.getDictListWithFilter('atom_site',
                                                                CARTN_DATA_ITEMS,
                                                                [{'name': self.__authAsymId, 'type': 'str', 'value': _atom['chain_id']},
                                                                 {'name': self.__authSeqId, 'type': 'int', 'value': _atom['seq_id']},
                                                                 {'name': self.__authAtomId, 'type': 'str', 'value': _atom['atom_id']},
                                                                 {'name': self.__modelNumName, 'type': 'int',
                                                                  'value': self.__representativeModelId},
                                                                 {'name': 'label_alt_id', 'type': 'enum',
                                                                  'enum': ('A')}
                                                                 ])

                            if len(_origin) != 1:
                                continue

                            origin = to_np_array(_origin[0])

                            _neighbor =\
                                self.__cR.getDictListWithFilter('atom_site',
                                                                AUTH_ATOM_CARTN_DATA_ITEMS,
                                                                [{'name': 'Cartn_x', 'type': 'range-float',
                                                                  'range': {'min_exclusive': (origin[0] - around),
                                                                            'max_exclusive': (origin[0] + around)}},
                                                                 {'name': 'Cartn_y', 'type': 'range-float',
                                                                  'range': {'min_exclusive': (origin[1] - around),
                                                                            'max_exclusive': (origin[1] + around)}},
                                                                 {'name': 'Cartn_z', 'type': 'range-float',
                                                                  'range': {'min_exclusive': (origin[2] - around),
                                                                            'max_exclusive': (origin[2] + around)}},
                                                                 {'name': self.__modelNumName, 'type': 'int',
                                                                  'value': self.__representativeModelId},
                                                                 {'name': 'label_alt_id', 'type': 'enum',
                                                                  'enum': ('A')}
                                                                 ])

                            if len(_neighbor) == 0:
                                continue

                            neighbor = [atom for atom in _neighbor if distance(to_np_array(atom), origin) < around]

                            for atom in neighbor:
                                del atom['x']
                                del atom['y']
                                del atom['z']
                                _atomSelection.append(atom)

                        except Exception as e:
                            if self.__verbose:
                                self.__lfh.write(f"+CharmmMRParserListener.exitFactor() ++ Error  - {str(e)}")

                    if len(self.factor['atom_selection']) > 0:
                        self.factor['atom_selection'] = [dict(s) for s in set(frozenset(atom.items()) for atom in _atomSelection)]

                        if len(self.factor['atom_selection']) == 0:
                            self.factor['atom_id'] = [None]
                            self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                            f"The {clauseName!r} clause has no effect.")

            elif ctx.Atom():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> atom")
                if not self.__hasPolySeq and not self.__hasNonPolySeq:
                    return

                simpleNameIndex = simpleNamesIndex = 0  # these indices are necessary to deal with mixing case of 'Simple_name' and 'Simple_names'
                if ctx.Simple_name(0):
                    chainId = str(ctx.Simple_name(0))
                    self.factor['chain_id'] = [ps['auth_chain_id'] for ps in self.__polySeq
                                               if ps['auth_chain_id'] == self.getRealChainId(chainId)]
                    if self.__hasNonPolySeq:
                        for np in self.__nonPolySeq:
                            _chainId = np['auth_chain_id']
                            if _chainId == self.getRealChainId(chainId) and _chainId not in self.factor['chain_id']:
                                self.factor['chain_id'].append(_chainId)
                    if len(self.factor['chain_id']) > 0:
                        simpleNameIndex += 1

                if simpleNameIndex == 0 and ctx.Simple_names(0):
                    chainId = str(ctx.Simple_names(0))
                    _chainId = toRegEx(chainId)
                    self.factor['chain_id'] = [ps['auth_chain_id'] for ps in self.__polySeq
                                               if re.match(_chainId, ps['auth_chain_id'])]
                    if self.__hasNonPolySeq:
                        for np in self.__nonPolySeq:
                            __chainId = np['auth_chain_id']
                            if re.match(_chainId, __chainId) and __chainId not in self.factor['chain_id']:
                                self.factor['chain_id'].append(__chainId)
                    simpleNamesIndex += 1

                if len(self.factor['chain_id']) == 0:
                    if len(self.__polySeq) == 1:
                        self.factor['chain_id'] = self.__polySeq[0]['chain_id']
                        self.factor['auth_chain_id'] = chainId
                    elif self.__reasons is not None:
                        self.factor['atom_id'] = [None]
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Couldn't specify segment name "
                                        f"'{chainId}' the coordinates.")  # do not use 'chainId!r' expression, '%' code throws ValueError
                    else:
                        if 'segment_id_mismatch' not in self.reasonsForReParsing:
                            self.reasonsForReParsing['segment_id_mismatch'] = {}
                            self.reasonsForReParsing['segment_id_match_stats'] = {}
                        if chainId not in self.reasonsForReParsing['segment_id_mismatch']:
                            self.reasonsForReParsing['segment_id_mismatch'][chainId] = None
                            self.reasonsForReParsing['segment_id_match_stats'][chainId] = {}
                        self.factor['alt_chain_id'] = chainId

                if ctx.Integer(0):
                    self.factor['seq_id'] = [int(str(ctx.Integer(0)))]

                if ctx.Integers():
                    seqId = str(ctx.Integers())
                    _seqId = toRegEx(seqId)
                    _seqIdSelect = set()
                    for chainId in self.factor['chain_id']:
                        ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                        if ps is not None:
                            found = False
                            for realSeqId in ps['auth_seq_id']:
                                realSeqId = self.getRealSeqId(ps, realSeqId)
                                if re.match(_seqId, str(realSeqId)):
                                    _seqIdSelect.add(realSeqId)
                                    found = True
                            if not found:
                                for realSeqId in ps['auth_seq_id']:
                                    realSeqId = self.getRealSeqId(ps, realSeqId)
                                    seqKey = (chainId, realSeqId)
                                    if seqKey in self.__authToLabelSeq:
                                        _, realSeqId = self.__authToLabelSeq[seqKey]
                                        if re.match(_seqId, str(realSeqId)):
                                            _seqIdSelect.add(realSeqId)
                    if self.__hasNonPolySeq:
                        for chainId in self.factor['chain_id']:
                            npList = [np for np in self.__nonPolySeq if np['auth_chain_id'] == chainId]
                            for np in npList:
                                found = False
                                for realSeqId in np['auth_seq_id']:
                                    realSeqId = self.getRealSeqId(np, realSeqId, False)
                                    if re.match(_seqId, str(realSeqId)):
                                        _seqIdSelect.add(realSeqId)
                                        found = True
                                if not found:
                                    for realSeqId in np['auth_seq_id']:
                                        realSeqId = self.getRealSeqId(np, realSeqId, False)
                                        seqKey = (chainId, realSeqId)
                                        if seqKey in self.__authToLabelSeq:
                                            _, realSeqId = self.__authToLabelSeq[seqKey]
                                            if re.match(_seqId, str(realSeqId)):
                                                _seqIdSelect.add(realSeqId)
                    self.factor['seq_id'] = list(_seqIdSelect)

                _atomIdSelect = set()
                if ctx.Simple_name(simpleNameIndex):
                    atomId = str(ctx.Simple_name(simpleNameIndex))
                    for chainId in self.factor['chain_id']:
                        ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                        if ps is None:
                            continue
                        for seqId in self.factor['seq_id']:
                            if seqId in ps['auth_seq_id']:
                                seqId = self.getRealSeqId(ps, seqId)
                                compId = ps['comp_id'][ps['auth_seq_id'].index(seqId)]
                                if self.__ccU.updateChemCompDict(compId):
                                    if any(cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == atomId):
                                        _atomIdSelect.add(atomId)
                    if self.__hasNonPolySeq:
                        for chainId in self.factor['chain_id']:
                            npList = [np for np in self.__nonPolySeq if np['auth_chain_id'] == chainId]
                            for np in npList:
                                for seqId in self.factor['seq_id']:
                                    if seqId in np['auth_seq_id']:
                                        seqId = self.getRealSeqId(np, seqId, False)
                                        compId = np['comp_id'][np['auth_seq_id'].index(seqId)]
                                        if self.__ccU.updateChemCompDict(compId):
                                            if any(cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == atomId):
                                                _atomIdSelect.add(atomId)

                elif ctx.Simple_names(simpleNamesIndex):
                    atomId = translateToStdAtomName(str(ctx.Simple_names(simpleNamesIndex)),
                                                    None if 'comp_id' not in self.factor else self.factor['comp_id'][0],
                                                    ccU=self.__ccU)
                    _atomId = toRegEx(atomId)
                    for chainId in self.factor['chain_id']:
                        ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                        if ps is None:
                            continue
                        for seqId in self.factor['seq_id']:
                            if seqId in ps['auth_seq_id']:
                                seqId = self.getRealSeqId(ps, seqId)
                                compId = ps['comp_id'][ps['auth_seq_id'].index(seqId)]
                                if self.__ccU.updateChemCompDict(compId):
                                    for cca in self.__ccU.lastAtomList:
                                        if cca[self.__ccU.ccaLeavingAtomFlag] != 'Y':
                                            realAtomId = cca[self.__ccU.ccaAtomId]
                                            if re.match(_atomId, realAtomId):
                                                _atomIdSelect.add(realAtomId)
                    if self.__hasNonPolySeq:
                        for chainId in self.factor['chain_id']:
                            npList = [np for np in self.__nonPolySeq if np['auth_chain_id'] == chainId]
                            for np in npList:
                                for seqId in self.factor['seq_id']:
                                    if seqId in np['auth_seq_id']:
                                        seqId = self.getRealSeqId(np, seqId, False)
                                        compId = np['comp_id'][np['auth_seq_id'].index(seqId)]
                                        if self.__ccU.updateChemCompDict(compId):
                                            for cca in self.__ccU.lastAtomList:
                                                if cca[self.__ccU.ccaLeavingAtomFlag] != 'Y':
                                                    realAtomId = cca[self.__ccU.ccaAtomId]
                                                    if re.match(_atomId, realAtomId):
                                                        _atomIdSelect.add(realAtomId)

                self.factor['atom_id'] = list(_atomIdSelect)

                self.consumeFactor_expressions("'atom' clause", False)

            elif ctx.Property():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> property")
                if not self.__hasCoord:
                    return
                absolute = bool(ctx.Abs())
                _attr_prop = str(ctx.Attr_properties())
                attr_prop = _attr_prop.lower()
                opCode = str(ctx.Comparison_ops()).lower()
                if len(self.numberFSelection) == 0 or None in self.numberFSelection:
                    return
                attr_value = self.numberFSelection[0]

                validProp = True

                if attr_prop.startswith('xcom')\
                        or attr_prop.startswith('ycom')\
                        or attr_prop.startswith('zcom')\
                        or attr_prop.startswith('wcom')\
                        or attr_prop.startswith('wmai'):  # XCOMP, YCOMP, ZCOMP, WCOMP, WMAI
                    self.factor['atom_id'] = [None]
                    self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                    f"The attribute property {_attr_prop!r} "
                                    "requires a comparison coordinate set.")
                    validProp = False

                elif attr_prop.startswith('char'):  # CAHRGE
                    valueType = {'name': 'pdbx_formal_charge'}
                    if opCode in ('.eq.', '.ae.'):
                        valueType['type'] = 'int' if not absolute else 'abs-int'
                        valueType['value'] = attr_value
                    elif opCode == '.lt.':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'max_exclusive': attr_value}
                    elif opCode == '.gt.':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'min_exclusive': attr_value}
                    elif opCode == '.le.':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'max_inclusive': attr_value}
                    elif opCode == '.gt.':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'min_inclusive': attr_value}
                    elif opCode == '.ne.':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'not_equal_to': attr_value}
                    atomSelection =\
                        self.__cR.getDictListWithFilter('atom_site',
                                                        AUTH_ATOM_DATA_ITEMS,
                                                        [valueType,
                                                         {'name': self.__modelNumName, 'type': 'int',
                                                          'value': self.__representativeModelId},
                                                         {'name': 'label_alt_id', 'type': 'enum',
                                                          'enum': ('A')}
                                                         ])

                    self.intersectionFactor_expressions(atomSelection)

                elif attr_prop in ('dx', 'dy', 'dz'):
                    self.factor['atom_id'] = [None]
                    self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                    f"The attribute property {_attr_prop!r} "
                                    "related to atomic force of each atom is not possessed in the static coordinate file.")
                    validProp = False

                elif attr_prop.startswith('fbet'):  # FBETA
                    self.factor['atom_id'] = [None]
                    self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                    f"The attribute property {_attr_prop!r} "
                                    "related to the Langevin dynamics (nonzero friction coefficient) is not possessed in the static coordinate file.")
                    validProp = False

                elif attr_prop == 'mass':
                    _typeSymbolSelect = set()
                    atomTypes = self.__cR.getDictList('atom_type')
                    if len(atomTypes) > 0 and 'symbol' in atomTypes[0]:
                        for atomType in atomTypes:
                            typeSymbol = atomType['symbol']
                            atomicNumber = int_atom(typeSymbol)
                            atomicWeight = ELEMENT_WEIGHTS[atomicNumber]

                            if (opCode == '.eq.' and atomicWeight == attr_value)\
                               or (opCode == '.lt.' and atomicWeight < attr_value)\
                               or (opCode == '.gt.' and atomicWeight > attr_value)\
                               or (opCode == '.le.' and atomicWeight <= attr_value)\
                               or (opCode == '.ge.' and atomicWeight >= attr_value)\
                               or (opCode == '.ne.' and atomicWeight != attr_value)\
                               or (opCode == '.ae.' and abs(atomicWeight - attr_value) < 0.001):
                                _typeSymbolSelect.add(typeSymbol)

                    atomSelection =\
                        self.__cR.getDictListWithFilter('atom_site',
                                                        AUTH_ATOM_DATA_ITEMS,
                                                        [{'name': 'type_symbol', 'type': 'enum',
                                                          'enum': _typeSymbolSelect},
                                                         {'name': self.__modelNumName, 'type': 'int',
                                                          'value': self.__representativeModelId},
                                                         {'name': 'label_alt_id', 'type': 'enum',
                                                          'enum': ('A')}
                                                         ])

                    self.intersectionFactor_expressions(atomSelection)

                elif attr_prop in ('xref', 'yref', 'zref'):
                    self.factor['atom_id'] = [None]
                    self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                    f"The attribute property {_attr_prop!r} "
                                    "requires a reference coordinate set.")
                    validProp = False

                elif attr_prop in ('vx', 'vy', 'vz'):
                    self.factor['atom_id'] = [None]
                    self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                    f"The attribute property {_attr_prop!r} "
                                    "related to current velocities of each atom is not possessed in the static coordinate file.")
                    validProp = False

                elif attr_prop in ('x', 'y', 'z'):
                    valueType = {'name': f"Cartn_{attr_prop}"}
                    if opCode == '.eq.':
                        valueType['type'] = 'float' if not absolute else 'abs-float'
                        valueType['value'] = attr_value
                    elif opCode == '.lt.':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'max_exclusive': attr_value}
                    elif opCode == '.gt.':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_exclusive': attr_value}
                    elif opCode == '.le.':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'max_inclusive': attr_value}
                    elif opCode == '.ge.':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_inclusive': attr_value}
                    elif opCode == '.ne.':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'not_equal_to': attr_value}
                    elif opCode == '.ae.':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_inclusive': attr_value - 0.001, 'max_inclusive': attr_value + 0.001}
                    atomSelection =\
                        self.__cR.getDictListWithFilter('atom_site',
                                                        AUTH_ATOM_DATA_ITEMS,
                                                        [valueType,
                                                         {'name': self.__modelNumName, 'type': 'int',
                                                          'value': self.__representativeModelId},
                                                         {'name': 'label_alt_id', 'type': 'enum',
                                                          'enum': ('A')}
                                                         ])

                    self.intersectionFactor_expressions(atomSelection)

                elif attr_prop.startswith('sca') or attr_prop in ('zero', 'one'):
                    self.factor['atom_id'] = [None]
                    self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                    f"The '{_attr_prop}' clause has no effect "
                                    "because the internal vector statement is not set.")
                    validProp = False

                elif attr_prop.startswith('econ') or attr_prop.startswith('epco') or attr_prop.startswith('cons')\
                        or attr_prop.startswith('igno') or attr_prop.startswith('aspv') or attr_prop.startswith('vdws')\
                        or attr_prop.startswith('alph') or attr_prop.startswith('effe') or attr_prop.startswith('radi')\
                        or attr_prop.startswith('rsca') or attr_prop.startswith('fdco')\
                        or attr_prop in ('move', 'type', 'fdim', 'fdep'):
                    self.factor['atom_id'] = [None]
                    self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                    f"The attribute property {_attr_prop!r} "
                                    "related to software specific parameters of each atom is not possessed in the static coordinate file.")
                    validProp = False

                if validProp and len(self.factor['atom_selection']) == 0:
                    self.factor['atom_id'] = [None]
                    _absolute = ' abs' if absolute else ''
                    self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                    f"The 'attribute' clause ('{_attr_prop}{_absolute} {opCode} {attr_value}') has no effect.")

            elif ctx.Bonded():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> bonded")
                if not self.__hasCoord:
                    return
                if 'atom_selection' in self.factor and len(self.factor['atom_selection']) > 0:
                    _atomSelection = []

                    for _atom in self.factor['atom_selection']:
                        chainId = _atom['chain_id']
                        compId = _atom['comp_id']
                        seqId = _atom['seq_id']
                        atomId = _atom['atom_id']

                        _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId)

                        # intra
                        if self.__ccU.updateChemCompDict(compId):
                            leavingAtomIds = [cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaLeavingAtomFlag] == 'Y']

                            _atomIdSelect = set()
                            for ccb in self.__ccU.lastBonds:
                                if ccb[self.__ccU.ccbAtomId1] == atomId:
                                    _atomIdSelect.add(ccb[self.__ccU.ccbAtomId2])
                                elif ccb[self.__ccU.ccbAtomId2] == atomId:
                                    _atomIdSelect.add(ccb[self.__ccU.ccbAtomId1])

                            hasLeaavindAtomId = False

                            for _atomId in _atomIdSelect:

                                if _atomId in leavingAtomIds:
                                    hasLeaavindAtomId = True
                                    continue

                                _atom = None
                                if coordAtomSite is not None:
                                    if _atomId in coordAtomSite['atom_id']:
                                        _atom = {}
                                        _atom['comp_id'] = coordAtomSite['comp_id']
                                    elif 'alt_atom_id' in coordAtomSite and _atomId in coordAtomSite['alt_atom_id']:
                                        _atom = {}
                                        _atom['comp_id'] = coordAtomSite['comp_id']

                                if _atom is not None and _atom['comp_id'] == compId:
                                    _atomSelection.append({'chain_id': chainId, 'seq_id': seqId, 'comp_id': compId, 'atom_id': _atomId})

                                else:
                                    ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                                    if ps is not None and seqId in ps['auth_seq_id'] and ps['comp_id'][ps['auth_seq_id'].index(seqId)] == compId:
                                        seqId = self.getRealSeqId(ps, seqId)
                                        if any(cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == _atomId):
                                            _atomSelection.append({'chain_id': chainId, 'seq_id': seqId, 'comp_id': compId, 'atom_id': _atomId})
                                    if self.__hasNonPolySeq:
                                        npList = [np for np in self.__nonPolySeq if np['auth_chain_id'] == chainId]
                                        for np in npList:
                                            if seqId in np['auth_seq_id'] and np['comp_id'][np['auth_seq_id'].index(seqId)] == compId:
                                                seqId = self.getRealSeqId(np, seqId, False)
                                                if any(cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == _atomId):
                                                    _atomSelection.append({'chain_id': chainId, 'seq_id': seqId, 'comp_id': compId, 'atom_id': _atomId})

                            # sequential
                            if hasLeaavindAtomId:
                                _origin =\
                                    self.__cR.getDictListWithFilter('atom_site',
                                                                    CARTN_DATA_ITEMS,
                                                                    [{'name': self.__authAsymId, 'type': 'str', 'value': chainId},
                                                                     {'name': self.__authSeqId, 'type': 'int', 'value': seqId},
                                                                     {'name': self.__authAtomId, 'type': 'str', 'value': atomId},
                                                                     {'name': self.__modelNumName, 'type': 'int',
                                                                      'value': self.__representativeModelId},
                                                                     {'name': 'label_alt_id', 'type': 'enum',
                                                                      'enum': ('A')}
                                                                     ])

                                if len(_origin) == 1:
                                    origin = to_np_array(_origin[0])

                                    ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                                    if ps is not None:
                                        for _seqId in [seqId - 1, seqId + 1]:
                                            if _seqId in ps['auth_seq_id']:
                                                _seqId = self.getRealSeqId(ps, _seqId)
                                                _compId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                                                if self.__ccU.updateChemCompDict(_compId):
                                                    leavingAtomIds = [cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaLeavingAtomFlag] == 'Y']

                                                    _atomIdSelect = set()
                                                    for ccb in self.__ccU.lastBonds:
                                                        if ccb[self.__ccU.ccbAtomId1] in leavingAtomIds:
                                                            _atomId = ccb[self.__ccU.ccbAtomId2]
                                                            if _atomId not in leavingAtomIds:
                                                                _atomIdSelect.add(_atomId)
                                                        if ccb[self.__ccU.ccbAtomId2] in leavingAtomIds:
                                                            _atomId = ccb[self.__ccU.ccbAtomId1]
                                                            if _atomId not in leavingAtomIds:
                                                                _atomIdSelect.add(_atomId)

                                                    for _atomId in _atomIdSelect:
                                                        _neighbor =\
                                                            self.__cR.getDictListWithFilter('atom_site',
                                                                                            CARTN_DATA_ITEMS,
                                                                                            [{'name': self.__authAsymId, 'type': 'str', 'value': chainId},
                                                                                             {'name': self.__authSeqId, 'type': 'int', 'value': _seqId},
                                                                                             {'name': self.__authAtomId, 'type': 'str', 'value': _atomId},
                                                                                             {'name': self.__modelNumName, 'type': 'int',
                                                                                              'value': self.__representativeModelId},
                                                                                             {'name': 'label_alt_id', 'type': 'enum',
                                                                                              'enum': ('A')}
                                                                                             ])

                                                        if len(_neighbor) != 1:
                                                            continue

                                                        if distance(to_np_array(_neighbor[0]), origin) < 2.5:
                                                            _atomSelection.append({'chain_id': chainId, 'seq_id': _seqId, 'comp_id': _compId, 'atom_id': _atomId})

                                    if self.__hasNonPolySeq:
                                        npList = [np for np in self.__nonPolySeq if np['auth_chain_id'] == chainId]
                                        for np in npList:
                                            for _seqId in [seqId - 1, seqId + 1]:
                                                if _seqId in np['auth_seq_id']:
                                                    _seqId = self.getRealSeqId(np, _seqId, False)
                                                    _compId = np['comp_id'][np['auth_seq_id'].index(_seqId)]
                                                    if self.__ccU.updateChemCompDict(_compId):
                                                        leavingAtomIds = [cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaLeavingAtomFlag] == 'Y']

                                                        _atomIdSelect = set()
                                                        for ccb in self.__ccU.lastBonds:
                                                            if ccb[self.__ccU.ccbAtomId1] in leavingAtomIds:
                                                                _atomId = ccb[self.__ccU.ccbAtomId2]
                                                                if _atomId not in leavingAtomIds:
                                                                    _atomIdSelect.add(_atomId)
                                                            if ccb[self.__ccU.ccbAtomId2] in leavingAtomIds:
                                                                _atomId = ccb[self.__ccU.ccbAtomId1]
                                                                if _atomId not in leavingAtomIds:
                                                                    _atomIdSelect.add(_atomId)

                                                        for _atomId in _atomIdSelect:
                                                            _neighbor =\
                                                                self.__cR.getDictListWithFilter('atom_site',
                                                                                                CARTN_DATA_ITEMS,
                                                                                                [{'name': self.__authAsymId, 'type': 'str', 'value': chainId},
                                                                                                 {'name': self.__authSeqId, 'type': 'int', 'value': _seqId},
                                                                                                 {'name': self.__authAtomId, 'type': 'str', 'value': _atomId},
                                                                                                 {'name': self.__modelNumName, 'type': 'int',
                                                                                                  'value': self.__representativeModelId},
                                                                                                 {'name': 'label_alt_id', 'type': 'enum',
                                                                                                  'enum': ('A')}
                                                                                                 ])

                                                            if len(_neighbor) != 1:
                                                                continue

                                                            if distance(to_np_array(_neighbor[0]), origin) < 2.5:
                                                                _atomSelection.append({'chain_id': chainId, 'seq_id': _seqId, 'comp_id': _compId, 'atom_id': _atomId})

                        # struct_conn category
                        _atom = self.__cR.getDictListWithFilter('struct_conn',
                                                                PTNR1_AUTH_ATOM_DATA_ITEMS,
                                                                [{'name': 'ptnr2_auth_asym_id', 'type': 'str', 'value': chainId},
                                                                 {'name': 'ptnr2_auth_seq_id', 'type': 'int', 'value': seqId},
                                                                 {'name': 'ptnr2_label_atom_id', 'type': 'str', 'value': atomId},
                                                                 {'name': self.__modelNumName, 'type': 'int',
                                                                  'value': self.__representativeModelId}
                                                                 ])

                        if len(_atom) == 1:
                            _atomSelection.append(_atom[0])

                        _atom = self.__cR.getDictListWithFilter('struct_conn',
                                                                PTNR2_AUTH_ATOM_DATA_ITEMS,
                                                                [{'name': 'ptnr1_auth_asym_id', 'type': 'str', 'value': chainId},
                                                                 {'name': 'ptnr1_auth_seq_id', 'type': 'int', 'value': seqId},
                                                                 {'name': 'ptnr1_label_atom_id', 'type': 'str', 'value': atomId},
                                                                 {'name': self.__modelNumName, 'type': 'int',
                                                                  'value': self.__representativeModelId}
                                                                 ])

                        if len(_atom) == 1:
                            _atomSelection.append(_atom[0])

                    self.factor['atom_selection'] = [dict(s) for s in set(frozenset(atom.items()) for atom in _atomSelection)]

                    if len(self.factor['atom_selection']) == 0:
                        self.factor['atom_id'] = [None]
                        self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                        "The 'bondedto' clause has no effect.")

                else:
                    self.factor['atom_id'] = [None]
                    self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                    "The 'bondedto' clause has no effect because no atom is selected.")

            elif ctx.ByGroup():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> bygroup")
                if not self.__hasCoord:
                    return
                if 'atom_selection' in self.factor and len(self.factor['atom_selection']) > 0:
                    _atomSelection = []

                    for _atom in self.factor['atom_selection']:
                        chainId = _atom['chain_id']
                        compId = _atom['comp_id']
                        seqId = _atom['seq_id']
                        atomId = _atom['atom_id']

                        _atomSelection.append(_atom)  # self atom

                        if self.__ccU.updateChemCompDict(compId):
                            _bondedAtomIdSelect = set()
                            for ccb in self.__ccU.lastBonds:
                                if ccb[self.__ccU.ccbAtomId1] == atomId:
                                    _bondedAtomIdSelect.add(ccb[self.__ccU.ccbAtomId2])
                                elif ccb[self.__ccU.ccbAtomId2] == atomId:
                                    _bondedAtomIdSelect.add(ccb[self.__ccU.ccbAtomId1])

                            _nonBondedAtomIdSelect = set()
                            for _atomId in _bondedAtomIdSelect:
                                for ccb in self.__ccU.lastBonds:
                                    if ccb[self.__ccU.ccbAtomId1] == _atomId:
                                        _nonBondedAtomIdSelect.add(ccb[self.__ccU.ccbAtomId2])
                                    elif ccb[self.__ccU.ccbAtomId2] == _atomId:
                                        _nonBondedAtomIdSelect.add(ccb[self.__ccU.ccbAtomId1])

                            if atomId in _nonBondedAtomIdSelect:
                                _nonBondedAtomIdSelect.remove(atomId)

                            for _atomId in _bondedAtomIdSelect:
                                if _atomId in _nonBondedAtomIdSelect:
                                    _nonBondedAtomIdSelect.remove(_atomId)

                            if len(_nonBondedAtomIdSelect) > 0:
                                _origin =\
                                    self.__cR.getDictListWithFilter('atom_site',
                                                                    CARTN_DATA_ITEMS,
                                                                    [{'name': self.__authAsymId, 'type': 'str', 'value': chainId},
                                                                     {'name': self.__authSeqId, 'type': 'int', 'value': seqId},
                                                                     {'name': self.__authAtomId, 'type': 'str', 'value': atomId},
                                                                     {'name': self.__modelNumName, 'type': 'int',
                                                                      'value': self.__representativeModelId},
                                                                     {'name': 'label_alt_id', 'type': 'enum',
                                                                      'enum': ('A')}
                                                                     ])

                                if len(_origin) == 1:
                                    origin = to_np_array(_origin[0])

                                    for _atomId in _nonBondedAtomIdSelect:
                                        _neighbor =\
                                            self.__cR.getDictListWithFilter('atom_site',
                                                                            CARTN_DATA_ITEMS,
                                                                            [{'name': self.__authAsymId, 'type': 'str', 'value': chainId},
                                                                             {'name': self.__authSeqId, 'type': 'int', 'value': seqId},
                                                                             {'name': self.__authAtomId, 'type': 'str', 'value': _atomId},
                                                                             {'name': self.__modelNumName, 'type': 'int',
                                                                              'value': self.__representativeModelId},
                                                                             {'name': 'label_alt_id', 'type': 'enum',
                                                                              'enum': ('A')}
                                                                             ])

                                        if len(_neighbor) != 1:
                                            continue

                                        if distance(to_np_array(_neighbor[0]), origin) < 2.0:
                                            _atomSelection.append({'chain_id': chainId, 'seq_id': seqId, 'comp_id': compId, 'atom_id': _atomId})

                                else:
                                    cca = next((cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == atomId), None)
                                    if cca is not None:
                                        _origin = {'x': float(cca[self.__ccU.ccaCartnX]), 'y': float(cca[self.__ccU.ccaCartnY]), 'z': float(cca[self.__ccU.ccaCartnZ])}
                                        origin = to_np_array(_origin)

                                        for _atomId in _nonBondedAtomIdSelect:
                                            _cca = next((_cca for _cca in self.__ccU.lastAtomList if _cca[self.__ccU.ccaAtomId] == _atomId), None)
                                            if _cca is not None:
                                                _neighbor = {'x': float(_cca[self.__ccU.ccaCartnX]), 'y': float(_cca[self.__ccU.ccaCartnY]), 'z': float(_cca[self.__ccU.ccaCartnZ])}

                                                if distance(to_np_array(_neighbor), origin) < 2.0:
                                                    _atomSelection.append({'chain_id': chainId, 'seq_id': seqId, 'comp_id': compId, 'atom_id': _atomId})

                    atomSelection = [dict(s) for s in set(frozenset(atom.items()) for atom in _atomSelection)]

                    if len(atomSelection) <= len(self.factor['atom_selection']):
                        self.factor['atom_id'] = [None]
                        self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                        "The 'bygroup' clause has no effect.")

                    self.factor['atom_selection'] = atomSelection

                else:
                    self.factor['atom_id'] = [None]
                    self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                    "The 'bygroup' clause has no effect because no atom is selected.")

            elif ctx.ByRes():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> byres")
                if not self.__hasCoord:
                    return
                if 'atom_selection' in self.factor and len(self.factor['atom_selection']) > 0:
                    _atomSelection = []

                    _sequenceSelect = set()

                    for _atom in self.factor['atom_selection']:
                        chainId = _atom['chain_id']
                        seqId = _atom['seq_id']

                        _sequenceSelect.add((chainId, seqId))

                    for (chainId, seqId) in _sequenceSelect:
                        _atom = next(_atom for _atom in self.factor['atom_selection'] if _atom['chain_id'] == chainId and _atom['seq_id'] == seqId)
                        compId = _atom['comp_id']

                        _atomByRes =\
                            self.__cR.getDictListWithFilter('atom_site',
                                                            ATOM_NAME_DATA_ITEMS,
                                                            [{'name': self.__authAsymId, 'type': 'str', 'value': chainId},
                                                             {'name': self.__authSeqId, 'type': 'int', 'value': seqId},
                                                             {'name': self.__modelNumName, 'type': 'int',
                                                              'value': self.__representativeModelId},
                                                             {'name': 'label_alt_id', 'type': 'enum',
                                                              'enum': ('A')}
                                                             ])

                        if len(_atomByRes) > 0 and _atomByRes[0]['comp_id'] == compId:
                            for _atom in _atomByRes:
                                _atomSelection.append({'chain_id': chainId, 'seq_id': seqId, 'comp_id': _atom['comp_id'], 'atom_id': _atom['atom_id']})

                        else:
                            ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                            if ps is not None and seqId in ps['auth_seq_id'] and ps['comp_id'][ps['auth_seq_id'].index(seqId)] == compId:
                                seqId = self.getRealSeqId(ps, seqId)
                                if self.__ccU.updateChemCompDict(compId):
                                    atomIds = [cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaLeavingAtomFlag] != 'Y']
                                    for atomId in atomIds:
                                        _atomSelection.append({'chain_id': chainId, 'seq_id': seqId, 'comp_id': compId, 'atom_id': atomId})
                            if self.__hasNonPolySeq:
                                npList = [np for np in self.__nonPolySeq if np['auth_chain_id'] == chainId]
                                for np in npList:
                                    if seqId in np['auth_seq_id'] and np['comp_id'][np['auth_seq_id'].index(seqId)] == compId:
                                        seqId = self.getRealSeqId(np, seqId, False)
                                        if self.__ccU.updateChemCompDict(compId):
                                            atomIds = [cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaLeavingAtomFlag] != 'Y']
                                            for atomId in atomIds:
                                                _atomSelection.append({'chain_id': chainId, 'seq_id': seqId, 'comp_id': compId, 'atom_id': atomId})

                    self.factor['atom_selection'] = [dict(s) for s in set(frozenset(atom.items()) for atom in _atomSelection)]

                    if len(self.factor['atom_selection']) == 0:
                        self.factor['atom_id'] = [None]
                        self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                        "The 'byres' clause has no effect.")

                else:
                    self.factor['atom_id'] = [None]
                    self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                    "The 'byres' clause has no effect because no atom is selected.")

            elif ctx.Chemical():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> chemical")
                if ctx.Colon():  # range expression
                    self.factor['type_symbols'] = [str(ctx.Simple_name(0)).upper(), str(ctx.Simple_name(1)).upper()]

                elif ctx.Simple_name(0):
                    self.factor['type_symbol'] = [str(ctx.Simple_name(0)).upper()]

                elif ctx.Simple_names(0):
                    self.factor['type_symbols'] = [str(ctx.Simple_names(0)).upper()]

                elif ctx.Symbol_name():
                    symbol_name = str(ctx.Symbol_name())
                    if symbol_name in self.evaluate:
                        val = self.evaluate[symbol_name]
                        if isinstance(val, list):
                            self.factor['type_symbol'] = [v.upper() for v in val]
                        else:
                            self.factor['type_symbol'] = [val.upper()]
                    else:
                        self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                        f"The symbol {symbol_name!r} is not defined.")

                self.consumeFactor_expressions("'chemical' clause", False)

            elif ctx.Hydrogen():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> hydrogen")
                if not self.__hasCoord:
                    return
                _typeSymbolSelect = set()
                atomTypes = self.__cR.getDictList('atom_type')
                if len(atomTypes) > 0 and 'symbol' in atomTypes[0]:
                    for atomType in atomTypes:
                        typeSymbol = atomType['symbol']
                        atomicNumber = int_atom(typeSymbol)
                        atomicWeight = ELEMENT_WEIGHTS[atomicNumber]
                        if atomicWeight < 3.5:
                            _typeSymbolSelect.add(typeSymbol)

                self.factor['type_symbol'] = list(_typeSymbolSelect)

                self.consumeFactor_expressions("'hydrogen' clause", False)

            elif ctx.NONE():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> none")
                self.factor['atom_selection'] = []

            elif ctx.Not_op():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> not")
                if not self.__hasCoord:
                    return

                if 'atom_selection' in self.factor and ('atom_id' in self.factor or 'atom_ids' in self.factor):
                    _refAtomSelection = self.factor['atom_selection']
                    del self.factor['atom_selection']
                    if self.stackFactors:
                        self.stackFactors.pop()
                    self.factor = self.__consumeFactor_expressions(self.factor, cifCheck=True)
                    if 'atom_selection' in self.factor:
                        self.factor['atom_selection'] = [atom for atom in _refAtomSelection
                                                         if not any(_atom for _atom in self.factor['atom_selection']
                                                                    if _atom['chain_id'] == atom['chain_id']
                                                                    and _atom['seq_id'] == atom['seq_id']
                                                                    and _atom['atom_id'] == atom['atom_id'])]
                    else:
                        self.factor['atom_selection'] = _refAtomSelection
                    if len(self.factor['atom_selection']) == 0:
                        self.factor['atom_id'] = [None]
                        self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                        "The 'not' clause has no effect.")

                elif 'atom_selection' not in self.factor:
                    self.factor['atom_id'] = [None]
                    self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                    "The 'not' clause has no effect.")

                else:

                    try:

                        _atomSelection =\
                            self.__cR.getDictListWithFilter('atom_site',
                                                            AUTH_ATOM_DATA_ITEMS,
                                                            [{'name': self.__modelNumName, 'type': 'int',
                                                              'value': self.__representativeModelId},
                                                             {'name': 'label_alt_id', 'type': 'enum',
                                                              'enum': ('A')}
                                                             ])

                    except Exception as e:
                        if self.__verbose:
                            self.__lfh.write(f"+CharmmMRParserListener.exitFactor() ++ Error  - {str(e)}")

                    _refAtomSelection = [atom for atom in self.factor['atom_selection'] if atom in _atomSelection]
                    self.factor['atom_selection'] = [atom for atom in _atomSelection if atom not in _refAtomSelection]

                    if len(self.factor['atom_selection']) == 0:
                        self.factor['atom_id'] = [None]
                        self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                        "The 'not' clause has no effect.")

            elif ctx.Point():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> point")
                if not self.__hasCoord:
                    return
                vector3D = [self.numberFSelection[0], self.numberFSelection[1], self.numberFSelection[2]]
                cut = self.numberFSelection[3]

                atomSelection = []

                try:

                    _neighbor =\
                        self.__cR.getDictListWithFilter('atom_site',
                                                        AUTH_ATOM_CARTN_DATA_ITEMS,
                                                        [{'name': 'Cartn_x', 'type': 'range-float',
                                                          'range': {'min_exclusive': (vector3D[0] - cut),
                                                                    'max_exclusive': (vector3D[0] + cut)}},
                                                         {'name': 'Cartn_y', 'type': 'range-float',
                                                          'range': {'min_exclusive': (vector3D[1] - cut),
                                                                    'max_exclusive': (vector3D[1] + cut)}},
                                                         {'name': 'Cartn_z', 'type': 'range-float',
                                                          'range': {'min_exclusive': (vector3D[2] - cut),
                                                                    'max_exclusive': (vector3D[2] + cut)}},
                                                         {'name': self.__modelNumName, 'type': 'int',
                                                          'value': self.__representativeModelId},
                                                         {'name': 'label_alt_id', 'type': 'enum',
                                                          'enum': ('A')}
                                                         ])

                    if len(_neighbor) > 0:
                        neighbor = [atom for atom in _neighbor if distance(to_np_array(atom), vector3D) < cut]

                        for atom in neighbor:
                            del atom['x']
                            del atom['y']
                            del atom['z']
                            atomSelection.append(atom)

                except Exception as e:
                    if self.__verbose:
                        self.__lfh.write(f"+CharmmMRParserListener.exitFactor() ++ Error  - {str(e)}")

                self.factor['atom_selection'] = atomSelection

                if len(self.factor['atom_selection']) == 0:
                    self.factor['atom_id'] = [None]
                    self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                    "The 'cut' clause has no effect.")

            elif ctx.Lone():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> lone")
                self.factor['atom_id'] = [None]
                self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                "The 'lone' clause has no effect "
                                "because the internal atom selection is fragile in the restraint file.")

            elif ctx.Previous():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> previous")
                self.factor['atom_id'] = [None]
                self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                "The 'previous' clause has no effect "
                                "because the internal atom selection is fragile in the restraint file.")

            elif ctx.User():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> user")
                self.factor['atom_id'] = [None]
                self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                "The 'user' clause has no effect "
                                "because the internal atom selection is fragile in the restraint file.")

            elif ctx.Recall():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> recall")
                self.factor['atom_id'] = [None]
                self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                "The 'recall' clause has no effect "
                                "because the internal atom selection is fragile in the restraint file.")

            elif ctx.IGroup():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> igroup")
                self.factor['atom_id'] = [None]
                self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                "The 'igroup' clause has no effect "
                                "because the internal atom selection is fragile in the restraint file.")

            elif ctx.Subset():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> subset")
                self.factor['atom_id'] = [None]
                self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                "The 'subset' clause has no effect "
                                "because the internal atom selection is fragile in the restraint file.")

            elif ctx.ByNumber():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> bynumber")

                if ctx.Colon():  # range expression
                    self.factor['atom_num'] = list(range(int(str(ctx.Integer(0))), int(str(ctx.Integer(0))) + 1))

                elif ctx.Integer(0):
                    self.factor['atom_num'] = [int(str(ctx.Integer(0)))]

                elif ctx.Integers():
                    self.factor['atom_nums'] = [str(ctx.Integers())]

                elif ctx.Symbol_name():
                    symbol_name = str(ctx.Symbol_name())
                    if symbol_name in self.evaluate:
                        val = self.evaluate[symbol_name]
                        if isinstance(val, list):
                            self.factor['atom_num'] = [v if isinstance(v, int) else int(v) for v in val]
                        else:
                            self.factor['atom_num'] = [val if isinstance(val, int) else int(val)]
                    else:
                        self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                        f"The symbol {symbol_name!r} is not defined.")

            elif ctx.IRes():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> ires")

                if ctx.Colon():  # range expression
                    self.factor['seq_id'] = list(range(int(str(ctx.Integer(0))), int(str(ctx.Integer(0))) + 1))

                elif ctx.Integer(0):
                    self.factor['seq_id'] = [int(str(ctx.Integer(0)))]

                elif ctx.Integers():
                    self.factor['seq_ids'] = [str(ctx.Integers())]

                elif ctx.Symbol_name():
                    symbol_name = str(ctx.Symbol_name())
                    if symbol_name in self.evaluate:
                        val = self.evaluate[symbol_name]
                        if isinstance(val, list):
                            self.factor['seq_id'] = [v if isinstance(v, int) else int(v) for v in val]
                        else:
                            self.factor['seq_id'] = [val if isinstance(val, int) else int(val)]
                    else:
                        self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                        f"The symbol {symbol_name!r} is not defined.")

            elif ctx.Residue():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> residue")

                eval_factor = False
                if 'seq_id' in self.factor or 'seq_ids' in self.factor:
                    __factor = copy.copy(self.factor)
                    self.consumeFactor_expressions("'residue' clause", False)
                    eval_factor = True

                if ctx.Colon():  # range expression
                    self.factor['seq_id'] = list(range(int(str(ctx.Integer(0))), int(str(ctx.Integer(0))) + 1))

                elif ctx.Integer(0):
                    self.factor['seq_id'] = [int(str(ctx.Integer(0)))]

                elif ctx.Integers():
                    self.factor['seq_ids'] = [str(ctx.Integers())]

                elif ctx.Symbol_name():
                    symbol_name = str(ctx.Symbol_name())
                    if symbol_name in self.evaluate:
                        val = self.evaluate[symbol_name]
                        if isinstance(val, list):
                            self.factor['seq_id'] = [v if isinstance(v, int) else int(v) for v in val]
                        else:
                            self.factor['seq_id'] = [val if isinstance(val, int) else int(val)]
                    else:
                        self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                        f"The symbol {symbol_name!r} is not defined.")

                if eval_factor and 'atom_selection' in self.factor:
                    if len(self.factor['atom_selection']) == 0:
                        _factor = copy.copy(self.factor)
                        if 'atom_selection' in __factor:
                            del __factor['atom_selection']
                        del _factor['atom_selection']
                        self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                        f"The 'residue' clause has no effect for a conjunction of factor {__factor} and {_factor}.")

            elif ctx.Resname():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> resname")

                eval_factor = False
                if 'comp_id' in self.factor or 'comp_ids' in self.factor:
                    __factor = copy.copy(self.factor)
                    self.consumeFactor_expressions("'resname' clause", False)
                    eval_factor = True

                if ctx.Colon():  # range expression
                    self.factor['comp_ids'] = [str(ctx.Simple_name(0)).upper(), str(ctx.Simple_name(1)).upper()]

                elif ctx.Simple_name(0):
                    self.factor['comp_id'] = [str(ctx.Simple_name(0)).upper()]

                elif ctx.Simple_names(0):
                    self.factor['comp_ids'] = [str(ctx.Simple_names(0)).upper()]

                elif ctx.Symbol_name():
                    symbol_name = str(ctx.Symbol_name())
                    if symbol_name in self.evaluate:
                        val = self.evaluate[symbol_name]
                        if isinstance(val, list):
                            self.factor['comp_id'] = [v.upper() for v in val]
                        else:
                            self.factor['comp_id'] = [val.upper()]
                    else:
                        self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                        f"The symbol {symbol_name!r} is not defined.")

                if eval_factor and 'atom_selection' in self.factor:
                    if len(self.factor['atom_selection']) == 0:
                        _factor = copy.copy(self.factor)
                        if 'atom_selection' in __factor:
                            del __factor['atom_selection']
                        del _factor['atom_selection']
                        self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                        f"The 'resname' clause has no effect for a conjunction of factor {__factor} and {_factor}.")

            elif ctx.ISeg():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> iseg")

                if ctx.Colon():  # range expression
                    self.factor['chain_id'] = [str(id) for id in range(int(str(ctx.Integer(0))), int(str(ctx.Integer(0))) + 1)]

                elif ctx.Integer(0):
                    self.factor['chain_id'] = [str(ctx.Integer(0))]

                elif ctx.Integers():
                    self.factor['chain_ids'] = [str(ctx.Integers())]

                elif ctx.Symbol_name():
                    symbol_name = str(ctx.Symbol_name())
                    if symbol_name in self.evaluate:
                        val = self.evaluate[symbol_name]
                        if isinstance(val, list):
                            self.factor['chain_id'] = [str(v) if isinstance(v, int) else int(v) for v in val]
                        else:
                            self.factor['chain_id'] = [str(val) if isinstance(val, int) else int(val)]
                    else:
                        self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                        f"The symbol {symbol_name!r} is not defined.")

            elif ctx.SegIdentifier():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> segidentifier")
                if not self.__hasPolySeq and not self.__hasNonPolySeq:
                    return

                eval_factor = False
                if 'chain_id' in self.factor:
                    __factor = copy.copy(self.factor)
                    self.consumeFactor_expressions("'segidentifier' clause", False)
                    eval_factor = True

                if ctx.Colon():  # range expression
                    if ctx.Simple_name(0):
                        begChainId = str(ctx.Simple_name(0))
                    elif ctx.Double_quote_string(0):
                        begChainId = str(ctx.Double_quote_string(0)).strip('"').strip()
                        if len(begChainId) == 0:
                            return
                    if ctx.Simple_name(1):
                        endChainId = str(ctx.Simple_name(1))
                    elif ctx.Double_quote_string(1):
                        endChainId = str(ctx.Double_quote_string(1)).strip('"').strip()
                        if len(endChainId) == 0:
                            return
                    self.factor['chain_id'] = [ps['auth_chain_id'] for ps in self.__polySeq
                                               if begChainId <= ps['auth_chain_id'] <= endChainId]
                    if self.__hasNonPolySeq:
                        for np in self.__nonPolySeq:
                            _chainId = np['auth_chain_id']
                            if begChainId <= _chainId <= endChainId and _chainId not in self.factor['chain_id']:
                                self.factor['chain_id'].append(_chainId)

                    if len(self.factor['chain_id']) == 0:
                        if len(self.__polySeq) == 1:
                            self.factor['chain_id'] = self.__polySeq[0]['chain_id']
                            self.factor['auth_chain_id'] = [begChainId, endChainId]
                        else:
                            self.factor['atom_id'] = [None]
                            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                            f"Couldn't specify segment name {begChainId:!r}:{endChainId:!r} in the coordinates.")

                else:
                    if ctx.Simple_name(0) or ctx.Double_quote_string(0):
                        if ctx.Simple_name(0):
                            chainId = str(ctx.Simple_name(0))
                        elif ctx.Double_quote_string(0):
                            chainId = str(ctx.Double_quote_string(0)).strip('"').strip()
                            if len(chainId) == 0:
                                return
                        self.factor['chain_id'] = [ps['auth_chain_id'] for ps in self.__polySeq
                                                   if ps['auth_chain_id'] == self.getRealChainId(chainId)]
                        if self.__hasNonPolySeq:
                            for np in self.__nonPolySeq:
                                _chainId = np['auth_chain_id']
                                if _chainId == self.getRealChainId(chainId) and _chainId not in self.factor['chain_id']:
                                    self.factor['chain_id'].append(_chainId)
                    if ctx.Simple_names(0):
                        chainId = str(ctx.Simple_names(0))
                        _chainId = toRegEx(chainId)
                        self.factor['chain_id'] = [ps['auth_chain_id'] for ps in self.__polySeq
                                                   if re.match(_chainId, ps['auth_chain_id'])]
                        if self.__hasNonPolySeq:
                            for np in self.__nonPolySeq:
                                __chainId = np['auth_chain_id']
                                if re.match(_chainId, __chainId) and __chainId not in self.factor['chain_id']:
                                    self.factor['chain_id'].append(__chainId)
                    if ctx.Symbol_name():
                        symbol_name = chainId = str(ctx.Symbol_name())
                        if symbol_name in self.evaluate:
                            val = self.evaluate[symbol_name]
                            if isinstance(val, list):
                                self.factor['chain_id'] = val
                            else:
                                self.factor['chain_id'] = [val]
                        else:
                            self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                            f"The symbol {symbol_name!r} is not defined.")
                    if len(self.factor['chain_id']) == 0:
                        if len(self.__polySeq) == 1:
                            self.factor['chain_id'] = self.__polySeq[0]['chain_id']
                            self.factor['auth_chain_id'] = chainId
                        elif self.__reasons is not None:
                            self.factor['atom_id'] = [None]
                            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                            "Couldn't specify segment name "
                                            f"'{chainId}' in the coordinates.")  # do not use 'chainId!r' expression, '%' code throws ValueError
                        else:
                            if 'segment_id_mismatch' not in self.reasonsForReParsing:
                                self.reasonsForReParsing['segment_id_mismatch'] = {}
                                self.reasonsForReParsing['segment_id_match_stats'] = {}
                            if chainId not in self.reasonsForReParsing['segment_id_mismatch']:
                                self.reasonsForReParsing['segment_id_mismatch'][chainId] = None
                                self.reasonsForReParsing['segment_id_match_stats'][chainId] = {}
                            self.factor['alt_chain_id'] = chainId

                if eval_factor and 'atom_selection' in self.factor:
                    if len(self.factor['atom_selection']) == 0:
                        _factor = copy.copy(self.factor)
                        if 'atom_selection' in __factor:
                            del __factor['atom_selection']
                        del _factor['atom_selection']
                        self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                        f"The 'segidentifier' clause has no effect for a conjunction of factor {__factor} and {_factor}.")

            if self.depth > 0 and self.__cur_union_expr:
                self.unionFactor = self.factor
            else:
                self.stackFactors.append(self.factor)

        finally:
            self.numberFSelection.clear()

    def selectRealisticBondConstraint(self, atom1, atom2, alt_atom_id1, alt_atom_id2, dst_func):
        """ Return realistic bond constraint taking into account the current coordinates.
        """
        if not self.__hasCoord:
            return atom1, atom2

        try:

            _p1 =\
                self.__cR.getDictListWithFilter('atom_site',
                                                CARTN_DATA_ITEMS,
                                                [{'name': self.__authAsymId, 'type': 'str', 'value': atom1['chain_id']},
                                                 {'name': self.__authSeqId, 'type': 'int', 'value': atom1['seq_id']},
                                                 {'name': self.__authAtomId, 'type': 'str', 'value': atom1['atom_id']},
                                                 {'name': self.__modelNumName, 'type': 'int',
                                                  'value': self.__representativeModelId},
                                                 {'name': 'label_alt_id', 'type': 'enum',
                                                  'enum': ('A')}
                                                 ])

            if len(_p1) != 1:
                return atom1, atom2

            p1 = to_np_array(_p1[0])

            _p2 =\
                self.__cR.getDictListWithFilter('atom_site',
                                                CARTN_DATA_ITEMS,
                                                [{'name': self.__authAsymId, 'type': 'str', 'value': atom2['chain_id']},
                                                 {'name': self.__authSeqId, 'type': 'int', 'value': atom2['seq_id']},
                                                 {'name': self.__authAtomId, 'type': 'str', 'value': atom2['atom_id']},
                                                 {'name': self.__modelNumName, 'type': 'int',
                                                  'value': self.__representativeModelId},
                                                 {'name': 'label_alt_id', 'type': 'enum',
                                                  'enum': ('A')}
                                                 ])

            if len(_p2) != 1:
                return atom1, atom2

            p2 = to_np_array(_p2[0])

            d_org = distance(p1, p2)

            lower_limit = dst_func.get('lower_limit')
            if lower_limit is not None:
                lower_limit = float(lower_limit)
            upper_limit = dst_func.get('upper_limit')
            if upper_limit is not None:
                upper_limit = float(upper_limit)

            if alt_atom_id1 is not None:

                _p1 =\
                    self.__cR.getDictListWithFilter('atom_site',
                                                    CARTN_DATA_ITEMS,
                                                    [{'name': self.__authAsymId, 'type': 'str', 'value': atom1['chain_id']},
                                                     {'name': self.__authSeqId, 'type': 'int', 'value': atom1['seq_id']},
                                                     {'name': self.__authAtomId, 'type': 'str', 'value': alt_atom_id1},
                                                     {'name': self.__modelNumName, 'type': 'int',
                                                      'value': self.__representativeModelId},
                                                     {'name': 'label_alt_id', 'type': 'enum',
                                                      'enum': ('A')}
                                                     ])

                if len(_p1) != 1:
                    return atom1, atom2

                p1_alt = to_np_array(_p1[0])

                d_alt = distance(p1_alt, p2)

                if dist_error(lower_limit, upper_limit, d_org) > dist_error(lower_limit, upper_limit, d_alt):
                    if 'auth_atom_id' not in atom1:
                        atom1['auth_atom_id'] = atom1['atom_id']
                    atom1['atom_id'] = alt_atom_id1

            elif alt_atom_id2 is not None:

                _p2 =\
                    self.__cR.getDictListWithFilter('atom_site',
                                                    CARTN_DATA_ITEMS,
                                                    [{'name': self.__authAsymId, 'type': 'str', 'value': atom2['chain_id']},
                                                     {'name': self.__authSeqId, 'type': 'int', 'value': atom2['seq_id']},
                                                     {'name': self.__authAtomId, 'type': 'str', 'value': alt_atom_id2},
                                                     {'name': self.__modelNumName, 'type': 'int',
                                                      'value': self.__representativeModelId},
                                                     {'name': 'label_alt_id', 'type': 'enum',
                                                      'enum': ('A')}
                                                     ])

                if len(_p2) != 1:
                    return atom1, atom2

                p2_alt = to_np_array(_p2[0])

                d_alt = distance(p1, p2_alt)

                if dist_error(lower_limit, upper_limit, d_org) > dist_error(lower_limit, upper_limit, d_alt):
                    if 'auth_atom_id' not in atom2:
                        atom2['auth_atom_id'] = atom2['atom_id']
                    atom2['atom_id'] = alt_atom_id2

        except Exception as e:
            if self.__verbose:
                self.__lfh.write(f"+CharmmMRParserListener.selectRealisticBondConstraint() ++ Error  - {str(e)}")

        return atom1, atom2

    def selectRealisticChi2AngleConstraint(self, atom1, atom2, atom3, atom4, dst_func):
        """ Return realistic chi2 angle constraint taking into account the current coordinates.
        """
        if not self.__hasCoord:
            return dst_func

        try:

            _p1 =\
                self.__cR.getDictListWithFilter('atom_site',
                                                CARTN_DATA_ITEMS,
                                                [{'name': self.__authAsymId, 'type': 'str', 'value': atom1['chain_id']},
                                                 {'name': self.__authSeqId, 'type': 'int', 'value': atom1['seq_id']},
                                                 {'name': self.__authAtomId, 'type': 'str', 'value': atom1['atom_id']},
                                                 {'name': self.__modelNumName, 'type': 'int',
                                                  'value': self.__representativeModelId},
                                                 {'name': 'label_alt_id', 'type': 'enum',
                                                  'enum': ('A')}
                                                 ])

            if len(_p1) != 1:
                return dst_func

            p1 = to_np_array(_p1[0])

            _p2 =\
                self.__cR.getDictListWithFilter('atom_site',
                                                CARTN_DATA_ITEMS,
                                                [{'name': self.__authAsymId, 'type': 'str', 'value': atom2['chain_id']},
                                                 {'name': self.__authSeqId, 'type': 'int', 'value': atom2['seq_id']},
                                                 {'name': self.__authAtomId, 'type': 'str', 'value': atom2['atom_id']},
                                                 {'name': self.__modelNumName, 'type': 'int',
                                                  'value': self.__representativeModelId},
                                                 {'name': 'label_alt_id', 'type': 'enum',
                                                  'enum': ('A')}
                                                 ])

            if len(_p2) != 1:
                return dst_func

            p2 = to_np_array(_p2[0])

            _p3 =\
                self.__cR.getDictListWithFilter('atom_site',
                                                CARTN_DATA_ITEMS,
                                                [{'name': self.__authAsymId, 'type': 'str', 'value': atom3['chain_id']},
                                                 {'name': self.__authSeqId, 'type': 'int', 'value': atom3['seq_id']},
                                                 {'name': self.__authAtomId, 'type': 'str', 'value': atom3['atom_id']},
                                                 {'name': self.__modelNumName, 'type': 'int',
                                                  'value': self.__representativeModelId},
                                                 {'name': 'label_alt_id', 'type': 'enum',
                                                  'enum': ('A')}
                                                 ])

            if len(_p3) != 1:
                return dst_func

            p3 = to_np_array(_p3[0])

            _p4 =\
                self.__cR.getDictListWithFilter('atom_site',
                                                CARTN_DATA_ITEMS,
                                                [{'name': self.__authAsymId, 'type': 'str', 'value': atom4['chain_id']},
                                                 {'name': self.__authSeqId, 'type': 'int', 'value': atom4['seq_id']},
                                                 {'name': self.__authAtomId, 'type': 'str', 'value': 'CD1'},
                                                 {'name': self.__modelNumName, 'type': 'int',
                                                  'value': self.__representativeModelId},
                                                 {'name': 'label_alt_id', 'type': 'enum',
                                                  'enum': ('A')}
                                                 ])

            if len(_p4) != 1:
                return dst_func

            p4 = to_np_array(_p4[0])

            chi2 = dihedral_angle(p1, p2, p3, p4)

            _p4 =\
                self.__cR.getDictListWithFilter('atom_site',
                                                CARTN_DATA_ITEMS,
                                                [{'name': self.__authAsymId, 'type': 'str', 'value': atom4['chain_id']},
                                                 {'name': self.__authSeqId, 'type': 'int', 'value': atom4['seq_id']},
                                                 {'name': self.__authAtomId, 'type': 'str', 'value': 'CD2'},
                                                 {'name': self.__modelNumName, 'type': 'int',
                                                  'value': self.__representativeModelId},
                                                 {'name': 'label_alt_id', 'type': 'enum',
                                                  'enum': ('A')}
                                                 ])

            if len(_p4) != 1:
                return dst_func

            alt_p4 = to_np_array(_p4[0])

            alt_chi2 = dihedral_angle(p1, p2, p3, alt_p4)

            target_value = dst_func.get('target_value')
            if target_value is not None:
                target_value = float(target_value)
            target_value_uncertainty = dst_func.get('target_value_uncertainty')
            if target_value_uncertainty is not None:
                target_value_uncertainty = float(target_value_uncertainty)

            lower_limit = dst_func.get('lower_limit')
            if lower_limit is not None:
                lower_limit = float(lower_limit)
            upper_limit = dst_func.get('upper_limit')
            if upper_limit is not None:
                upper_limit = float(upper_limit)

            lower_linear_limit = dst_func.get('lower_linear_limit')
            if lower_linear_limit is not None:
                lower_linear_limit = float(lower_linear_limit)
            upper_linear_limit = dst_func.get('upper_linear_limit')
            if upper_linear_limit is not None:
                upper_linear_limit = float(upper_linear_limit)

            target_value, lower_bound, upper_bound =\
                angle_target_values(target_value, target_value_uncertainty,
                                    lower_limit, upper_limit,
                                    lower_linear_limit, upper_linear_limit)

            if target_value is None:
                return dst_func

            if angle_error(lower_bound, upper_bound, target_value, chi2) > angle_error(lower_bound, upper_bound, target_value, alt_chi2):
                target_value = dst_func.get('target_value')
                if target_value is not None:
                    target_value = float(target_value) + 180.0
                lower_limit = dst_func.get('lower_limit')
                if lower_limit is not None:
                    lower_limit = float(lower_limit) + 180.0
                upper_limit = dst_func.get('upper_limit')
                if upper_limit is not None:
                    upper_limit = float(upper_limit) + 180.0

                if lower_linear_limit is not None:
                    lower_linear_limit += 180.0
                if upper_linear_limit is not None:
                    upper_linear_limit += 180.0

                _array = numpy.array([target_value, lower_limit, upper_limit, lower_linear_limit, upper_linear_limit],
                                     dtype=float)

                shift = 0.0
                if self.__correctCircularShift:
                    if numpy.nanmin(_array) >= THRESHHOLD_FOR_CIRCULAR_SHIFT:
                        shift = -(numpy.nanmax(_array) // 360) * 360
                    elif numpy.nanmax(_array) <= -THRESHHOLD_FOR_CIRCULAR_SHIFT:
                        shift = -(numpy.nanmin(_array) // 360) * 360
                if target_value is not None:
                    dst_func['target_value'] = str(target_value + shift)
                if lower_limit is not None:
                    dst_func['lower_limit'] = str(lower_limit + shift)
                if upper_limit is not None:
                    dst_func['upper_limit'] = str(upper_limit + shift)
                if lower_linear_limit is not None:
                    dst_func['lower_linear_limit'] = str(lower_linear_limit + shift)
                if upper_linear_limit is not None:
                    dst_func['upper_linear_limit'] = str(upper_linear_limit + shift)

        except Exception as e:
            if self.__verbose:
                self.__lfh.write(f"+CharmmMRParserListener.selectRealisticChi2AngleConstraint() ++ Error  - {str(e)}")

        return dst_func

    # Enter a parse tree produced by CharmmMRParser#number.
    def enterNumber(self, ctx: CharmmMRParser.NumberContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#number.
    def exitNumber(self, ctx: CharmmMRParser.NumberContext):
        if ctx.Real():
            self.numberSelection.append(float(str(ctx.Real())))

        elif ctx.Integer():
            self.numberSelection.append(float(str(ctx.Integer())))

        elif ctx.Symbol_name():
            symbol_name = str(ctx.Symbol_name())
            if symbol_name in self.evaluate:
                self.numberSelection.append(float(self.evaluate[symbol_name]))
            else:
                self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                f"The symbol {symbol_name!r} is not defined.")
                self.numberSelection.append(None)

        else:
            self.numberSelection.append(None)

    # Enter a parse tree produced by CharmmMRParser#number_f.
    def enterNumber_f(self, ctx: CharmmMRParser.Number_fContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#number_f.
    def exitNumber_f(self, ctx: CharmmMRParser.Number_fContext):
        if ctx.Real():
            self.numberFSelection.append(float(str(ctx.Real())))

        elif ctx.Integer():
            self.numberFSelection.append(float(str(ctx.Integer())))

        else:
            self.numberFSelection.append(None)

    # Enter a parse tree produced by CharmmMRParser#number_s.
    def enterNumber_s(self, ctx: CharmmMRParser.Number_sContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#number_s.
    def exitNumber_s(self, ctx: CharmmMRParser.Number_sContext):  # pylint: disable=unused-argument
        pass

    def getNumber_s(self, ctx: CharmmMRParser.Number_sContext):  # pylint: disable=no-self-use
        if ctx is None:
            return None

        if ctx.Real():
            return float(str(ctx.Real()))

        if ctx.Integer():
            return float(str(ctx.Integer()))

        if ctx.Symbol_name():
            return str(ctx.Symbol_name())

        return None

    # Enter a parse tree produced by CharmmMRParser#set_statement.
    def enterSet_statement(self, ctx: CharmmMRParser.Set_statementContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#set_statement.
    def exitSet_statement(self, ctx: CharmmMRParser.Set_statementContext):
        if ctx.Simple_name_VE(0):

            if ctx.Real_VE():
                self.evaluate[str(ctx.Simple_name_VE(0))] = float(str(ctx.Real_VE()))

            elif ctx.Integer_VE():
                self.evaluate[str(ctx.Simple_name_VE(0))] = int(str(ctx.Integer_VE()))

            elif ctx.Simple_name_VE(1):
                self.evaluate[str(ctx.Simple_name_VE(0))] = str(ctx.Simple_name_VE(1))

    def __getCurrentRestraint(self):
        if self.__cur_subtype == 'dist':
            return f"[Check the {self.distRestraints}th row of distance restraints] "
        if self.__cur_subtype == 'dihed':
            return f"[Check the {self.dihedRestraints}th row of dihedral angle restraints] "
        if self.__cur_subtype == 'geo':
            return f"[Check the {self.geoRestraints}th row of harmonic coordinate/NCS restraints] "
        return ''

    def __setLocalSeqScheme(self):
        if 'local_seq_scheme' not in self.reasonsForReParsing:
            self.reasonsForReParsing['local_seq_scheme'] = {}
        if self.__cur_subtype == 'dist':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.distRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'dihed':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.dihedRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'geo':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.geoRestraints)] = self.__preferAuthSeq
        if not self.__preferAuthSeq:
            self.__preferLabelSeqCount += 1
            if self.__preferLabelSeqCount > MAX_PREF_LABEL_SCHEME_COUNT:
                self.reasonsForReParsing['label_seq_scheme'] = True

    def __retrieveLocalSeqScheme(self):
        if self.__reasons is None or 'local_seq_scheme' not in self.__reasons:
            return
        if 'label_seq_scheme' in self.__reasons and self.__reasons['label_seq_scheme']:
            self.__preferAuthSeq = False
            self.__authSeqId = 'label_seq_id'
            return
        if self.__cur_subtype == 'dist':
            key = (self.__cur_subtype, self.distRestraints)
        elif self.__cur_subtype == 'dihed':
            key = (self.__cur_subtype, self.dihedRestraints)
        elif self.__cur_subtype == 'geo':
            key = (self.__cur_subtype, self.geoRestraints)
        else:
            return

        if key in self.__reasons['local_seq_scheme']:
            self.__preferAuthSeq = self.__reasons['local_seq_scheme'][key]

    def __addSf(self, constraintType=None, potentialType=None):
        content_subtype = contentSubtypeOf(self.__cur_subtype)

        if content_subtype is None:
            return

        self.__listIdCounter = incListIdCounter(self.__cur_subtype, self.__listIdCounter)

        key = (self.__cur_subtype, constraintType, potentialType, None, None)

        if key not in self.sfDict:
            self.sfDict[key] = []

        list_id = self.__listIdCounter[content_subtype]

        restraint_name = getRestraintName(self.__cur_subtype)

        sf_framecode = 'CHARMM_' + restraint_name.replace(' ', '_') + f'_{list_id}'

        sf = getSaveframe(self.__cur_subtype, sf_framecode, list_id, self.__entryId, self.__originalFileName,
                          constraintType=constraintType, potentialType=potentialType)

        lp = getLoop(self.__cur_subtype, hasInsCode=self.__authToInsCode is not None)
        if not isinstance(lp, dict):
            sf.add_loop(lp)

        _restraint_name = restraint_name.split()

        item = {'file_type': self.__file_type, 'saveframe': sf, 'loop': lp, 'list_id': list_id,
                'id': 0, 'index_id': 0,
                'constraint_type': ' '.join(_restraint_name[:-1])}

        if self.__cur_subtype == 'dist':
            item['constraint_subsubtype'] = 'simple'
            if constraintType is None:
                item['NOE_dist_averaging_method'] = self.noeAverage
            elif 'ROE' in constraintType:
                item['ROE_dist_averaging_method'] = self.noeAverage

        self.__lastSfDict[self.__cur_subtype] = item

        self.sfDict[key].append(item)

    def __getSf(self, constraintType=None, potentialType=None):
        key = (self.__cur_subtype, constraintType, potentialType, None, None)

        if key not in self.sfDict:
            replaced = False
            if potentialType is not None:
                old_key = (self.__cur_subtype, constraintType, None, None, None)
                if old_key in self.sfDict:
                    replaced = True
                    self.sfDict[key] = [self.sfDict[old_key].pop(-1)]
                    if len(self.sfDict[old_key]) == 0:
                        del self.sfDict[old_key]
                    sf = self.sfDict[key][-1]['saveframe']
                    idx = next((idx for idx, t in enumerate(sf.tags) if t[0] == 'Potential_type'), -1)
                    if idx != -1:
                        sf.tags[idx][1] = potentialType
                    else:
                        sf.add_tag('Potential_type', potentialType)
            if not replaced:
                self.__addSf(constraintType=constraintType, potentialType=potentialType)

        return self.sfDict[key][-1]

    def __trimSfWoLp(self):
        if self.__cur_subtype not in self.__lastSfDict:
            return
        if self.__lastSfDict[self.__cur_subtype]['index_id'] > 0:
            return
        for k, v in self.sfDict.items():
            for item in reversed(v):
                if item == self.__lastSfDict:
                    v.remove(item)
                    if len(v) == 0:
                        del self.sfDict[k]
                    self.__listIdCounter = decListIdCounter(k[0], self.__listIdCounter)
                    return

    def getContentSubtype(self):
        """ Return content subtype of CHARMM MR file.
        """

        contentSubtype = {'dist_restraint': self.distRestraints,
                          'dihed_restraint': self.dihedRestraints,
                          'geo_restraint': self.geoRestraints
                          }

        return {k: 1 for k, v in contentSubtype.items() if v > 0}

    def getPolymerSequence(self):
        """ Return polymer sequence of CHARMM MR file.
        """
        return None if self.__polySeqRst is None or len(self.__polySeqRst) == 0 else self.__polySeqRst

    def getSequenceAlignment(self):
        """ Return sequence alignment between coordinates and CHARMM MR.
        """
        return None if self.__seqAlign is None or len(self.__seqAlign) == 0 else self.__seqAlign

    def getChainAssignment(self):
        """ Return chain assignment between coordinates and CHARMM MR.
        """
        return None if self.__chainAssign is None or len(self.__chainAssign) == 0 else self.__chainAssign

    def getReasonsForReparsing(self):
        """ Return reasons for re-parsing CHARMM MR file.
        """
        return None if len(self.reasonsForReParsing) == 0 else self.reasonsForReParsing

    def getSfDict(self):
        """ Return a dictionary of pynmrstar saveframes.
        """
        if len(self.sfDict) == 0:
            return self.__listIdCounter, None
        ign_keys = []
        for k, v in self.sfDict.items():
            for item in reversed(v):
                if item['index_id'] == 0:
                    v.remove(item)
                    if len(v) == 0:
                        ign_keys.append(k)
                    self.__listIdCounter = decListIdCounter(k[0], self.__listIdCounter)
        for k in ign_keys:
            del self.sfDict[k]
        return self.__listIdCounter, None if len(self.sfDict) == 0 else self.sfDict

# del CharmmMRParser
