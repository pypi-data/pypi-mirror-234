##
# File: XplorMRParserListener.py
# Date: 09-Feb-2022
#
# Updates:
""" ParserLister class for XPLOR-NIH MR files.
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
    from wwpdb.utils.nmr.mr.XplorMRParser import XplorMRParser
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (toRegEx, toNefEx,
                                                       coordAssemblyChecker,
                                                       extendCoordChainsForExactNoes,
                                                       translateToStdResName,
                                                       translateToStdAtomName,
                                                       hasInterChainRestraint,
                                                       isIdenticalRestraint,
                                                       isLongRangeRestraint,
                                                       isAsymmetricRangeRestraint,
                                                       isAmbigAtomSelection,
                                                       getAltProtonIdInBondConstraint,
                                                       getTypeOfDihedralRestraint,
                                                       isLikePheOrTyr,
                                                       getRdcCode,
                                                       isCyclicPolymer,
                                                       getRestraintName,
                                                       contentSubtypeOf,
                                                       incListIdCounter,
                                                       decListIdCounter,
                                                       getSaveframe,
                                                       getLoop,
                                                       getAuxLoops,
                                                       getRow,
                                                       getAuxRow,
                                                       getDistConstraintType,
                                                       getPotentialType,
                                                       getDstFuncForHBond,
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
                                                       CSA_RESTRAINT_RANGE,
                                                       CSA_RESTRAINT_ERROR,
                                                       PCS_RESTRAINT_RANGE,
                                                       PCS_RESTRAINT_ERROR,
                                                       CCR_RESTRAINT_RANGE,
                                                       CCR_RESTRAINT_ERROR,
                                                       PRE_RESTRAINT_RANGE,
                                                       PRE_RESTRAINT_ERROR,
                                                       CS_RESTRAINT_RANGE,
                                                       CS_RESTRAINT_ERROR,
                                                       T1T2_RESTRAINT_RANGE,
                                                       T1T2_RESTRAINT_ERROR,
                                                       PROBABILITY_RANGE,
                                                       DIST_AMBIG_LOW,
                                                       DIST_AMBIG_UP,
                                                       DIST_AMBIG_MED,
                                                       DIST_AMBIG_UNCERT,
                                                       XPLOR_RDC_PRINCIPAL_AXIS_NAMES,
                                                       XPLOR_NITROXIDE_NAMES,
                                                       XPLOR_ORIGIN_AXIS_COLS,
                                                       CARTN_DATA_ITEMS,
                                                       AUTH_ATOM_DATA_ITEMS,
                                                       ATOM_NAME_DATA_ITEMS,
                                                       AUTH_ATOM_CARTN_DATA_ITEMS,
                                                       PTNR1_AUTH_ATOM_DATA_ITEMS,
                                                       PTNR2_AUTH_ATOM_DATA_ITEMS)
    from wwpdb.utils.nmr.ChemCompUtil import ChemCompUtil
    from wwpdb.utils.nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from wwpdb.utils.nmr.NEFTranslator.NEFTranslator import (NEFTranslator,
                                                             PARAMAGNETIC_ELEMENTS,
                                                             FERROMAGNETIC_ELEMENTS,
                                                             LANTHANOID_ELEMENTS)
    from wwpdb.utils.nmr.AlignUtil import (LEN_LARGE_ASYM_ID,
                                           LARGE_ASYM_ID,
                                           MAX_MAG_IDENT_ASYM_ID,
                                           monDict3,
                                           protonBeginCode,
                                           aminoProtonCode,
                                           jcoupBbPairCode,
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
    from nmr.mr.XplorMRParser import XplorMRParser
    from nmr.mr.ParserListenerUtil import (toRegEx, toNefEx,
                                           coordAssemblyChecker,
                                           extendCoordChainsForExactNoes,
                                           translateToStdResName,
                                           translateToStdAtomName,
                                           hasInterChainRestraint,
                                           isIdenticalRestraint,
                                           isLongRangeRestraint,
                                           isAsymmetricRangeRestraint,
                                           isAmbigAtomSelection,
                                           getAltProtonIdInBondConstraint,
                                           getTypeOfDihedralRestraint,
                                           isLikePheOrTyr,
                                           getRdcCode,
                                           isCyclicPolymer,
                                           getRestraintName,
                                           contentSubtypeOf,
                                           incListIdCounter,
                                           decListIdCounter,
                                           getSaveframe,
                                           getLoop,
                                           getAuxLoops,
                                           getRow,
                                           getAuxRow,
                                           getDistConstraintType,
                                           getPotentialType,
                                           getDstFuncForHBond,
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
                                           CSA_RESTRAINT_RANGE,
                                           CSA_RESTRAINT_ERROR,
                                           PCS_RESTRAINT_RANGE,
                                           PCS_RESTRAINT_ERROR,
                                           CCR_RESTRAINT_RANGE,
                                           CCR_RESTRAINT_ERROR,
                                           PRE_RESTRAINT_RANGE,
                                           PRE_RESTRAINT_ERROR,
                                           CS_RESTRAINT_RANGE,
                                           CS_RESTRAINT_ERROR,
                                           T1T2_RESTRAINT_RANGE,
                                           T1T2_RESTRAINT_ERROR,
                                           PROBABILITY_RANGE,
                                           DIST_AMBIG_LOW,
                                           DIST_AMBIG_UP,
                                           DIST_AMBIG_MED,
                                           DIST_AMBIG_UNCERT,
                                           XPLOR_RDC_PRINCIPAL_AXIS_NAMES,
                                           XPLOR_NITROXIDE_NAMES,
                                           XPLOR_ORIGIN_AXIS_COLS,
                                           CARTN_DATA_ITEMS,
                                           AUTH_ATOM_DATA_ITEMS,
                                           ATOM_NAME_DATA_ITEMS,
                                           AUTH_ATOM_CARTN_DATA_ITEMS,
                                           PTNR1_AUTH_ATOM_DATA_ITEMS,
                                           PTNR2_AUTH_ATOM_DATA_ITEMS)
    from nmr.ChemCompUtil import ChemCompUtil
    from nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from nmr.NEFTranslator.NEFTranslator import (NEFTranslator,
                                                 PARAMAGNETIC_ELEMENTS,
                                                 FERROMAGNETIC_ELEMENTS,
                                                 LANTHANOID_ELEMENTS)
    from nmr.AlignUtil import (LEN_LARGE_ASYM_ID,
                               LARGE_ASYM_ID,
                               MAX_MAG_IDENT_ASYM_ID,
                               monDict3,
                               protonBeginCode,
                               aminoProtonCode,
                               jcoupBbPairCode,
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


CSA_RANGE_MIN = CSA_RESTRAINT_RANGE['min_inclusive']
CSA_RANGE_MAX = CSA_RESTRAINT_RANGE['max_inclusive']

CSA_ERROR_MIN = CSA_RESTRAINT_ERROR['min_exclusive']
CSA_ERROR_MAX = CSA_RESTRAINT_ERROR['max_exclusive']


PCS_RANGE_MIN = PCS_RESTRAINT_RANGE['min_inclusive']
PCS_RANGE_MAX = PCS_RESTRAINT_RANGE['max_inclusive']

PCS_ERROR_MIN = PCS_RESTRAINT_ERROR['min_exclusive']
PCS_ERROR_MAX = PCS_RESTRAINT_ERROR['max_exclusive']


CCR_RANGE_MIN = CCR_RESTRAINT_RANGE['min_inclusive']
CCR_RANGE_MAX = CCR_RESTRAINT_RANGE['max_inclusive']

CCR_ERROR_MIN = CCR_RESTRAINT_ERROR['min_exclusive']
CCR_ERROR_MAX = CCR_RESTRAINT_ERROR['max_exclusive']


PRE_RANGE_MIN = PRE_RESTRAINT_RANGE['min_inclusive']
PRE_RANGE_MAX = PRE_RESTRAINT_RANGE['max_inclusive']

PRE_ERROR_MIN = PRE_RESTRAINT_ERROR['min_exclusive']
PRE_ERROR_MAX = PRE_RESTRAINT_ERROR['max_exclusive']


CS_RANGE_MIN = CS_RESTRAINT_RANGE['min_inclusive']
CS_RANGE_MAX = CS_RESTRAINT_RANGE['max_inclusive']

CS_ERROR_MIN = CS_RESTRAINT_ERROR['min_exclusive']
CS_ERROR_MAX = CS_RESTRAINT_ERROR['max_exclusive']


T1T2_RANGE_MIN = T1T2_RESTRAINT_RANGE['min_inclusive']
T1T2_RANGE_MAX = T1T2_RESTRAINT_RANGE['max_inclusive']

T1T2_ERROR_MIN = T1T2_RESTRAINT_ERROR['min_exclusive']
T1T2_ERROR_MAX = T1T2_RESTRAINT_ERROR['max_exclusive']


# This class defines a complete listener for a parse tree produced by XplorMRParser.
class XplorMRParserListener(ParseTreeListener):

    __file_type = 'nm-res-xpl'

    __verbose = None
    __lfh = None
    __debug = False
    __remediate = False
    __sel_expr_debug = False

    __createSfDict = True
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
    # auth_asym_id of fibril like polymer (exptl methods should contain SOLID-STATE NMR, ELECTRON MICROSCOPY)
    __fibril_chain_ids = []

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

    # large model
    __largeModel = False
    __representativeAsymId = 'A'

    # polymer sequence of MR file
    __polySeqRst = None

    __seqAlign = None
    __chainAssign = None

    # current restraint subtype
    __cur_subtype = ''
    __cur_subtype_altered = False
    __with_axis = False
    __with_para = False
    __in_block = False
    __cur_auth_atom_id = ''

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
    noePotential = 'biharmonic'
    noeAverage = 'r-6'
    squareExponent = 2.0
    softExponent = 2.0
    squareConstant = 20.0
    squareOffset = 0.0
    rSwitch = 10.0
    scale = 1.0
    asymptote = 0.0
    B_high = 0.01
    ceiling = 30.0
    temperature = 300.0
    monomers = 1
    ncount = 2
    scale_a = None
    adistExpectGrid = None
    adistExpectValue = 0.0
    adistSizeMaxDist = 10.0
    adistSizeStep = None
    adistForceConst = 1.0
    symmTarget = None
    symmDminus = None
    symmDplus = None

    # 3D vectors in point clause
    inVector3D = False
    inVector3D_columnSel = -1
    inVector3D_tail = None
    inVector3D_head = None
    vector3D = None

    # RDC
    potential = 'square'
    average = 'sum'

    # CSA
    csaType = None
    csaSigma = None

    # PRE
    preParameterDict = None

    # CS
    csExpect = None

    # planarity
    planeWeight = 300.0

    # NCS
    ncsSigb = 2.0
    ncsWeight = 300.0

    # Rama
    ramaScale = 1.0
    ramaCutoff = None
    ramaForceConst = 1.0
    ramaShape = None
    ramaSize = None
    ramaPhase = None
    ramaGaussian = None
    ramaQuartic = None

    # radius of gyration
    radiScale = 1.0

    # diffusion
    diffCoef = None
    diffForceConst = 1.0
    diffPotential = None
    diffType = None

    # orientation database
    nbaseCutoff = None
    nbaseHeight = None
    nbaseForceConst = 1.0
    nbaseGaussian = None
    nbaseMaxGauss = None
    nbaseNewGauss = None
    nbaseQuartic = None
    nbaseResidues = None
    nbaseCubicSize = None

    # paramagnetic orientation
    pangForceConst = 1.0

    # generic statements
    classification = None
    coefficients = None

    # collection of atom selection
    atomSelectionSet = []

    # factor of paramagnetic center
    paramagCenter = None

    # collection of number selection
    numberSelection = []

    # collection of number selection in factor
    numberFSelection = []

    # store[1-9]
    storeSet = {i: [] for i in range(1, 10)}

    # vector mode: do
    vectorDo = {}

    # evaluate
    evaluate = {}

    # control
    evaluateFor = {}

    # Hydrogen bond database restraint
    donor_columnSel = -1
    acceptor_columnSel = -1

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

    # current constraint type
    __cur_constraint_type = None

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

            exptl = cR.getDictList('exptl')
            if len(exptl) > 0:
                for item in exptl:
                    if 'method' in item:
                        if 'NMR' in item['method']:
                            self.__exptlMethod = item['method']
                            break
                if self.__exptlMethod == 'SOLID-STATE NMR' and len(self.__polySeq) >= 8:
                    fibril_chain_ids = []
                    for item in exptl:
                        if 'method' in item:
                            if item['method'] == 'ELECTRON MICROSCOPY':
                                for ps in self.__polySeq:
                                    if 'identical_chain_id' in ps:
                                        fibril_chain_ids.append(ps['auth_chain_id'])
                                        fibril_chain_ids.extend(ps['identical_chain_id'])
                    if len(fibril_chain_ids) > 0:
                        self.__fibril_chain_ids = list(set(fibril_chain_ids))

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

        self.distRestraints = 0      # XPLOR-NIH: Distance restraints
        self.dihedRestraints = 0     # XPLOR-NIH: Dihedral angle restraints
        self.rdcRestraints = 0       # XPLOR-NIH: Residual dipolar coupling restraints
        self.planeRestraints = 0     # XPLOR-NIH: Planarity restraints
        self.adistRestraints = 0     # XPLOR-NIH: Antidiatance restraints
        self.jcoupRestraints = 0     # XPLOR-NIH: Scalar J-coupling restraints
        self.hvycsRestraints = 0     # XPLOR-NIH: Carbon chemical shift restraints
        self.procsRestraints = 0     # XPLOR-NIH: Proton chemical shift restraints
        self.ramaRestraints = 0      # XPLOR-NIH: Dihedral angle database restraints
        self.radiRestraints = 0      # XPLOR-NIH: Radius of gyration restraints
        self.diffRestraints = 0      # XPLOR-NIH: Diffusion anisotropy restraints
        self.nbaseRestraints = 0     # XPLOR-NIH: Residue-residue position/orientation database restraints
        self.csaRestraints = 0       # XPLOR-NIH: (Pseudo) Chemical shift anisotropy restraints
        # self.angRestraints = 0       # XPLOR-NIH: Angle database restraints
        self.preRestraints = 0       # XPLOR-NIH: Paramagnetic relaxation enhancement restraints
        self.pcsRestraints = 0       # XPLOR-NIH: Paramagnetic pseudocontact shift restraints
        self.prdcRestraints = 0      # XPLOR-NIH: Paramagnetic residual dipolar coupling restraints
        self.pangRestraints = 0      # XPLOR-NIH: Paramagnetic orientation restraints
        self.pccrRestraints = 0      # XPLOR-NIH: Paramagnetic cross-correlation rate restraints
        self.hbondRestraints = 0     # XPLOR-NIH: Hydrogen bond geometry/database restraints
        self.geoRestraints = 0       # XPLOR-NIH: Harmonic coordinate/NCS restraints

        self.distStatements = 0      # XPLOR-NIH: Distance statements
        self.dihedStatements = 0     # XPLOR-NIH: Dihedral angle statements
        self.rdcStatements = 0       # XPLOR-NIH: Residual dipolar coupling statements
        self.planeStatements = 0     # XPLOR-NIH: Planarity statements
        self.adistStatements = 0     # XPLOR-NIH: Antidiatance statements
        self.jcoupStatements = 0     # XPLOR-NIH: Scalar J-coupling statements
        self.hvycsStatements = 0     # XPLOR-NIH: Carbon chemical shift statements
        self.procsStatements = 0     # XPLOR-NIH: Proton chemical shift statements
        self.ramaStatements = 0      # XPLOR-NIH: Dihedral angle database statements
        self.radiStatements = 0      # XPLOR-NIH: Radius of gyration statements
        self.diffStatements = 0      # XPLOR-NIH: Diffusion anisotropy statements
        self.nbaseStatements = 0     # XPLOR-NIH: Residue-residue position/orientation database statements
        self.csaStatements = 0       # XPLOR-NIH: (Pseudo) Chemical shift anisotropy statements
        # self.angStatements = 0       # XPLOR-NIH: Angle database statements
        self.preStatements = 0       # XPLOR-NIH: Paramagnetic relaxation enhancement statements
        self.pcsStatements = 0       # XPLOR-NIH: Paramagnetic pseudocontact shift statements
        self.prdcStatements = 0      # XPLOR-NIH: Paramagnetic residual dipolar coupling statements
        self.pangStatements = 0      # XPLOR-NIH: Paramagnetic orientation statements
        self.pccrStatements = 0      # XPLOR-NIH: Paramagnetic cross-correlation rate statements
        self.hbondStatements = 0     # XPLOR-NIH: Hydrogen bond geometry/database statements
        self.geoStatements = 0       # XPLOR-NIH: Harmonic coordinate/NCS restraints

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

    # Enter a parse tree produced by XplorMRParser#xplor_nih_mr.
    def enterXplor_nih_mr(self, ctx: XplorMRParser.Xplor_nih_mrContext):  # pylint: disable=unused-argument
        self.__polySeqRst = []
        self.__f = []
        self.__g = []

    # Exit a parse tree produced by XplorMRParser#xplor_nih_mr.
    def exitXplor_nih_mr(self, ctx: XplorMRParser.Xplor_nih_mrContext):  # pylint: disable=unused-argument

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

    # Enter a parse tree produced by XplorMRParser#distance_restraint.
    def enterDistance_restraint(self, ctx: XplorMRParser.Distance_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.distStatements += 1
        self.__cur_subtype = 'dist'

        self.noePotential = 'biharmonic'  # default potential
        self.noeAverage = 'r-6'  # default averaging method
        self.squareExponent = 2.0
        self.softExponent = 2.0
        self.squareConstant = 20.0
        self.squareOffset = 0.0
        self.rSwitch = 10.0
        self.scale = 1.0
        self.asymptote = 0.0
        self.B_high = 0.01
        self.ceiling = 30.0
        self.temperature = 300.0
        self.monomers = 1
        self.ncount = 2
        self.symmTarget = None
        self.symmDminus = None
        self.symmDplus = None

        if self.__createSfDict:
            self.__addSf()

    # Exit a parse tree produced by XplorMRParser#distance_restraint.
    def exitDistance_restraint(self, ctx: XplorMRParser.Distance_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict and self.__cur_subtype == 'dist':

            if self.__cur_subtype not in self.__lastSfDict:
                return

            sf = self.__lastSfDict[self.__cur_subtype]

            if 'aux_loops' in sf:
                return

            sf['aux_loops'] = getAuxLoops(self.__cur_subtype)

            aux_lp = next((aux_lp for aux_lp in sf['aux_loops'] if aux_lp.category == '_Gen_dist_constraint_software_param'), None)

            if aux_lp is None:
                return

            aux_lp.add_data(getAuxRow(self.__cur_subtype, aux_lp.category, sf['list_id'], self.__entryId,
                                      {'Type': 'class name', 'Value': self.classification}))
            aux_lp.add_data(getAuxRow(self.__cur_subtype, aux_lp.category, sf['list_id'], self.__entryId,
                                      {'Type': 'potential function', 'Value': self.noePotential}))
            aux_lp.add_data(getAuxRow(self.__cur_subtype, aux_lp.category, sf['list_id'], self.__entryId,
                                      {'Type': 'averaging method', 'Value': self.noeAverage}))
            aux_lp.add_data(getAuxRow(self.__cur_subtype, aux_lp.category, sf['list_id'], self.__entryId,
                                      {'Type': 'scaling constant', 'Value': self.scale}))
            aux_lp.add_data(getAuxRow(self.__cur_subtype, aux_lp.category, sf['list_id'], self.__entryId,
                                      {'Type': 'ceiling', 'Value': self.ceiling}))
            if self.noePotential in ('square', 'softsquare'):
                aux_lp.add_data(getAuxRow(self.__cur_subtype, aux_lp.category, sf['list_id'], self.__entryId,
                                          {'Type': 'exponent', 'Value': self.squareExponent}))
            if self.noePotential == 'softsquare':
                aux_lp.add_data(getAuxRow(self.__cur_subtype, aux_lp.category, sf['list_id'], self.__entryId,
                                          {'Type': 'soft exponent', 'Value': self.softExponent}))
            if self.noePotential in ('square', 'softsquare'):
                aux_lp.add_data(getAuxRow(self.__cur_subtype, aux_lp.category, sf['list_id'], self.__entryId,
                                          {'Type': 'auxiliary scaling constant', 'Value': self.squareConstant}))
            if self.noePotential in ('square', 'softsquare'):
                aux_lp.add_data(getAuxRow(self.__cur_subtype, aux_lp.category, sf['list_id'], self.__entryId,
                                          {'Type': 'negative offset', 'Value': self.squareOffset}))
            if self.noePotential == 'softsquare':
                aux_lp.add_data(getAuxRow(self.__cur_subtype, aux_lp.category, sf['list_id'], self.__entryId,
                                          {'Type': 'switch distance', 'Value': self.rSwitch}))
            if self.noePotential == 'softsquare':
                aux_lp.add_data(getAuxRow(self.__cur_subtype, aux_lp.category, sf['list_id'], self.__entryId,
                                          {'Type': 'asymptote slope', 'Value': self.asymptote}))
            if self.noePotential == 'high':
                aux_lp.add_data(getAuxRow(self.__cur_subtype, aux_lp.category, sf['list_id'], self.__entryId,
                                          {'Type': 'B_high', 'Value': self.B_high}))
            if self.noePotential == 'biharmonic':
                aux_lp.add_data(getAuxRow(self.__cur_subtype, aux_lp.category, sf['list_id'], self.__entryId,
                                          {'Type': 'temperature', 'Value': self.temperature}))
            if self.noeAverage == 'sum':
                aux_lp.add_data(getAuxRow(self.__cur_subtype, aux_lp.category, sf['list_id'], self.__entryId,
                                          {'Type': 'number monomers', 'Value': self.monomers}))
            if self.noePotential == 'high':
                aux_lp.add_data(getAuxRow(self.__cur_subtype, aux_lp.category, sf['list_id'], self.__entryId,
                                          {'Type': 'number assign statements', 'Value': self.ncount}))

            sf['saveframe'].add_loop(aux_lp)

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#dihedral_angle_restraint.
    def enterDihedral_angle_restraint(self, ctx: XplorMRParser.Dihedral_angle_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.dihedStatements += 1
        self.__cur_subtype = 'dihed'

        self.scale = 1.0

        if self.__createSfDict:
            self.__addSf()

    # Exit a parse tree produced by XplorMRParser#dihedral_angle_restraint.
    def exitDihedral_angle_restraint(self, ctx: XplorMRParser.Dihedral_angle_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#rdc_restraint.
    def enterRdc_restraint(self, ctx: XplorMRParser.Rdc_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.rdcStatements += 1
        self.__cur_subtype = 'rdc'

        self.potential = 'square'  # default potential
        self.scale = 1.0

        if self.__createSfDict:
            if ctx.VeAngle() or ctx.Anisotropy():
                self.__cur_subtype = 'dihed'
                self.__addSf('intervector projection angle')
                self.__cur_subtype = 'rdc'
            else:
                self.__addSf()

    # Exit a parse tree produced by XplorMRParser#rdc_restraint.
    def exitRdc_restraint(self, ctx: XplorMRParser.Rdc_restraintContext):
        self.__in_block = False

        if self.__createSfDict:
            if ctx.VeAngle() or ctx.Anisotropy():
                self.__cur_subtype = 'dihed'
                if self.__createSfDict and self.__cur_subtype not in self.__lastSfDict and self.__lastSfDict[self.__cur_subtype]['id'] == 0:
                    self.__trimSfWoLp()
                    self.__cur_subtype = 'rdc'
            else:
                self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#planar_restraint.
    def enterPlanar_restraint(self, ctx: XplorMRParser.Planar_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.planeStatements += 1
        self.__cur_subtype = 'plane'

        if self.__createSfDict:
            software_name = 'XPLOR-NIH/CNS' if self.__remediate else 'XPLOR-NIH'
            self.__addSf(f'planarity restraint, {software_name} PLANAR/GROUP statement')

    # Exit a parse tree produced by XplorMRParser#planar_restraint.
    def exitPlanar_restraint(self, ctx: XplorMRParser.Planar_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#harmonic_restraint.
    def enterHarmonic_restraint(self, ctx: XplorMRParser.Harmonic_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.geoStatements += 1
        self.__cur_subtype = 'geo'

        self.squareExponent = 2.0
        self.vector3D = [0.0] * 3

        if self.__createSfDict:
            software_name = 'XPLOR-NIH/CNS' if self.__remediate else 'XPLOR-NIH'
            self.__addSf(f'NCS restraint, {software_name} HARMonic statement')

    # Exit a parse tree produced by XplorMRParser#harmonic_restraint.
    def exitHarmonic_restraint(self, ctx: XplorMRParser.Harmonic_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#antidistance_restraint.
    def enterAntidistance_restraint(self, ctx: XplorMRParser.Antidistance_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.adistStatements += 1
        self.__cur_subtype = 'adist'

        if self.__createSfDict:
            self.__addSf('anti-distance restraint, XPLOR-NIH XADC statement')

    # Exit a parse tree produced by XplorMRParser#antidistance_restraint.
    def exitAntidistance_restraint(self, ctx: XplorMRParser.Antidistance_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#coupling_restraint.
    def enterCoupling_restraint(self, ctx: XplorMRParser.Coupling_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.jcoupStatements += 1
        self.__cur_subtype = 'jcoup'

        if self.__createSfDict:
            self.__addSf()

    # Exit a parse tree produced by XplorMRParser#coupling_restraint.
    def exitCoupling_restraint(self, ctx: XplorMRParser.Coupling_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#carbon_shift_restraint.
    def enterCarbon_shift_restraint(self, ctx: XplorMRParser.Carbon_shift_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.hvycsStatements += 1
        self.__cur_subtype = 'hvycs'

        if self.__createSfDict:
            self.__addSf()

    # Exit a parse tree produced by XplorMRParser#carbon_shift_restraint.
    def exitCarbon_shift_restraint(self, ctx: XplorMRParser.Carbon_shift_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#proton_shift_restraint.
    def enterProton_shift_restraint(self, ctx: XplorMRParser.Proton_shift_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.procsStatements += 1
        self.__cur_subtype = 'procs'

        if self.__createSfDict:
            self.__addSf()

    # Exit a parse tree produced by XplorMRParser#proton_shift_restraint.
    def exitProton_shift_restraint(self, ctx: XplorMRParser.Proton_shift_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#dihedral_angle_db_restraint.
    def enterDihedral_angle_db_restraint(self, ctx: XplorMRParser.Dihedral_angle_db_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.ramaStatements += 1
        self.__cur_subtype = 'rama'

        if self.__createSfDict:
            software_name = 'XPLOR-NIH/CNS' if self.__remediate else 'XPLOR-NIH'
            statement_name = 'RAMAchandran/CONFormation' if self.__remediate else 'RAMAchandran'
            self.__addSf(f'dihedral angle database restraint, {software_name} {statement_name} statement')

    # Exit a parse tree produced by XplorMRParser#dihedral_angle_db_restraint.
    def exitDihedral_angle_db_restraint(self, ctx: XplorMRParser.Dihedral_angle_db_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#radius_of_gyration_restraint.
    def enterRadius_of_gyration_restraint(self, ctx: XplorMRParser.Radius_of_gyration_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.radiStatements += 1
        self.__cur_subtype = 'radi'

        if self.__createSfDict:
            self.__addSf('radius of gyration restraint, XPLOR-NIH COLLapse statement')

    # Exit a parse tree produced by XplorMRParser#radius_of_gyration_restraint.
    def exitRadius_of_gyration_restraint(self, ctx: XplorMRParser.Radius_of_gyration_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#diffusion_anisotropy_restraint.
    def enterDiffusion_anisotropy_restraint(self, ctx: XplorMRParser.Diffusion_anisotropy_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.diffStatements += 1
        self.__cur_subtype = 'diff'

        if self.__createSfDict:
            software_name = 'XPLOR-NIH/CNS' if self.__remediate else 'XPLOR-NIH'
            self.__addSf(f'diffusion anisotropy restraint, {software_name} DANIsotropy statement')

    # Exit a parse tree produced by XplorMRParser#diffusion_anisotropy_restraint.
    def exitDiffusion_anisotropy_restraint(self, ctx: XplorMRParser.Diffusion_anisotropy_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#orientation_db_restraint.
    def enterOrientation_db_restraint(self, ctx: XplorMRParser.Orientation_db_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.nbaseStatements += 1
        self.__cur_subtype = 'nbase'

        if self.__createSfDict:
            self.__addSf('orientation database restraint, XPLOR-NIH ORIEnt statement')

    # Exit a parse tree produced by XplorMRParser#orientation_db_restraint.
    def exitOrientation_db_restraint(self, ctx: XplorMRParser.Orientation_db_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#csa_restraint.
    def enterCsa_restraint(self, ctx: XplorMRParser.Csa_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.csaStatements += 1  # either CSA or pseudo CSA
        self.__cur_subtype = 'csa'

        if self.__createSfDict:
            self.__addSf()

    # Exit a parse tree produced by XplorMRParser#csa_restraint.
    def exitCsa_restraint(self, ctx: XplorMRParser.Csa_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#pcsa_restraint.
    def enterPcsa_restraint(self, ctx: XplorMRParser.Pcsa_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.csaStatements += 1  # either CSA or pseudo CSA
        self.__cur_subtype = 'csa'

        if self.__createSfDict:
            self.__addSf()

    # Exit a parse tree produced by XplorMRParser#pcsa_restraint.
    def exitPcsa_restraint(self, ctx: XplorMRParser.Pcsa_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#one_bond_coupling_restraint.
    def enterOne_bond_coupling_restraint(self, ctx: XplorMRParser.One_bond_coupling_restraintContext):  # pylint: disable=unused-argument
        """
        @deprecated: This restraint has not been useful in practice, but has been preserved for historical reasons.
        """

    # Exit a parse tree produced by XplorMRParser#one_bond_coupling_restraint.
    def exitOne_bond_coupling_restraint(self, ctx: XplorMRParser.One_bond_coupling_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#angle_db_restraint.
    def enterAngle_db_restraint(self, ctx: XplorMRParser.Angle_db_restraintContext):  # pylint: disable=unused-argument
        """
        @deprecated:  This term has not proved useful in practice and is only here for historical reasons.
        """

    # Exit a parse tree produced by XplorMRParser#angle_db_restraint.
    def exitAngle_db_restraint(self, ctx: XplorMRParser.Angle_db_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#pre_restraint.
    def enterPre_restraint(self, ctx: XplorMRParser.Pre_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.preStatements += 1
        self.__cur_subtype = 'pre'

        if self.__createSfDict:
            self.__addSf()

    # Exit a parse tree produced by XplorMRParser#pre_restraint.
    def exitPre_restraint(self, ctx: XplorMRParser.Pre_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#pcs_restraint.
    def enterPcs_restraint(self, ctx: XplorMRParser.Pcs_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.pcsStatements += 1
        self.__cur_subtype = 'pcs'

        if self.__createSfDict:
            self.__addSf()

    # Exit a parse tree produced by XplorMRParser#pcs_restraint.
    def exitPcs_restraint(self, ctx: XplorMRParser.Pcs_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#prdc_restraint.
    def enterPrdc_restraint(self, ctx: XplorMRParser.Prdc_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.prdcStatements += 1
        self.__cur_subtype = 'prdc'

        self.potential = 'square'  # default potential

        # do not add saveframe here which requires paramagnetic center information

    # Exit a parse tree produced by XplorMRParser#prdc_restraint.
    def exitPrdc_restraint(self, ctx: XplorMRParser.Prdc_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

    # Enter a parse tree produced by XplorMRParser#porientation_restraint.
    def enterPorientation_restraint(self, ctx: XplorMRParser.Porientation_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.pangStatements += 1
        self.__cur_subtype = 'pang'

        if self.__createSfDict:
            self.__addSf('paramagnetic orientation restraint, XPLOR-NIH XANGle statement')

    # Exit a parse tree produced by XplorMRParser#porientation_restraint.
    def exitPorientation_restraint(self, ctx: XplorMRParser.Porientation_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#pccr_restraint.
    def enterPccr_restraint(self, ctx: XplorMRParser.Pccr_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.pccrStatements += 1
        self.__cur_subtype = 'pccr'

        self.potential = 'square'  # default potential

        if self.__createSfDict:
            self.__addSf()

    # Exit a parse tree produced by XplorMRParser#pccr_restraint.
    def exitPccr_restraint(self, ctx: XplorMRParser.Pccr_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#hbond_restraint.
    def enterHbond_restraint(self, ctx: XplorMRParser.Hbond_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.classification = '.'

        self.hbondStatements += 1
        self.__cur_subtype = 'hbond'

        if self.__createSfDict:
            self.__addSf()

    # Exit a parse tree produced by XplorMRParser#hbond_restraint.
    def exitHbond_restraint(self, ctx: XplorMRParser.Hbond_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#hbond_db_restraint.
    def enterHbond_db_restraint(self, ctx: XplorMRParser.Hbond_db_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.hbondStatements += 1
        self.__cur_subtype = 'hbond'

        if self.__createSfDict:
            self.__addSf()

    # Exit a parse tree produced by XplorMRParser#hbond_db_restraint.
    def exitHbond_db_restraint(self, ctx: XplorMRParser.Hbond_db_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#noe_statement.
    def enterNoe_statement(self, ctx: XplorMRParser.Noe_statementContext):
        if ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('BIHA'):
                self.noePotential = 'biharmonic'
            elif code.startswith('LOGN'):
                self.noePotential = 'lognormal'
            elif code.startswith('SQUA'):
                self.noePotential = 'square'
            elif code.startswith('SOFT'):
                self.noePotential = 'softsquare'
            elif code.startswith('SYMM'):
                self.noePotential = 'symmetry'
            elif code.startswith('HIGH'):
                self.noePotential = 'high'
            elif code.startswith('3DPO'):
                self.noePotential = '3dpo'
            else:
                self.noePotential = 'biharmonic'
                self.__f.append("[Enum mismatch ignorable] "
                                f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'NOE' statements. "
                                f"Instead, set the default potential {self.noePotential!r}.")

        elif ctx.Averaging_methods():
            code = str(ctx.Averaging_methods()).upper()
            if code == 'R-6':
                self.noeAverage = 'r-6'
            elif code == 'R-3':
                self.noeAverage = 'r-3'
            elif code == 'SUM':
                self.noeAverage = 'sum'
            elif code.startswith('CENT'):
                self.noeAverage = 'center'
            else:
                self.noeAverage = 'r-6'
                self.__f.append("[Enum mismatch ignorable] "
                                f"The averaging method {str(ctx.Averaging_methods())!r} is unknown method for the 'NOE' statements. "
                                f"Instead, set the default method {self.noeAverage!r}.")

        elif ctx.SqExponent():
            self.squareExponent = self.getNumber_s(ctx.number_s())
            if isinstance(self.squareExponent, str):
                if self.squareExponent in self.evaluate:
                    self.squareExponent = self.evaluate[self.squareExponent]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.squareExponent!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.squareExponent = 2.0
            if self.squareExponent is None or self.squareExponent <= 0.0:
                self.__f.append("[Invalid data] "
                                "The exponent value of square-well or soft-square function "
                                f"'NOE {str(ctx.SqExponent())} {self.getClass_name(ctx.class_name(0))} {self.squareExponent} END' must be a positive value.")

        elif ctx.SoExponent():
            self.softExponent = self.getNumber_s(ctx.number_s())
            if isinstance(self.softExponent, str):
                if self.softExponent in self.evaluate:
                    self.softExponent = self.evaluate[self.softExponent]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.softExponent!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.softExponent = 2.0
            if self.softExponent is None or self.softExponent <= 0.0:
                self.__f.append("[Invalid data] "
                                "The exponent value for soft-square function only "
                                f"'NOE {str(ctx.SoExponent())} {self.getClass_name(ctx.class_name(0))} {self.softExponent} END' must be a positive value.")

        elif ctx.SqConstant():
            self.squareConstant = self.getNumber_s(ctx.number_s())
            if isinstance(self.squareConstant, str):
                if self.squareConstant in self.evaluate:
                    self.squareConstant = self.evaluate[self.squareConstant]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.squareConstant!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.squareConstant = 20.0
            if self.squareConstant is None or self.squareConstant <= 0.0:
                self.__f.append("[Invalid data] "
                                "The auxiliary scaling constant of square-well or soft-square function "
                                f"'NOE {str(ctx.SqConstant())} {self.getClass_name(ctx.class_name(0))} {self.squareConstant} END' must be a positive value.")

        elif ctx.SqOffset():
            self.squareOffset = self.getNumber_s(ctx.number_s())
            if isinstance(self.squareOffset, str):
                if self.squareOffset in self.evaluate:
                    self.squareOffset = self.evaluate[self.squareOffset]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.squareOffset!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.squareOffset = 0.0
            if self.squareOffset is None or self.squareOffset < 0.0:
                self.__f.append("[Invalid data] "
                                "The negative offset value to all upper bounds of square-well or soft-square function "
                                f"'NOE {str(ctx.SqOffset())} {self.getClass_name(ctx.class_name(0))} {self.squareOffset} END' must not be a negative value.")

        elif ctx.Rswitch():
            self.rSwitch = self.getNumber_s(ctx.number_s())
            if isinstance(self.rSwitch, str):
                if self.rSwitch in self.evaluate:
                    self.rSwitch = self.evaluate[self.rSwitch]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.rSwitch!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.rSwitch = 10.0
            if self.rSwitch is None or self.rSwitch < 0.0:
                self.__f.append("[Invalid data] "
                                "The smoothing parameter of soft-square function "
                                f"'NOE {str(ctx.Rswitch())} {self.getClass_name(ctx.class_name(0))} {self.rSwitch} END' must not be a negative value.")

        elif ctx.Scale():
            self.scale = self.getNumber_s(ctx.number_s())
            if isinstance(self.scale, str):
                if self.scale in self.evaluate:
                    self.scale = self.evaluate[self.scale]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.scale!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.scale = 1.0
            if self.scale is None or self.scale == 0.0:
                self.__f.append("[Range value warning] "
                                f"The scale value 'NOE {str(ctx.Scale())} {self.getClass_name(ctx.class_name(0))} {self.scale} END' should be a positive value.")
            elif self.scale < 0.0:
                self.__f.append("[Invalid data] "
                                f"The scale value 'NOE {str(ctx.Scale())} {self.getClass_name(ctx.class_name(0))} {self.scale} END' must not be a negative value.")

        elif ctx.Asymptote():
            self.asymptote = self.getNumber_s(ctx.number_s())
            if isinstance(self.asymptote, str):
                if self.asymptote in self.evaluate:
                    self.asymptote = self.evaluate[self.asymptote]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.asymptote!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.asymptote = 0.0
            if self.asymptote is None:
                self.__f.append("[Range value warning] "
                                "The asymptote slope value "
                                f"'NOE {str(ctx.Asymptote())} {self.getClass_name(ctx.class_name(0))} {self.asymptote} END' should be a non-negative value.")
            elif self.asymptote < 0.0:
                self.__f.append("[Invalid data] "
                                "The asymptote slope value "
                                f"'NOE {str(ctx.Asymptote())} {self.getClass_name(ctx.class_name(0))} {self.asymptote} END' must not be a negative value.")

        elif ctx.Bhig():
            self.B_high = self.getNumber_s(ctx.number_s())
            if isinstance(self.B_high, str):
                if self.B_high in self.evaluate:
                    self.B_high = self.evaluate[self.B_high]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.B_high!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.B_high = 0.01
            if self.B_high is None:
                self.__f.append("[Range value warning] "
                                "The potential barrier value "
                                f"'NOE {str(ctx.Bhig())} {self.getClass_name(ctx.class_name(0))} {self.B_high} END' should be a non-negative value.")
            elif self.B_high < 0.0:
                self.__f.append("[Invalid data] "
                                "The potential barrier value "
                                f"'NOE {str(ctx.Bhig())} {self.getClass_name(ctx.class_name(0))} {self.B_high} END' must not be a negative value.")

        elif ctx.Ceiling():
            self.ceiling = self.getNumber_s(ctx.number_s())
            if isinstance(self.ceiling, str):
                if self.ceiling in self.evaluate:
                    self.ceiling = self.evaluate[self.ceiling]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.ceiling!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.ceiling = 30.0
            if self.ceiling is None:
                self.__f.append("[Range value warning] "
                                f"The ceiling value for energy constant 'NOE {str(ctx.Ceiling())} {self.ceiling} END' should be a non-negative value.")
            elif self.ceiling < 0.0:
                self.__f.append("[Invalid data] "
                                f"The ceiling value for energy constant 'NOE {str(ctx.Ceiling())} {self.ceiling} END' must not be a negative value.")

        elif ctx.Temperature():
            self.temperature = self.getNumber_s(ctx.number_s())
            if isinstance(self.temperature, str):
                if self.temperature in self.evaluate:
                    self.temperature = self.evaluate[self.temperature]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.temperature!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.temperature = 300.0
            if self.temperature is None:
                self.__f.append("[Range value warning] "
                                f"The temperature 'NOE {str(ctx.Temparature())} {self.temperature} END' should be a non-negative value.")
            elif self.temperature < 0.0:
                self.__f.append("[Invalid data] "
                                f"The temperature 'NOE {str(ctx.Temparature())} {self.temperature} END' must not be a negative value.")

        elif ctx.Monomers():
            self.monomers = int(str(ctx.Integer()))
            if self.monomers is None or self.monomers == 0:
                self.__f.append("[Range value warning] "
                                "The number of monomers "
                                f"'NOE {str(ctx.Monomers())} {self.getClass_name(ctx.class_name(0))} {self.monomers} END' should be a positive value.")
            elif self.monomers < 0:
                self.__f.append("[Invalid data] "
                                "The number of monomers "
                                f"'NOE {str(ctx.Monomers())} {self.getClass_name(ctx.class_name(0))} {self.monomers} END' must not be a negative value.")

        elif ctx.Ncount():
            self.ncount = int(str(ctx.Integer()))
            if self.ncount is None or self.ncount == 0:
                self.__f.append("[Range value warning] "
                                f"The number of assign statements "
                                f"'NOE {str(ctx.Ncount())} {self.getClass_name(ctx.class_name(0))} {self.ncount} END' should be a positive value.")
            elif self.ncount < 0:
                self.__f.append("[Invalid data] "
                                f"The number of assign statements "
                                f"'NOE {str(ctx.Ncount())} {self.getClass_name(ctx.class_name(0))} {self.ncount} END' must not be a negative value.")

        elif ctx.Reset():
            self.noePotential = 'biharmonic'  # default potential
            self.squareExponent = 2.0
            self.softExponent = 2.0
            self.squareConstant = 20.0
            self.squareOffset = 0.0
            self.rSwitch = 10.0
            self.scale = 1.0
            self.asymptote = 0.0
            self.B_high = 0.01
            self.ceiling = 30.0
            self.temperature = 300.0
            self.monomers = 1
            self.ncount = 2
            self.symmTarget = None
            self.symmDminus = None
            self.symmDplus = None

    # Exit a parse tree produced by XplorMRParser#noe_statement.
    def exitNoe_statement(self, ctx: XplorMRParser.Noe_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (NOE) classification={self.classification!r}")

    # Enter a parse tree produced by XplorMRParser#noe_assign.
    def enterNoe_assign(self, ctx: XplorMRParser.Noe_assignContext):  # pylint: disable=unused-argument
        self.distRestraints += 1
        self.__cur_subtype_altered = self.__cur_subtype != 'dist'
        if self.__cur_subtype != 'dist':
            self.distStatements += 1
        self.__cur_subtype = 'dist' if self.__cur_subtype not in ('pre', 'rdc') else self.__cur_subtype  # set 'pre', 'rdc' for error message

        self.atomSelectionSet.clear()
        self.__g.clear()

        self.scale_a = None
        self.paramagCenter = None

    # Exit a parse tree produced by XplorMRParser#noe_assign.
    def exitNoe_assign(self, ctx: XplorMRParser.Noe_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            if len(self.atomSelectionSet) == 2 and len(self.numberSelection) == 2 and not self.__in_block:

                if self.paramagCenter is not None:

                    try:
                        atom_id_2 = self.atomSelectionSet[1][0]['atom_id']
                        if atom_id_2[0] in protonBeginCode:
                            self.distRestraints -= 1
                            self.preRestraints += 1
                            if self.__cur_subtype_altered:
                                self.distStatements -= 1
                                if self.preStatements == 0:
                                    self.preStatements += 1
                            self.__cur_subtype = 'pre'
                            self.exitPre_assign(ctx)
                            return

                    except IndexError:
                        pass

                if len(self.atomSelectionSet[0]) == 1 and len(self.atomSelectionSet[1]) == 1:
                    chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                    seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                    comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                    atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                    chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                    seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                    comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                    atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                    if (atom_id_1[0] in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) and (atom_id_2[0] in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS)\
                       and chain_id_1 == chain_id_2:
                        if seq_id_1 == seq_id_2:
                            if atom_id_1 != atom_id_2 and self.__ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):
                                self.distRestraints -= 1
                                self.rdcRestraints += 1
                                if self.__cur_subtype_altered:
                                    self.distStatements -= 1
                                    if self.rdcStatements == 0:
                                        self.rdcStatements += 1
                                self.__cur_subtype = 'rdc'
                                self.exitTenso_assign(ctx)
                                return

                        elif abs(seq_id_1 - seq_id_2) == 1 and self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                                ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                                 or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')):
                            self.distRestraints -= 1
                            self.rdcRestraints += 1
                            if self.__cur_subtype_altered:
                                self.distStatements -= 1
                                if self.rdcStatements == 0:
                                    self.rdcStatements += 1
                            self.__cur_subtype = 'rdc'
                            self.exitTenso_assign(ctx)
                            return

            self.__cur_subtype = 'dist'  # to get consistent number of statement

            target = self.numberSelection[0]

            if len(self.numberSelection) > 2:
                dminus = self.numberSelection[1]
                dplus = self.numberSelection[2]

            elif len(self.numberSelection) > 1:
                dminus = dplus = self.numberSelection[1]

            else:
                dminus = dplus = 0.0

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            scale = self.scale if self.scale_a is None else self.scale_a

            if scale < 0.0:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The weight value '{scale}' must not be a negative value.")
                return
            if scale == 0.0:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The weight value '{scale}' should be a positive value.")

            target_value = target
            lower_limit = None
            upper_limit = None
            lower_linear_limit = None
            upper_linear_limit = None

            if self.noePotential == 'biharmonic':
                lower_limit = target - dminus
                upper_limit = target + dplus
            elif self.noePotential == 'lognormal':
                pass
            elif self.noePotential == 'square':
                if abs(self.squareExponent - 2.0) < abs(self.squareExponent - 1.0):
                    lower_linear = target - dminus
                    upper_linear = target + dplus - self.squareOffset
                else:
                    lower_linear_limit = target - dminus
                    upper_linear_limit = target + dplus - self.squareOffset
            elif self.noePotential == 'softsquare':
                if abs(self.squareExponent - 2.0) < abs(self.squareExponent - 1.0):
                    lower_linear = target - dminus
                    upper_linear = target + dplus - self.squareOffset
                    upper_linear_limit = target + dplus - self.squareOffset + self.rSwitch
                else:
                    lower_linear_limit = target - dminus
                    upper_linear_limit = target + dplus - self.squareOffset
            elif self.noePotential == 'symmetry':
                if target == 0.0:
                    target = self.symmTarget
                    dminus = self.symmDminus
                    dplus = self.symmDplus
                else:
                    self.symmTarget = target
                    self.symmDminus = dminus
                    self.symmDplus = dplus
                target_value = target
                if abs(self.squareExponent - 2.0) < abs(self.squareExponent - 1.0):
                    lower_linear = target - dminus
                    upper_linear = target + dplus - self.squareOffset
                    upper_linear_limit = target + dplus - self.squareOffset + self.rSwitch
                else:
                    lower_linear_limit = target - dminus
                    upper_linear_limit = target + dplus - self.squareOffset
            elif self.noePotential == 'high':
                lower_linear = target - dminus
                upper_linear = target + dplus
                lower_linear_limit = lower_linear - 0.1
                upper_linear_limit = upper_linear + 0.1
            else:  # 3dpo
                if target == 0.0:
                    target = self.symmTarget
                    dminus = self.symmDminus
                    dplus = self.symmDplus
                else:
                    self.symmTarget = target
                    self.symmDminus = dminus
                    self.symmDplus = dplus
                target_value = target
                lower_limit = target - dminus
                upper_limit = target + dplus

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

            dstFunc = self.validateDistanceRange(scale,
                                                 target_value, lower_limit, upper_limit,
                                                 lower_linear_limit, upper_linear_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPoly:
                return

            if len(self.atomSelectionSet[0]) == 0 or len(self.atomSelectionSet[1]) == 0:
                if len(self.__g) > 0:
                    self.__f.extend(self.__g)
                return

            combinationId = memberId = '.'
            if self.__createSfDict:
                sf = self.__getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                       self.__csStat, self.__originalFileName),
                                  potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                sf['id'] += 1
                if len(self.atomSelectionSet) > 2:
                    combinationId = 0
                if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                   and (isAmbigAtomSelection(self.atomSelectionSet[0], self.__csStat)
                        or isAmbigAtomSelection(self.atomSelectionSet[1], self.__csStat)):
                    memberId = 0

            for i in range(0, len(self.atomSelectionSet), 2):
                if isinstance(combinationId, int):
                    combinationId += 1
                if isinstance(memberId, int):
                    memberId = 0
                    _atom1 = _atom2 = None
                if self.__createSfDict:
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[i]) * len(self.atomSelectionSet[i + 1]) > 1 else '.'
                for atom1, atom2 in itertools.product(self.atomSelectionSet[i],
                                                      self.atomSelectionSet[i + 1]):
                    if isIdenticalRestraint([atom1, atom2]):
                        continue
                    if self.__createSfDict and memberLogicCode == '.':
                        altAtomId1, altAtomId2 = getAltProtonIdInBondConstraint([atom1, atom2], self.__csStat)
                        if altAtomId1 is not None or altAtomId2 is not None:
                            atom1, atom2 =\
                                self.selectRealisticBondConstraint(atom1, atom2,
                                                                   altAtomId1, altAtomId2,
                                                                   dstFunc)
                    if len(self.__fibril_chain_ids) > 0\
                       and atom1['chain_id'] in self.__fibril_chain_ids\
                       and atom2['chain_id'] in self.__fibril_chain_ids\
                       and not self.isRealisticDistanceRestraint(atom1, atom2, dstFunc):
                        continue
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
                                     combinationId, memberId, memberLogicCode,
                                     sf['list_id'], self.__entryId, dstFunc,
                                     self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                     atom1, atom2)
                        sf['loop'].add_data(row)

                        if sf['constraint_subsubtype'] == 'ambi':
                            continue

                        if isinstance(combinationId, int)\
                           or (memberLogicCode == 'OR'
                               and (isAmbigAtomSelection(self.atomSelectionSet[i], self.__csStat)
                                    or isAmbigAtomSelection(self.atomSelectionSet[i + 1], self.__csStat))):
                            sf['constraint_subsubtype'] = 'ambi'
                        if 'upper_limit' in dstFunc and dstFunc['upper_limit'] is not None:
                            upperLimit = float(dstFunc['upper_limit'])
                            if upperLimit <= DIST_AMBIG_LOW or upperLimit >= DIST_AMBIG_UP:
                                sf['constraint_subsubtype'] = 'ambi'

        finally:
            self.numberSelection.clear()

    def validateDistanceRange(self, weight,
                              target_value, lower_limit, upper_limit,
                              lower_linear_limit, upper_linear_limit):
        """ Validate distance value range.
        """

        validRange = True
        dstFunc = {'weight': weight, 'potential': self.noePotential, 'average': self.noeAverage}

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

    # Enter a parse tree produced by XplorMRParser#predict_statement.
    def enterPredict_statement(self, ctx: XplorMRParser.Predict_statementContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#predict_statement.
    def exitPredict_statement(self, ctx: XplorMRParser.Predict_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#noe_annotation.
    def enterNoe_annotation(self, ctx: XplorMRParser.Noe_annotationContext):
        if ctx.Weight():
            self.scale_a = self.getNumber_a(ctx.number_a())

    # Exit a parse tree produced by XplorMRParser#noe_annotation.
    def exitNoe_annotation(self, ctx: XplorMRParser.Noe_annotationContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#dihedral_statement.
    def enterDihedral_statement(self, ctx: XplorMRParser.Dihedral_statementContext):
        if ctx.Scale():
            self.scale = self.getNumber_s(ctx.number_s())
            if isinstance(self.scale, str):
                if self.scale in self.evaluate:
                    self.scale = self.evaluate[self.scale]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The scale value 'RESTRAINTS DIHEDRAL {str(ctx.Scale())}={self.scale} END' "
                                    f"where the symbol {self.scale!r} is not defined so that set the default value.")
                    self.scale = 1.0
            if self.scale < 0.0:
                self.__f.append("[Invalid data] "
                                f"The scale value 'RESTRAINTS DIHEDRAL {str(ctx.Scale())}={self.scale} END' must not be a negative value.")
            elif self.scale == 0.0:
                self.__f.append("[Range value warning] "
                                f"The scale value 'RESTRAINTS DIHEDRAL {str(ctx.Scale())}={self.scale} END' should be a positive value.")

        elif ctx.Reset():
            self.scale = 1.0

    # Exit a parse tree produced by XplorMRParser#dihedral_statement.
    def exitDihedral_statement(self, ctx: XplorMRParser.Dihedral_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#dihedral_assign.
    def enterDihedral_assign(self, ctx: XplorMRParser.Dihedral_assignContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1
        if self.__cur_subtype != 'dihed':
            self.dihedStatements += 1
        self.__cur_subtype = 'dihed'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#dihedral_assign.
    def exitDihedral_assign(self, ctx: XplorMRParser.Dihedral_assignContext):

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            energyConst = self.numberSelection[0]
            target = self.numberSelection[1]
            delta = abs(self.numberSelection[2])
            exponent = int(str(ctx.Integer()))

            if energyConst <= 0.0:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The energy constant value {energyConst} must be a positive value.")
                return

            if exponent not in (0, 1, 2, 4):
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The exponent value of dihedral angle restraint 'ed={exponent}' should be 1 (linear well), 2 (square well) or 4 (quartic well).")
                return

            target_value = target
            lower_limit = None
            upper_limit = None
            lower_linear_limit = None
            upper_linear_limit = None

            if delta > 0.0:
                if exponent in (2, 4):
                    lower_limit = target - delta
                    upper_limit = target + delta
                else:
                    lower_linear_limit = target - delta
                    upper_linear_limit = target + delta

            dstFunc = self.validateAngleRange(self.scale if exponent > 0 else 0.0, {'energy_const': energyConst, 'exponent': exponent},
                                              target_value, lower_limit, upper_limit,
                                              lower_linear_limit, upper_linear_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
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

    def areUniqueCoordAtoms(self, subtype_name, skip_col=None, allow_ambig=False, allow_ambig_warn_title=''):
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
                if allow_ambig:
                    self.__f.append(f"[{allow_ambig_warn_title}] {self.__getCurrentRestraint()}"
                                    f"Ambiguous atom selection '{atom1['chain_id']}:{atom1['seq_id']}:{atom1['comp_id']}:{atom1['atom_id']} or "
                                    f"{atom2['atom_id']}' found in {subtype_name} restraint.")
                    continue
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"Ambiguous atom selection '{atom1['chain_id']}:{atom1['seq_id']}:{atom1['comp_id']}:{atom1['atom_id']} or "
                                f"{atom2['atom_id']}' is not allowed as {subtype_name} restraint.")
                return False

        return True

    # Enter a parse tree produced by XplorMRParser#sani_statement.
    def enterSani_statement(self, ctx: XplorMRParser.Sani_statementContext):
        if ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.potential = 'square'
            elif code.startswith('HARM'):
                self.potential = 'harmonic'
            else:
                self.potential = 'square'
                self.__f.append("[Enum mismatch ignorable] "
                                f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'SANIsotropy' statements. "
                                f"Instead, set the default potential {self.potential!r}.")

        elif ctx.Reset():
            self.potential = 'square'
            self.coefficients = None

        elif ctx.Coefficients():
            self.coefficients = {'DFS': self.getNumber_s(ctx.number_s(0)),
                                 'anisotropy': self.getNumber_s(ctx.number_s(1)),
                                 'rhombicity': self.getNumber_s(ctx.number_s(2))
                                 }

    # Exit a parse tree produced by XplorMRParser#sani_statement.
    def exitSani_statement(self, ctx: XplorMRParser.Sani_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (SANI) classification={self.classification!r} "
                  f"coefficients={self.coefficients}")

    # Enter a parse tree produced by XplorMRParser#sani_assign.
    def enterSani_assign(self, ctx: XplorMRParser.Sani_assignContext):  # pylint: disable=unused-argument
        self.rdcRestraints += 1
        if self.__cur_subtype != 'rdc':
            self.rdcStatements += 1
        self.__cur_subtype = 'rdc'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#sani_assign.
    def exitSani_assign(self, ctx: XplorMRParser.Sani_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            target = self.numberSelection[0]

            if len(self.numberSelection) > 1:
                delta = abs(self.numberSelection[1])
            else:
                delta = 0.0

            target_value = target
            lower_limit = None
            upper_limit = None

            if self.potential == 'square' and delta > 0.0:
                lower_limit = target - delta
                upper_limit = target + delta
                if len(self.numberSelection) > 2:
                    error_less = delta
                    error_greater = abs(self.numberSelection[2])
                    lower_limit = target - error_less
                    upper_limit = target + error_greater

            dstFunc = self.validateRdcRange(1.0, {'potential': self.potential},
                                            target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return
            """
            if not self.areUniqueCoordAtoms('an RDC (SANI)', XPLOR_ORIGIN_AXIS_COLS):
                if len(self.__g) > 0:
                    self.__f.extend(self.__g)
                return
            """
            try:
                chain_id_1 = self.atomSelectionSet[4][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[4][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[4][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[4][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[5][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[5][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[5][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[5][0]['atom_id']
            except IndexError:
                if not self.areUniqueCoordAtoms('an RDC (SANI)', XPLOR_ORIGIN_AXIS_COLS):
                    if len(self.__g) > 0:
                        self.__f.extend(self.__g)
                return

            chain_id_set = None
            if self.__exptlMethod == 'SOLID-STATE NMR':
                ps = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                if ps is not None:
                    chain_id_set = [chain_id_1]
                    chain_id_set.extend(ps['identical_auth_chain_id'])
                    chain_id_set.sort()
                    if self.__symmetric != 'no':
                        pass
                    elif len(chain_id_set) > MAX_MAG_IDENT_ASYM_ID and chain_id_2 in chain_id_set:
                        self.__symmetric = 'linear'

                        try:

                            _head =\
                                self.__cR.getDictListWithFilter('atom_site',
                                                                CARTN_DATA_ITEMS,
                                                                [{'name': self.__authAsymId, 'type': 'str', 'value': chain_id_set[0]},
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
                                                                [{'name': self.__authAsymId, 'type': 'str', 'value': chain_id_set[-1]},
                                                                 {'name': self.__authSeqId, 'type': 'int', 'value': seq_id_1},
                                                                 {'name': self.__authAtomId, 'type': 'str', 'value': atom_id_1},
                                                                 {'name': self.__modelNumName, 'type': 'int',
                                                                  'value': self.__representativeModelId},
                                                                 {'name': 'label_alt_id', 'type': 'enum',
                                                                  'enum': ('A')}
                                                                 ])

                            if len(_head) == 1 and len(_tail) == 1:
                                if distance(to_np_array(_head[0]), to_np_array(_tail[0])) < 10.0:
                                    self.__symmetric = 'circular'

                        except Exception as e:
                            if self.__verbose:
                                self.__lfh.write(f"+XplorMRParserListener.exitSani_assign() ++ Error  - {str(e)}")

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Non-magnetic susceptible spin appears in RDC vector; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if chain_id_1 != chain_id_2:
                if self.__symmetric == 'no':
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
                if self.__symmetric == 'no':
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Found zero RDC vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif self.__ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                if not self.__ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                    if self.__nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.__nefT.validate_comp_atom(comp_id_2, atom_id_2):
                        if atom_id_1[0] in protonBeginCode and atom_id_2[0] in protonBeginCode:
                            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                            "Found an RDC vector over multiple covalent bonds in the 'SANIsotropy' statement; "
                                            f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}). "
                                            "Did you accidentally select 'SANIsotropy' statement, instead of 'XDIPolar' statement of XPLOR-NIH?")
                        else:
                            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                            "Found an RDC vector over multiple covalent bonds in the 'SANIsotropy' statement; "
                                            f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

            combinationId = '.'
            if self.__createSfDict:
                sf = self.__getSf(potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc),
                                  rdcCode=getRdcCode([self.atomSelectionSet[4][0], self.atomSelectionSet[5][0]]))
                sf['id'] += 1
                if len(self.atomSelectionSet[4]) > 1 or len(self.atomSelectionSet[5]) > 1:
                    combinationId = 0

            for atom1, atom2 in itertools.product(self.atomSelectionSet[4],
                                                  self.atomSelectionSet[5]):
                if isIdenticalRestraint([atom1, atom2]):
                    continue
                if self.__symmetric == 'no':
                    if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None):
                        continue
                else:
                    if isAsymmetricRangeRestraint([atom1, atom2], chain_id_set, self.__symmetric):
                        continue
                    if atom1['chain_id'] != atom2['chain_id']:
                        self.__f.append(f"[Anomalous RDC vector] {self.__getCurrentRestraint()}"
                                        "Found inter-chain RDC vector; "
                                        f"({atom1['chain_id']}:{atom1['seq_id']}:{atom1['comp_id']}:{atom1['atom_id']}, "
                                        f"{atom2['chain_id']}:{atom2['seq_id']}:{atom2['comp_id']}:{atom2['atom_id']}). "
                                        "However, it might be an artificial RDC constraint on solid-state NMR applied to symmetric samples such as fibrils.")
                if isinstance(combinationId, int):
                    combinationId += 1
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (SANI) id={self.rdcRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 combinationId, None, None,
                                 sf['list_id'], self.__entryId, dstFunc,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom1, atom2)
                    sf['loop'].add_data(row)

        finally:
            self.numberSelection.clear()

    def validateRdcRange(self, weight, misc_dict,
                         target_value, lower_limit, upper_limit,
                         lower_linear_limit=None, upper_linear_limit=None):
        """ Validate angle value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if isinstance(misc_dict, dict):
            for k, v in misc_dict.items():
                dstFunc[k] = v

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

        if lower_linear_limit is not None:
            if RDC_ERROR_MIN <= lower_linear_limit < RDC_ERROR_MAX:
                dstFunc['lower_linear_limit'] = f"{lower_linear_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The lower linear limit value='{lower_linear_limit:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if upper_linear_limit is not None:
            if RDC_ERROR_MIN < upper_linear_limit <= RDC_ERROR_MAX:
                dstFunc['upper_linear_limit'] = f"{upper_linear_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The upper linear limit value='{upper_linear_limit:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if lower_linear_limit is not None:
                if lower_linear_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

            if upper_linear_limit is not None:
                if upper_linear_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper linear limit value='{upper_linear_limit:.6f}' must be greater than the target value '{target_value}'.")

        else:

            if lower_limit is not None and upper_limit is not None:
                if lower_limit > upper_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if lower_linear_limit is not None and upper_limit is not None:
                if lower_linear_limit > upper_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if lower_limit is not None and upper_linear_limit is not None:
                if lower_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if lower_linear_limit is not None and upper_linear_limit is not None:
                if lower_linear_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if lower_limit is not None and lower_linear_limit is not None:
                if lower_linear_limit > lower_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the lower limit value '{lower_limit:.6f}'.")

            if upper_limit is not None and upper_linear_limit is not None:
                if upper_limit > upper_linear_limit:
                    validRange = False
                    self. __f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                     f"The upper limit value='{upper_limit:.6f}' must be less than the upper linear limit value '{upper_linear_limit:.6f}'.")

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

        if lower_linear_limit is not None:
            if RDC_RANGE_MIN <= lower_linear_limit <= RDC_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower linear limit value='{lower_linear_limit:.6f}' should be within range {RDC_RESTRAINT_RANGE}.")

        if upper_linear_limit is not None:
            if RDC_RANGE_MIN <= upper_linear_limit <= RDC_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper linear limit value='{upper_linear_limit:.6f}' should be within range {RDC_RESTRAINT_RANGE}.")

        return dstFunc

    # Enter a parse tree produced by XplorMRParser#xdip_statement.
    def enterXdip_statement(self, ctx: XplorMRParser.Xdip_statementContext):
        if ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.potential = 'square'
            elif code.startswith('HARM'):
                self.potential = 'harmonic'
            else:
                self.potential = 'square'
                self.__f.append("[Enum mismatch ignorable] "
                                f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'XDIPolar' statements. "
                                f"Instead, set the default potential {self.potential!r}.")

        elif ctx.Averaging_methods():
            code = str(ctx.Averaging_methods()).upper()
            if code.startswith('SUMD'):
                self.average = 'sum_diff'
            elif code == 'SUM':
                self.average = 'sum'
            elif code.startswith('AVER'):
                self.average = 'average'
            else:
                self.average = 'sum'
                self.__f.append("[Enum mismatch ignorable] "
                                f"The averaging method {str(ctx.Averaging_methods())!r} is unknown method for the 'XDIPolar' statements. "
                                f"Instead, set the default method {self.average!r}.")

        elif ctx.Scale():
            self.scale = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.scale, str):
                if self.scale in self.evaluate:
                    self.scale = self.evaluate[self.scale]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The symbol {self.scale!r} in the 'XDIPolar' statement is not defined so that set the default value.")
                    self.scale = 1.0
            if self.scale < 0.0:
                self.__f.append("[Invalid data] "
                                f"The scale value 'XDIPOLAR {str(ctx.Scale())} {self.scale} END' must not be a negative value.")
            elif self.scale == 0.0:
                self.__f.append("[Range value warning] "
                                f"The scale value 'XDIPOLAR {str(ctx.Scale())} {self.scale} END' should be a positive value.")

        elif ctx.Reset():
            self.potential = 'square'
            self.average = 'sum'
            self.scale = 1.0
            self.coefficients = None

        elif ctx.Coefficients():
            self.coefficients = {'DFS': self.getNumber_s(ctx.number_s(0)),
                                 'anisotropy': self.getNumber_s(ctx.number_s(1)),
                                 'rhombicity': self.getNumber_s(ctx.number_s(2))
                                 }

    # Exit a parse tree produced by XplorMRParser#xdip_statement.
    def exitXdip_statement(self, ctx: XplorMRParser.Xdip_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (XDIP) classification={self.classification!r} "
                  f"coefficients={self.coefficients}")

    # Enter a parse tree produced by XplorMRParser#xdip_assign.
    def enterXdip_assign(self, ctx: XplorMRParser.Xdip_assignContext):  # pylint: disable=unused-argument
        self.rdcRestraints += 1
        self.__cur_subtype = 'rdc'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#xdip_assign.
    def exitXdip_assign(self, ctx: XplorMRParser.Xdip_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            target = self.numberSelection[0]
            delta = abs(self.numberSelection[1])

            if len(self.numberSelection) > 3:
                lower_limit_1 = None
                upper_limit_1 = None
                lower_limit_2 = None
                upper_limit_2 = None

                target_value_1 = self.numberSelection[0]
                target_value_2 = self.numberSelection[3]
                error_greater_1 = abs(self.numberSelection[1])
                error_less_1 = abs(self.numberSelection[2])
                error_greater_2 = abs(self.numberSelection[4])
                error_less_2 = abs(self.numberSelection[5])

                if self.potential == 'square':
                    lower_limit_1 = target_value_1 - error_less_1
                    upper_limit_1 = target_value_1 + error_greater_1
                    lower_limit_2 = target_value_2 - error_less_2
                    upper_limit_2 = target_value_2 + error_greater_2

                dstFunc = self.validateRdcRange2(self.scale, {'potential': self.potential, 'average': self.average},
                                                 target_value_1, lower_limit_1, upper_limit_1,
                                                 target_value_2, lower_limit_2, upper_limit_2)

                if dstFunc is None:
                    return

            else:
                lower_limit = None
                upper_limit = None

                if self.potential == 'square' and delta > 0.0:
                    target_value = target
                    lower_limit = target - delta
                    upper_limit = target + delta
                    if len(self.numberSelection) > 2:
                        error_less = delta
                        error_greater = abs(self.numberSelection[2])
                        lower_limit = target - error_less
                        upper_limit = target + error_greater
                else:
                    target_value = target

                dstFunc = self.validateRdcRange(self.scale, {'potential': self.potential, 'average': self.average},
                                                target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return
            """
            if not self.areUniqueCoordAtoms('an RDC (XDIP)', XPLOR_ORIGIN_AXIS_COLS,
                                            allow_ambig=True, allow_ambig_warn_title='Anomalous RDC vector'):
                if len(self.__g) > 0:
                    self.__f.extend(self.__g)
                return
            """
            try:
                chain_id_1 = self.atomSelectionSet[4][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[4][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[4][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[4][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[5][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[5][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[5][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[5][0]['atom_id']
            except IndexError:
                if not self.areUniqueCoordAtoms('an RDC (XDIP)', XPLOR_ORIGIN_AXIS_COLS,
                                                allow_ambig=True, allow_ambig_warn_title='Anomalous RDC vector'):
                    if len(self.__g) > 0:
                        self.__f.extend(self.__g)
                return

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Non-magnetic susceptible spin appears in RDC vector; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            spin_system = f'{ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atom_id_1[0]][0]}{atom_id_1[0]}-{ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atom_id_2[0]][0]}{atom_id_2[0]}'

            if chain_id_1 != chain_id_2:
                ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    f"Found inter-chain {spin_system} dipolar coupling vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) > 1:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"Found inter-residue {spin_system} dipolar coupling vector; "
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
                                    f"Found inter-residue {spin_system} dipolar coupling vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif atom_id_1 == atom_id_2:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"Found zero {spin_system} dipolar coupling vector; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            else:
                if atom_id_1[0] not in protonBeginCode or atom_id_2[0] not in protonBeginCode:
                    self.__f.append(f"[Anomalous RDC vector] {self.__getCurrentRestraint()}"
                                    f"Found {spin_system} dipolar coupling vector in the 'XDIPolar' statement, which usually accepts 1H-1H dipolar coupling; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")

            combinationId = '.'
            if self.__createSfDict:
                sf = self.__getSf(potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc),
                                  rdcCode=getRdcCode([self.atomSelectionSet[4][0], self.atomSelectionSet[5][0]]))
                sf['id'] += 1
                if len(self.atomSelectionSet[4]) > 1 or len(self.atomSelectionSet[5]) > 1:
                    combinationId = 0

            for atom1, atom2 in itertools.product(self.atomSelectionSet[4],
                                                  self.atomSelectionSet[5]):
                if isIdenticalRestraint([atom1, atom2]):
                    continue
                if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None):
                    continue
                if isinstance(combinationId, int):
                    combinationId += 1
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (XDIP) id={self.rdcRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 combinationId, None, None,
                                 sf['list_id'], self.__entryId, dstFunc,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom1, atom2)
                    sf['loop'].add_data(row)

        finally:
            self.numberSelection.clear()

    def validateRdcRange2(self, weight, misc_dict,
                          target_value_1, lower_limit_1, upper_limit_1,
                          target_value_2, lower_limit_2, upper_limit_2):
        """ Validate two RDC value ranges.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if isinstance(misc_dict, dict):
            for k, v in misc_dict.items():
                dstFunc[k] = v

        if RDC_ERROR_MIN < target_value_1 < RDC_ERROR_MAX:
            dstFunc['target_value_1'] = f"{target_value_1:.6f}"
        else:
            validRange = False
            self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                            f"The target value(1)='{target_value_1}' must be within range {RDC_RESTRAINT_ERROR}.")

        if RDC_ERROR_MIN <= lower_limit_1 < RDC_ERROR_MAX:
            dstFunc['lower_limit_1'] = f"{lower_limit_1:.6f}"
        else:
            validRange = False
            self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                            f"The lower limit value(1)='{lower_limit_1:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if RDC_ERROR_MIN < upper_limit_1 <= RDC_ERROR_MAX:
            dstFunc['upper_limit_1'] = f"{upper_limit_1:.6f}"
        else:
            validRange = False
            self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                            f"The upper limit value(1)='{upper_limit_1:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if RDC_ERROR_MIN < target_value_2 < RDC_ERROR_MAX:
            dstFunc['target_value_2'] = f"{target_value_2:.6f}"
        else:
            validRange = False
            self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                            f"The target value(2)='{target_value_2}' must be within range {RDC_RESTRAINT_ERROR}.")

        if RDC_ERROR_MIN <= lower_limit_2 < RDC_ERROR_MAX:
            dstFunc['lower_limit_2'] = f"{lower_limit_2:.6f}"
        else:
            validRange = False
            self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                            f"The lower limit value(2)='{lower_limit_2:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if RDC_ERROR_MIN < upper_limit_2 <= RDC_ERROR_MAX:
            dstFunc['upper_limit_2'] = f"{upper_limit_2:.6f}"
        else:
            validRange = False
            self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                            f"The upper limit value(2)='{upper_limit_2:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if lower_limit_1 > target_value_1:
            validRange = False
            self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                            f"The lower limit value(1)='{lower_limit_1:.6f}' must be less than the target value(1) '{target_value_1}'.")

        if upper_limit_1 < target_value_1:
            validRange = False
            self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                            f"The upper limit value(1)='{upper_limit_1:.6f}' must be greater than the target value(1) '{target_value_1}'.")

        if lower_limit_2 > target_value_2:
            validRange = False
            self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                            f"The lower limit value(2)='{lower_limit_2:.6f}' must be less than the target value(2) '{target_value_2}'.")

        if upper_limit_2 < target_value_2:
            validRange = False
            self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                            f"The upper limit value(2)='{upper_limit_2:.6f}' must be greater than the target value(2) '{target_value_2}'.")

        if not validRange:
            return None

        if RDC_RANGE_MIN <= target_value_1 <= RDC_RANGE_MAX:
            pass
        else:
            self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                            f"The target value(1)='{target_value_1}' should be within range {RDC_RESTRAINT_RANGE}.")

        if RDC_RANGE_MIN <= lower_limit_1 <= RDC_RANGE_MAX:
            pass
        else:
            self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                            f"The lower limit value(1)='{lower_limit_1:.6f}' should be within range {RDC_RESTRAINT_RANGE}.")

        if RDC_RANGE_MIN <= upper_limit_1 <= RDC_RANGE_MAX:
            pass
        else:
            self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                            f"The upper limit value(1)='{upper_limit_1:.6f}' should be within range {RDC_RESTRAINT_RANGE}.")

        if RDC_RANGE_MIN <= target_value_2 <= RDC_RANGE_MAX:
            pass
        else:
            self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                            f"The target value(2)='{target_value_2}' should be within range {RDC_RESTRAINT_RANGE}.")

        if RDC_RANGE_MIN <= lower_limit_2 <= RDC_RANGE_MAX:
            pass
        else:
            self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                            f"The lower limit value(2)='{lower_limit_2:.6f}' should be within range {RDC_RESTRAINT_RANGE}.")

        if RDC_RANGE_MIN <= upper_limit_2 <= RDC_RANGE_MAX:
            pass
        else:
            self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                            f"The upper limit value(2)='{upper_limit_2:.6f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        return dstFunc

    # Enter a parse tree produced by XplorMRParser#vean_statement.
    def enterVean_statement(self, ctx: XplorMRParser.Vean_statementContext):  # pylint: disable=no-self-use
        if ctx.Reset():
            pass

    # Exit a parse tree produced by XplorMRParser#vean_statement.
    def exitVean_statement(self, ctx: XplorMRParser.Vean_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (VEAN) classification={self.classification!r}")

    # Enter a parse tree produced by XplorMRParser#vean_assign.
    def enterVean_assign(self, ctx: XplorMRParser.Vean_assignContext):  # pylint: disable=unused-argument
        self.rdcStatements += 1
        self.__cur_subtype = 'rdc'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#vean_assign.
    def exitVean_assign(self, ctx: XplorMRParser.Vean_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            if len(self.numberSelection) > 3:
                center_1 = self.numberSelection[0]
                range_1 = abs(self.numberSelection[1])
                center_2 = self.numberSelection[2]
                range_2 = abs(self.numberSelection[3])
            else:
                center_1 = self.numberSelection[0]
                range_1 = 0.0
                center_2 = self.numberSelection[1]
                range_2 = 0.0

            target_value_1 = center_1
            target_value_2 = center_2
            lower_limit_1 = center_1 - range_1
            upper_limit_1 = center_1 + range_1
            lower_limit_2 = center_2 - range_2
            upper_limit_2 = center_2 + range_2

            dstFunc = self.validateAngleRange2(self.scale,
                                               target_value_1, lower_limit_1, upper_limit_1,
                                               target_value_2, lower_limit_2, upper_limit_2)

            if self.__createSfDict:
                dstFunc = self.validateAngleRange(self.scale, {'potential': self.potential},
                                                  target_value_1, lower_limit_1, upper_limit_1)
                dstFunc2 = self.validateAngleRange(self.scale, {'potential': self.potential},
                                                   target_value_2, lower_limit_2, upper_limit_2)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            if not self.areUniqueCoordAtoms('an RDC (VEAN)'):
                if len(self.__g) > 0:
                    self.__f.extend(self.__g)
                return

            for i in range(0, 4, 2):
                chain_id_1 = self.atomSelectionSet[i][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[i][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[i][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[i][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[i + 1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[i + 1][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[i + 1][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[i + 1][0]['atom_id']

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
                                            "Found an RDC vector over multiple covalent bonds in the 'VEANgle' statement; "
                                            f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                            return

            if self.__createSfDict:
                self.__cur_subtype = 'dihed'
                sf = self.__getSf(constraintType='intervector projection angle',
                                  potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                self.__cur_subtype = 'rdc'
                sf['id'] += 1

            for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                self.atomSelectionSet[1],
                                                                self.atomSelectionSet[2],
                                                                self.atomSelectionSet[3]):
                if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None)\
                   or isLongRangeRestraint([atom3, atom4], self.__polySeq if self.__gapInAuthSeq else None):
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (VEAN) id={self.rdcRestraints} "
                          f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    self.__cur_subtype = 'dihed'
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 1, None, 'VEANgle',
                                 sf['list_id'], self.__entryId, dstFunc,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom1, atom2, atom3, atom4)
                    sf['loop'].add_data(row)
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 2, None, 'VEANgle',
                                 sf['list_id'], self.__entryId, dstFunc2,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom1, atom2, atom3, atom4)
                    sf['loop'].add_data(row)
                    self.__cur_subtype = 'rdc'

        finally:
            self.numberSelection.clear()

    def validateAngleRange2(self, weight,
                            target_value_1, lower_limit_1, upper_limit_1,
                            target_value_2, lower_limit_2, upper_limit_2):
        """ Validate two angle value ranges.
        """

        validRange = True
        dstFunc = {'weight': weight, 'potential': self.potential}

        if ANGLE_ERROR_MIN < target_value_1 < ANGLE_ERROR_MAX:
            dstFunc['target_value_1'] = f"{target_value_1}"
        else:
            validRange = False
            self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                            f"The target value(1)='{target_value_1}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if ANGLE_ERROR_MIN <= lower_limit_1 < ANGLE_ERROR_MAX:
            dstFunc['lower_limit_1'] = f"{lower_limit_1:.3f}"
        else:
            validRange = False
            self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                            f"The lower limit value(1)='{lower_limit_1:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if ANGLE_ERROR_MIN < upper_limit_1 <= ANGLE_ERROR_MAX:
            dstFunc['upper_limit_1'] = f"{upper_limit_1:.3f}"
        else:
            validRange = False
            self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                            f"The upper limit value(1)='{upper_limit_1:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if ANGLE_ERROR_MIN < target_value_2 < ANGLE_ERROR_MAX:
            dstFunc['target_value_2'] = f"{target_value_2}"
        else:
            validRange = False
            self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                            f"The target value(2)='{target_value_2}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if ANGLE_ERROR_MIN <= lower_limit_2 < ANGLE_ERROR_MAX:
            dstFunc['lower_limit_2'] = f"{lower_limit_2:.3f}"
        else:
            validRange = False
            self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                            f"The lower limit value(2)='{lower_limit_2:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if ANGLE_ERROR_MIN < upper_limit_2 <= ANGLE_ERROR_MAX:
            dstFunc['upper_limit_2'] = f"{upper_limit_2:.3f}"
        else:
            validRange = False
            self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                            f"The upper limit value(2)='{upper_limit_2:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if not validRange:
            return None

        if ANGLE_RANGE_MIN <= target_value_1 <= ANGLE_RANGE_MAX:
            pass
        else:
            self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                            f"The target value(1)='{target_value_1}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if ANGLE_RANGE_MIN <= lower_limit_1 <= ANGLE_RANGE_MAX:
            pass
        else:
            self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                            f"The lower limit value(1)='{lower_limit_1:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if ANGLE_RANGE_MIN <= upper_limit_1 <= ANGLE_RANGE_MAX:
            pass
        else:
            self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                            f"The upper limit value(1)='{upper_limit_1:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if ANGLE_RANGE_MIN <= target_value_2 <= ANGLE_RANGE_MAX:
            pass
        else:
            self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                            f"The target value(2)='{target_value_2}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if ANGLE_RANGE_MIN <= lower_limit_2 <= ANGLE_RANGE_MAX:
            pass
        else:
            self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                            f"The lower limit value(2)='{lower_limit_2:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if ANGLE_RANGE_MIN <= upper_limit_2 <= ANGLE_RANGE_MAX:
            pass
        else:
            self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                            f"The upper limit value(2)='{upper_limit_2:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        return dstFunc

    # Enter a parse tree produced by XplorMRParser#tenso_statement.
    def enterTenso_statement(self, ctx: XplorMRParser.Tenso_statementContext):
        if ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.potential = 'square'
            elif code.startswith('HARM'):
                self.potential = 'harmonic'
            else:
                self.potential = 'square'
                self.__f.append("[Enum mismatch ignorable] "
                                f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for 'TENSOr' statements. "
                                f"Instead, set the default potential {self.potential!r}.")

        elif ctx.Reset():
            self.potential = 'square'
            self.coefficients = None

        elif ctx.Coefficients():
            self.coefficients = {'DFS': self.getNumber_s(ctx.number_s())
                                 }

    # Exit a parse tree produced by XplorMRParser#tenso_statement.
    def exitTenso_statement(self, ctx: XplorMRParser.Tenso_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (TENSO) classification={self.classification!r} "
                  f"coefficients={self.coefficients}")

    # Enter a parse tree produced by XplorMRParser#tenso_assign.
    def enterTenso_assign(self, ctx: XplorMRParser.Tenso_assignContext):  # pylint: disable=unused-argument
        self.rdcRestraints += 1
        self.__cur_subtype = 'rdc'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#tenso_assign.
    def exitTenso_assign(self, ctx: XplorMRParser.Tenso_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            target = self.numberSelection[0]

            if len(self.numberSelection) > 1:
                delta = abs(self.numberSelection[1])
            else:
                delta = 0.0

            target_value = target
            lower_limit = None
            upper_limit = None

            if self.potential == 'square' and delta > 0.0:
                lower_limit = target - delta
                upper_limit = target + delta

            dstFunc = self.validateRdcRange(1.0, {'potential': self.potential},
                                            target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return
            """
            if not self.areUniqueCoordAtoms('an RDC (TENSO)'):
                if len(self.__g) > 0:
                    self.__f.extend(self.__g)
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
                if not self.areUniqueCoordAtoms('an RDC (TENSO)'):
                    if len(self.__g) > 0:
                        self.__f.extend(self.__g)
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
                                        "Found an RDC vector over multiple covalent bonds in the 'TENSOr' statement; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

            combinationId = '.'
            if self.__createSfDict:
                sf = self.__getSf(potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc),
                                  rdcCode=getRdcCode([self.atomSelectionSet[0][0], self.atomSelectionSet[1][0]]))
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
                    print(f"subtype={self.__cur_subtype} (TENSO) id={self.rdcRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 combinationId, None, None,
                                 sf['list_id'], self.__entryId, dstFunc,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom1, atom2)
                    sf['loop'].add_data(row)

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by XplorMRParser#anis_statement.
    def enterAnis_statement(self, ctx: XplorMRParser.Anis_statementContext):
        if ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.potential = 'square'
            elif code.startswith('HARM'):
                self.potential = 'harmonic'
            else:
                self.potential = 'square'
                self.__f.append("[Enum mismatch ignorable] "
                                f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'ANISotropy' statements. "
                                f"Instead, set the default potential {self.potential!r}.")

        elif ctx.Reset():
            self.potential = 'square'
            self.coefficients = None

        elif ctx.Coefficients():
            self.coefficients = {'a0': self.getNumber_s(ctx.number_s(0)),
                                 'a1': self.getNumber_s(ctx.number_s(1)),
                                 'a2': self.getNumber_s(ctx.number_s(2)),
                                 'a3': self.getNumber_s(ctx.number_s(3))
                                 }

    # Exit a parse tree produced by XplorMRParser#anis_statement.
    def exitAnis_statement(self, ctx: XplorMRParser.Anis_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (ANIS) classification={self.classification!r} "
                  f"coefficients={self.coefficients}")

    # Enter a parse tree produced by XplorMRParser#anis_assign.
    def enterAnis_assign(self, ctx: XplorMRParser.Anis_assignContext):  # pylint: disable=unused-argument
        self.rdcRestraints += 1
        self.__cur_subtype = 'rdc'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#anis_assign.
    def exitAnis_assign(self, ctx: XplorMRParser.Anis_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            target = self.numberSelection[0]

            if len(self.numberSelection) > 1:
                delta = abs(self.numberSelection[1])
            else:
                delta = 0.0

            target_value = target
            lower_limit = None
            upper_limit = None

            if self.potential == 'square' and delta > 0.0:
                lower_limit = target - delta
                upper_limit = target + delta

            dstFunc = self.validateRdcRange(1.0, {'potential': self.potential},
                                            target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            if not self.areUniqueCoordAtoms('an RDC (ANIS)'):
                if len(self.__g) > 0:
                    self.__f.extend(self.__g)
                return

            for i in range(0, 4, 2):
                chain_id_1 = self.atomSelectionSet[i][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[i][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[i][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[i][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[i + 1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[i + 1][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[i + 1][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[i + 1][0]['atom_id']

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
                                            "Found an RDC vector over multiple covalent bonds in the 'ANISotropy' statement; "
                                            f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                            return

            if self.__createSfDict:
                self.__cur_subtype = 'dihed'
                sf = self.__getSf(constraintType='intervector projection angle',
                                  potentialType=getPotentialType(self.__file_type, self.__cur_subtype, dstFunc))
                self.__cur_subtype = 'rdc'
                sf['id'] += 1

            for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                self.atomSelectionSet[1],
                                                                self.atomSelectionSet[2],
                                                                self.atomSelectionSet[3]):
                if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.__polySeq if self.__gapInAuthSeq else None):
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (ANIS) id={self.rdcRestraints} "
                          f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    self.__cur_subtype = 'dihed'
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, 'ANISotropy',
                                 sf['list_id'], self.__entryId, dstFunc,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom1, atom2, atom3, atom4)
                    sf['loop'].add_data(row)
                    self.__cur_subtype = 'rdc'

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by XplorMRParser#planar_statement.
    def enterPlanar_statement(self, ctx: XplorMRParser.Planar_statementContext):
        if ctx.Initialize():
            self.planeWeight = 300.0

    # Exit a parse tree produced by XplorMRParser#planar_statement.
    def exitPlanar_statement(self, ctx: XplorMRParser.Planar_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#planar_group.
    def enterPlanar_group(self, ctx: XplorMRParser.Planar_groupContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#planar_group.
    def exitPlanar_group(self, ctx: XplorMRParser.Planar_groupContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#group_statement.
    def enterGroup_statement(self, ctx: XplorMRParser.Group_statementContext):
        self.planeRestraints += 1
        if self.__cur_subtype != 'plane':
            self.planeStatements += 1
        self.__cur_subtype = 'plane'

        self.atomSelectionSet.clear()
        self.__g.clear()

        if ctx.Weight():
            self.planeWeight = self.getNumber_s(ctx.number_s())
            if isinstance(self.planeWeight, str):
                if self.planeWeight in self.evaluate:
                    self.planeWeight = self.evaluate[self.planeWeight]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The weight value 'GROUP {str(ctx.Weight())}={self.planeWeight} END' "
                                    f"where the symbol {self.planeWeight!r} is not defined so that set the default value.")
                    self.planeWeight = 300.0
            if self.planeWeight < 0.0:
                self.__f.append("[Invalid data] "
                                f"The weight value 'GROUP {str(ctx.Weight())}={self.planeWeight} END' must not be a negative value.")
            elif self.planeWeight == 0.0:
                self.__f.append("[Range value warning] "
                                f"The weight value 'GROUP {str(ctx.Weight())}={self.planeWeight} END' should be a positive value.")

    # Exit a parse tree produced by XplorMRParser#group_statement.
    def exitGroup_statement(self, ctx: XplorMRParser.Group_statementContext):  # pylint: disable=unused-argument
        if not self.__hasPolySeq and not self.__hasNonPolySeq:
            return

        if len(self.atomSelectionSet) == 0:
            return

        if self.__createSfDict:
            software_name = 'XPLOR-NIH/CNS' if self.__remediate else 'XPLOR-NIH'
            sf = self.__getSf(f'planarity restraint, {software_name} PLANAR/GROUP statement')
            sf['id'] += 1
            if len(sf['loop']['tags']) == 0:
                sf['loop']['tags'] = ['index_id', 'id',
                                      'auth_asym_id', 'auth_seq_id', 'auth_comp_id', 'auth_atom_id',
                                      'list_id', 'entry_id']
                sf['tags'].append(['weight', self.planeWeight])

        for atom1 in self.atomSelectionSet[0]:
            if self.__debug:
                print(f"subtype={self.__cur_subtype} (PLANAR/GROUP) id={self.planeRestraints} "
                      f"atom={atom1} weight={self.scale}")
            if self.__createSfDict and sf is not None:
                sf['index_id'] += 1
                sf['loop']['data'].append([sf['index_id'], sf['id'],
                                           atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                           sf['list_id'], self.__entryId])

    # Enter a parse tree produced by XplorMRParser#harmonic_statement.
    def enterHarmonic_statement(self, ctx: XplorMRParser.Harmonic_statementContext):
        if ctx.Exponent():
            self.squareExponent = int(str(ctx.Integer()))
            if self.squareExponent <= 0.0:
                self.__f.append("[Invalid data] "
                                f"The exponent value 'RESTRAINTS HARMONIC {str(ctx.Exponent())}={self.squareExponent} END' must be a positive value.")

        elif ctx.Normal():
            if ctx.number_s(0):
                self.vector3D = [self.getNumber_s(ctx.number_s(0)),
                                 self.getNumber_s(ctx.number_s(1)),
                                 self.getNumber_s(ctx.number_s(2))]

            elif ctx.Tail():
                self.inVector3D = True
                self.inVector3D_columnSel = -1
                self.inVector3D_tail = None
                self.inVector3D_head = None
                self.vector3D = None

    # Exit a parse tree produced by XplorMRParser#harmonic_statement.
    def exitHarmonic_statement(self, ctx: XplorMRParser.Harmonic_statementContext):  # pylint: disable=unused-argument
        if self.vector3D is None:
            self.vector3D = [0.0] * 3  # set default vector if not available

        if 'harm' not in self.vectorDo or len(self.vector3D['harm']) == 0:
            self.__f.append("[Invalid data] "
                            "No vector statement for harmonic coordinate restraints exists.")
            return

        for col, vector in enumerate(self.vector3D['harm'], start=1):
            dstFunc = {}
            if 'value' in vector:
                dstFunc['energy_const'] = vector['value']
            dstFunc['exponent'] = self.squareExponent
            for atom1 in vector['atom_selection']:
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (HARM) id={col} "
                          f"atom={atom1} {dstFunc} normal_vector={self.vector3D}")

        self.vector3D['harm'] = []

    # Enter a parse tree produced by XplorMRParser#harmonic_assign.
    def enterHarmonic_assign(self, ctx: XplorMRParser.Harmonic_assignContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1
        if self.__cur_subtype != 'geo':
            self.geoStatements += 1
        self.__cur_subtype = 'geo'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#harmonic_assign.
    def exitHarmonic_assign(self, ctx: XplorMRParser.Harmonic_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            self.vector3D = [self.numberSelection[0], self.numberSelection[1], self.numberSelection[2]]

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            for atom1 in self.atomSelectionSet[0]:
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (HARM) id={self.geoRestraints} "
                          f"atom={atom1} normal_vector={self.vector3D}")

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by XplorMRParser#antidistance_statement.
    def enterAntidistance_statement(self, ctx: XplorMRParser.Antidistance_statementContext):
        if ctx.Reset():
            self.adistExpectGrid = None
            self.adistExpectValue = 0.0
            self.adistSizeMaxDist = 10.0
            self.adistSizeStep = None
            self.adistForceConst = 1.0

        elif ctx.Expectation():
            self.adistExpectValue = self.getNumber_s(ctx.number_s())
            if isinstance(self.adistExpectValue, str):
                if self.adistExpectValue in self.evaluate:
                    self.adistExpectValue = self.evaluate[self.adistExpectValue]
                else:
                    self.__f.append("[Invalid data] "
                                    f"The symbol {self.adistExpectValue!r} in the 'XADC' statement is not defined.")
                    return

            if 0.0 <= self.adistExpectValue <= 1.0:
                pass
            else:
                self.__f.append("[Range value error] "
                                f"The expectation distance 'XADC {str(ctx.Expectation())} {str(ctx.Integer())} {self.adistExpectValue} END' "
                                f"must be within range {PROBABILITY_RANGE}.")

            self.adistExpectGrid = int(str(ctx.Integer()))

        elif ctx.Size():
            self.adistSizeMaxDist = self.getNumber_s(ctx.number_s())
            if isinstance(self.adistSizeMaxDist, str):
                if self.adistSizeMaxDist in self.evaluate:
                    self.adistSizeMaxDist = self.evaluate[self.adistSizeMaxDist]
                else:
                    self.__f.append("[Invalid data] "
                                    f"The symbol {self.adistSizeMaxDist!r} in the 'XADC' statement is not defined.")
                    return

            if DIST_ERROR_MIN < self.adistSizeMaxDist < DIST_ERROR_MAX:
                pass
            else:
                self.__f.append("[Range value error] "
                                f"The expectation distance 'XADC {str(ctx.Size())} {self.adistSizeMaxDist} {str(ctx.Integer())} END' "
                                f"must be within range {DIST_RESTRAINT_ERROR}.")

            self.adistSizeStep = int(str(ctx.Integer()))

        elif ctx.ForceConstant():
            self.adistForceConst = self.getNumber_s(ctx.number_s())

    # Exit a parse tree produced by XplorMRParser#antidistance_statement.
    def exitAntidistance_statement(self, ctx: XplorMRParser.Antidistance_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (XADC) classification={self.classification!r} "
                  f"expectation={self.adistExpectGrid} {self.adistExpectValue} "
                  f"size={self.adistSizeMaxDist} {self.adistSizeStep} "
                  f"force_constant={self.adistForceConst}")

    # Enter a parse tree produced by XplorMRParser#xadc_assign.
    def enterXadc_assign(self, ctx: XplorMRParser.Xadc_assignContext):  # pylint: disable=unused-argument
        self.adistRestraints += 1
        if self.__cur_subtype != 'adist':
            self.adistStatements += 1
        self.__cur_subtype = 'adist'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#xadc_assign.
    def exitXadc_assign(self, ctx: XplorMRParser.Xadc_assignContext):  # pylint: disable=unused-argument
        if not self.__hasPolySeq and not self.__hasNonPolySeq:
            return

        if self.__createSfDict:
            sf = self.__getSf('anti-distance restraint, XPLOR-NIH XADC statement')
            sf['id'] += 1
            if len(sf['loop']['tags']) == 0:
                sf['loop']['tags'] = ['index_id', 'id',
                                      'auth_asym_id_1', 'auth_seq_id_1', 'auth_comp_id_1', 'auth_atom_id_1',
                                      'auth_asym_id_2', 'auth_seq_id_2', 'auth_comp_id_2', 'auth_atom_id_2',
                                      'list_id', 'entry_id']
                sf['tags'].append(['classification', self.classification])
                sf['tags'].append(['expect_grid', self.adistExpectGrid])
                sf['tags'].append(['expect_value', self.adistExpectValue])
                sf['tags'].append(['max_distance', self.adistSizeMaxDist])
                sf['tags'].append(['num_of_bins', self.adistSizeStep])
                sf['tags'].append(['force_constant', self.adistForceConst])

        for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                              self.atomSelectionSet[1]):
            if isIdenticalRestraint([atom1, atom2]):
                continue
            if self.__debug:
                print(f"subtype={self.__cur_subtype} (XADC) id={self.adistRestraints} "
                      f"atom1={atom1} atom2={atom2} "
                      f"expectaion_value={self.adistExpectValue} max_distance={self.adistSizeMaxDist} force_constant={self.adistForceConst}")
            if self.__createSfDict and sf is not None:
                sf['index_id'] += 1
                sf['loop']['data'].append([sf['index_id'], sf['id'],
                                           atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                           atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id'],
                                           sf['list_id'], self.__entryId])

    # Enter a parse tree produced by XplorMRParser#coupling_statement.
    def enterCoupling_statement(self, ctx: XplorMRParser.Coupling_statementContext):
        if ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.potential = 'square'
            elif code.startswith('HARM'):
                self.potential = 'harmonic'
            else:
                self.potential = 'square'
                self.__f.append("[Enum mismatch ignorable] "
                                f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'COUPling' statements. "
                                f"Instead, set the default potential {self.potential!r}.")

        elif ctx.Reset():
            self.potential = 'square'
            self.coefficients = None

        elif ctx.Coefficients():
            self.coefficients = {'Karplus_coef_a': self.getNumber_s(ctx.number_s(0)),
                                 'Karplus_coef_b': self.getNumber_s(ctx.number_s(1)),
                                 'Karplus_coef_c': self.getNumber_s(ctx.number_s(2)),
                                 'Karplus_phase': self.getNumber_s(ctx.number_s(3))
                                 }

    # Exit a parse tree produced by XplorMRParser#coupling_statement.
    def exitCoupling_statement(self, ctx: XplorMRParser.Coupling_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (COUP) classification={self.classification!r} "
                  f"coefficients={self.coefficients}")

    # Enter a parse tree produced by XplorMRParser#coup_assign.
    def enterCoup_assign(self, ctx: XplorMRParser.Coup_assignContext):  # pylint: disable=unused-argument
        self.jcoupRestraints += 1
        self.__cur_subtype_altered = self.__cur_subtype != 'jcoup'
        self.__cur_subtype = 'jcoup' if self.__cur_subtype != 'rdc' else 'rdc'  # set 'rdc' for error message

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#coup_assign.
    def exitCoup_assign(self, ctx: XplorMRParser.Coup_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            target = self.numberSelection[0]
            delta = abs(self.numberSelection[1])

            target_value = target
            lower_limit = None
            upper_limit = None

            if len(self.atomSelectionSet) == 4 and self.__hasPolySeq and not self.__in_block:

                try:
                    atom_id_1 = self.atomSelectionSet[0][0]['atom_id']
                    atom_id_2 = self.atomSelectionSet[1][0]['atom_id']
                    atom_id_3 = self.atomSelectionSet[2][0]['atom_id']
                    atom_id_4 = self.atomSelectionSet[3][0]['atom_id']

                    if atom_id_1 == atom_id_3 and atom_id_2 == atom_id_4:
                        self.jcoupRestraints -= 1
                        self.rdcRestraints += 1
                        if self.__cur_subtype_altered:
                            self.jcoupStatements -= 1
                            if self.rdcStatements == 0:
                                self.rdcStatements += 1
                        self.__cur_subtype = 'rdc'
                        self.exitVean_assign(ctx)
                        return
                except IndexError:
                    self.jcoupRestraints -= 1
                    self.rdcRestraints += 1
                    if self.__cur_subtype_altered:
                        self.jcoupStatements -= 1
                        if self.rdcStatements == 0:
                            self.rdcStatements += 1
                    self.__cur_subtype = 'rdc'
                    self.exitVean_assign(ctx)
                    return

            self.__cur_subtype = 'jcoup'  # to get consistent number of statement

            if self.__cur_subtype_altered:
                self.jcoupStatements += 1

            if not self.__hasPolySeq and not self.__hasNonPolySeq:  # can't decide whether VEAN or COUP wo the coordinates
                return

            if self.potential != 'harmonic' and delta > 0.0:
                lower_limit = target - delta
                upper_limit = target + delta

            dstFunc = self.validateRdcRange(1.0, {'potential': self.potential},
                                            target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            dstFunc2 = None

            if len(self.numberSelection) > 3:
                target = self.numberSelection[2]
                delta = abs(self.numberSelection[3])

                target_value = target
                lower_limit = None
                upper_limit = None

                if self.potential != 'harmonic' and delta > 0.0:
                    lower_limit = target - delta
                    upper_limit = target + delta

                dstFunc2 = self.validateRdcRange(1.0, {'potential': self.potential},
                                                 target_value, lower_limit, upper_limit)

                if dstFunc2 is None:
                    return

            if not self.areUniqueCoordAtoms('a J-coupling (COUP)'):
                if len(self.__g) > 0:
                    self.__f.extend(self.__g)
                return

            for i in range(0, len(self.atomSelectionSet), 4):
                chain_id_1 = self.atomSelectionSet[i][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[i][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[i][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[i][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[i + 3][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[i + 3][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[i + 3][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[i + 3][0]['atom_id']

                if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    f"Non-magnetic susceptible spin appears in J-coupling vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                    f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

                if chain_id_1 != chain_id_2:
                    ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                    ps2 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                    if ps1 is None and ps2 is None:
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found inter-chain J-coupling vector; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif abs(seq_id_1 - seq_id_2) > 1:

                    if abs(seq_id_1 - seq_id_2) > 2 or {atom_id_1, atom_id_2} != {'H', 'N'}:
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found inter-residue J-coupling vector; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif abs(seq_id_1 - seq_id_2) == 1:

                    if self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                            ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in jcoupBbPairCode)
                             or (seq_id_1 > seq_id_2 and atom_id_1 in jcoupBbPairCode and atom_id_2 == 'C')
                             or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 == 'H')
                             or (seq_id_1 > seq_id_2 and atom_id_1 == 'H' and atom_id_2.startswith('HA'))
                             or {atom_id_1, atom_id_2} == {'H', 'N'}):
                        pass

                    else:
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found inter-residue J-coupling vector; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif atom_id_1 == atom_id_2:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Found zero J-coupling vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            if self.__createSfDict:
                sf = self.__getSf(self.classification)
                sf['id'] += 1

            if len(self.atomSelectionSet) == 4:
                for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                    self.atomSelectionSet[1],
                                                                    self.atomSelectionSet[2],
                                                                    self.atomSelectionSet[3]):
                    if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.__polySeq if self.__gapInAuthSeq else None):
                        if {atom1['atom_id'], atom4['atom_id']} != {'H', 'N'}:
                            continue
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} (COUP) id={self.jcoupRestraints} "
                              f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.__entryId, dstFunc,
                                     self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                     atom1, atom2, atom3, atom4)
                        sf['loop'].add_data(row)

            else:
                for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                    self.atomSelectionSet[1],
                                                                    self.atomSelectionSet[2],
                                                                    self.atomSelectionSet[3]):
                    if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.__polySeq if self.__gapInAuthSeq else None):
                        if {atom1['atom_id'], atom4['atom_id']} != {'H', 'N'}:
                            continue
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} (COUP) id={self.jcoupRestraints} "
                              f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.__entryId, dstFunc,
                                     self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                     atom1, atom2, atom3, atom4)
                        sf['loop'].add_data(row)

                for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[4],
                                                                    self.atomSelectionSet[5],
                                                                    self.atomSelectionSet[6],
                                                                    self.atomSelectionSet[7]):
                    if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.__polySeq if self.__gapInAuthSeq else None):
                        if {atom1['atom_id'], atom4['atom_id']} != {'H', 'N'}:
                            continue
                    if self.__debug:
                        if dstFunc2 is None:
                            print(f"subtype={self.__cur_subtype} (COUP) id={self.jcoupRestraints} "
                                  f"atom4={atom1} atom5={atom2} atom6={atom3} atom7={atom4} {dstFunc}")
                        else:
                            print(f"subtype={self.__cur_subtype} (COUP) id={self.jcoupRestraints} "
                                  f"atom4={atom1} atom5={atom2} atom6={atom3} atom7={atom4} {dstFunc2}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.__entryId, dstFunc if dstFunc2 is None else dstFunc2,
                                     self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                     atom1, atom2, atom3, atom4)
                        sf['loop'].add_data(row)

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by XplorMRParser#carbon_shift_statement.
    def enterCarbon_shift_statement(self, ctx: XplorMRParser.Carbon_shift_statementContext):
        if ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.potential = 'square'
            elif code.startswith('HARM'):
                self.potential = 'harmonic'
            else:
                self.potential = 'square'
                self.__f.append("[Enum mismatch ignorable] "
                                f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'CARBon' statements. "
                                f"Instead, set the default potential {self.potential!r}.")

        elif ctx.Reset():
            self.potential = 'square'

        elif ctx.Expectation():
            self.csExpect = {'psi_position': int(str(ctx.Integer(0))),
                             'phi_poistion': int(str(ctx.Integer(1))),
                             'ca_shift': self.getNumber_s(ctx.number_s(0)),
                             'ca_shift_error': self.getNumber_s(ctx.number_s(1)),
                             'cb_shift': self.getNumber_s(ctx.number_s(2)),
                             'cb_shift_error': self.getNumber_s(ctx.number_s(3))
                             }

    # Exit a parse tree produced by XplorMRParser#carbon_shift_statement.
    def exitCarbon_shift_statement(self, ctx: XplorMRParser.Carbon_shift_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (CARB) classification={self.classification!r} "
                  f"expectation={self.csExpect}")

    # Enter a parse tree produced by XplorMRParser#carbon_shift_assign.
    def enterCarbon_shift_assign(self, ctx: XplorMRParser.Carbon_shift_assignContext):  # pylint: disable=unused-argument
        self.hvycsRestraints += 1
        self.__cur_subtype = 'hvycs'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#carbon_shift_assign.
    def exitCarbon_shift_assign(self, ctx: XplorMRParser.Carbon_shift_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            ca_shift = self.numberSelection[0]
            cb_shift = self.numberSelection[1]

            if CS_ERROR_MIN < ca_shift < CS_ERROR_MAX:
                pass
            else:
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"CA chemical shift value '{ca_shift}' must be within range {CS_RESTRAINT_ERROR}.")
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            if not self.areUniqueCoordAtoms('a carbon chemical shift (CARB)'):
                if len(self.__g) > 0:
                    self.__f.extend(self.__g)
                return

            dstFunc = {'ca_shift': ca_shift, 'cb_shift': cb_shift, 'weight': 1.0, 'potential': self.potential}

            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

            chain_id_3 = self.atomSelectionSet[2][0]['chain_id']
            seq_id_3 = self.atomSelectionSet[2][0]['seq_id']
            atom_id_3 = self.atomSelectionSet[2][0]['atom_id']

            chain_id_4 = self.atomSelectionSet[3][0]['chain_id']
            seq_id_4 = self.atomSelectionSet[3][0]['seq_id']
            atom_id_4 = self.atomSelectionSet[3][0]['atom_id']

            chain_id_5 = self.atomSelectionSet[4][0]['chain_id']
            seq_id_5 = self.atomSelectionSet[4][0]['seq_id']
            atom_id_5 = self.atomSelectionSet[4][0]['atom_id']

            chain_ids = [chain_id_1, chain_id_2, chain_id_3, chain_id_4, chain_id_5]
            seq_ids = [seq_id_1, seq_id_2, seq_id_3, seq_id_4, seq_id_5]
            offsets = [seq_id - seq_id_3 for seq_id in seq_ids]
            atom_ids = [atom_id_1, atom_id_2, atom_id_3, atom_id_4, atom_id_5]

            if chain_ids != [chain_id_1] * 5 or offsets != [-1, 0, 0, 0, 1] or atom_ids != ['C', 'N', 'CA', 'C', 'N']:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "The atom selection order must be [C(i-1), N(i), CA(i), C(i), N(i+1)].")
                return

            comp_id = self.atomSelectionSet[2][0]['comp_id']

            if comp_id == 'GLY':
                del dstFunc['cb_shift']

            else:

                if CS_ERROR_MIN < cb_shift < CS_ERROR_MAX:
                    pass
                else:
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"CB chemical shift value '{ca_shift}' must be within range {CS_RESTRAINT_ERROR}.")
                    return

            if self.__createSfDict:
                sf = self.__getSf(self.classification)
                sf['id'] += 1

            for atom1, atom2, atom3, atom4, atom5 in itertools.product(self.atomSelectionSet[0],
                                                                       self.atomSelectionSet[1],
                                                                       self.atomSelectionSet[2],
                                                                       self.atomSelectionSet[3],
                                                                       self.atomSelectionSet[4]):
                if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.__polySeq if self.__gapInAuthSeq else None):
                    continue
                if isLongRangeRestraint([atom2, atom3, atom4, atom5], self.__polySeq if self.__gapInAuthSeq else None):
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (CARB) id={self.hvycsRestraints} "
                          f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} atom5={atom5} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, None,
                                 sf['list_id'], self.__entryId, dstFunc,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom1, atom2, atom3, atom4, atom5)
                    sf['loop'].add_data(row)

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by XplorMRParser#carbon_shift_rcoil.
    def enterCarbon_shift_rcoil(self, ctx: XplorMRParser.Carbon_shift_rcoilContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#carbon_shift_rcoil.
    def exitCarbon_shift_rcoil(self, ctx: XplorMRParser.Carbon_shift_rcoilContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            rcoil_a = self.numberSelection[0]
            rcoil_b = self.numberSelection[1]

            if CS_ERROR_MIN < rcoil_a < CS_ERROR_MAX:
                pass
            else:
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"Random coil 'a' chemical shift value '{rcoil_a}' must be within range {CS_RESTRAINT_ERROR}.")
                return

            if CS_ERROR_MIN < rcoil_b < CS_ERROR_MAX:
                pass
            else:
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"Random coil 'b' chemical shift value '{rcoil_b}' must be within range {CS_RESTRAINT_ERROR}.")
                return

            dstFunc = {'rcoil_a': rcoil_a, 'rcoil_b': rcoil_b}

            for atom1 in self.atomSelectionSet[0]:
                if atom1['atom_id'][0] != 'C':
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    f"Not a carbon; {atom1}.")
                    return

            for atom1 in self.atomSelectionSet[0]:
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (CARB/RCOI) id={self.hvycsRestraints} "
                          f"atom={atom1} {dstFunc}")

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by XplorMRParser#proton_shift_statement.
    def enterProton_shift_statement(self, ctx: XplorMRParser.Proton_shift_statementContext):
        if ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.potential = 'square'
            elif code.startswith('HARM'):
                self.potential = 'harmonic'
            else:
                self.potential = 'square'
                self.__f.append("[Enum mismatch ignorable] "
                                f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'PROTONshift' statements. "
                                f"Instead, set the default potential {self.potential!r}.")

        elif ctx.Reset():
            self.potential = 'square'
            self.coefficients = None

    # Exit a parse tree produced by XplorMRParser#proton_shift_statement.
    def exitProton_shift_statement(self, ctx: XplorMRParser.Proton_shift_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (PROTON) classification={self.classification!r}")

    # Enter a parse tree produced by XplorMRParser#observed.
    def enterObserved(self, ctx: XplorMRParser.ObservedContext):  # pylint: disable=unused-argument
        self.procsRestraints += 1
        self.__cur_subtype = 'procs'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#observed.
    def exitObserved(self, ctx: XplorMRParser.ObservedContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            obs_value = self.numberSelection[0]

            obs_value_2 = None
            if len(self.numberSelection) > 1:
                obs_value_2 = self.numberSelection[1]

            if CS_ERROR_MIN < obs_value < CS_ERROR_MAX:
                pass
            else:
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The observed chemical shift value '{obs_value}' must be within range {CS_RESTRAINT_ERROR}.")
                return

            if obs_value_2 is not None:
                if CS_ERROR_MIN < obs_value_2 < CS_ERROR_MAX:
                    pass
                else:
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The 2nd observed chemical shift value '{obs_value_2}' must be within range {CS_RESTRAINT_ERROR}.")
                    return

            if obs_value_2 is None:
                dstFunc = {'obs_value': obs_value}
            else:
                dstFunc = {'obs_value': obs_value, 'obs_value_2': obs_value_2}

            lenAtomSelectionSet = len(self.atomSelectionSet)

            if obs_value_2 is None and lenAtomSelectionSet == 2:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Missing observed chemical shift value for the 2nd atom selection.")
                return

            if obs_value_2 is not None and lenAtomSelectionSet == 1:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"Missing 2nd atom selection for the observed chemical shift value '{obs_value_2}'.")
                return

            for atom1 in self.atomSelectionSet[0]:
                if atom1['atom_id'][0] not in protonBeginCode:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    f"Not a proton; {atom1}.")
                return

            if self.__createSfDict:
                sf = self.__getSf(self.classification)
                sf['id'] += 1

            if lenAtomSelectionSet == 1:
                for atom1 in self.atomSelectionSet[0]:
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} (PROTON/OBSE) id={self.procsRestraints} "
                              f"atom={atom1} {dstFunc}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.__entryId, dstFunc,
                                     self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                     atom1)
                        sf['loop'].add_data(row)

            else:
                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} (PROTON/OBSE) id={self.procsRestraints} "
                              f"atom1={atom1} atom2={atom2} {dstFunc}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     1, None, '.',
                                     sf['list_id'], self.__entryId, dstFunc,
                                     self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                     atom1)
                        sf['loop'].add_data(row)
                        #
                        sf['index_id'] += 1
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     2, None, '.',
                                     sf['list_id'], self.__entryId, dstFunc,
                                     self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                     None, atom2)
                        sf['loop'].add_data(row)

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by XplorMRParser#proton_shift_rcoil.
    def enterProton_shift_rcoil(self, ctx: XplorMRParser.Proton_shift_rcoilContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#proton_shift_rcoil.
    def exitProton_shift_rcoil(self, ctx: XplorMRParser.Proton_shift_rcoilContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            rcoil = self.numberSelection[0]

            if CS_ERROR_MIN < rcoil < CS_ERROR_MAX:
                pass
            else:
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"Random coil chemical shift value '{rcoil}' must be within range {CS_RESTRAINT_ERROR}.")
                return

            dstFunc = {'rcoil': rcoil}

            for atom1 in self.atomSelectionSet[0]:
                if atom1['atom_id'][0] not in protonBeginCode:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    f"Not a proton; {atom1}.")
                    return

            for atom1 in self.atomSelectionSet[0]:
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (PROTON/RCOI) id={self.procsRestraints} "
                          f"atom={atom1} {dstFunc}")

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by XplorMRParser#proton_shift_anisotropy.
    def enterProton_shift_anisotropy(self, ctx: XplorMRParser.Proton_shift_anisotropyContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#proton_shift_anisotropy.
    def exitProton_shift_anisotropy(self, ctx: XplorMRParser.Proton_shift_anisotropyContext):
        co_or_cn = str(ctx.Simple_name(0))
        is_cooh = None
        if ctx.Logical():
            is_cooh = str(ctx.Logical()) in ('TRUE', 'ON')
        sc_or_bb = str(ctx.Simple_name(1))

        if not self.areUniqueCoordAtoms('a proton chemical shift (PROTON/ANIS)'):
            if len(self.__g) > 0:
                self.__f.extend(self.__g)
            return

        dstFunc = {'co_or_cn': co_or_cn.lower(), 'is_cooh': is_cooh, 'sc_or_bb': sc_or_bb.lower()}

        chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
        seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
        atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

        chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
        seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
        atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

        chain_id_3 = self.atomSelectionSet[2][0]['chain_id']
        seq_id_3 = self.atomSelectionSet[2][0]['seq_id']
        atom_id_3 = self.atomSelectionSet[2][0]['atom_id']

        chain_ids = [chain_id_1, chain_id_2, chain_id_3]
        seq_ids = [seq_id_1, seq_id_2, seq_id_3]
        offsets = [seq_id - seq_id_2 for seq_id in seq_ids]
        atom_ids = [atom_id_1, atom_id_2, atom_id_3]

        if chain_ids != [chain_id_1] * 3 or offsets != [0] * 3 or atom_ids != ['CA', 'C', 'O']:
            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                            "The atom selection order must be [CA(i), C(i), O(i)].")
            return

        for atom1, atom2, atom3 in itertools.product(self.atomSelectionSet[0],
                                                     self.atomSelectionSet[1],
                                                     self.atomSelectionSet[2]):
            if isLongRangeRestraint([atom1, atom2, atom3], self.__polySeq if self.__gapInAuthSeq else None):
                continue
            if self.__debug:
                print(f"subtype={self.__cur_subtype} (PROTON/ANIS) id={self.procsRestraints} "
                      f"atom1={atom1} atom2={atom2} atom3={atom3} {dstFunc}")

    # Enter a parse tree produced by XplorMRParser#proton_shift_amides.
    def enterProton_shift_amides(self, ctx: XplorMRParser.Proton_shift_amidesContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#proton_shift_amides.
    def exitProton_shift_amides(self, ctx: XplorMRParser.Proton_shift_amidesContext):  # pylint: disable=unused-argument
        for atom1 in self.atomSelectionSet[0]:
            if atom1['atom_id'] != 'H':
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"Not a backbone amide proton; {atom1}.")
                return

        for atom1 in self.atomSelectionSet[0]:
            print(f"subtype={self.__cur_subtype} (PROTON/AMID) id={self.procsRestraints} "
                  f"atom={atom1}")

    # Enter a parse tree produced by XplorMRParser#proton_shift_carbons.
    def enterProton_shift_carbons(self, ctx: XplorMRParser.Proton_shift_carbonsContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#proton_shift_carbons.
    def exitProton_shift_carbons(self, ctx: XplorMRParser.Proton_shift_carbonsContext):  # pylint: disable=unused-argument
        for atom1 in self.atomSelectionSet[0]:
            if atom1['atom_id'] != 'C':
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"Not a backbone carbonyl carbon; {atom1}.")
                return

        for atom1 in self.atomSelectionSet[0]:
            print(f"subtype={self.__cur_subtype} (PROTON/CARB) id={self.procsRestraints} "
                  f"atom={atom1}")

    # Enter a parse tree produced by XplorMRParser#proton_shift_nitrogens.
    def enterProton_shift_nitrogens(self, ctx: XplorMRParser.Proton_shift_nitrogensContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#proton_shift_nitrogens.
    def exitProton_shift_nitrogens(self, ctx: XplorMRParser.Proton_shift_nitrogensContext):  # pylint: disable=unused-argument
        for atom1 in self.atomSelectionSet[0]:
            if atom1['atom_id'] != 'N':
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"Not a backbone nitrogen; {atom1}.")
                return

        for atom1 in self.atomSelectionSet[0]:
            print(f"subtype={self.__cur_subtype} (PROTON/NITR) id={self.procsRestraints} "
                  f"atom={atom1}")

    # Enter a parse tree produced by XplorMRParser#proton_shift_oxygens.
    def enterProton_shift_oxygens(self, ctx: XplorMRParser.Proton_shift_oxygensContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#proton_shift_oxygens.
    def exitProton_shift_oxygens(self, ctx: XplorMRParser.Proton_shift_oxygensContext):  # pylint: disable=unused-argument
        for atom1 in self.atomSelectionSet[0]:
            if atom1['atom_id'] != 'O':
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"Not a backbone oxygen; {atom1}.")
                return

        for atom1 in self.atomSelectionSet[0]:
            print(f"subtype={self.__cur_subtype} (PROTON/OXYG) id={self.procsRestraints} "
                  f"atom={atom1}")

    # Enter a parse tree produced by XplorMRParser#proton_shift_ring_atoms.
    def enterProton_shift_ring_atoms(self, ctx: XplorMRParser.Proton_shift_ring_atomsContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#proton_shift_ring_atoms.
    def exitProton_shift_ring_atoms(self, ctx: XplorMRParser.Proton_shift_ring_atomsContext):
        ring_name = str(ctx.Simple_name())

        ringNames = ('PHE', 'TYR', 'HIS', 'TRP5', 'TRP6', 'ADE6', 'ADE5', 'GUA6', 'GUA5', 'THY', 'CYT', 'URA')

        if ring_name not in ringNames:
            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                            f"{ring_name!r} must be one of {ringNames}.")
            return

        if not self.areUniqueCoordAtoms('a proton chemical shift (PROTON/RING)'):
            if len(self.__g) > 0:
                self.__f.extend(self.__g)
            return

        if len(self.atomSelectionSet) == 5:
            for atom1, atom2, atom3, atom4, atom5 in itertools.product(self.atomSelectionSet[0],
                                                                       self.atomSelectionSet[1],
                                                                       self.atomSelectionSet[2],
                                                                       self.atomSelectionSet[3],
                                                                       self.atomSelectionSet[4]):
                if isLongRangeRestraint([atom1, atom2, atom3, atom4, atom5], self.__polySeq if self.__gapInAuthSeq else None):
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (PROTON/RING) id={self.procsRestraints} "
                          f"ring_name={ring_name} atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} atom5={atom5}")

        else:
            for atom1, atom2, atom3, atom4, atom5, atom6 in itertools.product(self.atomSelectionSet[0],
                                                                              self.atomSelectionSet[1],
                                                                              self.atomSelectionSet[2],
                                                                              self.atomSelectionSet[3],
                                                                              self.atomSelectionSet[4],
                                                                              self.atomSelectionSet[5]):
                if isLongRangeRestraint([atom1, atom2, atom3, atom4, atom5, atom6], self.__polySeq if self.__gapInAuthSeq else None):
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (PROTON/RING) id={self.procsRestraints} "
                          f"ring_name={ring_name} atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} atom5={atom5} atom6={atom6}")

    # Enter a parse tree produced by XplorMRParser#proton_shift_alphas_and_amides.
    def enterProton_shift_alphas_and_amides(self, ctx: XplorMRParser.Proton_shift_alphas_and_amidesContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#proton_shift_alphas_and_amides.
    def exitProton_shift_alphas_and_amides(self, ctx: XplorMRParser.Proton_shift_alphas_and_amidesContext):  # pylint: disable=unused-argument
        for atom1 in self.atomSelectionSet[0]:
            if atom1['atom_id'] == 'H' or atom1['atom_id'].startswith('HA'):
                pass
            else:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"Neither alpha protons nor amide proton; {atom1}.")
                return

        for atom1 in self.atomSelectionSet[0]:
            print(f"subtype={self.__cur_subtype} (PROTON/ALPH) id={self.procsRestraints} "
                  f"atom={atom1}")

    # Enter a parse tree produced by XplorMRParser#ramachandran_statement.
    def enterRamachandran_statement(self, ctx: XplorMRParser.Ramachandran_statementContext):
        if ctx.Scale():
            self.ramaScale = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.ramaScale, str):
                if self.ramaScale in self.evaluate:
                    self.ramaScale = self.evaluate[self.ramaScale]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The scale value 'RAMA {str(ctx.Scale())} {self.ramaScale} END' "
                                    f"where the symbol {self.ramaScale!r} is not defined so that set the default value.")
                    self.ramaScale = 1.0
            if self.ramaScale < 0.0:
                self.__f.append("[Invalid data] "
                                f"The scale value 'RAMA {str(ctx.Scale())} {self.ramaScale} END' must not be a negative value.")
            elif self.ramaScale == 0.0:
                self.__f.append("[Range value warning] "
                                f"The scale value 'RAMA {str(ctx.Scale())} {self.ramaScale} END' should be a positive value.")

        elif ctx.Cutoff():
            self.ramaCutoff = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.ramaCutoff, str):
                if self.ramaCutoff in self.evaluate:
                    self.ramaCutoff = self.evaluate[self.ramaCutoff]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The scale value 'RAMA {str(ctx.Cutoff())} {self.ramaCutoff} END'")

        elif ctx.ForceConstant():
            self.ramaForceConst = self.getNumber_s(ctx.number_s(0))

        elif ctx.Shape():
            self.ramaShape = str(ctx.Gauss_or_Quart()).lower()

        elif ctx.Size():
            self.ramaSize = []
            dim = str(ctx.Dimensions()).lower()
            self.ramaSize.append(self.getNumber_s(ctx.number_s(0)))
            if dim in ('twod', 'threed', 'fourd'):
                self.ramaSize.append(self.getNumber_s(ctx.number_s(1)))
            if dim in ('threed', 'fourd'):
                self.ramaSize.append(self.getNumber_s(ctx.number_s(2)))
            if dim == 'fourd':
                self.ramaSize.append(self.getNumber_s(ctx.number_s(3)))

        elif ctx.Phase():
            self.ramaPhase = []
            for d in range(4):
                offset = d * 3
                if ctx.number_s(offset):
                    phase = []
                    for i in range(3):
                        if ctx.number_s(offset + i):
                            phase.append(self.getNumber_s(ctx.number_s(offset + i)))
                        else:
                            break
                    self.ramaPhase.append(phase)
                else:
                    break

        elif ctx.Gaussian():
            self.ramaGaussian = []
            for d in range(4):
                offset = d * 3
                if ctx.number_s(offset):
                    phase = []
                    for i in range(3):
                        if ctx.number_s(offset + i):
                            phase.append(self.getNumber_s(ctx.number_s(offset + i)))
                        else:
                            break
                    self.ramaGaussian.append(phase)
                else:
                    break

        elif ctx.Quartic():
            self.ramaQuartic = []
            for d in range(4):
                offset = d * 3
                if ctx.number_s(offset):
                    phase = []
                    for i in range(3):
                        if ctx.number_s(offset + i):
                            phase.append(self.getNumber_s(ctx.number_s(offset + i)))
                        else:
                            break
                    self.ramaQuartic.append(phase)
                else:
                    break

        elif ctx.Reset():
            self.ramaScale = 1.0
            self.ramaCutoff = None
            self.ramaForceConst = 1.0
            self.ramaShape = None
            self.ramaSize = None
            self.ramaPhase = None
            self.ramaGaussian = None
            self.ramaQuartic = None

        elif ctx.Zero():
            self.ramaGaussian = None
            self.ramaQuartic = None

    # Exit a parse tree produced by XplorMRParser#ramachandran_statement.
    def exitRamachandran_statement(self, ctx: XplorMRParser.Ramachandran_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (RAMA) classification={self.classification!r} "
                  f"scale={self.ramaScale} cutoff={self.ramaCutoff} force_constant={self.ramaForceConst} "
                  f"shape={self.ramaShape} size={self.ramaSize} phase={self.ramaPhase} "
                  f"gaussian={self.ramaGaussian} quartic={self.ramaQuartic}")

    # Enter a parse tree produced by XplorMRParser#rama_assign.
    def enterRama_assign(self, ctx: XplorMRParser.Rama_assignContext):  # pylint: disable=unused-argument
        self.ramaRestraints += 1
        self.__cur_subtype = 'rama'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#rama_assign.
    def exitRama_assign(self, ctx: XplorMRParser.Rama_assignContext):  # pylint: disable=unused-argument
        if not self.__hasPolySeq and not self.__hasNonPolySeq:
            return

        if not self.areUniqueCoordAtoms('a dihedral angle database (RAMA)'):
            if len(self.__g) > 0:
                self.__f.extend(self.__g)
            return

        for i in range(0, len(self.atomSelectionSet), 2):
            chain_id_1 = self.atomSelectionSet[i][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[i][0]['seq_id']
            comp_id_1 = self.atomSelectionSet[i][0]['comp_id']
            atom_id_1 = self.atomSelectionSet[i][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[i + 1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[i + 1][0]['seq_id']
            comp_id_2 = self.atomSelectionSet[i + 1][0]['comp_id']
            atom_id_2 = self.atomSelectionSet[i + 1][0]['atom_id']

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Non-magnetic susceptible spin appears in dihedral angle vector; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if chain_id_1 != chain_id_2:
                ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Found inter-chain dihedral angle vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) > 1:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Found inter-residue dihedral angle vector; "
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
                                    "Found inter-residue dihedral angle vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif atom_id_1 == atom_id_2:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Found zero dihedral angle vector; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            elif self.__ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                if not self.__ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                    if self.__nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.__nefT.validate_comp_atom(comp_id_2, atom_id_2):
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found an dihedral angle vector over multiple covalent bonds in the 'RAMAchandran' statement; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

        if self.__createSfDict:
            software_name = 'XPLOR-NIH/CNS' if self.__remediate else 'XPLOR-NIH'
            statement_name = 'RAMAchandran/CONFormation' if self.__remediate else 'RAMAchandran'
            sf = self.__getSf(f'dihedral angle database restraint, {software_name} {statement_name} statement')
            sf['id'] += 1
            if len(sf['loop']['tags']) == 0:
                sf['loop']['tags'] = ['index_id', 'id', 'combination_id',
                                      'auth_asym_id_1', 'auth_seq_id_1', 'auth_comp_id_1', 'auth_atom_id_1',
                                      'auth_asym_id_2', 'auth_seq_id_2', 'auth_comp_id_2', 'auth_atom_id_2',
                                      'auth_asym_id_3', 'auth_seq_id_3', 'auth_comp_id_3', 'auth_atom_id_3',
                                      'auth_asym_id_4', 'auth_seq_id_4', 'auth_comp_id_4', 'auth_atom_id_4',
                                      'list_id', 'entry_id']
                sf['tags'].append(['classification', self.classification])
                sf['tags'].append(['scale', self.ramaScale])
                sf['tags'].append(['cutoff', self.ramaCutoff])
                sf['tags'].append(['force_constant', self.ramaForceConst])
                sf['tags'].append(['shape', self.ramaShape])
                sf['tags'].append(['size', self.ramaSize])
                sf['tags'].append(['phase', self.ramaPhase])
                if self.ramaGaussian is not None:
                    sf['tags'].append(['gaussian_param'], self.ramaGaussian)
                if self.ramaQuartic is not None:
                    sf['tags'].append(['quartic_param'], self.ramaQuartic)

        for i in range(0, len(self.atomSelectionSet), 4):
            for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[i],
                                                                self.atomSelectionSet[i + 1],
                                                                self.atomSelectionSet[i + 2],
                                                                self.atomSelectionSet[i + 3]):
                if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.__polySeq if self.__gapInAuthSeq else None):
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (RAMA) id={self.ramaRestraints} "
                          f"atom{i+1}={atom1} atom{i+2}={atom2} atom{i+3}={atom3} atom{i+4}={atom4}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    sf['loop']['data'].append([sf['index_id'], sf['id'], '.' if len(self.atomSelectionSet) == 4 else (i + 1),
                                               atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                               atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id'],
                                               atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id'],
                                               atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id'],
                                               sf['list_id'], self.__entryId])

    # Enter a parse tree produced by XplorMRParser#collapse_statement.
    def enterCollapse_statement(self, ctx: XplorMRParser.Collapse_statementContext):
        if ctx.Scale():
            self.radiScale = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.radiScale, str):
                if self.radiScale in self.evaluate:
                    self.radiScale = self.evaluate[self.radiScale]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The scale value 'COLL {str(ctx.Scale())} {self.radiScale} END' "
                                    f"where the symbol {self.radiScale!r} is not defined so that set the default value.")
                    self.radiScale = 1.0
            if self.radiScale < 0.0:
                self.__f.append("[Invalid data] "
                                f"The scale value 'COLL {str(ctx.Scale())} {self.radiScale} END' must not be a negative value.")
            elif self.radiScale == 0.0:
                self.__f.append("[Range value warning] "
                                f"The scale value 'COLL {str(ctx.Scale())} {self.radiScale} END' should be a positive value.")

        elif ctx.Reset():
            self.radiScale = 1.0

    # Exit a parse tree produced by XplorMRParser#collapse_statement.
    def exitCollapse_statement(self, ctx: XplorMRParser.Collapse_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (COLL) classification={self.classification!r} "
                  f"scale={self.radiScale}")

    # Enter a parse tree produced by XplorMRParser#coll_assign.
    def enterColl_assign(self, ctx: XplorMRParser.Coll_assignContext):  # pylint: disable=unused-argument
        self.radiRestraints += 1
        if self.__cur_subtype != 'radi':
            self.radiStatements += 1
        self.__cur_subtype = 'radi'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#coll_assign.
    def exitColl_assign(self, ctx: XplorMRParser.Coll_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            forceConst = self.numberSelection[0]
            targetRgyr = self.numberSelection[1]

            if forceConst <= 0.0:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The force constant value {forceConst} must be a positive value.")
                return

            if DIST_ERROR_MIN < targetRgyr < DIST_ERROR_MAX:
                pass
            else:
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The target Rgyr value {targetRgyr} must be within range {DIST_RESTRAINT_ERROR}.")
                return

            dstFunc = {'target_Rgyr': targetRgyr, 'force_const': forceConst}

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            if self.__createSfDict:
                sf = self.__getSf('radius of gyration restraint, XPLOR-NIH COLLapse statement')
                sf['id'] += 1
                if len(sf['loop']['tags']) == 0:
                    sf['loop']['tags'] = ['index_id', 'id',
                                          'auth_asym_id', 'auth_seq_id', 'auth_comp_id', 'auth_atom_id',
                                          'target_Rgry', 'force_constant'
                                          'list_id', 'entry_id']
                    sf['tags'].append(['classification', self.classification])
                    sf['tags'].append(['scale', self.radiScale])

            for atom1 in self.atomSelectionSet[0]:
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (COLL) id={self.radiRestraints} "
                          f"atom={atom1} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    sf['loop']['data'].append([sf['index_id'], sf['id'],
                                               atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                               targetRgyr, forceConst,
                                               sf['list_id'], self.__entryId])

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by XplorMRParser#diffusion_statement.
    def enterDiffusion_statement(self, ctx: XplorMRParser.Diffusion_statementContext):
        if ctx.Coefficients():
            self.diffCoef = {'Tc': self.getNumber_s(ctx.number_s(0)),
                             'anisotropy': self.getNumber_s(ctx.number_s(1)),
                             'rhombicity': self.getNumber_s(ctx.number_s(2)),
                             'frequency_1h': self.getNumber_s(ctx.number_s(3)),
                             'frequency_15n': self.getNumber_s(ctx.number_s(4))
                             }

        elif ctx.ForceConstant():
            self.diffForceConst = self.getNumber_s(ctx.number_s(0))

        elif ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.diffPotential = 'square'
            elif code.startswith('HARM'):
                self.diffPotential = 'harmonic'
            else:
                self.diffPotential = 'square'
                self.__f.append("[Enum mismatch ignorable] "
                                f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'DANIsotropy' statements. "
                                f"Instead, set the default potential {self.diffPotential!r}.")

        elif ctx.Type():
            self.diffType = str(ctx.Rdc_or_Diff_anis_types()).lower()

        elif ctx.Reset():
            self.diffCoef = None
            self.diffForceConst = 1.0
            self.diffPotential = 'square'
            self.diffType = None

    # Exit a parse tree produced by XplorMRParser#diffusion_statement.
    def exitDiffusion_statement(self, ctx: XplorMRParser.Diffusion_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (DANI) classification={self.classification!r} "
                  f"coefficients={self.diffCoef} force_constant={self.diffForceConst} "
                  f"potential={self.diffPotential} type={self.diffType}")

    # Enter a parse tree produced by XplorMRParser#dani_assign.
    def enterDani_assign(self, ctx: XplorMRParser.Dani_assignContext):  # pylint: disable=unused-argument
        self.diffRestraints += 1
        self.__cur_subtype = 'diff'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#dani_assign.
    def exitDani_assign(self, ctx: XplorMRParser.Dani_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            target = self.numberSelection[0]

            if len(self.numberSelection) > 1:
                delta = abs(self.numberSelection[1])
            else:
                delta = 0.0

            target_value = target
            lower_limit = None
            upper_limit = None

            if self.potential == 'square' and delta > 0.0:
                lower_limit = target - delta
                upper_limit = target + delta

            dstFunc = self.validateT1T2Range(1.0,
                                             target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            if not self.areUniqueCoordAtoms('a diffusion anisotropy (DANI)', XPLOR_ORIGIN_AXIS_COLS):
                if len(self.__g) > 0:
                    self.__f.extend(self.__g)
                return

            chain_id_1 = self.atomSelectionSet[4][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[4][0]['seq_id']
            comp_id_1 = self.atomSelectionSet[4][0]['comp_id']
            atom_id_1 = self.atomSelectionSet[4][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[5][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[5][0]['seq_id']
            comp_id_2 = self.atomSelectionSet[5][0]['comp_id']
            atom_id_2 = self.atomSelectionSet[5][0]['atom_id']

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Non-magnetic susceptible spin appears in diffusion anisotropy vector; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if chain_id_1 != chain_id_2:
                ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Found inter-chain diffusion anisotropy vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) > 1:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Found inter-residue diffusion anisotropy vector; "
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
                                    "Found inter-residue diffusion anisotropy vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif atom_id_1 == atom_id_2:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Found zero diffusion anisotropy vector; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            elif self.__ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                if not self.__ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                    if self.__nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.__nefT.validate_comp_atom(comp_id_2, atom_id_2):
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found a diffusion anisotropy vector over multiple covalent bonds in the 'DANIsotropy' statement; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

            if self.__createSfDict:
                software_name = 'XPLOR-NIH/CNS' if self.__remediate else 'XPLOR-NIH'
                sf = self.__getSf(f'diffusion anisotropy restraint, {software_name} DANIsotropy statement')
                sf['id'] += 1
                if len(sf['loop']['tags']) == 0:
                    sf['loop']['tags'] = ['index_id', 'id',
                                          'auth_asym_id_1', 'auth_seq_id_1', 'auth_comp_id_1', 'auth_atom_id_1',
                                          'auth_asym_id_2', 'auth_seq_id_2', 'auth_comp_id_2', 'auth_atom_id_2',
                                          't1/t2_ratio', 't1/t2_ratio_err',
                                          'list_id', 'entry_id']
                    sf['tags'].append(['classification', self.classification])
                    sf['tags'].append(['coefficients', self.diffCoef])
                    sf['tags'].append(['force_constant', self.diffForceConst])
                    sf['tags'].append(['potential', self.diffPotential])
                    sf['tags'].append(['type', self.diffType])

            for atom1, atom2 in itertools.product(self.atomSelectionSet[4],
                                                  self.atomSelectionSet[5]):
                if isIdenticalRestraint([atom1, atom2]):
                    continue
                if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None):
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (DANI) id={self.diffRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    sf['loop']['data'].append([sf['index_id'], sf['id'],
                                               atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                               atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id'],
                                               target, delta,
                                               sf['list_id'], self.__entryId])

        finally:
            self.numberSelection.clear()

    def validateT1T2Range(self, weight,
                          target_value, lower_limit, upper_limit,
                          lower_linear_limit=None, upper_linear_limit=None):
        """ Validate T1/T2 value range.
        """

        validRange = True
        dstFunc = {'weight': weight, 'potential': self.potential}

        if target_value is not None:
            if T1T2_ERROR_MIN < target_value < T1T2_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value}' must be within range {T1T2_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if T1T2_ERROR_MIN <= lower_limit < T1T2_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit:.6f}' must be within range {T1T2_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if T1T2_ERROR_MIN < upper_limit <= T1T2_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit:.6f}' must be within range {T1T2_RESTRAINT_ERROR}.")

        if lower_linear_limit is not None:
            if T1T2_ERROR_MIN <= lower_linear_limit < T1T2_ERROR_MAX:
                dstFunc['lower_linear_limit'] = f"{lower_linear_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The lower linear limit value='{lower_linear_limit:.6f}' must be within range {T1T2_RESTRAINT_ERROR}.")

        if upper_linear_limit is not None:
            if T1T2_ERROR_MIN < upper_linear_limit <= T1T2_ERROR_MAX:
                dstFunc['upper_linear_limit'] = f"{upper_linear_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The upper linear limit value='{upper_linear_limit:.6f}' must be within range {T1T2_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if lower_linear_limit is not None:
                if lower_linear_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

            if upper_linear_limit is not None:
                if upper_linear_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper linear limit value='{upper_linear_limit:.6f}' must be greater than the target value '{target_value}'.")

        else:

            if lower_limit is not None and upper_limit is not None:
                if lower_limit > upper_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if lower_linear_limit is not None and upper_limit is not None:
                if lower_linear_limit > upper_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if lower_limit is not None and upper_linear_limit is not None:
                if lower_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if lower_linear_limit is not None and upper_linear_limit is not None:
                if lower_linear_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if lower_limit is not None and lower_linear_limit is not None:
                if lower_linear_limit > lower_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the lower limit value '{lower_limit:.6f}'.")

            if upper_limit is not None and upper_linear_limit is not None:
                if upper_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.6f}' must be less than the upper linear limit value '{upper_linear_limit:.6f}'.")

        if not validRange:
            return None

        if target_value is not None:
            if T1T2_RANGE_MIN <= target_value <= T1T2_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value}' should be within range {T1T2_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if T1T2_RANGE_MIN <= lower_limit <= T1T2_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit:.6f}' should be within range {T1T2_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if T1T2_RANGE_MIN <= upper_limit <= T1T2_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit:.6f}' should be within range {T1T2_RESTRAINT_RANGE}.")

        if lower_linear_limit is not None:
            if T1T2_RANGE_MIN <= lower_linear_limit <= T1T2_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower linear limit value='{lower_linear_limit:.6f}' should be within range {T1T2_RESTRAINT_RANGE}.")

        if upper_linear_limit is not None:
            if T1T2_RANGE_MIN <= upper_linear_limit <= T1T2_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper linear limit value='{upper_linear_limit:.6f}' should be within range {T1T2_RESTRAINT_RANGE}.")

        return dstFunc

    # Enter a parse tree produced by XplorMRParser#orientation_statement.
    def enterOrientation_statement(self, ctx: XplorMRParser.Orientation_statementContext):  # pylint: disable=no-self-use
        if ctx.Cutoff():
            self.nbaseCutoff = self.getNumber_s(ctx.number_s(0))

        elif ctx.Height():
            self.nbaseHeight = self.getNumber_s(ctx.number_s(0))

        elif ctx.ForceConstant():
            self.nbaseForceConst = self.getNumber_s(ctx.number_s(0))

        elif ctx.Gaussian():
            self.nbaseGaussian = {'height': self.getNumber_s(ctx.number_s(0)),
                                  'x_center': self.getNumber_s(ctx.number_s(1)),
                                  'x_width': self.getNumber_s(ctx.number_s(2)),
                                  'y_center': self.getNumber_s(ctx.number_s(3)),
                                  'y_width': self.getNumber_s(ctx.number_s(4)),
                                  'z_center': self.getNumber_s(ctx.number_s(5)),
                                  'z_width': self.getNumber_s(ctx.number_s(6))
                                  }

        elif ctx.MaxGaussians():
            self.nbaseMaxGauss = int(str(ctx.Integer()))

        elif ctx.NewGaussian():
            self.nbaseNewGauss = {'height': self.getNumber_s(ctx.number_s(0)),
                                  'x_center': self.getNumber_s(ctx.number_s(1)),
                                  'x_width': self.getNumber_s(ctx.number_s(2)),
                                  'y_center': self.getNumber_s(ctx.number_s(3)),
                                  'y_width': self.getNumber_s(ctx.number_s(4)),
                                  'z_center': self.getNumber_s(ctx.number_s(5)),
                                  'z_width': self.getNumber_s(ctx.number_s(6)),
                                  'baseline_correction': self.getNumber_s(ctx.number_s(7))
                                  }

        elif ctx.Quartic():
            self.nbaseQuartic = {'height': self.getNumber_s(ctx.number_s(0)),
                                 'x_center': self.getNumber_s(ctx.number_s(1)),
                                 'x_width': self.getNumber_s(ctx.number_s(2)),
                                 'y_center': self.getNumber_s(ctx.number_s(3)),
                                 'y_width': self.getNumber_s(ctx.number_s(4)),
                                 'z_center': self.getNumber_s(ctx.number_s(5)),
                                 'z_width': self.getNumber_s(ctx.number_s(6))
                                 }

        elif ctx.Reset():
            self.nbaseCutoff = None
            self.nbaseHeight = None
            self.nbaseForceConst = 1.0
            self.nbaseGaussian = None
            self.nbaseMaxGauss = None
            self.nbaseNewGauss = None
            self.nbaseQuartic = None
            self.nbaseResidues = None
            self.nbaseCubicSize = None

        elif ctx.Residue():
            self.nbaseResidues = int(str(ctx.Integer()))

        elif ctx.Size():
            self.nbaseCubicSize = {'min': self.getNumber_s(ctx.number_s(0)),
                                   'max': self.getNumber_s(ctx.number_s(1))
                                   }

        elif ctx.Zero():
            self.nbaseGaussian = None
            self.nbaseMaxGauss = None
            self.nbaseNewGauss = None
            self.nbaseQuartic = None

    # Exit a parse tree produced by XplorMRParser#orientation_statement.
    def exitOrientation_statement(self, ctx: XplorMRParser.Orientation_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (ORIE) classification={self.classification!r} "
                  f"cutoff={self.nbaseCutoff} height={self.nbaseHeight} force_constant={self.nbaseForceConst} "
                  f"gaussian={self.nbaseGaussian} max_gaussians={self.nbaseMaxGauss} new_gaussian={self.nbaseNewGauss} "
                  f"quartic={self.nbaseQuartic} residues={self.nbaseResidues} "
                  f"cubic_size={self.nbaseCubicSize}")

    # Enter a parse tree produced by XplorMRParser#orie_assign.
    def enterOrie_assign(self, ctx: XplorMRParser.Orie_assignContext):  # pylint: disable=unused-argument
        self.nbaseRestraints += 1
        self.__cur_subtype = 'nbase'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#orie_assign.
    def exitOrie_assign(self, ctx: XplorMRParser.Orie_assignContext):  # pylint: disable=unused-argument
        if not self.__hasPolySeq and not self.__hasNonPolySeq:
            return

        if not self.areUniqueCoordAtoms('a residue-residue position/orientation database (ORIE)'):
            if len(self.__g) > 0:
                self.__f.extend(self.__g)
            return

        chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
        seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
        comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
        atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

        chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
        seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
        comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
        atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

        chain_id_3 = self.atomSelectionSet[2][0]['chain_id']
        seq_id_3 = self.atomSelectionSet[2][0]['seq_id']
        comp_id_3 = self.atomSelectionSet[2][0]['comp_id']
        atom_id_3 = self.atomSelectionSet[2][0]['atom_id']

        chain_id_4 = self.atomSelectionSet[3][0]['chain_id']
        seq_id_4 = self.atomSelectionSet[3][0]['seq_id']
        comp_id_4 = self.atomSelectionSet[3][0]['comp_id']
        atom_id_4 = self.atomSelectionSet[3][0]['atom_id']

        _, nucleotide, _ = self.__csStat.getTypeOfCompId(comp_id_1)

        if not nucleotide:
            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                            "Not a nucleic acid; "
                            f"{chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}.")
            return

        if comp_id_2 != comp_id_1:
            _, nucleotide, _ = self.__csStat.getTypeOfCompId(comp_id_2)

            if not nucleotide:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Not a nucleic acid; "
                                f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}.")
                return

        if comp_id_3 not in (comp_id_1, comp_id_2):
            _, nucleotide, _ = self.__csStat.getTypeOfCompId(comp_id_3)

            if not nucleotide:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Not a nucleic acid; "
                                f"{chain_id_3}:{seq_id_3}:{comp_id_3}:{atom_id_3}.")
                return

        if comp_id_4 not in (comp_id_1, comp_id_2, comp_id_3):
            _, nucleotide, _ = self.__csStat.getTypeOfCompId(comp_id_4)

            if not nucleotide:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Not a nucleic acid; "
                                f"{chain_id_4}:{seq_id_4}:{comp_id_4}:{atom_id_4}.")
                return

        if chain_id_1 == chain_id_2 and chain_id_2 == chain_id_3 and chain_id_3 == chain_id_4:
            if seq_id_1 == seq_id_2 and seq_id_2 == seq_id_3 and seq_id_3 == seq_id_4:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "All selected atoms are in the same residue; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}, "
                                f"{chain_id_3}:{seq_id_3}:{comp_id_3}:{atom_id_3}, "
                                f"{chain_id_4}:{seq_id_4}:{comp_id_4}:{atom_id_4}).")
                return

        if self.__createSfDict:
            sf = self.__getSf('orientation database restraint, XPLOR-NIH ORIEnt statement')
            sf['id'] += 1
            if len(sf['loop']['tags']) == 0:
                sf['loop']['tags'] = ['index_id', 'id',
                                      'auth_asym_id_1', 'auth_seq_id_1', 'auth_comp_id_1', 'auth_atom_id_1',
                                      'auth_asym_id_2', 'auth_seq_id_2', 'auth_comp_id_2', 'auth_atom_id_2',
                                      'auth_asym_id_3', 'auth_seq_id_3', 'auth_comp_id_3', 'auth_atom_id_3',
                                      'auth_asym_id_4', 'auth_seq_id_4', 'auth_comp_id_4', 'auth_atom_id_4',
                                      'list_id', 'entry_id']
                sf['tags'].append(['classification', self.classification])
                sf['tags'].append(['cutoff', self.nbaseCutoff])
                sf['tags'].append(['height', self.nbaseHeight])
                sf['tags'].append(['force_constant', self.nbaseForceConst])
                if self.nbaseGaussian is not None:
                    sf['tags'].append(['gaussian', self.nbaseGaussian])
                if self.nbaseMaxGauss is not None:
                    sf['tags'].append(['max_gaussians', self.nbaseMaxGauss])
                if self.nbaseNewGauss is not None:
                    sf['tags'].append(['new_gaussian', self.nbaseNewGauss])
                if self.nbaseQuartic is not None:
                    sf['tags'].append(['quartic', self.nbaseQuartic])
                sf['tags'].append(['residues', self.nbaseResidues])
                sf['tags'].append(['cubic_size', self.nbaseCubicSize])

        for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                            self.atomSelectionSet[1],
                                                            self.atomSelectionSet[2],
                                                            self.atomSelectionSet[3]):
            if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.__polySeq if self.__gapInAuthSeq else None):
                continue
            if self.__debug:
                print(f"subtype={self.__cur_subtype} (ORIE) id={self.nbaseRestraints} "
                      f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4}")
            if self.__createSfDict and sf is not None:
                sf['index_id'] += 1
                sf['loop']['data'].append([sf['index_id'], sf['id'],
                                           atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                           atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id'],
                                           atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id'],
                                           atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id'],
                                           sf['list_id'], self.__entryId])

    # Enter a parse tree produced by XplorMRParser#csa_statement.
    def enterCsa_statement(self, ctx: XplorMRParser.Csa_statementContext):
        if ctx.Csa_types():
            code = str(ctx.Csa_types()).upper()
            if code.startswith('PHOS'):
                self.csaType = 'phos'
            elif code.startswith('CARB'):
                self.csaType = 'carb'
            elif code.startswith('NITR'):
                self.csaType = 'nitr'

        elif ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.potential = 'square'
            elif code.startswith('HARM'):
                self.potential = 'harmonic'
            else:
                self.potential = 'square'
                self.__f.append("[Enum mismatch ignorable] "
                                f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'DCSA' statements. "
                                f"Instead, set the default potential {self.potential!r}.")

        elif ctx.Scale():
            self.scale = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.scale, str):
                if self.scale in self.evaluate:
                    self.scale = self.evaluate[self.scale]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The scale value 'DCSA {str(ctx.Scale())} {self.scale} END' "
                                    f"where the symbol {self.scale!r} is not defined so that set the default value.")
                    self.scale = 1.0
            if self.scale < 0.0:
                self.__f.append("[Invalid data] "
                                f"The scale value 'DCSA {str(ctx.Scale())} {self.scale} END' must not be a negative value.")
            elif self.scale == 0.0:
                self.__f.append("[Range value warning] "
                                f"The scale value 'DCSA {str(ctx.Scale())} {self.scale} END' should be a positive value.")

        elif ctx.Reset():
            self.potential = 'square'
            self.scale = 1.0
            self.coefficients = None
            self.csaType = None
            self.csaSigma = None

        elif ctx.Coefficients():
            self.coefficients = {'DFS': self.getNumber_s(ctx.number_s(0)),
                                 'anisotropy': self.getNumber_s(ctx.number_s(1)),
                                 'rhombicity': self.getNumber_s(ctx.number_s(2))
                                 }

        elif ctx.Sigma():
            self.csaSigma = {'s11': self.getNumber_s(ctx.number_s(0)),
                             's22': self.getNumber_s(ctx.number_s(1)),
                             's33': self.getNumber_s(ctx.number_s(2))
                             }

    # Exit a parse tree produced by XplorMRParser#csa_statement.
    def exitCsa_statement(self, ctx: XplorMRParser.Csa_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (DCSA) classification={self.classification!r} "
                  f"type={self.csaType} scale={self.scale} coefficients={self.coefficients} sigma={self.csaSigma}")

    # Enter a parse tree produced by XplorMRParser#csa_assign.
    def enterCsa_assign(self, ctx: XplorMRParser.Csa_assignContext):  # pylint: disable=unused-argument
        self.csaRestraints += 1
        if self.__cur_subtype != 'csa':
            self.csaStatements += 1
        self.__cur_subtype = 'csa'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#csa_assign.
    def exitCsa_assign(self, ctx: XplorMRParser.Csa_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            target = self.numberSelection[0]

            if len(self.numberSelection) > 2:
                cminus = self.numberSelection[1]
                cplus = self.numberSelection[2]

            elif len(self.numberSelection) > 1:
                cminus = cplus = self.numberSelection[1]

            else:
                cminus = cplus = 0.0

            target_value = target
            lower_limit = None
            upper_limit = None

            if self.potential == 'square':
                lower_limit = target - cminus
                upper_limit = target + cplus

            dstFunc = self.validateCsaRange(1.0,
                                            target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            if not self.areUniqueCoordAtoms('a CSA (DCSA)', XPLOR_ORIGIN_AXIS_COLS):
                if len(self.__g) > 0:
                    self.__f.extend(self.__g)
                return

            chain_id_1 = self.atomSelectionSet[4][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[4][0]['seq_id']
            comp_id_1 = self.atomSelectionSet[4][0]['comp_id']
            atom_id_1 = self.atomSelectionSet[4][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[5][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[5][0]['seq_id']
            comp_id_2 = self.atomSelectionSet[5][0]['comp_id']
            atom_id_2 = self.atomSelectionSet[5][0]['atom_id']

            chain_id_3 = self.atomSelectionSet[6][0]['chain_id']
            seq_id_3 = self.atomSelectionSet[6][0]['seq_id']
            comp_id_3 = self.atomSelectionSet[6][0]['comp_id']
            atom_id_3 = self.atomSelectionSet[6][0]['atom_id']

            if self.csaType is not None and atom_id_1[0] != self.csaType[0].upper():
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"Central atom {atom_id_1!r} and 'type={self.csaType}' are not consistent; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}, "
                                f"{chain_id_3}:{seq_id_3}:{comp_id_3}:{atom_id_3}).")
                return

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS)\
               or (atom_id_3[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Non-magnetic susceptible spin appears in CSA vector; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}, "
                                f"{chain_id_3}:{seq_id_3}:{comp_id_3}:{atom_id_3}).")
                return

            if chain_id_1 != chain_id_2 or chain_id_2 != chain_id_3:
                ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                ps3 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_3 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None and ps3 is None:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Found inter-chain CSA vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                    f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}, "
                                    f"{chain_id_3}:{seq_id_3}:{comp_id_3}:{atom_id_3}).")
                    return

            elif abs(seq_id_1 - seq_id_2) > 1 or abs(seq_id_2 - seq_id_3) > 1 or abs(seq_id_3 - seq_id_1) > 1:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Found inter-residue CSA vector; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}, "
                                f"{chain_id_3}:{seq_id_3}:{comp_id_3}:{atom_id_3}).")
                return

            elif abs(seq_id_1 - seq_id_2) == 1 or abs(seq_id_2 - seq_id_3) == 1 or abs(seq_id_3 - seq_id_1) == 1:

                if abs(seq_id_1 - seq_id_2) == 1:

                    if self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                            ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                             or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')
                             or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 == 'H')
                             or (seq_id_1 > seq_id_2 and atom_id_1 == 'H' and atom_id_2.startswith('HA'))):
                        pass

                    else:
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found inter-residue CSA vector; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                        f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}, "
                                        f"{chain_id_3}:{seq_id_3}:{comp_id_3}:{atom_id_3}).")
                        return

                elif abs(seq_id_2 - seq_id_3) == 1:

                    if self.__csStat.peptideLike(comp_id_2) and self.__csStat.peptideLike(comp_id_3) and\
                            ((seq_id_2 < seq_id_3 and atom_id_2 == 'C' and atom_id_3 in rdcBbPairCode)
                             or (seq_id_2 > seq_id_3 and atom_id_2 in rdcBbPairCode and atom_id_3 == 'C')
                             or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 == 'H')
                             or (seq_id_1 > seq_id_2 and atom_id_1 == 'H' and atom_id_2.startswith('HA'))):
                        pass

                    else:
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found inter-residue CSA vector; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                        f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}, "
                                        f"{chain_id_3}:{seq_id_3}:{comp_id_3}:{atom_id_3}).")
                        return

                elif abs(seq_id_3 - seq_id_1) == 1:

                    if self.__csStat.peptideLike(comp_id_3) and self.__csStat.peptideLike(comp_id_1) and\
                            ((seq_id_3 < seq_id_1 and atom_id_3 == 'C' and atom_id_1 in rdcBbPairCode)
                             or (seq_id_3 > seq_id_1 and atom_id_3 in rdcBbPairCode and atom_id_1 == 'C')):
                        pass

                    else:
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found inter-residue CSA vector; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                        f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}, "
                                        f"{chain_id_3}:{seq_id_3}:{comp_id_3}:{atom_id_3}).")
                        return

            elif atom_id_1 == atom_id_2 or atom_id_2 == atom_id_3 or atom_id_3 == atom_id_1:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Found zero CSA vector; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}, "
                                f"{chain_id_3}:{seq_id_3}:{comp_id_3}:{atom_id_3}).")
                return

            else:

                if self.__ccU.updateChemCompDict(comp_id_1) and seq_id_1 == seq_id_2:  # matches with comp_id in CCD

                    if not self.__ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                        if self.__nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.__nefT.validate_comp_atom(comp_id_2, atom_id_2):
                            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                            "Found an CSA vector over multiple covalent bonds; "
                                            f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                            f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}, "
                                            f"{chain_id_3}:{seq_id_3}:{comp_id_3}:{atom_id_3}).")
                            return

                if self.__ccU.updateChemCompDict(comp_id_1) and seq_id_1 == seq_id_3:  # matches with comp_id in CCD

                    if not self.__ccU.hasBond(comp_id_1, atom_id_3, atom_id_1):

                        if self.__nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.__nefT.validate_comp_atom(comp_id_3, atom_id_3):
                            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                            "Found an CSA vector over multiple covalent bonds; "
                                            f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                            f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}, "
                                            f"{chain_id_3}:{seq_id_3}:{comp_id_3}:{atom_id_3}).")
                            return

            if self.__createSfDict:
                sf = self.__getSf(self.classification)
                sf['id'] += 1

            for atom1, atom2, atom3 in itertools.product(self.atomSelectionSet[4],
                                                         self.atomSelectionSet[5],
                                                         self.atomSelectionSet[6]):
                if isLongRangeRestraint([atom1, atom2, atom3], self.__polySeq if self.__gapInAuthSeq else None):
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} id={self.csaRestraints} "
                          f"atom1(CSA central)={atom1} atom2={atom2} atom3={atom3} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, None,
                                 sf['list_id'], self.__entryId, dstFunc,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom2)
                    sf['loop'].add_data(row)

        finally:
            self.numberSelection.clear()

    def validateCsaRange(self, weight,
                         target_value, lower_limit, upper_limit,
                         lower_linear_limit=None, upper_linear_limit=None):
        """ Validate CSA value range.
        """

        validRange = True
        dstFunc = {'weight': weight, 'potential': self.potential}

        if target_value is not None:
            if CSA_ERROR_MIN < target_value < CSA_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value}' must be within range {CSA_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if CSA_ERROR_MIN <= lower_limit < CSA_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit:.6f}' must be within range {CSA_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if CSA_ERROR_MIN < upper_limit <= CSA_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit:.6f}' must be within range {CSA_RESTRAINT_ERROR}.")

        if lower_linear_limit is not None:
            if CSA_ERROR_MIN <= lower_linear_limit < CSA_ERROR_MAX:
                dstFunc['lower_linear_limit'] = f"{lower_linear_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The lower linear limit value='{lower_linear_limit:.6f}' must be within range {CSA_RESTRAINT_ERROR}.")

        if upper_linear_limit is not None:
            if CSA_ERROR_MIN < upper_linear_limit <= CSA_ERROR_MAX:
                dstFunc['upper_linear_limit'] = f"{upper_linear_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The upper linear limit value='{upper_linear_limit:.6f}' must be within range {CSA_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if lower_linear_limit is not None:
                if lower_linear_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

            if upper_linear_limit is not None:
                if upper_linear_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper linear limit value='{upper_linear_limit:.6f}' must be greater than the target value '{target_value}'.")

        else:

            if lower_limit is not None and upper_limit is not None:
                if lower_limit > upper_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if lower_linear_limit is not None and upper_limit is not None:
                if lower_linear_limit > upper_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if lower_limit is not None and upper_linear_limit is not None:
                if lower_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if lower_linear_limit is not None and upper_linear_limit is not None:
                if lower_linear_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if lower_limit is not None and lower_linear_limit is not None:
                if lower_linear_limit > lower_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the lower limit value '{lower_limit:.6f}'.")

            if upper_limit is not None and upper_linear_limit is not None:
                if upper_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.6f}' must be less than the upper linear limit value '{upper_linear_limit:.6f}'.")

        if not validRange:
            return None

        if target_value is not None:
            if CSA_RANGE_MIN <= target_value <= CSA_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value}' should be within range {CSA_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if CSA_RANGE_MIN <= lower_limit <= CSA_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit:.6f}' should be within range {CSA_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if CSA_RANGE_MIN <= upper_limit <= CSA_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit:.6f}' should be within range {CSA_RESTRAINT_RANGE}.")

        if lower_linear_limit is not None:
            if CSA_RANGE_MIN <= lower_linear_limit <= CSA_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower linear limit value='{lower_linear_limit:.6f}' should be within range {CSA_RESTRAINT_RANGE}.")

        if upper_linear_limit is not None:
            if CSA_RANGE_MIN <= upper_linear_limit <= CSA_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper linear limit value='{upper_linear_limit:.6f}' should be within range {CSA_RESTRAINT_RANGE}.")

        return dstFunc

    # Enter a parse tree produced by XplorMRParser#pcsa_statement.
    def enterPcsa_statement(self, ctx: XplorMRParser.Pcsa_statementContext):
        self.csaType = None

        if ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.potential = 'square'
            elif code.startswith('HARM'):
                self.potential = 'harmonic'
            else:
                self.potential = 'square'
                self.__f.append("[Enum mismatch ignorable] "
                                f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'PCSA' statements. "
                                f"Instead, set the default potential {self.potential!r}.")

        elif ctx.Scale():
            self.scale = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.scale, str):
                if self.scale in self.evaluate:
                    self.scale = self.evaluate[self.scale]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The scale value 'PCSA {str(ctx.Scale())} {self.scale} END' "
                                    f"where the symbol {self.scale!r} is not defined so that set the default value.")
                    self.scale = 1.0
            if self.scale < 0.0:
                self.__f.append("[Invalid data] "
                                f"The scale value 'PCSA {str(ctx.Scale())} {self.scale} END' must not be a negative value.")
            elif self.scale == 0.0:
                self.__f.append("[Range value warning] "
                                f"The scale value 'PCSA {str(ctx.Scale())} {self.scale} END' should be a positive value.")

        elif ctx.Reset():
            self.potential = 'square'
            self.scale = 1.0
            self.coefficients = None
            self.csaSigma = None

        elif ctx.Coefficients():
            self.coefficients = {'DFS': self.getNumber_s(ctx.number_s(0)),
                                 'anisotropy': self.getNumber_s(ctx.number_s(1)),
                                 'rhombicity': self.getNumber_s(ctx.number_s(2))
                                 }

        elif ctx.Sigma():
            self.csaSigma = {'d11': self.getNumber_s(ctx.number_s(0)),
                             'd22': self.getNumber_s(ctx.number_s(1)),
                             'd33': self.getNumber_s(ctx.number_s(2)),
                             'theta': self.getNumber_s(ctx.number_s(3))
                             }

    # Exit a parse tree produced by XplorMRParser#pcsa_statement.
    def exitPcsa_statement(self, ctx: XplorMRParser.Pcsa_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (PCSA) classification={self.classification!r} "
                  f"scale={self.scale} coefficients={self.coefficients} sigma={self.csaSigma}")

    # Enter a parse tree produced by XplorMRParser#one_bond_coupling_statement.
    def enterOne_bond_coupling_statement(self, ctx: XplorMRParser.One_bond_coupling_statementContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#one_bond_coupling_statement.
    def exitOne_bond_coupling_statement(self, ctx: XplorMRParser.One_bond_coupling_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#one_bond_assign.
    def enterOne_bond_assign(self, ctx: XplorMRParser.One_bond_assignContext):  # pylint: disable=unused-argument
        """
        @deprecated: This restraint has not been useful in practice, but has been preserved for historical reasons.
        """

    # Exit a parse tree produced by XplorMRParser#one_bond_assign.
    def exitOne_bond_assign(self, ctx: XplorMRParser.One_bond_assignContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#angle_db_statement.
    def enterAngle_db_statement(self, ctx: XplorMRParser.Angle_db_statementContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#angle_db_statement.
    def exitAngle_db_statement(self, ctx: XplorMRParser.Angle_db_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#angle_db_assign.
    def enterAngle_db_assign(self, ctx: XplorMRParser.Angle_db_assignContext):  # pylint: disable=unused-argument
        """
        @deprecated:  This term has not proved useful in practice and is only here for historical reasons.
        """

    # Exit a parse tree produced by XplorMRParser#angle_db_assign.
    def exitAngle_db_assign(self, ctx: XplorMRParser.Angle_db_assignContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#pre_statement.
    def enterPre_statement(self, ctx: XplorMRParser.Pre_statementContext):
        if self.preParameterDict is None:
            self.preParameterDict = {}

        if ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.potential = 'square'
            elif code.startswith('HARM'):
                self.potential = 'harmonic'
            else:
                self.potential = 'square'
                self.__f.append("[Enum mismatch ignorable] "
                                f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'PMAGnetic' statements. "
                                f"Instead, set the default potential {self.potential!r}.")

        elif ctx.Reset():
            self.potential = 'square'

        elif ctx.classification():
            self.preParameterDict[self.classification] = {}

        elif ctx.Kconst():
            _classification = str(ctx.Simple_name())
            if _classification not in self.preParameterDict:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The classification of '{str(ctx.Kconst())}={_classification!r} {self.getNumber_s(ctx.number_s(0))}' is unknown.")
                return
            self.preParameterDict[_classification]['k_const'] = self.getNumber_s(ctx.number_s(0))

        elif ctx.Omega():
            _classification = str(ctx.Simple_name())
            if _classification not in self.preParameterDict:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The classification of '{str(ctx.Omega())}={_classification!r} {self.getNumber_s(ctx.number_s(0))}' is unknown.")
                return
            self.preParameterDict[_classification]['omega'] = self.getNumber_s(ctx.number_s(0))

        elif ctx.Tauc():
            _classification = str(ctx.Simple_name())
            if _classification not in self.preParameterDict:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"The classification of '{str(ctx.Tauc())}={_classification!r} {self.getNumber_s(ctx.number_s(0))}' is unknown.")
                return
            self.preParameterDict[_classification]['tauc'] = self.getNumber_s(ctx.number_s(0))

    # Exit a parse tree produced by XplorMRParser#pre_statement.
    def exitPre_statement(self, ctx: XplorMRParser.Pre_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            parameters = f' parameters={self.preParameterDict[self.classification]}'\
                if self.classification in self.preParameterDict and len(self.preParameterDict[self.classification]) > 0\
                else ''
            print(f"subtype={self.__cur_subtype} (PMAG) classification={self.classification!r}{parameters}")

    # Enter a parse tree produced by XplorMRParser#pre_assign.
    def enterPre_assign(self, ctx: XplorMRParser.Pre_assignContext):  # pylint: disable=unused-argument
        self.preRestraints += 1
        if self.__cur_subtype != 'pre':
            self.preStatements += 1
        self.__cur_subtype = 'pre'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#pre_assign.
    def exitPre_assign(self, ctx: XplorMRParser.Pre_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            target = self.numberSelection[0]

            if len(self.numberSelection) > 1:
                delta = abs(self.numberSelection[1])
            else:
                delta = 0.0

            target_value = target
            lower_limit = None
            upper_limit = None

            if self.potential == 'square' and delta > 0.0:
                lower_limit = target - delta
                upper_limit = target + delta

            dstFunc = self.validatePreRange(1.0,
                                            target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            atom_id_0 = self.atomSelectionSet[0][0]['atom_id'] if len(self.atomSelectionSet[0]) > 0 and 'atom_id' in self.atomSelectionSet[0][0] else self.paramagCenter

            chain_id = self.atomSelectionSet[1][0]['chain_id']
            seq_id = self.atomSelectionSet[1][0]['seq_id']
            comp_id = self.atomSelectionSet[1][0]['comp_id']
            atom_id = self.atomSelectionSet[1][0]['atom_id']

            if atom_id[0] not in protonBeginCode:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                f"Not a proton; {chain_id}:{seq_id}:{comp_id}:{atom_id}.")
                return

            if self.__createSfDict:
                sf = self.__getSf(alignCenter=atom_id_0)
                sf['id'] += 1

            for atom1 in self.atomSelectionSet[1]:
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} id={self.preRestraints} "
                          f"paramag_center={atom_id_0} atom={atom1} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, None,
                                 sf['list_id'], self.__entryId, dstFunc,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom1)
                    sf['loop'].add_data(row)

        finally:
            self.numberSelection.clear()

    def validatePreRange(self, weight,
                         target_value, lower_limit, upper_limit,
                         lower_linear_limit=None, upper_linear_limit=None):
        """ Validate PRE value range.
        """

        validRange = True
        dstFunc = {'weight': weight, 'potential': self.potential}

        if target_value is not None:
            if PRE_ERROR_MIN < target_value < PRE_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value}' must be within range {PRE_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if PRE_ERROR_MIN <= lower_limit < PRE_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit:.6f}' must be within range {PRE_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if PRE_ERROR_MIN < upper_limit <= PRE_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit:.6f}' must be within range {PRE_RESTRAINT_ERROR}.")

        if lower_linear_limit is not None:
            if PRE_ERROR_MIN <= lower_linear_limit < PRE_ERROR_MAX:
                dstFunc['lower_linear_limit'] = f"{lower_linear_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The lower linear limit value='{lower_linear_limit:.6f}' must be within range {PRE_RESTRAINT_ERROR}.")

        if upper_linear_limit is not None:
            if PRE_ERROR_MIN < upper_linear_limit <= PRE_ERROR_MAX:
                dstFunc['upper_linear_limit'] = f"{upper_linear_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The upper linear limit value='{upper_linear_limit:.6f}' must be within range {PRE_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if lower_linear_limit is not None:
                if lower_linear_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

            if upper_linear_limit is not None:
                if upper_linear_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper linear limit value='{upper_linear_limit:.6f}' must be greater than the target value '{target_value}'.")

        else:

            if lower_limit is not None and upper_limit is not None:
                if lower_limit > upper_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if lower_linear_limit is not None and upper_limit is not None:
                if lower_linear_limit > upper_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if lower_limit is not None and upper_linear_limit is not None:
                if lower_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if lower_linear_limit is not None and upper_linear_limit is not None:
                if lower_linear_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if lower_limit is not None and lower_linear_limit is not None:
                if lower_linear_limit > lower_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the lower limit value '{lower_limit:.6f}'.")

            if upper_limit is not None and upper_linear_limit is not None:
                if upper_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.6f}' must be less than the upper linear limit value '{upper_linear_limit:.6f}'.")

        if not validRange:
            return None

        if target_value is not None:
            if PRE_RANGE_MIN <= target_value <= PRE_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value}' should be within range {PRE_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if PRE_RANGE_MIN <= lower_limit <= PRE_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit:.6f}' should be within range {PRE_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if PRE_RANGE_MIN <= upper_limit <= PRE_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit:.6f}' should be within range {PRE_RESTRAINT_RANGE}.")

        if lower_linear_limit is not None:
            if PRE_RANGE_MIN <= lower_linear_limit <= PRE_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower linear limit value='{lower_linear_limit:.6f}' should be within range {PRE_RESTRAINT_RANGE}.")

        if upper_linear_limit is not None:
            if PRE_RANGE_MIN <= upper_linear_limit <= PRE_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper linear limit value='{upper_linear_limit:.6f}' should be within range {PRE_RESTRAINT_RANGE}.")

        return dstFunc

    # Enter a parse tree produced by XplorMRParser#pcs_statement.
    def enterPcs_statement(self, ctx: XplorMRParser.Pcs_statementContext):
        if ctx.Reset():
            self.coefficients = None

        elif ctx.Coefficients():
            self.coefficients = {'a1': self.getNumber_s(ctx.number_s(0)),
                                 'a2': self.getNumber_s(ctx.number_s(1))
                                 }

    # Exit a parse tree produced by XplorMRParser#pcs_statement.
    def exitPcs_statement(self, ctx: XplorMRParser.Pcs_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (XPCS) classification={self.classification!r} "
                  f"coefficients={self.coefficients}")

    # Enter a parse tree produced by XplorMRParser#pcs_assign.
    def enterPcs_assign(self, ctx: XplorMRParser.Pcs_assignContext):  # pylint: disable=unused-argument
        self.pcsRestraints += 1
        self.__cur_subtype_altered = self.__cur_subtype != 'pcs'
        self.__cur_subtype = 'pcs' if self.__cur_subtype != 'hvycs' else 'hvycs'  # set 'hvycs' for error message

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#pcs_assign.
    def exitPcs_assign(self, ctx: XplorMRParser.Pcs_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            if not self.__in_block:
                try:
                    # check whether if carbon shift restraints or not
                    atom_id_5 = self.atomSelectionSet[4][0]['atom_id']
                except IndexError:
                    self.pcsRestraints -= 1
                    self.hvycsRestraints += 1
                    if self.__cur_subtype_altered:
                        self.pcsStatements -= 1
                        if self.hvycsStatements == 0:
                            self.hvycsStatements += 1
                    self.__cur_subtype = 'hvycs'
                    self.exitCarbon_shift_assign(ctx)
                    return

                try:
                    # check whether if carbon shift restraints or not
                    atom_id_1 = self.atomSelectionSet[0][0]['atom_id']
                    atom_id_2 = self.atomSelectionSet[1][0]['atom_id']
                    atom_id_3 = self.atomSelectionSet[2][0]['atom_id']
                    atom_id_4 = self.atomSelectionSet[3][0]['atom_id']
                except IndexError:
                    atom_id_1, atom_id_2, atom_id_3, atom_id_4 = 'OO', 'Z', 'X', 'Y'

                atom_ids = [atom_id_1, atom_id_2, atom_id_3, atom_id_4, atom_id_5]

                if atom_ids == ['C', 'N', 'CA', 'C', 'N']:
                    self.pcsRestraints -= 1
                    self.hvycsRestraints += 1
                    if self.__cur_subtype_altered:
                        self.pcsStatements -= 1
                        if self.hvycsStatements == 0:
                            self.hvycsStatements += 1
                    self.__cur_subtype = 'hvycs'
                    self.exitCarbon_shift_assign(ctx)
                    return

            self.__cur_subtype = 'pcs'  # to get consistent number of statement

            if self.__cur_subtype_altered:
                self.pcsStatements += 1

            if not self.__hasPolySeq and not self.__hasNonPolySeq:  # can't decide whether CARB or XPCS wo the coordinates
                return

            target = self.numberSelection[0]

            if len(self.numberSelection) > 1:
                delta = abs(self.numberSelection[1])
            else:
                delta = 0.0

            target_value = target
            lower_limit = None
            upper_limit = None

            if delta > 0.0:
                lower_limit = target - delta
                upper_limit = target + delta

            if len(self.numberSelection) > 2:
                error_less = delta
                error_greater = abs(self.numberSelection[2])
                lower_limit = target - error_less
                upper_limit = target + error_greater

            dstFunc = self.validatePcsRange(1.0, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            atom_id_0 = self.atomSelectionSet[0][0]['atom_id'] if len(self.atomSelectionSet[0]) > 0 and 'atom_id' in self.atomSelectionSet[0][0] else self.paramagCenter

            if self.__createSfDict:
                sf = self.__getSf(alignCenter=atom_id_0)
                sf['id'] += 1

            for atom1 in self.atomSelectionSet[4]:
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} id={self.pcsRestraints} "
                          f"paramag_center={atom_id_0} atom={atom1} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, None,
                                 sf['list_id'], self.__entryId, dstFunc,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom1)
                    sf['loop'].add_data(row)

        finally:
            self.numberSelection.clear()

    def validatePcsRange(self, weight,
                         target_value, lower_limit, upper_limit,
                         lower_linear_limit=None, upper_linear_limit=None):
        """ Validate PCS value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

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

        if lower_linear_limit is not None:
            if PCS_ERROR_MIN <= lower_linear_limit < PCS_ERROR_MAX:
                dstFunc['lower_linear_limit'] = f"{lower_linear_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The lower linear limit value='{lower_linear_limit:.6f}' must be within range {PCS_RESTRAINT_ERROR}.")

        if upper_linear_limit is not None:
            if PCS_ERROR_MIN < upper_linear_limit <= PCS_ERROR_MAX:
                dstFunc['upper_linear_limit'] = f"{upper_linear_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The upper linear limit value='{upper_linear_limit:.6f}' must be within range {PCS_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if lower_linear_limit is not None:
                if lower_linear_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

            if upper_linear_limit is not None:
                if upper_linear_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper linear limit value='{upper_linear_limit:.6f}' must be greater than the target value '{target_value}'.")

        else:

            if lower_limit is not None and upper_limit is not None:
                if lower_limit > upper_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if lower_linear_limit is not None and upper_limit is not None:
                if lower_linear_limit > upper_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if lower_limit is not None and upper_linear_limit is not None:
                if lower_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if lower_linear_limit is not None and upper_linear_limit is not None:
                if lower_linear_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if lower_limit is not None and lower_linear_limit is not None:
                if lower_linear_limit > lower_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the lower limit value '{lower_limit:.6f}'.")

            if upper_limit is not None and upper_linear_limit is not None:
                if upper_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.6f}' must be less than the upper linear limit value '{upper_linear_limit:.6f}'.")

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

        if lower_linear_limit is not None:
            if PCS_RANGE_MIN <= lower_linear_limit <= PCS_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower linear limit value='{lower_linear_limit:.6f}' should be within range {PCS_RESTRAINT_RANGE}.")

        if upper_linear_limit is not None:
            if PCS_RANGE_MIN <= upper_linear_limit <= PCS_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper linear limit value='{upper_linear_limit:.6f}' should be within range {PCS_RESTRAINT_RANGE}.")

        return dstFunc

    # Enter a parse tree produced by XplorMRParser#prdc_statement.
    def enterPrdc_statement(self, ctx: XplorMRParser.Prdc_statementContext):
        if ctx.Reset():
            self.potential = 'square'
            self.coefficients = None

        elif ctx.Coefficients():
            self.coefficients = {'a1': self.getNumber_s(ctx.number_s(0)),
                                 'a2': self.getNumber_s(ctx.number_s(1))
                                 }

    # Exit a parse tree produced by XplorMRParser#prdc_statement.
    def exitPrdc_statement(self, ctx: XplorMRParser.Prdc_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (XRDC) classification={self.classification!r} "
                  f"coefficients={self.coefficients}")

    # Enter a parse tree produced by XplorMRParser#prdc_assign.
    def enterPrdc_assign(self, ctx: XplorMRParser.Prdc_assignContext):  # pylint: disable=unused-argument
        self.prdcRestraints += 1
        self.__cur_subtype = 'prdc'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#prdc_assign.
    def exitPrdc_assign(self, ctx: XplorMRParser.Prdc_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            target = self.numberSelection[0]

            if len(self.numberSelection) > 1:
                delta = abs(self.numberSelection[1])
            else:
                delta = 0.0

            target_value = target
            lower_limit = None
            upper_limit = None

            if delta > 0.0:
                lower_limit = target - delta
                upper_limit = target + delta

            dstFunc = self.validateRdcRange(1.0, {'potential': self.potential},
                                            target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            if not self.areUniqueCoordAtoms('a paramagnetic RDC (XRDC)', XPLOR_ORIGIN_AXIS_COLS):
                if len(self.__g) > 0:
                    self.__f.extend(self.__g)
                return

            atom_id_0 = self.atomSelectionSet[0][0]['atom_id'] if len(self.atomSelectionSet[0]) > 0 and 'atom_id' in self.atomSelectionSet[0][0] else self.paramagCenter

            chain_id_1 = self.atomSelectionSet[4][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[4][0]['seq_id']
            comp_id_1 = self.atomSelectionSet[4][0]['comp_id']
            atom_id_1 = self.atomSelectionSet[4][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[5][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[5][0]['seq_id']
            comp_id_2 = self.atomSelectionSet[5][0]['comp_id']
            atom_id_2 = self.atomSelectionSet[5][0]['atom_id']

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
                                        "Found an RDC vector over multiple covalent bonds in the 'XRDCoupling' statement; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

            combinationId = '.'
            if self.__createSfDict:
                sf = self.__getSf(alignCenter=atom_id_0)
                sf['id'] += 1
                if len(self.atomSelectionSet[4]) > 1 or len(self.atomSelectionSet[5]) > 1:
                    combinationId = 0

            for atom1, atom2 in itertools.product(self.atomSelectionSet[4],
                                                  self.atomSelectionSet[5]):
                if isIdenticalRestraint([atom1, atom2]):
                    continue
                if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None):
                    continue
                if isinstance(combinationId, int):
                    combinationId += 1
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (XRDC) id={self.prdcRestraints} "
                          f"paramag_center={atom_id_0} atom1={atom1} atom2={atom2} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 combinationId, None, None,
                                 sf['list_id'], self.__entryId, dstFunc,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom1, atom2)
                    sf['loop'].add_data(row)

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by XplorMRParser#porientation_statement.
    def enterPorientation_statement(self, ctx: XplorMRParser.Porientation_statementContext):  # pylint: disable=no-self-use
        if ctx.ForceConstant():
            self.pangForceConst = self.getNumber_s(ctx.number_s())

        elif ctx.Reset():
            self.pangForceConst = 1.0

    # Exit a parse tree produced by XplorMRParser#porientation_statement.
    def exitPorientation_statement(self, ctx: XplorMRParser.Porientation_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (XANG) classification={self.classification!r} "
                  f"force_constant={self.pangForceConst}")

    # Enter a parse tree produced by XplorMRParser#porientation_assign.
    def enterPorientation_assign(self, ctx: XplorMRParser.Porientation_assignContext):  # pylint: disable=unused-argument
        self.pangRestraints += 1
        self.__cur_subtype = 'pang'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#porientation_assign.
    def exitPorientation_assign(self, ctx: XplorMRParser.Porientation_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            theta = self.numberSelection[0]
            phi = self.numberSelection[1]
            delta = abs(self.numberSelection[2])

            target_value = theta
            lower_limit = theta - delta
            upper_limit = theta + delta

            dstFunc = self.validateAngleRange(1.0, {'angle_name': 'theta'},
                                              target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            dstFunc2 = {'weight': 1.0, 'angle_name': 'phi'}

            target_value = phi
            lower_limit = phi - delta
            upper_limit = phi + delta

            dstFunc2 = self.validateAngleRange(1.0, {'angle_name': 'phi'},
                                               target_value, lower_limit, upper_limit)

            if dstFunc2 is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            if not self.areUniqueCoordAtoms('a paramagnetic orientation (XANG)'):
                if len(self.__g) > 0:
                    self.__f.extend(self.__g)
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
                                "Non-magnetic susceptible spin appears in orientation vector; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if chain_id_1 != chain_id_2:
                ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Found inter-chain orientation vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) > 1:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Found inter-residue orientation vector; "
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
                                    "Found inter-residue orientation vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif atom_id_1 == atom_id_2:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Found zero orientation vector; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            elif self.__ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                if not self.__ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                    if self.__nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.__nefT.validate_comp_atom(comp_id_2, atom_id_2):
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found an orientation vector over multiple covalent bonds in the 'XANGle' statement; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

            if self.__createSfDict:
                sf = self.__getSf('paramagnetic orientation restraint, XPLOR-NIH XANGle statement')
                sf['id'] += 1
                if len(sf['loop']['tags']) == 0:
                    sf['loop']['tags'] = ['index_id', 'id',
                                          'auth_asym_id_1', 'auth_seq_id_1', 'auth_comp_id_1', 'auth_atom_id_1',
                                          'auth_asym_id_2', 'auth_seq_id_2', 'auth_comp_id_2', 'auth_atom_id_2',
                                          'theta', 'phi', 'err',
                                          'list_id', 'entry_id']
                    sf['tags'].append(['classification', self.classification])
                    sf['tags'].append(['force_constant', self.nbaseForceConst])

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if isIdenticalRestraint([atom1, atom2]):
                    continue
                if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None):
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (XANG) id={self.pangRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc} {dstFunc2}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    sf['loop']['data'].append([sf['index_id'], sf['id'],
                                               atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                               atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id'],
                                               theta, phi, delta,
                                               sf['list_id'], self.__entryId])

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by XplorMRParser#pccr_statement.
    def enterPccr_statement(self, ctx: XplorMRParser.Pccr_statementContext):
        if ctx.Reset():
            self.coefficients = None

        elif ctx.Coefficients():
            self.coefficients = {'proportionality': self.getNumber_s(ctx.number_s())}

    # Exit a parse tree produced by XplorMRParser#pccr_statement.
    def exitPccr_statement(self, ctx: XplorMRParser.Pccr_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (XCCR) classification={self.classification!r} "
                  f"coefficients={self.coefficients}")

    # Enter a parse tree produced by XplorMRParser#pccr_assign.
    def enterPccr_assign(self, ctx: XplorMRParser.Pccr_assignContext):  # pylint: disable=unused-argument
        self.pccrRestraints += 1
        self.__cur_subtype = 'pccr'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#pccr_assign.
    def exitPccr_assign(self, ctx: XplorMRParser.Pccr_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            target = self.numberSelection[0]

            if len(self.numberSelection) > 1:
                delta = abs(self.numberSelection[1])
            else:
                delta = 0.0

            target_value = target
            lower_limit = None
            upper_limit = None

            if delta > 0.0:
                lower_limit = target - delta
                upper_limit = target + delta

            dstFunc = self.validateCcrRange(1.0,
                                            target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq and not self.__hasNonPolySeq:
                return

            if not self.areUniqueCoordAtoms('a paramagnetic cross-correlation rate (XCCR)'):
                if len(self.__g) > 0:
                    self.__f.extend(self.__g)
                return

            atom_id_0 = self.atomSelectionSet[0][0]['atom_id'] if len(self.atomSelectionSet[0]) > 0 and 'atom_id' in self.atomSelectionSet[0][0] else self.paramagCenter

            chain_id_1 = self.atomSelectionSet[1][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[1][0]['seq_id']
            comp_id_1 = self.atomSelectionSet[1][0]['comp_id']
            atom_id_1 = self.atomSelectionSet[1][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[2][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[2][0]['seq_id']
            comp_id_2 = self.atomSelectionSet[2][0]['comp_id']
            atom_id_2 = self.atomSelectionSet[2][0]['atom_id']

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Non-magnetic susceptible spin appears in CCR vector; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if chain_id_1 != chain_id_2:
                ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Found inter-chain CCR vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) > 1:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Found inter-residue CCR vector; "
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
                                    "Found inter-residue CCR vector; "
                                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif atom_id_1 == atom_id_2:
                self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                "Found zero CCR vector; "
                                f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            elif self.__ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                if not self.__ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                    if self.__nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.__nefT.validate_comp_atom(comp_id_2, atom_id_2):
                        self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                        "Found an CCR vector over multiple covalent bonds in the 'XCCR' statement; "
                                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

            if self.__createSfDict:
                sf = self.__getSf(alignCenter=atom_id_0)
                sf['id'] += 1

            for atom1, atom2 in itertools.product(self.atomSelectionSet[1],
                                                  self.atomSelectionSet[2]):
                if isIdenticalRestraint([atom1, atom2]):
                    continue
                if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None):
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (XCCR) id={self.pccrRestraints} "
                          f"paramag_center={atom_id_0} atom1={atom1} atom2={atom2} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, None,
                                 sf['list_id'], self.__entryId, dstFunc,
                                 self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                                 atom_id_0, None, atom1, atom2)
                    sf['loop'].add_data(row)

        finally:
            self.numberSelection.clear()

    def validateCcrRange(self, weight,
                         target_value, lower_limit, upper_limit,
                         lower_linear_limit=None, upper_linear_limit=None):
        """ Validate CCR value range.
        """

        validRange = True
        dstFunc = {'weight': weight, 'potential': self.potential}

        if target_value is not None:
            if CCR_ERROR_MIN < target_value < CCR_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value}' must be within range {CCR_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if CCR_ERROR_MIN <= lower_limit < CCR_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit:.6f}' must be within range {CCR_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if CCR_ERROR_MIN < upper_limit <= CCR_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit:.6f}' must be within range {CCR_RESTRAINT_ERROR}.")

        if lower_linear_limit is not None:
            if CCR_ERROR_MIN <= lower_linear_limit < CCR_ERROR_MAX:
                dstFunc['lower_linear_limit'] = f"{lower_linear_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The lower linear limit value='{lower_linear_limit:.6f}' must be within range {CCR_RESTRAINT_ERROR}.")

        if upper_linear_limit is not None:
            if CCR_ERROR_MIN < upper_linear_limit <= CCR_ERROR_MAX:
                dstFunc['upper_linear_limit'] = f"{upper_linear_limit:.6f}"
            else:
                validRange = False
                self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                f"The upper linear limit value='{upper_linear_limit:.6f}' must be within range {CCR_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if lower_linear_limit is not None:
                if lower_linear_limit > target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

            if upper_linear_limit is not None:
                if upper_linear_limit < target_value:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper linear limit value='{upper_linear_limit:.6f}' must be greater than the target value '{target_value}'.")

        else:

            if lower_limit is not None and upper_limit is not None:
                if lower_limit > upper_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if lower_linear_limit is not None and upper_limit is not None:
                if lower_linear_limit > upper_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if lower_limit is not None and upper_linear_limit is not None:
                if lower_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if lower_linear_limit is not None and upper_linear_limit is not None:
                if lower_linear_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if lower_limit is not None and lower_linear_limit is not None:
                if lower_linear_limit > lower_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the lower limit value '{lower_limit:.6f}'.")

            if upper_limit is not None and upper_linear_limit is not None:
                if upper_limit > upper_linear_limit:
                    validRange = False
                    self.__f.append(f"[Range value error] {self.__getCurrentRestraint()}"
                                    f"The upper limit value='{upper_limit:.6f}' must be less than the upper linear limit value '{upper_linear_limit:.6f}'.")

        if not validRange:
            return None

        if target_value is not None:
            if CCR_RANGE_MIN <= target_value <= CCR_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The target value='{target_value}' should be within range {CCR_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if CCR_RANGE_MIN <= lower_limit <= CCR_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower limit value='{lower_limit:.6f}' should be within range {CCR_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if CCR_RANGE_MIN <= upper_limit <= CCR_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper limit value='{upper_limit:.6f}' should be within range {CCR_RESTRAINT_RANGE}.")

        if lower_linear_limit is not None:
            if CCR_RANGE_MIN <= lower_linear_limit <= CCR_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The lower linear limit value='{lower_linear_limit:.6f}' should be within range {CCR_RESTRAINT_RANGE}.")

        if upper_linear_limit is not None:
            if CCR_RANGE_MIN <= upper_linear_limit <= CCR_RANGE_MAX:
                pass
            else:
                self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                f"The upper linear limit value='{upper_linear_limit:.6f}' should be within range {CCR_RESTRAINT_RANGE}.")

        return dstFunc

    # Enter a parse tree produced by XplorMRParser#hbond_statement.
    def enterHbond_statement(self, ctx: XplorMRParser.Hbond_statementContext):  # pylint: disable=no-self-use
        if ctx.Reset():
            pass

    # Exit a parse tree produced by XplorMRParser#hbond_statement.
    def exitHbond_statement(self, ctx: XplorMRParser.Hbond_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (HBDA) classification={self.classification!r}")

    # Enter a parse tree produced by XplorMRParser#hbond_assign.
    def enterHbond_assign(self, ctx: XplorMRParser.Hbond_assignContext):  # pylint: disable=unused-argument
        self.hbondRestraints += 1
        if self.__cur_subtype != 'hbond':
            self.hbondStatements += 1
        self.__cur_subtype = 'hbond'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#hbond_assign.
    def exitHbond_assign(self, ctx: XplorMRParser.Hbond_assignContext):  # pylint: disable=unused-argument
        if not self.__hasPolySeq and not self.__hasNonPolySeq:
            return

        if not self.areUniqueCoordAtoms('a hydrogen bond geometry (HBDA)'):
            if len(self.__g) > 0:
                self.__f.extend(self.__g)
            return

        donor = self.atomSelectionSet[0][0]
        hydrogen = self.atomSelectionSet[1][0]
        acceptor = self.atomSelectionSet[2][0]

        if donor['chain_id'] != hydrogen['chain_id']:
            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                            "The donor atom and its hygrogen are in different chains; "
                            f"({donor['chain_id']}:{donor['seq_id']}:{donor['comp_id']}:{donor['atom_id']}, "
                            f"{hydrogen['chain_id']}:{hydrogen['seq_id']}:{hydrogen['comp_id']}:{hydrogen['atom_id']}).")
            return

        if donor['seq_id'] != hydrogen['seq_id']:
            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                            "The donor atom and its hygrogen are in different residues; "
                            f"({donor['chain_id']}:{donor['seq_id']}:{donor['comp_id']}:{donor['atom_id']}, "
                            f"{hydrogen['chain_id']}:{hydrogen['seq_id']}:{hydrogen['comp_id']}:{hydrogen['atom_id']}).")
            return

        if donor['atom_id'][0] not in ('N', 'O', 'F'):
            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                            "The donor atom type should be one of Nitrogen, Oxygen, Fluorine; "
                            f"{donor['chain_id']}:{donor['seq_id']}:{donor['comp_id']}:{donor['atom_id']}. "
                            "The XPLOR-NIH atom selections for hydrogen bond geometry restraint must be in the order of donor, hydrogen, and acceptor.")
            return

        if acceptor['atom_id'][0] not in ('N', 'O', 'F'):
            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                            "The acceptor atom type should be one of Nitrogen, Oxygen, Fluorine; "
                            f"{acceptor['chain_id']}:{acceptor['seq_id']}:{acceptor['comp_id']}:{acceptor['atom_id']}. "
                            "The XPLOR-NIH atom selections for hydrogen bond geometry restraint must be in the order of donor, hydrogen, and acceptor.")
            return

        if hydrogen['atom_id'][0] not in protonBeginCode:
            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                            "Not a hydrogen; "
                            f"{hydrogen['chain_id']}:{hydrogen['seq_id']}:{hydrogen['comp_id']}:{hydrogen['atom_id']}. "
                            "The XPLOR-NIH atom selections for hydrogen bond geometry restraint must be in the order of donor, hydrogen, and acceptor.")
            return

        comp_id = donor['comp_id']

        if self.__ccU.updateChemCompDict(comp_id):  # matches with comp_id in CCD

            atom_id_1 = donor['atom_id']
            atom_id_2 = hydrogen['atom_id']

            if not self.__ccU.hasBond(comp_id, atom_id_1, atom_id_2):

                if self.__nefT.validate_comp_atom(comp_id, atom_id_1) and self.__nefT.validate_comp_atom(comp_id, atom_id_2):
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Found a donor-hydrogen vector over multiple covalent bonds in the 'HBDA' statement; "
                                    f"({donor['chain_id']}:{donor['seq_id']}:{donor['comp_id']}:{donor['atom_id']}, "
                                    f"{hydrogen['chain_id']}:{hydrogen['seq_id']}:{hydrogen['comp_id']}:{hydrogen['atom_id']}).")
                    return

        chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
        seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
        atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

        chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
        seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
        atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

        chain_id_3 = self.atomSelectionSet[2][0]['chain_id']
        seq_id_3 = self.atomSelectionSet[2][0]['seq_id']
        atom_id_3 = self.atomSelectionSet[2][0]['atom_id']

        try:

            _donor =\
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

            _hydrogen =\
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

            _acceptor =\
                self.__cR.getDictListWithFilter('atom_site',
                                                CARTN_DATA_ITEMS,
                                                [{'name': self.__authAsymId, 'type': 'str', 'value': chain_id_3},
                                                 {'name': self.__authSeqId, 'type': 'int', 'value': seq_id_3},
                                                 {'name': self.__authAtomId, 'type': 'str', 'value': atom_id_3},
                                                 {'name': self.__modelNumName, 'type': 'int',
                                                  'value': self.__representativeModelId},
                                                 {'name': 'label_alt_id', 'type': 'enum',
                                                  'enum': ('A')}
                                                 ])

            if len(_donor) == 1 and len(_hydrogen) == 1 and len(_acceptor) == 1:
                dist = distance(to_np_array(_hydrogen[0]), to_np_array(_acceptor[0]))
                if dist > 2.5:
                    self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                    f"The distance of the hydrogen bond linkage ({chain_id_1}:{seq_id_1}:{atom_id_1} - "
                                    f"{chain_id_2}:{seq_id_2}:{atom_id_2}) is too far apart in the coordinates ({dist:.3f}Å).")

                dist = distance(to_np_array(_donor[0]), to_np_array(_acceptor[0]))
                if dist > 3.5:
                    self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                    f"The distance of the hydrogen bond linkage ({chain_id_1}:{seq_id_1}:{atom_id_1} - "
                                    f"{chain_id_2}:{seq_id_2}:{atom_id_2}) is too far apart in the coordinates ({dist:.3f}Å).")

        except Exception as e:
            if self.__verbose:
                self.__lfh.write(f"+XplorMRParserListener.exitHbond_assign() ++ Error  - {str(e)}")

        if self.__createSfDict:
            sf = self.__getSf(self.classification)
            sf['id'] += 1

        for atom1, atom2, atom3 in itertools.product(self.atomSelectionSet[0],
                                                     self.atomSelectionSet[1],
                                                     self.atomSelectionSet[2]):
            if isLongRangeRestraint([atom1, atom2, atom3], self.__polySeq if self.__gapInAuthSeq else None):
                continue
            if self.__debug:
                print(f"subtype={self.__cur_subtype} (HBDA) id={self.hbondRestraints} "
                      f"donor={atom1} hydrogen={atom2} acceptor={atom3}")
            if self.__createSfDict and sf is not None:
                sf['index_id'] += 1
                memberLogicCode = 'AND'
                row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                             1, None, memberLogicCode,
                             sf['list_id'], self.__entryId, getDstFuncForHBond(atom1, atom3),
                             self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                             atom1, atom3)
                sf['loop'].add_data(row)
                #
                sf['index_id'] += 1
                memberLogicCode = 'AND'
                row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                             2, None, memberLogicCode,
                             sf['list_id'], self.__entryId, getDstFuncForHBond(atom2, atom3),
                             self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                             atom2, atom3)
                sf['loop'].add_data(row)

    # Enter a parse tree produced by XplorMRParser#hbond_db_statement.
    def enterHbond_db_statement(self, ctx: XplorMRParser.Hbond_db_statementContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#hbond_db_statement.
    def exitHbond_db_statement(self, ctx: XplorMRParser.Hbond_db_statementContext):  # pylint: disable=unused-argument
        if self.__debug:
            print(f"subtype={self.__cur_subtype} (HBDB)")

    # Enter a parse tree produced by XplorMRParser#hbond_db_assign.
    def enterHbond_db_assign(self, ctx: XplorMRParser.Hbond_db_assignContext):  # pylint: disable=unused-argument
        self.hbondRestraints += 1
        if self.__cur_subtype != 'hbond':
            self.hbondStatements += 1
        self.__cur_subtype = 'hbond'

        self.atomSelectionSet.clear()
        self.__g.clear()

        self.donor_columnSel = self.acceptor_columnSel = -1

    # Exit a parse tree produced by XplorMRParser#hbond_db_assign.
    def exitHbond_db_assign(self, ctx: XplorMRParser.Hbond_db_assignContext):  # pylint: disable=unused-argument
        if not self.__hasPolySeq and not self.__hasNonPolySeq:
            return

        if not self.areUniqueCoordAtoms('a hydrogen bond database (HBDB)'):
            if len(self.__g) > 0:
                self.__f.extend(self.__g)
            return

        if self.donor_columnSel < 0:
            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                            "The donor atom has not been selected. 'don' tag must be exist in an atom selection expression of each Hydrogen bond database (HBDB) statement. "
                            "e.g. assign (acc and resid 2 and segid A and name O ) (don and resid 8 and segid A and name HN)")
            return

        if self.acceptor_columnSel < 0:
            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                            "The acceptor atom has not been selected. 'acc' tag must be exist in an atom selection expression of each Hydrogen bond database (HBDB) statement. "
                            "e.g. assign (acc and resid 2 and segid A and name O ) (don and resid 8 and segid A and name HN)")
            return

        acceptor = self.atomSelectionSet[self.acceptor_columnSel][0]
        donor = self.atomSelectionSet[self.donor_columnSel][0]

        if acceptor['atom_id'][0] not in ('N', 'O', 'F'):
            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                            "The acceptor atom type should be one of Nitrogen, Oxygen, Fluorine; "
                            f"{acceptor['chain_id']}:{acceptor['seq_id']}:{acceptor['comp_id']}:{acceptor['atom_id']}.")
            return

        if donor['atom_id'][0] not in protonBeginCode:
            self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                            "The donor atom type should be Hydrogen; "
                            f"{donor['chain_id']}:{donor['seq_id']}:{donor['comp_id']}:{donor['atom_id']}.")
            return

        chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
        seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
        atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

        chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
        seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
        atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

        try:

            _acceptor =\
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

            _hydrogen =\
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

            if len(_hydrogen) == 1 and len(_acceptor) == 1:
                dist = distance(to_np_array(_hydrogen[0]), to_np_array(_acceptor[0]))
                if dist > 2.5:
                    self.__f.append(f"[Range value warning] {self.__getCurrentRestraint()}"
                                    f"The distance of the hydrogen bond linkage ({chain_id_1}:{seq_id_1}:{atom_id_1} - "
                                    f"{chain_id_2}:{seq_id_2}:{atom_id_2}) is too far apart in the coordinates ({dist:.3f}Å).")

        except Exception as e:
            if self.__verbose:
                self.__lfh.write(f"+XplorMRParserListener.exitHbond_db_assign() ++ Error  - {str(e)}")

        if self.__createSfDict:
            sf = self.__getSf(self.classification)
            sf['id'] += 1

        for atom1, atom2 in itertools.product(self.atomSelectionSet[self.donor_columnSel],
                                              self.atomSelectionSet[self.acceptor_columnSel]):
            if isIdenticalRestraint([atom1, atom2]):
                continue
            if self.__debug:
                print(f"subtype={self.__cur_subtype} (HBDB) id={self.hbondRestraints} "
                      f"donor={atom1} acceptor={atom2}")
            if self.__createSfDict and sf is not None:
                sf['index_id'] += 1
                row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                             '.', None, None,
                             sf['list_id'], self.__entryId, getDstFuncForHBond(atom1, atom2),
                             self.__authToStarSeq, self.__authToInsCode, self.__offsetHolder,
                             atom1, atom2)
                sf['loop'].add_data(row)

    # Enter a parse tree produced by XplorMRParser#ncs_restraint.
    def enterNcs_restraint(self, ctx: XplorMRParser.Ncs_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = True

        self.geoStatements += 1
        self.__cur_subtype = 'geo'

        if self.__createSfDict:
            software_name = 'XPLOR-NIH/CNS' if self.__remediate else 'XPLOR-NIH'
            self.__addSf(f'NCS restraint, {software_name} NCS/GROUP statement')

    # Exit a parse tree produced by XplorMRParser#ncs_restraint.
    def exitNcs_restraint(self, ctx: XplorMRParser.Ncs_restraintContext):  # pylint: disable=unused-argument
        self.__in_block = False

        if self.__createSfDict:
            self.__trimSfWoLp()

    # Enter a parse tree produced by XplorMRParser#ncs_statement.
    def enterNcs_statement(self, ctx: XplorMRParser.Ncs_statementContext):
        if ctx.Initialize():
            self.ncsSigb = 2.0
            self.ncsWeight = 300.0

    # Exit a parse tree produced by XplorMRParser#ncs_statement.
    def exitNcs_statement(self, ctx: XplorMRParser.Ncs_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#ncs_group_statement.
    def enterNcs_group_statement(self, ctx: XplorMRParser.Ncs_group_statementContext):
        self.geoRestraints += 1
        if self.__cur_subtype != 'geo':
            self.geoStatements += 1
        self.__cur_subtype = 'geo'

        self.atomSelectionSet.clear()
        self.__g.clear()

        if ctx.Sigb():
            self.ncsSigb = self.getNumber_s(ctx.number_s())
            if isinstance(self.ncsSigb, str):
                if self.ncsSigb in self.evaluate:
                    self.ncsSigb = self.evaluate[self.ncsSigb]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The B-factor value 'GROUP {str(ctx.Sigb())}={self.ncsSigb} END' "
                                    f"where the symbol {self.ncsSigb!r} is not defined so that set the default value.")
                    self.ncsSigb = 2.0
            if self.ncsSigb <= 0.0:
                self.__f.append("[Invalid data] "
                                f"The B-factor value 'GROUP {str(ctx.Sigb())}={self.ncsSigb} END' must be a positive value.")

        elif ctx.Weight():
            self.ncsWeight = self.getNumber_s(ctx.number_s())
            if isinstance(self.ncsWeight, str):
                if self.ncsWeight in self.evaluate:
                    self.ncsWeight = self.evaluate[self.ncsWeight]
                else:
                    self.__f.append("[Unsupported data] "
                                    f"The weight value 'GROUP {str(ctx.Weight())}={self.ncsWeight} END' "
                                    f"where the symbol {self.ncsWeight!r} is not defined so that set the default value.")
                    self.ncsWeight = 300.0
            if self.ncsWeight < 0.0:
                self.__f.append("[Invalid data] "
                                f"The weight value 'GROUP {str(ctx.Weight())}={self.ncsWeight} END' must not be a negative value.")
            elif self.ncsWeight == 0.0:
                self.__f.append("[Range value warning] "
                                f"The weight value 'GROUP {str(ctx.Weight())}={self.ncsWeight} END' should be a positive value.")

    # Exit a parse tree produced by XplorMRParser#ncs_group_statement.
    def exitNcs_group_statement(self, ctx: XplorMRParser.Ncs_group_statementContext):  # pylint: disable=unused-argument
        if not self.__hasPolySeq and not self.__hasNonPolySeq:
            return

        if len(self.atomSelectionSet) == 0:
            return

        if self.__createSfDict:
            software_name = 'XPLOR-NIH/CNS' if self.__remediate else 'XPLOR-NIH'
            sf = self.__getSf(f'NCS restraint, {software_name} NCS/GROUP statement')
            sf['id'] += 1
            if len(sf['loop']['tags']) == 0:
                sf['loop']['tags'] = ['index_id', 'id',
                                      'auth_asym_id', 'auth_seq_id', 'auth_comp_id', 'auth_atom_id',
                                      'list_id', 'entry_id']
                sf['tags'].append(['sigma_b', self.ncsSigb])
                sf['tags'].append(['weight', self.ncsWeight])

        for atom1 in self.atomSelectionSet[0]:
            if atom1['atom_id'] == 'H':
                continue
            if self.__debug:
                print(f"subtype={self.__cur_subtype} (NCS/GROUP) id={self.geoRestraints} "
                      f"atom={atom1} sigb={self.ncsSigb} weight={self.ncsWeight}")
            if self.__createSfDict and sf is not None:
                sf['index_id'] += 1
                sf['loop']['data'].append([sf['index_id'], sf['id'],
                                           atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                           sf['list_id'], self.__entryId])

    # Enter a parse tree produced by XplorMRParser#selection.
    def enterSelection(self, ctx: XplorMRParser.SelectionContext):  # pylint: disable=unused-argument
        if self.__sel_expr_debug:
            print("  " * self.depth + "enter_selection")

        if self.inVector3D:
            self.inVector3D_columnSel += 1

        elif self.depth == 0:
            self.stackSelections = []
            self.stackTerms = []
            self.factor = {}

    # Exit a parse tree produced by XplorMRParser#selection.
    def exitSelection(self, ctx: XplorMRParser.SelectionContext):  # pylint: disable=unused-argument
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

        if self.inVector3D:
            if self.inVector3D_columnSel == 0:
                self.inVector3D_tail = atomSelection[0]
                if len(atomSelection) > 1:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Ambiguous atoms have been selected to create a 3d-vector in the 'tail' clause.")
            else:
                self.inVector3D_head = atomSelection[0]
                if len(atomSelection) > 1:
                    self.__f.append(f"[Invalid data] {self.__getCurrentRestraint()}"
                                    "Ambiguous atoms have been selected to create a 3d-vector in the 'head' clause.")

        else:
            self.atomSelectionSet.append(atomSelection)

    # Enter a parse tree produced by XplorMRParser#selection_expression.
    def enterSelection_expression(self, ctx: XplorMRParser.Selection_expressionContext):
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

    # Exit a parse tree produced by XplorMRParser#selection_expression.
    def exitSelection_expression(self, ctx: XplorMRParser.Selection_expressionContext):  # pylint: disable=unused-argument
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

    # Enter a parse tree produced by XplorMRParser#term.
    def enterTerm(self, ctx: XplorMRParser.TermContext):
        if self.__sel_expr_debug:
            print("  " * self.depth + f"enter_term, intersection: {bool(ctx.And_op(0))}")

        self.stackFactors = []
        self.factor = {}

        self.depth += 1

    # Exit a parse tree produced by XplorMRParser#term.
    def exitTerm(self, ctx: XplorMRParser.TermContext):  # pylint: disable=unused-argument
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

        self.__with_para = self.__cur_subtype in ('pcs', 'pre', 'prdc', 'pccr')

        if len(self.atomSelectionSet) == 0:

            # for the case dist -> pre transition occurs
            if self.__cur_subtype == 'dist'\
               and 'atom_id' in _factor and _factor['atom_id'][0] != 'CA'\
               and (_factor['atom_id'][0] in PARAMAGNETIC_ELEMENTS or _factor['atom_id'][0] == 'OO'):
                self.__with_para = True

            if self.__with_para:
                self.paramagCenter = copy.copy(_factor)

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

        self.__with_axis = self.__cur_subtype in ('rdc', 'diff', 'csa', 'pcs', 'pre', 'prdc')

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
            if 'atom_id' in _factor and _factor['atom_id'][0] is not None:
                _atomId = _factor['atom_id'][0].upper() if len(_factor['atom_id'][0]) <= 2 else _factor['atom_id'][0][:2].upper()
                if self.__with_axis and _atomId in XPLOR_RDC_PRINCIPAL_AXIS_NAMES:
                    return _factor
                if self.__with_para and (('comp_id' in _factor and _factor['atom_id'][0] == _factor['comp_id'][0] and _atomId in PARAMAGNETIC_ELEMENTS)
                                         or _atomId in FERROMAGNETIC_ELEMENTS
                                         or _atomId in LANTHANOID_ELEMENTS):
                    return _factor
                if self.__cur_subtype == 'dist' and _atomId in XPLOR_NITROXIDE_NAMES:
                    return _factor
            __factor = copy.copy(_factor)
            del __factor['atom_selection']
            if _factor['atom_id'][0] is not None:
                if self.__cur_subtype != 'plane':
                    if cifCheck:
                        if self.__cur_union_expr:
                            self.__g.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                            f"The {clauseName} has no effect for a factor {__factor}.")
                        else:
                            self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
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
                        self.__g.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
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

                    if not self.__with_axis and not self.__with_para:
                        updatePolySeqRst(self.__polySeqRst, chainId, seqId, compId)

                    atomSiteAtomId = None if coordAtomSite is None else coordAtomSite['atom_id']

                    for atomId in _factor['atom_id']:
                        _atomId = atomId.upper() if len(atomId) <= 2 else atomId[:2].upper()
                        if self.__with_axis:
                            if _atomId in XPLOR_RDC_PRINCIPAL_AXIS_NAMES:
                                continue
                        if self.__with_para:
                            if ((atomId == compId and _atomId in PARAMAGNETIC_ELEMENTS) or _atomId in FERROMAGNETIC_ELEMENTS or _atomId in LANTHANOID_ELEMENTS):
                                continue
                        if self.__with_axis or self.__with_para:
                            updatePolySeqRst(self.__polySeqRst, chainId, seqId, compId)

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

                        if self.__cur_subtype == 'dist' and atomId in XPLOR_NITROXIDE_NAMES and coordAtomSite is not None\
                           and atomId not in atomSiteAtomId:
                            if compId == 'CYS' and 'SG' in atomSiteAtomId:
                                atomIds = ['SG']
                                _factor['alt_atom_id'] = atomId + '(nitroxide attached point)'
                            elif compId == 'SER' and 'OG' in atomSiteAtomId:
                                atomIds = ['OG']
                                _factor['alt_atom_id'] = atomId + '(nitroxide attached point)'
                            elif compId == 'GLU' and 'OE2' in atomSiteAtomId:
                                atomIds = ['OE2']
                                _factor['alt_atom_id'] = atomId + '(nitroxide attached point)'
                            elif compId == 'ASP' and 'OD2' in atomSiteAtomId:
                                atomIds = ['OD2']
                                _factor['alt_atom_id'] = atomId + '(nitroxide attached point)'
                            elif compId == 'GLN' and 'NE2' in atomSiteAtomId:
                                atomIds = ['NE2']
                                _factor['alt_atom_id'] = atomId + '(nitroxide attached point)'
                            elif compId == 'ASN' and 'ND2' in atomSiteAtomId:
                                atomIds = ['ND2']
                                _factor['alt_atom_id'] = atomId + '(nitroxide attached point)'
                            elif compId == 'LYS' and 'NZ' in atomSiteAtomId:
                                atomIds = ['NZ']
                                _factor['alt_atom_id'] = atomId + '(nitroxide attached point)'
                            elif compId == 'THR' and 'OG1' in atomSiteAtomId:
                                atomIds = ['OG1']
                                _factor['alt_atom_id'] = atomId + '(nitroxide attached point)'

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
                                                """
                                                seqKey = _seqKey
                                                chainId, seqId = seqKey
                                                if len(self.atomSelectionSet) > 0:
                                                    self.__setLocalSeqScheme()
                                                """
                                            elif 'alt_atom_id' in _coordAtomSite and _atomId in _coordAtomSite['alt_atom_id']:
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['alt_atom_id'].index(_atomId)]
                                                self.__authSeqId = 'auth_seq_id'
                                                self.__authAtomId = 'auth_atom_id'
                                                """
                                                seqKey = _seqKey
                                                chainId, seqId = seqKey
                                                if len(self.atomSelectionSet) > 0:
                                                    self.__setLocalSeqScheme()
                                                """
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

                            if ccdCheck and compId is not None and _atomId not in XPLOR_RDC_PRINCIPAL_AXIS_NAMES and _atomId not in XPLOR_NITROXIDE_NAMES:
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

    # Enter a parse tree produced by XplorMRParser#factor.
    def enterFactor(self, ctx: XplorMRParser.FactorContext):
        if self.__sel_expr_debug:
            print("  " * self.depth + f"enter_factor, concatenation: {bool(ctx.factor())}")

        if ctx.Point():
            self.inVector3D = True
            self.inVector3D_columnSel = -1
            self.inVector3D_tail = None
            self.inVector3D_head = None
            self.vector3D = None

        self.depth += 1

    # Exit a parse tree produced by XplorMRParser#factor.
    def exitFactor(self, ctx: XplorMRParser.FactorContext):
        self.depth -= 1
        if self.__sel_expr_debug:
            print("  " * self.depth + "exit_factor")

        def set_store(num):
            if self.__sel_expr_debug:
                print("  " * self.depth + f"--> store{num}")
            if len(self.storeSet[num]) == 0:
                self.factor['atom_id'] = [None]
                self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                f"The 'store{num}' clause has no effect "
                                "because the internal vector statement is not set.")
            else:
                self.factor = copy.copy(self.storeSet[num])

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

            if ctx.All() or ctx.Known():
                clauseName = 'all' if ctx.All() else 'known'
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
                        self.__lfh.write(f"+XplorMRParserListener.exitFactor() ++ Error  - {str(e)}")

            elif ctx.Around() or ctx.Saround():
                clauseName = 'around' if ctx.Around() else 'saround'
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
                                self.__lfh.write(f"+XplorMRParserListener.exitFactor() ++ Error  - {str(e)}")

                    if ctx.Saround():
                        identity = numpy.identity(3, dtype=float)
                        zero = numpy.zeros(3, dtype=float)

                        oper_list = self.__cR.getDictList('pdbx_struct_oper_list')
                        if len(oper_list) > 0:
                            for oper in oper_list:
                                matrix = numpy.array([[float(oper['matrix[1][1]']), float(oper['matrix[1][2]']), float(oper['matrix[1][3]'])],
                                                     [float(oper['matrix[2][1]']), float(oper['matrix[2][2]']), float(oper['matrix[2][3]'])],
                                                     [float(oper['matrix[3][1]']), float(oper['matrix[3][2]']), float(oper['matrix[3][3]'])]], dtype=float)
                                vector = numpy.array([float(oper['vector[1]']), float(oper['vector[2]']), float(oper['vector[3]'])], dtype=float)

                                if numpy.array_equal(matrix, identity) and numpy.array_equal(vector, zero):
                                    continue

                                inv_matrix = numpy.linalg.inv(matrix)

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

                                        origin = numpy.dot(inv_matrix, numpy.subtract(to_np_array(_origin[0]), vector))

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
                                            self.__lfh.write(f"+XplorMRParserListener.exitFactor() ++ Error  - {str(e)}")

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
                    if len(self.__fibril_chain_ids) > 0 and not self.__hasNonPoly:
                        if chainId[0] in self.__fibril_chain_ids:
                            self.factor['chain_id'] = [chainId[0]]
                    elif len(self.__polySeq) == 1:
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

            elif ctx.Attribute():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> attribute")
                if not self.__hasCoord:
                    return
                absolute = bool(ctx.Abs())
                _attr_prop = str(ctx.Attr_properties())
                attr_prop = _attr_prop.lower()
                opCode = str(ctx.Comparison_ops())
                if len(self.numberFSelection) == 0 or None in self.numberFSelection:
                    return
                attr_value = self.numberFSelection[0]

                validProp = True

                if attr_prop == 'b':
                    valueType = {'name': 'B_iso_or_equiv'}
                    if opCode == '=':
                        valueType['type'] = 'float' if not absolute else 'abs-float'
                        valueType['value'] = attr_value
                    elif opCode == '<':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'max_exclusive': attr_value}
                    elif opCode == '>':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_exclusive': attr_value}
                    elif opCode == '<=':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'max_inclusive': attr_value}
                    elif opCode == '>=':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_inclusive': attr_value}
                    elif opCode == '#':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
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

                elif attr_prop.startswith('bcom')\
                        or attr_prop.startswith('qcom')\
                        or attr_prop.startswith('xcom')\
                        or attr_prop.startswith('ycom')\
                        or attr_prop.startswith('zcom'):  # BCOMP, QCOMP, XCOMP, YCOMP, ZCOM`
                    self.factor['atom_id'] = [None]
                    self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                    f"The attribute property {_attr_prop!r} "
                                    "requires a comparison coordinate set.")
                    validProp = False

                elif attr_prop.startswith('char'):  # CAHRGE
                    valueType = {'name': 'pdbx_formal_charge'}
                    if opCode == '=':
                        valueType['type'] = 'int' if not absolute else 'abs-int'
                        valueType['value'] = attr_value
                    elif opCode == '<':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'max_exclusive': attr_value}
                    elif opCode == '>':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'min_exclusive': attr_value}
                    elif opCode == '<=':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'max_inclusive': attr_value}
                    elif opCode == '>=':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'min_inclusive': attr_value}
                    elif opCode == '#':
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

                elif attr_prop in ('dx', 'dy', 'dz', 'harm'):
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

                            if (opCode == '=' and atomicWeight == attr_value)\
                               or (opCode == '<' and atomicWeight < attr_value)\
                               or (opCode == '>' and atomicWeight > attr_value)\
                               or (opCode == '<=' and atomicWeight <= attr_value)\
                               or (opCode == '>=' and atomicWeight >= attr_value)\
                               or (opCode == '#' and atomicWeight != attr_value):
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

                elif attr_prop == 'q':
                    valueType = {'name': 'occupancy'}
                    if opCode == '=':
                        valueType['type'] = 'float' if not absolute else 'abs-float'
                        valueType['value'] = attr_value
                    elif opCode == '<':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'max_exclusive': attr_value}
                    elif opCode == '>':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_exclusive': attr_value}
                    elif opCode == '<=':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'max_inclusive': attr_value}
                    elif opCode == '>=':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_inclusive': attr_value}
                    elif opCode == '#':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
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

                elif attr_prop in ('refx', 'refy', 'refz', 'rmsd'):
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
                    if opCode == '=':
                        valueType['type'] = 'float' if not absolute else 'abs-float'
                        valueType['value'] = attr_value
                    elif opCode == '<':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'max_exclusive': attr_value}
                    elif opCode == '>':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_exclusive': attr_value}
                    elif opCode == '<=':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'max_inclusive': attr_value}
                    elif opCode == '>=':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_inclusive': attr_value}
                    elif opCode == '#':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
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

                elif attr_prop.startswith('store'):
                    store_id = int(attr_prop[-1])
                    self.factor['atom_id'] = [None]
                    if len(self.storeSet[store_id]) == 0:
                        self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                        f"The 'store{store_id}' clause has no effect "
                                        "because the internal vector statement is not set.")
                        validProp = False

                if validProp and 'atom_selection' in self.factor and len(self.factor['atom_selection']) == 0:
                    self.factor['atom_id'] = [None]
                    _absolute = ' abs' if absolute else ''
                    self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                    f"The 'attribute' clause ('{_attr_prop}{_absolute} {opCode} {attr_value}') has no effect.")

            elif ctx.BondedTo():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> bondedto")
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
                    elif symbol_name in self.evaluateFor:
                        val = self.evaluateFor[symbol_name]
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

            elif ctx.Id():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> id")
                self.factor['atom_id'] = [None]
                self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                "The 'id' clause has no effect "
                                "because the internal atom number is not included in the coordinate file.")

            elif ctx.Name():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> name")

                eval_factor = False
                if 'atom_id' in self.factor or 'atom_ids' in self.factor:
                    __factor = copy.copy(self.factor)
                    self.consumeFactor_expressions("'name' clause", False)
                    eval_factor = True

                if ctx.Colon():  # range expression
                    if ctx.Simple_name(0):
                        begAtomId = str(ctx.Simple_name(0))
                    elif ctx.Double_quote_string(0):
                        begAtomId = str(ctx.Double_quote_string(0)).strip('"').strip()
                        if len(begAtomId) == 0:
                            return
                    if ctx.Simple_name(1):
                        endAtomId = str(ctx.Simple_name(1))
                    elif ctx.Double_quote_string(1):
                        endAtomId = str(ctx.Double_quote_string(1)).strip('"').strip()
                        if len(endAtomId) == 0:
                            return
                    self.factor['atom_ids'] = [begAtomId, endAtomId]

                elif ctx.Simple_name(0) or ctx.Double_quote_string(0):
                    if ctx.Simple_name(0):
                        self.factor['atom_id'] = [str(ctx.Simple_name(0))]
                    elif ctx.Double_quote_string(0):
                        self.factor['atom_id'] = [str(ctx.Double_quote_string(0)).strip('"').strip()]

                elif ctx.Simple_names(0):
                    self.factor['atom_ids'] = [str(ctx.Simple_names(0))]

                elif ctx.Symbol_name():
                    symbol_name = str(ctx.Symbol_name())
                    if symbol_name in self.evaluate:
                        val = self.evaluate[symbol_name]
                        if isinstance(val, list):
                            self.factor['atom_id'] = val
                        else:
                            self.factor['atom_id'] = [val]
                    elif symbol_name in self.evaluateFor:
                        val = self.evaluateFor[symbol_name]
                        if isinstance(val, list):
                            self.factor['atom_id'] = val
                        else:
                            self.factor['atom_id'] = [val]
                    else:
                        self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                        f"The symbol {symbol_name!r} is not defined.")

                if eval_factor and 'atom_selection' in self.factor:
                    if len(self.factor['atom_selection']) == 0 and 'atom_id' in __factor and __factor['atom_id'][0] is not None:
                        __atomId = __factor['atom_id'][0].upper() if len(__factor['atom_id'][0]) <= 2 else __factor['atom_id'][0][:2].upper()
                        if self.__with_axis and __atomId in XPLOR_RDC_PRINCIPAL_AXIS_NAMES:
                            pass
                        elif self.__with_para and (('comp_id' in __factor and __factor['atom_id'][0] == __factor['comp_id'][0] and __atomId in PARAMAGNETIC_ELEMENTS)
                                                   or __atomId in FERROMAGNETIC_ELEMENTS or __atomId in LANTHANOID_ELEMENTS):
                            pass
                        elif self.__cur_subtype == 'plane':
                            pass
                        elif self.__cur_subtype == 'dist' and __atomId in XPLOR_NITROXIDE_NAMES:
                            pass
                        else:
                            _factor = copy.copy(self.factor)
                            if 'atom_selection' in __factor:
                                del __factor['atom_selection']
                            del _factor['atom_selection']
                            self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                            f"The 'name' clause has no effect for a conjunction of factor {__factor} and {_factor}.")

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
                            self.__lfh.write(f"+XplorMRParserListener.exitFactor() ++ Error  - {str(e)}")

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
                if ctx.Tail():

                    if self.inVector3D_tail is not None:

                        try:

                            _tail =\
                                self.__cR.getDictListWithFilter('atom_site',
                                                                CARTN_DATA_ITEMS,
                                                                [{'name': self.__authAsymId, 'type': 'str', 'value': self.inVector3D_tail['chain_id']},
                                                                 {'name': self.__authSeqId, 'type': 'int', 'value': self.inVector3D_tail['seq_id']},
                                                                 {'name': self.__authAtomId, 'type': 'str', 'value': self.inVector3D_tail['atom_id']},
                                                                 {'name': self.__modelNumName, 'type': 'int',
                                                                  'value': self.__representativeModelId},
                                                                 {'name': 'label_alt_id', 'type': 'enum',
                                                                  'enum': ('A')}
                                                                 ])

                            if len(_tail) == 1:
                                tail = to_np_array(_tail[0])

                                if self.inVector3D_head is None:
                                    self.vector3D = tail

                                else:

                                    _head =\
                                        self.__cR.getDictListWithFilter('atom_site',
                                                                        CARTN_DATA_ITEMS,
                                                                        [{'name': self.__authAsymId, 'type': 'str', 'value': self.inVector3D_head['chain_id']},
                                                                         {'name': self.__authSeqId, 'type': 'int', 'value': self.inVector3D_head['seq_id']},
                                                                         {'name': self.__authAtomId, 'type': 'str', 'value': self.inVector3D_head['atom_id']},
                                                                         {'name': self.__modelNumName, 'type': 'int',
                                                                          'value': self.__representativeModelId},
                                                                         {'name': 'label_alt_id', 'type': 'enum',
                                                                          'enum': ('A')}
                                                                         ])

                                    if len(_head) == 1:
                                        head = to_np_array(_head[0])
                                        self.vector3D = numpy.subtract(tail, head, dtype=float)

                        except Exception as e:
                            if self.__verbose:
                                self.__lfh.write(f"+XplorMRParserListener.exitFactor() ++ Error  - {str(e)}")

                    self.inVector3D_tail = self.inVector3D_head = None
                    if len(self.numberFSelection) == 0 or None in self.numberFSelection:
                        return
                    cut = self.numberFSelection[0]

                else:
                    if len(self.numberFSelection) == 0 or None in self.numberFSelection:
                        return
                    self.vector3D = [self.numberFSelection[0], self.numberFSelection[1], self.numberFSelection[2]]
                    cut = self.numberFSelection[3]

                if self.vector3D is None:
                    self.factor['atom_id'] = [None]
                    self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                    "The 'point' clause has no effect because no 3d-vector is specified.")

                else:
                    atomSelection = []

                    try:

                        _neighbor =\
                            self.__cR.getDictListWithFilter('atom_site',
                                                            AUTH_ATOM_CARTN_DATA_ITEMS,
                                                            [{'name': 'Cartn_x', 'type': 'range-float',
                                                              'range': {'min_exclusive': (self.vector3D[0] - cut),
                                                                        'max_exclusive': (self.vector3D[0] + cut)}},
                                                             {'name': 'Cartn_y', 'type': 'range-float',
                                                              'range': {'min_exclusive': (self.vector3D[1] - cut),
                                                                        'max_exclusive': (self.vector3D[1] + cut)}},
                                                             {'name': 'Cartn_z', 'type': 'range-float',
                                                              'range': {'min_exclusive': (self.vector3D[2] - cut),
                                                                        'max_exclusive': (self.vector3D[2] + cut)}},
                                                             {'name': self.__modelNumName, 'type': 'int',
                                                              'value': self.__representativeModelId},
                                                             {'name': 'label_alt_id', 'type': 'enum',
                                                              'enum': ('A')}
                                                             ])

                        if len(_neighbor) > 0:
                            neighbor = [atom for atom in _neighbor if distance(to_np_array(atom), self.vector3D) < cut]

                            for atom in neighbor:
                                del atom['x']
                                del atom['y']
                                del atom['z']
                                atomSelection.append(atom)

                    except Exception as e:
                        if self.__verbose:
                            self.__lfh.write(f"+XplorMRParserListener.exitFactor() ++ Error  - {str(e)}")

                    self.factor['atom_selection'] = atomSelection

                    if len(self.factor['atom_selection']) == 0:
                        self.factor['atom_id'] = [None]
                        self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                        "The 'cut' clause has no effect.")

                self.inVector3D = False
                self.vector3D = None

            elif ctx.Previous():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> previous")
                self.factor['atom_id'] = [None]
                self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                "The 'previous' clause has no effect "
                                "because the internal atom selection is fragile in the restraint file.")

            elif ctx.Pseudo():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> pseudo")
                if not self.__hasCoord:
                    return
                atomSelection = []

                try:

                    _atomSelection =\
                        self.__cR.getDictListWithFilter('atom_site',
                                                        AUTH_ATOM_DATA_ITEMS,
                                                        [{'name': self.__modelNumName, 'type': 'int',
                                                          'value': self.__representativeModelId},
                                                         {'name': 'label_alt_id', 'type': 'enum',
                                                          'enum': ('A')}
                                                         ])

                    lastCompId = None
                    pseudoAtoms = None

                    for _atom in _atomSelection:
                        compId = _atom['comp_id']
                        atomId = _atom['atom_id']

                        if compId is not lastCompId:
                            pseudoAtoms = self.__csStat.getPseudoAtoms(compId)
                            lastCompId = compId

                        if atomId in pseudoAtoms:
                            atomSelection.append(_atom)

                except Exception as e:
                    if self.__verbose:
                        self.__lfh.write(f"+XplorMRParserListener.exitFactor() ++ Error  - {str(e)}")

                self.intersectionFactor_expressions(atomSelection)

                if len(self.factor['atom_selection']) == 0:
                    self.factor['atom_id'] = [None]
                    self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                    "The 'pseudo' clause has no effect.")

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
                    elif symbol_name in self.evaluateFor:
                        val = self.evaluateFor[symbol_name]
                        if isinstance(val, list):
                            self.factor['seq_id'] = [v if isinstance(v, int) else int(v) for v in val]
                        else:
                            self.factor['seq_id'] = [val if isinstance(val, int) else int(val)]
                    else:
                        self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                        f"The symbol {symbol_name!r} is not defined.")

                if eval_factor and 'atom_selection' in self.factor:
                    if len(self.factor['atom_selection']) == 0 and 'atom_id' in __factor:
                        __atomId = __factor['atom_id'][0].upper() if len(__factor['atom_id'][0]) <= 2 else __factor['atom_id'][0][:2].upper()
                        if self.__with_axis and __atomId in XPLOR_RDC_PRINCIPAL_AXIS_NAMES:
                            pass
                        elif self.__with_para and (('comp_id' in __factor and __factor['atom_id'][0] == __factor['comp_id'][0] and __atomId in PARAMAGNETIC_ELEMENTS)
                                                   or __atomId in FERROMAGNETIC_ELEMENTS or __atomId in LANTHANOID_ELEMENTS):
                            pass
                        elif self.__cur_subtype == 'plane':
                            pass
                        elif self.__cur_subtype == 'dist' and __atomId in XPLOR_NITROXIDE_NAMES:
                            pass
                        else:
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
                    elif symbol_name in self.evaluateFor:
                        val = self.evaluateFor[symbol_name]
                        if isinstance(val, list):
                            self.factor['comp_id'] = [v.upper() for v in val]
                        else:
                            self.factor['comp_id'] = [val.upper()]
                    else:
                        self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                        f"The symbol {symbol_name!r} is not defined.")

                if eval_factor and 'atom_selection' in self.factor:
                    if len(self.factor['atom_selection']) == 0 and 'atom_id' in __factor:
                        __atomId = __factor['atom_id'][0].upper() if len(__factor['atom_id'][0]) <= 2 else __factor['atom_id'][0][:2].upper()
                        if self.__with_axis and __atomId in XPLOR_RDC_PRINCIPAL_AXIS_NAMES:
                            pass
                        elif self.__with_para and (('comp_id' in __factor and __factor['atom_id'][0] == __factor['comp_id'][0] and __atomId in PARAMAGNETIC_ELEMENTS)
                                                   or __atomId in FERROMAGNETIC_ELEMENTS or __atomId in LANTHANOID_ELEMENTS):
                            pass
                        elif self.__cur_subtype == 'plane':
                            pass
                        elif self.__cur_subtype == 'dist' and __atomId in XPLOR_NITROXIDE_NAMES:
                            pass
                        else:
                            _factor = copy.copy(self.factor)
                            if 'atom_selection' in __factor:
                                del __factor['atom_selection']
                            del _factor['atom_selection']
                            self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                            f"The 'resname' clause has no effect for a conjunction of factor {__factor} and {_factor}.")

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
                        elif symbol_name in self.evaluateFor:
                            val = self.evaluateFor[symbol_name]
                            if isinstance(val, list):
                                self.factor['chain_id'] = val
                            else:
                                self.factor['chain_id'] = [val]
                        else:
                            self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                            f"The symbol {symbol_name!r} is not defined.")
                    if len(self.factor['chain_id']) == 0:
                        if len(self.__fibril_chain_ids) > 0 and not self.__hasNonPoly:
                            if chainId[0] in self.__fibril_chain_ids:
                                self.factor['chain_id'] = [chainId[0]]
                        elif len(self.__polySeq) == 1:
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
                    if len(self.factor['atom_selection']) == 0 and 'atom_id' in __factor:
                        __atomId = __factor['atom_id'][0].upper() if len(__factor['atom_id'][0]) <= 2 else __factor['atom_id'][0][:2].upper()
                        if self.__with_axis and __atomId in XPLOR_RDC_PRINCIPAL_AXIS_NAMES:
                            pass
                        elif self.__with_para and (('comp_id' in __factor and __factor['atom_id'][0] == __factor['comp_id'][0] and __atomId in PARAMAGNETIC_ELEMENTS)
                                                   or __atomId in FERROMAGNETIC_ELEMENTS or __atomId in LANTHANOID_ELEMENTS):
                            pass
                        elif self.__cur_subtype == 'plane':
                            pass
                        elif self.__cur_subtype == 'dist' and __atomId in XPLOR_NITROXIDE_NAMES:
                            pass
                        else:
                            _factor = copy.copy(self.factor)
                            if 'atom_selection' in __factor:
                                del __factor['atom_selection']
                            del _factor['atom_selection']
                            self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                            f"The 'segidentifier' clause has no effect for a conjunction of factor {__factor} and {_factor}.")

            elif ctx.Store1():
                set_store(1)

            elif ctx.Store2():
                set_store(2)

            elif ctx.Store3():
                set_store(3)

            elif ctx.Store4():
                set_store(4)

            elif ctx.Store5():
                set_store(5)

            elif ctx.Store6():
                set_store(6)

            elif ctx.Store7():
                set_store(7)

            elif ctx.Store8():
                set_store(8)

            elif ctx.Store9():
                set_store(9)

            elif ctx.Tag():
                if self.__sel_expr_debug:
                    print("  " * self.depth + "--> tag")
                if not self.__hasCoord:
                    return
                atomSelection = []
                _sequenceSelect = []

                try:

                    _atomSelection =\
                        self.__cR.getDictListWithFilter('atom_site',
                                                        AUTH_ATOM_DATA_ITEMS,
                                                        [{'name': self.__modelNumName, 'type': 'int',
                                                          'value': self.__representativeModelId},
                                                         {'name': 'label_alt_id', 'type': 'enum',
                                                          'enum': ('A')}
                                                         ])

                    for _atom in _atomSelection:
                        _sequence = (_atom['chain_id'], _atom['seq_id'])

                        if _sequence in _sequenceSelect:
                            continue

                        atomSelection.append(_atom)
                        _sequenceSelect.append(_sequence)

                except Exception as e:
                    if self.__verbose:
                        self.__lfh.write(f"+XplorMRParserListener.exitFactor() ++ Error  - {str(e)}")

                self.intersectionFactor_expressions(atomSelection)

                if len(self.factor['atom_selection']) == 0:
                    self.factor['atom_id'] = [None]
                    self.__f.append(f"[Insufficient atom selection] {self.__getCurrentRestraint()}"
                                    "The 'tag' clause has no effect.")

            elif ctx.Donor():
                self.donor_columnSel = len(self.atomSelectionSet)

            elif ctx.Acceptor():
                self.acceptor_columnSel = len(self.atomSelectionSet)

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
                self.__lfh.write(f"+XplorMRParserListener.selectRealisticBondConstraint() ++ Error  - {str(e)}")

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
                self.__lfh.write(f"+XplorMRParserListener.selectRealisticChi2AngleConstraint() ++ Error  - {str(e)}")

        return dst_func

    def isRealisticDistanceRestraint(self, atom1, atom2, dst_func):
        """ Return whether a given distance restraint is realistic in the assembly.
        """
        if not self.__hasCoord:
            return True

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
                return True

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
                return True

            p2 = to_np_array(_p2[0])

            d_org = distance(p1, p2)

            lower_limit = dst_func.get('lower_limit')
            if lower_limit is not None:
                lower_limit = float(lower_limit)
            upper_limit = dst_func.get('upper_limit')
            if upper_limit is not None:
                upper_limit = float(upper_limit)

            if dist_error(lower_limit, upper_limit, d_org) >= DIST_AMBIG_UP:
                return False

        except Exception as e:
            if self.__verbose:
                self.__lfh.write(f"+XplorMRParserListener.isRealisticDistanceRestraint() ++ Error  - {str(e)}")

        return True

    # Enter a parse tree produced by XplorMRParser#number.
    def enterNumber(self, ctx: XplorMRParser.NumberContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#number.
    def exitNumber(self, ctx: XplorMRParser.NumberContext):
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

    # Enter a parse tree produced by XplorMRParser#number_f.
    def enterNumber_f(self, ctx: XplorMRParser.Number_fContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#number_f.
    def exitNumber_f(self, ctx: XplorMRParser.Number_fContext):
        if ctx.Real():
            self.numberFSelection.append(float(str(ctx.Real())))

        elif ctx.Integer():
            self.numberFSelection.append(float(str(ctx.Integer())))

        else:
            self.numberFSelection.append(None)

    # Enter a parse tree produced by XplorMRParser#number_s.
    def enterNumber_s(self, ctx: XplorMRParser.Number_sContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#number_s.
    def exitNumber_s(self, ctx: XplorMRParser.Number_sContext):  # pylint: disable=unused-argument
        pass

    def getNumber_s(self, ctx: XplorMRParser.Number_sContext):  # pylint: disable=no-self-use
        if ctx is None:
            return None

        if ctx.Real():
            return float(str(ctx.Real()))

        if ctx.Integer():
            return float(str(ctx.Integer()))

        if ctx.Symbol_name():
            return str(ctx.Symbol_name())

        return None

    # Enter a parse tree produced by XplorMRParser#number_a.
    def enterNumber_a(self, ctx: XplorMRParser.Number_aContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#number_a.
    def exitNumber_a(self, ctx: XplorMRParser.Number_aContext):  # pylint: disable=unused-argument
        pass

    def getNumber_a(self, ctx: XplorMRParser.Number_aContext):  # pylint: disable=no-self-use
        if ctx is None:
            return None

        if ctx.Real():
            return float(str(ctx.Real()))

        if ctx.Integer():
            return float(str(ctx.Integer()))

        return None

    # Enter a parse tree produced by XplorMRParser#classification.
    def enterClassification(self, ctx: XplorMRParser.ClassificationContext):
        self.classification = self.getClass_name(ctx.class_name())

    # Exit a parse tree produced by XplorMRParser#classification.
    def exitClassification(self, ctx: XplorMRParser.ClassificationContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#class_name.
    def enterClass_name(self, ctx: XplorMRParser.Class_nameContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#class_name.
    def exitClass_name(self, ctx: XplorMRParser.Class_nameContext):  # pylint: disable=unused-argument
        pass

    def getClass_name(self, ctx: XplorMRParser.Class_nameContext):  # pylint: disable=no-self-use
        if ctx is None:
            return None

        if ctx.Simple_name():
            return str(ctx.Simple_name())

        if ctx.Noe():
            return str(ctx.Noe())

        if ctx.Restraints():
            return str(ctx.Restraints())

        if ctx.AngleDb():
            return str(ctx.AngleDb())

        if ctx.HBonded():
            return str(ctx.HBonded())

        if ctx.Dihedral():
            return str(ctx.Dihedral())

        if ctx.Improper():
            return str(ctx.Improper())

        return None

    # Enter a parse tree produced by XplorMRParser#flag_statement.
    def enterFlag_statement(self, ctx: XplorMRParser.Flag_statementContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#flag_statement.
    def exitFlag_statement(self, ctx: XplorMRParser.Flag_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#vector_statement.
    def enterVector_statement(self, ctx: XplorMRParser.Vector_statementContext):  # pylint: disable=unused-argument
        self.__cur_vector_mode = ''
        self.__cur_vector_atom_prop_type = ''

        self.__cur_vflc_op_code = ''
        self.stackVflc = []

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#vector_statement.
    def exitVector_statement(self, ctx: XplorMRParser.Vector_statementContext):  # pylint: disable=unused-argument
        if self.__cur_vector_mode == 'identity':
            if self.__cur_vector_atom_prop_type.startswith('store'):
                self.storeSet[int(self.__cur_vector_atom_prop_type[-1])] = {'atom_selection': copy.copy(self.atomSelectionSet[0])}

        elif self.__cur_vector_mode == 'do':
            if len(self.__cur_vector_atom_prop_type) > 0:
                vector_name = self.__cur_vector_atom_prop_type
                if len(vector_name) > 4:
                    vector_name = vector_name[:4]
                if vector_name not in self.vectorDo:
                    self.vectorDo[vector_name] = []
                vector = {'atom_selection': copy.copy(self.atomSelectionSet[0])}
                while self.stackVflc:
                    vector['value'] = self.stackVflc.pop()
                self.vectorDo[vector_name].append(vector)

    # Enter a parse tree produced by XplorMRParser#vector_mode.
    def enterVector_mode(self, ctx: XplorMRParser.Vector_modeContext):
        if ctx.Identity_Lp():
            self.__cur_vector_mode = 'identity'

        elif ctx.Do_Lp():
            self.__cur_vector_mode = 'do'

        elif ctx.Show():
            self.__cur_vector_mode = 'show'

    # Exit a parse tree produced by XplorMRParser#vector_mode.
    def exitVector_mode(self, ctx: XplorMRParser.Vector_modeContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#vector_expression.
    def enterVector_expression(self, ctx: XplorMRParser.Vector_expressionContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#vector_expression.
    def exitVector_expression(self, ctx: XplorMRParser.Vector_expressionContext):
        if ctx.Atom_properties_VE():
            self.__cur_vector_atom_prop_type = str(ctx.Atom_properties_VE()).lower()

    # Enter a parse tree produced by XplorMRParser#vector_operation.
    def enterVector_operation(self, ctx: XplorMRParser.Vector_operationContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#vector_operation.
    def exitVector_operation(self, ctx: XplorMRParser.Vector_operationContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#vflc.
    def enterVflc(self, ctx: XplorMRParser.VflcContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#vflc.
    def exitVflc(self, ctx: XplorMRParser.VflcContext):
        if ctx.Integer_VE():
            self.stackVflc.append(int(str(ctx.Integer_VE())))
        elif ctx.Real_VE():
            self.stackVflc.append(float(str(ctx.Real_VE())))
        elif ctx.Simple_name_VE():
            self.stackVflc.append(str(ctx.Simple_name_VE()))
        elif ctx.Double_quote_string_VE():
            self.stackVflc.append(str(ctx.Double_quote_string_VE()).strip('"').strip())
        elif ctx.Symbol_name_VE():
            symbol_name = str(ctx.Symbol_name_VE())
            if symbol_name in self.evaluate:
                self.stackVflc.append(self.evaluate[symbol_name])
            elif symbol_name in self.evaluateFor:
                self.stackVflc.append(self.evaluateFor[symbol_name])
            else:
                self.__f.append(f"[Unsupported data] {self.__getCurrentRestraint()}"
                                f"The symbol {symbol_name!r} is not defined.")
        elif ctx.Atom_properties_VE():
            pass
        elif ctx.vector_func_call():
            pass

    # Enter a parse tree produced by XplorMRParser#vector_func_call.
    def enterVector_func_call(self, ctx: XplorMRParser.Vector_func_callContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#vector_func_call.
    def exitVector_func_call(self, ctx: XplorMRParser.Vector_func_callContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#vector_show_property.
    def enterVector_show_property(self, ctx: XplorMRParser.Vector_show_propertyContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#vector_show_property.
    def exitVector_show_property(self, ctx: XplorMRParser.Vector_show_propertyContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#evaluate_statement.
    def enterEvaluate_statement(self, ctx: XplorMRParser.Evaluate_statementContext):
        if ctx.Symbol_name_VE():
            self.__cur_symbol_name = str(ctx.Symbol_name_VE())

        self.__cur_vflc_op_code = ''
        self.stackVflc = []

    # Exit a parse tree produced by XplorMRParser#evaluate_statement.
    def exitEvaluate_statement(self, ctx: XplorMRParser.Evaluate_statementContext):  # pylint: disable=unused-argument
        if self.stackVflc:
            self.evaluate[self.__cur_symbol_name] = self.stackVflc[0]

            if self.__cur_vflc_op_code in ('+', '-', '*', '/', '^'):
                s = self.stackVflc[0]
                n = self.stackVflc[1]
                if isinstance(s, list) and not isinstance(n, list):
                    if self.__cur_vflc_op_code == '+':
                        self.evaluate[self.__cur_symbol_name] = [_s + n for _s in s]
                    elif self.__cur_vflc_op_code == '-':
                        self.evaluate[self.__cur_symbol_name] = [_s - n for _s in s]
                    elif self.__cur_vflc_op_code == '*':
                        self.evaluate[self.__cur_symbol_name] = [_s * n for _s in s]
                    elif self.__cur_vflc_op_code == '/':
                        self.evaluate[self.__cur_symbol_name] = [_s / n for _s in s]
                    elif self.__cur_vflc_op_code == '^':
                        self.evaluate[self.__cur_symbol_name] = [_s ** n for _s in s]
                elif not isinstance(s, list) and isinstance(n, list):
                    if self.__cur_vflc_op_code == '+':
                        self.evaluate[self.__cur_symbol_name] = [s + _n for _n in n]
                    elif self.__cur_vflc_op_code == '-':
                        self.evaluate[self.__cur_symbol_name] = [s - _n for _n in n]
                    elif self.__cur_vflc_op_code == '*':
                        self.evaluate[self.__cur_symbol_name] = [s * _n for _n in n]
                    elif self.__cur_vflc_op_code == '/':
                        self.evaluate[self.__cur_symbol_name] = [s / _n for _n in n]
                    elif self.__cur_vflc_op_code == '^':
                        self.evaluate[self.__cur_symbol_name] = [s ** _n for _n in n]
                elif isinstance(s, list) and isinstance(n, list):
                    if self.__cur_vflc_op_code == '+':
                        self.evaluate[self.__cur_symbol_name] = [_s + _n for _s, _n in zip(s, n)]
                    elif self.__cur_vflc_op_code == '-':
                        self.evaluate[self.__cur_symbol_name] = [_s - _n for _s, _n in zip(s, n)]
                    elif self.__cur_vflc_op_code == '*':
                        self.evaluate[self.__cur_symbol_name] = [_s * _n for _s, _n in zip(s, n)]
                    elif self.__cur_vflc_op_code == '/':
                        self.evaluate[self.__cur_symbol_name] = [_s / _n for _s, _n in zip(s, n)]
                    elif self.__cur_vflc_op_code == '^':
                        self.evaluate[self.__cur_symbol_name] = [_s ** _n for _s, _n in zip(s, n)]
                else:
                    if self.__cur_vflc_op_code == '+':
                        self.evaluate[self.__cur_symbol_name] = s + n
                    elif self.__cur_vflc_op_code == '-':
                        self.evaluate[self.__cur_symbol_name] = s - n
                    elif self.__cur_vflc_op_code == '*':
                        self.evaluate[self.__cur_symbol_name] = s * n
                    elif self.__cur_vflc_op_code == '/':
                        self.evaluate[self.__cur_symbol_name] = s / n
                    elif self.__cur_vflc_op_code == '^':
                        self.evaluate[self.__cur_symbol_name] = s ** n

        self.stackVflc.clear()

    # Enter a parse tree produced by XplorMRParser#evaluate_operation.
    def enterEvaluate_operation(self, ctx: XplorMRParser.Evaluate_operationContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#evaluate_operation.
    def exitEvaluate_operation(self, ctx: XplorMRParser.Evaluate_operationContext):
        if ctx.Add_op_VE():
            self.__cur_vflc_op_code = '+'
        elif ctx.Sub_op_VE():
            self.__cur_vflc_op_code = '-'
        elif ctx.Mul_op_VE():
            self.__cur_vflc_op_code = '*'
        elif ctx.Div_op_VE():
            self.__cur_vflc_op_code = '/'
        elif ctx.Exp_op_VE():
            self.__cur_vflc_op_code = '^'

    # Enter a parse tree produced by XplorMRParser#patch_statement.
    def enterPatch_statement(self, ctx: XplorMRParser.Patch_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1
        self.__cur_subtype = 'geo'

        self.atomSelectionSet.clear()
        self.__g.clear()

    # Exit a parse tree produced by XplorMRParser#patch_statement.
    def exitPatch_statement(self, ctx: XplorMRParser.Patch_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#parameter_setting.
    def enterParameter_setting(self, ctx: XplorMRParser.Parameter_settingContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XplorMRParser#parameter_setting.
    def exitParameter_setting(self, ctx: XplorMRParser.Parameter_settingContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#parameter_statement.
    def enterParameter_statement(self, ctx: XplorMRParser.Parameter_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1
        self.__cur_subtype = 'geo'

    # Exit a parse tree produced by XplorMRParser#parameter_statement.
    def exitParameter_statement(self, ctx: XplorMRParser.Parameter_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XplorMRParser#noe_assign_loop.
    def enterNoe_assign_loop(self, ctx: XplorMRParser.Noe_assign_loopContext):
        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by XplorMRParser#noe_assign_loop.
    def exitNoe_assign_loop(self, ctx: XplorMRParser.Noe_assign_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

    # Enter a parse tree produced by XplorMRParser#dihedral_assign_loop.
    def enterDihedral_assign_loop(self, ctx: XplorMRParser.Dihedral_assign_loopContext):
        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by XplorMRParser#dihedral_assign_loop.
    def exitDihedral_assign_loop(self, ctx: XplorMRParser.Dihedral_assign_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

    # Enter a parse tree produced by XplorMRParser#sani_assign_loop.
    def enterSani_assign_loop(self, ctx: XplorMRParser.Sani_assign_loopContext):
        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by XplorMRParser#sani_assign_loop.
    def exitSani_assign_loop(self, ctx: XplorMRParser.Sani_assign_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

    # Enter a parse tree produced by XplorMRParser#xadc_assign_loop.
    def enterXadc_assign_loop(self, ctx: XplorMRParser.Xadc_assign_loopContext):
        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by XplorMRParser#xadc_assign_loop.
    def exitXadc_assign_loop(self, ctx: XplorMRParser.Xadc_assign_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

    # Enter a parse tree produced by XplorMRParser#coup_assign_loop.
    def enterCoup_assign_loop(self, ctx: XplorMRParser.Coup_assign_loopContext):
        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by XplorMRParser#coup_assign_loop.
    def exitCoup_assign_loop(self, ctx: XplorMRParser.Coup_assign_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

    # Enter a parse tree produced by XplorMRParser#coll_assign_loop.
    def enterColl_assign_loop(self, ctx: XplorMRParser.Coll_assign_loopContext):
        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by XplorMRParser#coll_assign_loop.
    def exitColl_assign_loop(self, ctx: XplorMRParser.Coll_assign_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

    # Enter a parse tree produced by XplorMRParser#csa_assign_loop.
    def enterCsa_assign_loop(self, ctx: XplorMRParser.Csa_assign_loopContext):
        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by XplorMRParser#csa_assign_loop.
    def exitCsa_assign_loop(self, ctx: XplorMRParser.Csa_assign_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

    # Enter a parse tree produced by XplorMRParser#pre_assign_loop.
    def enterPre_assign_loop(self, ctx: XplorMRParser.Pre_assign_loopContext):
        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by XplorMRParser#pre_assign_loop.
    def exitPre_assign_loop(self, ctx: XplorMRParser.Pre_assign_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

    # Enter a parse tree produced by XplorMRParser#pcs_assign_loop.
    def enterPcs_assign_loop(self, ctx: XplorMRParser.Pcs_assign_loopContext):
        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by XplorMRParser#pcs_assign_loop.
    def exitPcs_assign_loop(self, ctx: XplorMRParser.Pcs_assign_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

    # Enter a parse tree produced by XplorMRParser#hbond_assign_loop.
    def enterHbond_assign_loop(self, ctx: XplorMRParser.Hbond_assign_loopContext):
        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by XplorMRParser#hbond_assign_loop.
    def exitHbond_assign_loop(self, ctx: XplorMRParser.Hbond_assign_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

    # Enter a parse tree produced by XplorMRParser#hbond_db_assign_loop.
    def enterHbond_db_assign_loop(self, ctx: XplorMRParser.Hbond_db_assign_loopContext):
        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by XplorMRParser#hbond_db_assign_loop.
    def exitHbond_db_assign_loop(self, ctx: XplorMRParser.Hbond_db_assign_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

    # Enter a parse tree produced by XplorMRParser#planar_group_loop.
    def enterPlanar_group_loop(self, ctx: XplorMRParser.Planar_group_loopContext):
        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by XplorMRParser#planar_group_loop.
    def exitPlanar_group_loop(self, ctx: XplorMRParser.Planar_group_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

    def __getCurrentRestraint(self):
        if self.__cur_subtype == 'dist':
            return f"[Check the {self.distRestraints}th row of distance restraints] "
        if self.__cur_subtype == 'dihed':
            return f"[Check the {self.dihedRestraints}th row of dihedral angle restraints] "
        if self.__cur_subtype == 'rdc':
            return f"[Check the {self.rdcRestraints}th row of residual dipolar coupling restraints] "
        if self.__cur_subtype == 'plane':
            return f"[Check the {self.planeRestraints}th row of planarity restraints] "
        if self.__cur_subtype == 'adist':
            return f"[Check the {self.adistRestraints}th row of antidistance restraints] "
        if self.__cur_subtype == 'jcoup':
            return f"[Check the {self.jcoupRestraints}th row of scalar J-coupling restraints] "
        if self.__cur_subtype == 'hvycs':
            return f"[Check the {self.hvycsRestraints}th row of carbon chemical shift restraints] "
        if self.__cur_subtype == 'procs':
            return f"[Check the {self.procsRestraints}th row of proton chemical shift restraints] "
        if self.__cur_subtype == 'rama':
            return f"[Check the {self.ramaRestraints}th row of dihedral angle database restraints] "
        if self.__cur_subtype == 'radi':
            return f"[Check the {self.radiRestraints}th row of radius of gyration restraints] "
        if self.__cur_subtype == 'diff':
            return f"[Check the {self.diffRestraints}th row of duffusion anisotropy restraints] "
        if self.__cur_subtype == 'nbase':
            return f"[Check the {self.nbaseRestraints}th row of residue-residue position/orientation database restraints] "
        if self.__cur_subtype == 'csa':
            return f"[Check the {self.csaRestraints}th row of (pseudo) chemical shift anisotropy restraints] "
        # if self.__cur_subtype == 'ang':
        #     return f"[Check the {self.angRestraints}th row of angle database restraints] "
        if self.__cur_subtype == 'pre':
            return f"[Check the {self.preRestraints}th row of paramagnetic relaxation enhancement restraints] "
        if self.__cur_subtype == 'pcs':
            return f"[Check the {self.pcsRestraints}th row of paramagnetic pseudocontact shift restraints] "
        if self.__cur_subtype == 'prdc':
            return f"[Check the {self.prdcRestraints}th row of paramagnetic residual dipolar coupling restraints] "
        if self.__cur_subtype == 'pang':
            return f"[Check the {self.pangRestraints}th row of paramagnetic orientation restraints] "
        if self.__cur_subtype == 'pccr':
            return f"[Check the {self.pccrRestraints}th row of paramagnetic cross-correlation rate restraints] "
        if self.__cur_subtype == 'hbond':
            return f"[Check the {self.hbondRestraints}th row of hydrogen bond geometry restraints] "
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
        elif self.__cur_subtype == 'rdc':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.rdcRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'plane':
            self.reasonsForReParsing['loca_seq_scheme'][(self.__cur_subtype, self.planeRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'adist':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.adistRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'jcoup':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.jcoupRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'hvycs':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.hvycsRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'procs':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.procsRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'rama':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.ramaRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'radi':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.radiRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'diff':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.diffRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'nbase':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.nbaseRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'csa':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.csaRestraints)] = self.__preferAuthSeq
        # elif self.__cur_subtype == 'ang':
        #     self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.angRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'pre':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.preRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'pcs':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.pcsRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'prdc':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.prdcRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'pang':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.pangRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'pccr':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.pccrRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'hbond':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.hbondRestraints)] = self.__preferAuthSeq
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
        elif self.__cur_subtype == 'rdc':
            key = (self.__cur_subtype, self.rdcRestraints)
        elif self.__cur_subtype == 'plane':
            key = (self.__cur_subtype, self.planeRestraints)
        elif self.__cur_subtype == 'adist':
            key = (self.__cur_subtype, self.adistRestraints)
        elif self.__cur_subtype == 'jcoup':
            key = (self.__cur_subtype, self.jcoupRestraints)
        elif self.__cur_subtype == 'hvycs':
            key = (self.__cur_subtype, self.hvycsRestraints)
        elif self.__cur_subtype == 'procs':
            key = (self.__cur_subtype, self.procsRestraints)
        elif self.__cur_subtype == 'rama':
            key = (self.__cur_subtype, self.ramaRestraints)
        elif self.__cur_subtype == 'radi':
            key = (self.__cur_subtype, self.radiRestraints)
        elif self.__cur_subtype == 'diff':
            key = (self.__cur_subtype, self.diffRestraints)
        elif self.__cur_subtype == 'nbase':
            key = (self.__cur_subtype, self.nbaseRestraints)
        elif self.__cur_subtype == 'csa':
            key = (self.__cur_subtype, self.csaRestraints)
        # elif self.__cur_subtype == 'ang':
        #     key = (self.__cur_subtype, self.angRestraints)
        elif self.__cur_subtype == 'pre':
            key = (self.__cur_subtype, self.preRestraints)
        elif self.__cur_subtype == 'pcs':
            key = (self.__cur_subtype, self.pcsRestraints)
        elif self.__cur_subtype == 'prdc':
            key = (self.__cur_subtype, self.prdcRestraints)
        elif self.__cur_subtype == 'pang':
            key = (self.__cur_subtype, self.pangRestraints)
        elif self.__cur_subtype == 'pccr':
            key = (self.__cur_subtype, self.pccrRestraints)
        elif self.__cur_subtype == 'hbond':
            key = (self.__cur_subtype, self.hbondRestraints)
        elif self.__cur_subtype == 'geo':
            key = (self.__cur_subtype, self.geoRestraints)
        else:
            return

        if key in self.__reasons['local_seq_scheme']:
            self.__preferAuthSeq = self.__reasons['local_seq_scheme'][key]

    def __addSf(self, constraintType=None, potentialType=None, rdcCode=None,
                alignCenter=None):
        content_subtype = contentSubtypeOf(self.__cur_subtype)

        if content_subtype is None:
            return

        self.__cur_constraint_type = constraintType

        self.__listIdCounter = incListIdCounter(self.__cur_subtype, self.__listIdCounter)

        key = (self.__cur_subtype, constraintType, potentialType, rdcCode, None if alignCenter is None else str(alignCenter))

        if self.__cur_subtype not in self.sfDict:
            self.sfDict[key] = []

        list_id = self.__listIdCounter[content_subtype]

        cns_compatible_types = ['dist', 'dihed', 'rdc', 'plane', 'jcoup', 'hvycs', 'procs', 'rama', 'diff', 'nbase', 'geo']

        restraint_name = getRestraintName(self.__cur_subtype)

        sf_framecode = ('XPLOR-NIH/CNS' if self.__remediate and self.__cur_subtype in cns_compatible_types else 'XPLOR-NIH')\
            + '_' + restraint_name.replace(' ', '_') + f'_{list_id}'

        sf = getSaveframe(self.__cur_subtype, sf_framecode, list_id, self.__entryId, self.__originalFileName,
                          constraintType=constraintType, potentialType=potentialType, rdcCode=rdcCode,
                          alignCenter=alignCenter)

        not_valid = True

        lp = getLoop(self.__cur_subtype, hasInsCode=self.__authToInsCode is not None)
        if not isinstance(lp, dict):
            sf.add_loop(lp)
            not_valid = False

        _restraint_name = restraint_name.split()

        item = {'file_type': self.__file_type, 'saveframe': sf, 'loop': lp, 'list_id': list_id,
                'id': 0, 'index_id': 0,
                'constraint_type': ' '.join(_restraint_name[:-1])}

        if not_valid:
            item['tags'] = []

        if self.__cur_subtype == 'dist':
            item['constraint_subsubtype'] = 'simple'
            if constraintType is None:
                item['NOE_dist_averaging_method'] = self.noeAverage
            elif 'ROE' in constraintType:
                item['ROE_dist_averaging_method'] = self.noeAverage

        self.__lastSfDict[self.__cur_subtype] = item

        self.sfDict[key].append(item)

    def __getSf(self, constraintType=None, potentialType=None, rdcCode=None,
                alignCenter=None):
        key = (self.__cur_subtype, constraintType, potentialType, rdcCode, None if alignCenter is None else str(alignCenter))

        if key not in self.sfDict:
            replaced = False
            if potentialType is not None or rdcCode is not None or alignCenter is not None:
                old_key = (self.__cur_subtype, self.__cur_constraint_type, None, None, None)
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
            elif constraintType is not None:
                old_key = (self.__cur_subtype, None, None, None, None)
                if old_key in self.sfDict:
                    replaced = True
                    self.sfDict[key] = [self.sfDict[old_key].pop(-1)]
            if not replaced:
                self.__addSf(constraintType=constraintType, potentialType=potentialType, rdcCode=rdcCode,
                             alignCenter=alignCenter)

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
        """ Return content subtype of XPLOR-NIH MR file.
        """

        if self.distStatements == 0 and self.distRestraints > 0:
            self.distStatements = 1

        if self.dihedStatements == 0 and self.dihedRestraints > 0:
            self.dihedStatements = 1

        if self.rdcStatements == 0 and self.rdcRestraints > 0:
            self.rdcStatements = 1

        if self.planeStatements == 0 and self.planeRestraints > 0:
            self.planeStatements = 1

        if self.adistStatements == 0 and self.adistRestraints > 0:
            self.adistStatements = 1

        if self.jcoupStatements == 0 and self.jcoupRestraints > 0:
            self.jcoupStatements = 1

        if self.hvycsStatements == 0 and self.hvycsRestraints > 0:
            self.hvycsStatements = 1

        if self.procsStatements == 0 and self.procsRestraints > 0:
            self.procsStatements = 1

        if self.ramaStatements == 0 and self.ramaRestraints > 0:
            self.ramaStatements = 1

        if self.radiStatements == 0 and self.radiRestraints > 0:
            self.radiStatements = 1

        if self.diffStatements == 0 and self.diffRestraints > 0:
            self.diffStatements = 1

        if self.nbaseStatements == 0 and self.nbaseRestraints > 0:
            self.nbaseStatements = 1

        if self.csaStatements == 0 and self.csaRestraints > 0:
            self.csaStatements = 1

        # if self.angStatements == 0 and self.angRestraints > 0:
        #     self.angStatements = 1

        if self.preStatements == 0 and self.preRestraints > 0:
            self.preStatements = 1

        if self.pcsStatements == 0 and self.pcsRestraints > 0:
            self.pcsStatements = 1

        if self.prdcStatements == 0 and self.prdcRestraints > 0:
            self.prdcStatements = 1

        if self.pangStatements == 0 and self.pangRestraints > 0:
            self.pangStatements = 1

        if self.pccrStatements == 0 and self.pccrRestraints > 0:
            self.pccrStatements = 1

        if self.hbondStatements == 0 and self.hbondRestraints > 0:
            self.hbondStatements = 1

        if self.geoStatements == 0 and self.geoRestraints > 0:
            self.geoStatements = 1

        contentSubtype = {'dist_restraint': self.distStatements,
                          'dihed_restraint': self.dihedStatements,
                          'rdc_restraint': self.rdcStatements,
                          'plane_restraint': self.planeStatements,
                          'adist_restraint': self.adistStatements,
                          'jcoup_restraint': self.jcoupStatements,
                          'hvycs_restraint': self.hvycsStatements,
                          'procs_restraint': self.procsStatements,
                          'rama_restraint': self.ramaStatements,
                          'radi_restraint': self.radiStatements,
                          'diff_restraint': self.diffStatements,
                          'nbase_restraint': self.nbaseStatements,
                          'csa_restraint': self.csaStatements,
                          # 'ang_restraint': self.angStatements,
                          'pre_restraint': self.preStatements,
                          'pcs_restraint': self.pcsStatements,
                          'prdc_restraint': self.prdcStatements,
                          'pang_restraint': self.pangStatements,
                          'pccr_restraint': self.pccrStatements,
                          'hbond_restraint': self.hbondStatements,
                          'geo_restraint': self.geoStatements
                          }

        return {k: v for k, v in contentSubtype.items() if v > 0}

    def getPolymerSequence(self):
        """ Return polymer sequence of XPLOR-NIH MR file.
        """
        return None if self.__polySeqRst is None or len(self.__polySeqRst) == 0 else self.__polySeqRst

    def getSequenceAlignment(self):
        """ Return sequence alignment between coordinates and XPLOR-NIH MR.
        """
        return None if self.__seqAlign is None or len(self.__seqAlign) == 0 else self.__seqAlign

    def getChainAssignment(self):
        """ Return chain assignment between coordinates and XPLOR-NIH MR.
        """
        return None if self.__chainAssign is None or len(self.__chainAssign) == 0 else self.__chainAssign

    def getReasonsForReparsing(self):
        """ Return reasons for re-parsing XPLOR-NIH MR file.
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

# del XplorMRParser
