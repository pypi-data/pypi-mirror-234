##
# File: CyanaMRParserListener.py
# Date: 27-Jan-2022
#
# Updates:
""" ParserLister class for CYANA MR files.
    @author: Masashi Yokochi
"""
import sys
import re
import itertools
import numpy
import copy
import collections

from antlr4 import ParseTreeListener

try:
    from wwpdb.utils.align.alignlib import PairwiseAlign  # pylint: disable=no-name-in-module
    from wwpdb.utils.nmr.mr.CyanaMRParser import CyanaMRParser
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (coordAssemblyChecker,
                                                       extendCoordChainsForExactNoes,
                                                       translateToStdResName,
                                                       translateToStdAtomName,
                                                       getRdcCode,
                                                       isIdenticalRestraint,
                                                       isLongRangeRestraint,
                                                       hasIntraChainRestraint,
                                                       hasInterChainRestraint,
                                                       isAmbigAtomSelection,
                                                       isCyclicPolymer,
                                                       getAltProtonIdInBondConstraint,
                                                       isLikePheOrTyr,
                                                       getRestraintName,
                                                       contentSubtypeOf,
                                                       incListIdCounter,
                                                       decListIdCounter,
                                                       getSaveframe,
                                                       getLoop,
                                                       getRow,
                                                       getDistConstraintType,
                                                       getPotentialType,
                                                       getDstFuncForHBond,
                                                       getDstFuncForSsBond,
                                                       ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS,
                                                       REPRESENTATIVE_MODEL_ID,
                                                       MAX_PREF_LABEL_SCHEME_COUNT,
                                                       THRESHHOLD_FOR_CIRCULAR_SHIFT,
                                                       DIST_RESTRAINT_RANGE,
                                                       DIST_RESTRAINT_ERROR,
                                                       ANGLE_RESTRAINT_RANGE,
                                                       ANGLE_RESTRAINT_ERROR,
                                                       RDC_RESTRAINT_RANGE,
                                                       RDC_RESTRAINT_ERROR,
                                                       PCS_RESTRAINT_RANGE,
                                                       PCS_RESTRAINT_ERROR,
                                                       DIST_AMBIG_LOW,
                                                       DIST_AMBIG_UP,
                                                       DIST_AMBIG_MED,
                                                       DIST_AMBIG_UNCERT,
                                                       KNOWN_ANGLE_NAMES,
                                                       KNOWN_ANGLE_ATOM_NAMES,
                                                       KNOWN_ANGLE_SEQ_OFFSET,
                                                       KNOWN_ANGLE_CARBO_ATOM_NAMES,
                                                       KNOWN_ANGLE_CARBO_SEQ_OFFSET,
                                                       CYANA_MR_FILE_EXTS,
                                                       CARTN_DATA_ITEMS)
    from wwpdb.utils.nmr.ChemCompUtil import ChemCompUtil
    from wwpdb.utils.nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from wwpdb.utils.nmr.NEFTranslator.NEFTranslator import NEFTranslator
    from wwpdb.utils.nmr.AlignUtil import (LARGE_ASYM_ID,
                                           monDict3,
                                           protonBeginCode,
                                           aminoProtonCode,
                                           rdcBbPairCode,
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
    from nmr.mr.CyanaMRParser import CyanaMRParser
    from nmr.mr.ParserListenerUtil import (coordAssemblyChecker,
                                           extendCoordChainsForExactNoes,
                                           translateToStdResName,
                                           translateToStdAtomName,
                                           getRdcCode,
                                           isIdenticalRestraint,
                                           isLongRangeRestraint,
                                           hasIntraChainRestraint,
                                           hasInterChainRestraint,
                                           isAmbigAtomSelection,
                                           isCyclicPolymer,
                                           getAltProtonIdInBondConstraint,
                                           isLikePheOrTyr,
                                           getRestraintName,
                                           contentSubtypeOf,
                                           incListIdCounter,
                                           decListIdCounter,
                                           getSaveframe,
                                           getLoop,
                                           getRow,
                                           getDistConstraintType,
                                           getPotentialType,
                                           getDstFuncForHBond,
                                           getDstFuncForSsBond,
                                           ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS,
                                           REPRESENTATIVE_MODEL_ID,
                                           MAX_PREF_LABEL_SCHEME_COUNT,
                                           THRESHHOLD_FOR_CIRCULAR_SHIFT,
                                           DIST_RESTRAINT_RANGE,
                                           DIST_RESTRAINT_ERROR,
                                           ANGLE_RESTRAINT_RANGE,
                                           ANGLE_RESTRAINT_ERROR,
                                           RDC_RESTRAINT_RANGE,
                                           RDC_RESTRAINT_ERROR,
                                           PCS_RESTRAINT_RANGE,
                                           PCS_RESTRAINT_ERROR,
                                           DIST_AMBIG_LOW,
                                           DIST_AMBIG_UP,
                                           DIST_AMBIG_MED,
                                           DIST_AMBIG_UNCERT,
                                           KNOWN_ANGLE_NAMES,
                                           KNOWN_ANGLE_ATOM_NAMES,
                                           KNOWN_ANGLE_SEQ_OFFSET,
                                           KNOWN_ANGLE_CARBO_ATOM_NAMES,
                                           KNOWN_ANGLE_CARBO_SEQ_OFFSET,
                                           CYANA_MR_FILE_EXTS,
                                           CARTN_DATA_ITEMS)
    from nmr.ChemCompUtil import ChemCompUtil
    from nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from nmr.NEFTranslator.NEFTranslator import NEFTranslator
    from nmr.AlignUtil import (LARGE_ASYM_ID,
                               monDict3,
                               protonBeginCode,
                               aminoProtonCode,
                               rdcBbPairCode,
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


RDC_RANGE_MIN = RDC_RESTRAINT_RANGE['min_inclusive']
RDC_RANGE_MAX = RDC_RESTRAINT_RANGE['max_inclusive']

RDC_ERROR_MIN = RDC_RESTRAINT_ERROR['min_exclusive']
RDC_ERROR_MAX = RDC_RESTRAINT_ERROR['max_exclusive']


PCS_RANGE_MIN = PCS_RESTRAINT_RANGE['min_inclusive']
PCS_RANGE_MAX = PCS_RESTRAINT_RANGE['max_inclusive']

PCS_ERROR_MIN = PCS_RESTRAINT_ERROR['min_exclusive']
PCS_ERROR_MAX = PCS_RESTRAINT_ERROR['max_exclusive']


# This class defines a complete listener for a parse tree produced by CyanaMRParser.
class CyanaMRParserListener(ParseTreeListener):

    __file_type = 'nm-res-cya'

    __verbose = None
    __lfh = None
    __debug = False
    __remediate = False

    __createSfDict = False
    __omitDistLimitOutlier = True
    __allowZeroUpperLimit = False
    __correctCircularShift = True
    __applyPdbStatCap = False

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

    __upl_or_lol = None  # must be one of (None, 'upl_only', 'upl_w_lol', 'lol_only', 'lol_w_upl')

    __file_ext = None  # must be one of (None, 'upl', 'lol', 'aco', 'rdc', 'pcs', 'upv', 'lov', 'cco')
    __cur_dist_type = ''
    __local_dist_types = []  # list items must be one of ('upl', 'lol')

    # CIF reader
    __cR = None
    __hasCoord = False

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
    __gapInAuthSeq = False

    # chain number dictionary
    __chainNumberDict = None

    # polymer sequence of MR file
    __polySeqRst = None

    __seqAlign = None
    __chainAssign = None

    # current restraint subtype
    __cur_subtype = ''
    __cur_subtype_altered = False
    __cur_comment_inlined = False
    __cur_rdc_orientation = 0

    # column_order of distance restraints with chain
    __col_order_of_dist_w_chain = {}

    # RDC parameter dictionary
    rdcParameterDict = None

    # PCS parameter dictionary
    pcsParameterDict = None

    # collection of atom selection
    atomSelectionSet = []

    # collection of number selection
    numberSelection = []

    # collection of auxiliary atom selection
    auxAtomSelectionSet = ''

    # current residue name for atom name mapping
    __cur_resname_for_mapping = ''

    # unambigous atom name mapping
    unambigAtomNameMapping = {}

    # ambigous atom name mapping
    ambigAtomNameMapping = {}

    # collection of general atom name extended with ambig code
    genAtomNameSelection = []

    __f = None
    warningMessage = None

    reasonsForReParsing = {}

    # original source MR file name
    __originalFileName = '.'

    # list id counter
    __listIdCounter = {}

    # entry ID
    __entryId = '.'

    # dictionary of pynmrstar saveframes
    sfDict = {}

    # current constraint type
    __cur_constraint_type = None

    # last edited pynmrstar saveframe
    __lastSfDict = {}

    def __init__(self, verbose=True, log=sys.stdout,
                 representativeModelId=REPRESENTATIVE_MODEL_ID,
                 mrAtomNameMapping=None,
                 cR=None, caC=None, ccU=None, csStat=None, nefT=None,
                 reasons=None, upl_or_lol=None, file_ext=None):
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

        if self.__hasPolySeq:
            self.__gapInAuthSeq = any(ps for ps in self.__polySeq if ps['gap_in_auth_seq'])

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

        self.__upl_or_lol = upl_or_lol

        if upl_or_lol not in (None, 'upl_only', 'upl_w_lol', 'lol_only', 'lol_w_upl'):
            msg = f"The argument 'upl_or_lol' must be one of {(None, 'upl_only', 'upl_w_lol', 'lol_only', 'lol_w_upl')}"
            log.write(f"'+CyanaMRParserListener.__init__() ++ ValueError  -  {msg}")
            raise ValueError(f"'+CyanaMRParserListener.__init__() ++ ValueError  -  {msg}")

        self.__file_ext = file_ext

        if file_ext not in CYANA_MR_FILE_EXTS:
            msg = f"The argument 'file_ext' must be one of {CYANA_MR_FILE_EXTS}"
            log.write(f"'+CyanaMRParserListener.__init__() ++ ValueError  -  {msg}")
            raise ValueError(f"'+CyanaMRParserListener.__init__() ++ ValueError  -  {msg}")

        if upl_or_lol is None and file_ext is not None:

            if file_ext == 'upl':
                self.__upl_or_lol = 'upl_w_lol'

            if file_ext == 'lol':
                self.__upl_or_lol = 'lol_w_upl'

        self.__max_dist_value = DIST_ERROR_MIN
        self.__min_dist_value = DIST_ERROR_MAX
        self.__col_order_of_dist_w_chain = {}

        self.__dihed_lb_greater_than_ub = False
        self.__dihed_ub_always_positive = True

        self.distRestraints = 0      # CYANA: Distance restraint file (.upl or .lol)
        self.dihedRestraints = 0     # CYANA: Torsion angle restraint file (.aco)
        self.rdcRestraints = 0       # CYANA: Residual dipolar coupling restraint file (.rdc)
        self.pcsRestraints = 0       # CYANA: Pseudocontact shift restraint file (.pcs)
        self.noepkRestraints = 0     # CYANA: NOESY volume restraint file (.upv or .lov)
        self.jcoupRestraints = 0     # CYANA: Scalar coupling constant restraint file (.cco)
        self.geoRestraints = 0       # CYANA: Coordinate geometry restraints
        self.hbondRestraints = 0     # CYANA: Hydrogen bond geometry restraints
        self.ssbondRestraints = 0    # CYANA: Disulfide bond geometry restraints
        self.fchiralRestraints = 0   # CYANA: Floating chiral stereo assignments

        self.sfDict = {}

    def setDebugMode(self, debug):
        self.__debug = debug

    def setRemediateMode(self, remediate):
        self.__remediate = remediate

    def createSfDict(self, createSfDict):
        self.__createSfDict = createSfDict

    def setOriginaFileName(self, originalFileName):
        self.__originalFileName = originalFileName

    def setListIdCounter(self, listIdCounter):
        self.__listIdCounter = listIdCounter

    def setEntryId(self, entryId):
        self.__entryId = entryId

    # Enter a parse tree produced by CyanaMRParser#cyana_mr.
    def enterCyana_mr(self, ctx: CyanaMRParser.Cyana_mrContext):  # pylint: disable=unused-argument
        self.__chainNumberDict = {}
        self.__polySeqRst = []
        self.__f = []

    # Exit a parse tree produced by CyanaMRParser#cyana_mr.
    def exitCyana_mr(self, ctx: CyanaMRParser.Cyana_mrContext):  # pylint: disable=unused-argument

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

                if self.__reasons is None and any(f for f in self.__f if 'Atom not found' in f):
                    if len(self.unambigAtomNameMapping) > 0:
                        if 'unambig_atom_id_remap' not in self.reasonsForReParsing:
                            self.reasonsForReParsing['unambig_atom_id_remap'] = self.unambigAtomNameMapping
                    if len(self.ambigAtomNameMapping) > 0:
                        if 'ambig_atom_id_remap' not in self.reasonsForReParsing:
                            self.reasonsForReParsing['ambig_atom_id_remap'] = self.ambigAtomNameMapping
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

            if self.__remediate:
                if self.__dihed_lb_greater_than_ub and self.__dihed_ub_always_positive:
                    if 'dihed_unusual_order' not in self.reasonsForReParsing:
                        self.reasonsForReParsing['dihed_unusual_order'] = True

        finally:
            self.warningMessage = sorted(list(set(self.__f)), key=self.__f.index)

    # Enter a parse tree produced by CyanaMRParser#comment.
    def enterComment(self, ctx: CyanaMRParser.CommentContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#comment.
    def exitComment(self, ctx: CyanaMRParser.CommentContext):
        if self.__cur_comment_inlined:
            return

        for col in range(20):
            if ctx.Any_name(col):
                text = str(ctx.Any_name(col)).lower()
                if 'cco' in text or 'coupling' in text:
                    self.__cur_dist_type = 'cco'
                    break
                if ('upl' in text or 'upper' in text) and not ('lol' in text or 'lower' in text):
                    self.__cur_dist_type = 'upl'
                    break
                if ('lol' in text or 'lower' in text) and not ('upl' in text or 'upper' in text):
                    self.__cur_dist_type = 'lol'
                    break
            else:
                break

    # Enter a parse tree produced by CyanaMRParser#distance_restraints.
    def enterDistance_restraints(self, ctx: CyanaMRParser.Distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist' if self.__file_ext is None or self.__file_ext != 'cco' else 'jcoup'

        self.__cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#distance_restraints.
    def exitDistance_restraints(self, ctx: CyanaMRParser.Distance_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#distance_restraint.
    def enterDistance_restraint(self, ctx: CyanaMRParser.Distance_restraintContext):  # pylint: disable=unused-argument
        if self.__cur_subtype == 'dist':
            self.distRestraints += 1
        elif self.__cur_subtype == 'jcoup':
            self.jcoupRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#distance_restraint.
    def exitDistance_restraint(self, ctx: CyanaMRParser.Distance_restraintContext):

        if self.__cur_subtype == 'dist' and (self.__cur_dist_type == 'cco' or len(self.numberSelection) == 6):
            self.__cur_subtype = 'jcoup'
            self.distRestraints -= 1
            self.jcoupRestraints += 1

        try:

            if None in self.genAtomNameSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                elif self.__cur_subtype == 'jcoup':
                    self.jcoupRestraints -= 1
                return

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = self.genAtomNameSelection[0].upper()
            seqId2 = int(str(ctx.Integer(1)))
            compId2 = str(ctx.Simple_name(1)).upper()
            atomId2 = self.genAtomNameSelection[1].upper()

            if len(compId1) == 1 and len(compId2) == 1 and compId1.isalpha() and compId2.isalpha():
                atom_like = self.__csStat.getAtomLikeNameSet(True, True, 1)
                if atomId1 in atom_like and atomId2 in atom_like:
                    self.exitDistance_wo_comp_restraint(compId1, seqId1, atomId1, compId2, seqId2, atomId2)
                    return

            target_value = None
            lower_limit = None
            upper_limit = None
            target_value_uncertainty = None

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                elif self.__cur_subtype == 'jcoup':
                    self.jcoupRestraints -= 1
                return

            if self.__cur_subtype == 'dist':

                value = self.numberSelection[0]
                weight = 1.0

                delta = None
                has_square = False

                if len(self.numberSelection) > 2:
                    value2 = self.numberSelection[1]
                    weight = self.numberSelection[2]

                    has_square = True

                elif len(self.numberSelection) > 1:
                    value2 = self.numberSelection[1]

                    if value2 <= 1.0 or value2 < value:
                        delta = abs(value2)
                    else:
                        has_square = True

                if weight < 0.0:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    f"The relative weight value of '{weight}' must not be a negative value.")
                    return
                if weight == 0.0:
                    self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                    f"The relative weight value of '{weight}' should be a positive value.")

                if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX and not self.__cur_subtype_altered:
                    if value > self.__max_dist_value:
                        self.__max_dist_value = value
                    if value < self.__min_dist_value:
                        self.__min_dist_value = value

                if has_square:

                    if 'upl' in (self.__file_ext, self.__cur_dist_type):
                        upper_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                        lower_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif value2 > DIST_RANGE_MAX:  # lol_only
                        lower_limit = value

                    elif (0.0 if self.__file_ext in ('upl', 'lol') else 1.8) <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                        upper_limit = value2
                        lower_limit = value
                        if self.__applyPdbStatCap:
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # upl_only
                        if value2 > 1.8:
                            upper_limit = value2
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            upper_limit = value2

                elif delta is not None:

                    if 'upl' in (self.__file_ext, self.__cur_dist_type):
                        upper_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                        lower_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    else:
                        if self.__applyPdbStatCap:
                            target_value = value
                            if delta > 0.0:
                                lower_limit = value - delta
                                upper_limit = value + delta
                        else:
                            if value > 1.8:
                                upper_limit = value
                            else:
                                lower_limit = value
                            if value2 > 0.0:
                                target_value_uncertainty = value2

                elif 'upl' in (self.__file_ext, self.__cur_dist_type):
                    upper_limit = value

                elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                    lower_limit = value

                elif self.__upl_or_lol is None:
                    if self.__cur_dist_type == 'upl':
                        upper_limit = value
                    elif self.__cur_dist_type == 'lol':
                        lower_limit = value
                    elif value > 1.8:
                        upper_limit = value
                    else:
                        lower_limit = value

                elif self.__upl_or_lol == 'upl_only':
                    if self.__cur_dist_type == 'upl':
                        upper_limit = value
                        if self.__applyPdbStatCap:
                            lower_limit = 1.8  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                    elif self.__cur_dist_type == 'lol':
                        lower_limit = value
                    elif value > 1.8:
                        upper_limit = value
                        if self.__applyPdbStatCap:
                            lower_limit = 1.8  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                    else:
                        lower_limit = value

                elif self.__upl_or_lol == 'upl_w_lol':
                    upper_limit = value

                elif self.__upl_or_lol == 'lol_only':
                    lower_limit = value
                    if self.__applyPdbStatCap:
                        upper_limit = 5.5  # default value of PDBStat
                        target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                else:  # 'lol_w_upl'
                    lower_limit = value

                if len(self.__cur_dist_type) > 0 and self.__cur_dist_type not in self.__local_dist_types:
                    self.__local_dist_types.append(self.__cur_dist_type)

                if not self.__hasPolySeq and not self.__hasNonPolySeq:  # can't decide whether NOE or RDC wo the coordinates
                    return

                self.__retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if len(self.atomSelectionSet[0]) == 1 and len(self.atomSelectionSet[1]) == 1:

                    isRdc = True

                    chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                    seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                    comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                    atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                    chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                    seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                    comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                    atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                    if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                        isRdc = False

                    if chain_id_1 != chain_id_2:
                        isRdc = False

                    if abs(seq_id_1 - seq_id_2) > 1:
                        isRdc = False

                    if abs(seq_id_1 - seq_id_2) == 1:

                        if self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                                ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                                 or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')):
                            pass

                        else:
                            isRdc = False

                    elif atom_id_1 == atom_id_2:
                        isRdc = False

                    elif self.__ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                        if not self.__ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                            if self.__nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.__nefT.validate_comp_atom(comp_id_2, atom_id_2):
                                isRdc = False

                    if not isRdc:
                        self.__cur_subtype_altered = False

                    else:

                        isRdc = False

                        if self.__cur_subtype_altered and atom_id_1 + atom_id_2 == self.auxAtomSelectionSet:
                            isRdc = True

                        elif value < 1.0 or value > 6.0:
                            self.auxAtomSelectionSet = atom_id_1 + atom_id_2
                            self.__cur_subtype_altered = True
                            self.__cur_rdc_orientation += 1
                            isRdc = True

                        if isRdc:
                            self.__cur_subtype = 'rdc'
                            self.rdcRestraints += 1
                            self.distRestraints -= 1

                            target_value = value
                            lower_limit = upper_limit = None

                            if len(self.numberSelection) > 2:
                                error = abs(self.numberSelection[1])
                                lower_limit = target_value - error
                                upper_limit = target_value + error

                            dstFunc = self.validateRdcRange(weight, self.__cur_rdc_orientation, target_value, lower_limit, upper_limit)

                            if dstFunc is None:
                                return

                            if self.__createSfDict:
                                sf = self.__getSf(potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc),
                                                  rdcCode=getRdcCode([self.atomSelectionSet[0][0], self.atomSelectionSet[1][0]]),
                                                  orientationId=self.__cur_rdc_orientation)
                                sf['id'] += 1

                            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                                  self.atomSelectionSet[1]):
                                if isIdenticalRestraint([atom1, atom2]):
                                    continue
                                if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None):
                                    continue
                                if self.__debug:
                                    print(f"subtype={self.__cur_subtype} id={self.rdcRestraints} "
                                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                                if self.__createSfDict and sf is not None:
                                    sf['index_id'] += 1
                                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                                 '.', None, None,
                                                 sf['list_id'], self.__entryId, dstFunc,
                                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                                 atom1, atom2)
                                    sf['loop'].add_data(row)

                            self.__cur_subtype = 'dist'

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

                dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit,
                                                     target_value_uncertainty,
                                                     self.__omitDistLimitOutlier)

                if dstFunc is None:
                    return

                if self.__createSfDict:
                    sf = self.__getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                           self.__csStat, self.__originalFileName),
                                      potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

                if self.__createSfDict:
                    if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                        memberLogicCode = '.'

                    memberId = '.'
                    if memberLogicCode == 'OR':
                        if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                           and (isAmbigAtomSelection(self.atomSelectionSet[0], self.__csStat)
                                or isAmbigAtomSelection(self.atomSelectionSet[1], self.__csStat)):
                            memberId = 0
                            _atom1 = _atom2 = None

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isIdenticalRestraint([atom1, atom2]):
                        continue
                    if has_intra_chain and (atom1['chain_id'] != atom2['chain_id'] or atom1['chain_id'] not in rep_chain_id_set):
                        continue
                    if self.__createSfDict and memberLogicCode == '.':
                        altAtomId1, altAtomId2 = getAltProtonIdInBondConstraint([atom1, atom2], self.__csStat)
                        if altAtomId1 is not None or altAtomId2 is not None:
                            atom1, atom2 =\
                                self.selectRealisticBondConstraint(atom1, atom2,
                                                                   altAtomId1, altAtomId2,
                                                                   dstFunc)
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
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

            else:  # cco

                target = self.numberSelection[0]
                error = None

                weight = 1.0
                if len(self.numberSelection) > 2:
                    error = abs(self.numberSelection[1])
                    weight = self.numberSelection[2]

                elif len(self.numberSelection) > 1:
                    error = abs(self.numberSelection[1])

                if weight < 0.0:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    f"The relative weight value of '{weight}' must not be a negative value.")
                    return
                if weight == 0.0:
                    self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                    f"The relative weight value of '{weight}' should be a positive value.")

                target_value = target
                lower_limit = target - error if error is not None else None
                upper_limit = target + error if error is not None else None

                dstFunc = self.validateRdcRange(weight, None, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.__hasPolySeq and not self.__hasNonPolySeq:
                    return

                self.__retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if not self.areUniqueCoordAtoms('a Scalar coupling'):
                    return

                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Non-magnetic susceptible spin appears in scalar coupling constant; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                    f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

                if chain_id_1 != chain_id_2:
                    ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                    ps2 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                    if ps1 is None and ps2 is None:
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found inter-chain scalar coupling constant; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif abs(seq_id_1 - seq_id_2) > 1:

                    if abs(seq_id_1 - seq_id_2) > 2 or {atom_id_1, atom_id_2} != {'H', 'N'}:
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found inter-residue scalar coupling constant; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif abs(seq_id_1 - seq_id_2) == 1:

                    if self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                            ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                             or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')
                             or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 == 'H')
                             or (seq_id_1 > seq_id_2 and atom_id_1 == 'H' and atom_id_2.startswith('HA'))
                             or {atom_id_1, atom_id_2} == {'H', 'N'}):
                        pass

                    else:
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found inter-residue scalar coupling constant; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif atom_id_1 == atom_id_2:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Found zero scalar coupling constant; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

                if self.__createSfDict:
                    sf = self.__getSf()
                    sf['id'] += 1

                for atom1, atom4 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isLongRangeRestraint([atom1, atom4], self.__polySeq if self.__gapInAuthSeq else None):
                        if {atom1['atom_id'], atom4['atom_id']} != {'H', 'N'}:
                            continue
                    self.__ccU.updateChemCompDict(atom1['comp_id'])
                    atom2_can = self.__ccU.getBondedAtoms(atom1['comp_id'], atom1['atom_id'])
                    atom3_can = self.__ccU.getBondedAtoms(atom1['comp_id'], atom4['atom_id'])
                    atom_id_2 = atom_id_3 = None
                    for ccb in self.__ccU.lastBonds:
                        if ccb[self.__ccU.ccbAtomId1] in atom2_can and ccb[self.__ccU.ccbAtomId2] in atom3_can:
                            atom_id_2 = ccb[self.__ccU.ccbAtomId1]
                            atom_id_3 = ccb[self.__ccU.ccbAtomId2]
                            break
                        if ccb[self.__ccU.ccbAtomId2] in atom2_can and ccb[self.__ccU.ccbAtomId1] in atom3_can:
                            atom_id_2 = ccb[self.__ccU.ccbAtomId2]
                            atom_id_3 = ccb[self.__ccU.ccbAtomId1]
                            break
                    if atom_id_2 is None or atom_id_3 is None:
                        continue
                    atom2 = copy.copy(atom1)
                    atom2['atom_id'] = atom_id_2
                    atom3 = copy.copy(atom4)
                    atom3['atom_id'] = atom_id_3
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.jcoupRestraints} "
                              f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.__entryId, dstFunc,
                                     self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                     atom1, atom2, atom3, atom4)
                        sf['loop'].add_data(row)

        except ValueError:
            if self.__cur_subtype == 'dist':
                self.distRestraints -= 1
            elif self.__cur_subtype == 'jcoup':
                self.jcoupRestraints -= 1
        finally:
            self.numberSelection.clear()
            self.genAtomNameSelection.clear()

    # Exit a parse tree produced by CyanaMRParser#distance_restraint.
    def exitDistance_wo_comp_restraint(self, chainId1, seqId1, atomId1, chainId2, seqId2, atomId2):

        try:

            target_value = None
            lower_limit = None
            upper_limit = None
            target_value_uncertainty = None

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                elif self.__cur_subtype == 'jcoup':
                    self.jcoupRestraints -= 1
                return

            if self.__cur_subtype == 'dist':

                value = self.numberSelection[0]
                weight = 1.0

                delta = None
                has_square = False

                if len(self.numberSelection) > 2:
                    value2 = self.numberSelection[1]
                    weight = self.numberSelection[2]

                    has_square = True

                elif len(self.numberSelection) > 1:
                    value2 = self.numberSelection[1]

                    if value2 <= 1.0 or value2 < value:
                        delta = abs(value2)
                    else:
                        has_square = True

                if weight < 0.0:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    f"The relative weight value of '{weight}' must not be a negative value.")
                    return
                if weight == 0.0:
                    self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                    f"The relative weight value of '{weight}' should be a positive value.")

                if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX and not self.__cur_subtype_altered:
                    if value > self.__max_dist_value:
                        self.__max_dist_value = value
                    if value < self.__min_dist_value:
                        self.__min_dist_value = value

                if has_square:

                    if 'upl' in (self.__file_ext, self.__cur_dist_type):
                        upper_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                        lower_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif value2 > DIST_RANGE_MAX:  # lol_only
                        lower_limit = value

                    elif (0.0 if self.__file_ext in ('upl', 'lol') else 1.8) <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                        upper_limit = value2
                        lower_limit = value
                        if self.__applyPdbStatCap:
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # upl_only
                        if value2 > 1.8:
                            upper_limit = value2
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            upper_limit = value2

                elif delta is not None:

                    if 'upl' in (self.__file_ext, self.__cur_dist_type):
                        upper_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                        lower_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    else:
                        if self.__applyPdbStatCap:
                            target_value = value
                            if delta > 0.0:
                                lower_limit = value - delta
                                upper_limit = value + delta
                        else:
                            upper_limit = value
                            if value2 > 0.0:
                                target_value_uncertainty = value2

                elif 'upl' in (self.__file_ext, self.__cur_dist_type):
                    upper_limit = value

                elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                    lower_limit = value

                elif self.__upl_or_lol is None:
                    if self.__cur_dist_type == 'upl':
                        upper_limit = value
                    elif self.__cur_dist_type == 'lol':
                        lower_limit = value
                    elif value > 1.8:
                        upper_limit = value
                    else:
                        lower_limit = value

                elif self.__upl_or_lol == 'upl_only':
                    if self.__cur_dist_type == 'upl':
                        upper_limit = value
                        if self.__applyPdbStatCap:
                            lower_limit = 1.8  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                    elif self.__cur_dist_type == 'lol':
                        lower_limit = value
                    elif value > 1.8:
                        upper_limit = value
                        if self.__applyPdbStatCap:
                            lower_limit = 1.8  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                    else:
                        lower_limit = value

                elif self.__upl_or_lol == 'upl_w_lol':
                    upper_limit = value

                elif self.__upl_or_lol == 'lol_only':
                    lower_limit = value
                    if self.__applyPdbStatCap:
                        upper_limit = 5.5  # default value of PDBStat
                        target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                else:  # 'lol_w_upl'
                    lower_limit = value

                if len(self.__cur_dist_type) > 0 and self.__cur_dist_type not in self.__local_dist_types:
                    self.__local_dist_types.append(self.__cur_dist_type)

                if not self.__hasPolySeq and not self.__hasNonPolySeq:  # can't decide whether NOE or RDC wo the coordinates
                    return

                self.__retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId1, seqId1, atomId1)
                chainAssign2 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId2, seqId2, atomId2)

                if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, None, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if len(self.atomSelectionSet[0]) == 1 and len(self.atomSelectionSet[1]) == 1:

                    isRdc = True

                    chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                    seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                    comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                    atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                    chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                    seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                    comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                    atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                    if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                        isRdc = False

                    if chain_id_1 != chain_id_2:
                        isRdc = False

                    if abs(seq_id_1 - seq_id_2) > 1:
                        isRdc = False

                    if abs(seq_id_1 - seq_id_2) == 1:

                        if self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                                ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                                 or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')):
                            pass

                        else:
                            isRdc = False

                    elif atom_id_1 == atom_id_2:
                        isRdc = False

                    elif self.__ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                        if not self.__ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                            if self.__nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.__nefT.validate_comp_atom(comp_id_2, atom_id_2):
                                isRdc = False

                    if not isRdc:
                        self.__cur_subtype_altered = False

                    else:

                        isRdc = False

                        if self.__cur_subtype_altered and atom_id_1 + atom_id_2 == self.auxAtomSelectionSet:
                            isRdc = True

                        elif value < 1.0 or value > 6.0:
                            self.auxAtomSelectionSet = atom_id_1 + atom_id_2
                            self.__cur_subtype_altered = True
                            self.__cur_rdc_orientation += 1
                            isRdc = True

                        if isRdc:
                            self.__cur_subtype = 'rdc'
                            self.rdcRestraints += 1
                            self.distRestraints -= 1

                            target_value = value
                            lower_limit = upper_limit = None

                            if len(self.numberSelection) > 2:
                                error = abs(self.numberSelection[1])
                                lower_limit = target_value - error
                                upper_limit = target_value + error

                            dstFunc = self.validateRdcRange(weight, self.__cur_rdc_orientation, target_value, lower_limit, upper_limit)

                            if dstFunc is None:
                                return

                            if self.__createSfDict:
                                sf = self.__getSf(potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc),
                                                  rdcCode=getRdcCode([self.atomSelectionSet[0][0], self.atomSelectionSet[1][0]]),
                                                  orientationId=self.__cur_rdc_orientation)
                                sf['id'] += 1

                            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                                  self.atomSelectionSet[1]):
                                if isIdenticalRestraint([atom1, atom2]):
                                    continue
                                if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None):
                                    continue
                                if self.__debug:
                                    print(f"subtype={self.__cur_subtype} id={self.rdcRestraints} "
                                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                                if self.__createSfDict and sf is not None:
                                    sf['index_id'] += 1
                                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                                 '.', None, None,
                                                 sf['list_id'], self.__entryId, dstFunc,
                                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                                 atom1, atom2)
                                    sf['loop'].add_data(row)

                            self.__cur_subtype = 'dist'

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

                dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit,
                                                     target_value_uncertainty,
                                                     self.__omitDistLimitOutlier)

                if dstFunc is None:
                    return

                if self.__createSfDict:
                    sf = self.__getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                           self.__csStat, self.__originalFileName),
                                      potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

                if self.__createSfDict:
                    if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                        memberLogicCode = '.'

                    memberId = '.'
                    if memberLogicCode == 'OR':
                        if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                           and (isAmbigAtomSelection(self.atomSelectionSet[0], self.__csStat)
                                or isAmbigAtomSelection(self.atomSelectionSet[1], self.__csStat)):
                            memberId = 0
                            _atom1 = _atom2 = None

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isIdenticalRestraint([atom1, atom2]):
                        continue
                    if has_intra_chain and (atom1['chain_id'] != atom2['chain_id'] or atom1['chain_id'] not in rep_chain_id_set):
                        continue
                    if self.__createSfDict and memberLogicCode == '.':
                        altAtomId1, altAtomId2 = getAltProtonIdInBondConstraint([atom1, atom2], self.__csStat)
                        if altAtomId1 is not None or altAtomId2 is not None:
                            atom1, atom2 =\
                                self.selectRealisticBondConstraint(atom1, atom2,
                                                                   altAtomId1, altAtomId2,
                                                                   dstFunc)
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
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

            else:  # cco

                target = self.numberSelection[0]
                error = None

                weight = 1.0
                if len(self.numberSelection) > 2:
                    error = abs(self.numberSelection[1])
                    weight = self.numberSelection[2]

                elif len(self.numberSelection) > 1:
                    error = abs(self.numberSelection[1])

                if weight < 0.0:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    f"The relative weight value of '{weight}' must not be a negative value.")
                    return
                if weight == 0.0:
                    self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                    f"The relative weight value of '{weight}' should be a positive value.")

                target_value = target
                lower_limit = target - error if error is not None else None
                upper_limit = target + error if error is not None else None

                dstFunc = self.validateRdcRange(weight, None, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.__hasPolySeq and not self.__hasNonPolySeq:
                    return

                self.__retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId1, seqId1, atomId1)
                chainAssign2 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId2, seqId2, atomId2)

                if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, None, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if not self.areUniqueCoordAtoms('a Scalar coupling'):
                    return

                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Non-magnetic susceptible spin appears in scalar coupling constant; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                    f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

                if chain_id_1 != chain_id_2:
                    ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                    ps2 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                    if ps1 is None and ps2 is None:
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found inter-chain scalar coupling constant; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif abs(seq_id_1 - seq_id_2) > 1:

                    if abs(seq_id_1 - seq_id_2) > 2 or {atom_id_1, atom_id_2} != {'H', 'N'}:
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found inter-residue scalar coupling constant; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif abs(seq_id_1 - seq_id_2) == 1:

                    if self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                            ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                             or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')
                             or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 == 'H')
                             or (seq_id_1 > seq_id_2 and atom_id_1 == 'H' and atom_id_2.startswith('HA'))
                             or {atom_id_1, atom_id_2} == {'H', 'N'}):
                        pass

                    else:
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found inter-residue scalar coupling constant; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif atom_id_1 == atom_id_2:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Found zero scalar coupling constant; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

                if self.__createSfDict:
                    sf = self.__getSf()
                    sf['id'] += 1

                for atom1, atom4 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isLongRangeRestraint([atom1, atom4], self.__polySeq if self.__gapInAuthSeq else None):
                        if {atom1['atom_id'], atom4['atom_id']} != {'H', 'N'}:
                            continue
                    self.__ccU.updateChemCompDict(atom1['comp_id'])
                    atom2_can = self.__ccU.getBondedAtoms(atom1['comp_id'], atom1['atom_id'])
                    atom3_can = self.__ccU.getBondedAtoms(atom1['comp_id'], atom4['atom_id'])
                    atom_id_2 = atom_id_3 = None
                    for ccb in self.__ccU.lastBonds:
                        if ccb[self.__ccU.ccbAtomId1] in atom2_can and ccb[self.__ccU.ccbAtomId2] in atom3_can:
                            atom_id_2 = ccb[self.__ccU.ccbAtomId1]
                            atom_id_3 = ccb[self.__ccU.ccbAtomId2]
                            break
                        if ccb[self.__ccU.ccbAtomId2] in atom2_can and ccb[self.__ccU.ccbAtomId1] in atom3_can:
                            atom_id_2 = ccb[self.__ccU.ccbAtomId2]
                            atom_id_3 = ccb[self.__ccU.ccbAtomId1]
                            break
                    if atom_id_2 is None or atom_id_3 is None:
                        continue
                    atom2 = copy.copy(atom1)
                    atom2['atom_id'] = atom_id_2
                    atom3 = copy.copy(atom4)
                    atom3['atom_id'] = atom_id_3
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.jcoupRestraints} "
                              f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.__entryId, dstFunc,
                                     self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                     atom1, atom2, atom3, atom4)
                        sf['loop'].add_data(row)

        except ValueError:
            if self.__cur_subtype == 'dist':
                self.distRestraints -= 1
            elif self.__cur_subtype == 'jcoup':
                self.jcoupRestraints -= 1
        finally:
            self.numberSelection.clear()

    def validateDistanceRange(self, weight, target_value, lower_limit, upper_limit, target_value_uncertainty, omit_dist_limit_outlier):
        """ Validate distance value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if target_value_uncertainty is not None:
            dstFunc['target_value_uncertainty'] = f"{target_value_uncertainty}"

        if target_value is not None and upper_limit is not None and lower_limit is not None\
           and abs(target_value - lower_limit) <= DIST_AMBIG_UNCERT\
           and abs(target_value - upper_limit) <= DIST_AMBIG_UNCERT:
            if target_value >= DIST_AMBIG_MED:
                lower_limit = None
            elif target_value <= DIST_AMBIG_LOW:
                upper_limit = None

        if target_value is not None:
            if DIST_ERROR_MIN < target_value < DIST_ERROR_MAX or (target_value == 0.0 and target_value_uncertainty is not None and self.__allowZeroUpperLimit):
                dstFunc['target_value'] = f"{target_value:.3f}" if target_value > 0.0 else "0.0"
            else:
                if target_value <= DIST_ERROR_MIN and omit_dist_limit_outlier:
                    if 'upl' in (self.__file_ext, self.__cur_dist_type) or 'lol' in (self.__file_ext, self.__cur_dist_type):
                        dstFunc['target_value'] = f"{target_value:.3f}"
                    else:
                        self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                        f"The target value='{target_value:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                        target_value = None
                else:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The target value='{target_value:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if DIST_ERROR_MIN <= lower_limit < DIST_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.3f}" if lower_limit > 0.0 else "0.0"
            else:
                if lower_limit <= DIST_ERROR_MIN and omit_dist_limit_outlier:
                    if 'lol' in (self.__file_ext, self.__cur_dist_type):
                        dstFunc['lower_limit'] = f"{lower_limit:.3f}"
                    else:
                        self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                        f"The lower limit value='{lower_limit:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                        lower_limit = None
                else:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if DIST_ERROR_MIN < upper_limit <= DIST_ERROR_MAX or (upper_limit == 0.0 and target_value_uncertainty is not None and self.__allowZeroUpperLimit):
                dstFunc['upper_limit'] = f"{upper_limit:.3f}" if upper_limit > 0.0 else "0.0"
            else:
                if (upper_limit <= DIST_ERROR_MIN or upper_limit > DIST_ERROR_MAX) and omit_dist_limit_outlier:
                    if 'upl' in (self.__file_ext, self.__cur_dist_type):
                        dstFunc['upper_limit'] = f"{upper_limit:.3f}"
                    else:
                        self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                        f"The upper limit value='{upper_limit:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                        upper_limit = None
                else:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.3f}' must be less than the target value '{target_value:.3f}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.3f}' must be greater than the target value '{target_value:.3f}'.")

        else:

            if lower_limit is not None and upper_limit is not None:
                if lower_limit > upper_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.3f}' must be less than the upper limit value '{upper_limit:.3f}'.")

        if not validRange:
            return None

        if target_value is not None:
            if DIST_RANGE_MIN <= target_value <= DIST_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value:.3f}' should be within range {DIST_RESTRAINT_RANGE}.")

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

        return dstFunc

    def validatePeakVolumeRange(self, weight, target_value, lower_limit, upper_limit):
        """ Validate NOESY peak volume value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if target_value is not None:
            dstFunc['target_value'] = f"{target_value}"

        if lower_limit is not None:
            dstFunc['lower_limit'] = f"{lower_limit}"

        if upper_limit is not None:
            dstFunc['upper_limit'] = f"{upper_limit}"

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit}' must be greater than the target value '{target_value}'.")

        if not validRange:
            return None

        return dstFunc

    def getRealChainSeqId(self, ps, seqId, compId=None, isPolySeq=True):
        if compId is not None:
            compId = translateToStdResName(compId, self.__ccU)
        # if self.__reasons is not None and 'label_seq_scheme' in self.__reasons and self.__reasons['label_seq_scheme']:
        if not self.__preferAuthSeq:
            seqKey = (ps['chain_id' if isPolySeq else 'auth_chain_id'], seqId)
            if seqKey in self.__labelToAuthSeq:
                _chainId, _seqId = self.__labelToAuthSeq[seqKey]
                if _seqId in ps['auth_seq_id']:
                    return _chainId, _seqId
        if seqId in ps['auth_seq_id']:
            if compId is None:
                return ps['auth_chain_id'], seqId
            idx = ps['auth_seq_id'].index(seqId)
            if compId in (ps['comp_id'][idx], ps['auth_comp_id'][idx]):
                return ps['auth_chain_id'], seqId
        # if seqId in ps['seq_id']:
        #     idx = ps['seq_id'].index(seqId)
        #     if compId is None:
        #         return ps['auth_chain_id'], ps['auth_seq_id'][idx]
        #     if compId in (ps['comp_id'][idx], ps['auth_comp_id'][idx]):
        #         return ps['auth_chain_id'], ps['auth_seq_id'][idx]
        return ps['chain_id' if isPolySeq else 'auth_chain_id'], seqId

    def assignCoordPolymerSequence(self, seqId, compId, atomId):
        """ Assign polymer sequences of the coordinates.
        """

        chainAssign = set()
        _seqId = seqId
        _compId = compId

        fixedChainId = None
        fixedSeqId = None

        preferNonPoly = False

        if self.__mrAtomNameMapping is not None and compId not in monDict3:
            seqId, compId, _ = retrieveAtomIdentFromMRMap(self.__mrAtomNameMapping, seqId, compId, atomId)

        if self.__reasons is not None:
            if 'ambig_atom_id_remap' in self.__reasons and compId in self.__reasons['ambig_atom_id_remap']\
               and atomId in self.__reasons['ambig_atom_id_remap'][compId]:
                return self.atomIdListToChainAssign(self.__reasons['ambig_atom_id_remap'][compId][atomId])
            if 'unambig_atom_id_remap' in self.__reasons and compId in self.__reasons['unambig_atom_id_remap']\
               and atomId in self.__reasons['unambig_atom_id_remap'][compId]:
                atomId = self.__reasons['unambig_atom_id_remap'][compId][atomId][0]  # select representative one
            if 'non_poly_remap' in self.__reasons and compId in self.__reasons['non_poly_remap']\
               and seqId in self.__reasons['non_poly_remap'][compId]:
                fixedChainId, fixedSeqId = retrieveRemappedNonPoly(self.__reasons['non_poly_remap'], None, seqId, compId)
                preferNonPoly = True
            if 'branched_remap' in self.__reasons and seqId in self.__reasons['branched_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['branched_remap'], seqId)
                preferNonPoly = True
            if 'chain_id_remap' in self.__reasons and seqId in self.__reasons['chain_id_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_remap'], seqId)
            elif 'chain_id_clone' in self.__reasons and seqId in self.__reasons['chain_id_clone']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_clone'], seqId)
            elif 'seq_id_remap' in self.__reasons:
                fixedChainId, fixedSeqId = retrieveRemappedSeqId(self.__reasons['seq_id_remap'], None, seqId)
            if fixedSeqId is not None:
                _seqId = fixedSeqId

        if len(self.ambigAtomNameMapping) > 0:
            if compId in self.ambigAtomNameMapping\
               and atomId in self.ambigAtomNameMapping[compId]:
                return self.atomIdListToChainAssign(self.ambigAtomNameMapping[compId][atomId])
        if len(self.unambigAtomNameMapping) > 0:
            if compId in self.unambigAtomNameMapping\
               and atomId in self.unambigAtomNameMapping[compId]:
                atomId = self.unambigAtomNameMapping[compId][atomId][0]  # select representative one

        compId = translateToStdResName(_compId, self.__ccU)
        updatePolySeqRst(self.__polySeqRst, self.__polySeq[0]['chain_id'] if fixedChainId is None else fixedChainId, _seqId, compId, _compId)

        for ps in self.__polySeq:
            if preferNonPoly:
                continue
            chainId, seqId = self.getRealChainSeqId(ps, _seqId, compId)
            if self.__reasons is not None:
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                    if fixedSeqId is not None:
                        seqId = fixedSeqId
                elif fixedSeqId is not None:
                    seqId = fixedSeqId
            if seqId in ps['auth_seq_id']:
                idx = ps['auth_seq_id'].index(seqId)
                cifCompId = ps['comp_id'][idx]
                origCompId = ps['auth_comp_id'][idx]
                if cifCompId != compId:
                    compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                    if compId in compIds:
                        cifCompId = compId
                        origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                          if _seqId == seqId and _compId == compId)
                if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                    _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, self.__hasCoord)
                    atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                if compId in (cifCompId, origCompId):
                    if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.add((chainId, seqId, cifCompId, True))
                elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                    chainAssign.add((chainId, seqId, cifCompId, True))
                    # """ defer to sequence alignment error
                    # if cifCompId != translateToStdResName(compId, self.__ccU):
                    #     self.__f.append(f"[Unmatched residue name] {self.__getCurrentRestraint()}"
                    #                     f"The residue name {_seqId}:{_compId} is unmatched with the name of the coordinates, {cifCompId}.")
                    # """
            elif 'gap_in_auth_seq' in ps:
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
                        idx = ps['auth_seq_id'].index(_seqId_) - (_seqId_ - seqId)
                        try:
                            seqId_ = ps['auth_seq_id'][idx]
                            cifCompId = ps['comp_id'][idx]
                            origCompId = ps['auth_comp_id'][idx]
                            if cifCompId != compId:
                                compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                                if compId in compIds:
                                    cifCompId = compId
                                    origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                                      if _seqId == seqId and _compId == compId)
                            if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                                _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId_, self.__hasCoord)
                                atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                            if compId in (cifCompId, origCompId):
                                if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.add((chainId, seqId_, cifCompId, True))
                                elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.add((chainId, seqId_, cifCompId, True))
                        except IndexError:
                            pass

        if self.__hasNonPolySeq:
            for np in self.__nonPolySeq:
                chainId, seqId = self.getRealChainSeqId(np, _seqId, compId, False)
                if self.__reasons is not None:
                    if fixedChainId is not None:
                        if fixedChainId != chainId:
                            continue
                        if fixedSeqId is not None:
                            seqId = fixedSeqId
                    elif fixedSeqId is not None:
                        seqId = fixedSeqId
                if seqId in np['auth_seq_id']:
                    idx = np['auth_seq_id'].index(seqId)
                    cifCompId = np['comp_id'][idx]
                    origCompId = np['auth_comp_id'][idx]
                    if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                        _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, self.__hasCoord)
                        atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                    if 'alt_auth_seq_id' in np and seqId in np['auth_seq_id'] and seqId not in np['alt_auth_seq_id']:
                        seqId = next(_altSeqId for _seqId, _altSeqId in zip(np['auth_seq_id'], np['alt_auth_seq_id']) if _seqId == seqId)
                    if compId in (cifCompId, origCompId):
                        if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.add((chainId, seqId, cifCompId, False))
                    elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.add((chainId, seqId, cifCompId, False))

        if len(chainAssign) == 0:
            for ps in self.__polySeq:
                if preferNonPoly:
                    continue
                chainId = ps['chain_id']
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__authToLabelSeq:
                    _, seqId = self.__authToLabelSeq[seqKey]
                    if seqId in ps['seq_id']:
                        idx = ps['seq_id'].index(seqId)
                        cifCompId = ps['comp_id'][idx]
                        origCompId = ps['auth_comp_id'][idx]
                        if cifCompId != compId:
                            compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                            if compId in compIds:
                                cifCompId = compId
                                origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                                  if _seqId == seqId and _compId == compId)
                        if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                            _, coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId, self.__hasCoord)
                            atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                        if compId in (cifCompId, origCompId):
                            if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((ps['auth_chain_id'], _seqId, cifCompId, True))
                                # if 'label_seq_scheme' not in self.reasonsForReParsing:
                                #     self.reasonsForReParsing['label_seq_scheme'] = True
                        elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.add((ps['auth_chain_id'], _seqId, cifCompId, True))
                            # """ defer to sequence alignment error
                            # if cifCompId != translateToStdResName(compId, self.__ccU):
                            #     self.__f.append(f"[Unmatched residue name] {self.__getCurrentRestraint()}"
                            #                     f"The residue name {_seqId}:{_compId} is unmatched with the name of the coordinates, {cifCompId}.")
                            # """

            if self.__hasNonPolySeq:
                for np in self.__nonPolySeq:
                    chainId = np['auth_chain_id']
                    if fixedChainId is not None and fixedChainId != chainId:
                        continue
                    seqKey = (chainId, _seqId)
                    if seqKey in self.__authToLabelSeq:
                        _, seqId = self.__authToLabelSeq[seqKey]
                        if seqId in np['seq_id']:
                            idx = np['seq_id'].index(seqId)
                            cifCompId = np['comp_id'][idx]
                            origCompId = np['auth_comp_id'][idx]
                            if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                                _, coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId, self.__hasCoord)
                                atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                            if compId in (cifCompId, origCompId):
                                if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.add((np['auth_chain_id'], _seqId, cifCompId, False))
                                    # if 'label_seq_scheme' not in self.reasonsForReParsing:
                                    #     self.reasonsForReParsing['label_seq_scheme'] = True
                            elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((np['auth_chain_id'], _seqId, cifCompId, False))

        if len(chainAssign) == 0 and self.__altPolySeq is not None:
            for ps in self.__altPolySeq:
                if preferNonPoly:
                    continue
                chainId = ps['auth_chain_id']
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
                if _seqId in ps['auth_seq_id']:
                    cifCompId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                    if cifCompId != compId:
                        compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                        if compId in compIds:
                            cifCompId = compId
                    chainAssign.add((chainId, _seqId, cifCompId, True))
                    # """ defer to sequence alignment error
                    # if cifCompId != translateToStdResName(compId, self.__ccU):
                    #     self.__f.append(f"[Unmatched residue name] {self.__getCurrentRestraint()}"
                    #                     f"The residue name {_seqId}:{_compId} is unmatched with the name of the coordinates, {cifCompId}.")
                    # """

        if len(chainAssign) == 0:
            for ps in self.__polySeq:
                if preferNonPoly:
                    continue
                chainId = ps['chain_id']
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__labelToAuthSeq:
                    _, seqId = self.__labelToAuthSeq[seqKey]
                    if seqId in ps['auth_seq_id']:
                        idx = ps['auth_seq_id'].index(seqId)
                        cifCompId = ps['comp_id'][idx]
                        origCompId = ps['auth_comp_id'][idx]
                        if cifCompId != compId:
                            compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                            if compId in compIds:
                                cifCompId = compId
                                origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                                  if _seqId == seqId and _compId == compId)
                        if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                            _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, self.__hasCoord)
                            atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                        if compId in (cifCompId, origCompId):
                            if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((ps['auth_chain_id'], seqId, cifCompId, True))
                                self.__authSeqId = 'label_seq_id'
                                self.__setLocalSeqScheme()
                                # if 'label_seq_scheme' not in self.reasonsForReParsing:
                                #     self.reasonsForReParsing['label_seq_scheme'] = True
                        elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.add((ps['auth_chain_id'], seqId, cifCompId, True))
                            self.__authSeqId = 'label_seq_id'
                            self.__setLocalSeqScheme()
                            # """ defer to sequence alignment error
                            # if cifCompId != translateToStdResName(compId, self.__ccU):
                            #     self.__f.append(f"[Unmatched residue name] {self.__getCurrentRestraint()}"
                            #                     f"The residue name {_seqId}:{_compId} is unmatched with the name of the coordinates, {cifCompId}.")
                            # """

        if len(chainAssign) == 0:
            if seqId == 1 or (chainId if fixedChainId is None else fixedChainId, seqId - 1) in self.__coordUnobsRes:
                if atomId in aminoProtonCode and atomId != 'H1':
                    return self.assignCoordPolymerSequence(seqId, compId, 'H1')
            if seqId < 1 and len(self.__polySeq) == 1:
                self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                f"{_seqId}:{_compId}:{atomId} is not present in the coordinates. "
                                f"The residue number '{_seqId}' is not present in polymer sequence of chain {self.__polySeq[0]['chain_id']} of the coordinates. "
                                "Please update the sequence in the Macromolecules page.")
            else:
                self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                f"{_seqId}:{_compId}:{atomId} is not present in the coordinates.")

        return list(chainAssign)

    def assignCoordPolymerSequenceWithChainId(self, refChainId, seqId, compId, atomId):
        """ Assign polymer sequences of the coordinates.
        """

        _refChainId = refChainId

        chainAssign = set()
        _seqId = seqId
        _compId = compId

        fixedChainId = None
        fixedSeqId = None

        preferNonPoly = False

        if self.__mrAtomNameMapping is not None and compId not in monDict3:
            seqId, compId, _ = retrieveAtomIdentFromMRMap(self.__mrAtomNameMapping, seqId, compId, atomId)

        if self.__reasons is not None:
            if 'ambig_atom_id_remap' in self.__reasons and compId in self.__reasons['ambig_atom_id_remap']\
               and atomId in self.__reasons['ambig_atom_id_remap'][compId]:
                return self.atomIdListToChainAssign(self.__reasons['ambig_atom_id_remap'][compId][atomId])
            if 'unambig_atom_id_remap' in self.__reasons and compId in self.__reasons['unambig_atom_id_remap']\
               and atomId in self.__reasons['unambig_atom_id_remap'][compId]:
                atomId = self.__reasons['unambig_atom_id_remap'][compId][atomId][0]  # select representative one
            if 'non_poly_remap' in self.__reasons and compId in self.__reasons['non_poly_remap']\
               and seqId in self.__reasons['non_poly_remap'][compId]:
                fixedChainId, fixedSeqId = retrieveRemappedNonPoly(self.__reasons['non_poly_remap'], str(refChainId), seqId, compId)
                refChainId = fixedChainId
                preferNonPoly = True
            if 'branched_remap' in self.__reasons and seqId in self.__reasons['branched_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['branched_remap'], seqId)
                refChainId = fixedChainId
                preferNonPoly = True
            if 'chain_id_remap' in self.__reasons and seqId in self.__reasons['chain_id_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_remap'], seqId)
                refChainId = fixedChainId
            elif 'chain_id_clone' in self.__reasons and seqId in self.__reasons['chain_id_clone']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_clone'], seqId)
                refChainId = fixedChainId
            elif 'seq_id_remap' in self.__reasons:
                _, fixedSeqId = retrieveRemappedSeqId(self.__reasons['seq_id_remap'], str(refChainId), seqId)
            if fixedSeqId is not None:
                _seqId = fixedSeqId

        if len(self.ambigAtomNameMapping) > 0:
            if compId in self.ambigAtomNameMapping and atomId in self.ambigAtomNameMapping[compId]:
                return self.atomIdListToChainAssign(self.ambigAtomNameMapping[compId][atomId])
        if len(self.unambigAtomNameMapping) > 0:
            if compId in self.unambigAtomNameMapping and atomId in self.unambigAtomNameMapping[compId]:
                atomId = self.unambigAtomNameMapping[compId][atomId][0]  # select representative one

        compId = translateToStdResName(_compId, self.__ccU)
        updatePolySeqRst(self.__polySeqRst, str(refChainId), _seqId, compId, _compId)

        if refChainId is not None or refChainId != _refChainId:
            if any(ps for ps in self.__polySeq if ps['auth_chain_id'] == _refChainId):
                fixedChainId = _refChainId
            elif self.__hasNonPolySeq:
                if any(np for np in self.__nonPolySeq if np['auth_chain_id'] == _refChainId):
                    fixedChainId = _refChainId

        for ps in self.__polySeq:
            if preferNonPoly:
                continue
            chainId, seqId = self.getRealChainSeqId(ps, _seqId, compId)
            if fixedChainId is None and refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                if chainId != self.__chainNumberDict[refChainId]:
                    continue
            if self.__reasons is not None:
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                    if fixedSeqId is not None:
                        seqId = fixedSeqId
                elif fixedSeqId is not None:
                    seqId = fixedSeqId
            if seqId in ps['auth_seq_id']:
                idx = ps['auth_seq_id'].index(seqId)
                cifCompId = ps['comp_id'][idx]
                origCompId = ps['auth_comp_id'][idx]
                if cifCompId != compId:
                    compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                    if compId in compIds:
                        cifCompId = compId
                        origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                          if _seqId == seqId and _compId == compId)
                if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                    _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, self.__hasCoord)
                    atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                if compId in (cifCompId, origCompId):
                    if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.add((chainId, seqId, cifCompId, True))
                        if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                            self.__chainNumberDict[refChainId] = chainId
                elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                    chainAssign.add((chainId, seqId, cifCompId, True))
                    if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                        self.__chainNumberDict[refChainId] = chainId
                    # """ defer to sequence alignment error
                    # if cifCompId != translateToStdResName(compId, self.__ccU):
                    #     self.__f.append(f"[Unmatched residue name] {self.__getCurrentRestraint()}"
                    #                     f"The residue name {_seqId}:{_compId} is unmatched with the name of the coordinates, {cifCompId}.")
                    # """
            elif 'gap_in_auth_seq' in ps:
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
                        idx = ps['auth_seq_id'].index(_seqId_) - (_seqId_ - seqId)
                        try:
                            seqId_ = ps['auth_seq_id'][idx]
                            cifCompId = ps['comp_id'][idx]
                            origCompId = ps['auth_comp_id'][idx]
                            if cifCompId != compId:
                                compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                                if compId in compIds:
                                    cifCompId = compId
                                    origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                                      if _seqId == seqId and _compId == compId)
                            if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                                _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId_, self.__hasCoord)
                                atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                            if compId in (cifCompId, origCompId):
                                if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.add((chainId, seqId_, cifCompId, True))
                                elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.add((chainId, seqId_, cifCompId, True))
                        except IndexError:
                            pass

        if self.__hasNonPolySeq:
            for np in self.__nonPolySeq:
                chainId, seqId = self.getRealChainSeqId(np, _seqId, compId, False)
                if fixedChainId is None and refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                    if chainId != self.__chainNumberDict[refChainId]:
                        continue
                if self.__reasons is not None:
                    if fixedChainId is not None:
                        if fixedChainId != chainId:
                            continue
                        if fixedSeqId is not None:
                            seqId = fixedSeqId
                    elif fixedSeqId is not None:
                        seqId = fixedSeqId
                if seqId in np['auth_seq_id']:
                    idx = np['auth_seq_id'].index(seqId)
                    cifCompId = np['comp_id'][idx]
                    origCompId = np['auth_comp_id'][idx]
                    if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                        _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, self.__hasCoord)
                        atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                    if 'alt_auth_seq_id' in np and seqId in np['auth_seq_id'] and seqId not in np['alt_auth_seq_id']:
                        seqId = next(_altSeqId for _seqId, _altSeqId in zip(np['auth_seq_id'], np['alt_auth_seq_id']) if _seqId == seqId)
                    if compId in (cifCompId, origCompId):
                        if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.add((chainId, seqId, cifCompId, False))
                            if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                self.__chainNumberDict[refChainId] = chainId
                    elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.add((chainId, seqId, cifCompId, False))
                        if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                            self.__chainNumberDict[refChainId] = chainId

        if len(chainAssign) == 0:
            for ps in self.__polySeq:
                if preferNonPoly:
                    continue
                chainId = ps['chain_id']
                if refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                    if chainId != self.__chainNumberDict[refChainId]:
                        continue
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__authToLabelSeq:
                    _, seqId = self.__authToLabelSeq[seqKey]
                    if seqId in ps['seq_id']:
                        idx = ps['seq_id'].index(seqId)
                        cifCompId = ps['comp_id'][idx]
                        origCompId = ps['auth_comp_id'][idx]
                        if cifCompId != compId:
                            compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                            if compId in compIds:
                                cifCompId = compId
                                origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                                  if _seqId == seqId and _compId == compId)
                        if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                            _, coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId, self.__hasCoord)
                            atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                        if compId in (cifCompId, origCompId):
                            if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((ps['auth_chain_id'], _seqId, cifCompId, True))
                                if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                    self.__chainNumberDict[refChainId] = chainId
                                # if 'label_seq_scheme' not in self.reasonsForReParsing:
                                #     self.reasonsForReParsing['label_seq_scheme'] = True
                        elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.add((ps['auth_chain_id'], _seqId, cifCompId, True))
                            if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                self.__chainNumberDict[refChainId] = chainId
                            # """ defer to sequence alignment error
                            # if cifCompId != translateToStdResName(compId, self.__ccU):
                            #     self.__f.append(f"[Unmatched residue name] {self.__getCurrentRestraint()}"
                            #             f"The residue name {_seqId}:{_compId} is unmatched with the name of the coordinates, {cifCompId}.")
                            # """

            if self.__hasNonPolySeq:
                for np in self.__nonPolySeq:
                    chainId = np['auth_chain_id']
                    if refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                        if chainId != self.__chainNumberDict[refChainId]:
                            continue
                    if fixedChainId is not None:
                        if fixedChainId != chainId:
                            continue
                    seqKey = (chainId, _seqId)
                    if seqKey in self.__authToLabelSeq:
                        _, seqId = self.__authToLabelSeq[seqKey]
                        if seqId in np['seq_id']:
                            idx = np['seq_id'].index(seqId)
                            cifCompId = np['comp_id'][idx]
                            origCompId = np['auth_comp_id'][idx]
                            if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                                _, coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId, self.__hasCoord)
                                atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                            if compId in (cifCompId, origCompId):
                                if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.add((np['auth_chain_id'], _seqId, cifCompId, False))
                                    if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                        self.__chainNumberDict[refChainId] = chainId
                                    # if 'label_seq_scheme' not in self.reasonsForReParsing:
                                    #     self.reasonsForReParsing['label_seq_scheme'] = True
                            elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((np['auth_chain_id'], _seqId, cifCompId, False))
                                if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                    self.__chainNumberDict[refChainId] = chainId

        if len(chainAssign) == 0 and self.__altPolySeq is not None:
            for ps in self.__altPolySeq:
                if preferNonPoly:
                    continue
                chainId = ps['auth_chain_id']
                if fixedChainId is None and refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                    if chainId != self.__chainNumberDict[refChainId]:
                        continue
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                    if fixedSeqId is not None:
                        _seqId = fixedSeqId
                elif fixedSeqId is not None:
                    _seqId = fixedSeqId
                if _seqId in ps['auth_seq_id']:
                    cifCompId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                    if cifCompId != compId:
                        compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                        if compId in compIds:
                            cifCompId = compId
                    chainAssign.add((chainId, _seqId, cifCompId, True))
                    if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                        self.__chainNumberDict[refChainId] = chainId
                    # """ defer to sequence alignment error
                    # if cifCompId != translateToStdResName(compId, self.__ccU):
                    #     self.__f.append(f"[Unmatched residue name] {self.__getCurrentRestraint()}"
                    #                     f"The residue name {_seqId}:{_compId} is unmatched with the name of the coordinates, {cifCompId}.")
                    # """

        if len(chainAssign) == 0:
            for ps in self.__polySeq:
                if preferNonPoly:
                    continue
                chainId = ps['chain_id']
                if refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                    if chainId != self.__chainNumberDict[refChainId]:
                        continue
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__labelToAuthSeq:
                    _, seqId = self.__labelToAuthSeq[seqKey]
                    if seqId in ps['auth_seq_id']:
                        idx = ps['auth_seq_id'].index(seqId)
                        cifCompId = ps['comp_id'][idx]
                        origCompId = ps['auth_comp_id'][idx]
                        if cifCompId != compId:
                            compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                            if compId in compIds:
                                cifCompId = compId
                                origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                                  if _seqId == seqId and _compId == compId)
                        if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                            _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, self.__hasCoord)
                            atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                        if compId in (cifCompId, origCompId):
                            if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((ps['auth_chain_id'], seqId, cifCompId, True))
                                self.__authSeqId = 'label_seq_id'
                                self.__setLocalSeqScheme()
                                if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                    self.__chainNumberDict[refChainId] = chainId
                                # if 'label_seq_scheme' not in self.reasonsForReParsing:
                                #     self.reasonsForReParsing['label_seq_scheme'] = True
                        elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.add((ps['auth_chain_id'], seqId, cifCompId, True))
                            self.__authSeqId = 'label_seq_id'
                            self.__setLocalSeqScheme()
                            if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                self.__chainNumberDict[refChainId] = chainId
                            # """ defer to sequence alignment error
                            # if cifCompId != translateToStdResName(compId, self.__ccU):
                            #     self.__f.append(f"[Unmatched residue name] {self.__getCurrentRestraint()}"
                            #                     f"The residue name {_seqId}:{_compId} is unmatched with the name of the coordinates, {cifCompId}.")
                            # """

        if len(chainAssign) == 0:
            if seqId == 1 or (refChainId, seqId - 1) in self.__coordUnobsRes:
                if atomId in aminoProtonCode and atomId != 'H1':
                    return self.assignCoordPolymerSequenceWithChainId(refChainId, seqId, compId, 'H1')
            if compId == 'AMB' and (('-' in atomId and ':' in atomId) or '.' in atomId):
                self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                f"{_seqId}:{_compId}:{atomId} is not present in the coordinates. "
                                "Please attach ambiguous atom name mapping information generated by 'makeDIST_RST' to the CYANA restraint file.")
            else:
                if seqId < 1 and len(self.__polySeq) == 1:
                    self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                    f"{_seqId}:{_compId}:{atomId} is not present in the coordinates. "
                                    f"The residue number '{_seqId}' is not present in polymer sequence of chain {refChainId} of the coordinates. "
                                    "Please update the sequence in the Macromolecules page.")
                else:
                    self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                    f"{_seqId}:{_compId}:{atomId} is not present in the coordinates.")

        elif any(ca for ca in chainAssign if ca[0] == refChainId) and any(ca for ca in chainAssign if ca[0] != refChainId):
            _chainAssign = copy.copy(chainAssign)
            for _ca in _chainAssign:
                if _ca[0] != refChainId:
                    chainAssign.remove(_ca)

        return list(chainAssign)

    def assignCoordPolymerSequenceWithoutCompId(self, seqId, atomId=None):
        """ Assign polymer sequences of the coordinates.
        """

        chainAssign = set()
        _seqId = seqId

        fixedChainId = None
        fixedSeqId = None

        if self.__reasons is not None:
            if 'branched_remap' in self.__reasons and seqId in self.__reasons['branched_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['branched_remap'], seqId)
            if 'chain_id_remap' in self.__reasons and seqId in self.__reasons['chain_id_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_remap'], seqId)
            elif 'chain_id_clone' in self.__reasons and seqId in self.__reasons['chain_id_clone']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_clone'], seqId)
            if 'seq_id_remap' not in self.__reasons:
                if fixedSeqId is not None:
                    seqId = _seqId = fixedSeqId

        for ps in self.__polySeq:
            chainId, seqId = self.getRealChainSeqId(ps, _seqId, None)
            if self.__reasons is not None:
                if 'seq_id_remap' not in self.__reasons:
                    if fixedChainId != chainId:
                        continue
                else:
                    _, fixedSeqId = retrieveRemappedSeqId(self.__reasons['seq_id_remap'], chainId, seqId)
                    if fixedSeqId is not None:
                        seqId = _seqId = fixedSeqId
            if seqId in ps['auth_seq_id']:
                idx = ps['auth_seq_id'].index(seqId)
                cifCompId = ps['comp_id'][idx]
                if self.__reasons is not None:
                    if 'non_poly_remap' in self.__reasons and cifCompId in self.__reasons['non_poly_remap']\
                       and seqId in self.__reasons['non_poly_remap'][cifCompId]:
                        fixedChainId, fixedSeqId = retrieveRemappedNonPoly(self.__reasons['non_poly_remap'], chainId, seqId, cifCompId)
                        if fixedSeqId is not None:
                            seqId = _seqId = fixedSeqId
                        if fixedChainId != chainId or seqId not in ps['auth_seq_id']:
                            continue
                updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                if atomId is None or len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                    chainAssign.add((chainId, seqId, cifCompId, True))
            elif 'gap_in_auth_seq' in ps:
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
                        idx = ps['auth_seq_id'].index(_seqId_) - (_seqId_ - seqId)
                        try:
                            seqId_ = ps['auth_seq_id'][idx]
                            cifCompId = ps['comp_id'][idx]
                            updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                            if atomId is None or len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((chainId, seqId_, cifCompId, True))
                        except IndexError:
                            pass

        if self.__hasNonPolySeq:
            for np in self.__nonPolySeq:
                chainId, seqId = self.getRealChainSeqId(np, _seqId, None, False)
                if self.__reasons is not None:
                    if 'seq_id_remap' not in self.__reasons:
                        if fixedChainId != chainId:
                            continue
                    else:
                        _, fixedSeqId = retrieveRemappedSeqId(self.__reasons['seq_id_remap'], chainId, seqId)
                        if fixedSeqId is not None:
                            seqId = _seqId = fixedSeqId
                if seqId in np['auth_seq_id']:
                    idx = np['auth_seq_id'].index(seqId)
                    cifCompId = np['comp_id'][idx]
                    updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                    if atomId is None or len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.add((chainId, seqId, cifCompId, False))

        if len(chainAssign) == 0:
            for ps in self.__polySeq:
                chainId = ps['chain_id']
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__authToLabelSeq:
                    _, seqId = self.__authToLabelSeq[seqKey]
                    if seqId in ps['seq_id']:
                        cifCompId = ps['comp_id'][ps['seq_id'].index(seqId)]
                        updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                        if atomId is None or len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.add((ps['auth_chain_id'], _seqId, cifCompId, True))
                            # if 'label_seq_scheme' not in self.reasonsForReParsing:
                            #     self.reasonsForReParsing['label_seq_scheme'] = True

            if self.__hasNonPolySeq:
                for np in self.__nonPolySeq:
                    chainId = np['auth_chain_id']
                    if fixedChainId is not None:
                        if fixedChainId != chainId:
                            continue
                    seqKey = (chainId, _seqId)
                    if seqKey in self.__authToLabelSeq:
                        _, seqId = self.__authToLabelSeq[seqKey]
                        if seqId in np['seq_id']:
                            cifCompId = np['comp_id'][np['seq_id'].index(seqId)]
                            updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                            if atomId is None or len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((np['auth_chain_id'], _seqId, cifCompId, False))
                                # if 'label_seq_scheme' not in self.reasonsForReParsing:
                                #     self.reasonsForReParsing['label_seq_scheme'] = True

        if len(chainAssign) == 0 and self.__altPolySeq is not None:
            for ps in self.__altPolySeq:
                chainId = ps['auth_chain_id']
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                if _seqId in ps['auth_seq_id']:
                    cifCompId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                    updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                    chainAssign.add((chainId, _seqId, cifCompId, True))

        if len(chainAssign) == 0:
            for ps in self.__polySeq:
                chainId = ps['chain_id']
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__labelToAuthSeq:
                    _, seqId = self.__labelToAuthSeq[seqKey]
                    if seqId in ps['auth_seq_id']:
                        cifCompId = ps['comp_id'][ps['auth_seq_id'].index(seqId)]
                        updatePolySeqRst(self.__polySeqRst, chainId, seqId, cifCompId)
                        if atomId is None or len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.add((ps['auth_chain_id'], seqId, cifCompId, True))
                            self.__authSeqId = 'label_seq_id'
                            self.__setLocalSeqScheme()
                            # if 'label_seq_scheme' not in self.reasonsForReParsing:
                            #     self.reasonsForReParsing['label_seq_scheme'] = True

        if len(chainAssign) == 0:
            if seqId == 1 or (chainId if fixedChainId is None else fixedChainId, seqId - 1) in self.__coordUnobsRes:
                if atomId is not None and atomId in aminoProtonCode and atomId != 'H1':
                    return self.assignCoordPolymerSequenceWithoutCompId(seqId, 'H1')
            if atomId is not None and (('-' in atomId and ':' in atomId) or '.' in atomId):
                self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                f"{_seqId}:{atomId} is not present in the coordinates. "
                                "Please attach ambiguous atom name mapping information generated by 'makeDIST_RST' to the CYANA restraint file.")
            else:
                if seqId < 1 and len(self.__polySeq) == 1:
                    self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                    f"{_seqId}:{atomId} is not present in the coordinates. "
                                    f"The residue number '{_seqId}' is not present in polymer sequence of chain {self.__polySeq[0]['chain_id']} of the coordinates. "
                                    "Please update the sequence in the Macromolecules page.")
                else:
                    self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                    f"{_seqId}:{atomId} is not present in the coordinates.")

        return list(chainAssign)

    def assignCoordPolymerSequenceWithChainIdWithoutCompId(self, fixedChainId, seqId, atomId):
        """ Assign polymer sequences of the coordinates.
        """

        chainAssign = set()
        _seqId = seqId

        fixedSeqId = None

        if self.__reasons is not None:
            if 'branched_remap' in self.__reasons and seqId in self.__reasons['branched_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['branched_remap'], seqId)
            if 'chain_id_remap' in self.__reasons and seqId in self.__reasons['chain_id_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_remap'], seqId)
            elif 'chain_id_clone' in self.__reasons and seqId in self.__reasons['chain_id_clone']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_clone'], seqId)
            if 'seq_id_remap' not in self.__reasons:
                if fixedSeqId is not None:
                    seqId = _seqId = fixedSeqId

        for ps in self.__polySeq:
            chainId, seqId = self.getRealChainSeqId(ps, _seqId, None)
            if chainId != fixedChainId:
                continue
            if self.__reasons is not None:
                if 'seq_id_remap' not in self.__reasons:
                    if fixedChainId != chainId:
                        continue
                else:
                    _, fixedSeqId = retrieveRemappedSeqId(self.__reasons['seq_id_remap'], chainId, seqId)
                    if fixedSeqId is not None:
                        seqId = _seqId = fixedSeqId
            if seqId in ps['auth_seq_id']:
                idx = ps['auth_seq_id'].index(seqId)
                cifCompId = ps['comp_id'][idx]
                if self.__reasons is not None:
                    if 'non_poly_remap' in self.__reasons and cifCompId in self.__reasons['non_poly_remap']\
                       and seqId in self.__reasons['non_poly_remap'][cifCompId]:
                        fixedChainId, fixedSeqId = retrieveRemappedNonPoly(self.__reasons['non_poly_remap'], chainId, seqId, cifCompId)
                        if fixedSeqId is not None:
                            seqId = _seqId = fixedSeqId
                        if fixedChainId != chainId or seqId not in ps['auth_seq_id']:
                            continue
                updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                    chainAssign.add((chainId, seqId, cifCompId, True))
            elif 'gap_in_auth_seq' in ps:
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
                        idx = ps['auth_seq_id'].index(_seqId_) - (_seqId_ - seqId)
                        try:
                            seqId_ = ps['auth_seq_id'][idx]
                            cifCompId = ps['comp_id'][idx]
                            updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                            if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((chainId, seqId_, cifCompId, True))
                        except IndexError:
                            pass

        if self.__hasNonPolySeq:
            for np in self.__nonPolySeq:
                chainId, seqId = self.getRealChainSeqId(np, _seqId, None, False)
                if chainId != fixedChainId:
                    continue
                if self.__reasons is not None:
                    if 'seq_id_remap' not in self.__reasons:
                        if fixedChainId != chainId:
                            continue
                    else:
                        _, fixedSeqId = retrieveRemappedSeqId(self.__reasons['seq_id_remap'], chainId, seqId)
                        if fixedSeqId is not None:
                            seqId = _seqId = fixedSeqId
                if seqId in np['auth_seq_id']:
                    idx = np['auth_seq_id'].index(seqId)
                    cifCompId = np['comp_id'][idx]
                    updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                    if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.add((chainId, seqId, cifCompId, False))

        if len(chainAssign) == 0:
            for ps in self.__polySeq:
                chainId = ps['chain_id']
                if chainId != fixedChainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__authToLabelSeq:
                    _, seqId = self.__authToLabelSeq[seqKey]
                    if seqId in ps['seq_id']:
                        cifCompId = ps['comp_id'][ps['seq_id'].index(seqId)]
                        updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                        if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.add((ps['auth_chain_id'], _seqId, cifCompId, True))
                            # if 'label_seq_scheme' not in self.reasonsForReParsing:
                            #     self.reasonsForReParsing['label_seq_scheme'] = True

            if self.__hasNonPolySeq:
                for np in self.__nonPolySeq:
                    chainId = np['auth_chain_id']
                    if chainId != fixedChainId:
                        continue
                    seqKey = (chainId, _seqId)
                    if seqKey in self.__authToLabelSeq:
                        _, seqId = self.__authToLabelSeq[seqKey]
                        if seqId in np['seq_id']:
                            cifCompId = np['comp_id'][np['seq_id'].index(seqId)]
                            updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                            if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((np['auth_chain_id'], _seqId, cifCompId, False))
                                # if 'label_seq_scheme' not in self.reasonsForReParsing:
                                #     self.reasonsForReParsing['label_seq_scheme'] = True

        if len(chainAssign) == 0 and self.__altPolySeq is not None:
            for ps in self.__altPolySeq:
                chainId = ps['auth_chain_id']
                if chainId != fixedChainId:
                    continue
                if _seqId in ps['auth_seq_id']:
                    cifCompId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                    updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                    chainAssign.add((chainId, _seqId, cifCompId, True))

        if len(chainAssign) == 0:
            for ps in self.__polySeq:
                chainId = ps['chain_id']
                if chainId != fixedChainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__labelToAuthSeq:
                    _, seqId = self.__labelToAuthSeq[seqKey]
                    if seqId in ps['auth_seq_id']:
                        cifCompId = ps['comp_id'][ps['auth_seq_id'].index(seqId)]
                        updatePolySeqRst(self.__polySeqRst, fixedChainId, seqId, cifCompId)
                        if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.add((ps['auth_chain_id'], seqId, cifCompId, True))
                            self.__authSeqId = 'label_seq_id'
                            self.__setLocalSeqScheme()
                            # if 'label_seq_scheme' not in self.reasonsForReParsing:
                            #     self.reasonsForReParsing['label_seq_scheme'] = True

        if len(chainAssign) == 0:
            if seqId == 1 or (fixedChainId, seqId - 1) in self.__coordUnobsRes:
                if atomId in aminoProtonCode and atomId != 'H1':
                    return self.assignCoordPolymerSequenceWithChainIdWithoutCompId(fixedChainId, seqId, 'H1')
            if (('-' in atomId and ':' in atomId) or '.' in atomId):
                self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                f"{fixedChainId}:{_seqId}:{atomId} is not present in the coordinates. "
                                "Please attach ambiguous atom name mapping information generated by 'makeDIST_RST' to the CYANA restraint file.")
            else:
                if seqId < 1 and len(self.__polySeq) == 1:
                    self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                    f"{fixedChainId}:{_seqId}:{atomId} is not present in the coordinates. "
                                    f"The residue number '{_seqId}' is not present in polymer sequence of chain {fixedChainId} of the coordinates. "
                                    "Please update the sequence in the Macromolecules page.")
                else:
                    self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                    f"{fixedChainId}:{_seqId}:{atomId} is not present in the coordinates.")

        return list(chainAssign)

    def selectCoordAtoms(self, chainAssign, seqId, compId, atomId, allowAmbig=True, enableWarning=True, offset=0):
        """ Select atoms of the coordinates.
        """

        atomSelection = []

        authAtomId = atomId

        _compId = compId
        _atomId = atomId

        if compId is not None:

            if self.__mrAtomNameMapping is not None and compId not in monDict3:
                _atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, compId, atomId)

            if self.__reasons is not None:
                if 'ambig_atom_id_remap' in self.__reasons and compId in self.__reasons['ambig_atom_id_remap']\
                   and atomId in self.__reasons['ambig_atom_id_remap'][compId]:
                    atomSelection = self.atomIdListToAtomSelection(self.__reasons['ambig_atom_id_remap'][compId][atomId])
                    for atom in atomSelection:
                        chainId = atom['chain_id']
                        cifSeqId = atom['seq_id']
                        cifCompId = atom['comp_id']
                        cifAtomId = atom['atom_id']
                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, self.__hasCoord)
                        self.testCoordAtomIdConsistency(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, enableWarning)
                    if len(atomSelection) > 0:
                        self.atomSelectionSet.append(atomSelection)
                    return
                if 'unambig_atom_id_remap' in self.__reasons and compId in self.__reasons['unambig_atom_id_remap']\
                   and atomId in self.__reasons['unambig_atom_id_remap'][compId]:
                    atomIds = self.__reasons['unambig_atom_id_remap'][compId][atomId]
                    for chainId, cifSeqId, cifCompId, isPolySeq in chainAssign:
                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, self.__hasCoord)
                        for cifAtomId in atomIds:
                            self.testCoordAtomIdConsistency(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, enableWarning)
                            atomSelection.append({'chain_id': chainId, 'seq_id': cifSeqId, 'comp_id': cifCompId, 'atom_id': cifAtomId})
                    if len(atomSelection) > 0:
                        self.atomSelectionSet.append(atomSelection)
                    return

            if len(self.ambigAtomNameMapping) > 0:
                if compId in self.ambigAtomNameMapping and atomId in self.ambigAtomNameMapping[compId]:
                    atomSelection = self.atomIdListToAtomSelection(self.ambigAtomNameMapping[compId][atomId])
                    for atom in atomSelection:
                        chainId = atom['chain_id']
                        cifSeqId = atom['seq_id']
                        cifCompId = atom['comp_id']
                        cifAtomId = atom['atom_id']
                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, self.__hasCoord)
                        self.testCoordAtomIdConsistency(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, enableWarning)
                    if len(atomSelection) > 0:
                        self.atomSelectionSet.append(atomSelection)
                    return
            if len(self.unambigAtomNameMapping) > 0:
                if compId in self.unambigAtomNameMapping and atomId in self.unambigAtomNameMapping[compId]:
                    atomIds = self.unambigAtomNameMapping[compId][atomId]
                    for chainId, cifSeqId, cifCompId, isPolySeq in chainAssign:
                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, self.__hasCoord)
                        for cifAtomId in atomIds:
                            self.testCoordAtomIdConsistency(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, enableWarning)
                            atomSelection.append({'chain_id': chainId, 'seq_id': cifSeqId, 'comp_id': cifCompId, 'atom_id': cifAtomId})
                    if len(atomSelection) > 0:
                        self.atomSelectionSet.append(atomSelection)
                    return

            compId = translateToStdResName(_compId, self.__ccU)

        for chainId, cifSeqId, cifCompId, isPolySeq in chainAssign:

            if offset != 0:
                cifSeqId += offset
                cifCompId = compId

            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, self.__hasCoord)

            if self.__cur_subtype == 'dist' and _compId is not None and _compId.startswith('MTS') and cifCompId != _compId\
               and _atomId[0] in ('O', 'N') and coordAtomSite is not None:

                if cifCompId == 'CYS' and 'SG' in coordAtomSite['atom_id']:
                    atomId = 'SG'
                elif cifCompId == 'SER' and 'OG' in coordAtomSite['atom_id']:
                    atomId = 'OG'
                elif cifCompId == 'GLU' and 'OE2' in coordAtomSite['atom_id']:
                    atomId = 'OE2'
                elif cifCompId == 'ASP' and 'OD2' in coordAtomSite['atom_id']:
                    atomId = 'OD2'
                elif cifCompId == 'GLN' and 'NE2' in coordAtomSite['atom_id']:
                    atomId = 'NE2'
                elif cifCompId == 'ASN' and 'ND2' in coordAtomSite['atom_id']:
                    atomId = 'ND2'
                elif cifCompId == 'LYS' and 'NZ' in coordAtomSite['atom_id']:
                    atomId = 'NZ'
                elif cifCompId == 'THR' and 'OG1' in coordAtomSite['atom_id']:
                    atomId = 'OG1'

            if self.__mrAtomNameMapping is not None and cifCompId not in monDict3:
                _atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, cifSeqId, cifCompId, atomId, coordAtomSite)
                if atomId != _atomId and coordAtomSite is not None and _atomId in coordAtomSite['atom_id']:
                    atomId = _atomId
                elif self.__reasons is not None and 'branched_remap' in self.__reasons:
                    _seqId = retrieveOriginalSeqIdFromMRMap(self.__reasons['branched_remap'], chainId, cifSeqId)
                    if _seqId != cifSeqId:
                        _, _, atomId = retrieveAtomIdentFromMRMap(self.__mrAtomNameMapping, _seqId, cifCompId, atomId, coordAtomSite)

            _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(cifCompId, atomId, leave_unmatched=True)
            if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(cifCompId, atomId[:-1], leave_unmatched=True)
                if atomId[-1].isdigit() and int(atomId[-1]) <= len(_atomId):
                    _atomId = [_atomId[int(atomId[-1]) - 1]]

            if details is not None:
                _atomId_ = translateToStdAtomName(atomId, compId, ccU=self.__ccU)
                if _atomId_ != atomId:
                    if atomId.startswith('HT') and len(_atomId_) == 2:
                        _atomId_ = 'H'
                    __atomId = self.__nefT.get_valid_star_atom_in_xplor(cifCompId, _atomId_)[0]
                    if coordAtomSite is not None:
                        if any(_atomId_ for _atomId_ in __atomId if _atomId_ in coordAtomSite['atom_id']):
                            _atomId = __atomId
                        elif __atomId[0][0] in protonBeginCode:
                            __bondedTo = self.__ccU.getBondedAtoms(cifCompId, __atomId[0])
                            if len(__bondedTo) > 0 and __bondedTo[0] in coordAtomSite['atom_id']:
                                _atomId = __atomId
                elif coordAtomSite is not None:
                    _atomId = []
            # _atomId = self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]

            if coordAtomSite is not None\
               and not any(_atomId_ for _atomId_ in _atomId if _atomId_ in coordAtomSite['atom_id'])\
               and atomId in coordAtomSite['atom_id']:
                _atomId = [atomId]

            if coordAtomSite is None and not isPolySeq and self.__hasNonPolySeq:
                try:
                    for np in self.__nonPolySeq:
                        if np['auth_chain_id'] == chainId and cifSeqId in np['auth_seq_id']:
                            cifSeqId = np['seq_id'][np['auth_seq_id'].index(cifSeqId)]
                            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, self.__hasCoord)
                            if coordAtomSite is not None:
                                break
                except ValueError:
                    pass

            lenAtomId = len(_atomId)
            if compId != cifCompId and compId in monDict3 and cifCompId in monDict3:
                multiChain = insCode = False
                if len(chainAssign) > 0:
                    chainIds = [ca[0] for ca in chainAssign]
                    multiChain = len(collections.Counter(chainIds).most_common()) > 1
                ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                if ps is not None:
                    compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == cifSeqId]
                    if compId in compIds:
                        insCode = True
                        cifCompId = compId
                if not multiChain and not insCode:
                    if self.__preferAuthSeq:
                        _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, asis=False)
                        if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                            if lenAtomId > 0 and _atomId[0] in _coordAtomSite['atom_id']:
                                # self.__preferAuthSeq = False
                                self.__authSeqId = 'label_seq_id'
                                self.__setLocalSeqScheme()
                                continue
                    self.__f.append(f"[Sequence mismatch] {self.__getCurrentRestraint()}"
                                    f"Residue name {_compId!r} of the restraint does not match with {chainId}:{cifSeqId}:{cifCompId} of the coordinates.")
                    continue

            if compId != cifCompId and compId in monDict3 and not isPolySeq:
                continue

            if lenAtomId == 0:
                if compId != cifCompId and any(item for item in chainAssign if item[2] == compId):
                    continue
                if seqId == 1 and isPolySeq and cifCompId == 'ACE' and cifCompId != compId and offset == 0:
                    self.selectCoordAtoms(chainAssign, seqId, compId, atomId, allowAmbig, enableWarning, offset=1)
                    return
                if enableWarning:
                    self.__f.append(f"[Invalid atom nomenclature] {self.__getCurrentRestraint()}"
                                    f"{seqId}:{_compId}:{atomId} is invalid atom nomenclature.")
                continue
            if lenAtomId > 1 and not allowAmbig:
                if enableWarning:
                    self.__f.append(f"[Invalid atom selection] {self.__getCurrentRestraint()}"
                                    f"Ambiguous atom selection '{seqId}:{_compId}:{atomId}' is not allowed as a angle restraint.")
                continue

            for cifAtomId in _atomId:

                if seqKey in self.__coordUnobsRes and cifCompId in monDict3 and self.__reasons is not None and 'non_poly_remap' in self.__reasons:
                    if self.__ccU.updateChemCompDict(cifCompId):
                        try:
                            next(cca for cca in self.__ccU.lastAtomList
                                 if cca[self.__ccU.ccaAtomId] == cifAtomId and cca[self.__ccU.ccaLeavingAtomFlag] != 'Y')
                        except StopIteration:
                            continue
                        try:
                            if len(authAtomId) > len(cifAtomId):
                                next(cca for cca in self.__ccU.lastAtomList
                                     if cca[self.__ccU.ccaAtomId] == authAtomId and cca[self.__ccU.ccaLeavingAtomFlag] != 'Y')
                        except StopIteration:
                            break

                atomSelection.append({'chain_id': chainId, 'seq_id': cifSeqId, 'comp_id': cifCompId,
                                      'atom_id': cifAtomId, 'auth_atom_id': authAtomId})

                self.testCoordAtomIdConsistency(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, enableWarning)

        if len(atomSelection) > 0:
            self.atomSelectionSet.append(atomSelection)

    def testCoordAtomIdConsistency(self, chainId, seqId, compId, atomId, seqKey, coordAtomSite, enableWarning=True):
        if not self.__hasCoord:
            return

        found = False

        if coordAtomSite is not None:
            if atomId in coordAtomSite['atom_id']:
                found = True
            elif 'alt_atom_id' in coordAtomSite and atomId in coordAtomSite['alt_atom_id']:
                found = True
                self.__authAtomId = 'auth_atom_id'

            elif self.__preferAuthSeq:
                _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, asis=False)
                if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                    if atomId in _coordAtomSite['atom_id']:
                        found = True
                        self.__preferAuthSeq = False
                        self.__authSeqId = 'label_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                        found = True
                        self.__preferAuthSeq = False
                        self.__authSeqId = 'label_seq_id'
                        self.__authAtomId = 'auth_atom_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()

            else:
                self.__preferAuthSeq = True
                _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId)
                if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                    if atomId in _coordAtomSite['atom_id']:
                        found = True
                        self.__authSeqId = 'auth_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                        found = True
                        self.__authSeqId = 'auth_seq_id'
                        self.__authAtomId = 'auth_atom_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    else:
                        self.__preferAuthSeq = False
                else:
                    self.__preferAuthSeq = False

        elif self.__preferAuthSeq:
            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, asis=False)
            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                if atomId in _coordAtomSite['atom_id']:
                    found = True
                    self.__preferAuthSeq = False
                    self.__authSeqId = 'label_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    self.__preferAuthSeq = False
                    self.__authSeqId = 'label_seq_id'
                    self.__authAtomId = 'auth_atom_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()

        else:
            self.__preferAuthSeq = True
            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId)
            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                if atomId in _coordAtomSite['atom_id']:
                    found = True
                    self.__authSeqId = 'auth_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    self.__authSeqId = 'auth_seq_id'
                    self.__authAtomId = 'auth_atom_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                else:
                    self.__preferAuthSeq = False
            else:
                self.__preferAuthSeq = False

        if found:
            return

        if self.__preferAuthSeq:
            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, asis=False)
            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                if atomId in _coordAtomSite['atom_id']:
                    found = True
                    self.__preferAuthSeq = False
                    self.__authSeqId = 'label_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    self.__preferAuthSeq = False
                    self.__authSeqId = 'label_seq_id'
                    self.__authAtomId = 'auth_atom_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()

        else:
            self.__preferAuthSeq = True
            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId)
            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                if atomId in _coordAtomSite['atom_id']:
                    found = True
                    self.__authSeqId = 'auth_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    self.__authSeqId = 'auth_seq_id'
                    self.__authAtomId = 'auth_atom_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                else:
                    self.__preferAuthSeq = False
            else:
                self.__preferAuthSeq = False

        if found:
            return

        if self.__ccU.updateChemCompDict(compId):
            cca = next((cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == atomId), None)
            if cca is not None and seqKey not in self.__coordUnobsRes and self.__ccU.lastChemCompDict['_chem_comp.pdbx_release_status'] == 'REL':
                checked = False
                ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId), None)
                if seqId == 1 or (chainId, seqId - 1) in self.__coordUnobsRes or (ps is not None and ps['auth_seq_id'][0] == seqId):
                    if atomId in aminoProtonCode and atomId != 'H1':
                        self.testCoordAtomIdConsistency(chainId, seqId, compId, 'H1', seqKey, coordAtomSite)
                        return
                    if atomId in aminoProtonCode or atomId == 'P' or atomId.startswith('HOP'):
                        checked = True
                if not checked:
                    if atomId[0] in protonBeginCode:
                        bondedTo = self.__ccU.getBondedAtoms(compId, atomId)
                        if len(bondedTo) > 0:
                            if coordAtomSite is not None and bondedTo[0] in coordAtomSite['atom_id'] and cca[self.__ccU.ccaLeavingAtomFlag] != 'Y':
                                self.__f.append(f"[Hydrogen not instantiated] {self.__getCurrentRestraint()}"
                                                f"{chainId}:{seqId}:{compId}:{atomId} is not properly instantiated in the coordinates. "
                                                "Please re-upload the model file.")
                                return
                    if enableWarning:
                        if chainId in LARGE_ASYM_ID:
                            self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                            f"{chainId}:{seqId}:{compId}:{atomId} is not present in the coordinates.")

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
                self.__lfh.write(f"+CyanaMRParserListener.selectRealisticBondConstraint() ++ Error  - {str(e)}")

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
                self.__lfh.write(f"+CyanaMRParserListener.selectRealisticChi2AngleConstraint() ++ Error  - {str(e)}")

        return dst_func

    def getCoordAtomSiteOf(self, chainId, seqId, cifCheck=True, asis=True):
        seqKey = (chainId, seqId)
        coordAtomSite = None
        if cifCheck:
            preferAuthSeq = self.__preferAuthSeq if asis else not self.__preferAuthSeq
            if preferAuthSeq:
                if seqKey in self.__coordAtomSite:
                    coordAtomSite = self.__coordAtomSite[seqKey]
            else:
                if seqKey in self.__labelToAuthSeq:
                    seqKey = self.__labelToAuthSeq[seqKey]
                    if seqKey in self.__coordAtomSite:
                        coordAtomSite = self.__coordAtomSite[seqKey]
        return seqKey, coordAtomSite

    # Enter a parse tree produced by CyanaMRParser#torsion_angle_restraints.
    def enterTorsion_angle_restraints(self, ctx: CyanaMRParser.Torsion_angle_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dihed'
        self.__cur_dist_type = ''

        self.__cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#torsion_angle_restraints.
    def exitTorsion_angle_restraints(self, ctx: CyanaMRParser.Torsion_angle_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#torsion_angle_restraint.
    def enterTorsion_angle_restraint(self, ctx: CyanaMRParser.Torsion_angle_restraintContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#torsion_angle_restraint.
    def exitTorsion_angle_restraint(self, ctx: CyanaMRParser.Torsion_angle_restraintContext):  # pylint: disable=unused-argument

        try:

            _compId = str(ctx.Simple_name(0)).upper()
            compId = translateToStdResName(_compId, self.__ccU)
            if self.__cur_subtype_altered:  # invoked from exitCco_restraint()
                seqId = int(str(ctx.Integer()))
                chainId = str(ctx.Simple_name(1)).upper()
                angleName = str(ctx.Simple_name(2)).upper()
            else:
                seqId = int(str(ctx.Integer(0)))
                angleName = str(ctx.Simple_name(1)).upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            target_value = None
            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]

            if self.__remediate and self.__reasons is not None and 'dihed_unusual_order' in self.__reasons:
                target_value, deviation = lower_limit, upper_limit
                if deviation > 0.0:
                    lower_limit = target_value - deviation
                    upper_limit = target_value + deviation
                else:
                    lower_limit = upper_limit = None

            weight = 1.0
            if len(self.numberSelection) > 2:
                weight = self.numberSelection[2]

            if weight < 0.0:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The relative weight value of '{weight}' should be a positive value.")
            """
            if lower_limit > upper_limit:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The angle's lower limit '{lower_limit}' must be less than or equal to the upper limit '{upper_limit}'.")
                if self.__remediate:
                    self.__dihed_lb_greater_than_ub = True
                return
            """
            if self.__remediate and upper_limit < 0.0:
                self.__dihed_ub_always_positive = False

            # target_value = (upper_limit + lower_limit) / 2.0

            dstFunc = self.validateAngleRange(weight, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            # support AMBER's dihedral angle naming convention for nucleic acids
            # http://ambermd.org/tutorials/advanced/tutorial4/
            if angleName in ('EPSILN', 'EPSLN'):
                angleName = 'EPSILON'

            # nucleic CHI angle
            if angleName == 'CHIN':
                angleName = 'CHI'

            if angleName not in KNOWN_ANGLE_NAMES:
                lenAngleName = len(angleName)
                try:
                    # For the case 'EPSIL' could be standard name 'EPSILON'
                    angleName = next(name for name in KNOWN_ANGLE_NAMES if len(name) >= lenAngleName and name[:lenAngleName] == angleName)
                except StopIteration:
                    self.__f.append(f"[Insufficient angle selection] {self.__getCurrentRestraint()}"
                                    f"The angle identifier {str(ctx.Simple_name(1))!r} is unknown for the residue {_compId!r}, "
                                    "of which CYANA residue library should be uploaded.")
                    return

            peptide, nucleotide, carbohydrate = self.__csStat.getTypeOfCompId(compId)

            if carbohydrate:
                chainAssign = self.assignCoordPolymerSequence(seqId, compId, 'CA')
                if len(chainAssign) > 0:
                    ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainAssign[0][0]), None)
                    if ps is not None and 'type' in ps and 'polypeptide' in ps['type']:
                        peptide = True
                        nucleotide = carbohydrate = False

            if carbohydrate and angleName in KNOWN_ANGLE_CARBO_ATOM_NAMES:
                atomNames = KNOWN_ANGLE_CARBO_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_CARBO_SEQ_OFFSET[angleName]
            else:
                atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

            if angleName != 'PPA':

                if isinstance(atomNames, list):
                    atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)
                else:  # nucleic CHI angle
                    atomId = next(name for name, offset in zip(atomNames['Y'], seqOffset['Y']) if offset == 0)

                if not isinstance(atomId, str):
                    self.__ccU.updateChemCompDict(compId)
                    atomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if atomId.match(cca[self.__ccU.ccaAtomId])), None)
                    if atomId is None and carbohydrate:
                        atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                        if isinstance(atomNames, list):
                            atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)
                        else:  # nucleic CHI angle
                            atomId = next(name for name, offset in zip(atomNames['Y'], seqOffset['Y']) if offset == 0)

                        if not isinstance(atomId, str):
                            atomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if atomId.match(cca[self.__ccU.ccaAtomId])), None)
                            if atomId is None:
                                self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                                f"{seqId}:{_compId} is not present in the coordinates.")
                                return

                self.__retrieveLocalSeqScheme()

                if self.__cur_subtype_altered:  # invoked from exitCco_restraint()
                    chainAssign = self.assignCoordPolymerSequenceWithChainId(chainId, seqId, compId, atomId)
                else:
                    chainAssign = self.assignCoordPolymerSequence(seqId, compId, atomId)

                if len(chainAssign) == 0:
                    self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                    f"{seqId}:{_compId} is not present in the coordinates.")
                    return

                for chainId, cifSeqId, cifCompId, _ in chainAssign:
                    if carbohydrate:
                        if self.__branched is not None:
                            ps = next((ps for ps in self.__branched if ps['auth_chain_id'] == chainId), None)
                        if ps is None:
                            ps = next(ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId)
                    else:
                        ps = next(ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId)

                    peptide, nucleotide, carbohydrate = self.__csStat.getTypeOfCompId(cifCompId)

                    if peptide and angleName in ('PHI', 'PSI', 'OMEGA',
                                                 'CHI1', 'CHI2', 'CHI3', 'CHI4', 'CHI5',
                                                 'CHI21', 'CHI22', 'CHI31', 'CHI32', 'CHI42'):
                        pass
                    elif nucleotide and angleName in ('ALPHA', 'BETA', 'GAMMA', 'DELTA', 'EPSILON', 'ZETA',
                                                      'CHI', 'ETA', 'THETA', "ETA'", "THETA'",
                                                      'NU0', 'NU1', 'NU2', 'NU3', 'NU4',
                                                      'TAU0', 'TAU1', 'TAU2', 'TAU3', 'TAU4'):
                        pass
                    elif carbohydrate and angleName in ('PHI', 'PSI', 'OMEGA'):
                        pass
                    else:
                        self.__f.append(f"[Insufficient angle selection] {self.__getCurrentRestraint()}"
                                        f"The angle identifier {str(ctx.Simple_name(1))!r} is unknown for the residue {_compId!r}, "
                                        "of which CYANA residue library should be uploaded.")
                        return

                    atomNames = None
                    seqOffset = None

                    if carbohydrate:
                        atomNames = KNOWN_ANGLE_CARBO_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_CARBO_SEQ_OFFSET[angleName]
                    elif nucleotide and angleName == 'CHI':
                        if self.__ccU.updateChemCompDict(cifCompId):
                            try:
                                next(cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == 'N9')
                                atomNames = KNOWN_ANGLE_ATOM_NAMES['CHI']['R']
                                seqOffset = KNOWN_ANGLE_SEQ_OFFSET['CHI']['R']
                            except StopIteration:
                                atomNames = KNOWN_ANGLE_ATOM_NAMES['CHI']['Y']
                                seqOffset = KNOWN_ANGLE_SEQ_OFFSET['CHI']['Y']
                    else:
                        atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                    prevCifAtomId = None
                    prevOffset = None

                    for atomId, offset in zip(atomNames, seqOffset):

                        atomSelection = []

                        _cifSeqId = cifSeqId + offset
                        _cifCompId = cifCompId if offset == 0 else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)] if _cifSeqId in ps['auth_seq_id'] else None)

                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, _cifSeqId, self.__hasCoord)

                        if _cifCompId is None:
                            # """
                            # try:
                            #     _cifCompId = ps['comp_id'][ps['auth_seq_id'].index(cifSeqId) + offset]
                            # except IndexError:
                            #     pass
                            # """
                            if _cifCompId is None:
                                self.__f.append(f"[Sequence mismatch warning] {self.__getCurrentRestraint()}"
                                                f"The residue number '{seqId+offset}' is not present in polymer sequence of chain {chainId} of the coordinates. "
                                                "Please update the sequence in the Macromolecules page.")
                                return
                                # _cifCompId = '.'
                            cifAtomId = atomId

                        else:
                            self.__ccU.updateChemCompDict(_cifCompId)

                            if isinstance(atomId, str):
                                cifAtomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == atomId), None)
                            else:
                                cifAtomIds = [cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList
                                              if atomId.match(cca[self.__ccU.ccaAtomId])
                                              and (coordAtomSite is None
                                                   or (coordAtomSite is not None and cca[self.__ccU.ccaAtomId] in coordAtomSite['atom_id']))]

                                if len(cifAtomIds) > 0:
                                    if prevCifAtomId is not None and offset == prevOffset:
                                        cifAtomId = next((_cifAtomId for _cifAtomId in cifAtomIds
                                                          if any(b for b in self.__ccU.lastBonds
                                                                 if ((b[self.__ccU.ccbAtomId1] == prevCifAtomId and b[self.__ccU.ccbAtomId2] == _cifAtomId)
                                                                     or (b[self.__ccU.ccbAtomId1] == _cifAtomId and b[self.__ccU.ccbAtomId2] == prevCifAtomId)))), None)
                                        if cifAtomId is None:
                                            offset -= 1
                                            _cifSeqId = cifSeqId + offset
                                            _cifCompId = cifCompId if offset == 0\
                                                else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)] if _cifSeqId in ps['auth_seq_id'] else None)
                                            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, _cifSeqId, self.__hasCoord)
                                            if coordAtomSite is not None:
                                                cifAtomId = next((_cifAtomId for _cifAtomId in cifAtomIds if _cifAtomId in coordAtomSite['atom_id']), None)

                                    else:
                                        cifAtomId = cifAtomIds[0]
                                else:
                                    cifAtomId = None

                            if cifAtomId is None:
                                self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                                f"{seqId+offset}:{_compId}:{atomId} involved in the {angleName} dihedral angle is not present in the coordinates.")
                                return

                        prevCifAtomId = cifAtomId
                        prevOffset = offset

                        atomSelection.append({'chain_id': chainId, 'seq_id': _cifSeqId, 'comp_id': _cifCompId, 'atom_id': cifAtomId})

                        self.testCoordAtomIdConsistency(chainId, _cifSeqId, _cifCompId, cifAtomId, seqKey, coordAtomSite, True)

                        if self.__hasCoord and coordAtomSite is None:
                            return

                        if len(atomSelection) > 0:
                            self.atomSelectionSet.append(atomSelection)

                    if len(self.atomSelectionSet) < 4:
                        return

                    if not self.areUniqueCoordAtoms('a Torsion angle'):
                        return

                    if self.__createSfDict:
                        sf = self.__getSf(potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                        sf['id'] += 1

                    for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                        self.atomSelectionSet[1],
                                                                        self.atomSelectionSet[2],
                                                                        self.atomSelectionSet[3]):
                        if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.__polySeq if self.__gapInAuthSeq else None):
                            continue
                        if peptide and angleName == 'CHI2' and atom4['atom_id'] == 'CD1' and isLikePheOrTyr(atom2['comp_id'], self.__ccU):
                            dstFunc = self.selectRealisticChi2AngleConstraint(atom1, atom2, atom3, atom4,
                                                                              dstFunc)
                        if self.__debug:
                            print(f"subtype={self.__cur_subtype} id={self.dihedRestraints} angleName={angleName} "
                                  f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                        if self.__createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                         '.', None, angleName,
                                         sf['list_id'], self.__entryId, dstFunc,
                                         self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                         atom1, atom2, atom3, atom4)
                            sf['loop'].add_data(row)

            # phase angle of pseudorotation
            else:

                atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)

                if not isinstance(atomId, str):
                    self.__ccU.updateChemCompDict(compId)
                    atomId = next(cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if atomId.match(cca[self.__ccU.ccaAtomId]))

                self.__retrieveLocalSeqScheme()

                chainAssign = self.assignCoordPolymerSequence(seqId, compId, atomId)

                if len(chainAssign) == 0:
                    self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                    f"{seqId}:{_compId} is not present in the coordinates.")
                    return

                for chainId, cifSeqId, cifCompId, _ in chainAssign:
                    ps = next(ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId)

                    peptide, nucleotide, carbohydrate = self.__csStat.getTypeOfCompId(cifCompId)

                    atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                    seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                    if nucleotide:
                        pass
                    else:
                        self.__f.append(f"[Insufficient angle selection] {self.__getCurrentRestraint()}"
                                        f"The angle identifier {str(ctx.Simple_name(1))!r} did not match with residue {_compId!r}.")
                        return

                    for atomId, offset in zip(atomNames, seqOffset):

                        atomSelection = []

                        _cifSeqId = cifSeqId + offset
                        _cifCompId = cifCompId if offset == 0 else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)] if _cifSeqId in ps['auth_seq_id'] else None)

                        if _cifCompId is None:
                            try:
                                _cifCompId = ps['comp_id'][ps['auth_seq_id'].index(cifSeqId) + offset]
                            except IndexError:
                                pass
                            if _cifCompId is None:
                                self.__f.append(f"[Sequence mismatch warning] {self.__getCurrentRestraint()}"
                                                f"The residue number '{seqId+offset}' is not present in polymer sequence of chain {chainId} of the coordinates. "
                                                "Please update the sequence in the Macromolecules page.")
                                return
                                # _cifCompId = '.'
                            cifAtomId = atomId

                        else:
                            self.__ccU.updateChemCompDict(_cifCompId)

                            cifAtomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == atomId), None)

                            if cifAtomId is None:
                                self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                                f"{seqId+offset}:{_compId}:{atomId} involved in the {angleName} dihedral angle is not present in the coordinates.")
                                return

                        atomSelection.append({'chain_id': chainId, 'seq_id': _cifSeqId, 'comp_id': _cifCompId, 'atom_id': cifAtomId})

                        if len(atomSelection) > 0:
                            self.atomSelectionSet.append(atomSelection)

                    if len(self.atomSelectionSet) < 5:
                        return

                    if not self.areUniqueCoordAtoms('a Torsion angle'):
                        return

                    if self.__createSfDict:
                        sf = self.__getSf(potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                        sf['id'] += 1

                    for atom1, atom2, atom3, atom4, atom5 in itertools.product(self.atomSelectionSet[0],
                                                                               self.atomSelectionSet[1],
                                                                               self.atomSelectionSet[2],
                                                                               self.atomSelectionSet[3],
                                                                               self.atomSelectionSet[4]):
                        if isLongRangeRestraint([atom1, atom2, atom3, atom4, atom5], self.__polySeq if self.__gapInAuthSeq else None):
                            continue
                        if self.__debug:
                            print(f"subtype={self.__cur_subtype} id={self.dihedRestraints} angleName={angleName} "
                                  f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} atom5={atom5} {dstFunc}")
                        if self.__createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                         '.', None, angleName,
                                         sf['list_id'], self.__entryId, dstFunc,
                                         self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                         None, None, None, None, atom5)
                            sf['loop'].add_data(row)

        except ValueError:
            self.dihedRestraints -= 1
        finally:
            self.numberSelection.clear()

    def validateAngleRange(self, weight, target_value, lower_limit, upper_limit):
        """ Validate angle value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if self.__correctCircularShift:
            _array = numpy.array([target_value, lower_limit, upper_limit],
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

        if target_value is not None:
            if ANGLE_ERROR_MIN < target_value < ANGLE_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value:.3f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if ANGLE_ERROR_MIN <= lower_limit < ANGLE_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if ANGLE_ERROR_MIN < upper_limit <= ANGLE_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if not validRange:
            return None

        if target_value is not None:
            if ANGLE_RANGE_MIN <= target_value <= ANGLE_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if ANGLE_RANGE_MIN <= lower_limit <= ANGLE_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if ANGLE_RANGE_MIN <= upper_limit <= ANGLE_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        return dstFunc

    # Enter a parse tree produced by CyanaMRParser#rdc_restraints.
    def enterRdc_restraints(self, ctx: CyanaMRParser.Rdc_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'rdc'
        self.__cur_dist_type = ''

        self.__cur_subtype_altered = False
        self.__cur_comment_inlined = True

        self.rdcParameterDict = {}

    # Exit a parse tree produced by CyanaMRParser#rdc_restraints.
    def exitRdc_restraints(self, ctx: CyanaMRParser.Rdc_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#rdc_parameter.
    def enterRdc_parameter(self, ctx: CyanaMRParser.Rdc_parameterContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#rdc_parameter.
    def exitRdc_parameter(self, ctx: CyanaMRParser.Rdc_parameterContext):
        orientation = self.__cur_rdc_orientation = int(str(ctx.Integer(0)))
        magnitude = self.numberSelection[0]
        rhombicity = self.numberSelection[1]
        orientationCenterSeqId = int(str(ctx.Integer(1)))

        self.rdcParameterDict[orientation] = {'magnitude': magnitude,
                                              'rhombicity': rhombicity,
                                              'orientation_center_seq_id': orientationCenterSeqId}

        if self.__debug:
            print(f"subtype={self.__cur_subtype} orientation={orientation} "
                  f"parameters={self.rdcParameterDict[orientation]}")

        self.numberSelection.clear()

        if self.__createSfDict:
            self.__addSf(constraintType='RDC', orientationId=orientation, cyanaParameter=self.rdcParameterDict[orientation])

    # Enter a parse tree produced by CyanaMRParser#rdc_restraint.
    def enterRdc_restraint(self, ctx: CyanaMRParser.Rdc_restraintContext):  # pylint: disable=unused-argument
        self.rdcRestraints += 1

        self.atomSelectionSet.clear()

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Exit a parse tree produced by CyanaMRParser#rdc_restraint.
    def exitRdc_restraint(self, ctx: CyanaMRParser.Rdc_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()
            seqId2 = int(str(ctx.Integer(1)))
            compId2 = str(ctx.Simple_name(2)).upper()
            atomId2 = str(ctx.Simple_name(3)).upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.rdcRestraints -= 1
                return

            target = self.numberSelection[0]
            error = abs(self.numberSelection[1])
            weight = self.numberSelection[2]
            orientation = int(str(ctx.Integer(2)))
            # if len(self.numberSelection) > 3:
            #     scale = self.numberSelection[3]

            if weight < 0.0:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The relative weight value of '{weight}' should be a positive value.")

            if orientation not in self.rdcParameterDict:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The orientation '{orientation}' must be defined before you start to describe RDC restraints.")
                return

            if seqId1 == self.rdcParameterDict[orientation]['orientation_center_seq_id']:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The residue number '{seqId1}' must not be the same as the center of orientation.")
                return

            if seqId2 == self.rdcParameterDict[orientation]['orientation_center_seq_id']:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The residue number '{seqId2}' must not be the same as the center of orientation.")
                return

            target_value = target
            lower_limit = target - error
            upper_limit = target + error

            dstFunc = self.validateRdcRange(weight, orientation, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

            if len(self.atomSelectionSet) < 2:
                return
            """
            if not self.areUniqueCoordAtoms('an RDC'):
                return
            """
            try:
                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']
            except IndexError:
                self.areUniqueCoordAtoms('an RDC')
                return

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Non-magnetic susceptible spin appears in RDC vector; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if chain_id_1 != chain_id_2:
                ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Found inter-chain RDC vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) > 1:
                ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']), None)
                if ps1 is None:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Found inter-residue RDC vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) == 1:

                if self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                        ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                         or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')
                         or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 == 'H')
                         or (seq_id_1 > seq_id_2 and atom_id_1 == 'H' and atom_id_2.startswith('HA'))):
                    pass

                else:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Found inter-residue RDC vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif atom_id_1 == atom_id_2:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Found zero RDC vector; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            elif self.__ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                if not self.__ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                    if self.__nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.__nefT.validate_comp_atom(comp_id_2, atom_id_2):
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found an RDC vector over multiple covalent bonds; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

            combinationId = '.'
            if self.__createSfDict:
                sf = self.__getSf(potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc),
                                  rdcCode=getRdcCode([self.atomSelectionSet[0][0], self.atomSelectionSet[1][0]]),
                                  orientationId=orientation)
                sf['id'] += 1
                if len(self.atomSelectionSet[0]) > 1 or len(self.atomSelectionSet[1]) > 1:
                    combinationId = 0

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if isIdenticalRestraint([atom1, atom2]):
                    continue
                if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None):
                    continue
                if isinstance(combinationId, int):
                    combinationId += 1
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} id={self.rdcRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 combinationId, None, None,
                                 sf['list_id'], self.__entryId, dstFunc,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom1, atom2)
                    sf['loop'].add_data(row)

        except ValueError:
            self.rdcRestraints -= 1
        finally:
            self.numberSelection.clear()

    def validateRdcRange(self, weight, orientation, target_value, lower_limit, upper_limit):
        """ Validate RDC value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if orientation is not None:
            dstFunc['orientation'] = orientation

        if target_value is not None:
            if RDC_ERROR_MIN < target_value < RDC_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value}' must be within range {RDC_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if RDC_ERROR_MIN <= lower_limit < RDC_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if RDC_ERROR_MIN < upper_limit <= RDC_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

        if not validRange:
            return None

        if target_value is not None:
            if RDC_RANGE_MIN <= target_value <= RDC_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value}' should be within range {RDC_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if RDC_RANGE_MIN <= lower_limit <= RDC_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit:.6f}' should be within range {RDC_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if RDC_RANGE_MIN <= upper_limit <= RDC_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit:.6f}' should be within range {RDC_RESTRAINT_RANGE}.")

        return dstFunc

    def areUniqueCoordAtoms(self, subtype_name):
        """ Check whether atom selection sets are uniquely assigned.
        """

        for _atomSelectionSet in self.atomSelectionSet:

            if len(_atomSelectionSet) < 2:
                continue

            for (atom1, atom2) in itertools.combinations(_atomSelectionSet, 2):
                if atom1['chain_id'] != atom2['chain_id']:
                    continue
                if atom1['seq_id'] != atom2['seq_id']:
                    continue
                self.__f.append(f"[Invalid atom selection] {self.__getCurrentRestraint()}"
                                f"Ambiguous atom selection '{atom1['chain_id']}:{atom1['seq_id']}:{atom1['comp_id']}:{atom1['atom_id']} or "
                                f"{atom2['atom_id']}' is not allowed as {subtype_name} restraint.")
                return False

        return True

    # Enter a parse tree produced by CyanaMRParser#pcs_restraints.
    def enterPcs_restraints(self, ctx: CyanaMRParser.Pcs_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'pcs'
        self.__cur_dist_type = ''

        self.__cur_subtype_altered = False
        self.__cur_comment_inlined = True

        self.pcsParameterDict = {}

    # Exit a parse tree produced by CyanaMRParser#pcs_restraints.
    def exitPcs_restraints(self, ctx: CyanaMRParser.Pcs_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#pcs_parameter.
    def enterPcs_parameter(self, ctx: CyanaMRParser.Pcs_parameterContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#pcs_parameter.
    def exitPcs_parameter(self, ctx: CyanaMRParser.Pcs_parameterContext):
        orientation = int(str(ctx.Integer(0)))
        magnitude = self.numberSelection[0]
        rhombicity = self.numberSelection[1]
        orientationCenterSeqId = int(str(ctx.Integer(1)))

        self.pcsParameterDict[orientation] = {'magnitude': magnitude,
                                              'rhombicity': rhombicity,
                                              'orientation_center_seq_id': orientationCenterSeqId}

        if self.__debug:
            print(f"subtype={self.__cur_subtype} orientation={orientation} "
                  f"parameters={self.pcsParameterDict[orientation]}")

        self.numberSelection.clear()

        if self.__createSfDict:
            self.__addSf(orientationId=orientation, cyanaParameter=self.pcsParameterDict[orientation])

    # Enter a parse tree produced by CyanaMRParser#pcs_restraint.
    def enterPcs_restraint(self, ctx: CyanaMRParser.Pcs_restraintContext):  # pylint: disable=unused-argument
        self.pcsRestraints += 1

        self.atomSelectionSet.clear()

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Exit a parse tree produced by CyanaMRParser#pcs_restraint.
    def exitPcs_restraint(self, ctx: CyanaMRParser.Pcs_restraintContext):  # pylint: disable=unused-argument

        try:

            seqId = int(str(ctx.Integer(0)))
            compId = str(ctx.Simple_name(0)).upper()
            atomId = str(ctx.Simple_name(1)).upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.pcsRestraints -= 1
                return

            target = self.numberSelection[0]
            error = abs(self.numberSelection[1])
            weight = self.numberSelection[2]
            orientation = int(str(ctx.Integer(1)))

            if weight < 0.0:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The relative weight value of '{weight}' should be a positive value.")

            if orientation not in self.pcsParameterDict:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The orientation '{orientation}' must be defined before you start to describe PCS restraints.")
                return

            if seqId == self.pcsParameterDict[orientation]['orientation_center_seq_id']:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The residue number '{seqId}' must not be the same as the center of orientation.")
                return

            target_value = target
            lower_limit = target - error
            upper_limit = target + error

            dstFunc = self.validatePcsRange(weight, orientation, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            self.__retrieveLocalSeqScheme()

            chainAssign = self.assignCoordPolymerSequence(seqId, compId, atomId)

            if len(chainAssign) == 0:
                return

            self.selectCoordAtoms(chainAssign, seqId, compId, atomId)

            if len(self.atomSelectionSet) < 1:
                return

            if self.__createSfDict:
                sf = self.__getSf(orientationId=orientation)
                sf['id'] += 1

            for atom in self.atomSelectionSet[0]:
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} id={self.pcsRestraints} "
                          f"atom={atom} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, None,
                                 sf['list_id'], self.__entryId, dstFunc,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom)
                    sf['loop'].add_data(row)

        except ValueError:
            self.pcsRestraints -= 1
        finally:
            self.numberSelection.clear()

    def validatePcsRange(self, weight, orientation, target_value, lower_limit, upper_limit):
        """ Validate PCS value range.
        """

        validRange = True
        dstFunc = {'weight': weight, 'orientation': orientation}

        if target_value is not None:
            if PCS_ERROR_MIN < target_value < PCS_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value}' must be within range {PCS_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if PCS_ERROR_MIN <= lower_limit < PCS_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit:.6f}' must be within range {PCS_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if PCS_ERROR_MIN < upper_limit <= PCS_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit:.6f}' must be within range {PCS_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

        if not validRange:
            return None

        if target_value is not None:
            if PCS_RANGE_MIN <= target_value <= PCS_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value}' should be within range {PCS_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if PCS_RANGE_MIN <= lower_limit <= PCS_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit:.6f}' should be within range {PCS_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if PCS_RANGE_MIN <= upper_limit <= PCS_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit:.6f}' should be within range {PCS_RESTRAINT_RANGE}.")

        return dstFunc

    # Enter a parse tree produced by CyanaMRParser#fixres_distance_restraints.
    def enterFixres_distance_restraints(self, ctx: CyanaMRParser.Fixres_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist' if self.__file_ext is None or self.__file_ext not in ('upv', 'lov') else 'noepk'
        if self.__reasons is not None and 'noepk_fixres' in self.__reasons:
            self.__cur_subtype = 'noepk'

        self.__cur_subtype_altered = False
        self.__cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixres_distance_restraints.
    def exitFixres_distance_restraints(self, ctx: CyanaMRParser.Fixres_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixres_distance_restraint.
    def enterFixres_distance_restraint(self, ctx: CyanaMRParser.Fixres_distance_restraintContext):  # pylint: disable=unused-argument
        if self.__cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixres_distance_restraint.
    def exitFixres_distance_restraint(self, ctx: CyanaMRParser.Fixres_distance_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()

            int_col = 1
            str_col = 1

            omit_dist_limit_outlier = self.__reasons is not None and self.__omitDistLimitOutlier

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            for num_col, value in enumerate(self.numberSelection):
                atomId1 = str(ctx.Simple_name(str_col)).upper()
                seqId2 = int(str(ctx.Integer(int_col)))
                compId2 = str(ctx.Simple_name(str_col + 1)).upper()
                atomId2 = str(ctx.Simple_name(str_col + 2)).upper()

                target_value = None
                lower_limit = None
                upper_limit = None

                if self.__cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        if value > self.__max_dist_value:
                            self.__max_dist_value = value
                        if value < self.__min_dist_value:
                            self.__min_dist_value = value

                    if 'upl' in (self.__file_ext, self.__cur_dist_type):
                        upper_limit = value

                    elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                        lower_limit = value

                    elif self.__upl_or_lol is None:
                        if self.__cur_dist_type == 'upl':
                            upper_limit = value
                        elif self.__cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                        else:
                            lower_limit = value

                    elif self.__upl_or_lol == 'upl_only':
                        if self.__cur_dist_type == 'upl':
                            upper_limit = value
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        elif self.__cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            lower_limit = value

                    elif self.__upl_or_lol == 'upl_w_lol':
                        upper_limit = value

                    elif self.__upl_or_lol == 'lol_only':
                        lower_limit = value
                        if self.__applyPdbStatCap:
                            upper_limit = 5.5  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # 'lol_w_upl'
                        lower_limit = value

                    if len(self.__cur_dist_type) > 0 and self.__cur_dist_type not in self.__local_dist_types:
                        self.__local_dist_types.append(self.__cur_dist_type)

                    if self.__hasPolySeq:

                        self.__retrieveLocalSeqScheme()

                        chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                        chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                        if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                            return

                        self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                        self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                        if len(self.atomSelectionSet) < 2:
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

                    dstFunc = self.validateDistanceRange(1.0, target_value, lower_limit, upper_limit,
                                                         None,
                                                         omit_dist_limit_outlier)

                    if dstFunc is None and abs(value) > DIST_ERROR_MAX * 10.0:
                        self.reasonsForReParsing['noepk_fixres'] = True

                else:  # 'noepk'

                    target_value = value

                    dstFunc = self.validatePeakVolumeRange(1.0, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.__hasPolySeq and not self.__hasNonPolySeq:
                    return

                if self.__cur_subtype != 'dist':

                    self.__retrieveLocalSeqScheme()

                    chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                    chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                    if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                if self.__createSfDict:
                    sf = self.__getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                           self.__csStat, self.__originalFileName),
                                      potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

                if self.__createSfDict:
                    if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                        memberLogicCode = '.'

                    memberId = '.'
                    if memberLogicCode == 'OR':
                        if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                           and (isAmbigAtomSelection(self.atomSelectionSet[0], self.__csStat)
                                or isAmbigAtomSelection(self.atomSelectionSet[1], self.__csStat)):
                            memberId = 0
                            _atom1 = _atom2 = None

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isIdenticalRestraint([atom1, atom2]):
                        continue
                    if has_intra_chain and (atom1['chain_id'] != atom2['chain_id'] or atom1['chain_id'] not in rep_chain_id_set):
                        continue
                    if self.__createSfDict and memberLogicCode == '.':
                        altAtomId1, altAtomId2 = getAltProtonIdInBondConstraint([atom1, atom2], self.__csStat)
                        if altAtomId1 is not None or altAtomId2 is not None:
                            atom1, atom2 =\
                                self.selectRealisticBondConstraint(atom1, atom2,
                                                                   altAtomId1, altAtomId2,
                                                                   dstFunc)
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
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

                        if self.__cur_subtype == 'noepk':
                            break

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

                if num_col > 0 and self.__cur_subtype == 'dist':
                    self.distRestraints += 1

                self.atomSelectionSet.clear()

                int_col += 1
                str_col += 3

        except ValueError:
            if self.__cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#fixresw_distance_restraints.
    def enterFixresw_distance_restraints(self, ctx: CyanaMRParser.Fixresw_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist' if self.__file_ext is None or self.__file_ext not in ('upv', 'lov') else 'noepk'
        if self.__reasons is not None and 'noepk_fixresw' in self.__reasons:
            self.__cur_subtype = 'noepk'

        self.__cur_subtype_altered = False
        self.__cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixresw_distance_restraints.
    def exitFixresw_distance_restraints(self, ctx: CyanaMRParser.Fixresw_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixresw_distance_restraint.
    def enterFixresw_distance_restraint(self, ctx: CyanaMRParser.Fixresw_distance_restraintContext):  # pylint: disable=unused-argument
        if self.__cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixresw_distance_restraint.
    def exitFixresw_distance_restraint(self, ctx: CyanaMRParser.Fixresw_distance_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()

            int_col = 1
            str_col = 1

            omit_dist_limit_outlier = self.__reasons is not None and self.__omitDistLimitOutlier

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            for num_col in range(0, len(self.numberSelection), 2):
                atomId1 = str(ctx.Simple_name(str_col)).upper()
                seqId2 = int(str(ctx.Integer(int_col)))
                compId2 = str(ctx.Simple_name(str_col + 1)).upper()
                atomId2 = str(ctx.Simple_name(str_col + 2)).upper()

                value = self.numberSelection[num_col]
                value2 = self.numberSelection[num_col + 1]

                delta = None
                has_square = False

                if value2 <= 1.0 or value2 < value:
                    delta = abs(value2)
                else:
                    weight = 1.0
                    has_square = True

                if weight < 0.0:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    f"The relative weight value of '{weight}' must not be a negative value.")
                    return
                if weight == 0.0:
                    self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                    f"The relative weight value of '{weight}' should be a positive value.")

                target_value = None
                lower_limit = None
                upper_limit = None
                target_value_uncertainty = None

                if self.__cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        if value > self.__max_dist_value:
                            self.__max_dist_value = value
                        if value < self.__min_dist_value:
                            self.__min_dist_value = value

                    if has_square:

                        if 'upl' in (self.__file_ext, self.__cur_dist_type):
                            upper_limit = value
                            if len(self.numberSelection) > 1:
                                weight = abs(value2)

                        elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                            lower_limit = value
                            if len(self.numberSelection) > 1:
                                weight = abs(value2)

                        elif value2 > DIST_RANGE_MAX:  # lol_only
                            lower_limit = value

                        elif (0.0 if self.__file_ext in ('upl', 'lol') else 1.8) <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                            upper_limit = value2
                            lower_limit = value
                            if self.__applyPdbStatCap:
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                        else:  # upl_only
                            if value2 > 1.8:
                                upper_limit = value2
                                if self.__applyPdbStatCap:
                                    lower_limit = 1.8  # default value of PDBStat
                                    target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                            else:
                                upper_limit = value2

                    elif delta is not None:

                        if 'upl' in (self.__file_ext, self.__cur_dist_type):
                            upper_limit = value
                            if len(self.numberSelection) > 1:
                                weight = abs(value2)

                        elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                            lower_limit = value
                            if len(self.numberSelection) > 1:
                                weight = abs(value2)

                        else:
                            if self.__applyPdbStatCap:
                                target_value = value
                                if delta > 0.0:
                                    lower_limit = value - delta
                                    upper_limit = value + delta
                            else:
                                upper_limit = value
                                if value2 > 0.0:
                                    target_value_uncertainty = value2

                    elif 'upl' in (self.__file_ext, self.__cur_dist_type):
                        upper_limit = value

                    elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                        lower_limit = value

                    elif self.__upl_or_lol is None:
                        if self.__cur_dist_type == 'upl':
                            upper_limit = value
                        elif self.__cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                        else:
                            lower_limit = value

                    elif self.__upl_or_lol == 'upl_only':
                        if self.__cur_dist_type == 'upl':
                            upper_limit = value
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        elif self.__cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            lower_limit = value

                    elif self.__upl_or_lol == 'upl_w_lol':
                        upper_limit = value

                    elif self.__upl_or_lol == 'lol_only':
                        lower_limit = value
                        if self.__applyPdbStatCap:
                            upper_limit = 5.5  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # 'lol_w_upl'
                        lower_limit = value

                    if len(self.__cur_dist_type) > 0 and self.__cur_dist_type not in self.__local_dist_types:
                        self.__local_dist_types.append(self.__cur_dist_type)

                    if self.__hasPolySeq:

                        self.__retrieveLocalSeqScheme()

                        chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                        chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                        if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                            return

                        self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                        self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                        if len(self.atomSelectionSet) < 2:
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

                    dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit,
                                                         target_value_uncertainty,
                                                         omit_dist_limit_outlier)

                    if dstFunc is None and (abs(value) > DIST_ERROR_MAX * 10.0 or abs(value2) > DIST_ERROR_MAX * 10.0):
                        self.reasonsForReParsing['noepk_fixresw'] = True

                else:  # 'noepk'

                    if has_square:
                        lower_limit = value
                        upper_limit = value2
                    else:
                        target_value = value

                    dstFunc = self.validatePeakVolumeRange(weight, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.__hasPolySeq and not self.__hasNonPolySeq:
                    return

                if self.__cur_subtype != 'dist':

                    self.__retrieveLocalSeqScheme()

                    chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                    chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                    if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                if self.__createSfDict:
                    sf = self.__getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                           self.__csStat, self.__originalFileName),
                                      potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

                if self.__createSfDict:
                    if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                        memberLogicCode = '.'

                    memberId = '.'
                    if memberLogicCode == 'OR':
                        if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                           and (isAmbigAtomSelection(self.atomSelectionSet[0], self.__csStat)
                                or isAmbigAtomSelection(self.atomSelectionSet[1], self.__csStat)):
                            memberId = 0
                            _atom1 = _atom2 = None

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isIdenticalRestraint([atom1, atom2]):
                        continue
                    if has_intra_chain and (atom1['chain_id'] != atom2['chain_id'] or atom1['chain_id'] not in rep_chain_id_set):
                        continue
                    if self.__createSfDict and memberLogicCode == '.':
                        altAtomId1, altAtomId2 = getAltProtonIdInBondConstraint([atom1, atom2], self.__csStat)
                        if altAtomId1 is not None or altAtomId2 is not None:
                            atom1, atom2 =\
                                self.selectRealisticBondConstraint(atom1, atom2,
                                                                   altAtomId1, altAtomId2,
                                                                   dstFunc)
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
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

                        if self.__cur_subtype == 'noepk':
                            break

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

                if num_col > 0 and self.__cur_subtype == 'dist':
                    self.distRestraints += 1

                self.atomSelectionSet.clear()

                int_col += 1
                str_col += 3

        except ValueError:
            if self.__cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#fixresw2_distance_restraints.
    def enterFixresw2_distance_restraints(self, ctx: CyanaMRParser.Fixresw2_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist' if self.__file_ext is None or self.__file_ext not in ('upv', 'lov') else 'noepk'
        if self.__reasons is not None and 'noepk_fixresw2' in self.__reasons:
            self.__cur_subtype = 'noepk'

        self.__cur_subtype_altered = False
        self.__cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixresw2_distance_restraints.
    def exitFixresw2_distance_restraints(self, ctx: CyanaMRParser.Fixresw2_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixresw2_distance_restraint.
    def enterFixresw2_distance_restraint(self, ctx: CyanaMRParser.Fixresw2_distance_restraintContext):  # pylint: disable=unused-argument
        if self.__cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixresw2_distance_restraint.
    def exitFixresw2_distance_restraint(self, ctx: CyanaMRParser.Fixresw2_distance_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()

            int_col = 1
            str_col = 1

            omit_dist_limit_outlier = self.__reasons is not None and self.__omitDistLimitOutlier

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            for num_col in range(0, len(self.numberSelection), 3):
                atomId1 = str(ctx.Simple_name(str_col)).upper()
                seqId2 = int(str(ctx.Integer(int_col)))
                compId2 = str(ctx.Simple_name(str_col + 1)).upper()
                atomId2 = str(ctx.Simple_name(str_col + 2)).upper()

                value = self.numberSelection[num_col]
                value2 = self.numberSelection[num_col + 1]
                weight = self.numberSelection[num_col + 2]

                if weight < 0.0:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    f"The relative weight value of '{weight}' must not be a negative value.")
                    return
                if weight == 0.0:
                    self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                    f"The relative weight value of '{weight}' should be a positive value.")

                target_value = None
                lower_limit = None
                upper_limit = None

                if self.__cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        if value > self.__max_dist_value:
                            self.__max_dist_value = value
                        if value < self.__min_dist_value:
                            self.__min_dist_value = value

                    if value2 > DIST_RANGE_MAX:  # lol_only
                        lower_limit = value

                    elif 1.8 <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                        upper_limit = value2
                        lower_limit = value
                        if self.__applyPdbStatCap:
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # upl_only
                        if value2 > 1.8:
                            upper_limit = value2
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            upper_limit = value2

                    if self.__hasPolySeq:

                        self.__retrieveLocalSeqScheme()

                        chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                        chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                        if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                            return

                        self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                        self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                        if len(self.atomSelectionSet) < 2:
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

                    dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit,
                                                         None,
                                                         omit_dist_limit_outlier)

                    if dstFunc is None and (abs(value) > DIST_ERROR_MAX * 10.0 or abs(value2) > DIST_ERROR_MAX * 10.0):
                        self.reasonsForReParsing['noepk_fixresw2'] = True

                else:  # 'noepk'

                    lower_limit = value
                    upper_limit = value2

                    dstFunc = self.validatePeakVolumeRange(weight, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.__hasPolySeq and not self.__hasNonPolySeq:
                    return

                if self.__cur_subtype != 'dist':

                    self.__retrieveLocalSeqScheme()

                    chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                    chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                    if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                if self.__createSfDict:
                    sf = self.__getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                           self.__csStat, self.__originalFileName),
                                      potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

                if self.__createSfDict:
                    if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                        memberLogicCode = '.'

                    memberId = '.'
                    if memberLogicCode == 'OR':
                        if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                           and (isAmbigAtomSelection(self.atomSelectionSet[0], self.__csStat)
                                or isAmbigAtomSelection(self.atomSelectionSet[1], self.__csStat)):
                            memberId = 0
                            _atom1 = _atom2 = None

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isIdenticalRestraint([atom1, atom2]):
                        continue
                    if has_intra_chain and (atom1['chain_id'] != atom2['chain_id'] or atom1['chain_id'] not in rep_chain_id_set):
                        continue
                    if self.__createSfDict and memberLogicCode == '.':
                        altAtomId1, altAtomId2 = getAltProtonIdInBondConstraint([atom1, atom2], self.__csStat)
                        if altAtomId1 is not None or altAtomId2 is not None:
                            atom1, atom2 =\
                                self.selectRealisticBondConstraint(atom1, atom2,
                                                                   altAtomId1, altAtomId2,
                                                                   dstFunc)
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
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

                        if self.__cur_subtype == 'noepk':
                            break

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

                if num_col > 0 and self.__cur_subtype == 'dist':
                    self.distRestraints += 1

                self.atomSelectionSet.clear()

                int_col += 1
                str_col += 3

        except ValueError:
            if self.__cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#fixatm_distance_restraints.
    def enterFixatm_distance_restraints(self, ctx: CyanaMRParser.Fixatm_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist' if self.__file_ext is None or self.__file_ext not in ('upv', 'lov') else 'noepk'
        if self.__reasons is not None and 'noepk_fixatm' in self.__reasons:
            self.__cur_subtype = 'noepk'

        self.__cur_subtype_altered = False
        self.__cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixatm_distance_restraints.
    def exitFixatm_distance_restraints(self, ctx: CyanaMRParser.Fixatm_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixatm_distance_restraint.
    def enterFixatm_distance_restraint(self, ctx: CyanaMRParser.Fixatm_distance_restraintContext):  # pylint: disable=unused-argument
        if self.__cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixatm_distance_restraint.
    def exitFixatm_distance_restraint(self, ctx: CyanaMRParser.Fixatm_distance_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()

            int_col = 1
            str_col = 2

            omit_dist_limit_outlier = self.__reasons is not None and self.__omitDistLimitOutlier

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            for num_col, value in enumerate(self.numberSelection):
                seqId2 = int(str(ctx.Integer(int_col)))
                compId2 = str(ctx.Simple_name(str_col)).upper()
                atomId2 = str(ctx.Simple_name(str_col + 1)).upper()

                target_value = None
                lower_limit = None
                upper_limit = None

                if self.__cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        if value > self.__max_dist_value:
                            self.__max_dist_value = value
                        if value < self.__min_dist_value:
                            self.__min_dist_value = value

                    if 'upl' in (self.__file_ext, self.__cur_dist_type):
                        upper_limit = value

                    elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                        lower_limit = value

                    elif self.__upl_or_lol is None:
                        if self.__cur_dist_type == 'upl':
                            upper_limit = value
                        elif self.__cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                        else:
                            lower_limit = value

                    elif self.__upl_or_lol == 'upl_only':
                        if self.__cur_dist_type == 'upl':
                            upper_limit = value
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        elif self.__cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            lower_limit = value

                    elif self.__upl_or_lol == 'upl_w_lol':
                        upper_limit = value

                    elif self.__upl_or_lol == 'lol_only':
                        lower_limit = value
                        if self.__applyPdbStatCap:
                            upper_limit = 5.5  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # 'lol_w_upl'
                        lower_limit = value

                    if len(self.__cur_dist_type) > 0 and self.__cur_dist_type not in self.__local_dist_types:
                        self.__local_dist_types.append(self.__cur_dist_type)

                    if self.__hasPolySeq:

                        self.__retrieveLocalSeqScheme()

                        chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                        chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                        if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                            return

                        self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                        self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                        if len(self.atomSelectionSet) < 2:
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

                    dstFunc = self.validateDistanceRange(1.0, target_value, lower_limit, upper_limit,
                                                         None,
                                                         omit_dist_limit_outlier)

                    if dstFunc is None and abs(value) > DIST_ERROR_MAX * 10.0:
                        self.reasonsForReParsing['noepk_fixatm'] = True

                else:  # 'noepk'

                    target_value = value

                    dstFunc = self.validatePeakVolumeRange(1.0, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.__hasPolySeq and not self.__hasNonPolySeq:
                    return

                if self.__cur_subtype != 'dist':

                    self.__retrieveLocalSeqScheme()

                    chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                    chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                    if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                if self.__createSfDict:
                    sf = self.__getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                           self.__csStat, self.__originalFileName),
                                      potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

                if self.__createSfDict:
                    if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                        memberLogicCode = '.'

                    memberId = '.'
                    if memberLogicCode == 'OR':
                        if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                           and (isAmbigAtomSelection(self.atomSelectionSet[0], self.__csStat)
                                or isAmbigAtomSelection(self.atomSelectionSet[1], self.__csStat)):
                            memberId = 0
                            _atom1 = _atom2 = None

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isIdenticalRestraint([atom1, atom2]):
                        continue
                    if has_intra_chain and (atom1['chain_id'] != atom2['chain_id'] or atom1['chain_id'] not in rep_chain_id_set):
                        continue
                    if self.__createSfDict and memberLogicCode == '.':
                        altAtomId1, altAtomId2 = getAltProtonIdInBondConstraint([atom1, atom2], self.__csStat)
                        if altAtomId1 is not None or altAtomId2 is not None:
                            atom1, atom2 =\
                                self.selectRealisticBondConstraint(atom1, atom2,
                                                                   altAtomId1, altAtomId2,
                                                                   dstFunc)
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
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

                        if self.__cur_subtype == 'noepk':
                            break

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

                if num_col > 0 and self.__cur_subtype == 'dist':
                    self.distRestraints += 1

                self.atomSelectionSet.clear()

                int_col += 1
                str_col += 2

        except ValueError:
            if self.__cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#fixatmw_distance_restraints.
    def enterFixatmw_distance_restraints(self, ctx: CyanaMRParser.Fixatmw_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist' if self.__file_ext is None or self.__file_ext not in ('upv', 'lov') else 'noepk'
        if self.__reasons is not None and 'noepk_fixatmw' in self.__reasons:
            self.__cur_subtype = 'noepk'

        self.__cur_subtype_altered = False
        self.__cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixatmw_distance_restraints.
    def exitFixatmw_distance_restraints(self, ctx: CyanaMRParser.Fixatmw_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixatmw_distance_restraint.
    def enterFixatmw_distance_restraint(self, ctx: CyanaMRParser.Fixatmw_distance_restraintContext):  # pylint: disable=unused-argument
        if self.__cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixatmw_distance_restraint.
    def exitFixatmw_distance_restraint(self, ctx: CyanaMRParser.Fixatmw_distance_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()

            int_col = 1
            str_col = 2

            omit_dist_limit_outlier = self.__reasons is not None and self.__omitDistLimitOutlier

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            for num_col in range(0, len(self.numberSelection), 2):
                seqId2 = int(str(ctx.Integer(int_col)))
                compId2 = str(ctx.Simple_name(str_col)).upper()
                atomId2 = str(ctx.Simple_name(str_col + 1)).upper()

                value = self.numberSelection[num_col]
                value2 = self.numberSelection[num_col + 1]

                delta = None
                has_square = False

                if value2 < 0.0:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    f"The relative weight value of '{value2}' must not be a negative value.")
                    return
                if value2 == 0.0:
                    self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                    f"The relative weight value of '{value2}' should be a positive value.")

                if value2 <= 1.0 or value2 < value:
                    delta = abs(value2)
                else:
                    weight = 1.0
                    has_square = True

                target_value = None
                lower_limit = None
                upper_limit = None
                target_value_uncertainty = None

                if self.__cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        if value > self.__max_dist_value:
                            self.__max_dist_value = value
                        if value < self.__min_dist_value:
                            self.__min_dist_value = value

                    if has_square:

                        if 'upl' in (self.__file_ext, self.__cur_dist_type):
                            upper_limit = value
                            if len(self.numberSelection) > 1:
                                weight = abs(value2)

                        elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                            lower_limit = value
                            if len(self.numberSelection) > 1:
                                weight = abs(value2)

                        elif value2 > DIST_RANGE_MAX:  # lol_only
                            lower_limit = value

                        elif (0.0 if self.__file_ext in ('upl', 'lol') else 1.8) <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                            upper_limit = value2
                            lower_limit = value
                            if self.__applyPdbStatCap:
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                        else:  # upl_only
                            if value2 > 1.8:
                                upper_limit = value2
                                if self.__applyPdbStatCap:
                                    lower_limit = 1.8  # default value of PDBStat
                                    target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                            else:
                                upper_limit = value2

                    elif delta is not None:

                        if 'upl' in (self.__file_ext, self.__cur_dist_type):
                            upper_limit = value
                            if len(self.numberSelection) > 1:
                                weight = abs(value2)

                        elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                            lower_limit = value
                            if len(self.numberSelection) > 1:
                                weight = abs(value2)

                        else:
                            if self.__applyPdbStatCap:
                                target_value = value
                                if delta > 0.0:
                                    lower_limit = value - delta
                                    upper_limit = value + delta
                            else:
                                upper_limit = value
                                if value2 > 0.0:
                                    target_value_uncertainty = value2

                    elif 'upl' in (self.__file_ext, self.__cur_dist_type):
                        upper_limit = value

                    elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                        lower_limit = value

                    elif self.__upl_or_lol is None:
                        if self.__cur_dist_type == 'upl':
                            upper_limit = value
                        elif self.__cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                        else:
                            lower_limit = value

                    elif self.__upl_or_lol == 'upl_only':
                        if self.__cur_dist_type == 'upl':
                            upper_limit = value
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        elif self.__cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            lower_limit = value

                    elif self.__upl_or_lol == 'upl_w_lol':
                        upper_limit = value

                    elif self.__upl_or_lol == 'lol_only':
                        lower_limit = value
                        if self.__applyPdbStatCap:
                            upper_limit = 5.5  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # 'lol_w_upl'
                        lower_limit = value

                    if len(self.__cur_dist_type) > 0 and self.__cur_dist_type not in self.__local_dist_types:
                        self.__local_dist_types.append(self.__cur_dist_type)

                    if self.__hasPolySeq:

                        self.__retrieveLocalSeqScheme()

                        chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                        chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                        if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                            return

                        self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                        self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                        if len(self.atomSelectionSet) < 2:
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

                    dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit,
                                                         target_value_uncertainty,
                                                         omit_dist_limit_outlier)

                    if dstFunc is None and (abs(value) > DIST_ERROR_MAX * 10.0 or abs(value2) > DIST_ERROR_MAX * 10.0):
                        self.reasonsForReParsing['noepk_fixatmw'] = True

                else:  # 'noepk'

                    if has_square:
                        lower_limit = value
                        upper_limit = value2
                    else:
                        target_value = value

                    dstFunc = self.validatePeakVolumeRange(weight, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.__hasPolySeq and not self.__hasNonPolySeq:
                    return

                if self.__cur_subtype != 'dist':

                    self.__retrieveLocalSeqScheme()

                    chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                    chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                    if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                if self.__createSfDict:
                    sf = self.__getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                           self.__csStat, self.__originalFileName),
                                      potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

                if self.__createSfDict:
                    if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                        memberLogicCode = '.'

                    memberId = '.'
                    if memberLogicCode == 'OR':
                        if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                           and (isAmbigAtomSelection(self.atomSelectionSet[0], self.__csStat)
                                or isAmbigAtomSelection(self.atomSelectionSet[1], self.__csStat)):
                            memberId = 0
                            _atom1 = _atom2 = None

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isIdenticalRestraint([atom1, atom2]):
                        continue
                    if has_intra_chain and (atom1['chain_id'] != atom2['chain_id'] or atom1['chain_id'] not in rep_chain_id_set):
                        continue
                    if self.__createSfDict and memberLogicCode == '.':
                        altAtomId1, altAtomId2 = getAltProtonIdInBondConstraint([atom1, atom2], self.__csStat)
                        if altAtomId1 is not None or altAtomId2 is not None:
                            atom1, atom2 =\
                                self.selectRealisticBondConstraint(atom1, atom2,
                                                                   altAtomId1, altAtomId2,
                                                                   dstFunc)
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
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

                        if self.__cur_subtype == 'noepk':
                            break

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

                if num_col > 0 and self.__cur_subtype == 'dist':
                    self.distRestraints += 1

                self.atomSelectionSet.clear()

                int_col += 1
                str_col += 2

        except ValueError:
            if self.__cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#fixatmw2_distance_restraints.
    def enterFixatmw2_distance_restraints(self, ctx: CyanaMRParser.Fixatmw2_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist' if self.__file_ext is None or self.__file_ext not in ('upv', 'lov') else 'noepk'
        if self.__reasons is not None and 'noepk_fixatmw2' in self.__reasons:
            self.__cur_subtype = 'noepk'

        self.__cur_subtype_altered = False
        self.__cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixatmw2_distance_restraints.
    def exitFixatmw2_distance_restraints(self, ctx: CyanaMRParser.Fixatmw2_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixatmw2_distance_restraint.
    def enterFixatmw2_distance_restraint(self, ctx: CyanaMRParser.Fixatmw2_distance_restraintContext):  # pylint: disable=unused-argument
        if self.__cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixatmw2_distance_restraint.
    def exitFixatmw2_distance_restraint(self, ctx: CyanaMRParser.Fixatmw2_distance_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()

            int_col = 1
            str_col = 2

            omit_dist_limit_outlier = self.__reasons is not None and self.__omitDistLimitOutlier

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            for num_col in range(0, len(self.numberSelection), 3):
                seqId2 = int(str(ctx.Integer(int_col)))
                compId2 = str(ctx.Simple_name(str_col)).upper()
                atomId2 = str(ctx.Simple_name(str_col + 1)).upper()

                value = self.numberSelection[num_col]
                value2 = self.numberSelection[num_col + 1]
                weight = self.numberSelection[num_col + 2]

                if weight < 0.0:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    f"The relative weight value of '{weight}' must not be a negative value.")
                    return
                if weight == 0.0:
                    self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                    f"The relative weight value of '{weight}' should be a positive value.")

                target_value = None
                lower_limit = None
                upper_limit = None

                if self.__cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        if value > self.__max_dist_value:
                            self.__max_dist_value = value
                        if value < self.__min_dist_value:
                            self.__min_dist_value = value

                    if value2 > DIST_RANGE_MAX:  # lol_only
                        lower_limit = value

                    elif 1.8 <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                        upper_limit = value2
                        lower_limit = value
                        if self.__applyPdbStatCap:
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # upl_only
                        if value2 > 1.8:
                            upper_limit = value2
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            upper_limit = value2

                    if self.__hasPolySeq:

                        self.__retrieveLocalSeqScheme()

                        chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                        chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                        if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                            return

                        self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                        self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                        if len(self.atomSelectionSet) < 2:
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

                    dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit,
                                                         None,
                                                         omit_dist_limit_outlier)

                    if dstFunc is None and (abs(value) > DIST_ERROR_MAX * 10.0 or abs(value2) > DIST_ERROR_MAX * 10.0):
                        self.reasonsForReParsing['noepk_fixatmw2'] = True

                else:  # 'noepk'

                    lower_limit = value
                    upper_limit = value2

                    dstFunc = self.validatePeakVolumeRange(weight, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.__hasPolySeq and not self.__hasNonPolySeq:
                    return

                if self.__cur_subtype != 'dist':

                    self.__retrieveLocalSeqScheme()

                    chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                    chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                    if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                if self.__createSfDict:
                    sf = self.__getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                           self.__csStat, self.__originalFileName),
                                      potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

                if self.__createSfDict:
                    if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                        memberLogicCode = '.'

                    memberId = '.'
                    if memberLogicCode == 'OR':
                        if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                           and (isAmbigAtomSelection(self.atomSelectionSet[0], self.__csStat)
                                or isAmbigAtomSelection(self.atomSelectionSet[1], self.__csStat)):
                            memberId = 0
                            _atom1 = _atom2 = None

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isIdenticalRestraint([atom1, atom2]):
                        continue
                    if has_intra_chain and (atom1['chain_id'] != atom2['chain_id'] or atom1['chain_id'] not in rep_chain_id_set):
                        continue
                    if self.__createSfDict and memberLogicCode == '.':
                        altAtomId1, altAtomId2 = getAltProtonIdInBondConstraint([atom1, atom2], self.__csStat)
                        if altAtomId1 is not None or altAtomId2 is not None:
                            atom1, atom2 =\
                                self.selectRealisticBondConstraint(atom1, atom2,
                                                                   altAtomId1, altAtomId2,
                                                                   dstFunc)
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
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

                        if self.__cur_subtype == 'noepk':
                            break

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

                if num_col > 0 and self.__cur_subtype == 'dist':
                    self.distRestraints += 1

                self.atomSelectionSet.clear()

                int_col += 1
                str_col += 2

        except ValueError:
            if self.__cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#qconvr_distance_restraints.
    def enterQconvr_distance_restraints(self, ctx: CyanaMRParser.Qconvr_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist'

    # Exit a parse tree produced by CyanaMRParser#qconvr_distance_restraints.
    def exitQconvr_distance_restraints(self, ctx: CyanaMRParser.Qconvr_distance_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#qconvr_distance_restraint.
    def enterQconvr_distance_restraint(self, ctx: CyanaMRParser.Qconvr_distance_restraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#qconvr_distance_restraint.
    def exitQconvr_distance_restraint(self, ctx: CyanaMRParser.Qconvr_distance_restraintContext):

        try:

            upl = bool(ctx.NoeUpp())

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()
            seqId2 = int(str(ctx.Integer(1)))
            compId2 = str(ctx.Simple_name(2)).upper()
            atomId2 = str(ctx.Simple_name(3)).upper()

            target_value = None
            lower_limit = None
            upper_limit = None

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            value = self.numberSelection[0]
            weight = 1.0

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                if upl and value > self.__max_dist_value:
                    self.__max_dist_value = value
                if not upl and value < self.__min_dist_value:
                    self.__min_dist_value = value

            if upl:
                upper_limit = value
            else:
                lower_limit = value

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

            if len(self.atomSelectionSet) < 2:
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

            dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit,
                                                 None,
                                                 self.__omitDistLimitOutlier)

            if dstFunc is None:
                return

            if self.__createSfDict:
                sf = self.__getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                       self.__csStat, self.__originalFileName),
                                  potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                sf['id'] += 1
                memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

            has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

            if self.__createSfDict:
                if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                    memberLogicCode = '.'

                memberId = '.'
                if memberLogicCode == 'OR':
                    if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                       and (isAmbigAtomSelection(self.atomSelectionSet[0], self.__csStat)
                            or isAmbigAtomSelection(self.atomSelectionSet[1], self.__csStat)):
                        memberId = 0
                        _atom1 = _atom2 = None

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if isIdenticalRestraint([atom1, atom2]):
                    continue
                if has_intra_chain and (atom1['chain_id'] != atom2['chain_id'] or atom1['chain_id'] not in rep_chain_id_set):
                    continue
                if self.__createSfDict and memberLogicCode == '.':
                    altAtomId1, altAtomId2 = getAltProtonIdInBondConstraint([atom1, atom2], self.__csStat)
                    if altAtomId1 is not None or altAtomId2 is not None:
                        atom1, atom2 =\
                            self.selectRealisticBondConstraint(atom1, atom2,
                                                               altAtomId1, altAtomId2,
                                                               dstFunc)
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
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

        except ValueError:
            self.distRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain_restraints.
    def enterDistance_w_chain_restraints(self, ctx: CyanaMRParser.Distance_w_chain_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist'

        self.__cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain_restraints.
    def exitDistance_w_chain_restraints(self, ctx: CyanaMRParser.Distance_w_chain_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain_restraint.
    def enterDistance_w_chain_restraint(self, ctx: CyanaMRParser.Distance_w_chain_restraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain_restraint.
    def exitDistance_w_chain_restraint(self, ctx: CyanaMRParser.Distance_w_chain_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            seqId2 = int(str(ctx.Integer(1)))
            jVal = [''] * 6
            for j in range(6):
                jVal[j] = str(ctx.Simple_name(j)).upper()

            if len(self.__col_order_of_dist_w_chain) == 0:
                for j in range(3):
                    if len(jVal[j]) > 2 and translateToStdResName(jVal[j], self.__ccU) in monDict3:
                        compId = translateToStdResName(jVal[j], self.__ccU)
                        if self.__ccU.updateChemCompDict(compId):
                            for k in range(3):
                                if k == j:
                                    continue
                                atomId = jVal[k]
                                _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId, leave_unmatched=True)
                                if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                                    _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)
                                    if atomId[-1].isdigit() and int(atomId[-1]) <= len(_atomId):
                                        _atomId = [_atomId[int(atomId[-1]) - 1]]

                                if details is not None:
                                    _atomId_ = translateToStdAtomName(atomId, compId, ccU=self.__ccU)
                                    if _atomId_ != atomId:
                                        if atomId.startswith('HT') and len(_atomId_) == 2:
                                            _atomId_ = 'H'
                                        _atomId = self.__nefT.get_valid_star_atom_in_xplor(compId, _atomId_)[0]
                                if len(_atomId) > 0:
                                    cca = next((cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == _atomId[0]), None)
                                    if cca is not None:
                                        self.__col_order_of_dist_w_chain['comp_id_1'] = j
                                        self.__col_order_of_dist_w_chain['atom_id_1'] = k
                                        self.__col_order_of_dist_w_chain['chain_id_1'] = 3 - (j + k)
                                        break
                    elif len(jVal[j]) > 1 and translateToStdResName(jVal[j], self.__ccU) not in monDict3:
                        compId = translateToStdResName(jVal[j], self.__ccU)
                        if self.__ccU.updateChemCompDict(compId):
                            for k in range(3):
                                if k == j:
                                    continue
                                atomId = jVal[k]
                                _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId, leave_unmatched=True)
                                if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                                    _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)
                                    if atomId[-1].isdigit() and int(atomId[-1]) <= len(_atomId):
                                        _atomId = [_atomId[int(atomId[-1]) - 1]]

                                if details is not None:
                                    _atomId_ = translateToStdAtomName(atomId, compId, ccU=self.__ccU)
                                    if _atomId_ != atomId:
                                        if atomId.startswith('HT') and len(_atomId_) == 2:
                                            _atomId_ = 'H'
                                        _atomId = self.__nefT.get_valid_star_atom_in_xplor(compId, _atomId_)[0]
                                if len(_atomId) > 0:
                                    cca = next((cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == _atomId[0]), None)
                                    if cca is not None:
                                        self.__col_order_of_dist_w_chain['comp_id_1'] = j
                                        self.__col_order_of_dist_w_chain['atom_id_1'] = k
                                        self.__col_order_of_dist_w_chain['chain_id_1'] = 3 - (j + k)
                                        break
                for j in range(3, 6):
                    if len(jVal[j]) > 2 and translateToStdResName(jVal[j], self.__ccU) in monDict3:
                        compId = translateToStdResName(jVal[j], self.__ccU)
                        if self.__ccU.updateChemCompDict(compId):
                            for k in range(3, 6):
                                if k == j:
                                    continue
                                atomId = jVal[k]
                                _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId, leave_unmatched=True)
                                if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                                    _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)
                                    if atomId[-1].isdigit() and int(atomId[-1]) <= len(_atomId):
                                        _atomId = [_atomId[int(atomId[-1]) - 1]]

                                if details is not None:
                                    _atomId_ = translateToStdAtomName(atomId, compId, ccU=self.__ccU)
                                    if atomId.startswith('HT') and len(_atomId_) == 2:
                                        _atomId_ = 'H'
                                    if _atomId_ != atomId:
                                        _atomId = self.__nefT.get_valid_star_atom_in_xplor(compId, _atomId_)[0]
                                if len(_atomId) > 0:
                                    cca = next((cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == _atomId[0]), None)
                                    if cca is not None:
                                        self.__col_order_of_dist_w_chain['comp_id_2'] = j
                                        self.__col_order_of_dist_w_chain['atom_id_2'] = k
                                        self.__col_order_of_dist_w_chain['chain_id_2'] = 12 - (j + k)
                                        break
                    elif len(jVal[j]) > 1 and translateToStdResName(jVal[j], self.__ccU) not in monDict3:
                        compId = translateToStdResName(jVal[j], self.__ccU)
                        if self.__ccU.updateChemCompDict(compId):
                            for k in range(3, 6):
                                if k == j:
                                    continue
                                atomId = jVal[k]
                                _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId, leave_unmatched=True)
                                if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                                    _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)
                                    if atomId[-1].isdigit() and int(atomId[-1]) <= len(_atomId):
                                        _atomId = [_atomId[int(atomId[-1]) - 1]]

                                if details is not None:
                                    _atomId_ = translateToStdAtomName(atomId, compId, ccU=self.__ccU)
                                    if atomId.startswith('HT') and len(_atomId_) == 2:
                                        _atomId_ = 'H'
                                    if _atomId_ != atomId:
                                        _atomId = self.__nefT.get_valid_star_atom_in_xplor(compId, _atomId_)[0]
                                if len(_atomId) > 0:
                                    cca = next((cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == _atomId[0]), None)
                                    if cca is not None:
                                        self.__col_order_of_dist_w_chain['comp_id_2'] = j
                                        self.__col_order_of_dist_w_chain['atom_id_2'] = k
                                        self.__col_order_of_dist_w_chain['chain_id_2'] = 12 - (j + k)
                                        break

            if len(self.__col_order_of_dist_w_chain) != 6:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Failed to identify columns for comp_id_1, atom_id_1, chain_id_1, comp_id_2, atom_id_2, chain_id_2.")
                self.distRestraints -= 1
                return

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.distRestraints -= 1
                return

            target_value = None
            lower_limit = None
            upper_limit = None
            target_value_uncertainty = None

            value = self.numberSelection[0]
            weight = 1.0

            delta = None
            has_square = False

            if len(self.numberSelection) > 2:
                value2 = self.numberSelection[1]
                weight = self.numberSelection[2]

                has_square = True

            elif len(self.numberSelection) > 1:
                value2 = self.numberSelection[1]

                if value2 <= 1.0 or value2 < value:
                    delta = abs(value2)
                else:
                    has_square = True

            if weight < 0.0:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The relative weight value of '{weight}' should be a positive value.")

            if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX and not self.__cur_subtype_altered:
                if value > self.__max_dist_value:
                    self.__max_dist_value = value
                if value < self.__min_dist_value:
                    self.__min_dist_value = value

            if has_square:

                if 'upl' in (self.__file_ext, self.__cur_dist_type):
                    upper_limit = value
                    if len(self.numberSelection) > 1:
                        weight = abs(value2)

                elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                    lower_limit = value
                    if len(self.numberSelection) > 1:
                        weight = abs(value2)

                elif value2 > DIST_RANGE_MAX:  # lol_only
                    lower_limit = value

                elif (0.0 if self.__file_ext in ('upl', 'lol') else 1.8) <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                    upper_limit = value2
                    lower_limit = value
                    if self.__applyPdbStatCap:
                        target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                else:  # upl_only
                    if value2 > 1.8:
                        upper_limit = value2
                        if self.__applyPdbStatCap:
                            lower_limit = 1.8  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                    else:
                        upper_limit = value2

            elif delta is not None:

                if 'upl' in (self.__file_ext, self.__cur_dist_type):
                    upper_limit = value
                    if len(self.numberSelection) > 1:
                        weight = abs(value2)

                elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                    lower_limit = value
                    if len(self.numberSelection) > 1:
                        weight = abs(value2)

                else:
                    if self.__applyPdbStatCap:
                        target_value = value
                        if delta > 0.0:
                            lower_limit = value - delta
                            upper_limit = value + delta
                    else:
                        upper_limit = value
                        if value2 > 0.0:
                            target_value_uncertainty = value2

            elif 'upl' in (self.__file_ext, self.__cur_dist_type):
                upper_limit = value

            elif 'lol' in (self.__file_ext, self.__cur_dist_type):
                lower_limit = value

            elif self.__upl_or_lol is None:
                if self.__cur_dist_type == 'upl':
                    upper_limit = value
                elif self.__cur_dist_type == 'lol':
                    lower_limit = value
                elif value > 1.8:
                    upper_limit = value
                else:
                    lower_limit = value

            elif self.__upl_or_lol == 'upl_only':
                if self.__cur_dist_type == 'upl':
                    upper_limit = value
                    if self.__applyPdbStatCap:
                        lower_limit = 1.8  # default value of PDBStat
                        target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                elif self.__cur_dist_type == 'lol':
                    lower_limit = value
                elif value > 1.8:
                    upper_limit = value
                    if self.__applyPdbStatCap:
                        lower_limit = 1.8  # default value of PDBStat
                        target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                else:
                    lower_limit = value

            elif self.__upl_or_lol == 'upl_w_lol':
                upper_limit = value

            elif self.__upl_or_lol == 'lol_only':
                lower_limit = value
                if self.__applyPdbStatCap:
                    upper_limit = 5.5  # default value of PDBStat
                    target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

            else:  # 'lol_w_upl'
                lower_limit = value

            if len(self.__cur_dist_type) > 0 and self.__cur_dist_type not in self.__local_dist_types:
                self.__local_dist_types.append(self.__cur_dist_type)

            if not self.__hasPolySeq and not self.__hasNonPolySeq:  # can't decide whether NOE or RDC wo the coordinates
                return

            chainId1 = jVal[self.__col_order_of_dist_w_chain['chain_id_1']]
            chainId2 = jVal[self.__col_order_of_dist_w_chain['chain_id_2']]
            compId1 = jVal[self.__col_order_of_dist_w_chain['comp_id_1']]
            compId2 = jVal[self.__col_order_of_dist_w_chain['comp_id_2']]
            atomId1 = jVal[self.__col_order_of_dist_w_chain['atom_id_1']]
            atomId2 = jVal[self.__col_order_of_dist_w_chain['atom_id_2']]

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

            if len(self.atomSelectionSet) < 2:
                return

            if len(self.atomSelectionSet[0]) == 1 and len(self.atomSelectionSet[1]) == 1:

                isRdc = True

                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                    isRdc = False

                if chain_id_1 != chain_id_2:
                    isRdc = False

                if abs(seq_id_1 - seq_id_2) > 1:
                    isRdc = False

                if abs(seq_id_1 - seq_id_2) == 1:

                    if self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                            ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                             or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')):
                        pass

                    else:
                        isRdc = False

                elif atom_id_1 == atom_id_2:
                    isRdc = False

                elif self.__ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                    if not self.__ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                        if self.__nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.__nefT.validate_comp_atom(comp_id_2, atom_id_2):
                            isRdc = False

                if not isRdc:
                    self.__cur_subtype_altered = False

                else:

                    isRdc = False

                    if self.__cur_subtype_altered and atom_id_1 + atom_id_2 == self.auxAtomSelectionSet:
                        isRdc = True

                    elif value < 1.0 or value > 6.0:
                        self.auxAtomSelectionSet = atom_id_1 + atom_id_2
                        self.__cur_subtype_altered = True
                        self.__cur_rdc_orientation += 1
                        isRdc = True

                    if isRdc:
                        self.__cur_subtype = 'rdc'
                        self.rdcRestraints += 1
                        self.distRestraints -= 1

                        target_value = value
                        lower_limit = upper_limit = None

                        if len(self.numberSelection) > 2:
                            error = abs(self.numberSelection[1])
                            lower_limit = target_value - error
                            upper_limit = target_value + error

                        dstFunc = self.validateRdcRange(weight, self.__cur_rdc_orientation, target_value, lower_limit, upper_limit)

                        if dstFunc is None:
                            return

                        if self.__createSfDict:
                            sf = self.__getSf(potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc),
                                              rdcCode=getRdcCode([self.atomSelectionSet[0][0], self.atomSelectionSet[1][0]]),
                                              orientationId=self.__cur_rdc_orientation)
                            sf['id'] += 1

                        for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                              self.atomSelectionSet[1]):
                            if isIdenticalRestraint([atom1, atom2]):
                                continue
                            if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None):
                                continue
                            if self.__debug:
                                print(f"subtype={self.__cur_subtype} id={self.rdcRestraints} "
                                      f"atom1={atom1} atom2={atom2} {dstFunc}")
                            if self.__createSfDict and sf is not None:
                                sf['index_id'] += 1
                                row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                             '.', None, None,
                                             sf['list_id'], self.__entryId, dstFunc,
                                             self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                             atom1, atom2)
                                sf['loop'].add_data(row)

                        self.__cur_subtype = 'dist'

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

            dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit,
                                                 target_value_uncertainty,
                                                 self.__omitDistLimitOutlier)

            if dstFunc is None:
                return

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.atomSelectionSet.clear()

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

            if len(self.atomSelectionSet) < 2:
                return

            if self.__createSfDict:
                sf = self.__getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                       self.__csStat, self.__originalFileName),
                                  potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                sf['id'] += 1
                memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                memberId = '.'
                if memberLogicCode == 'OR':
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
                    print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
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

        except ValueError:
            self.distRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain2_restraints.
    def enterDistance_w_chain2_restraints(self, ctx: CyanaMRParser.Distance_w_chain2_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist'

        self.__cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain2_restraints.
    def exitDistance_w_chain2_restraints(self, ctx: CyanaMRParser.Distance_w_chain2_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain2_restraint.
    def enterDistance_w_chain2_restraint(self, ctx: CyanaMRParser.Distance_w_chain2_restraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain2_restraint.
    def exitDistance_w_chain2_restraint(self, ctx: CyanaMRParser.Distance_w_chain2_restraintContext):
        self.exitDistance_w_chain_restraint(ctx)

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain3_restraints.
    def enterDistance_w_chain3_restraints(self, ctx: CyanaMRParser.Distance_w_chain3_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist'

        self.__cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain3_restraints.
    def exitDistance_w_chain3_restraints(self, ctx: CyanaMRParser.Distance_w_chain3_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain3_restraint.
    def enterDistance_w_chain3_restraint(self, ctx: CyanaMRParser.Distance_w_chain3_restraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain3_restraint.
    def exitDistance_w_chain3_restraint(self, ctx: CyanaMRParser.Distance_w_chain3_restraintContext):
        self.exitDistance_w_chain_restraint(ctx)

    # Enter a parse tree produced by CyanaMRParser#torsion_angle_w_chain_restraints.
    def enterTorsion_angle_w_chain_restraints(self, ctx: CyanaMRParser.Torsion_angle_w_chain_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dihed'
        self.__cur_dist_type = ''

        self.__cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#torsion_angle_w_chain_restraints.
    def exitTorsion_angle_w_chain_restraints(self, ctx: CyanaMRParser.Torsion_angle_w_chain_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#torsion_angle_w_chain_restraint.
    def enterTorsion_angle_w_chain_restraint(self, ctx: CyanaMRParser.Torsion_angle_w_chain_restraintContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#torsion_angle_w_chain_restraint.
    def exitTorsion_angle_w_chain_restraint(self, ctx: CyanaMRParser.Torsion_angle_w_chain_restraintContext):

        try:

            chainId = str(ctx.Simple_name(0))
            seqId = int(str(ctx.Integer()))
            compId = str(ctx.Simple_name(1)).upper()
            _compId = translateToStdResName(compId, self.__ccU)
            angleName = str(ctx.Simple_name(2)).upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            target_value = None
            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]

            if self.__remediate and self.__reasons is not None and 'dihed_unusual_order' in self.__reasons:
                target_value, deviation = lower_limit, upper_limit
                if deviation > 0.0:
                    lower_limit = target_value - deviation
                    upper_limit = target_value + deviation
                else:
                    lower_limit = upper_limit = None

            weight = 1.0
            if len(self.numberSelection) > 2:
                weight = self.numberSelection[2]

            if weight < 0.0:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The relative weight value of '{weight}' should be a positive value.")
            """
            if lower_limit > upper_limit:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The angle's lower limit '{lower_limit}' must be less than or equal to the upper limit '{upper_limit}'.")
                if self.__remediate:
                    self.__dihed_lb_greater_than_ub = True
                return
            """
            if self.__remediate and upper_limit < 0.0:
                self.__dihed_ub_always_positive = False

            # target_value = (upper_limit + lower_limit) / 2.0

            dstFunc = self.validateAngleRange(weight, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            # support AMBER's dihedral angle naming convention for nucleic acids
            # http://ambermd.org/tutorials/advanced/tutorial4/
            if angleName in ('EPSILN', 'EPSLN'):
                angleName = 'EPSILON'

            # nucleic CHI angle
            if angleName == 'CHIN':
                angleName = 'CHI'

            if angleName not in KNOWN_ANGLE_NAMES:
                lenAngleName = len(angleName)
                try:
                    # For the case 'EPSIL' could be standard name 'EPSILON'
                    angleName = next(name for name in KNOWN_ANGLE_NAMES if len(name) >= lenAngleName and name[:lenAngleName] == angleName)
                except StopIteration:
                    self.__f.append(f"[Insufficient angle selection] {self.__getCurrentRestraint()}"
                                    f"The angle identifier {str(ctx.Simple_name(2))!r} is unknown for the residue {_compId!r}, "
                                    "of which CYANA residue library should be uploaded.")
                    return

            peptide, nucleotide, carbohydrate = self.__csStat.getTypeOfCompId(compId)

            if carbohydrate:
                chainAssign = self.assignCoordPolymerSequenceWithChainId(chainId, seqId, compId, 'CA')
                if len(chainAssign) > 0:
                    ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chainAssign[0][0]), None)
                    if ps is not None and 'type' in ps and 'polypeptide' in ps['type']:
                        peptide = True
                        nucleotide = carbohydrate = False

            if carbohydrate and angleName in KNOWN_ANGLE_CARBO_ATOM_NAMES:
                atomNames = KNOWN_ANGLE_CARBO_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_CARBO_SEQ_OFFSET[angleName]
            else:
                atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

            if angleName != 'PPA':

                if isinstance(atomNames, list):
                    atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)
                else:  # nucleic CHI angle
                    atomId = next(name for name, offset in zip(atomNames['Y'], seqOffset['Y']) if offset == 0)

                if not isinstance(atomId, str):
                    self.__ccU.updateChemCompDict(compId)
                    atomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if atomId.match(cca[self.__ccU.ccaAtomId])), None)
                    if atomId is None and carbohydrate:
                        atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                        if isinstance(atomNames, list):
                            atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)
                        else:  # nucleic CHI angle
                            atomId = next(name for name, offset in zip(atomNames['Y'], seqOffset['Y']) if offset == 0)

                        if not isinstance(atomId, str):
                            atomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if atomId.match(cca[self.__ccU.ccaAtomId])), None)
                            if atomId is None:
                                self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                                f"{seqId}:{_compId} is not present in the coordinates.")
                                return

                self.__retrieveLocalSeqScheme()

                chainAssign = self.assignCoordPolymerSequenceWithChainId(chainId, seqId, compId, atomId)

                if len(chainAssign) == 0:
                    self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                    f"{seqId}:{_compId} is not present in the coordinates.")
                    return

                for chainId, cifSeqId, cifCompId, _ in chainAssign:
                    if carbohydrate:
                        if self.__branched is not None:
                            ps = next((ps for ps in self.__branched if ps['auth_chain_id'] == chainId), None)
                        if ps is None:
                            ps = next(ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId)
                    else:
                        ps = next(ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId)

                    peptide, nucleotide, carbohydrate = self.__csStat.getTypeOfCompId(cifCompId)

                    if peptide and angleName in ('PHI', 'PSI', 'OMEGA',
                                                 'CHI1', 'CHI2', 'CHI3', 'CHI4', 'CHI5',
                                                 'CHI21', 'CHI22', 'CHI31', 'CHI32', 'CHI42'):
                        pass
                    elif nucleotide and angleName in ('ALPHA', 'BETA', 'GAMMA', 'DELTA', 'EPSILON', 'ZETA',
                                                      'CHI', 'ETA', 'THETA', "ETA'", "THETA'",
                                                      'NU0', 'NU1', 'NU2', 'NU3', 'NU4',
                                                      'TAU0', 'TAU1', 'TAU2', 'TAU3', 'TAU4'):
                        pass
                    elif carbohydrate and angleName in ('PHI', 'PSI', 'OMEGA'):
                        pass
                    else:
                        self.__f.append(f"[Insufficient angle selection] {self.__getCurrentRestraint()}"
                                        f"The angle identifier {str(ctx.Simple_name(2))!r} is unknown for the residue {_compId!r}, "
                                        "of which CYANA residue library should be uploaded.")
                        return

                    atomNames = None
                    seqOffset = None

                    if carbohydrate:
                        atomNames = KNOWN_ANGLE_CARBO_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_CARBO_SEQ_OFFSET[angleName]
                    elif nucleotide and angleName == 'CHI':
                        if self.__ccU.updateChemCompDict(cifCompId):
                            try:
                                next(cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == 'N9')
                                atomNames = KNOWN_ANGLE_ATOM_NAMES['CHI']['R']
                                seqOffset = KNOWN_ANGLE_SEQ_OFFSET['CHI']['R']
                            except StopIteration:
                                atomNames = KNOWN_ANGLE_ATOM_NAMES['CHI']['Y']
                                seqOffset = KNOWN_ANGLE_SEQ_OFFSET['CHI']['Y']
                    else:
                        atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                    prevCifAtomId = None
                    prevOffset = None

                    for atomId, offset in zip(atomNames, seqOffset):

                        atomSelection = []

                        _cifSeqId = cifSeqId + offset
                        _cifCompId = cifCompId if offset == 0 else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)] if _cifSeqId in ps['auth_seq_id'] else None)

                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, _cifSeqId, self.__hasCoord)

                        if _cifCompId is None:
                            # """"
                            # try:
                            #     _cifCompId = ps['comp_id'][ps['auth_seq_id'].index(cifSeqId) + offset]
                            # except IndexError:
                            #     pass
                            # """
                            if _cifCompId is None:
                                self.__f.append(f"[Sequence mismatch warning] {self.__getCurrentRestraint()}"
                                                f"The residue number '{seqId+offset}' is not present in polymer sequence of chain {chainId} of the coordinates. "
                                                "Please update the sequence in the Macromolecules page.")
                                return
                                # _cifCompId = '.'
                            cifAtomId = atomId

                        else:
                            self.__ccU.updateChemCompDict(_cifCompId)

                            if isinstance(atomId, str):
                                cifAtomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == atomId), None)
                            else:
                                cifAtomIds = [cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList
                                              if atomId.match(cca[self.__ccU.ccaAtomId])
                                              and (coordAtomSite is None
                                                   or (coordAtomSite is not None and cca[self.__ccU.ccaAtomId] in coordAtomSite['atom_id']))]

                                if len(cifAtomIds) > 0:
                                    if prevCifAtomId is not None and offset == prevOffset:
                                        cifAtomId = next((_cifAtomId for _cifAtomId in cifAtomIds
                                                          if any(b for b in self.__ccU.lastBonds
                                                                 if ((b[self.__ccU.ccbAtomId1] == prevCifAtomId and b[self.__ccU.ccbAtomId2] == _cifAtomId)
                                                                     or (b[self.__ccU.ccbAtomId1] == _cifAtomId and b[self.__ccU.ccbAtomId2] == prevCifAtomId)))), None)
                                        if cifAtomId is None:
                                            offset -= 1
                                            _cifSeqId = cifSeqId + offset
                                            _cifCompId = cifCompId if offset == 0\
                                                else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)] if _cifSeqId in ps['auth_seq_id'] else None)
                                            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, _cifSeqId, self.__hasCoord)
                                            if coordAtomSite is not None:
                                                cifAtomId = next((_cifAtomId for _cifAtomId in cifAtomIds if _cifAtomId in coordAtomSite['atom_id']), None)

                                    else:
                                        cifAtomId = cifAtomIds[0]
                                else:
                                    cifAtomId = None

                            if cifAtomId is None:
                                self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                                f"{seqId+offset}:{_compId}:{atomId} involved in the {angleName} dihedral angle is not present in the coordinates.")
                                return

                        prevCifAtomId = cifAtomId
                        prevOffset = offset

                        atomSelection.append({'chain_id': chainId, 'seq_id': _cifSeqId, 'comp_id': _cifCompId, 'atom_id': cifAtomId})

                        self.testCoordAtomIdConsistency(chainId, _cifSeqId, _cifCompId, cifAtomId, seqKey, coordAtomSite, True)

                        if self.__hasCoord and coordAtomSite is None:
                            return

                        if len(atomSelection) > 0:
                            self.atomSelectionSet.append(atomSelection)

                    if len(self.atomSelectionSet) < 4:
                        return

                    if not self.areUniqueCoordAtoms('a Torsion angle'):
                        return

                    if self.__createSfDict:
                        sf = self.__getSf(potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                        sf['id'] += 1

                    for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                        self.atomSelectionSet[1],
                                                                        self.atomSelectionSet[2],
                                                                        self.atomSelectionSet[3]):
                        if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.__polySeq if self.__gapInAuthSeq else None):
                            continue
                        if peptide and angleName == 'CHI2' and atom4['atom_id'] == 'CD1' and isLikePheOrTyr(atom2['comp_id'], self.__ccU):
                            dstFunc = self.selectRealisticChi2AngleConstraint(atom1, atom2, atom3, atom4,
                                                                              dstFunc)
                        if self.__debug:
                            print(f"subtype={self.__cur_subtype} id={self.dihedRestraints} angleName={angleName} "
                                  f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                        if self.__createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                         '.', None, angleName,
                                         sf['list_id'], self.__entryId, dstFunc,
                                         self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                         atom1, atom2, atom3, atom4)
                            sf['loop'].add_data(row)

            # phase angle of pseudorotation
            else:

                atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)

                if not isinstance(atomId, str):
                    self.__ccU.updateChemCompDict(compId)
                    atomId = next(cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if atomId.match(cca[self.__ccU.ccaAtomId]))

                self.__retrieveLocalSeqScheme()

                chainAssign = self.assignCoordPolymerSequenceWithChainId(chainId, seqId, compId, atomId)

                if len(chainAssign) == 0:
                    self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                    f"{seqId}:{_compId} is not present in the coordinates.")
                    return

                for chainId, cifSeqId, cifCompId, _ in chainAssign:
                    ps = next(ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId)

                    peptide, nucleotide, carbohydrate = self.__csStat.getTypeOfCompId(cifCompId)

                    atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                    seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                    if nucleotide:
                        pass
                    else:
                        self.__f.append(f"[Insufficient angle selection] {self.__getCurrentRestraint()}"
                                        f"The angle identifier {str(ctx.Simple_name(2))!r} did not match with residue {_compId!r}.")
                        return

                    for atomId, offset in zip(atomNames, seqOffset):

                        atomSelection = []

                        _cifSeqId = cifSeqId + offset
                        _cifCompId = cifCompId if offset == 0 else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)] if _cifSeqId in ps['auth_seq_id'] else None)

                        if _cifCompId is None:
                            try:
                                _cifCompId = ps['comp_id'][ps['auth_seq_id'].index(cifSeqId) + offset]
                            except IndexError:
                                pass
                            if _cifCompId is None:
                                self.__f.append(f"[Sequence mismatch warning] {self.__getCurrentRestraint()}"
                                                f"The residue number '{seqId+offset}' is not present in polymer sequence of chain {chainId} of the coordinates. "
                                                "Please update the sequence in the Macromolecules page.")
                                return
                                # _cifCompId = '.'
                            cifAtomId = atomId

                        else:
                            self.__ccU.updateChemCompDict(_cifCompId)

                            cifAtomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == atomId), None)

                            if cifAtomId is None:
                                self.__f.append(f"[Atom not found] {self.__getCurrentRestraint()}"
                                                f"{seqId+offset}:{_compId}:{atomId} involved in the {angleName} dihedral angle is not present in the coordinates.")
                                return

                        atomSelection.append({'chain_id': chainId, 'seq_id': _cifSeqId, 'comp_id': _cifCompId, 'atom_id': cifAtomId})

                        if len(atomSelection) > 0:
                            self.atomSelectionSet.append(atomSelection)

                    if len(self.atomSelectionSet) < 5:
                        return

                    if not self.areUniqueCoordAtoms('a Torsion angle'):
                        return

                    if self.__createSfDict:
                        sf = self.__getSf(potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                        sf['id'] += 1

                    for atom1, atom2, atom3, atom4, atom5 in itertools.product(self.atomSelectionSet[0],
                                                                               self.atomSelectionSet[1],
                                                                               self.atomSelectionSet[2],
                                                                               self.atomSelectionSet[3],
                                                                               self.atomSelectionSet[4]):
                        if isLongRangeRestraint([atom1, atom2, atom3, atom4, atom5], self.__polySeq if self.__gapInAuthSeq else None):
                            continue
                        if self.__debug:
                            print(f"subtype={self.__cur_subtype} id={self.dihedRestraints} angleName={angleName} "
                                  f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} atom5={atom5} {dstFunc}")
                        if self.__createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                         '.', None, angleName,
                                         sf['list_id'], self.__entryId, dstFunc,
                                         self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                         None, None, None, None, atom5)
                            sf['loop'].add_data(row)

        except ValueError:
            self.dihedRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#cco_restraints.
    def enterCco_restraints(self, ctx: CyanaMRParser.Cco_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'jcoup'

        self.__cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#cco_restraints.
    def exitCco_restraints(self, ctx: CyanaMRParser.Cco_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#cco_restraint.
    def enterCco_restraint(self, ctx: CyanaMRParser.Cco_restraintContext):  # pylint: disable=unused-argument
        self.jcoupRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#cco_restraint.
    def exitCco_restraint(self, ctx: CyanaMRParser.Cco_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer()))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()
            atomId2 = str(ctx.Simple_name(2)).upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.jcoupRestraints -= 1
                return

            if atomId2 in KNOWN_ANGLE_NAMES:
                self.__cur_subtype_altered = True
                self.__cur_subtype = 'dihed'
                self.dihedRestraints += 1
                self.jcoupRestraints -= 1
                self.exitTorsion_angle_restraint(ctx)
                return

            target = self.numberSelection[0]
            error = None

            weight = 1.0
            if len(self.numberSelection) > 2:
                error = abs(self.numberSelection[1])
                weight = self.numberSelection[2]

            elif len(self.numberSelection) > 1:
                error = abs(self.numberSelection[1])

            if weight < 0.0:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The relative weight value of '{weight}' should be a positive value.")

            target_value = target
            lower_limit = target - error if error is not None else None
            upper_limit = target + error if error is not None else None

            dstFunc = self.validateRdcRange(weight, None, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequence(seqId1, compId1, atomId2)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId1, compId1, atomId2)

            if len(self.atomSelectionSet) < 2:
                return

            if not self.areUniqueCoordAtoms('a Scalar coupling'):
                return

            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
            comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
            comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Non-magnetic susceptible spin appears in scalar coupling constant; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if chain_id_1 != chain_id_2:
                ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Found inter-chain scalar coupling constant; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) > 1:

                if abs(seq_id_1 - seq_id_2) > 2 or {atom_id_1, atom_id_2} != {'H', 'N'}:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Found inter-residue scalar coupling constant; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) == 1:

                if self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                        ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                         or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')
                         or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 == 'H')
                         or (seq_id_1 > seq_id_2 and atom_id_1 == 'H' and atom_id_2.startswith('HA'))
                         or {atom_id_1, atom_id_2} == {'H', 'N'}):
                    pass

                else:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Found inter-residue scalar coupling constant; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif atom_id_1 == atom_id_2:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Found zero scalar coupling constant; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if self.__createSfDict:
                sf = self.__getSf()
                sf['id'] += 1

            for atom1, atom4 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if isLongRangeRestraint([atom1, atom4], self.__polySeq if self.__gapInAuthSeq else None):
                    if {atom1['atom_id'], atom4['atom_id']} != {'H', 'N'}:
                        continue
                self.__ccU.updateChemCompDict(atom1['comp_id'])
                atom2_can = self.__ccU.getBondedAtoms(atom1['comp_id'], atom1['atom_id'])
                atom3_can = self.__ccU.getBondedAtoms(atom1['comp_id'], atom4['atom_id'])
                atom_id_2 = atom_id_3 = None
                for ccb in self.__ccU.lastBonds:
                    if ccb[self.__ccU.ccbAtomId1] in atom2_can and ccb[self.__ccU.ccbAtomId2] in atom3_can:
                        atom_id_2 = ccb[self.__ccU.ccbAtomId1]
                        atom_id_3 = ccb[self.__ccU.ccbAtomId2]
                        break
                    if ccb[self.__ccU.ccbAtomId2] in atom2_can and ccb[self.__ccU.ccbAtomId1] in atom3_can:
                        atom_id_2 = ccb[self.__ccU.ccbAtomId2]
                        atom_id_3 = ccb[self.__ccU.ccbAtomId1]
                        break
                if atom_id_2 is None or atom_id_3 is None:
                    continue
                atom2 = copy.copy(atom1)
                atom2['atom_id'] = atom_id_2
                atom3 = copy.copy(atom4)
                atom3['atom_id'] = atom_id_3
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} id={self.jcoupRestraints} "
                          f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, None,
                                 sf['list_id'], self.__entryId, dstFunc,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom1, atom2, atom3, atom4)
                    sf['loop'].add_data(row)

        except ValueError:
            self.jcoupRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#ssbond_macro.
    def enterSsbond_macro(self, ctx: CyanaMRParser.Ssbond_macroContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'ssbond'
        self.__cur_dist_type = ''

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#ssbond_macro.
    def exitSsbond_macro(self, ctx: CyanaMRParser.Ssbond_macroContext):

        try:

            self.ssbondRestraints += 1

            try:
                _seqId1, _seqId2 = str(ctx.Ssbond_resids()).split('-')
                seqId1, seqId2 = int(_seqId1), int(_seqId2)
            except ValueError:
                self.ssbondRestraints -= 1
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            compId = 'CYSS'
            atomId = 'SG'

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId, atomId)
            chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId, atomId)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId, atomId)
            self.selectCoordAtoms(chainAssign2, seqId2, compId, atomId)

            if len(self.atomSelectionSet) < 2:
                return

            for atom1 in self.atomSelectionSet[0]:
                if atom1['comp_id'] != 'CYS':
                    self.__f.append(f"[Invalid atom selection] {self.__getCurrentRestraint()}"
                                    f"Failed to select a Cystein residue for disulfide bond between '{seqId1}' and '{seqId2}'.")
                    self.ssbondRestraints -= 1
                    return

            for atom2 in self.atomSelectionSet[1]:
                if atom2['comp_id'] != 'CYS':
                    self.__f.append(f"[Invalid atom selection] {self.__getCurrentRestraint()}"
                                    f"Failed to select a Cystein residue for disulfide bond between '{seqId1}' and '{seqId2}'.")
                    self.ssbondRestraints -= 1
                    return

            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

            try:

                _head =\
                    self.__cR.getDictListWithFilter('atom_site',
                                                    CARTN_DATA_ITEMS,
                                                    [{'name': self.__authAsymId, 'type': 'str', 'value': chain_id_1},
                                                     {'name': self.__authSeqId, 'type': 'int', 'value': seq_id_1},
                                                     {'name': self.__authAtomId, 'type': 'str', 'value': atom_id_1},
                                                     {'name': self.__modelNumName, 'type': 'int',
                                                      'value': self.__representativeModelId},
                                                     {'name': 'label_alt_id', 'type': 'enum',
                                                      'enum': ('A')}
                                                     ])

                _tail =\
                    self.__cR.getDictListWithFilter('atom_site',
                                                    CARTN_DATA_ITEMS,
                                                    [{'name': self.__authAsymId, 'type': 'str', 'value': chain_id_2},
                                                     {'name': self.__authSeqId, 'type': 'int', 'value': seq_id_2},
                                                     {'name': self.__authAtomId, 'type': 'str', 'value': atom_id_2},
                                                     {'name': self.__modelNumName, 'type': 'int',
                                                      'value': self.__representativeModelId},
                                                     {'name': 'label_alt_id', 'type': 'enum',
                                                      'enum': ('A')}
                                                     ])

                if len(_head) == 1 and len(_tail) == 1:
                    dist = distance(to_np_array(_head[0]), to_np_array(_tail[0]))
                    if dist > 2.5:
                        self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                        f"The distance of the disulfide bond linkage ({chain_id_1}:{seq_id_1}:{atom_id_1} - "
                                        f"{chain_id_2}:{seq_id_2}:{atom_id_2}) is too far apart in the coordinates ({dist:.3f}Å).")

            except Exception as e:
                if self.__verbose:
                    self.__lfh.write(f"+CyanaMRParserListener.exitSsbond_macro() ++ Error  - {str(e)}")

            if self.__createSfDict:
                sf = self.__getSf()
                sf['id'] += 1

            has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if isIdenticalRestraint([atom1, atom2]):
                    continue
                if has_intra_chain and (atom1['chain_id'] != atom2['chain_id'] or atom1['chain_id'] not in rep_chain_id_set):
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (CYANA macro: disulfide bond linkage) id={self.ssbondRestraints} "
                          f"atom1={atom1} atom2={atom2}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, None,
                                 sf['list_id'], self.__entryId, getDstFuncForSsBond(atom1, atom2),
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom1, atom2)
                    sf['loop'].add_data(row)

        finally:
            self.atomSelectionSet.clear()

    # Enter a parse tree produced by CyanaMRParser#hbond_macro.
    def enterHbond_macro(self, ctx: CyanaMRParser.Hbond_macroContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'hbond'
        self.__cur_dist_type = ''

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#hbond_macro.
    def exitHbond_macro(self, ctx: CyanaMRParser.Hbond_macroContext):

        try:

            self.hbondRestraints += 1

            seqId1 = int(str(ctx.Integer_HB(0)))
            seqId2 = int(str(ctx.Integer_HB(1)))
            atomId1 = str(ctx.Simple_name_HB(0))
            atomId2 = str(ctx.Simple_name_HB(1))

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId2, atomId2)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, None, atomId2)

            if len(self.atomSelectionSet) < 2:
                return

            if not self.areUniqueCoordAtoms('a hydrogen bond linkage'):
                return

            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

            try:

                _head =\
                    self.__cR.getDictListWithFilter('atom_site',
                                                    CARTN_DATA_ITEMS,
                                                    [{'name': self.__authAsymId, 'type': 'str', 'value': chain_id_1},
                                                     {'name': self.__authSeqId, 'type': 'int', 'value': seq_id_1},
                                                     {'name': self.__authAtomId, 'type': 'str', 'value': atom_id_1},
                                                     {'name': self.__modelNumName, 'type': 'int',
                                                      'value': self.__representativeModelId},
                                                     {'name': 'label_alt_id', 'type': 'enum',
                                                      'enum': ('A')}
                                                     ])

                _tail =\
                    self.__cR.getDictListWithFilter('atom_site',
                                                    CARTN_DATA_ITEMS,
                                                    [{'name': self.__authAsymId, 'type': 'str', 'value': chain_id_2},
                                                     {'name': self.__authSeqId, 'type': 'int', 'value': seq_id_2},
                                                     {'name': self.__authAtomId, 'type': 'str', 'value': atom_id_2},
                                                     {'name': self.__modelNumName, 'type': 'int',
                                                      'value': self.__representativeModelId},
                                                     {'name': 'label_alt_id', 'type': 'enum',
                                                      'enum': ('A')}
                                                     ])

                if len(_head) == 1 and len(_tail) == 1:
                    dist = distance(to_np_array(_head[0]), to_np_array(_tail[0]))
                    if dist > (3.4 if atom_id_1[0] not in protonBeginCode and atom_id_2[0] not in protonBeginCode else 2.4):
                        self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                        f"The distance of the hydrogen bond linkage ({chain_id_1}:{seq_id_1}:{atom_id_1} - "
                                        f"{chain_id_2}:{seq_id_2}:{atom_id_2}) is too far apart in the coordinates ({dist:.3f}Å).")

            except Exception as e:
                if self.__verbose:
                    self.__lfh.write(f"+CyanaMRParserListener.exitHbond_macro() ++ Error  - {str(e)}")

            if self.__createSfDict:
                sf = self.__getSf()
                sf['id'] += 1

            has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if isIdenticalRestraint([atom1, atom2]):
                    continue
                if has_intra_chain and (atom1['chain_id'] != atom2['chain_id'] or atom1['chain_id'] not in rep_chain_id_set):
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (CYANA macro: hydrogen bond linkage) id={self.hbondRestraints} "
                          f"atom1={atom1} atom2={atom2}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, None,
                                 sf['list_id'], self.__entryId, getDstFuncForHBond(atom1, atom2),
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom1, atom2)
                    sf['loop'].add_data(row)

        finally:
            self.atomSelectionSet.clear()

    # Enter a parse tree produced by CyanaMRParser#link_statement.
    def enterLink_statement(self, ctx: CyanaMRParser.Link_statementContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'geo'
        self.__cur_dist_type = ''

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#link_statement.
    def exitLink_statement(self, ctx: CyanaMRParser.Link_statementContext):

        try:

            self.geoRestraints += 1

            seqId1 = int(str(ctx.Integer(0)))
            seqId2 = int(str(ctx.Integer(1)))
            atomId1 = str(ctx.Simple_name(0))
            atomId2 = str(ctx.Simple_name(1))

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId2, atomId2)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            # circular shift
            if self.__reasons is not None and 'seq_id_remap' in self.__reasons and len(chainAssign1) == 1 and len(chainAssign2) == 1 and {atomId1, atomId2} == {'N', 'C'}:
                chainId1 = chainAssign1[0][0]
                chainId2 = chainAssign2[0][0]
                if chainId1 == chainId2:
                    seqIdDict = next((remap['seq_id_dict'] for remap in self.__reasons['seq_id_remap'] if remap['chain_id'] == chainId1), None)
                    if seqIdDict is not None:
                        seqIdDictKeys = seqIdDict.keys()
                        seqIdDictVals = seqIdDict.values()
                        minSeqId = min(seqIdDictKeys)
                        maxSeqId = max(seqIdDictKeys)
                        if {seqId1, seqId2} == {minSeqId, maxSeqId}:
                            _minSeqId = min(seqIdDictVals)
                            _maxSeqId = max(seqIdDictVals)
                            if seqId1 == minSeqId and atomId1 == 'N' and seqId2 == maxSeqId and atomId2 == 'C':
                                seqId1 = next(k for k, v in seqIdDict.items() if v == _minSeqId)
                                seqId2 = next(k for k, v in seqIdDict.items() if v == _maxSeqId)

                                chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)
                                chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId2, atomId2)

                            elif seqId2 == minSeqId and atomId2 == 'N' and seqId1 == maxSeqId and atomId1 == 'C':
                                seqId2 = next(k for k, v in seqIdDict.items() if v == _minSeqId)
                                seqId1 = next(k for k, v in seqIdDict.items() if v == _maxSeqId)

                                chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)
                                chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId2, atomId2)

            self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, None, atomId2)

            if len(self.atomSelectionSet) < 2:
                return

            if not self.areUniqueCoordAtoms('a covalent bond linkage'):
                return

            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

            try:

                _head =\
                    self.__cR.getDictListWithFilter('atom_site',
                                                    CARTN_DATA_ITEMS,
                                                    [{'name': self.__authAsymId, 'type': 'str', 'value': chain_id_1},
                                                     {'name': self.__authSeqId, 'type': 'int', 'value': seq_id_1},
                                                     {'name': self.__authAtomId, 'type': 'str', 'value': atom_id_1},
                                                     {'name': self.__modelNumName, 'type': 'int',
                                                      'value': self.__representativeModelId},
                                                     {'name': 'label_alt_id', 'type': 'enum',
                                                      'enum': ('A')}
                                                     ])

                _tail =\
                    self.__cR.getDictListWithFilter('atom_site',
                                                    CARTN_DATA_ITEMS,
                                                    [{'name': self.__authAsymId, 'type': 'str', 'value': chain_id_2},
                                                     {'name': self.__authSeqId, 'type': 'int', 'value': seq_id_2},
                                                     {'name': self.__authAtomId, 'type': 'str', 'value': atom_id_2},
                                                     {'name': self.__modelNumName, 'type': 'int',
                                                      'value': self.__representativeModelId},
                                                     {'name': 'label_alt_id', 'type': 'enum',
                                                      'enum': ('A')}
                                                     ])

                if len(_head) == 1 and len(_tail) == 1:
                    dist = distance(to_np_array(_head[0]), to_np_array(_tail[0]))
                    if dist > (3.5 if atom_id_1[0] not in protonBeginCode and atom_id_2[0] not in protonBeginCode else 2.5):
                        self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                        f"The distance of the covalent bond linkage ({chain_id_1}:{seq_id_1}:{atom_id_1} - "
                                        f"{chain_id_2}:{seq_id_2}:{atom_id_2}) is too far apart in the coordinates ({dist:.3f}Å).")

            except Exception as e:
                if self.__verbose:
                    self.__lfh.write(f"+CyanaMRParserListener.exitLink_statement() ++ Error  - {str(e)}")

            if self.__createSfDict:
                sf = self.__getSf('covalent bond linkage')
                sf['id'] += 1
                if len(sf['loop']['tags']) == 0:
                    sf['loop']['tags'] = ['index_id', 'id',
                                          'auth_asym_id_1', 'auth_seq_id_1', 'auth_comp_id_1', 'auth_atom_id_1',
                                          'auth_asym_id_2', 'auth_seq_id_2', 'auth_comp_id_2', 'auth_atom_id_2',
                                          'list_id', 'entry_id']

            has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if isIdenticalRestraint([atom1, atom2]):
                    continue
                if has_intra_chain and (atom1['chain_id'] != atom2['chain_id'] or atom1['chain_id'] not in rep_chain_id_set):
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (CYANA statement: covalent bond linkage) id={self.geoRestraints} "
                          f"atom1={atom1} atom2={atom2}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    sf['loop']['data'].append([sf['index_id'], sf['id'],
                                               atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                               atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id'],
                                               sf['list_id'], self.__entryId])

        finally:
            self.atomSelectionSet.clear()

    # Enter a parse tree produced by CyanaMRParser#stereoassign_macro.
    def enterStereoassign_macro(self, ctx: CyanaMRParser.Stereoassign_macroContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'fchiral'
        self.__cur_dist_type = ''

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#stereoassign_macro.
    def exitStereoassign_macro(self, ctx: CyanaMRParser.Stereoassign_macroContext):

        try:

            self.fchiralRestraints += 1

            _strip = str(ctx.Double_quote_string()).strip('"').strip()
            _split = re.sub(' +', ' ', _strip).split(' ')

            len_split = len(_split)

            if len_split < 2:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"Could not interpret '{str(ctx.Double_quote_string())}' as floating chiral stereo assignment.")
                return

            atomId1 = _split[0].upper()
            atomId2 = None

            if not atomId1.isalnum():
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"Could not interpret '{str(ctx.Double_quote_string())}' as floating chiral stereo assignment.")
                return

            if _split[1].isdecimal():
                seq_id_offset = 1
            else:
                seq_id_offset = 2
                atomId2 = _split[1].upper()

            for p in range(seq_id_offset, len_split):
                if not _split[p].isdecimal():
                    if len(_split[p]) > 1 and _split[p][1:].isdecimal():
                        continue
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    f"Could not interpret '{str(ctx.Double_quote_string())}' as floating chiral stereo assignment.")
                    return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            self.__retrieveLocalSeqScheme()

            seqId1 = int(_split[seq_id_offset] if _split[seq_id_offset][0].isdecimal() else _split[seq_id_offset][1:])

            chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)

            if atomId2 is not None:

                chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId2)

                if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId1, None, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if self.__createSfDict:
                    sf = self.__getSf()
                    sf['id'] += 1

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isIdenticalRestraint([atom1, atom2]):
                        continue
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} (CYANA macro: atom stereo) id={self.fchiralRestraints} "
                              f"atom1={atom1} atom2={atom2}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.__entryId, None,
                                     self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                     atom1, atom2)
                        sf['loop'].add_data(row)
                        break

                for p in range(seq_id_offset + 1, len_split):
                    self.atomSelectionSet.clear()

                    seqId1 = int(_split[p] if _split[p][0].isdecimal() else _split[p][1:])

                    chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)
                    chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId2)

                    if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId1, None, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                    for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                          self.atomSelectionSet[1]):
                        if isIdenticalRestraint([atom1, atom2]):
                            continue
                        if self.__debug:
                            print(f"subtype={self.__cur_subtype} (CYANA macro: atom stereo) id={self.fchiralRestraints} "
                                  f"atom1={atom1} atom2={atom2}")
                        if self.__createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                         '.', None, None,
                                         sf['list_id'], self.__entryId, None,
                                         self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                         atom1, atom2)
                            sf['loop'].add_data(row)
                            break

            else:

                if len(chainAssign1) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)

                if len(self.atomSelectionSet) < 1:
                    return

                comp_id = self.atomSelectionSet[0][0]['comp_id']
                atom_id = self.atomSelectionSet[0][0]['atom_id']

                atomId2 = self.__csStat.getGeminalAtom(comp_id, atom_id)

                if atomId2 is None:
                    return

                chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId2)

                if len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign2, seqId1, None, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if self.__createSfDict:
                    sf = self.__getSf()
                    sf['id'] += 1

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isIdenticalRestraint([atom1, atom2]):
                        continue
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} (CYANA macro: atom stereo) id={self.fchiralRestraints} "
                              f"atom1={atom1} atom2={atom2}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.__entryId, None,
                                     self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                     atom1, atom2)
                        sf['loop'].add_data(row)
                        break

                for p in range(seq_id_offset + 1, len_split):
                    self.atomSelectionSet.clear()

                    seqId1 = int(_split[p] if _split[p][0].isdecimal() else _split[p][1:])

                    chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)

                    if len(chainAssign1) == 0:
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)

                    if len(self.atomSelectionSet) < 1:
                        return

                    comp_id = self.atomSelectionSet[0][0]['comp_id']
                    atom_id = self.atomSelectionSet[0][0]['atom_id']

                    atomId2 = self.__csStat.getGeminalAtom(comp_id, atom_id)

                    if atomId2 is None:
                        return

                    chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId2)

                    if len(chainAssign2) == 0:
                        return

                    self.selectCoordAtoms(chainAssign2, seqId1, None, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                    for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                          self.atomSelectionSet[1]):
                        if isIdenticalRestraint([atom1, atom2]):
                            continue
                        if self.__debug:
                            print(f"subtype={self.__cur_subtype} (CYANA macro: atom stereo) id={self.fchiralRestraints} "
                                  f"atom1={atom1} atom2={atom2}")
                        if self.__createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                         '.', None, None,
                                         sf['list_id'], self.__entryId, None,
                                         self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                         atom1, atom2)
                            sf['loop'].add_data(row)
                            break

        finally:
            self.atomSelectionSet.clear()

    # Enter a parse tree produced by CyanaMRParser#declare_variable.
    def enterDeclare_variable(self, ctx: CyanaMRParser.Declare_variableContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#declare_variable.
    def exitDeclare_variable(self, ctx: CyanaMRParser.Declare_variableContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#set_variable.
    def enterSet_variable(self, ctx: CyanaMRParser.Set_variableContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#set_variable.
    def exitSet_variable(self, ctx: CyanaMRParser.Set_variableContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#unset_variable.
    def enterUnset_variable(self, ctx: CyanaMRParser.Unset_variableContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#unset_variable.
    def exitUnset_variable(self, ctx: CyanaMRParser.Unset_variableContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#print_macro.
    def enterPrint_macro(self, ctx: CyanaMRParser.Print_macroContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#print_macro.
    def exitPrint_macro(self, ctx: CyanaMRParser.Print_macroContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#unambig_atom_name_mapping.
    def enterUnambig_atom_name_mapping(self, ctx: CyanaMRParser.Unambig_atom_name_mappingContext):
        self.__cur_resname_for_mapping = str(ctx.Simple_name()).upper()

        self.__cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#unambig_atom_name_mapping.
    def exitUnambig_atom_name_mapping(self, ctx: CyanaMRParser.Unambig_atom_name_mappingContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#mapping_list.
    def enterMapping_list(self, ctx: CyanaMRParser.Mapping_listContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#mapping_list.
    def exitMapping_list(self, ctx: CyanaMRParser.Mapping_listContext):
        atomName = str(ctx.Simple_name_MP(0)).upper()
        iupacName = set()

        i = 1
        while ctx.Simple_name_MP(i):
            iupacName.add(str(ctx.Simple_name_MP(i)).upper())
            i += 1

        if self.__cur_resname_for_mapping not in self.unambigAtomNameMapping:
            self.unambigAtomNameMapping[self.__cur_resname_for_mapping] = {}
        self.unambigAtomNameMapping[self.__cur_resname_for_mapping][atomName] = list(iupacName)

    # Enter a parse tree produced by CyanaMRParser#ambig_atom_name_mapping.
    def enterAmbig_atom_name_mapping(self, ctx: CyanaMRParser.Ambig_atom_name_mappingContext):
        self.__cur_resname_for_mapping = str(ctx.Simple_name()).upper()

        self.__cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#ambig_atom_name_mapping.
    def exitAmbig_atom_name_mapping(self, ctx: CyanaMRParser.Ambig_atom_name_mappingContext):  # pylint: disable=unused-argument
        self.updateAmbigAtomNameMapping()

        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#ambig_list.
    def enterAmbig_list(self, ctx: CyanaMRParser.Ambig_listContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#ambig_list.
    def exitAmbig_list(self, ctx: CyanaMRParser.Ambig_listContext):
        if ctx.Ambig_code_MP():
            ambigCode = str(ctx.Ambig_code_MP())
            i = 0
        else:
            ambigCode = str(ctx.Simple_name_MP(0)).upper()
            i = 1

        mapName = []

        j = 0
        while ctx.Simple_name_MP(i):
            mapName.append({'atom_name': str(ctx.Simple_name_MP(i)).upper(),
                            'seq_id': int(str(ctx.Integer_MP(j)))})
            i += 1
            j += 1

        if self.__cur_resname_for_mapping not in self.ambigAtomNameMapping:
            self.ambigAtomNameMapping[self.__cur_resname_for_mapping] = {}
        self.ambigAtomNameMapping[self.__cur_resname_for_mapping][ambigCode] = mapName

    def updateAmbigAtomNameMapping(self):
        if (not self.__hasPolySeq and not self.__hasNonPolySeq) or len(self.ambigAtomNameMapping) == 0:
            return

        unambigResidues = None
        if len(self.unambigAtomNameMapping) > 0:
            unambigResidues = [translateToStdResName(residue, self.__ccU) for residue in self.unambigAtomNameMapping.keys()]

        for ambigDict in self.ambigAtomNameMapping.values():
            for ambigList in ambigDict.values():
                for ambig in ambigList:

                    if 'atom_id_list' in ambig:
                        continue

                    atomName = ambig['atom_name']
                    seqId = ambig['seq_id']

                    chainAssign = self.assignCoordPolymerSequenceWithoutCompId(seqId)

                    if len(chainAssign) == 0:
                        continue

                    ambig['atom_id_list'] = []

                    for cifChainId, cifSeqId, cifCompId, _ in chainAssign:

                        has_unambig = False

                        if unambigResidues is not None and cifCompId in unambigResidues:

                            unambigMap = next(v for k, v in self.unambigAtomNameMapping.items()
                                              if translateToStdResName(k, self.__ccU) == cifCompId)

                            if atomName in unambigMap:

                                for cifAtomId in unambigMap[atomName]:
                                    ambig['atom_id_list'].append({'chain_id': cifChainId,
                                                                  'seq_id': cifSeqId,
                                                                  'comp_id': cifCompId,
                                                                  'atom_id': cifAtomId})

                                has_unambig = True

                        if has_unambig:
                            continue

                        self.atomSelectionSet.clear()

                        self.selectCoordAtoms(chainAssign, seqId, None, ambig['atom_name'].upper(), enableWarning=False)

                        if len(self.atomSelectionSet[0]) > 0:
                            ambig['atom_id_list'].extend(self.atomSelectionSet[0])
                            continue

                        _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(cifCompId, atomName, leave_unmatched=True)
                        if details is not None and len(atomName) > 1:
                            _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(cifCompId, atomName[:-1], leave_unmatched=True)

                        if details is not None:
                            _atomId_ = translateToStdAtomName(atomName, cifCompId, ccU=self.__ccU)
                            if _atomId_ != atomName:
                                if atomName.startswith('HT') and len(_atomId_) == 2:
                                    _atomId_ = 'H'
                                _atomId = self.__nefT.get_valid_star_atom_in_xplor(cifCompId, _atomId_)[0]

                        for cifAtomId in _atomId:
                            ambig['atom_id_list'].append({'chain_id': cifChainId,
                                                          'seq_id': cifSeqId,
                                                          'comp_id': cifCompId,
                                                          'atom_id': cifAtomId})

                    ambig['atom_id_list'] = [dict(s) for s in set(frozenset(atom.items()) for atom in ambig['atom_id_list'])]

    def atomIdListToChainAssign(self, atomIdList):  # pylint: disable=no-self-use
        chainAssign = set()
        for item in atomIdList:
            if 'atom_id_list' in item:
                for atom_id in item['atom_id_list']:
                    chainAssign.add((atom_id['chain_id'], atom_id['seq_id'], atom_id['comp_id']))
        return list(chainAssign)

    def atomIdListToAtomSelection(self, atomIdList):  # pylint: disable=no-self-use
        atomSelection = []
        for item in atomIdList:
            if 'atom_id_list' in item:
                for atom_id in item['atom_id_list']:
                    if atom_id not in atomSelection:
                        atomSelection.append(atom_id)
        return atomSelection

    # Enter a parse tree produced by CyanaMRParser#number.
    def enterNumber(self, ctx: CyanaMRParser.NumberContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#number.
    def exitNumber(self, ctx: CyanaMRParser.NumberContext):
        if ctx.Float():
            self.numberSelection.append(float(str(ctx.Float())))

        elif ctx.Integer():
            self.numberSelection.append(float(str(ctx.Integer())))

        else:
            self.numberSelection.append(None)

    # Enter a parse tree produced by CyanaMRParser#gen_atom_name.
    def enterGen_atom_name(self, ctx: CyanaMRParser.Gen_atom_nameContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#gen_atom_name.
    def exitGen_atom_name(self, ctx: CyanaMRParser.Gen_atom_nameContext):
        if ctx.Simple_name():
            self.genAtomNameSelection.append(str(ctx.Simple_name()))

        elif ctx.Ambig_code():
            self.genAtomNameSelection.append(str(ctx.Ambig_code()))

        else:
            self.genAtomNameSelection.append(None)

    def __getCurrentRestraint(self):
        if self.__cur_subtype == 'dist':
            return f"[Check the {self.distRestraints}th row of distance restraints] "
        if self.__cur_subtype == 'dihed':
            return f"[Check the {self.dihedRestraints}th row of torsion angle restraints] "
        if self.__cur_subtype == 'rdc':
            return f"[Check the {self.rdcRestraints}th row of residual dipolar coupling restraints] "
        if self.__cur_subtype == 'pcs':
            return f"[Check the {self.pcsRestraints}th row of pseudocontact shift restraints] "
        if self.__cur_subtype == 'noepk':
            return f"[Check the {self.noepkRestraints}th row of NOESY volume restraints] "
        if self.__cur_subtype == 'jcoup':
            return f"[Check the {self.jcoupRestraints}th row of scalar coupling constant restraints] "
        if self.__cur_subtype == 'geo':
            return f"[Check the {self.geoRestraints}th row of coordinate geometry restraints] "
        if self.__cur_subtype == 'hbond':
            return f"[Check the {self.hbondRestraints}th row of hydrogen bond restraints] "
        if self.__cur_subtype == 'ssbond':
            return f"[Check the {self.ssbondRestraints}th row of disulfide bond restraints] "
        if self.__cur_subtype == 'fchiral':
            return f"[Check the {self.fchiralRestraints}th row of floating chiral stereo assignments] "
        return ''

    def __setLocalSeqScheme(self):
        if 'local_seq_scheme' not in self.reasonsForReParsing:
            self.reasonsForReParsing['local_seq_scheme'] = {}
        if self.__cur_subtype == 'dist':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.distRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'dihed':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.dihedRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'rdc':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.rdcRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'pcs':
            self.reasonsForReParsing['loca_seq_scheme'][(self.__cur_subtype, self.pcsRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'noepk':
            self.reasonsForReParsing['loca_seq_scheme'][(self.__cur_subtype, self.noepkRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'jcoup':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.jcoupRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'geo':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.geoRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'hbond':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.hbondRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'ssbond':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.ssbondRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'fchiral':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.fchiralRestraints)] = self.__preferAuthSeq
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
        elif self.__cur_subtype == 'rdc':
            key = (self.__cur_subtype, self.rdcRestraints)
        elif self.__cur_subtype == 'pcs':
            key = (self.__cur_subtype, self.pcsRestraints)
        elif self.__cur_subtype == 'noepk':
            key = (self.__cur_subtype, self.noepkRestraints)
        elif self.__cur_subtype == 'jcoup':
            key = (self.__cur_subtype, self.jcoupRestraints)
        elif self.__cur_subtype == 'geo':
            key = (self.__cur_subtype, self.geoRestraints)
        elif self.__cur_subtype == 'hbond':
            key = (self.__cur_subtype, self.hbondRestraints)
        elif self.__cur_subtype == 'ssbond':
            key = (self.__cur_subtype, self.ssbondRestraints)
        elif self.__cur_subtype == 'fchiral':
            key = (self.__cur_subtype, self.fchiralRestraints)
        else:
            return

        if key in self.__reasons['local_seq_scheme']:
            self.__preferAuthSeq = self.__reasons['local_seq_scheme'][key]

    def __addSf(self, constraintType=None, potentialType=None, rdcCode=None,
                orientationId=None, cyanaParameter=None):
        content_subtype = contentSubtypeOf(self.__cur_subtype)

        if content_subtype is None:
            return

        self.__cur_constraint_type = constraintType

        self.__listIdCounter = incListIdCounter(self.__cur_subtype, self.__listIdCounter)

        key = (self.__cur_subtype, constraintType, potentialType, rdcCode, orientationId)

        if key not in self.sfDict:
            self.sfDict[key] = []

        list_id = self.__listIdCounter[content_subtype]

        restraint_name = getRestraintName(self.__cur_subtype)

        sf_framecode = 'CYANA_' + restraint_name.replace(' ', '_') + f'_{list_id}'

        sf = getSaveframe(self.__cur_subtype, sf_framecode, list_id, self.__entryId, self.__originalFileName,
                          constraintType=constraintType, potentialType=potentialType, rdcCode=rdcCode,
                          cyanaParameter=cyanaParameter)

        not_valid = True

        lp = getLoop(self.__cur_subtype, hasInsCode=self.__authToInsCode is not None)
        if not isinstance(lp, dict):
            sf.add_loop(lp)
            not_valid = False

        _restraint_name = restraint_name.split()
        if _restraint_name[-1] == 'assignments':
            _restraint_name.append('dummy')  # to preserve 'floating chiral stereo assignments'

        item = {'file_type': self.__file_type, 'saveframe': sf, 'loop': lp, 'list_id': list_id,
                'id': 0, 'index_id': 0,
                'constraint_type': ' '.join(_restraint_name[:-1])}

        if not_valid:
            item['tags'] = []

        if self.__cur_subtype == 'dist':
            item['constraint_subsubtype'] = 'simple'

        self.__lastSfDict[self.__cur_subtype] = item

        self.sfDict[key].append(item)

    def __getSf(self, constraintType=None, potentialType=None, rdcCode=None,
                orientationId=None, cyanaParameter=None):
        key = (self.__cur_subtype, constraintType, potentialType, rdcCode, orientationId)

        if key not in self.sfDict:
            replaced = False
            if potentialType is not None or rdcCode is not None or orientationId is not None:
                old_key = (self.__cur_subtype, self.__cur_constraint_type, None, None, orientationId)
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
                    if rdcCode is not None:
                        idx = next((idx for idx, t in enumerate(sf.tags) if t[0] == 'Details'), -1)
                        if idx != -1:
                            sf.tags[idx][1] = rdcCode
                        else:
                            sf.add_tag('Details', rdcCode)
            if not replaced:
                self.__addSf(constraintType=constraintType, potentialType=potentialType, rdcCode=rdcCode,
                             orientationId=orientationId, cyanaParameter=cyanaParameter)

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
        """ Return content subtype of CYANA MR file.
        """

        contentSubtype = {'dist_restraint': self.distRestraints,
                          'dihed_restraint': self.dihedRestraints,
                          'rdc_restraint': self.rdcRestraints,
                          'pcs_restraint': self.pcsRestraints,
                          'noepk_restraint': self.noepkRestraints,
                          'jcoup_restraint': self.jcoupRestraints,
                          'geo_restraint': self.geoRestraints,
                          'hbond_restraint': self.hbondRestraints,
                          'ssbond_restraint': self.ssbondRestraints,
                          'fchiral_restraint': self.fchiralRestraints
                          }

        return {k: 1 for k, v in contentSubtype.items() if v > 0}

    def getEffectiveContentSubtype(self):
        """ Return effective content subtype of CYANA MR file (excluding .upv, lov, and .cco).
        """

        contentSubtype = {'dist_restraint': self.distRestraints,
                          'dihed_restraint': self.dihedRestraints,
                          'rdc_restraint': self.rdcRestraints,
                          'pcs_restraint': self.pcsRestraints
                          }

        return {k: 1 for k, v in contentSubtype.items() if v > 0}

    def getPolymerSequence(self):
        """ Return polymer sequence of CYANA MR file.
        """
        return None if self.__polySeqRst is None or len(self.__polySeqRst) == 0 else self.__polySeqRst

    def getSequenceAlignment(self):
        """ Return sequence alignment between coordinates and CYANA MR.
        """
        return None if self.__seqAlign is None or len(self.__seqAlign) == 0 else self.__seqAlign

    def getChainAssignment(self):
        """ Return chain assignment between coordinates and CYANA MR.
        """
        return None if self.__chainAssign is None or len(self.__chainAssign) == 0 else self.__chainAssign

    def getReasonsForReparsing(self):
        """ Return reasons for re-parsing CYANA MR file.
        """
        return None if len(self.reasonsForReParsing) == 0 else self.reasonsForReParsing

    def getTypeOfDistanceRestraints(self):
        """ Return type of distance restraints of the CYANA MR file.
        """
        if self.__file_ext is not None:
            if self.__file_ext in ('upl', 'lol'):
                return self.__file_ext

        if len(self.__local_dist_types) > 0:
            if 'upl' in self.__local_dist_types and 'lol' not in self.__local_dist_types:
                return 'upl'
            if 'lol' in self.__local_dist_types and 'upl' not in self.__local_dist_types:
                return 'lol'
            return 'both'

        if self.__max_dist_value == DIST_ERROR_MIN:
            return ''

        if self.__max_dist_value > 3.5 and self.__min_dist_value > 2.7:
            return 'upl'
        if self.__max_dist_value < 2.7:
            return 'lol'

        return 'both'

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

# del CyanaMRParser
