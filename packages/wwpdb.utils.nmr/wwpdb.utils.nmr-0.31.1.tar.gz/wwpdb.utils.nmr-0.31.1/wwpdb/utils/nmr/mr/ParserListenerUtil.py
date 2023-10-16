##
# File: ParserListenerUtil.py
# Date: 18-Feb-2022
#
# Updates:
# 13-Sep-2023  M. Yokochi - construct pseudo CCD from the coordinates (DAOTHER-8817)
# 29-Sep-2023  M. Yokochi - add atom name mapping dictionary (DAOTHER-8817, 8828)
""" Utilities for MR/PT parser listener.
    @author: Masashi Yokochi
"""
import sys
import re
import copy
import collections
import itertools

import numpy

import pynmrstar

from operator import itemgetter

try:
    from wwpdb.utils.nmr.AlignUtil import (monDict3,
                                           emptyValue,
                                           protonBeginCode,
                                           pseProBeginCode,
                                           aminoProtonCode,
                                           LARGE_ASYM_ID,
                                           LEN_LARGE_ASYM_ID,
                                           MAX_MAG_IDENT_ASYM_ID,
                                           alignPolymerSequence,
                                           assignPolymerSequence,
                                           getScoreOfSeqAlign)
    from wwpdb.utils.nmr.io.CifReader import SYMBOLS_ELEMENT
except ImportError:
    from nmr.AlignUtil import (monDict3,
                               emptyValue,
                               protonBeginCode,
                               pseProBeginCode,
                               aminoProtonCode,
                               LARGE_ASYM_ID,
                               LEN_LARGE_ASYM_ID,
                               MAX_MAG_IDENT_ASYM_ID,
                               alignPolymerSequence,
                               assignPolymerSequence,
                               getScoreOfSeqAlign)
    from nmr.io.CifReader import SYMBOLS_ELEMENT

MAX_ERROR_REPORT = 1
MAX_ERR_LINENUM_REPORT = 20

# isotope numbers of NMR observable nucleus
ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS = {'H': [1, 2, 3],
                                   'C': [13],
                                   'N': [15, 14],
                                   'O': [17],
                                   'P': [31],
                                   'S': [33],
                                   'F': [19],
                                   'CD': [113, 111],
                                   'CA': [43]
                                   }


# nucleus with half spin
HALF_SPIN_NUCLEUS = ('H', 'C', 'N', 'P', 'F', 'CD')


# allowed BMRB ambiguity codes
ALLOWED_AMBIGUITY_CODES = (1, 2, 3, 4, 5, 6, 9)


ALLOWED_ISOTOPE_NUMBERS = []
for isotopeNums in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.values():
    ALLOWED_ISOTOPE_NUMBERS.extend(isotopeNums)

WELL_KNOWN_ISOTOPE_NUMBERS = copy.copy(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS['H'])
WELL_KNOWN_ISOTOPE_NUMBERS.extend(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS['C'])
WELL_KNOWN_ISOTOPE_NUMBERS.extend(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS['N'])
WELL_KNOWN_ISOTOPE_NUMBERS.extend(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS['P'])


REPRESENTATIVE_MODEL_ID = 1


MAX_PREF_LABEL_SCHEME_COUNT = 100


THRESHHOLD_FOR_CIRCULAR_SHIFT = 340


DIST_RESTRAINT_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 101.0}
DIST_RESTRAINT_ERROR = {'min_exclusive': 0.0, 'max_exclusive': 150.0}


ANGLE_RESTRAINT_RANGE = {'min_inclusive': -341.0, 'max_inclusive': 341.0}
ANGLE_RESTRAINT_ERROR = {'min_exclusive': -360.0, 'max_exclusive': 360.0}


RDC_RESTRAINT_RANGE = {'min_inclusive': -150.0, 'max_inclusive': 150.0}
RDC_RESTRAINT_ERROR = {'min_exclusive': -200.0, 'max_exclusive': 200.0}


CS_RESTRAINT_RANGE = {'min_inclusive': -300.0, 'max_inclusive': 300.0}
CS_RESTRAINT_ERROR = {'min_exclusive': -999.0, 'max_exclusive': 999.0}


CSA_RESTRAINT_RANGE = {'min_inclusive': -300.0, 'max_inclusive': 300.0}
CSA_RESTRAINT_ERROR = {'min_exclusive': -999.0, 'max_exclusive': 999.0}


PCS_RESTRAINT_RANGE = {'min_inclusive': -20.0, 'max_inclusive': 20.0}
PCS_RESTRAINT_ERROR = {'min_exclusive': -40.0, 'max_exclusive': 40.0}


CCR_RESTRAINT_RANGE = {'min_inclusive': -10.0, 'max_inclusive': 10.0}
CCR_RESTRAINT_ERROR = {'min_exclusive': -20.0, 'max_exclusive': 20.0}


PRE_RESTRAINT_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 20.0}
PRE_RESTRAINT_ERROR = {'min_exclusive': 0.0, 'max_exclusive': 40.0}


T1T2_RESTRAINT_RANGE = {'min_inclusive': 1.0, 'max_inclusive': 20.0}
T1T2_RESTRAINT_ERROR = {'min_exclusive': 0.0, 'max_exclusive': 100.0}


CS_UNCERTAINTY_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 3.0}

DIST_UNCERTAINTY_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 5.0}

ANGLE_UNCERTAINTY_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 90.0}

RDC_UNCERTAINTY_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 5.0}

WEIGHT_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 100.0}

SCALE_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 100.0}

PROBABILITY_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 1.0}

DIST_AMBIG_LOW = 1.0
DIST_AMBIG_BND = 4.0
DIST_AMBIG_MED = 6.0
DIST_AMBIG_UP = 12.0
DIST_AMBIG_UNCERT = 0.1

# @see: https://x3dna.org/highlights/torsion-angles-of-nucleic-acid-structures for nucleic acids
KNOWN_ANGLE_ATOM_NAMES = {'PHI': ['C', 'N', 'CA', 'C'],  # i-1, i, i, i
                          'PSI': ['N', 'CA', 'C', 'N'],  # i, i, i, i+1
                          'OMEGA': ['CA', 'C', 'N', 'CA'],  # i, i, i+1, i+1; modified CYANA definition [O C N (H or CD for Proline residue)]
                          'CHI1': ['N', 'CA', 'CB', re.compile(r'^[COS]G1?$')],
                          'CHI2': ['CA', 'CB', re.compile(r'^CG1?$'), re.compile(r'^[CNOS]D1?$')],
                          'CHI3': ['CB', 'CG', re.compile(r'^[CS]D$'), re.compile(r'^[CNO]E1?$')],
                          'CHI4': ['CG', 'CD', re.compile(r'^[CN]E$'), re.compile(r'^[CN]Z$')],
                          'CHI5': ['CD', 'NE', 'CZ', 'NH1'],
                          'CHI21': ['CA', 'CB', re.compile(r'^[CO]G1$'), re.compile(r'^CD1|HG11?$')],  # ILE: (CG1, CD1), THR: (OG1, HG1), VAL: (CD1, HG11)
                          'CHI22': ['CA', 'CB', 'CG2', 'HG21'],  # ILE or THR or VAL
                          'CHI31': ['CB', re.compile(r'^CG1?$'), 'CD1', 'HD11'],  # ILE: CG1, LEU: CG
                          'CHI32': ['CB', 'CG', re.compile(r'^[CO]D2$'), re.compile(r'^HD21?$')],  # ASP: (OD2, HD2), LEU: (CD2, HD21)
                          'CHI42': ['CG', 'CD', 'OE2', 'HE2'],  # GLU
                          'ALPHA': ["O3'", 'P', "O5'", "C5'"],  # i-1, i, i, i
                          'BETA': ['P', "O5'", "C5'", "C4'"],
                          'GAMMA': ["O5'", "C5'", "C4'", "C3'"],
                          'DELTA': ["C5'", "C4'", "C3'", "O3'"],
                          'EPSILON': ["C4'", "C3'", "O3'", 'P'],  # i, i, i, i+1
                          'ZETA': ["C3'", "O3'", 'P', "O5'"],  # i, i, i+1, i+1
                          # aka. CHIN (nucleic CHI angle)
                          'CHI': {'Y': ["O4'", "C1'", 'N1', 'C2'],  # for pyrimidines (i.e. C, T, U) N1/3
                                  'R': ["O4'", "C1'", 'N9', 'C4']  # for purines (i.e. G, A) N1/3/7/9
                                  },
                          'ETA': ["C4'", 'P', "C4'", 'P'],  # i-1, i, i, i+1
                          'THETA': ['P', "C4'", 'P', "C4'"],  # i, i, i+1, i+1
                          "ETA'": ["C1'", 'P', "C1'", 'P'],  # i-1, i, i, i+1
                          "THETA'": ['P', "C1'", 'P', "C1'"],  # i, i, i+1, i+1
                          'NU0': ["C4'", "O4'", "C1'", "C2'"],
                          'NU1': ["O4'", "C1'", "C2'", "C3'"],
                          'NU2': ["C1'", "C2'", "C3'", "C4'"],
                          'NU3': ["C2'", "C3'", "C4'", "O4'"],
                          'NU4': ["C3'", "C4'", "O4'", "C1'"],
                          'TAU0': ["C4'", "O4'", "C1'", "C2'"],  # identical to NU0
                          'TAU1': ["O4'", "C1'", "C2'", "C3'"],  # identical to NU1
                          'TAU2': ["C1'", "C2'", "C3'", "C4'"],  # identical to NU2
                          'TAU3': ["C2'", "C3'", "C4'", "O4'"],  # identical to NU3
                          'TAU4': ["C3'", "C4'", "O4'", "C1'"],  # identical to NU4
                          'PPA': ["C1'", "C2'", "C3'", "C4'", "O4'"]  # phase angle of pseudorotation made up from five NU[0-4] dihedral angles
                          }

# @see: http://dx.doi.org/10.1107/S0907444909001905
KNOWN_ANGLE_CARBO_ATOM_NAMES = {'PHI': [re.compile(r'^H1|O5$'), 'C1', re.compile(r'^O[14]$'), re.compile(r'^C[46]$')],
                                'PSI': ['C1', re.compile(r'^O[14]$'), re.compile(r'^C[46]$'), re.compile(r'^H4|C[35]$')],
                                'OMEGA': [re.compile(r'^O[14]$'), 'C6', 'C5', re.compile('^H5|C4|O5$')]}

KNOWN_ANGLE_NAMES = KNOWN_ANGLE_ATOM_NAMES.keys()

KNOWN_ANGLE_SEQ_OFFSET = {'PHI': [-1, 0, 0, 0],  # i-1, i, i, i
                          'PSI': [0, 0, 0, 1],  # i, i, i, i+1
                          'OMEGA': [0, 0, 1, 1],  # i, i, i+1, i+1; modified CYANA definition [O C N (H or CD for Proline residue)]
                          'CHI1': [0] * 4,
                          'CHI2': [0] * 4,
                          'CHI3': [0] * 4,
                          'CHI4': [0] * 4,
                          'CHI5': [0] * 4,
                          'CHI21': [0] * 4,  # ILE: (CG1, CD1), THR: (OG1, HG1), VAL: (CD1, HG11)
                          'CHI22': [0] * 4,  # ILE or THR or VAL
                          'CHI31': [0] * 4,  # ILE: CG1, LEU: CG
                          'CHI32': [0] * 4,  # ASP: (OD2, HD2), LEU: (CD2, HD21)
                          'CHI42': [0] * 4,  # GLU
                          'ALPHA': [-1, 0, 0, 0],  # i-1, i, i, i
                          'BETA': [0] * 4,
                          'GAMMA': [0] * 4,
                          'DELTA': [0] * 4,
                          'EPSILON': [0, 0, 0, 1],  # i, i, i, i+1
                          'ZETA': [0, 0, 1, 1],  # i, i, i+1, i+1
                          # aka. CHIN (nucleic CHI angle)
                          'CHI': {'Y': [0] * 4,  # for pyrimidines (i.e. C, T, U) N1/3
                                  'R': [0] * 4  # for purines (i.e. G, A) N1/3/7/9
                                  },
                          'ETA': [-1, 0, 0, 1],  # i-1, i, i, i+1
                          'THETA': [0, 0, 1, 1],  # i, i, i+1, i+1
                          "ETA'": [-1, 0, 0, 1],  # i-1, i, i, i+1
                          "THETA'": [0, 0, 1, 1],  # i, i, i+1, i+1
                          'NU0': [0] * 4,
                          'NU1': [0] * 4,
                          'NU2': [0] * 4,
                          'NU3': [0] * 4,
                          'NU4': [0] * 4,
                          'TAU0': [0] * 4,  # identical to NU0
                          'TAU1': [0] * 4,  # identical to NU1
                          'TAU2': [0] * 4,  # identical to NU2
                          'TAU3': [0] * 4,  # identical to NU3
                          'TAU4': [0] * 4,  # identical to NU4
                          'PPA': [0] * 5  # phase angle of pseudorotation made up from five NU[0-4] dihedral angles
                          }

KNOWN_ANGLE_CARBO_SEQ_OFFSET = {'PHI': [0, 0, 0, -1],  # i, i, i, i-n; for n > 0
                                'PSI': [0, 0, -1, -1],  # i, i, i-n, i-n; for n > 0
                                'OMEGA': [0, -1, -1, -1]  # i, i-n, i-n, i-n; for n > 0
                                }

XPLOR_RDC_PRINCIPAL_AXIS_NAMES = ('OO', 'X', 'Y', 'Z')

XPLOR_ORIGIN_AXIS_COLS = [0, 1, 2, 3]

XPLOR_NITROXIDE_NAMES = ('NO', 'NX', 'NR', 'NAI')

LEGACY_PDB_RECORDS = ['HEADER', 'OBSLTE', 'TITLE ', 'SPLIT ', 'CAVEAT', 'COMPND', 'SOURCE', 'KEYWDS', 'EXPDAT',
                      'NUMMDL', 'MDLTYP', 'AUTHOR', 'REVDAT', 'SPRSDE', 'JRNL', 'REMARK',
                      'DBREF', 'DBREF1', 'DBREF2', 'SEQADV', 'SEQRES', 'MODRES',
                      'HET ', 'HETNAM', 'HETSYN', 'FORMUL',
                      'HELIX ', 'SHEET ',
                      'SSBOND', 'LINK ', 'CISPEP',
                      'SITE ',
                      'CRYST1', 'ORIGX1', 'ORIGX2', 'ORIGX3', 'SCALE1', 'SCALE2', 'SCALE3',
                      'MTRIX1', 'MTRIX2', 'MTRIX3',
                      'MODEL ', 'ATOM ', 'ANISOU', 'TER ', 'HETATM', 'ENDMDL',
                      'CONECT',
                      'MASTER'
                      ]

CYANA_MR_FILE_EXTS = (None, 'upl', 'lol', 'aco', 'rdc', 'pcs', 'upv', 'lov', 'cco')

NMR_STAR_SF_TAG_PREFIXES = {'dist_restraint': '_Gen_dist_constraint_list',
                            'dihed_restraint': '_Torsion_angle_constraint_list',
                            'rdc_restraint': '_RDC_constraint_list',
                            'noepk_restraint': '_Homonucl_NOE_list',
                            'jcoup_restraint': '_J_three_bond_constraint_list',
                            'rdc_raw_data': '_RDC_list',
                            'csa_restraint': '_Chem_shift_anisotropy',
                            'ddc_restraint': '_Dipolar_coupling_list',
                            'hvycs_restraint': '_CA_CB_constraint_list',
                            'procs_restraint': '_H_chem_shift_constraint_list',
                            'csp_restraint': '_Chem_shift_perturbation_list',
                            'auto_relax_restraint': '_Auto_relaxation_list',
                            'heteronucl_noe_data': '_Heteronucl_NOE_list',
                            'heteronucl_t1_data': '_Heteronucl_T1_list',
                            'heteronucl_t2_data': '_Heteronucl_T2_list',
                            'heteronucl_t1r_data': '_Heteronucl_T1rho_list',
                            'order_param_data': '_Order_parameter_list',
                            'ccr_d_csa_restraint': '_Cross_correlation_D_CSA_list',
                            'ccr_dd_restraint': '_Cross_correlation_DD_list',
                            'fchiral_restraint': '_Floating_chirality_assign',
                            'saxs_restraint': '_SAXS_constraint_list',
                            'other_restraint': '_Other_data_type_list'
                            }

NMR_STAR_SF_CATEGORIES = {'dist_restraint': 'general_distance_constraints',
                          'dihed_restraint': 'torsion_angle_constraints',
                          'rdc_restraint': 'RDC_constraints',
                          'noepk_restraint': 'homonucl_NOEs',
                          'jcoup_restraint': 'J_three_bond_constraints',
                          'rdc_raw_data': 'RDCs',
                          'csa_restraint': 'chem_shift_anisotropy',
                          'ddc_restraint': 'dipolar_couplings',
                          'hvycs_restraint': 'CA_CB_chem_shift_constraints',
                          'procs_restraint': 'H_chem_shift_constraints',
                          'csp_restraint': 'chem_shift_perturbation',
                          'auto_relax_restraint': 'auto_relaxation',
                          'heteronucl_noe_data': 'heteronucl_NOEs',
                          'heteronucl_t1_data': 'heteronucl_T1_relaxation',
                          'heteronucl_t2_data': 'heteronucl_T2_relaxation',
                          'heteronucl_t1r_data': 'heteronucl_T1rho_relaxation',
                          'order_param_data': 'order_parameters',
                          'ccr_d_csa_restraint': 'dipole_CSA_cross_correlations',
                          'ccr_dd_restraint': 'dipole_dipole_cross_correlations',
                          'fchiral_restraint': 'floating_chiral_stereo_assign',
                          'saxs_restraint': 'saxs_constraints',
                          'other_restraint': 'other_data_types'
                          }

NMR_STAR_SF_TAG_ITEMS = {'dist_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                            {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                            {'name': 'Constraint_type', 'type': 'enum', 'mandatory': False,
                                             'enum': ('NOE', 'NOE build-up', 'NOE not seen', 'ROE', 'ROE build-up',
                                                      'hydrogen bond', 'disulfide bond', 'paramagnetic relaxation',
                                                      'symmetry', 'general distance', 'mutation', 'chemical shift perturbation',
                                                      'undefined', 'unknown')},
                                            {'name': 'Potential_type', 'type': 'enum', 'mandatory': False,
                                             'enum': ('log-harmonic', 'parabolic', 'square-well-parabolic',
                                                      'square-well-parabolic-linear', 'upper-bound-parabolic',
                                                      'lower-bound-parabolic', 'upper-bound-parabolic-linear',
                                                      'lower-bound-parabolic-linear', 'undefined', 'unknown')},
                                            {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                            {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                            {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                            ],
                         'dihed_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                             {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                             {'name': 'Constraint_type', 'type': 'enum', 'mandatory': False,
                                              'enum': ('J-couplings', 'backbone chemical shifts', 'undefined', 'unknown')},
                                             {'name': 'Potential_type', 'type': 'enum', 'mandatory': False,
                                              'enum': ('parabolic', 'square-well-parabolic', 'square-well-parabolic-linear',
                                                       'upper-bound-parabolic', 'lower-bound-parabolic', 'upper-bound-parabolic-linear',
                                                       'lower-bound-parabolic-linear', 'undefined', 'unknown')},
                                             {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                             {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                             {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                             ],
                         'rdc_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                           {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                           {'name': 'Constraint_type', 'type': 'enum', 'mandatory': False,
                                            'enum': ('RDC', 'undefined', 'unknown')},
                                           {'name': 'Potential_type', 'type': 'enum', 'mandatory': False,
                                            'enum': ('parabolic', 'square-well-parabolic', 'square-well-parabolic-linear',
                                                     'upper-bound-parabolic', 'lower-bound-parabolic', 'upper-bound-parabolic-linear',
                                                     'lower-bound-parabolic-linear', 'undefined', 'unknown')},
                                           {'name': 'Tensor_magnitude', 'type': 'float', 'mandatory': False},
                                           {'name': 'Tensor_rhombicity', 'type': 'positive-float', 'mandatory': False},
                                           {'name': 'Tensor_auth_asym_ID', 'type': 'str', 'mandatory': False},
                                           {'name': 'Tensor_auth_seq_ID', 'type': 'str', 'mandatory': False},
                                           {'name': 'Tensor_auth_comp_ID', 'type': 'str', 'mandatory': False},
                                           {'name': 'Details', 'type': 'str', 'mandatory': False},
                                           {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                           {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                           {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                           ],
                         'noepk_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                             {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                             {'name': 'Homonuclear_NOE_val_type', 'type': 'enum', 'mandatory': True,
                                              'enum': ('peak volume', 'peak height', 'contour count', 'na')},
                                             {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                             {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                             {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                             ],
                         'jcoup_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                             {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                             {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                             {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                             {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                             ],
                         'rdc_raw_data': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                          {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                          {'name': 'Spectrometer_frequency_1H', 'type': 'positive-float', 'mandatory': False,
                                           'enforce-non-zero': True},
                                          {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                          {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                          {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                          ],
                         'csa_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                           {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                           {'name': 'Spectrometer_frequency_1H', 'type': 'positive-float', 'mandatory': False,
                                            'enforce-non-zero': True},
                                           {'name': 'Val_units', 'type': 'enum', 'mandatory': False,
                                            'enum': ('ppm', 'ppb')},
                                           {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                           {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                           {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                           ],
                         'ddc_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                           {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                           {'name': 'Spectrometer_frequency_1H', 'type': 'positive-float', 'mandatory': False,
                                            'enforce-non-zero': True},
                                           {'name': 'Scaling_factor', 'type': 'positive-float', 'mandatory': False},
                                           {'name': 'Fitting_procedure', 'type': 'str', 'mandatory': False},
                                           {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                           {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                           {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                           ],
                         'hvycs_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                             {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                             {'name': 'Units', 'type': 'str', 'mandatory': False},
                                             {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                             {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                             {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                             ],
                         'procs_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                             {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                             {'name': 'Units', 'type': 'str', 'mandatory': False},
                                             {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                             {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                             {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                             ],
                         'csp_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                           {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                           {'name': 'Type', 'type': 'enum', 'mandatory': False,
                                            'enum': ('macromolecular binding', 'ligand binding', 'ligand fragment binding', 'paramagnetic ligand binding')},
                                           {'name': 'Details', 'type': 'str', 'mandatory': False},
                                           {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                           {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                           {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                           ],
                         'auto_relax_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                                  {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                                  {'name': 'Temp_calibration_method', 'type': 'enum', 'mandatory': False,
                                                   'enum': ('methanol', 'monoethylene glycol', 'no calibration applied')},
                                                  {'name': 'Temp_control_method', 'type': 'enum', 'mandatory': False,
                                                   'enum': ('single scan interleaving', 'temperature compensation block',
                                                            'single scan interleaving and temperature compensation block',
                                                            'no temperature control applied')},
                                                  {'name': 'Spectrometer_frequency_1H', 'type': 'positive-float', 'mandatory': False,
                                                   'enforce-non-zero': True},
                                                  {'name': 'Exact_field_strength', 'type': 'positive-float', 'mandatory': False,
                                                   'enforce-non-zero': True},
                                                  {'name': 'Common_relaxation_type_name', 'type': 'enum', 'mandatory': False,
                                                   'enum': ('R1', 'R2', 'R1rho', 'ZQ relaxation', 'longitudinal spin order',
                                                            'single quantum antiphase', 'DQ relaxation')},
                                                  {'name': 'Relaxation_coherence_type', 'type': 'enum', 'mandatory': True,
                                                   'enum': ('Iz', 'Sz', '(I+)+(I-)', '(S+)+(S-)', 'I+', 'I-', 'S+', 'S-',
                                                            '(I+S-)+(I-S+)', 'I-S+', 'I+S-', 'IzSz', '((I+)+(I-))Sz', 'Iz((S+)+(S-))',
                                                            'I+Sz', 'I-Sz', 'IzS+', 'IzS-', '(I+S+)+(I-S-)', 'I+S+', 'I-S-')},
                                                  {'name': 'Relaxation_val_units', 'type': 'enum', 'mandatory': True,
                                                   'enum': ('s-1', 'ms-1', 'us-1', 'ns-1', 'ps-1')},
                                                  {'name': 'Rex_units', 'type': 'enum', 'mandatory': False,
                                                   'enum': ('s-1', 'ms-1', 'us-1')},
                                                  {'name': 'Rex_field_strength', 'type': 'positive-float', 'mandatory': False,
                                                   'enforce-non-zero': True},
                                                  {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                                  {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                                  {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                  ],
                         'heteronucl_noe_data': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                                 {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                                 {'name': 'Spectrometer_frequency_1H', 'type': 'positive-float', 'mandatory': False,
                                                  'enforce-non-zero': True},
                                                 {'name': 'Heteronuclear_NOE_val_type', 'type': 'enum', 'mandatory': True,
                                                  'enum': ('peak height', 'peak integral', 'contour count', 'relative intensities', 'na')},
                                                 {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                                 {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                                 {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                 ],
                         'heteronucl_t1_data': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                                {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                                {'name': 'Spectrometer_frequency_1H', 'type': 'positive-float', 'mandatory': False,
                                                 'enforce-non-zero': True},
                                                {'name': 'T1_coherence_type', 'type': 'enum', 'mandatory': True,
                                                 'enum': ('Iz', 'Sz', 'na')},
                                                {'name': 'T1_val_units', 'type': 'enum', 'mandatory': True,
                                                 'enum': ('s', 's-1', 'ms', 'ms-1')},
                                                {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                                {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                                {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                ],
                         'heteronucl_t2_data': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                                {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                                {'name': 'Temp_calibration_method', 'type': 'enum', 'mandatory': False,
                                                 'enum': ('methanol', 'monoethylene glycol', 'no calibration applied')},
                                                {'name': 'Temp_control_method', 'type': 'enum', 'mandatory': False,
                                                 'enum': ('single scan interleaving', 'temperature compensation block',
                                                          'single scan interleaving and temperature compensation block',
                                                          'no temperature control applied')},
                                                {'name': 'Spectrometer_frequency_1H', 'type': 'positive-float', 'mandatory': False,
                                                 'enforce-non-zero': True},
                                                {'name': 'T2_coherence_type', 'type': 'enum', 'mandatory': True,
                                                 'enum': ('I(+,-)', 'S(+,-)', 'na')},
                                                {'name': 'T2_val_units', 'type': 'enum', 'mandatory': True,
                                                 'enum': ('s', 's-1', 'ms', 'ms-1')},
                                                {'name': 'Rex_units', 'type': 'enum', 'mandatory': False,
                                                 'enum': ('s-1', 'ms-1', 'us-1')},
                                                {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                                {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                                {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                ],
                         'heteronucl_t1r_data': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                                 {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                                 {'name': 'Temp_calibration_method', 'type': 'enum', 'mandatory': False,
                                                  'enum': ('methanol', 'monoethylene glycol', 'no calibration applied')},
                                                 {'name': 'Temp_control_method', 'type': 'enum', 'mandatory': False,
                                                  'enum': ('single scan interleaving', 'temperature compensation block',
                                                           'single scan interleaving and temperature compensation block',
                                                           'no temperature control applied')},
                                                 {'name': 'Spectrometer_frequency_1H', 'type': 'positive-float', 'mandatory': False,
                                                  'enforce-non-zero': True},
                                                 {'name': 'T1rho_coherence_type', 'type': 'enum', 'mandatory': True,
                                                  'enum': ('I(+,-)', 'S(+,-)', 'na')},
                                                 {'name': 'T1rho_val_units', 'type': 'enum', 'mandatory': True,
                                                  'enum': ('s', 's-1', 'ms', 'ms-1')},
                                                 {'name': 'Rex_units', 'type': 'enum', 'mandatory': False,
                                                  'enum': ('s-1', 'ms-1', 'us-1')},
                                                 {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                                 {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                                 {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                 ],
                         'order_param_data': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                              {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                              {'name': 'Tau_e_val_units', 'type': 'enum', 'mandatory': False,
                                               'enum': ('s', 'ms', 'us', 'ns', 'ps')},
                                              {'name': 'Tau_f_val_units', 'type': 'enum', 'mandatory': False,
                                               'enum': ('s', 'ms', 'us', 'ns', 'ps')},
                                              {'name': 'Tau_s_val_units', 'type': 'enum', 'mandatory': False,
                                               'enum': ('s', 'ms', 'us', 'ns', 'ps')},
                                              {'name': 'Rex_val_units', 'type': 'enum', 'mandatory': False,
                                               'enum': ('s-1', 'ms-1', 'us-1')},
                                              {'name': 'Rex_field_strength', 'type': 'positive-float', 'mandatory': False,
                                               'enforce-non-zero': True},
                                              {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                              {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                              {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                              ],
                         'ccr_d_csa_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                                 {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                                 {'name': 'Spectrometer_frequency_1H', 'type': 'positive-float', 'mandatory': False,
                                                  'enforce-non-zero': True},
                                                 {'name': 'Val_units', 'type': 'enum', 'mandatory': True,
                                                  'enum': ('s-1', 'ms-1', 'us-1')},
                                                 {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                                 {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                                 {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                 ],
                         'ccr_dd_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                              {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                              {'name': 'Spectrometer_frequency_1H', 'type': 'positive-float', 'mandatory': False,
                                               'enforce-non-zero': True},
                                              {'name': 'Val_units', 'type': 'enum', 'mandatory': True,
                                               'enum': ('s-1', 'ms-1', 'us-1')},
                                              {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                              {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                              {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                              ],
                         'fchiral_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                               {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                               {'name': 'Stereo_count', 'type': 'int', 'mandatory': False},
                                               {'name': 'Stereo_assigned_count', 'type': 'int', 'mandatory': True},
                                               {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                               {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                               {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                               ],
                         'saxs_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                            {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                            {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                            {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                            {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                            ],
                         'other_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                             {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                             {'name': 'Definition', 'type': 'str', 'mandatory': True},
                                             {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                             {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                             {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                             ]
                         }

NMR_STAR_LP_CATEGORIES = {'dist_restraint': '_Gen_dist_constraint',
                          'dihed_restraint': '_Torsion_angle_constraint',
                          'rdc_restraint': '_RDC_constraint',
                          'noepk_restraint': '_Homonucl_NOE',
                          'jcoup_restraint': '_J_three_bond_constraint',
                          'rdc_raw_data': '_RDC',
                          'csa_restraint': '_CS_anisotropy',
                          'ddc_restraint': '_Dipolar_coupling',
                          'hvycs_restraint': '_CA_CB_constraint',
                          'procs_restraint': '_H_chem_shift_constraint',
                          'csp_restraint': '_Chem_shift_perturbation',
                          'auto_relax_restraint': '_Auto_relaxation',
                          'heteronucl_noe_data': '_Heteronucl_NOE',
                          'heteronucl_t1_data': '_T1',
                          'heteronucl_t2_data': '_T2',
                          'heteronucl_t1r_data': '_T1rho',
                          'order_param_data': '_Order_param',
                          'ccr_d_csa_restraint': '_Cross_correlation_D_CSA',
                          'ccr_dd_restraint': '_Cross_correlation_DD',
                          'fchiral_restraint': '_Floating_chirality',
                          'saxs_restraint': '_SAXS_constraint',
                          'other_restraint': '_Other_data'
                          }

NMR_STAR_LP_KEY_ITEMS = {'dist_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                            {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_1'},
                                            {'name': 'Entity_ID_1', 'type': 'positive-int'},
                                            {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                            {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                            {'name': 'Atom_ID_1', 'type': 'str'},
                                            {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_2'},
                                            {'name': 'Entity_ID_2', 'type': 'positive-int'},
                                            {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                            {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                            {'name': 'Atom_ID_2', 'type': 'str'}
                                            ],
                         'dihed_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                             {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_1'},
                                             {'name': 'Entity_ID_1', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                             {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_1', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_2'},
                                             {'name': 'Entity_ID_2', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                             {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_2', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_3', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_3'},
                                             {'name': 'Entity_ID_3', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID_3', 'type': 'int', 'default-from': 'Seq_ID_3'},
                                             {'name': 'Comp_ID_3', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_3', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_4', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_4'},
                                             {'name': 'Entity_ID_4', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID_4', 'type': 'int', 'default-from': 'Seq_ID_4'},
                                             {'name': 'Comp_ID_4', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_4', 'type': 'str'}
                                             ],
                         'rdc_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                           {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_1'},
                                           {'name': 'Entity_ID_1', 'type': 'positive-int'},
                                           {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                           {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                           {'name': 'Atom_ID_1', 'type': 'str'},
                                           {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_2'},
                                           {'name': 'Entity_ID_2', 'type': 'positive-int'},
                                           {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                           {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                           {'name': 'Atom_ID_2', 'type': 'str'}
                                           ],
                         'noepk_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                             {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1'},
                                             {'name': 'Entity_ID_1', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                             {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_1', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1'},
                                             {'name': 'Entity_ID_2', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                             {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_2', 'type': 'str'}
                                             ],
                         'jcoup_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                             {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_1'},
                                             {'name': 'Entity_ID_1', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                             {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_1', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_2'},
                                             {'name': 'Entity_ID_2', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                             {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_2', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_3', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_3'},
                                             {'name': 'Entity_ID_3', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID_3', 'type': 'int', 'default-from': 'Seq_ID_3'},
                                             {'name': 'Comp_ID_3', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_3', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_4', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_4'},
                                             {'name': 'Entity_ID_4', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID_4', 'type': 'int', 'default-from': 'Seq_ID_4'},
                                             {'name': 'Comp_ID_4', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_4', 'type': 'str'}
                                             ],
                         'rdc_raw_data': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                          {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1'},
                                          {'name': 'Entity_ID_1', 'type': 'positive-int'},
                                          {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                          {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                          {'name': 'Atom_ID_1', 'type': 'str'},
                                          {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1'},
                                          {'name': 'Entity_ID_2', 'type': 'positive-int'},
                                          {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                          {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                          {'name': 'Atom_ID_2', 'type': 'str'}
                                          ],
                         'csa_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                           {'name': 'Entity_assembly_ID', 'type': 'positive-int-as-str', 'default': '1'},
                                           {'name': 'Entity_ID', 'type': 'positive-int'},
                                           {'name': 'Comp_index_ID', 'type': 'int', 'default-from': 'Seq_ID'},
                                           {'name': 'Comp_ID', 'type': 'str', 'uppercase': True},
                                           {'name': 'Atom_ID', 'type': 'str'}
                                           ],
                         'ddc_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                           {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1'},
                                           {'name': 'Entity_ID_1', 'type': 'positive-int'},
                                           {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                           {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                           {'name': 'Atom_ID_1', 'type': 'str'},
                                           {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1'},
                                           {'name': 'Entity_ID_2', 'type': 'positive-int'},
                                           {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                           {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                           {'name': 'Atom_ID_2', 'type': 'str'}
                                           ],
                         'hvycs_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                             {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_1'},
                                             {'name': 'Entity_ID_1', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                             {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_1', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_2'},
                                             {'name': 'Entity_ID_2', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                             {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_2', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_3', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_3'},
                                             {'name': 'Entity_ID_3', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID_3', 'type': 'int', 'default-from': 'Seq_ID_3'},
                                             {'name': 'Comp_ID_3', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_3', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_4', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_4'},
                                             {'name': 'Entity_ID_4', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID_4', 'type': 'int', 'default-from': 'Seq_ID_4'},
                                             {'name': 'Comp_ID_4', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_4', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_5', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_5'},
                                             {'name': 'Entity_ID_5', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID_5', 'type': 'int', 'default-from': 'Seq_ID_5'},
                                             {'name': 'Comp_ID_5', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_5', 'type': 'str'}
                                             ],
                         'procs_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                             {'name': 'Entity_assembly_ID', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID'},
                                             {'name': 'Entity_ID', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID', 'type': 'int', 'default-from': 'Seq_ID'},
                                             {'name': 'Comp_ID', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID', 'type': 'str'}
                                             ],
                         'csp_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                           {'name': 'Entity_assembly_ID', 'type': 'positive-int-as-str', 'default': '1'},
                                           {'name': 'Entity_ID', 'type': 'positive-int'},
                                           {'name': 'Comp_index_ID', 'type': 'int', 'default-from': 'Seq_ID'},
                                           {'name': 'Comp_ID', 'type': 'str', 'uppercase': True},
                                           {'name': 'Atom_ID', 'type': 'str'}
                                           ],
                         'auto_relax_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                                  {'name': 'Entity_assembly_ID', 'type': 'positive-int-as-str', 'default': '1'},
                                                  {'name': 'Entity_ID', 'type': 'positive-int'},
                                                  {'name': 'Comp_index_ID', 'type': 'int', 'default-from': 'Seq_ID'},
                                                  {'name': 'Comp_ID', 'type': 'str', 'uppercase': True},
                                                  {'name': 'Atom_ID', 'type': 'str'}
                                                  ],
                         'heteronucl_noe_data': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                                 {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_1'},
                                                 {'name': 'Entity_ID_1', 'type': 'positive-int'},
                                                 {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                                 {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                                 {'name': 'Atom_ID_1', 'type': 'str'},
                                                 {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_2'},
                                                 {'name': 'Entity_ID_2', 'type': 'positive-int'},
                                                 {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                                 {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                                 {'name': 'Atom_ID_2', 'type': 'str'}
                                                 ],
                         'heteronucl_t1_data': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                                {'name': 'Entity_assembly_ID', 'type': 'positive-int-as-str', 'default': '1'},
                                                {'name': 'Entity_ID', 'type': 'positive-int'},
                                                {'name': 'Comp_index_ID', 'type': 'int', 'default-from': 'Seq_ID'},
                                                {'name': 'Comp_ID', 'type': 'str', 'uppercase': True},
                                                {'name': 'Atom_ID', 'type': 'str'}
                                                ],
                         'heteronucl_t2_data': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                                {'name': 'Entity_assembly_ID', 'type': 'positive-int-as-str', 'default': '1'},
                                                {'name': 'Entity_ID', 'type': 'positive-int'},
                                                {'name': 'Comp_index_ID', 'type': 'int', 'default-from': 'Seq_ID'},
                                                {'name': 'Comp_ID', 'type': 'str', 'uppercase': True},
                                                {'name': 'Atom_ID', 'type': 'str'}
                                                ],
                         'heteronucl_t1r_data': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                                 {'name': 'Entity_assembly_ID', 'type': 'positive-int-as-str', 'default': '1'},
                                                 {'name': 'Entity_ID', 'type': 'positive-int'},
                                                 {'name': 'Comp_index_ID', 'type': 'int', 'default-from': 'Seq_ID'},
                                                 {'name': 'Comp_ID', 'type': 'str', 'uppercase': True},
                                                 {'name': 'Atom_ID', 'type': 'str'}
                                                 ],
                         'order_param_data': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                              {'name': 'Entity_assembly_ID', 'type': 'positive-int-as-str', 'default': '1'},
                                              {'name': 'Entity_ID', 'type': 'positive-int'},
                                              {'name': 'Comp_index_ID', 'type': 'int', 'default-from': 'Seq_ID'},
                                              {'name': 'Comp_ID', 'type': 'str', 'uppercase': True},
                                              {'name': 'Atom_ID', 'type': 'str'}
                                              ],
                         'ccr_d_csa_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                                 {'name': 'Dipole_entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1'},
                                                 {'name': 'Dipole_entity_ID_1', 'type': 'positive-int'},
                                                 {'name': 'Dipole_comp_index_ID_1', 'type': 'int', 'default-from': 'Dipole_seq_ID_1'},
                                                 {'name': 'Dipole_comp_ID_1', 'type': 'str', 'uppercase': True},
                                                 {'name': 'Dipole_atom_ID_1', 'type': 'str'},
                                                 {'name': 'Dipole_entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1'},
                                                 {'name': 'Dipole_entity_ID_2', 'type': 'positive-int'},
                                                 {'name': 'Dipole_comp_index_ID_2', 'type': 'int', 'default-from': 'Dipole_seq_ID_2'},
                                                 {'name': 'Dipole_comp_ID_2', 'type': 'str', 'uppercase': True},
                                                 {'name': 'Dipole_atom_ID_2', 'type': 'str'},
                                                 {'name': 'CSA_entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1'},
                                                 {'name': 'CSA_entity_ID_1', 'type': 'positive-int'},
                                                 {'name': 'CSA_comp_index_ID_1', 'type': 'int', 'default-from': 'CSA_seq_ID_1'},
                                                 {'name': 'CSA_comp_ID_1', 'type': 'str', 'uppercase': True},
                                                 {'name': 'CSA_atom_ID_1', 'type': 'str'},
                                                 {'name': 'CSA_entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1'},
                                                 {'name': 'CSA_entity_ID_2', 'type': 'positive-int'},
                                                 {'name': 'CSA_comp_index_ID_2', 'type': 'int', 'default-from': 'CSA_seq_ID_2'},
                                                 {'name': 'CSA_comp_ID_2', 'type': 'str', 'uppercase': True},
                                                 {'name': 'CSA_atom_ID_2', 'type': 'str'}
                                                 ],
                         'ccr_dd_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                              {'name': 'Dipole_1_entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1'},
                                              {'name': 'Dipole_1 entity_ID_1', 'type': 'positive-int'},
                                              {'name': 'Dipole_1_comp_index_ID_1', 'type': 'int', 'default-from': 'Dipole_1_seq_ID_1'},
                                              {'name': 'Dipole_1_comp_ID_1', 'type': 'str', 'uppercase': True},
                                              {'name': 'Dipole_1_atom_ID_1', 'type': 'str'},
                                              {'name': 'Dipole_1_entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1'},
                                              {'name': 'Dipole_1_entity_ID_2', 'type': 'positive-int'},
                                              {'name': 'Dipole_1_comp_index_ID_2', 'type': 'int', 'default-from': 'Dipole_1_seq_ID_2'},
                                              {'name': 'Dipole_1_comp_ID_2', 'type': 'str', 'uppercase': True},
                                              {'name': 'Dipole_1_atom_ID_2', 'type': 'str'},
                                              {'name': 'Dipole_2_entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1'},
                                              {'name': 'Dipole_2_entity_ID_1', 'type': 'positive-int'},
                                              {'name': 'Dipole_2_comp_index_ID_1', 'type': 'int', 'default-from': 'Dipole_2_seq_ID_1'},
                                              {'name': 'Dipole_2_comp_ID_1', 'type': 'str', 'uppercase': True},
                                              {'name': 'Dipole_2_atom_ID_1', 'type': 'str'},
                                              {'name': 'Dipole_2_entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1'},
                                              {'name': 'Dipole_2_entity_ID_2', 'type': 'positive-int'},
                                              # 'Dipole_2_comp_index_ID_2' is inferred from NMR-STAR Dictionary
                                              {'name': 'Dipole_2_comp_index_ID_2', 'type': 'int', 'default-from': 'Dipole_2_seq_ID_2'},
                                              {'name': 'Dipole_2_comp_ID_2', 'type': 'str', 'uppercase': True},
                                              {'name': 'Dipole_2_atom_ID_2', 'type': 'str'}
                                              ],
                         'fchiral_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                               {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_1'},
                                               {'name': 'Entity_ID_1', 'type': 'positive-int'},
                                               {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                               {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                               {'name': 'Atom_ID_1', 'type': 'str'},
                                               {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_2'},
                                               {'name': 'Entity_ID_2', 'type': 'positive-int'},
                                               {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                               {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                               {'name': 'Atom_ID_2', 'type': 'str'}
                                               ],
                         'saxs_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                            {'name': 'Q_value', 'type': 'positive-float'}
                                            ],
                         'other_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                             {'name': 'Entity_assembly_ID', 'type': 'positive-int-as-str', 'default': '1'},
                                             {'name': 'Entity_ID', 'type': 'positive-int'},
                                             {'name': 'Comp_index_ID', 'type': 'int', 'default-from': 'Seq_ID'},
                                             {'name': 'Comp_ID', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID', 'type': 'str'}
                                             ]
                         }

NMR_STAR_LP_DATA_ITEMS = {'dist_restraint': [{'name': 'Index_ID', 'type': 'index-int', 'mandatory': False},
                                             {'name': 'Combination_ID', 'type': 'positive-int', 'mandatory': False,
                                              'enforce-non-zero': True},
                                             {'name': 'Member_ID', 'type': 'positive-int', 'mandatory': False,
                                              'enforce-non-zero': True},
                                             {'name': 'Member_logic_code', 'type': 'enum', 'mandatory': False,
                                              'enum': ('OR', 'AND'),
                                              'enforce-enum': True},
                                             {'name': 'Target_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True, 'void-zero': True,
                                              'range': DIST_RESTRAINT_RANGE,
                                              'group': {'member-with': ['Lower_linear_limit',
                                                                        'Upper_linear_limit',
                                                                        'Distance_lower_bound_val',
                                                                        'Distance_upper_bound_val'],
                                                        'coexist-with': None,
                                                        'smaller-than': ['Lower_linear_limit', 'Distance_lower_bound_val'],
                                                        'larger-than': ['Distance_upper_bound_val', 'Upper_linear_limit']}},
                                             {'name': 'Target_val_uncertainty', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                              'range': DIST_UNCERTAINTY_RANGE},
                                             {'name': 'Lower_linear_limit', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True, 'void-zero': True,
                                              'range': DIST_RESTRAINT_RANGE,
                                              'group': {'member-with': ['Target_val',
                                                                        'Upper_linear_limit',
                                                                        'Distance_lower_bound_val',
                                                                        'Distance_upper_bound_val'],
                                                        'coexist-with': None,  # ['Upper_linear_limit', 'Distance_lower_bound_val', 'Distance_upper_bound_val'],
                                                        'smaller-than': None,
                                                        'larger-than': ['Distance_lower_bound_val', 'Distance_upper_bound_val', 'Upper_linear_limit']}},
                                             {'name': 'Distance_lower_bound_val', 'type': 'range-float', 'mandatory': False,
                                              'group-mandatory': True, 'void-zero': True,
                                              'range': DIST_RESTRAINT_RANGE,
                                              'group': {'member-with': ['Target_val', 'Lower_linear_limit', 'Upper_linear_limit', 'Distance_upper_bound_val'],
                                                        'coexist-with': None,  # ['Distance_upper_bound_val'],
                                                        'smaller-than': ['Lower_linear_limit'],
                                                        'larger-than': ['Distance_upper_bound_val', 'Upper_linear_limit']}},
                                             {'name': 'Distance_upper_bound_val', 'type': 'range-float', 'mandatory': False,
                                              'group-mandatory': True, 'void-zero': True,
                                              'range': DIST_RESTRAINT_RANGE,
                                              'group': {'member-with': ['Target_val', 'Lower_linear_limit', 'Upper_linear_limit', 'Distance_lower_bound_val'],
                                                        'coexist-with': None,  # ['Distance_lower_bound_val'],
                                                        'smaller-than': ['Lower_linear_limit', 'Distance_lower_bound_val'],
                                                        'larger-than': ['Upper_linear_limit']}},
                                             {'name': 'Upper_linear_limit', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True, 'void-zero': True,
                                              'range': DIST_RESTRAINT_RANGE,
                                              'group': {'member-with': ['Target_val',
                                                                        'Lower_linear_limit',
                                                                        'Distance_lower_bound_val',
                                                                        'Distance_upper_bound_val'],
                                                        'coexist-with': None,  # ['Lower_linear_limit', 'Distance_lower_bound_val', 'Distance_upper_bound_val'],
                                                        'smaller-than': ['Lower_linear_limit', 'Distance_lower_bound_val', 'Distance_upper_bound_val'],
                                                        'larger-than': None}},
                                             {'name': 'Weight', 'type': 'range-float', 'mandatory': False,
                                              'range': WEIGHT_RANGE},
                                             # 'enforce-non-zero': True},
                                             {'name': 'Distance_val', 'type': 'range-float', 'mandatory': False,
                                                      'range': DIST_RESTRAINT_RANGE},
                                             {'name': 'Auth_asym_ID_1', 'type': 'str', 'mandatory': False},
                                             {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                             {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                             {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                             {'name': 'Auth_atom_name_1', 'type': 'str', 'mandatory': False},
                                             {'name': 'Auth_asym_ID_2', 'type': 'str', 'mandatory': False},
                                             {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                             {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                             {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                             {'name': 'Auth_atom_name_2', 'type': 'str', 'mandatory': False},
                                             {'name': 'Gen_dist_constraint_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                              'default': '1', 'default-from': 'parent'},
                                             {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                             ],
                          'dihed_restraint': [{'name': 'Index_ID', 'type': 'index-int', 'mandatory': False},
                                              {'name': 'Combination_ID', 'type': 'positive-int', 'mandatory': False,
                                               'enforce-non-zero': True},
                                              {'name': 'Torsion_angle_name', 'type': 'str', 'mandatory': False},
                                              {'name': 'Angle_target_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                               'range': ANGLE_RESTRAINT_RANGE,
                                               'group': {'member-with': ['Angle_lower_linear_limit',
                                                                         'Angle_upper_linear_limit',
                                                                         'Angle_lower_bound_val',
                                                                         'Angle_upper_bound_val'],
                                                         'coexist-with': None,
                                                         'smaller-than': None,  # (DAOTHER-8442) ['Angle_lower_linear_limit', 'Angle_lower_bound_val'],
                                                         'larger-than': None,  # (DAOTHER-8442) ['Angle_upper_bound_val', 'Angle_upper_linear_limit'],
                                                         'circular-shift': 360.0}},
                                              {'name': 'Angle_target_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                               'range': ANGLE_UNCERTAINTY_RANGE},
                                              {'name': 'Angle_lower_linear_limit', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                               'range': ANGLE_RESTRAINT_RANGE,
                                               'group': {'member-with': ['Angle_target_val', 'Angle_upper_linear_limit',
                                                                         'Angle_lower_bound_val', 'Angle_upper_bound_val'],
                                                         'coexist-with': None,  # ['Angle_upper_linear_limit', 'Angle_lower_bound_val', 'Angle_upper_bound_val'],
                                                         'smaller-than': None,
                                                         'larger-than': ['Angle_lower_bound_val'],
                                                         # (DAOTHER-8442) ['Angle_lower_bound_val', 'Angle_upper_bound', 'Angle_upper_linear_limit'],
                                                         'circular-shift': 360.0}},
                                              {'name': 'Angle_lower_bound_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                               'range': ANGLE_RESTRAINT_RANGE,
                                               'group': {'member-with': ['Angle_target_val', 'Angle_lower_linear_limit',
                                                                         'Angle_upper_linear_limit', 'Angle_upper_bound_val'],
                                                         'coexist-with': None,  # ['Angle_upper_bound_val'],
                                                         'smaller-than': ['Angle_lower_linear_limit'],
                                                         'larger-than': None,  # (DAOTHER-8442) ['Angle_upper_bound_val', 'Angle_upper_linear_limit'],
                                                         'circular-shift': 360.0}},
                                              {'name': 'Angle_upper_bound_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                               'range': ANGLE_RESTRAINT_RANGE,
                                               'group': {'member-with': ['Angle_target_val', 'Angle_lower_linear_limit',
                                                                         'Angle_upper_linear_limit', 'Angle_lower_bound_val'],
                                                         'coexist-with': None,  # ['Angle_lower_bound_val'],
                                                         'smaller-than': None,  # (DAOTHER-8442) ['Angle_lower_bound_val', 'Angle_upper_linear_limit'],
                                                         'larger-than': ['Angle_upper_linear_limit'],
                                                         'circular-shift': 360.0}},
                                              {'name': 'Angle_upper_linear_limit', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                               'range': ANGLE_RESTRAINT_RANGE,
                                               'group': {'member-with': ['Angle_target_val', 'Angle_lower_linear_limit',
                                                                         'Angle_lower_bound_val', 'Angle_upper_bound_val'],
                                                         'coexist-with': None,  # ['Angle_lower_linear_limit', 'Angle_lower_bound_val', 'Angle_upper_bound_val'],
                                                         'smaller-than': ['Angle_upper_bound_val'],
                                                         # (DAOTHER-8442) ['Angle_lower_linear_limit', 'Angle_lower_bound_val', 'Angle_upper_bound_val'],
                                                         'larger-than': None,
                                                         'circular-shift': 360.0}},
                                              {'name': 'Weight', 'type': 'range-float', 'mandatory': False,
                                               'range': WEIGHT_RANGE},
                                              # 'enforce-non-zero': True},
                                              {'name': 'Auth_asym_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_name_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_name_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_3', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_name_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_4', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_name_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'Torsion_angle_constraint_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                               'default': '1', 'default-from': 'parent'},
                                              {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                              ],
                          'rdc_restraint': [{'name': 'Index_ID', 'type': 'index-int', 'mandatory': False},
                                            {'name': 'Combination_ID', 'type': 'positive-int', 'mandatory': False,
                                             'enforce-non-zero': True},
                                            {'name': 'Target_value', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                             'range': RDC_RESTRAINT_RANGE,
                                             'group': {'member-with': ['RDC_lower_linear_limit', 'RDC_upper_linear_limit', 'RDC_lower_bound', 'RDC_upper_bound'],
                                                       'coexist-with': None,
                                                       'smaller-than': ['RDC_lower_linear_limit', 'RDC_lower_bound'],
                                                       'larger-than': ['RDC_upper_bound', 'RDC_upper_linear_limit']}},
                                            {'name': 'Target_value_uncertainty', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                             'range': RDC_UNCERTAINTY_RANGE},
                                            {'name': 'RDC_lower_linear_limit', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                             'range': RDC_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Target_value', 'RDC_upper_linear_limit', 'RDC_lower_bound', 'RDC_upper_bound'],
                                                       'coexist-with': None,  # ['RDC_upper_linear_limit', 'RDC_lower_bound', 'RDC_upper_bound'],
                                                       'smaller-than': None,
                                                       'larger-than': ['RDC_lower_bound', 'RDC_upper_bound', 'RDC_upper_linear_limit']}},
                                            {'name': 'RDC_lower_bound', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                             'range': RDC_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Target_value', 'RDC_lower_linear_limit', 'RDC_upper_linear_limit', 'RDC_upper_bound'],
                                                       'coexist-with': None,  # ['RDC_upper_bound'],
                                                       'smaller-than': ['RDC_lower_linear_limit'],
                                                       'larger-than': ['RDC_upper_bound', 'RDC_upper_linear_limit']}},
                                            {'name': 'RDC_upper_bound', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                             'range': RDC_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Target_value', 'RDC_lower_linear_limit', 'RDC_upper_linear_limit', 'RDC_lower_bound'],
                                                       'coexist-with': None,  # ['RDC_lower_bound'],
                                                       'smaller-than': ['RDC_lower_linear_limit', 'RDC_lower_bound'],
                                                       'larger-than': ['RDC_upper_linear_limit']}},
                                            {'name': 'RDC_upper_linear_limit', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                             'range': RDC_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Target_value', 'RDC_upper_linear_limit', 'RDC_lower_bound', 'RDC_upper_bound'],
                                                       'coexist-with': None,  # ['RDC_upper_linear_limit', 'RDC_lower_bound', 'RDC_upper_bound'],
                                                       'smaller-than': ['RDC_lower_linear_limit', 'RDC_lower_bound', 'RDC_upper_bound'],
                                                       'larger-than': None}},
                                            {'name': 'Weight', 'type': 'range-float', 'mandatory': False,
                                             'range': WEIGHT_RANGE},
                                            # 'enforce-non-zero': True},
                                            {'name': 'RDC_val', 'type': 'range-float', 'mandatory': False,
                                             'range': RDC_RESTRAINT_RANGE},
                                            {'name': 'RDC_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                             'range': RDC_UNCERTAINTY_RANGE},
                                            {'name': 'RDC_val_scale_factor', 'type': 'range-float', 'mandatory': False,
                                             'range': SCALE_RANGE,
                                             'enforce-non-zero': True},
                                            {'name': 'RDC_distant_dependent', 'type': 'bool', 'mandatory': False},
                                            {'name': 'Auth_asym_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                            {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_name_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_asym_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                            {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_name_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'RDC_constraint_list_ID', 'type': 'pointer-index', 'mandatory': True, 'default': '1', 'default-from': 'parent'},
                                            {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                            ],
                          'noepk_restraint': [{'name': 'Val', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                               'group': {'member-with': ['Val_min', 'Val_max'],
                                                         'coexist-with': None,
                                                         'smaller-than': None,
                                                         'larger-than': None}},
                                              {'name': 'Val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                               'range': {'min_inclusive': 0.0}},
                                              {'name': 'Val_min', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                               'group': {'member-with': ['Val', 'Val_max'],
                                                         'coexist-with': None,
                                                         'smaller-than': None,
                                                         'larger-than': ['Val_max']}},
                                              {'name': 'Val_max', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                               'group': {'member-with': ['Val', 'Val_min'],
                                                         'coexist-with': None,
                                                         'smaller-than': ['Val_min'],
                                                         'larger-than': None}},
                                              {'name': 'Auth_entity_assembly_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_entity_assembly_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Homonucl_NOE_list_ID', 'type': 'pointer-index', 'mandatory': True, 'default': '1', 'default-from': 'parent'},
                                              {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                              ],
                          'jcoup_restraint': [{'name': 'Coupling_constant_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                               'range': RDC_RESTRAINT_RANGE,
                                               'group': {'member-with': ['Coupling_constant_lower_bound', 'Coupling_constant_upper_bound'],
                                                         'coexist-with': None,
                                                         'smaller-than': None,
                                                         'larger-than': None}},
                                              {'name': 'Coupling_constant_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                               'range': {'min_inclusive': 0.0}},
                                              {'name': 'Coupling_constant_lower_bound', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                               'range': RDC_RESTRAINT_RANGE,
                                               'group': {'member-with': ['Coupling_constant_upper_bound'],
                                                         'coexist-with': None,
                                                         'smaller-than': None,
                                                         'larger-than': ['Coupling_constant_upper_bound']}},
                                              {'name': 'Coupling_constant_upper_bound', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                               'range': RDC_RESTRAINT_RANGE,
                                               'group': {'member-with': ['Coupling_constant_lower_bound'],
                                                         'coexist-with': None,
                                                         'smaller-than': ['Coupling_constant_lower_bound'],
                                                         'larger-than': None}},
                                              {'name': 'Auth_asym_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_3', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_4', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'J_three_bond_constraint_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                               'default': '1', 'default-from': 'parent'},
                                              {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                              ],
                          'rdc_raw_data': [{'name': 'RDC_code', 'type': 'str', 'mandatory': True},
                                           {'name': 'Atom_type_1', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID_1',
                                            'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                            'enforce-enum': True},
                                           {'name': 'Atom_isotope_number_1', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID_1',
                                            'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                            'enforce-enum': True},
                                           {'name': 'Ambiguity_code_1', 'type': 'enum-int', 'mandatory': False,
                                            'enum': ALLOWED_AMBIGUITY_CODES,
                                            'enforce-enum': True},
                                           {'name': 'Atom_type_2', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID_2',
                                            'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                            'enforce-enum': True},
                                           {'name': 'Atom_isotope_number_2', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID_2',
                                            'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                            'enforce-enum': True},
                                           {'name': 'Ambiguity_code_2', 'type': 'enum-int', 'mandatory': False,
                                            'enum': ALLOWED_AMBIGUITY_CODES,
                                            'enforce-enum': True},
                                           {'name': 'Val', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                            'group': {'member-with': ['Val_min', 'Val_max'],
                                                      'coexist-with': None,
                                                      'smaller-than': None,
                                                      'larger-than': None}},
                                           {'name': 'Val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                            'range': {'min_inclusive': 0.0}},
                                           {'name': 'Val_min', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                            'group': {'member-with': ['Val', 'Val_max'],
                                                      'coexist-with': None,
                                                      'smaller-than': None,
                                                      'larger-than': ['Val_max']}},
                                           {'name': 'Val_max', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                            'group': {'member-with': ['Val', 'Val_min'],
                                                      'coexist-with': None,
                                                      'smaller-than': ['Val_min'],
                                                      'larger-than': None}},
                                           {'name': 'Val_bond_length', 'type': 'range-float', 'mandatory': False,
                                            'range': DIST_RESTRAINT_RANGE},
                                           {'name': 'Auth_entity_assembly_ID_1', 'type': 'str', 'mandatory': False},
                                           {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                           {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                           {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                           {'name': 'Auth_entity_assembly_ID_2', 'type': 'str', 'mandatory': False},
                                           {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                           {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                           {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                           {'name': 'RDC_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                            'default': '1', 'default-from': 'parent'},
                                           {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                           ],
                          'csa_restraint': [{'name': 'Atom_type', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID',
                                             'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                             'enforce-enum': True},
                                            {'name': 'Atom_isotope_number', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID',
                                             'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                             'enforce-enum': True},
                                            {'name': 'Val', 'type': 'range-float', 'mandatory': True,
                                             'range': CSA_RESTRAINT_RANGE},
                                            {'name': 'Val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                             'range': {'min_inclusive': 0.0}},
                                            {'name': 'Principal_value_sigma_11_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': CSA_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_value_sigma_22_val', 'Principal_value_sigma_33_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Principal_value_sigma_22_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': CSA_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_value_sigma_11_val', 'Principal_value_sigma_33_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Principal_value_sigma_33_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': CSA_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_value_sigma_11_val', 'Principal_value_sigma_22_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Principal_Euler_angle_alpha_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': ANGLE_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_Euler_angle_beta_val', 'Principal_Euler_angle_gamma_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Principal_Euler_angle_beta_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': ANGLE_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_Euler_angle_alpha_val', 'Principal_Euler_angle_gamma_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Principal_Euler_angle_gamma_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': ANGLE_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_Euler_angle_alpha_val', 'Principal_Euler_angle_beta_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Bond_length', 'type': 'range-float', 'mandatory': False,
                                             'range': DIST_RESTRAINT_RANGE},
                                            {'name': 'Auth_entity_assembly_ID', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_seq_ID', 'type': 'int', 'mandatory': False},
                                            {'name': 'Auth_comp_ID', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_ID', 'type': 'str', 'mandatory': False},
                                            {'name': 'Chem_shift_anisotropy_ID', 'type': 'pointer-index', 'mandatory': True,
                                             'default': '1', 'default-from': 'parent'},
                                            {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                            ],
                          'ddc_restraint': [{'name': 'Dipolar_coupling_code', 'type': 'str', 'mandatory': True},
                                            {'name': 'Atom_type_1', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID_1',
                                             'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                             'enforce-enum': True},
                                            {'name': 'Atom_isotope_number_1', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID_1',
                                             'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                             'enforce-enum': True},
                                            {'name': 'Ambiguity_code_1', 'type': 'enum-int', 'mandatory': False,
                                             'enum': ALLOWED_AMBIGUITY_CODES,
                                             'enforce-enum': True},
                                            {'name': 'Atom_type_2', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID_2',
                                             'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                             'enforce-enum': True},
                                            {'name': 'Atom_isotope_number_2', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID_2',
                                             'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                             'enforce-enum': True},
                                            {'name': 'Ambiguity_code_2', 'type': 'enum-int', 'mandatory': False,
                                             'enum': ALLOWED_AMBIGUITY_CODES,
                                             'enforce-enum': True},
                                            {'name': 'Val', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                             'group': {'member-with': ['Val_min', 'Val_max'],
                                                       'coexist-with': None,
                                                       'smaller-than': None,
                                                       'larger-than': None}},
                                            {'name': 'Val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                             'range': {'min_inclusive': 0.0}},
                                            {'name': 'Val_min', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                             'group': {'member-with': ['Val_max'],
                                                       'coexist-with': None,
                                                       'smaller-than': None,
                                                       'larger-than': ['Val_max']}},
                                            {'name': 'Val_max', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                             'group': {'member-with': ['Val_min'],
                                                       'coexist-with': None,
                                                       'smaller-than': ['Val_min'],
                                                       'larger-than': None}},
                                            {'name': 'Principal_Euler_angle_alpha_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': ANGLE_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_Euler_angle_beta_val', 'Principal_Euler_angle_gamma_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Principal_Euler_angle_beta_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': ANGLE_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_Euler_angle_alpha_val', 'Principal_Euler_angle_gamma_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Principal_Euler_angle_gamma_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': ANGLE_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_Euler_angle_alpha_val', 'Principal_Euler_angle_beta_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Auth_entity_assembly_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                            {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_entity_assembly_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                            {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_entity_assembly_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                            {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_entity_assembly_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                            {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Dipolar_coupling_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                             'default': '1', 'default-from': 'parent'},
                                            {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                            ],
                          'hvycs_restraint': [{'name': 'CA_chem_shift_val', 'type': 'range-float', 'mandatory': True,
                                               'range': CS_RESTRAINT_RANGE},
                                              {'name': 'CA_chem_shift_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                               'range': CS_UNCERTAINTY_RANGE},
                                              {'name': 'CB_chem_shift_val', 'type': 'range-float', 'mandatory': False,
                                               'range': CS_RESTRAINT_RANGE},
                                              {'name': 'CB_chem_shift_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                               'range': CS_UNCERTAINTY_RANGE},
                                              {'name': 'Auth_asym_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_3', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_4', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_5', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_5', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_5', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_5', 'type': 'str', 'mandatory': False},
                                              {'name': 'CA_CB_constraint_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                               'default': '1', 'default-from': 'parent'},
                                              {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                              ],
                          'procs_restraint': [{'name': 'Atom_type', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID',
                                               'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                               'enforce-enum': True},
                                              {'name': 'Atom_isotope_number', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID',
                                               'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                               'enforce-enum': True},
                                              {'name': 'Chem_shift_val', 'type': 'range-float', 'mandatory': True,
                                               'range': CS_RESTRAINT_RANGE},
                                              {'name': 'Chem_shift_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                               'range': CS_UNCERTAINTY_RANGE},
                                              {'name': 'Auth_asym_ID', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID', 'type': 'str', 'mandatory': False},
                                              {'name': 'H_chem_shift_constraint_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                               'default': '1', 'default-from': 'parent'},
                                              {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                              ],
                          'csp_restraint': [{'name': 'Atom_type', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID',
                                             'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                             'enforce-enum': True},
                                            {'name': 'Atom_isotope_number', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID',
                                             'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                             'enforce-enum': True},
                                            {'name': 'Chem_shift_val', 'type': 'range-float', 'mandatory': False,
                                             'range': CS_RESTRAINT_RANGE},
                                            {'name': 'Chem_shift_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                             'range': CS_UNCERTAINTY_RANGE},
                                            {'name': 'Difference_chem_shift_val', 'type': 'range-float', 'mandatory': False,
                                             'range': CS_RESTRAINT_RANGE},
                                            {'name': 'Difference_chem_shift_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                             'range': CS_UNCERTAINTY_RANGE},
                                            {'name': 'Auth_entity_assembly_ID', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_seq_ID', 'type': 'int', 'mandatory': False},
                                            {'name': 'Auth_comp_ID', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_ID', 'type': 'str', 'mandatory': False},
                                            {'name': 'Chem_shift_perturbation_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                             'default': '1', 'default-from': 'parent'},
                                            {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                            ],
                          'auto_relax_restraint': [{'name': 'Atom_type', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID',
                                                    'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                    'enforce-enum': True},
                                                   {'name': 'Atom_isotope_number', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID',
                                                    'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                    'enforce-enum': True},
                                                   {'name': 'Auto_relaxation_val', 'type': 'range-float', 'mandatory': True,
                                                    'range': PRE_RESTRAINT_RANGE},
                                                   {'name': 'Auto_relaxation_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                                    'range': PRE_RESTRAINT_RANGE},
                                                   {'name': 'Rex_val', 'type': 'range-float', 'mandatory': False,
                                                    'range': PRE_RESTRAINT_RANGE},
                                                   {'name': 'Rex_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                                    'range': PRE_RESTRAINT_RANGE},
                                                   {'name': 'Auth_entity_assembly_ID', 'type': 'str', 'mandatory': False},
                                                   {'name': 'Auth_seq_ID', 'type': 'int', 'mandatory': False},
                                                   {'name': 'Auth_comp_ID', 'type': 'str', 'mandatory': False},
                                                   {'name': 'Auth_atom_ID', 'type': 'str', 'mandatory': False},
                                                   {'name': 'Auto_relaxation_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                                    'default': '1', 'default-from': 'parent'},
                                                   {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                   ],
                          'heteronucl_noe_data': [{'name': 'Atom_type_1', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID_1',
                                                   'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                   'enforce-enum': True},
                                                  {'name': 'Atom_isotope_number_1', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID_1',
                                                   'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                   'enforce-enum': True},
                                                  {'name': 'Atom_type_2', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID_2',
                                                   'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                   'enforce-enum': True},
                                                  {'name': 'Atom_isotope_number_2', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID_2',
                                                   'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                   'enforce-enum': True},
                                                  {'name': 'Val', 'type': 'float', 'mandatory': True},
                                                  {'name': 'Val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                                   'range': {'min_inclusive': 0.0}},
                                                  {'name': 'Auth_entity_assembly_ID_1', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                                  {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Auth_entity_assembly_ID_2', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                                  {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Heteronucl_NOE_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                                   'default': '1', 'default-from': 'parent'},
                                                  {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                  ],
                          'heteronucl_t1_data': [{'name': 'Atom_type', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID',
                                                  'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                  'enforce-enum': True},
                                                 {'name': 'Atom_isotope_number', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID',
                                                  'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                  'enforce-enum': True},
                                                 {'name': 'Val', 'type': 'float', 'mandatory': True},
                                                 {'name': 'Val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                                  'range': {'min_inclusive': 0.0}},
                                                 {'name': 'Auth_entity_assembly_ID', 'type': 'str', 'mandatory': False},
                                                 {'name': 'Auth_seq_ID', 'type': 'int', 'mandatory': False},
                                                 {'name': 'Auth_comp_ID', 'type': 'str', 'mandatory': False},
                                                 {'name': 'Auth_atom_ID', 'type': 'str', 'mandatory': False},
                                                 {'name': 'Heteronucl_T1_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                                  'default': '1', 'default-from': 'parent'},
                                                 {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                 ],
                          'heteronucl_t2_data': [{'name': 'Atom_type', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID',
                                                  'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                  'enforce-enum': True},
                                                 {'name': 'Atom_isotope_number', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID',
                                                  'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                  'enforce-enum': True},
                                                 {'name': 'T2_val', 'type': 'float', 'mandatory': True},
                                                 {'name': 'T2_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                                  'range': {'min_inclusive': 0.0}},
                                                 {'name': 'Rex_val', 'type': 'float', 'mandatory': False},
                                                 {'name': 'Rex_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                                  'range': {'min_inclusive': 0.0}},
                                                 {'name': 'Auth_entity_assembly_ID', 'type': 'str', 'mandatory': False},
                                                 {'name': 'Auth_seq_ID', 'type': 'int', 'mandatory': False},
                                                 {'name': 'Auth_comp_ID', 'type': 'str', 'mandatory': False},
                                                 {'name': 'Auth_atom_ID', 'type': 'str', 'mandatory': False},
                                                 {'name': 'Heteronucl_T2_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                                  'default': '1', 'default-from': 'parent'},
                                                 {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                 ],
                          'heteronucl_t1r_data': [{'name': 'Atom_type', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID',
                                                   'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                   'enforce-enum': True},
                                                  {'name': 'Atom_isotope_number', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID',
                                                   'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                   'enforce-enum': True},
                                                  {'name': 'T1rho_val', 'type': 'float', 'mandatory': True},
                                                  {'name': 'T1rho_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                                   'range': {'min_inclusive': 0.0}},
                                                  {'name': 'Rex_val', 'type': 'float', 'mandatory': False},
                                                  {'name': 'Rex_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                                   'range': {'min_inclusive': 0.0}},
                                                  {'name': 'Auth_entity_assembly_ID', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Auth_seq_ID', 'type': 'int', 'mandatory': False},
                                                  {'name': 'Auth_comp_ID', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Auth_atom_ID', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Heteronucl_T1rho_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                                   'default': '1', 'default-from': 'parent'},
                                                  {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                  ],
                          'order_param_data': [{'name': 'Atom_type', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID',
                                                'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                'enforce-enum': True},
                                               {'name': 'Atom_isotope_number', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID',
                                                'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                'enforce-enum': True},
                                               {'name': 'Order_param_val', 'type': 'range-float', 'mandatory': True,
                                                'range': PROBABILITY_RANGE},
                                               {'name': 'Order_param_val_fit_err', 'type': 'range-float', 'mandatory': False,
                                                'range': PROBABILITY_RANGE},
                                               {'name': 'Tau_e_val', 'type': 'positive-float', 'mandatory': False},
                                               {'name': 'Tau_e_val_fit_err', 'type': 'positive-float', 'mandatory': False},
                                               {'name': 'Tau_f_val', 'type': 'positive-float', 'mandatory': False},
                                               {'name': 'Tau_f_val_fit_err', 'type': 'positive-float', 'mandatory': False},
                                               {'name': 'Tau_s_val', 'type': 'positive-float', 'mandatory': False},
                                               {'name': 'Tau_s_val_fit_err', 'type': 'positive-float', 'mandatory': False},
                                               {'name': 'Rex_val', 'type': 'range-float', 'mandatory': False,
                                                'range': PRE_RESTRAINT_RANGE},
                                               {'name': 'Rex_val_fit_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                                'range': PRE_RESTRAINT_RANGE},
                                               {'name': 'Model_free_sum_squared_errs', 'type': 'positive-float', 'mandatory': False},
                                               {'name': 'Model_fit', 'type': 'enum', 'mandatory': False,
                                                'enum': ('Rex', 'S2', 'S2, te', 'S2, Rex', 'S2, te, Rex', 'S2f, S2, ts', 'S2f, S2s, ts',
                                                         'S2f, tf, S2, ts', 'S2f, tf, S2s, ts', 'S2f, S2, ts, Rex', 'S2f, S2s, ts, Rex',
                                                         'S2f, tf, S2, ts, Rex', 'S2f, tf, S2s, ts, Rex', 'na')},
                                               {'name': 'Sf2_val', 'type': 'range-float', 'mandatory': False,
                                                'range': PROBABILITY_RANGE},
                                               {'name': 'Sf2_val_fit_err', 'type': 'range-float', 'mandatory': False,
                                                'range': PROBABILITY_RANGE},
                                               {'name': 'Ss2_val', 'type': 'range-float', 'mandatory': False,
                                                'range': PROBABILITY_RANGE},
                                               {'name': 'Ss2_val_fit_err', 'type': 'range-float', 'mandatory': False,
                                                'range': PROBABILITY_RANGE},
                                               {'name': 'SH2_val', 'type': 'range-float', 'mandatory': False,
                                                'range': PROBABILITY_RANGE},
                                               {'name': 'SH2_val_fit_err', 'type': 'range-float', 'mandatory': False,
                                                'range': PROBABILITY_RANGE},
                                               {'name': 'SN2_val', 'type': 'range-float', 'mandatory': False,
                                                'range': PROBABILITY_RANGE},
                                               {'name': 'SN2_val_fit_err', 'type': 'range-float', 'mandatory': False,
                                                'range': PROBABILITY_RANGE},
                                               {'name': 'Auth_entity_assembly_ID', 'type': 'str', 'mandatory': False},
                                               {'name': 'Auth_seq_ID', 'type': 'int', 'mandatory': False},
                                               {'name': 'Auth_comp_ID', 'type': 'str', 'mandatory': False},
                                               {'name': 'Auth_atom_ID', 'type': 'str', 'mandatory': False},
                                               {'name': 'Order_parameter_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                                'default': '1', 'default-from': 'parent'},
                                               {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                               ],
                          'ccr_d_csa_restraint': [{'name': 'Dipole_atom_type_1', 'type': 'enum', 'mandatory': True, 'default-from': 'Dipole_atom_ID_1',
                                                   'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                   'enforce-enum': True},
                                                  {'name': 'Dipole_atom_isotope_number_1', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Dipole_atom_ID_1',
                                                   'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                   'enforce-enum': True},
                                                  {'name': 'Dipole_atom_type_2', 'type': 'enum', 'mandatory': True, 'default-from': 'Dipole_atom_ID_2',
                                                   'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                   'enforce-enum': True},
                                                  {'name': 'Dipole_atom_isotope_number_2', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Dipole_atom_ID_2',
                                                   'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                   'enforce-enum': True},
                                                  {'name': 'CSA_atom_type_1', 'type': 'enum', 'mandatory': True, 'default-from': 'CSA_atom_ID_1',
                                                   'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                   'enforce-enum': True},
                                                  {'name': 'CSA_atom_isotope_number_1', 'type': 'enum-int', 'mandatory': True, 'default-from': 'CSA_atom_ID_1',
                                                   'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                   'enforce-enum': True},
                                                  {'name': 'CSA_atom_type_2', 'type': 'enum', 'mandatory': True, 'default-from': 'CSA_atom_ID_2',
                                                   'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                   'enforce-enum': True},
                                                  {'name': 'CSA_atom_isotope_number_2', 'type': 'enum-int', 'mandatory': True, 'default-from': 'CSA_atom_ID_2',
                                                   'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                   'enforce-enum': True},
                                                  {'name': 'Val', 'type': 'range-float', 'mandatory': True,
                                                   'range': CCR_RESTRAINT_RANGE},
                                                  {'name': 'Val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                                   'range': CCR_RESTRAINT_RANGE},
                                                  {'name': 'Dipole_auth_entity_assembly_ID_1', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Dipole_auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                                  {'name': 'Dipole_auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Dipole_auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Dipole_auth_entity_assembly_ID_2', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Dipole_auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                                  {'name': 'Dipole_auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Dipole_auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                                  {'name': 'CSA_auth_entity_assembly_ID_1', 'type': 'str', 'mandatory': False},
                                                  {'name': 'CSA_auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                                  {'name': 'CSA_auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                                  {'name': 'CSA_auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                                  {'name': 'CSA_auth_entity_assembly_ID_2', 'type': 'str', 'mandatory': False},
                                                  {'name': 'CSA_auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                                  {'name': 'CSA_auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                                  {'name': 'CSA_auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Cross_correlation_D_CSA_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                                   'default': '1', 'default-from': 'parent'},
                                                  {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                  ],
                          'ccr_dd_restraint': [{'name': 'Dipole_1_atom_type_1', 'type': 'enum', 'mandatory': True, 'default-from': 'Dipole_1_atom_ID_1',
                                                'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                'enforce-enum': True},
                                               {'name': 'Dipole_1_atom_isotope_number_1', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Dipole_1_atom_ID_1',
                                                'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                'enforce-enum': True},
                                               {'name': 'Dipole_1_atom_type_2', 'type': 'enum', 'mandatory': True, 'default-from': 'Dipole_1_atom_ID_2',
                                                'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                'enforce-enum': True},
                                               {'name': 'Dipole_1_atom_isotope_number_2', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Dipole_1_atom_ID_2',
                                                'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                'enforce-enum': True},
                                               {'name': 'Dipole_2_atom_type_1', 'type': 'enum', 'mandatory': True, 'default-from': 'Dipole_2_atom_ID_1',
                                                'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                'enforce-enum': True},
                                               {'name': 'Dipole_2_atom_isotope_number_1', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Dipole_2_atom_ID_1',
                                                'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                'enforce-enum': True},
                                               {'name': 'Dipole_2_atom_type_2', 'type': 'enum', 'mandatory': True, 'default-from': 'Dipole_2_atom_ID_2',
                                                'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                'enforce-enum': True},
                                               {'name': 'Dipole_2_atom_isotope_number_2', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Dipole_2_atom_ID_2',
                                                'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                'enforce-enum': True},
                                               {'name': 'Val', 'type': 'range-float', 'mandatory': True,
                                                'range': CCR_RESTRAINT_RANGE},
                                               {'name': 'Val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                                'range': CCR_RESTRAINT_RANGE},
                                               {'name': 'Dipole_1_auth_entity_assembly_ID_1', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_1_auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                               {'name': 'Dipole_1_auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_1_auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_1_auth_entity_assembly_ID_2', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_1_auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                               {'name': 'Dipole_1_auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_1_auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_2_auth_entity_assembly_ID_1', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_2_auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                               {'name': 'Dipole_2_auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_2_auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_2_auth_entity_assembly_ID_2', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_2_auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                               {'name': 'Dipole_2_auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_2_auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                               {'name': 'Cross_correlation_DD_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                                'default': '1', 'default-from': 'parent'},
                                               {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                               ],
                          'fchiral_restraint': [{'name': 'Stereospecific_assignment_code', 'type': 'str', 'mandatory': True},
                                                {'name': 'Auth_asym_ID_1', 'type': 'str', 'mandatory': False},
                                                {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                                {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                                {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                                {'name': 'Auth_asym_ID_2', 'type': 'str', 'mandatory': False},
                                                {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                                {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                                {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                                {'name': 'Floating_chirality_assign_ID', 'type': 'pointer-index', 'mandatory': True,
                                                 'default': '1', 'default-from': 'parent'},
                                                {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                ],
                          'saxs_restraint': [{'name': 'Intensity_val', 'type': 'float', 'mandatory': True},
                                             {'name': 'Intensity_val_err', 'type': 'float', 'mandatory': True},
                                             {'name': 'Weight_val', 'type': 'range-float', 'mandatory': False,
                                              'range': WEIGHT_RANGE},
                                             {'name': 'SAXS_constraint_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                              'default': '1', 'default-from': 'parent'},
                                             {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                             ],
                          'other_restraint': [{'name': 'Atom_type', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID',
                                               'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                               'enforce-enum': True},
                                              {'name': 'Atom_isotope_number', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID',
                                               'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                               'enforce-enum': True},
                                              {'name': 'Val', 'type': 'float', 'mandatory': True},
                                              {'name': 'Val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                               'range': {'min_inclusive': 0.0}},
                                              {'name': 'Auth_entity_assembly_ID', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID', 'type': 'str', 'mandatory': False},
                                              {'name': 'Other_data_type_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                               'default': '1', 'default-from': 'parent'},
                                              {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                              ]
                          }

NMR_STAR_LP_DATA_ITEMS_INS_CODE = {'dist_restraint': copy.copy(NMR_STAR_LP_DATA_ITEMS['dist_restraint'][:-2]),
                                   'dihed_restraint': copy.copy(NMR_STAR_LP_DATA_ITEMS['dihed_restraint'][:-2]),
                                   'rdc_restraint': copy.copy(NMR_STAR_LP_DATA_ITEMS['rdc_restraint'][:-2])
                                   }

NMR_STAR_LP_DATA_ITEMS_INS_CODE['dist_restraint'].extend([{'name': 'PDB_ins_code_1', 'type': 'str', 'mandatory': False},
                                                          {'name': 'PDB_ins_code_2', 'type': 'str', 'mandatory': False},
                                                          {'name': 'Gen_dist_constraint_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                                           'default': '1', 'default-from': 'parent'},
                                                          {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                          ])

NMR_STAR_LP_DATA_ITEMS_INS_CODE['dihed_restraint'].extend([{'name': 'PDB_ins_code_1', 'type': 'str', 'mandatory': False},
                                                           {'name': 'PDB_ins_code_2', 'type': 'str', 'mandatory': False},
                                                           {'name': 'PDB_ins_code_3', 'type': 'str', 'mandatory': False},
                                                           {'name': 'PDB_ins_code_4', 'type': 'str', 'mandatory': False},
                                                           {'name': 'Torsion_angle_constraint_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                                            'default': '1', 'default-from': 'parent'},
                                                           {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                           ])

NMR_STAR_LP_DATA_ITEMS_INS_CODE['rdc_restraint'].extend([{'name': 'PDB_ins_code_1', 'type': 'str', 'mandatory': False},
                                                         {'name': 'PDB_ins_code_2', 'type': 'str', 'mandatory': False},
                                                         {'name': 'RDC_constraint_list_ID', 'type': 'pointer-index', 'mandatory': True, 'default': '1', 'default-from': 'parent'},
                                                         {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                         ])

NMR_STAR_AUX_LP_CATEGORIES = {'dist_restraint': ['_Gen_dist_constraint_software_param']
                              }

NMR_STAR_AUX_LP_KEY_ITEMS = {'dist_restraint': {'_Gen_dist_constraint_software_param': [
                                                {'name': 'Software_ID', 'type': 'int', 'mandatory': True},
                                                {'name': 'Type', 'type': 'str', 'mandatory': True}]
                                                }
                             }

NMR_STAR_AUX_LP_DATA_ITEMS = {'dist_restraint': {'_Gen_dist_constraint_software_param': [
                                                 {'name': 'Value', 'type': 'str', 'mandatory': False},
                                                 {'name': 'Range', 'type': 'str', 'mandatory': False},
                                                 {'name': 'Gen_dist_constraint_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                                  'default': '1', 'default-from': 'parent'},
                                                 {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}]
                                                 }
                              }

CARTN_DATA_ITEMS = [{'name': 'Cartn_x', 'type': 'float', 'alt_name': 'x'},
                    {'name': 'Cartn_y', 'type': 'float', 'alt_name': 'y'},
                    {'name': 'Cartn_z', 'type': 'float', 'alt_name': 'z'}
                    ]

AUTH_ATOM_DATA_ITEMS = [{'name': 'auth_asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                        {'name': 'auth_seq_id', 'type': 'int', 'alt_name': 'seq_id'},
                        {'name': 'label_comp_id', 'type': 'str', 'alt_name': 'comp_id'},
                        {'name': 'label_atom_id', 'type': 'str', 'alt_name': 'atom_id'}
                        ]

ATOM_NAME_DATA_ITEMS = [{'name': 'label_comp_id', 'type': 'str', 'alt_name': 'comp_id'},
                        {'name': 'label_atom_id', 'type': 'str', 'alt_name': 'atom_id'}
                        ]

AUTH_ATOM_CARTN_DATA_ITEMS = CARTN_DATA_ITEMS
AUTH_ATOM_CARTN_DATA_ITEMS.extend(AUTH_ATOM_DATA_ITEMS)

PTNR1_AUTH_ATOM_DATA_ITEMS = [{'name': 'ptnr1_auth_asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                              {'name': 'ptnr1_auth_seq_id', 'type': 'int', 'alt_name': 'seq_id'},
                              {'name': 'ptnr1_label_comp_id', 'type': 'str', 'alt_name': 'comp_id'},
                              {'name': 'ptnr1_label_atom_id', 'type': 'str', 'alt_name': 'atom_id'}
                              ]

PTNR2_AUTH_ATOM_DATA_ITEMS = [{'name': 'ptnr2_auth_asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                              {'name': 'ptnr2_auth_seq_id', 'type': 'int', 'alt_name': 'seq_id'},
                              {'name': 'ptnr2_label_comp_id', 'type': 'str', 'alt_name': 'comp_id'},
                              {'name': 'ptnr2_label_atom_id', 'type': 'str', 'alt_name': 'atom_id'}
                              ]


def toRegEx(string):
    """ Return regular expression for a given string including XPLOR-NIH wildcard format.
    """

    if '*' in string:  # any string
        return string.replace('*', '.*')
    if '%' in string:  # a single character
        return string.replace('%', '.')
    if '#' in string:  # any number
        return string.replace('#', '[+-]?[0-9\\.]*')
    if '+' in string:  # any digit
        return string.replace('+', '[0-9]*')
    return string


def toNefEx(string):
    """ Return NEF regular expression for a given string including XPLOR-NIH wildcard format.
    """

    if '*' in string:  # any string
        return re.sub(r'\*\*', '*', string)
    if '%' in string:  # a single character
        return re.sub(r'\*\*', '*', string.replace('%', '*'))
    if '#' in string:  # any number
        return re.sub(r'\*\*', '*', string.replace('#', '*'))
    if '+' in string:  # any digit
        return re.sub(r'\%\%', '%', string.replace('+', '%'))
    return string


def stripQuot(string):
    """ Return strippped string by removing single/double quotation marks.
    """

    _string = string.strip()

    while True:
        if (_string[0] == '\'' and _string[-1] == '\'')\
           or (_string[0] == '"' and _string[-1] == '"'):
            _string = _string[1:len(_string) - 1].strip()
        else:
            break

    return _string


def translateToStdAtomName(atomId, refCompId=None, refAtomIdList=None, ccU=None, unambig=False):
    """ Translate software specific atom nomenclature for standard residues to the CCD one.
    """

    atomId = atomId.upper()

    if refAtomIdList is not None:
        if atomId in refAtomIdList:
            return atomId

    if refCompId is not None and ccU is not None:
        refCompId = translateToStdResName(refCompId, ccU)
        if ccU.updateChemCompDict(refCompId):
            if refAtomIdList is not None:
                if atomId in refAtomIdList:
                    return atomId
            _refAtomIdList = [cca[ccU.ccaAtomId] for cca in ccU.lastAtomList]
            if "'" not in atomId and atomId in _refAtomIdList:
                return atomId
            # DNA/RNA OH 5/3 prime terminus
            if atomId.startswith("H1'"):
                if refAtomIdList is not None:
                    if atomId == "H1''" and "H1'A" in refAtomIdList:  # 4DG
                        return "H1'A"
                    if atomId == "H1''" and "H1'" in refAtomIdList:
                        return "H1'"
                if atomId == "H1''" and "H1'A" in _refAtomIdList:  # 4DG
                    return "H1'A"
                if atomId == "H1''" and "H1'" in _refAtomIdList:
                    return "H1'"
            elif atomId.startswith("H2'"):
                if refAtomIdList is not None:
                    if atomId == "H2'" and "H2'1" in refAtomIdList:  # DCZ, THM
                        return "H2'1"
                    if atomId == "H2''" and "H2'2" in refAtomIdList:  # DCZ, THM
                        return "H2'2"
                    if atomId == "H2''" and "H2'" in refAtomIdList:
                        return "H2'"
                    if atomId == "H2''''" and "H2''" in refAtomIdList:
                        return "H2''"
                    if atomId == "H2''''" and "H2'2" in refAtomIdList:  # DCZ, THM
                        return "H2'2"
                    if atomId == "H2''1" and "H2'1" in refAtomIdList:  # 4EN
                        return "H2'1"
                    if atomId == "H2''2" and "H2'2" in refAtomIdList:  # 4EN
                        return "H2'2"
                    if atomId == "H2''1" and "H2'" in refAtomIdList:
                        return "H2'"
                    if atomId == "H2''2" and "H2''" in refAtomIdList:
                        return "H2''"
                if atomId == "H2'" and "H2'1" in _refAtomIdList:  # DCZ, THM
                    return "H2'1"
                if atomId == "H2''" and "H2'2" in _refAtomIdList:  # DCZ, THM
                    return "H2'2"
                if atomId == "H2''" and "H2'" in _refAtomIdList:
                    return "H2'"
                if atomId == "H2''''" and "H2''" in _refAtomIdList:
                    return "H2''"
                if atomId == "H2''''" and "H2'2" in _refAtomIdList:  # DCZ, THM
                    return "H2'2"
                if atomId == "H2''" and "H2'2" in _refAtomIdList:  # DCZ, THM
                    return "H2'2"
                if atomId == "H2''1" and "H2'1" in _refAtomIdList:  # 4EN
                    return "H2'1"
                if atomId == "H2''2" and "H2'2" in _refAtomIdList:  # 4EN
                    return "H2'2"
                if atomId == "H2''1" and "H2'" in _refAtomIdList:
                    return "H2'"
                if atomId == "H2''2" and "H2''" in _refAtomIdList:
                    return "H2''"
            elif atomId.startswith("H3'"):
                if refAtomIdList is not None:
                    if atomId == "H3''" and "H3'A" in refAtomIdList:
                        return "H3'A"
                    if atomId == "H3''" and "H3'" in refAtomIdList:
                        return "H3'"
                if atomId == "H3''" and "H3'A" in _refAtomIdList:
                    return "H3'A"
                if atomId == "H3''" and "H3'" in _refAtomIdList:
                    return "H3'"
            elif atomId.startswith("H4'"):
                if refAtomIdList is not None:
                    if atomId == "H4''" and "H4'A" in refAtomIdList:  # 4DG
                        return "H4'A"
                    if atomId == "H4''" and "H4'" in refAtomIdList:
                        return "H4'"
                if atomId == "H4''" and "H4'A" in _refAtomIdList:  # 4DG
                    return "H4'A"
                if atomId == "H4''" and "H4'" in _refAtomIdList:
                    return "H4'"
            elif atomId.startswith("H5'"):
                if refAtomIdList is not None:
                    if atomId == "H5'" and "H5'1" in refAtomIdList:  # DCZ, THM
                        return "H5'1"
                    if atomId == "H5''" and "H5'2" in refAtomIdList:  # DCZ, THM
                        return "H5'2"
                    if atomId == "H5''''" and "H5''" in refAtomIdList:
                        return "H5''"
                    if atomId == "H5''''" and "H5'2" in refAtomIdList:  # DCZ, THM
                        return "H5'2"
                    if atomId == "H5''" and "H5'A" in refAtomIdList:  # 4DG, 23G
                        return "H5'A"
                    if atomId == "H5''1" and "H5'1" in refAtomIdList:  # 4EN
                        return "H5'1"
                    if atomId == "H5''2" and "H5'2" in refAtomIdList:  # 4EN
                        return "H5'2"
                    if atomId == "H5''1" and "H5'" in refAtomIdList:
                        return "H5'"
                    if atomId == "H5''2" and "H5''" in refAtomIdList:
                        return "H5''"
                if atomId == "H5'" and "H5'1" in _refAtomIdList:  # DCZ, THM
                    return "H5'1"
                if atomId == "H5''" and "H5'2" in _refAtomIdList:  # DCZ, THM
                    return "H5'2"
                if atomId == "H5''''" and "H5''" in _refAtomIdList:
                    return "H5''"
                if atomId == "H5''''" and "H5'2" in _refAtomIdList:  # DCZ, THM
                    return "H5'2"
                if atomId == "H5''" and "H5'A" in _refAtomIdList:  # 4DG, 23G
                    return "H5'A"
                if atomId == "H5''1" and "H5'1" in _refAtomIdList:  # 4EN
                    return "H5'1"
                if atomId == "H5''2" and "H5'2" in _refAtomIdList:  # 4EN
                    return "H5'2"
                if atomId == "H5''1" and "H5'" in _refAtomIdList:
                    return "H5'"
                if atomId == "H5''2" and "H5''" in _refAtomIdList:
                    return "H5''"

            if atomId in _refAtomIdList:
                return atomId

            if atomId.startswith('M'):  # methyl group
                if refAtomIdList is not None:
                    if 'H' + atomId[1:] + '1' in refAtomIdList:
                        return 'H' + atomId[1:]
                if 'H' + atomId[1:] + '1' in _refAtomIdList:
                    return 'H' + atomId[1:]
                candidates = ccU.getRepMethylProtons(refCompId)
                if len(candidates) == 1:
                    atomId = candidates[0]
                    return atomId[:-1] if atomId.endswith('1') else atomId
            elif refAtomIdList is not None and ((atomId[0] + 'N' + atomId[1:] in refAtomIdList) or (atomId[0] + 'N' + atomId[1:] + '1' in refAtomIdList)):  # 5CM
                return atomId[0] + 'N' + atomId[1:]
            elif (atomId[0] + 'N' + atomId[1:] in _refAtomIdList) or (atomId[0] + 'N' + atomId[1:] + '1' in _refAtomIdList):  # 5CM
                return atomId[0] + 'N' + atomId[1:]
            elif refAtomIdList is not None and atomId[0].endswith('2') and (atomId[0:-1] + 'A') in refAtomIdList:
                return atomId[0:-1] + 'A'
            elif atomId[0].endswith('2') and (atomId[0:-1] + 'A') in _refAtomIdList:
                return atomId[0:-1] + 'A'
            elif refAtomIdList is not None and atomId[0].endswith('3') and (atomId[0:-1] + 'B') in refAtomIdList:
                return atomId[0:-1] + 'B'
            elif atomId[0].endswith('3') and (atomId[0:-1] + 'B') in _refAtomIdList:
                return atomId[0:-1] + 'B'
            elif atomId.startswith('1H'):
                if refAtomIdList is not None:
                    if atomId[1:] + '1' in refAtomIdList:
                        return atomId[1:] + '1'
                if atomId[1:] + '1' in _refAtomIdList:
                    return atomId[1:] + '1'
            elif atomId.startswith('2H'):
                if refAtomIdList is not None:
                    if atomId[1:] + '2' in refAtomIdList:
                        return atomId[1:] + '2'
                if atomId[1:] + '2' in _refAtomIdList:
                    return atomId[1:] + '2'
            elif atomId.startswith('3H'):
                if refAtomIdList is not None:
                    if atomId[1:] + '3' in refAtomIdList:
                        return atomId[1:] + '3'
                if atomId[1:] + '3' in _refAtomIdList:
                    return atomId[1:] + '3'
            elif atomId == "HX'":  # derived from 2mko AMBER RDC restraints
                if refAtomIdList is not None:
                    if "H4'" in refAtomIdList:
                        return "H4'"
                if "H4'" in _refAtomIdList:
                    return "H4'"

            if not unambig:

                # ambiguous atom generated by 'makeDIST_RST'
                if atomId[0] == 'Q':
                    if atomId.startswith('QP'):
                        if refAtomIdList is not None:
                            if 'H' + atomId[2:] + '2' in refAtomIdList:
                                return 'H' + atomId[2:] + '%'
                        if 'H' + atomId[2:] + '2' in _refAtomIdList:
                            return 'H' + atomId[2:] + '%'
                    else:
                        if refAtomIdList is not None:
                            if 'H' + atomId[1:] + '2' in refAtomIdList:
                                return 'H' + atomId[1:] + '%'
                        if 'H' + atomId[1:] + '2' in _refAtomIdList:
                            return 'H' + atomId[1:] + '%'

                elif atomId[-1] in ('-', '+'):
                    if refAtomIdList is not None:
                        if atomId[:-1] + '2' in refAtomIdList:
                            return atomId[:-1] + '%'
                    if atomId[:-1] + '2' in _refAtomIdList:
                        return atomId[:-1] + '%'

                elif atomId[0] == 'M':
                    if atomId[-1] in ('X', 'Y'):
                        if refAtomIdList is not None:
                            if 'H' + atomId[1:-1] + '1' in refAtomIdList or 'H' + atomId[1:-1] + '11' in refAtomIdList:
                                return 'H' + atomId[1:-1] + '%'
                        if 'H' + atomId[1:-1] + '1' in _refAtomIdList or 'H' + atomId[1:-1] + '11' in _refAtomIdList:
                            return 'H' + atomId[1:-1] + '%'
                    elif refAtomIdList is not None and ('H' + atomId[1:] + '1' in refAtomIdList or 'H' + atomId[1:] + '11' in refAtomIdList):
                        return 'H' + atomId[1:] + '%'
                    elif 'H' + atomId[1:] + '1' in _refAtomIdList or 'H' + atomId[1:] + '11' in _refAtomIdList:
                        return 'H' + atomId[1:] + '%'

                elif refAtomIdList is not None and atomId + '2' in refAtomIdList:
                    return atomId + '%'
                elif atomId + '2' in _refAtomIdList:
                    return atomId + '%'

    if refCompId is not None:

        # GROMACS atom nomenclature
        if refCompId == 'ILE':
            if atomId in ('HD1', 'HD2', 'HD3'):
                return 'HD1' + atomId[-1]
            if atomId == 'CD':
                return 'CD1'
        if len(refCompId) == 3 and refCompId in monDict3:
            if atomId == 'O1':
                return 'O'
            if atomId == 'O2':
                return 'OXT'
            if atomId.startswith('HT') and len(atomId) > 2:
                return 'H' + atomId[2:]

        # BIOSYM atom nomenclature
        if (atomId[-1] in ('R', 'S', 'Z', 'E') or (len(atomId) > 2 and atomId[-1] in ('*', '%') and atomId[-2] in ('R', 'S'))):
            if refCompId in ('CYS', 'ASP', 'HIS', 'SER'):
                if atomId == 'HBR':
                    return 'HB3'
                if atomId == 'HBS':
                    return 'HB2'
            elif refCompId in ('GLU', 'PHE', 'TRP', 'TYR'):
                if atomId == 'HBR':
                    return 'HB2'
                if atomId == 'HBS':
                    return 'HB3'
                if atomId == 'HGR':
                    return 'HG3'
                if atomId == 'HGS':
                    return 'HG2'
            elif refCompId == 'GLY':
                if atomId == 'HAR':
                    return 'HA2'
                if atomId == 'HAS':
                    return 'HA3'
            elif refCompId == 'ILE':
                if atomId == 'HG1R':
                    return 'HG12'
                if atomId == 'HG1S':
                    return 'HG13'
            elif refCompId == 'LYS':
                if atomId == 'HBR':
                    return 'HB2'
                if atomId == 'HBS':
                    return 'HB3'
                if atomId == 'HGR':
                    return 'HG2'
                if atomId == 'HGS':
                    return 'HG3'
                if atomId == 'HDR':
                    return 'HD3'
                if atomId == 'HDS':
                    return 'HD2'
                if atomId == 'HER':
                    return 'HE3'
                if atomId == 'HES':
                    return 'HE2'
            elif refCompId == 'LEU':
                if atomId == 'HBR':
                    return 'HB2'
                if atomId == 'HBS':
                    return 'HB3'
                if atomId in ('HDR*', 'HDR%'):
                    return 'HD1'
                if atomId in ('HDS*', 'HDS%'):
                    return 'HD2'
                if atomId == 'CDR':
                    return 'CD1'
                if atomId == 'CDS':
                    return 'CD2'
            elif refCompId == 'MET':
                if atomId == 'HBR':
                    return 'HB3'
                if atomId == 'HBS':
                    return 'HB2'
                if atomId == 'HGR':
                    return 'HG3'
                if atomId == 'HGS':
                    return 'HG2'
            elif refCompId == 'ASN':
                if atomId == 'HBR':
                    return 'HB3'
                if atomId == 'HBS':
                    return 'HB2'
                if atomId == 'HD2Z':
                    return 'HD22'
                if atomId == 'HD2E':
                    return 'HD21'
            elif refCompId == 'PRO':
                if atomId == 'HBR':
                    return 'HB2'
                if atomId == 'HBS':
                    return 'HB3'
                if atomId == 'HGR':
                    return 'HG3'
                if atomId == 'HGS':
                    return 'HG2'
                if atomId == 'HDR':
                    return 'HD3'
                if atomId == 'HDS':
                    return 'HD2'
            elif refCompId == 'GLN':
                if atomId == 'HBR':
                    return 'HB2'
                if atomId == 'HBS':
                    return 'HB3'
                if atomId == 'HGR':
                    return 'HG3'
                if atomId == 'HGS':
                    return 'HG2'
                if atomId == 'HE2Z':
                    return 'HE22'
                if atomId == 'HE2E':
                    return 'HE21'
            elif refCompId == 'ARG':
                if atomId == 'HBR':
                    return 'HB2'
                if atomId == 'HBS':
                    return 'HB3'
                if atomId == 'HGR':
                    return 'HG3'
                if atomId == 'HGS':
                    return 'HG2'
                if atomId == 'HDR':
                    return 'HD3'
                if atomId == 'HDS':
                    return 'HD2'
                if atomId == 'NHZ':
                    return 'NH1'
                if atomId == 'NHE':
                    return 'NH2'
                if atomId == 'HH1Z':
                    return 'HH11'
                if atomId == 'HH1E':
                    return 'HH12'
                if atomId == 'HH2Z':
                    return 'HH21'
                if atomId == 'HH2E':
                    return 'HH22'
            elif refCompId == 'VAL':
                if atomId in ('HGR*', 'HGR%'):
                    return 'HG1'
                if atomId in ('HGS*', 'HGS%'):
                    return 'HG2'
                if atomId == 'CGR':
                    return 'CG1'
                if atomId == 'CGS':
                    return 'CG2'

        if refCompId == 'NH2':
            if atomId in ('HN*', 'HN%', 'H*', 'H%', 'QH', 'QN') and not unambig:
                return 'HN%'
            if atomId in ('H', 'HN'):
                return 'HN1'
            if atomId.startswith('H'):
                return 'HN2'

        if refCompId == 'ACE':
            if atomId in ('HA*', 'HA%', 'QH', 'MH', 'QA', 'MA') and not unambig:
                return 'H%'
            if atomId == 'CA':
                return 'CH3'

        if refCompId in ('HEB', 'HEC'):
            if atomId[0] in pseProBeginCode:
                if atomId == 'QM1':
                    return 'HMB'
                if atomId == 'QT2':
                    return 'HBB'
                if atomId.startswith('HT2') and refCompId == 'HEC':
                    return 'HAB'
                if atomId in ('HT2', 'HA2', 'HA21', 'HA22') and refCompId == 'HEB':
                    return 'HAB'
                if atomId == 'HA23' and refCompId == 'HEB':
                    return 'HAB2'
                if atomId == 'QM3':
                    return 'HMC'
                if atomId == 'QT4':
                    return 'HBC'
                if atomId.startswith('HT4'):
                    return 'HAC'
                if atomId == 'QM5':
                    return 'HMD'
                if atomId == 'HA62':
                    return 'HAD1'
                if atomId == 'HA63':
                    return 'HAD2'
                if atomId == 'HB62':
                    return 'HBD1'
                if atomId == 'HB63':
                    return 'HBD2'
                if atomId == 'HA72':
                    return 'HAA1'
                if atomId == 'HA73':
                    return 'HAA2'
                if atomId == 'HB72':
                    return 'HBA1'
                if atomId == 'HB73':
                    return 'HBA2'
                if atomId == 'HA6':
                    return 'HAD'
                if atomId == 'HB6':
                    return 'HBD'
                if atomId == 'HA7':
                    return 'HAA'
                if atomId == 'HB7':
                    return 'HBA'
                if atomId == 'QM8':
                    return 'HMA'
                if atomId == 'HAM':
                    return 'HHA'
                if atomId == 'HBM':
                    return 'HHB'
                if atomId in ('HGM', 'HCM'):
                    return 'HHC'
                if atomId == 'HDM':
                    return 'HHD'

    if atomId.endswith("O'1"):
        atomId = atomId[:len(atomId) - 3] + "O1'"
    elif atomId.endswith("O'2"):
        atomId = atomId[:len(atomId) - 3] + "O2'"
    elif atomId.endswith("O'3"):
        atomId = atomId[:len(atomId) - 3] + "O3'"
    elif atomId.endswith("O'4"):
        atomId = atomId[:len(atomId) - 3] + "O4'"
    elif atomId.endswith("O'5"):
        atomId = atomId[:len(atomId) - 3] + "O5'"
    elif atomId.endswith("O'6"):
        atomId = atomId[:len(atomId) - 3] + "O6'"
    elif atomId.endswith("'1") and not atomId.endswith("''1"):
        atomId = atomId.rstrip('1')
    elif atomId.endswith("'2") and not atomId.endswith("''2"):
        atomId = atomId.rstrip('2') + "'"
    elif atomId == 'O1P':
        atomId = 'OP1'
    elif atomId == 'O2P':
        atomId = 'OP2'
    elif atomId == 'O3P':
        atomId = 'OP3'
    elif atomId == 'H3T':
        atomId = "HO3'"
    elif atomId == 'H5T':
        atomId = 'HOP2'
    elif atomId.endswith("''"):
        if atomId[0] in ('C', 'O') and atomId[1].isdigit():
            atomId = atomId[:len(atomId) - 1]
    elif atomId.endswith('"'):
        atomId = atomId[:len(atomId) - 1] + "''"

    if refAtomIdList is not None and atomId not in refAtomIdList:
        if not atomId.endswith("'") and (atomId + "'") in refAtomIdList:
            return atomId + "'"
        if atomId.endswith("''''"):
            if atomId.startswith('H2') and "H2'2" in refAtomIdList:
                return "H2'2"
            if atomId.startswith('H5') and "H5'2" in refAtomIdList:
                return "H5'2"
            if atomId[:-2] in refAtomIdList:
                return atomId[:-2]
        if atomId.endswith("'''"):
            if atomId.startswith('H2') and "H2'1" in refAtomIdList:
                return "H2'1"
            if atomId.startswith('H5') and "H5'1" in refAtomIdList:
                return "H5'1"
            if atomId[:-1] in refAtomIdList:
                return atomId[:-1]
        if atomId == "H2''1" and "H2'" in refAtomIdList:
            return "H2'"
        if atomId == "H5''1" and "H5'" in refAtomIdList:
            return "H5'"
        if atomId in ("H2''2", "H2''"):
            if "HO2'" in refAtomIdList:
                return "HO2'"
            if "H2''" in refAtomIdList:
                return "H2''"
            if atomId == "H2''" and "H2'1" in refAtomIdList:
                return "H2'1"
        if atomId in ("H5''2", "H5''"):
            if "H5''" in refAtomIdList:
                return "H5''"
            if atomId == "H5''" and "H5'1" in refAtomIdList:
                return "H5'1"
        if atomId.endswith("''") and atomId[:-1] in refAtomIdList:
            return atomId[:-1]
        if atomId[0] == 'H' and len(atomId) == 3 and atomId[1].isdigit() and atomId[2] in ('1', '2'):
            n = atomId[1]
            if atomId.endswith('1') and ('HN' + n) in refAtomIdList:
                return 'HN' + n
            if atomId.endswith('2') and ('HN' + n + 'A') in refAtomIdList:
                return 'HN' + n + 'A'

    if atomId.endswith('+1') or atomId.endswith('+2') or atomId.endswith('+3'):
        if atomId[:-2] in SYMBOLS_ELEMENT:
            return atomId[:-2]

    return atomId


def translateToStdAtomNameOfDmpc(atomId, dmpcNameSystemId=-1):
    """ Translate software specific atom nomenclature for DMPC to CCD PX4.
    """

    atomId = atomId.upper()

    if dmpcNameSystemId == 1:  # 2mzi
        if atomId.startswith('CN') and len(atomId) == 3:
            if atomId[-1] == '1':
                return 'C3'
            if atomId[-1] == '2':
                return 'C4'
            if atomId[-1] == '3':
                return 'C5'
        if atomId == 'NTM':
            return 'N1'
        if atomId == 'CA':
            return 'C2'
        if atomId == 'CB':
            return 'C1'
        if atomId == 'P':
            return 'P1'
        if atomId == 'OA':
            return 'O3'
        if atomId == 'OB':
            return 'O1'
        if atomId == 'OC':
            return 'O2'
        if atomId == 'OD':
            return 'O4'
        if atomId == 'CC':
            return 'C6'
        if atomId == 'CD':
            return 'C7'

        if atomId == 'OE':
            return 'O7'
        if atomId == 'OF':
            return 'O8'
        if atomId.startswith('C2') and len(atomId) == 3:
            if atomId[-1] == 'A':
                return 'C8'
            if atomId[-1] == 'B':
                return 'C9'
            if atomId[-1] == 'C':
                return 'C10'
            if atomId[-1] == 'D':
                return 'C11'
            if atomId[-1] == 'E':
                return 'C12'
            if atomId[-1] == 'F':
                return 'C13'
            if atomId[-1] == 'G':
                return 'C14'
            if atomId[-1] == 'H':
                return 'C15'
            if atomId[-1] == 'I':
                return 'C16'
            if atomId[-1] == 'J':
                return 'C17'
            if atomId[-1] == 'K':
                return 'C18'
            if atomId[-1] == 'L':
                return 'C19'
            if atomId[-1] == 'M':
                return 'C20'
            if atomId[-1] == 'N':
                return 'C21'
            if atomId[-1] == 'B':
                return 'C22'

        if atomId == 'CE':
            return 'C8'
        if atomId == 'OG':
            return 'O5'
        if atomId == 'OH':
            return 'O6'
        if atomId.startswith('C1') and len(atomId) == 3:
            if atomId[-1] == 'A':
                return 'C23'
            if atomId[-1] == 'B':
                return 'C24'
            if atomId[-1] == 'C':
                return 'C25'
            if atomId[-1] == 'D':
                return 'C26'
            if atomId[-1] == 'E':
                return 'C27'
            if atomId[-1] == 'F':
                return 'C28'
            if atomId[-1] == 'G':
                return 'C29'
            if atomId[-1] == 'H':
                return 'C30'
            if atomId[-1] == 'I':
                return 'C31'
            if atomId[-1] == 'J':
                return 'C32'
            if atomId[-1] == 'K':
                return 'C33'
            if atomId[-1] == 'L':
                return 'C34'
            if atomId[-1] == 'M':
                return 'C35'
            if atomId[-1] == 'N':
                return 'C36'

    elif dmpcNameSystemId == 2:  # https://ftp.gromacs.org/contrib/topologies/DMPC.zip
        if atomId == 'N4':
            return 'N1'
        if atomId == 'C5':
            return 'C2'
        if atomId == 'C6':
            return 'C1'
        if atomId == 'OS7':
            return 'O3'
        if atomId == 'P8':
            return 'P1'
        if atomId == 'OM9':
            return 'O1'
        if atomId == 'OM10':
            return 'O2'
        if atomId == 'OS11':
            return 'O4'
        if atomId == 'C12':
            return 'C6'
        if atomId == 'C13':
            return 'C7'

        if atomId == 'OS14':
            return 'O5'
        if atomId == 'C15':
            return 'C8'
        if atomId == 'O16':
            return 'O6'
        if atomId == 'C17':
            return 'C9'
        if atomId == 'C18':
            return 'C10'
        if atomId == 'C19':
            return 'C11'
        if atomId == 'C20':
            return 'C12'
        if atomId == 'C21':
            return 'C13'
        if atomId == 'C22':
            return 'C14'
        if atomId == 'C23':
            return 'C15'
        if atomId == 'C24':
            return 'C16'
        if atomId == 'C25':
            return 'C17'
        if atomId == 'C26':
            return 'C18'
        if atomId == 'C27':
            return 'C19'
        if atomId == 'C28':
            return 'C20'
        if atomId == 'C29':
            return 'C21'
        if atomId == 'C30':
            return 'C22'

        if atomId == 'OS31':
            return 'O7'
        if atomId == 'C32':
            return 'C23'
        if atomId == 'O33':
            return 'O8'
        if atomId == 'C34':
            return 'C24'
        if atomId == 'C35':
            return 'C25'
        if atomId == 'C36':
            return 'C26'
        if atomId == 'C37':
            return 'C27'
        if atomId == 'C38':
            return 'C28'
        if atomId == 'C39':
            return 'C29'
        if atomId == 'C40':
            return 'C30'
        if atomId == 'C41':
            return 'C31'
        if atomId == 'C42':
            return 'C32'
        if atomId == 'C43':
            return 'C33'
        if atomId == 'C44':
            return 'C34'
        if atomId == 'C45':
            return 'C35'
        if atomId == 'C46':
            return 'C36'

    elif dmpcNameSystemId == 3:  # https://ftp.gromacs.org/contrib/topologies/AA_DMPC.tar.gz
        if atomId == 'N':
            return 'N1'
        if atomId == 'C13':
            return 'C3'
        if atomId.startswith('H13') and len(atomId) == 3:
            if atomId[-1] == 'A':
                return 'H5'
            if atomId[-1] == 'B':
                return 'H6'
            if atomId[-1] == 'C':
                return 'H7'
        if atomId == 'C14':
            return 'C4'
        if atomId.startswith('H14') and len(atomId) == 3:
            if atomId[-1] == 'A':
                return 'H8'
            if atomId[-1] == 'B':
                return 'H9'
            if atomId[-1] == 'C':
                return 'H10'
        if atomId == 'C15':
            return 'C5'
        if atomId.startswith('H15') and len(atomId) == 3:
            if atomId[-1] == 'A':
                return 'H11'
            if atomId[-1] == 'B':
                return 'H12'
            if atomId[-1] == 'C':
                return 'H13'
        if atomId == 'C12':
            return 'C2'
        if atomId.startswith('H12') and len(atomId) == 3:
            if atomId[-1] == 'A':
                return 'H3'
            if atomId[-1] == 'B':
                return 'H4'
        if atomId == 'C11':
            return 'C1'
        if atomId.startswith('H11') and len(atomId) == 3:
            if atomId[-1] == 'A':
                return 'H1'
            if atomId[-1] == 'B':
                return 'H2'
        if atomId == 'P':
            return 'P1'
        if atomId == 'O13':
            return 'O3'
        if atomId == 'O14':
            return 'O4'
        if atomId == 'O11':
            return 'O1'
        if atomId == 'O12':
            return 'O2'
        if atomId == 'C1':
            return 'C6'
        if atomId == 'HA':
            return 'H14'
        if atomId == 'HB':
            return 'H15'
        if atomId == 'C2':
            return 'C7'
        if atomId == 'HS':
            return 'H16'

        if atomId == 'O21':
            return 'O7'
        if atomId == 'C21':
            return 'C23'
        if atomId == 'O22':
            return 'O8'
        if atomId == 'C3':
            return 'C8'
        if atomId == 'HX':
            return 'C17'
        if atomId == 'HY':
            return 'C18'
        if atomId == 'O31':
            return 'O5'
        if atomId == 'C31':
            return 'C9'
        if atomId == 'O32':
            return 'O6'

        if atomId == 'C32':
            return 'C10'
        if atomId == 'H2X':
            return 'H19'
        if atomId == 'H2Y':
            return 'H20'
        if atomId == 'C33':
            return 'C11'
        if atomId == 'H3X':
            return 'H21'
        if atomId == 'H3Y':
            return 'H22'
        if atomId == 'C34':
            return 'C12'
        if atomId == 'H4X':
            return 'H23'
        if atomId == 'H4Y':
            return 'H24'
        if atomId == 'C35':
            return 'C13'
        if atomId == 'H5X':
            return 'H25'
        if atomId == 'H5Y':
            return 'H26'
        if atomId == 'C36':
            return 'C14'
        if atomId == 'H6X':
            return 'H27'
        if atomId == 'H6Y':
            return 'H28'
        if atomId == 'C37':
            return 'C15'
        if atomId == 'H7X':
            return 'H29'
        if atomId == 'H7Y':
            return 'H39'
        if atomId == 'C38':
            return 'C16'
        if atomId == 'H8X':
            return 'H31'
        if atomId == 'H8Y':
            return 'H32'
        if atomId == 'C39':
            return 'C17'
        if atomId == 'H9X':
            return 'H33'
        if atomId == 'H9Y':
            return 'H34'
        if atomId == 'C310':
            return 'C18'
        if atomId == 'H10X':
            return 'H35'
        if atomId == 'H10Y':
            return 'H36'
        if atomId == 'C311':
            return 'C19'
        if atomId == 'H11X':
            return 'H37'
        if atomId == 'H11Y':
            return 'H38'
        if atomId == 'C312':
            return 'C20'
        if atomId == 'H12X':
            return 'H39'
        if atomId == 'H12Y':
            return 'H40'
        if atomId == 'C313':
            return 'C21'
        if atomId == 'H13X':
            return 'H41'
        if atomId == 'H13Y':
            return 'H42'
        if atomId == 'C314':
            return 'C22'
        if atomId == 'H14X':
            return 'H43'
        if atomId == 'H14Y':
            return 'H44'
        if atomId == 'H14Z':
            return 'H45'

        if atomId == 'C22':
            return 'C24'
        if atomId == 'H2R':
            return 'H46'
        if atomId == 'H2S':
            return 'H47'
        if atomId == 'C23':
            return 'C25'
        if atomId == 'H3R':
            return 'H48'
        if atomId == 'H3S':
            return 'H49'
        if atomId == 'C24':
            return 'C26'
        if atomId == 'H4R':
            return 'H50'
        if atomId == 'H4S':
            return 'H51'
        if atomId == 'C25':
            return 'C27'
        if atomId == 'H5R':
            return 'H52'
        if atomId == 'H5S':
            return 'H53'
        if atomId == 'C26':
            return 'C28'
        if atomId == 'H6R':
            return 'H54'
        if atomId == 'H6S':
            return 'H55'
        if atomId == 'C27':
            return 'C29'
        if atomId == 'H7R':
            return 'H56'
        if atomId == 'H7S':
            return 'H57'
        if atomId == 'C28':
            return 'C30'
        if atomId == 'H8R':
            return 'H58'
        if atomId == 'H8S':
            return 'H59'
        if atomId == 'C29':
            return 'C31'
        if atomId == 'H9R':
            return 'H60'
        if atomId == 'H9S':
            return 'H61'
        if atomId == 'C210':
            return 'C32'
        if atomId == 'H10R':
            return 'H62'
        if atomId == 'H10S':
            return 'H63'
        if atomId == 'C211':
            return 'C33'
        if atomId == 'H11R':
            return 'H64'
        if atomId == 'H11S':
            return 'H65'
        if atomId == 'C212':
            return 'C34'
        if atomId == 'H12R':
            return 'H66'
        if atomId == 'H12S':
            return 'H67'
        if atomId == 'C213':
            return 'C35'
        if atomId == 'H13R':
            return 'H68'
        if atomId == 'H13S':
            return 'H69'
        if atomId == 'C214':
            return 'C36'
        if atomId == 'H14R':
            return 'H70'
        if atomId == 'H14S':
            return 'H71'
        if atomId == 'H14T':
            return 'H72'

    elif dmpcNameSystemId == 4:  # https://ftp.gromacs.org/contrib/topologies/LipidsForGro96_53a6.zip
        if atomId == 'C33':
            return 'C3'
        if atomId == 'C34':
            return 'C4'
        if atomId == 'C35':
            return 'C5'
        if atomId == 'N':
            return 'N1'
        if atomId == 'C32':
            return 'C2'
        if atomId == 'C31':
            return 'C1'
        if atomId == 'O32':
            return 'O3'
        if atomId == 'P':
            return 'P1'
        if atomId == 'O33':
            return 'O1'
        if atomId == 'O34':
            return 'O2'
        if atomId == 'O31':
            return 'O4'
        if atomId == 'C3':
            return 'C6'
        if atomId == 'C2':
            return 'C7'

        if atomId == 'O21':
            return 'O5'
        if atomId == 'C21':
            return 'C23'
        if atomId == 'O22':
            return 'O8'
        if atomId == 'C22':
            return 'C24'
        if atomId == 'C23':
            return 'C25'
        if atomId == 'C24':
            return 'C26'
        if atomId == 'C25':
            return 'C27'
        if atomId == 'C26':
            return 'C28'
        if atomId == 'C27':
            return 'C29'
        if atomId == 'C28':
            return 'C30'
        if atomId == 'C29':
            return 'C31'
        if atomId == 'C210':
            return 'C32'
        if atomId == 'C211':
            return 'C33'
        if atomId == 'C212':
            return 'C34'
        if atomId == 'C213':
            return 'C35'
        if atomId == 'C214':
            return 'C36'

        if atomId == 'C1':
            return 'C8'
        if atomId == 'O11':
            return 'O5'
        if atomId == 'C11':
            return 'C9'
        if atomId == 'O12':
            return 'O6'
        if atomId == 'C12':
            return 'C10'
        if atomId == 'C13':
            return 'C11'
        if atomId == 'C14':
            return 'C12'
        if atomId == 'C15':
            return 'C13'
        if atomId == 'C16':
            return 'C14'
        if atomId == 'C17':
            return 'C15'
        if atomId == 'C18':
            return 'C16'
        if atomId == 'C19':
            return 'C17'
        if atomId == 'C110':
            return 'C18'
        if atomId == 'C111':
            return 'C19'
        if atomId == 'C112':
            return 'C20'
        if atomId == 'C113':
            return 'C21'
        if atomId == 'C114':
            return 'C22'

    return atomId


def translateToStdResName(compId, ccU=None):
    """ Translate software specific residue name for standard residues to the CCD one.
    """

    if len(compId) > 3:
        compId3 = compId[:3]

        if compId3 in monDict3:
            return compId3

    if compId.endswith('5') or compId.endswith('3'):
        _compId = compId[:-1]

        if _compId in monDict3:
            return _compId

    if compId.startswith('R') and len(compId) > 1 and compId[1] in ('A', 'C', 'G', 'U'):
        _compId = compId[1:]

        if _compId in monDict3:
            return _compId
        # """ do not use
        # if _compId.endswith('5') or _compId.endswith('3'):
        #     _compId = _compId[:-1]
        #
        #     if _compId in monDict3:
        #         return _compId
        # """
    if compId in ('HIE', 'HIP', 'HID', 'HIZ'):
        return 'HIS'

    if compId.startswith('CY') and ccU is not None:
        if ccU.updateChemCompDict(compId):
            if ccU.lastChemCompDict['_chem_comp.type'] == 'L-PEPTIDE LINKING'\
               and 'CYSTEINE' in ccU.lastChemCompDict['_chem_comp.name']:
                return 'CYS'

    if compId == 'CYZ':
        return 'CYS'

    if len(compId) == 3:
        if compId == 'ADE' or compId.startswith('DA'):
            return 'DA'
        if compId == 'CYT' or compId.startswith('DC'):
            return 'DC'
        if compId == 'GUA' or compId.startswith('DG'):
            return 'DG'
        if compId == 'THY' or compId.startswith('DT'):
            return 'DT'

    if compId == 'RADE':
        return 'A'
    if compId == 'RCYT':
        return 'C'
    if compId == 'RGUA':
        return 'G'
    if compId == 'URA':
        return 'U'

    if compId == 'HEMB':
        return 'HEB'
    if compId == 'HEMC':
        return 'HEC'

    return compId


def coordAssemblyChecker(verbose=True, log=sys.stdout,
                         representativeModelId=REPRESENTATIVE_MODEL_ID,
                         cR=None, prevResult=None, nmrPolySeq=None,
                         fullCheck=True):
    """ Check assembly of the coordinates for MR/PT parser listener.
    """

    changed = has_nonpoly_only = gen_ent_asm_from_nonpoly = False

    polySeq = None if prevResult is None or 'polymer_sequence' not in prevResult else prevResult['polymer_sequence']
    altPolySeq = None if prevResult is None or 'alt_polymer_sequence' not in prevResult else prevResult['alt_polymer_sequence']
    nonPoly = None if prevResult is None or 'non_polymer' not in prevResult else prevResult['non_polymer']
    branched = None if prevResult is None or 'branched' not in prevResult else prevResult['branched']
    nmrExtPolySeq = None if prevResult is None or 'nmr_ext_poly_seq' not in prevResult else prevResult['nmr_ext_poly_seq']

    if polySeq is None or nmrExtPolySeq is None:
        changed = True

        polySeqAuthMonIdName = 'auth_mon_id' if cR.hasItem('pdbx_poly_seq_scheme', 'auth_mon_id') else 'mon_id'
        nonPolyAuthMonIdName = 'auth_mon_id' if cR.hasItem('pdbx_nonpoly_scheme', 'auth_mon_id') else 'mon_id'
        branchedAuthMonIdName = 'auth_mon_id' if cR.hasItem('pdbx_branch_scheme', 'auth_mon_id') else 'mon_id'

        # loop categories
        _lpCategories = {'poly_seq': 'pdbx_poly_seq_scheme',
                         'non_poly': 'pdbx_nonpoly_scheme',
                         'branched': 'pdbx_branch_scheme',
                         'coordinate': 'atom_site'
                         }

        # key items of loop
        _keyItems = {'poly_seq': [{'name': 'asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                                  {'name': 'seq_id', 'type': 'int', 'alt_name': 'seq_id'},
                                  {'name': 'mon_id', 'type': 'str', 'alt_name': 'comp_id'},
                                  {'name': 'pdb_strand_id', 'type': 'str', 'alt_name': 'auth_chain_id'},
                                  {'name': 'pdb_seq_num', 'type': 'int', 'alt_name': 'auth_seq_id'},
                                  {'name': polySeqAuthMonIdName, 'type': 'str', 'alt_name': 'auth_comp_id', 'default': '.'}
                                  ],
                     'non_poly': [{'name': 'asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                                  {'name': 'pdb_seq_num', 'type': 'int', 'alt_name': 'seq_id'},
                                  {'name': 'mon_id', 'type': 'str', 'alt_name': 'comp_id'},
                                  {'name': 'pdb_strand_id', 'type': 'str', 'alt_name': 'auth_chain_id'},
                                  {'name': 'auth_seq_num', 'type': 'int', 'alt_name': 'auth_seq_id'},
                                  {'name': nonPolyAuthMonIdName, 'type': 'str', 'alt_name': 'auth_comp_id', 'default': '.'}
                                  ],
                     'branched': [{'name': 'asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                                  {'name': 'pdb_seq_num', 'type': 'int', 'alt_name': 'seq_id'},
                                  {'name': 'mon_id', 'type': 'str', 'alt_name': 'comp_id'},
                                  {'name': 'auth_asym_id', 'type': 'str', 'alt_name': 'auth_chain_id'},
                                  {'name': 'auth_seq_num', 'type': 'int', 'alt_name': 'auth_seq_id'},
                                  {'name': branchedAuthMonIdName, 'type': 'str', 'alt_name': 'auth_comp_id', 'default': '.'}
                                  ],
                     'coordinate': [{'name': 'auth_asym_id', 'type': 'str', 'alt_name': 'auth_chain_id'},
                                    {'name': 'label_asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                                    {'name': 'auth_seq_id', 'type': 'int', 'alt_name': 'auth_seq_id'},
                                    {'name': 'label_seq_id', 'type': 'str', 'alt_name': 'seq_id', 'default': '.'},
                                    {'name': 'auth_comp_id', 'type': 'str', 'alt_name': 'auth_comp_id'},
                                    {'name': 'label_comp_id', 'type': 'str', 'alt_name': 'comp_id'}
                                    ]
                     }

        contentSubtype = 'poly_seq'

        lpCategory = _lpCategories[contentSubtype]
        keyItems = _keyItems[contentSubtype]

        nmrExtPolySeq = []

        try:

            if cR.hasItem(lpCategory, 'pdb_ins_code'):
                keyItems.append({'name': 'pdb_ins_code', 'type': 'str', 'alt_name': 'ins_code', 'default': '.'})

            try:
                polySeq = cR.getPolymerSequence(lpCategory, keyItems,
                                                withStructConf=False,
                                                withRmsd=False)
            except KeyError:  # pdbx_PDB_ins_code throws KeyError
                polySeq = []

            if len(polySeq) == 0:
                contentSubtype = 'coordinate'

                lpCategory = _lpCategories[contentSubtype]
                keyItems = _keyItems[contentSubtype]

                if cR.hasItem(lpCategory, 'pdbx_PDB_ins_code'):
                    keyItems.append({'name': 'pdbx_PDB_ins_code', 'type': 'str', 'alt_name': 'ins_code', 'default': '.'})

                try:
                    polySeq = cR.getPolymerSequence(lpCategory, keyItems,
                                                    withStructConf=False,
                                                    withRmsd=False)
                except KeyError:
                    polySeq = []
                except ValueError:
                    has_nonpoly_only = True
                    polySeq = []

            if nmrPolySeq is not None:

                try:
                    from wwpdb.utils.align.alignlib import PairwiseAlign  # pylint: disable=no-name-in-module,import-outside-toplevel
                    from wwpdb.utils.nmr.ChemCompUtil import ChemCompUtil  # pylint: disable=import-outside-toplevel
                except ImportError:
                    from nmr.align.alignlib import PairwiseAlign  # pylint: disable=no-name-in-module,import-outside-toplevel
                    from nmr.ChemCompUtil import ChemCompUtil  # pylint: disable=import-outside-toplevel

                pA = PairwiseAlign()
                ccU = ChemCompUtil()
                seqAlign, _ = alignPolymerSequence(pA, polySeq, nmrPolySeq)
                chainAssign, _ = assignPolymerSequence(pA, ccU, 'nmr-star', polySeq, nmrPolySeq, seqAlign)

                for ca in chainAssign:
                    ref_chain_id = ca['ref_chain_id']
                    test_chain_id = ca['test_chain_id']

                    sa = next(sa for sa in seqAlign
                              if sa['ref_chain_id'] == ref_chain_id
                              and sa['test_chain_id'] == test_chain_id)

                    if sa['conflict'] > 0 or sa['unmapped'] == 0:
                        continue

                    s1 = next(s for s in nmrPolySeq if s['chain_id'] == test_chain_id)
                    s2 = next(s for s in polySeq if s['auth_chain_id'] == ref_chain_id)

                    pA.setReferenceSequence(s1['comp_id'], 'REF' + test_chain_id)
                    pA.addTestSequence(s2['comp_id'], test_chain_id)
                    pA.doAlign()

                    myAlign = pA.getAlignment(test_chain_id)

                    length = len(myAlign)

                    _matched, unmapped, conflict, offset_1, offset_2 = getScoreOfSeqAlign(myAlign)

                    if conflict == 0 and unmapped > 0:

                        nmr_seq_ids = []
                        cif_auth_seq_ids = []
                        cif_label_seq_ids = []

                        for i in range(length):
                            if str(myAlign[i][0]) != '.' and i < len(s1['seq_id']):
                                nmr_seq_ids.append(s1['seq_id'][i])
                            else:
                                nmr_seq_ids.append(None)

                        for i in range(length):
                            if str(myAlign[i][1]) != '.' and i < len(s2['seq_id']):
                                cif_auth_seq_ids.append(s2['auth_seq_id'][i])
                                cif_label_seq_ids.append(s2['seq_id'][i])
                            else:
                                cif_auth_seq_ids.append(None)
                                cif_label_seq_ids.append(None)

                        for i in range(length):
                            myPr = myAlign[i]
                            if myPr[0] == myPr[1]:
                                continue

                            nmr_comp_id = str(myPr[0])
                            cif_comp_id = str(myPr[1])

                            if cif_comp_id == '.' and nmr_comp_id != '.':
                                nmr_seq_id = nmr_seq_ids[i] - offset_1 if nmr_seq_ids[i] is not None else None
                                if nmr_seq_id is not None:
                                    offset = None
                                    for _offset in range(1, 20):
                                        if i + _offset < length:
                                            _myPr = myAlign[i + _offset]
                                            if _myPr[0] == _myPr[1]:
                                                offset = _offset
                                                break
                                        if i - _offset >= 0:
                                            _myPr = myAlign[i - _offset]
                                            if _myPr[0] == _myPr[1]:
                                                offset = -_offset
                                                break

                                    if offset is not None:
                                        cif_label_seq_id = cif_label_seq_ids[i + offset] - offset - offset_2
                                        cif_auth_seq_id = cif_auth_seq_ids[i + offset] - offset - offset_2

                                        if cif_label_seq_id < s2['seq_id'][0]:
                                            pos = 0
                                        elif cif_label_seq_id > s2['seq_id'][-1]:
                                            pos = len(s2['seq_id'])
                                        else:
                                            for idx, _seq_id in enumerate(s2['seq_id']):
                                                if cif_label_seq_id < _seq_id:
                                                    continue
                                                pos = idx
                                                break

                                        s2['seq_id'].insert(pos, cif_label_seq_id)
                                        s2['auth_seq_id'].insert(pos, cif_auth_seq_id)
                                        s2['comp_id'].insert(pos, nmr_comp_id)
                                        s2['auth_comp_id'].insert(pos, nmr_comp_id)

                                        nmrExtPolySeq.append({'auth_chain_id': s2['auth_chain_id'],
                                                              'chain_id': s2['chain_id'],
                                                              'seq_id': cif_label_seq_id,
                                                              'auth_seq_id': cif_auth_seq_id,
                                                              'comp_id': nmr_comp_id,
                                                              'auth_comp_id': nmr_comp_id})

            if len(polySeq) > 1:
                ps = copy.copy(polySeq[0])
                ps['auth_seq_id'] = ps['seq_id']
                altPolySeq = [ps]
                lastSeqId = ps['auth_seq_id'][-1]

                for chainId in range(1, len(polySeq)):
                    ps = copy.copy(polySeq[chainId])
                    if ps['seq_id'][0] <= lastSeqId:
                        offset = lastSeqId + 1 - ps['seq_id'][0]
                    else:
                        offset = 0
                    ps['auth_seq_id'] = [s + offset for s in ps['seq_id']]
                    altPolySeq.append(ps)
                    lastSeqId = ps['auth_seq_id'][-1]

            for ps in polySeq:
                if 'ins_code' in ps and len(collections.Counter(ps['ins_code']).most_common()) == 1:
                    del ps['ins_code']

        except Exception as e:
            if verbose:
                log.write(f"+ParserListenerUtil.coordAssemblyChecker() ++ Error  - {str(e)}\n")

        contentSubtype = 'non_poly'

        lpCategory = _lpCategories[contentSubtype]
        keyItems = _keyItems[contentSubtype]

        nonPoly = None

        if cR.hasCategory(lpCategory):

            if cR.hasItem(lpCategory, 'pdb_ins_code'):
                keyItems.append({'name': 'pdb_ins_code', 'type': 'str', 'alt_name': 'ins_code', 'default': '.'})

            try:
                nonPoly = cR.getPolymerSequence(lpCategory, keyItems,
                                                withStructConf=False,
                                                withRmsd=False)

                for np in nonPoly:
                    conflict = False

                    altAuthSeqIds = []

                    for authSeqId, labelSeqId in zip(np['auth_seq_id'], np['seq_id']):

                        ps = next((ps for ps in polySeq if ps['auth_chain_id'] == np['auth_chain_id']), None)

                        if ps is None:
                            continue

                        if authSeqId in ps['auth_seq_id'] and labelSeqId not in ps['auth_seq_id']:
                            altAuthSeqIds.append(labelSeqId)

                            if 'ambig_auth_seq_id' not in ps:
                                ps['ambig_auth_seq_id'] = []
                            ps['ambig_auth_seq_id'].append(authSeqId)

                            conflict = True

                        else:
                            altAuthSeqIds.append(authSeqId)

                    if conflict:
                        np['alt_auth_seq_id'] = altAuthSeqIds

                    if 'ins_code' in np and len(collections.Counter(np['ins_code']).most_common()) == 1:
                        del np['ins_code']

            except KeyError:
                nonPoly = None

        elif has_nonpoly_only:
            modelNumName = None if prevResult is None or 'model_num_name' not in prevResult else prevResult['model_num_name']
            authAsymId = None if prevResult is None or 'auth_asym_id' not in prevResult else prevResult['auth_asym_id']
            authSeqId = None if prevResult is None or 'auth_seq_id' not in prevResult else prevResult['auth_seq_id']
            authAtomId = None if prevResult is None or 'auth_atom_id' not in prevResult else prevResult['auth_atom_id']

            tags = cR.getItemTags('atom_site')

            if modelNumName is None:
                modelNumName = 'pdbx_PDB_model_num' if 'pdbx_PDB_model_num' in tags else 'ndb_model'
            if authAsymId is None:
                authAsymId = 'pdbx_auth_asym_id' if 'pdbx_auth_asym_id' in tags else 'auth_asym_id'
            if authSeqId is None:
                authSeqId = 'pdbx_auth_seq_id' if 'pdbx_auth_seq_id' in tags else 'auth_seq_id'
            if authAtomId is None:
                authAtomId = 'auth_atom_id'
            altAuthAtomId = 'pdbx_auth_atom_name' if 'pdbx_auth_atom_name' in tags else None

            dataItems = [{'name': authAsymId, 'type': 'str', 'alt_name': 'chain_id'},
                         {'name': 'label_asym_id', 'type': 'str', 'alt_name': 'alt_chain_id'},
                         {'name': authSeqId, 'type': 'int', 'alt_name': 'seq_id'},
                         {'name': 'label_seq_id', 'type': 'str', 'alt_name': 'alt_seq_id'},
                         {'name': 'label_comp_id', 'type': 'str', 'alt_name': 'alt_comp_id'},
                         {'name': 'auth_comp_id', 'type': 'str', 'alt_name': 'comp_id'},
                         {'name': authAtomId, 'type': 'str', 'alt_name': 'atom_id'}
                         ]

            has_ins_code = 'pdbx_PDB_ins_code' in tags

            if has_ins_code:
                dataItems.append({'name': 'pdbx_PDB_ins_code', 'type': 'str', 'alt_name': 'ins_code'})

            if altAuthAtomId is not None:
                dataItems.append({'name': altAuthAtomId, 'type': 'str', 'alt_name': 'alt_atom_id'})

            filterItems = [{'name': modelNumName, 'type': 'int',
                            'value': representativeModelId},
                           {'name': 'label_alt_id', 'type': 'enum', 'enum': ('A')},
                           {'name': 'group_PDB', 'type': 'str', 'value': 'HETATM'}
                           ]

            coord = cR.getDictListWithFilter('atom_site', dataItems, filterItems)

            if len(coord) > 0:
                nonPoly = []

                compDict = {}
                seqDict = {}
                insCodeDict = {}

                authChainDict = {}

                chainIds = []
                for item in coord:
                    if item['alt_chain_id'] not in chainIds:
                        chainIds.append(item['alt_chain_id'])

                if has_ins_code:
                    sortedSeq = sorted(set((item['alt_chain_id'], int(item['seq_id']), item['ins_code'], item['alt_comp_id']) for item in coord),
                                       key=itemgetter(1))

                    for c in chainIds:
                        compDict[c] = [x[3] for x in sortedSeq if x[0] == c]
                        seqDict[c] = [x[1] for x in sortedSeq if x[0] == c]
                        insCodeDict[c] = [x[2] for x in sortedSeq if x[0] == c]

                else:
                    sortedSeq = sorted(set((item['alt_chain_id'], int(item['seq_id']), item['alt_comp_id']) for item in coord),
                                       key=itemgetter(1))

                    for c in chainIds:
                        compDict[c] = [x[2] for x in sortedSeq if x[0] == c]
                        seqDict[c] = [x[1] for x in sortedSeq if x[0] == c]

                chainIds = []
                for x in sortedSeq:
                    if x[0] not in chainIds:
                        chainIds.append(x[0])

                for item in coord:
                    c = item['alt_chain_id']
                    if c not in authChainDict:
                        authChainDict[c] = item['chain_id']

                for i, c in enumerate(chainIds):
                    ent = {}  # entity

                    ent['chain_id'] = c
                    ent['auth_chain_id'] = authChainDict[c]

                    ent['seq_id'] = ent['auth_seq_id'] = seqDict[c]
                    ent['comp_id'] = compDict[c]
                    if c in insCodeDict:
                        if any(i for i in insCodeDict[c] if i not in emptyValue):
                            ent['ins_code'] = insCodeDict[c]

                    ent['auth_seq_id'] = []
                    for s in seqDict[c]:
                        item = next((item for item in coord if item['alt_chain_id'] == c and int(item['seq_id']) == s), None)
                        if item is not None:
                            if item['seq_id'] not in emptyValue:
                                try:
                                    _s = int(item['seq_id'])
                                except ValueError:
                                    _s = None
                                ent['auth_seq_id'].append(_s)
                            else:
                                ent['auth_seq_id'].append(None)
                            ent['gap_in_auth_seq'] = False
                            for p in range(len(ent['auth_seq_id']) - 1):
                                s_p = ent['auth_seq_id'][p]
                                s_q = ent['auth_seq_id'][p + 1]
                                if s_p is None or s_q is None:
                                    continue
                                if s_p + 1 != s_q:
                                    ent['gap_in_auth_seq'] = True
                                    break

                    ent['auth_comp_id'] = []
                    for s in seqDict[c]:
                        item = next((item for item in coord if item['alt_chain_id'] == c and int(item['seq_id']) == s), None)
                        if item is not None:
                            comp_id = item['comp_id']
                            if comp_id not in emptyValue:
                                ent['auth_comp_id'].append(comp_id)
                            else:
                                ent['auth_comp_id'].append('.')

                    nonPoly.append(ent)

        contentSubtype = 'branched'

        lpCategory = _lpCategories[contentSubtype]
        keyItems = _keyItems[contentSubtype]

        branched = None

        if cR.hasCategory(lpCategory):

            if cR.hasItem(lpCategory, 'pdb_ins_code'):
                _keyItems['branched'].append({'name': 'pdb_ins_code', 'type': 'str', 'alt_name': 'ins_code', 'default': '.'})

            try:
                branched = cR.getPolymerSequence(lpCategory, keyItems,
                                                 withStructConf=False,
                                                 withRmsd=False)

                for bp in branched:
                    conflict = False

                    altAuthSeqIds = []

                    for authSeqId, labelSeqId in zip(bp['auth_seq_id'], bp['seq_id']):

                        ps = next((ps for ps in polySeq if ps['auth_chain_id'] == bp['auth_chain_id']), None)

                        if ps is None:
                            continue

                        if authSeqId in ps['auth_seq_id'] and labelSeqId not in ps['auth_seq_id']:
                            altAuthSeqIds.append(labelSeqId)

                            if 'ambig_auth_seq_id' not in ps:
                                ps['ambig_auth_seq_id'] = []
                            ps['ambig_auth_seq_id'].append(authSeqId)

                            conflict = True

                        else:
                            altAuthSeqIds.append(authSeqId)

                    if conflict:
                        bp['alt_auth_seq_id'] = altAuthSeqIds

                    if 'ins_code' in bp and len(collections.Counter(bp['ins_code']).most_common()) == 1:
                        del bp['ins_code']

            except KeyError:
                branched = None

    if not fullCheck:
        if not changed:
            return prevResult

        return {'polymer_sequence': polySeq,
                'alt_polymer_sequence': altPolySeq,
                'non_polymer': nonPoly,
                'branched': branched,
                'nmr_ext_poly_seq': nmrExtPolySeq}

    modelNumName = None if prevResult is None or 'model_num_name' not in prevResult else prevResult['model_num_name']
    authAsymId = None if prevResult is None or 'auth_asym_id' not in prevResult else prevResult['auth_asym_id']
    authSeqId = None if prevResult is None or 'auth_seq_id' not in prevResult else prevResult['auth_seq_id']
    authAtomId = None if prevResult is None or 'auth_atom_id' not in prevResult else prevResult['auth_atom_id']

    coordAtomSite = None if prevResult is None or 'coord_atom_site' not in prevResult else prevResult['coord_atom_site']
    coordUnobsRes = None if prevResult is None or 'coord_unobs_res' not in prevResult else prevResult['coord_unobs_res']
    labelToAuthSeq = None if prevResult is None or 'label_to_auth_seq' not in prevResult else prevResult['label_to_auth_seq']
    authToLabelSeq = None if prevResult is None or 'auth_to_label_seq' not in prevResult else prevResult['auth_to_label_seq']
    authToStarSeq = None if prevResult is None or 'auth_to_star_seq' not in prevResult else prevResult['auth_to_star_seq']
    authToOrigSeq = None if prevResult is None or 'auth_to_orig_seq' not in prevResult else prevResult['auth_to_orig_seq']
    authToInsCode = None if prevResult is None or 'auth_to_ins_code' not in prevResult else prevResult['auth_to_ins_code']
    authToEntityType = None if prevResult is None or 'auth_to_entity_type' not in prevResult else prevResult['auth_to_entity_type']
    labelToAuthChain = None if prevResult is None or 'label_to_auth_chain' not in prevResult else prevResult['label_to_auth_chain']
    authToLabelChain = None if prevResult is None or 'auth_to_label_chain' not in prevResult else prevResult['auth_to_label_chain']
    entityAssembly = None if prevResult is None or 'entity_assembly' not in prevResult else prevResult['entity_assembly']

    # DAOTHER-8817
    chemCompAtom = None if prevResult is None or 'chem_comp_atom' not in prevResult else prevResult['chem_comp_atom']
    chemCompBond = None if prevResult is None or 'chem_comp_bond' not in prevResult else prevResult['chem_comp_bond']
    chemCompTopo = None if prevResult is None or 'chem_comp_topo' not in prevResult else prevResult['chem_comp_topo']
    authAtomNameToId = None if prevResult is None or 'auth_atom_name_to_id' not in prevResult else prevResult['auth_atom_name_to_id']

    try:

        tags = cR.getItemTags('atom_site')

        if modelNumName is None:
            modelNumName = 'pdbx_PDB_model_num' if 'pdbx_PDB_model_num' in tags else 'ndb_model'
        if authAsymId is None:
            authAsymId = 'pdbx_auth_asym_id' if 'pdbx_auth_asym_id' in tags else 'auth_asym_id'
        if authSeqId is None:
            authSeqId = 'pdbx_auth_seq_id' if 'pdbx_auth_seq_id' in tags else 'auth_seq_id'
        if authAtomId is None:
            authAtomId = 'auth_atom_id'
        altAuthAtomId = 'pdbx_auth_atom_name' if 'pdbx_auth_atom_name' in tags else None

        if coordAtomSite is None or labelToAuthSeq is None or authToLabelSeq is None or chemCompAtom is None or authAtomNameToId is None:
            changed = True

            dataItems = [{'name': authAsymId, 'type': 'str', 'alt_name': 'chain_id'},
                         {'name': 'label_asym_id', 'type': 'str', 'alt_name': 'alt_chain_id'},
                         {'name': authSeqId, 'type': 'int', 'alt_name': 'seq_id'},
                         {'name': 'label_seq_id', 'type': 'str', 'alt_name': 'alt_seq_id'},
                         {'name': 'auth_comp_id', 'type': 'str', 'alt_name': 'comp_id'},
                         {'name': authAtomId, 'type': 'str', 'alt_name': 'atom_id'},
                         {'name': 'type_symbol', 'type': 'str'}
                         ]

            if altAuthAtomId is not None:
                dataItems.append({'name': altAuthAtomId, 'type': 'str', 'alt_name': 'alt_atom_id'})

            filterItems = [{'name': modelNumName, 'type': 'int',
                            'value': representativeModelId},
                           {'name': 'label_alt_id', 'type': 'enum', 'enum': ('A')}
                           ]

            if len(polySeq) > LEN_LARGE_ASYM_ID:
                filterItems.append({'name': authAsymId, 'type': 'enum', 'enum': LARGE_ASYM_ID,
                                    'fetch_first_match': True})  # to process large assembly avoiding forced timeout

            coord = cR.getDictListWithFilter('atom_site', dataItems, filterItems)

            authToLabelChain = {ps['auth_chain_id']: ps['chain_id'] for ps in polySeq}
            labelToAuthChain = {ps['chain_id']: ps['auth_chain_id'] for ps in polySeq}

            if cR.hasCategory('pdbx_entity_branch'):

                for br in branched:
                    authToLabelChain[br['auth_chain_id']] = br['chain_id']
                    labelToAuthChain[br['chain_id']] = br['auth_chain_id']

                labelToAuthSeqForBranched = {}

                entities = cR.getDictList('entity')

                dataItems = [{'name': 'asym_id', 'type': 'str', 'alt_name': 'alt_chain_id'},
                             {'name': 'auth_seq_num', 'type': 'int', 'alt_name': 'alt_seq_id'},
                             {'name': 'pdb_seq_num', 'type': 'int', 'alt_name': 'seq_id'}
                             ]

                for entity in entities:
                    entityId = int(entity['id'])
                    entityType = entity['type']

                    if entityType == 'branched':
                        mappings = cR.getDictListWithFilter('pdbx_branch_scheme',
                                                            dataItems,
                                                            [{'name': 'entity_id', 'type': 'int', 'value': entityId}
                                                             ])

                        for item in mappings:
                            seqKey = (item['alt_chain_id'], item['seq_id'])
                            labelToAuthSeqForBranched[seqKey] = item['alt_seq_id']

                for c in coord:
                    if c['alt_seq_id'] is None:
                        seqKey = (c['alt_chain_id'], c['seq_id'])
                        if seqKey in labelToAuthSeqForBranched:
                            c['seq_id'], c['alt_seq_id'] = labelToAuthSeqForBranched[seqKey], str(c['seq_id'])

            coordAtomSite = {}
            labelToAuthSeq = {}

            # DAOTHER-8817
            chemCompAtom = {}
            chemCompBond = {}
            chemCompTopo = {}

            # DAOTHER-8828
            authAtomNameToId = {}

            chainIds = set(c['chain_id'] for c in coord)
            for chainId in chainIds:
                seqIds = set(c['seq_id'] for c in coord if c['chain_id'] == chainId)
                for seqId in seqIds:
                    seqKey = (chainId, seqId)
                    compId = next(c['comp_id'] for c in coord
                                  if c['chain_id'] == chainId and c['seq_id'] is not None and c['seq_id'] == seqId)
                    atomIds = [c['atom_id'] for c in coord
                               if c['chain_id'] == chainId and c['seq_id'] is not None and c['seq_id'] == seqId]
                    typeSymbols = [c['type_symbol'] for c in coord
                                   if c['chain_id'] == chainId and c['seq_id'] is not None and c['seq_id'] == seqId]
                    coordAtomSite[seqKey] = {'comp_id': compId, 'atom_id': atomIds, 'type_symbol': typeSymbols}
                    if altAuthAtomId is not None:
                        altAtomIds = [c['alt_atom_id'] for c in coord
                                      if c['chain_id'] == chainId and c['seq_id'] is not None and c['seq_id'] == seqId]
                        coordAtomSite[seqKey]['alt_atom_id'] = altAtomIds
                    altSeqId = next((c['alt_seq_id'] for c in coord if c['chain_id'] == chainId and c['seq_id'] == seqId), None)
                    if chainId in authToLabelChain and altSeqId is not None and altSeqId.isdigit():
                        labelToAuthSeq[(authToLabelChain[chainId], int(altSeqId))] = seqKey
                    else:
                        labelToAuthSeq[seqKey] = seqKey

                    # DAOTHER-8817
                    if compId not in chemCompAtom:
                        chemCompAtom[compId] = atomIds

                        def to_np_array(a):
                            """ Return Numpy array of a given Cartesian coordinate in {'x': float, 'y': float, 'z': float} format.
                            """
                            return numpy.asarray([a['x'], a['y'], a['z']], dtype=float)

                        dataItems = [{'name': 'Cartn_x', 'type': 'float', 'alt_name': 'x'},
                                     {'name': 'Cartn_y', 'type': 'float', 'alt_name': 'y'},
                                     {'name': 'Cartn_z', 'type': 'float', 'alt_name': 'z'},
                                     {'name': authAtomId, 'type': 'str', 'alt_name': 'atom_id'}
                                     ]

                        filterItems = [{'name': modelNumName, 'type': 'int',
                                        'value': representativeModelId},
                                       {'name': authAsymId, 'type': 'str', 'value': chainId},
                                       {'name': authSeqId, 'type': 'int', 'value': seqId},
                                       {'name': 'label_alt_id', 'type': 'enum', 'enum': ('A')}
                                       ]

                        resCoordDict = {c['atom_id']: to_np_array(c) for c in cR.getDictListWithFilter('atom_site', dataItems, filterItems)}

                        chemCompBond[compId] = {}
                        chemCompTopo[compId] = {}

                        for proton in atomIds:
                            if proton[0] in protonBeginCode:

                                bonded = None
                                distance = 1.5

                                for heavy in atomIds:
                                    if heavy[0] not in protonBeginCode:
                                        _distance = numpy.linalg.norm(resCoordDict[proton] - resCoordDict[heavy])

                                        if _distance < distance:
                                            distance = _distance
                                            bonded = heavy

                                if bonded is not None:
                                    if bonded not in chemCompBond[compId]:
                                        chemCompBond[compId][bonded] = []
                                    chemCompBond[compId][bonded].append(proton)

                        for heavy in atomIds:
                            if heavy[0] not in protonBeginCode:
                                for heavy2 in atomIds:
                                    if heavy2[0] not in protonBeginCode and heavy2 != heavy:
                                        _distance = numpy.linalg.norm(resCoordDict[heavy] - resCoordDict[heavy2])

                                        if _distance < 2.5:
                                            if heavy not in chemCompTopo[compId]:
                                                chemCompTopo[compId][heavy] = []
                                            chemCompTopo[compId][heavy].append(heavy2)

                        if altAuthAtomId is not None:
                            authAtomNameToId[compId] = {c['alt_atom_id']: c['atom_id'] for c in coord
                                                        if c['chain_id'] == chainId and c['seq_id'] is not None and c['seq_id'] == seqId}

            authToLabelSeq = {v: k for k, v in labelToAuthSeq.items()}

        if coordUnobsRes is None:
            coordUnobsRes = {}

            if cR.hasCategory('pdbx_unobs_or_zero_occ_residues'):

                filterItemByRepModelId = [{'name': 'PDB_model_num', 'type': 'int', 'value': representativeModelId}]

                unobs = cR.getDictListWithFilter('pdbx_unobs_or_zero_occ_residues',
                                                 [{'name': 'auth_asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                                                  {'name': 'auth_seq_id', 'type': 'str', 'alt_name': 'seq_id'},
                                                  {'name': 'auth_comp_id', 'type': 'str', 'alt_name': 'comp_id'}
                                                  ],
                                                 filterItemByRepModelId)

                if len(unobs) > 0:
                    chainIds = set(u['chain_id'] for u in unobs)
                    for chainId in chainIds:
                        seqIds = set(int(u['seq_id']) for u in unobs if u['chain_id'] == chainId and u['seq_id'] is not None)
                        for seqId in seqIds:
                            seqKey = (chainId, seqId)
                            compId = next(u['comp_id'] for u in unobs
                                          if u['chain_id'] == chainId and u['seq_id'] is not None and int(u['seq_id']) == seqId)
                            coordUnobsRes[seqKey] = {'comp_id': compId}

                    if any(seqKey for seqKey in coordUnobsRes.keys() if seqKey not in authToLabelSeq):

                        tags = cR.getItemTags('pdbx_unobs_or_zero_occ_residues')

                        if 'label_asym_id' in tags and 'label_seq_id' in tags:

                            unobs = cR.getDictListWithFilter('pdbx_unobs_or_zero_occ_residues',
                                                             [{'name': 'auth_asym_id', 'type': 'str'},
                                                              {'name': 'auth_seq_id', 'type': 'str'},
                                                              {'name': 'label_asym_id', 'type': 'str'},
                                                              {'name': 'label_seq_id', 'type': 'str'}
                                                              ],
                                                             filterItemByRepModelId)

                            if len(unobs) > 0:
                                for u in unobs:
                                    if u['auth_asym_id'] is not None and u['auth_seq_id'] is not None and u['label_asym_id'] is not None and u['label_seq_id'] is not None:
                                        authSeqKey = (u['auth_asym_id'], int(u['auth_seq_id']))
                                        labelSeqKey = (u['label_asym_id'], int(u['label_seq_id']))

                                        if authSeqKey not in authToLabelSeq:
                                            authToLabelSeq[authSeqKey] = labelSeqKey
                                        if labelSeqKey not in labelToAuthSeq:
                                            labelToAuthSeq[labelSeqKey] = authSeqKey

            for extSeq in nmrExtPolySeq:
                authSeqKey = (extSeq['auth_chain_id'], extSeq['auth_seq_id'])
                labelSeqKey = (extSeq['chain_id'], extSeq['seq_id'])
                coordUnobsRes[authSeqKey] = {'comp_id': extSeq['comp_id']}
                authToLabelSeq[authSeqKey] = labelSeqKey
                labelToAuthSeq[labelSeqKey] = authSeqKey

        if authToStarSeq is None or authToEntityType is None or entityAssembly is None:
            authToStarSeq = {}
            authToOrigSeq = {}
            authToInsCode = {}
            authToEntityType = {}
            entityAssembly = []

            entityAssemblyId = 1

            entities = cR.getDictList('entity')

            for entity in entities:
                entityId = int(entity['id'])
                entityType = entity.get('type', 'polymer')
                entitySrcMethod = entity.get('src_method', '.')
                entityDesc = entity.get('pdbx_description', '.')
                entityFW = entity.get('formula_weight', '.')
                if entityFW not in emptyValue:
                    entityFW = float(entityFW)
                entityCopies = entity.get('pdbx_number_of_molecules', '.')
                if entityCopies not in emptyValue:
                    entityCopies = int(entityCopies)
                entityEC = entity.get('pdbx_ec', '.')
                entityParent = entity.get('pdbx_parent_entity_id', '.')
                if entityParent not in emptyValue:
                    entityParent = int(entityParent)
                entityMutation = entity.get('pdbx_mutation', '.')
                entityFragment = entity.get('pdbx_fragment', '.')
                entityDetails = entity.get('details', '.')

                filterItemByEntityId = [{'name': 'entity_id', 'type': 'int', 'value': entityId}]

                entityRole = '.'
                if cR.hasCategory('entity_name_com'):
                    roles = cR.getDictListWithFilter('entity_name_com',
                                                     [{'name': 'name', 'type': 'str'}
                                                      ],
                                                     filterItemByEntityId)
                    if len(roles) > 0:
                        entityRole = ','.join([role['name'] for role in roles if role['name'] is not None])
                        if len(entityRole) == 0:
                            entityRole = '.'

                if entityType == 'polymer':
                    entityPolyType = oneLetterCodeCan = oneLetterCode = targetIdentifier = '.'
                    nstdMonomer = nstdLinkage = '.'
                    nstdChirality = None
                    if cR.hasCategory('entity_poly'):

                        tags = cR.getItemTags('entity_poly')

                        hasSeqOneLetterCodeCan = 'pdbx_seq_one_letter_code_can' in tags
                        hasPdbxTargetIdentifier = 'pdbx_target_identifier' in tags
                        hasNstdMonomer = 'nstd_monomer' in tags
                        hasNstdLinkage = 'nstd_linkage' in tags
                        hasNstdChirality = 'nstd_chirality' in tags

                        dataItems = [{'name': 'type', 'type': 'str'},
                                     {'name': 'pdbx_seq_one_letter_code', 'type': 'str'}]

                        if hasSeqOneLetterCodeCan:
                            dataItems.append({'name': 'pdbx_seq_one_letter_code_can', 'type': 'str'})

                        if hasPdbxTargetIdentifier:
                            dataItems.append({'name': 'pdbx_target_identifier', 'type': 'str'})

                        if hasNstdMonomer:
                            dataItems.append({'name': 'nstd_monomer', 'type': 'str'})

                        if hasNstdLinkage:
                            dataItems.append({'name': 'nstd_linkage', 'type': 'str'})

                        if hasNstdChirality:
                            dataItems.append({'name': 'nstd_chirality', 'type': 'str'})

                        polyTypes = cR.getDictListWithFilter('entity_poly',
                                                             dataItems,
                                                             filterItemByEntityId)

                        if len(polyTypes) > 0:
                            polyType = polyTypes[0]
                            entityPolyType = polyType['type']
                            oneLetterCode = polyType['pdbx_seq_one_letter_code']
                            if hasSeqOneLetterCodeCan:
                                oneLetterCodeCan = polyType['pdbx_seq_one_letter_code_can']
                            if hasPdbxTargetIdentifier:
                                targetIdentifier = polyType['pdbx_target_identifier']
                            if hasNstdMonomer:
                                nstdMonomer = polyType['nstd_monomer']
                            if hasNstdLinkage:
                                nstdLinkage = polyType['nstd_linkage']
                            if hasNstdChirality:
                                nstdChirality = polyType['nstd_chirality']

                    if cR.hasCategory('pdbx_poly_seq_scheme'):
                        has_ins_code = cR.hasItem('pdbx_poly_seq_scheme', 'pdb_ins_code')

                        dataItems = [{'name': 'asym_id', 'type': 'str', 'alt_name': 'label_asym_id'},
                                     {'name': 'pdb_strand_id', 'type': 'str', 'alt_name': 'auth_asym_id'},
                                     {'name': 'auth_seq_num', 'type': 'int', 'alt_name': 'alt_seq_id'},
                                     {'name': 'pdb_seq_num', 'type': 'int', 'alt_name': 'auth_seq_id'},
                                     {'name': 'seq_id', 'type': 'int'},
                                     {'name': 'mon_id', 'type': 'str', 'alt_name': 'comp_id'},
                                     {'name': 'auth_mon_id', 'type': 'str', 'alt_name': 'alt_comp_id'}
                                     ]

                        if has_ins_code:
                            dataItems.append({'name': 'pdb_ins_code', 'type': 'str', 'alt_name': 'ins_code'})

                        mappings = cR.getDictListWithFilter('pdbx_poly_seq_scheme',
                                                            dataItems,
                                                            filterItemByEntityId)

                        authAsymIds = []
                        labelAsymIds = []
                        compIds = set()
                        for item in mappings:
                            if item['auth_asym_id'] not in authAsymIds:
                                authAsymIds.append(item['auth_asym_id'])
                            if item['label_asym_id'] not in labelAsymIds:
                                labelAsymIds.append(item['label_asym_id'])
                            compIds.add(item['comp_id'])
                        for extSeq in nmrExtPolySeq:
                            if extSeq['auth_chain_id'] not in authAsymIds:
                                continue
                            compIds.add(extSeq['comp_id'])

                        if len(authAsymIds) <= MAX_MAG_IDENT_ASYM_ID:
                            if len(labelAsymIds) == 1:
                                for item in mappings:
                                    seqKey = (item['auth_asym_id'], item['auth_seq_id'], item['comp_id'])
                                    authToStarSeq[seqKey] = (entityAssemblyId, item['seq_id'], entityId, True)
                                    authToOrigSeq[seqKey] = (item['alt_seq_id'], item['alt_comp_id'])
                                    if has_ins_code and item['ins_code'] not in emptyValue:
                                        authToInsCode[seqKey] = item['ins_code']
                                    authToEntityType[seqKey] = entityPolyType  # e.g. polypeptide(L), polyribonucleotide, polydeoxyribonucleotide
                                ext_mappings = 0
                                ext_fw = 0.0
                                for extSeq in nmrExtPolySeq:
                                    if extSeq['auth_chain_id'] not in authAsymIds:
                                        continue
                                    seqKey = (extSeq['auth_chain_id'], extSeq['auth_seq_id'], extSeq['comp_id'])
                                    authToStarSeq[seqKey] = (entityAssemblyId, extSeq['seq_id'], entityId, True)
                                    authToOrigSeq[seqKey] = (extSeq['seq_id'], extSeq['auth_comp_id'])
                                    authToEntityType[seqKey] = entityPolyType  # e.g. polypeptide(L), polyribonucleotide, polydeoxyribonucleotide
                                    ext_mappings += 1
                                    if extSeq['chain_id'] not in monDict3:
                                        nstdMonomer = 'yes'
                                    ext_fw += ccU.getEffectiveFormulaWeight(extSeq['comp_id'])

                                for item in mappings:
                                    altKey = (item['auth_asym_id'], item['alt_seq_id'], item['comp_id'])
                                    if altKey not in authToStarSeq:
                                        authToStarSeq[altKey] = (entityAssemblyId, item['seq_id'], entityId, True)
                                        if has_ins_code and item['ins_code'] not in emptyValue:
                                            authToInsCode[altKey] = item['ins_code']
                                        authToEntityType[altKey] = entityPolyType
                                for extSeq in nmrExtPolySeq:
                                    if extSeq['auth_chain_id'] not in authAsymIds:
                                        continue
                                    altKey = (extSeq['auth_chain_id'], extSeq['auth_seq_id'], extSeq['comp_id'])
                                    if altKey not in authToStarSeq:
                                        authToStarSeq[altKey] = (entityAssemblyId, extSeq['seq_id'], entityId, True)
                                        authToEntityType[altKey] = entityPolyType

                                entityAssembly.append({'entity_assembly_id': entityAssemblyId, 'entity_id': entityId,
                                                       'entity_type': entityType, 'entity_src_method': entitySrcMethod,
                                                       'entity_desc': entityDesc, 'entity_fw': round(entityFW + ext_fw, 3),
                                                       'entity_copies': entityCopies, 'entity_ec': entityEC,
                                                       'entity_parent': entityParent,
                                                       'entity_mutation': entityMutation,
                                                       'entity_fragment': entityFragment,
                                                       'entity_details': entityDetails,
                                                       'entity_role': entityRole,
                                                       'entity_poly_type': entityPolyType,
                                                       'one_letter_code_can': oneLetterCodeCan,
                                                       'one_letter_code': oneLetterCode,
                                                       'nstd_monomer': nstdMonomer,
                                                       'nstd_linkage': nstdLinkage,
                                                       'nstd_chirality': nstdChirality,
                                                       'target_identifier': targetIdentifier,
                                                       'num_of_monomers': len(mappings) + ext_mappings,
                                                       'auth_asym_id': ','.join(authAsymIds),
                                                       'label_asym_id': ','.join(labelAsymIds),
                                                       'comp_id_set': compIds})
                                entityAssemblyId += 1

                            else:

                                _labelAsymIds = copy.copy(labelAsymIds)

                                for labelAsymId in _labelAsymIds:

                                    authAsymIds = []
                                    labelAsymIds = []
                                    compIds = set()
                                    for item in mappings:
                                        if item['label_asym_id'] != labelAsymId:
                                            continue
                                        if item['auth_asym_id'] not in authAsymIds:
                                            authAsymIds.append(item['auth_asym_id'])
                                        if item['label_asym_id'] not in labelAsymIds:
                                            labelAsymIds.append(item['label_asym_id'])
                                        compIds.add(item['comp_id'])
                                    for extSeq in nmrExtPolySeq:
                                        if extSeq['chain_id'] != labelAsymId:
                                            continue
                                        compIds.add(extSeq['comp_id'])

                                    if len(authAsymIds) <= MAX_MAG_IDENT_ASYM_ID:
                                        if len(labelAsymIds) == 1:
                                            for item in mappings:
                                                if item['label_asym_id'] != labelAsymId:
                                                    continue
                                                seqKey = (item['auth_asym_id'], item['auth_seq_id'], item['comp_id'])
                                                authToStarSeq[seqKey] = (entityAssemblyId, item['seq_id'], entityId, True)
                                                authToOrigSeq[seqKey] = (item['alt_seq_id'], item['alt_comp_id'])
                                                if has_ins_code and item['ins_code'] not in emptyValue:
                                                    authToInsCode[seqKey] = item['ins_code']
                                                authToEntityType[seqKey] = entityPolyType  # e.g. polypeptide(L), polyribonucleotide, polydeoxyribonucleotide
                                            ext_mappings = 0
                                            ext_fw = 0.0
                                            for extSeq in nmrExtPolySeq:
                                                if extSeq['chain_id'] != labelAsymId:
                                                    continue
                                                seqKey = (extSeq['auth_chain_id'], extSeq['auth_seq_id'], extSeq['comp_id'])
                                                authToStarSeq[seqKey] = (entityAssemblyId, extSeq['seq_id'], entityId, True)
                                                authToOrigSeq[seqKey] = (extSeq['seq_id'], extSeq['auth_comp_id'])
                                                authToEntityType[seqKey] = entityPolyType  # e.g. polypeptide(L), polyribonucleotide, polydeoxyribonucleotide
                                                ext_mappings += 1
                                                if extSeq['chain_id'] not in monDict3:
                                                    nstdMonomer = 'yes'
                                                ext_fw += ccU.getEffectiveFormulaWeight(extSeq['comp_id'])

                                            for item in mappings:
                                                if item['label_asym_id'] != labelAsymId:
                                                    continue
                                                altKey = (item['auth_asym_id'], item['alt_seq_id'], item['comp_id'])
                                                if altKey not in authToStarSeq:
                                                    authToStarSeq[altKey] = (entityAssemblyId, item['seq_id'], entityId, True)
                                                    if has_ins_code and item['ins_code'] not in emptyValue:
                                                        authToInsCode[altKey] = item['ins_code']
                                                    authToEntityType[altKey] = entityPolyType
                                            for extSeq in nmrExtPolySeq:
                                                if extSeq['chain_id'] != labelAsymId:
                                                    continue
                                                altKey = (extSeq['auth_chain_id'], extSeq['auth_seq_id'], extSeq['comp_id'])
                                                if altKey not in authToStarSeq:
                                                    authToStarSeq[altKey] = (entityAssemblyId, extSeq['seq_id'], entityId, True)
                                                    authToEntityType[altKey] = entityPolyType

                                            entityAssembly.append({'entity_assembly_id': entityAssemblyId, 'entity_id': entityId,
                                                                   'entity_type': entityType, 'entity_src_method': entitySrcMethod,
                                                                   'entity_desc': entityDesc, 'entity_fw': round(entityFW + ext_fw, 3),
                                                                   'entity_copies': entityCopies, 'entity_ec': entityEC,
                                                                   'entity_parent': entityParent,
                                                                   'entity_mutation': entityMutation,
                                                                   'entity_fragment': entityFragment,
                                                                   'entity_details': entityDetails,
                                                                   'entity_role': entityRole,
                                                                   'entity_poly_type': entityPolyType,
                                                                   'one_letter_code_can': oneLetterCodeCan,
                                                                   'one_letter_code': oneLetterCode,
                                                                   'nstd_monomer': nstdMonomer,
                                                                   'nstd_linkage': nstdLinkage,
                                                                   'nstd_chirality': nstdChirality,
                                                                   'target_identifier': targetIdentifier,
                                                                   'num_of_monomers': len(mappings) + ext_mappings,
                                                                   'auth_asym_id': ','.join(authAsymIds),
                                                                   'label_asym_id': ','.join(labelAsymIds),
                                                                   'comp_id_set': compIds})
                                            entityAssemblyId += 1

                        else:

                            for _authAsymId in authAsymIds:
                                labelAsymIds = []
                                for item in mappings:
                                    if item['auth_asym_id'] == _authAsymId:
                                        seqKey = (item['auth_asym_id'], item['auth_seq_id'], item['comp_id'])
                                        authToStarSeq[seqKey] = (entityAssemblyId, item['seq_id'], entityId, True)
                                        authToOrigSeq[seqKey] = (item['alt_seq_id'], item['alt_comp_id'])
                                        if has_ins_code and item['ins_code'] not in emptyValue:
                                            authToInsCode[seqKey] = item['ins_code']
                                        authToEntityType[seqKey] = entityPolyType  # e.g. polypeptide(L), polyribonucleotide, polydeoxyribonucleotide
                                        if item['label_asym_id'] not in labelAsymIds:
                                            labelAsymIds.append(item['label_asym_id'])
                                ext_mappings = 0
                                ext_fw = 0.0
                                for extSeq in nmrExtPolySeq:
                                    if extSeq['auth_chain_id'] == _authAsymId:
                                        seqKey = (extSeq['auth_chain_id'], extSeq['auth_seq_id'], extSeq['comp_id'])
                                        authToStarSeq[seqKey] = (entityAssemblyId, extSeq['seq_id'], entityId, True)
                                        authToOrigSeq[seqKey] = (extSeq['seq_id'], extSeq['auth_comp_id'])
                                        authToEntityType[seqKey] = entityPolyType  # e.g. polypeptide(L), polyribonucleotide, polydeoxyribonucleotide
                                        ext_mappings += 1
                                        if extSeq['chain_id'] not in monDict3:
                                            nstdMonomer = 'yes'
                                        ext_fw += ccU.getEffectiveFormulaWeight(extSeq['comp_id'])

                                for item in mappings:
                                    if item['auth_asym_id'] == _authAsymId:
                                        altKey = (item['auth_asym_id'], item['alt_seq_id'], item['comp_id'])
                                        if altKey not in authToStarSeq:
                                            authToStarSeq[altKey] = (entityAssemblyId, item['seq_id'], entityId, True)
                                            if has_ins_code and item['ins_code'] not in emptyValue:
                                                authToInsCode[altKey] = item['ins_code']
                                            authToEntityType[altKey] = entityPolyType
                                for extSeq in nmrExtPolySeq:
                                    if extSeq['auth_chain_id'] == _authAsymId:
                                        altKey = (extSeq['auth_chain_id'], extSeq['auth_seq_id'], extSeq['comp_id'])
                                        if altKey not in authToStarSeq:
                                            authToStarSeq[altKey] = (entityAssemblyId, extSeq['seq_id'], entityId, True)
                                            authToEntityType[altKey] = entityPolyType

                                entityAssembly.append({'entity_assembly_id': entityAssemblyId, 'entity_id': entityId,
                                                       'entity_type': entityType, 'entity_src_method': entitySrcMethod,
                                                       'entity_desc': entityDesc, 'entity_fw': round(entityFW + ext_fw, 3),
                                                       'entity_copies': 1, 'entity_ec': entityEC,
                                                       'entity_parent': entityParent,
                                                       'entity_mutation': entityMutation,
                                                       'entity_fragment': entityFragment,
                                                       'entity_details': entityDetails,
                                                       'entity_role': entityRole,
                                                       'entity_poly_type': entityPolyType,
                                                       'one_letter_code_can': oneLetterCodeCan,
                                                       'one_letter_code': oneLetterCode,
                                                       'nstd_monomer': nstdMonomer,
                                                       'nstd_linkage': nstdLinkage,
                                                       'nstd_chirality': nstdChirality,
                                                       'target_identifier': targetIdentifier,
                                                       'num_of_monomers': len(mappings) + ext_mappings,
                                                       'auth_asym_id': _authAsymId,
                                                       'label_asym_id': ','.join(labelAsymIds),
                                                       'comp_id_set': compIds})
                                entityAssemblyId += 1

                elif entityType == 'branched':
                    entityPolyType = '.'
                    if cR.hasCategory('pdbx_entity_branch'):
                        polyTypes = cR.getDictListWithFilter('pdbx_entity_branch',
                                                             [{'name': 'type', 'type': 'str'}
                                                              ],
                                                             filterItemByEntityId)
                        if len(polyTypes) > 0:
                            entityPolyType = polyTypes[0]['type']

                    if cR.hasCategory('pdbx_branch_scheme'):
                        has_ins_code = cR.hasItem('pdbx_branch_scheme', 'pdb_ins_code')

                        dataItems = [{'name': 'asym_id', 'type': 'str', 'alt_name': 'label_asym_id'},
                                     {'name': 'auth_asym_id', 'type': 'str'},
                                     {'name': 'auth_seq_num', 'type': 'int', 'alt_name': 'alt_seq_id'},
                                     {'name': 'pdb_seq_num', 'type': 'int', 'alt_name': 'auth_seq_id'},
                                     {'name': 'num', 'type': 'int', 'alt_name': 'seq_id'},
                                     {'name': 'mon_id', 'type': 'str', 'alt_name': 'comp_id'},
                                     {'name': 'auth_mon_id', 'type': 'str', 'alt_name': 'alt_comp_id'}
                                     ]

                        if has_ins_code:
                            dataItems.append({'name': 'pdb_ins_code', 'type': 'str', 'alt_name': 'ins_code'})

                        mappings = cR.getDictListWithFilter('pdbx_branch_scheme',
                                                            dataItems,
                                                            filterItemByEntityId)

                        authAsymIds = []
                        for item in mappings:
                            if item['auth_asym_id'] not in authAsymIds:
                                authAsymIds.append(item['auth_asym_id'])

                        if len(authAsymIds) <= MAX_MAG_IDENT_ASYM_ID:
                            labelAsymIds = []
                            for item in mappings:
                                seqKey = (item['auth_asym_id'], item['auth_seq_id'], item['comp_id'])
                                authToStarSeq[seqKey] = (entityAssemblyId, item['seq_id'], entityId, False)
                                authToOrigSeq[seqKey] = (item['alt_seq_id'], item['alt_comp_id'])
                                if has_ins_code and item['ins_code'] not in emptyValue:
                                    authToInsCode[seqKey] = item['ins_code']
                                authToEntityType[seqKey] = entityPolyType  # e.g. oligosaccharide
                                if item['label_asym_id'] not in labelAsymIds:
                                    labelAsymIds.append(item['label_asym_id'])

                            for item in mappings:
                                altKey = (item['auth_asym_id'], item['alt_seq_id'], item['comp_id'])
                                if altKey not in authToStarSeq:
                                    authToStarSeq[altKey] = (entityAssemblyId, item['seq_id'], entityId, True)
                                    if has_ins_code and item['ins_code'] not in emptyValue:
                                        authToInsCode[altKey] = item['ins_code']
                                    authToEntityType[altKey] = entityPolyType

                            entityAssembly.append({'entity_assembly_id': entityAssemblyId, 'entity_id': entityId,
                                                   'entity_type': entityType, 'entity_src_method': entitySrcMethod,
                                                   'entity_desc': entityDesc, 'entity_fw': entityFW,
                                                   'entity_copies': entityCopies,
                                                   'entity_details': entityDetails,
                                                   'entity_role': entityRole,
                                                   'entity_poly_type': entityPolyType,
                                                   'num_of_monomers': len(mappings),
                                                   'auth_asym_id': ','.join(authAsymIds),
                                                   'label_asym_id': ','.join(labelAsymIds)})
                            entityAssemblyId += 1

                        else:

                            for _authAsymId in authAsymIds:
                                labelAsymIds = []
                                for item in mappings:
                                    if item['auth_asym_id'] == _authAsymId:
                                        seqKey = (item['auth_asym_id'], item['auth_seq_id'], item['comp_id'])
                                        authToStarSeq[seqKey] = (entityAssemblyId, item['seq_id'], entityId, False)
                                        if has_ins_code and item['ins_code'] not in emptyValue:
                                            authToInsCode[seqKey] = item['ins_code']
                                        authToEntityType[seqKey] = entityPolyType  # e.g. oligosaccharide
                                        if item['label_asym_id'] not in labelAsymIds:
                                            labelAsymIds.append(item['label_asym_id'])

                                for item in mappings:
                                    if item['auth_asym_id'] == _authAsymId:
                                        altKey = (item['auth_asym_id'], item['alt_seq_id'], item['comp_id'])
                                        if altKey not in authToStarSeq:
                                            authToStarSeq[altKey] = (entityAssemblyId, item['seq_id'], entityId, True)
                                            if has_ins_code and item['ins_code'] not in emptyValue:
                                                authToInsCode[altKey] = item['ins_code']
                                            authToEntityType[altKey] = entityPolyType

                                entityAssembly.append({'entity_assembly_id': entityAssemblyId, 'entity_id': entityId,
                                                       'entity_type': entityType, 'entity_src_method': entitySrcMethod,
                                                       'entity_desc': entityDesc, 'entity_fw': entityFW,
                                                       'entity_copies': 1,
                                                       'entity_details': entityDetails,
                                                       'entity_role': entityRole,
                                                       'entity_poly_type': entityPolyType,
                                                       'num_of_monomers': len(mappings),
                                                       'auth_asym_id': _authAsymId,
                                                       'label_asym_id': ','.join(labelAsymIds)})
                                entityAssemblyId += 1

                elif entityType == 'non-polymer':
                    if cR.hasCategory('pdbx_nonpoly_scheme'):
                        has_ins_code = cR.hasItem('pdbx_nonpoly_scheme', 'pdb_ins_code')

                        dataItems = [{'name': 'asym_id', 'type': 'str', 'alt_name': 'label_asym_id'},
                                     {'name': 'pdb_strand_id', 'type': 'str', 'alt_name': 'auth_asym_id'},
                                     {'name': 'auth_seq_num', 'type': 'int', 'alt_name': 'alt_seq_id'},
                                     {'name': 'pdb_seq_num', 'type': 'int', 'alt_name': 'auth_seq_id'},
                                     {'name': 'ndb_seq_num', 'type': 'int', 'alt_name': 'seq_id'},
                                     {'name': 'mon_id', 'type': 'str', 'alt_name': 'comp_id'},
                                     {'name': 'auth_mon_id', 'type': 'str', 'alt_name': 'alt_comp_id'}
                                     ]

                        if has_ins_code:
                            dataItems.append({'name': 'pdb_ins_code', 'type': 'str', 'alt_name': 'ins_code'})

                        mappings = cR.getDictListWithFilter('pdbx_nonpoly_scheme',
                                                            dataItems,
                                                            filterItemByEntityId)

                        authAsymIds = []
                        compId = None
                        for idx, item in enumerate(mappings):
                            seqKey = (item['auth_asym_id'], item['auth_seq_id'], item['comp_id'])
                            authToStarSeq[seqKey] = (entityAssemblyId, idx + 1, entityId, True)
                            authToOrigSeq[seqKey] = (item['alt_seq_id'], item['alt_comp_id'])
                            if has_ins_code and item['ins_code'] not in emptyValue:
                                authToInsCode[seqKey] = item['ins_code']
                            authToEntityType[seqKey] = 'non-polymer'
                            if item['auth_asym_id'] not in authAsymIds:
                                authAsymIds.append(item['auth_asym_id'])
                            if compId is None:
                                compId = item['comp_id']

                        for idx, item in enumerate(mappings):
                            altKey = (item['auth_asym_id'], item['alt_seq_id'], item['comp_id'])
                            if altKey not in authToStarSeq:
                                authToStarSeq[altKey] = (entityAssemblyId, idx + 1, entityId, False)
                                if has_ins_code and item['ins_code'] not in emptyValue:
                                    authToInsCode[altKey] = item['ins_code']
                                authToEntityType[altKey] = 'non-polymer'

                        labelAsymIds = []
                        for item in mappings:
                            if item['label_asym_id'] not in labelAsymIds:
                                labelAsymIds.append(item['label_asym_id'])

                        entityAssembly.append({'entity_assembly_id': entityAssemblyId, 'entity_id': entityId,
                                               'entity_type': entityType, 'entity_src_method': entitySrcMethod,
                                               'entity_desc': entityDesc, 'entity_fw': entityFW,
                                               'entity_copies': entityCopies,
                                               'entity_details': entityDetails,
                                               'entity_role': entityRole,
                                               'auth_asym_id': ','.join(authAsymIds),
                                               'label_asym_id': ','.join(labelAsymIds),
                                               'comp_id': compId})
                        entityAssemblyId += 1

                    elif has_nonpoly_only:
                        gen_ent_asm_from_nonpoly = True

            if gen_ent_asm_from_nonpoly:

                _idx = {}
                for item in nonPoly:
                    for compId in item['comp_id']:
                        if compId not in _idx:
                            _idx[compId] = 0

                for item in nonPoly:
                    for idx, compId in enumerate(item['comp_id']):

                        for entity in entities:
                            entityId = int(entity['id'])
                            entityType = entity.get('type', 'polymer')
                            if entityType != 'non-polymer':
                                continue
                            entitySrcMethod = entity.get('src_method', '.')
                            entityDesc = entity.get('pdbx_description', '.')
                            entityFW = entity.get('formula_weight', '.')
                            if entityFW not in emptyValue:
                                entityFW = float(entityFW)
                            entityCopies = entity.get('pdbx_number_of_molecules', '.')
                            if entityCopies not in emptyValue:
                                entityCopies = int(entityCopies)
                            entityEC = entity.get('pdbx_ec', '.')
                            entityParent = entity.get('pdbx_parent_entity_id', '.')
                            if entityParent not in emptyValue:
                                entityParent = int(entityParent)
                            entityMutation = entity.get('pdbx_mutation', '.')
                            entityFragment = entity.get('pdbx_fragment', '.')
                            if compId != entityFragment:
                                continue
                            entityDetails = entity.get('details', '.')

                            filterItemByEntityId = [{'name': 'entity_id', 'type': 'int', 'value': entityId}]

                            entityRole = '.'
                            if cR.hasCategory('entity_name_com'):
                                roles = cR.getDictListWithFilter('entity_name_com',
                                                                 [{'name': 'name', 'type': 'str'}
                                                                  ],
                                                                 filterItemByEntityId)
                                if len(roles) > 0:
                                    entityRole = ','.join([role['name'] for role in roles if role['name'] is not None])
                                    if len(entityRole) == 0:
                                        entityRole = '.'

                            seqKey = (item['auth_chain_id'], item['auth_seq_id'][idx], compId)
                            authToStarSeq[seqKey] = (entityAssemblyId, _idx[compId] + 1, entityId, True)
                            authToOrigSeq[seqKey] = (item['seq_id'][idx], compId)
                            if 'ins_code' in item and item['ins_code'][idx] not in emptyValue:
                                authToInsCode[seqKey] = item['ins_code'][idx]
                            authToEntityType[seqKey] = 'non-polymer'

                            authAsymIds = labelAsymIds = []
                            for _item in nonPoly:
                                if idx < len(item['comp_id']) and item['comp_id'][idx] == compId:
                                    if _item['auth_chain_id'] not in authAsymIds:
                                        authAsymIds.append(_item['auth_chain_id'])
                                    if _item['chain_id'] not in labelAsymIds:
                                        labelAsymIds.append(_item['chain_id'])

                            _idx[compId] += 1

                            entityAssembly.append({'entity_assembly_id': entityAssemblyId, 'entity_id': entityId,
                                                   'entity_type': entityType, 'entity_src_method': entitySrcMethod,
                                                   'entity_desc': entityDesc, 'entity_fw': entityFW,
                                                   'entity_copies': entityCopies,
                                                   'entity_details': entityDetails,
                                                   'entity_role': entityRole,
                                                   'auth_asym_id': ','.join(authAsymIds),
                                                   'label_asym_id': ','.join(labelAsymIds),
                                                   'fixed_auth_asym_id': item['auth_chain_id'],
                                                   'fixed_label_asym_id': item['chain_id'],
                                                   'comp_id': compId})
                            entityAssemblyId += 1

                            break

    except Exception as e:
        if verbose:
            log.write(f"+ParserListenerUtil.coordAssemblyChecker() ++ Error  - {str(e)}\n")

    if authToInsCode is not None and len(authToInsCode) == 0:
        authToInsCode = None

    if not changed:
        return prevResult

    return {'model_num_name': modelNumName,
            'auth_asym_id': authAsymId,
            'auth_seq_id': authSeqId,
            'auth_atom_id': authAtomId,
            'polymer_sequence': polySeq,
            'alt_polymer_sequence': altPolySeq,
            'non_polymer': nonPoly,
            'branched': branched,
            'nmr_ext_poly_seq': nmrExtPolySeq,
            'coord_atom_site': coordAtomSite,
            'coord_unobs_res': coordUnobsRes,
            'label_to_auth_seq': labelToAuthSeq,
            'auth_to_label_seq': authToLabelSeq,
            'label_to_auth_chain': labelToAuthChain,
            'auth_to_label_chain': authToLabelChain,
            'auth_to_star_seq': authToStarSeq,
            'auth_to_orig_seq': authToOrigSeq,
            'auth_to_ins_code': authToInsCode,
            'auth_to_entity_type': authToEntityType,
            'entity_assembly': entityAssembly,
            'chem_comp_atom': chemCompAtom,
            'chem_comp_bond': chemCompBond,
            'chem_comp_topo': chemCompTopo,
            'auth_atom_name_to_id': authAtomNameToId}


def extendCoordChainsForExactNoes(modelChainIdExt,
                                  polySeq, altPolySeq, coordAtomSite, coordUnobsRes,
                                  authToLabelSeq, authToStarSeq):
    """ Extend coordinate chains for eNOEs-guided multiple conformers.
    """

    _polySeq = None

    if polySeq is not None:
        _polySeq = copy.copy(polySeq)

        for ps in polySeq:
            if ps['auth_chain_id'] in modelChainIdExt:
                for dstChainId in modelChainIdExt[ps['auth_chain_id']]:
                    if not any(ps for ps in polySeq if ps['auth_chain_id'] == dstChainId):
                        _ps = copy.copy(ps)
                        _ps['chain_id'] = _ps['auth_chain_id'] = dstChainId
                        _polySeq.append(_ps)

    _altPolySeq = None

    if altPolySeq is not None:
        _altPolySeq = copy.copy(altPolySeq)

        for ps in altPolySeq:
            if ps['auth_chain_id'] in modelChainIdExt:
                for dstChainId in modelChainIdExt[ps['auth_chain_id']]:
                    if not any(ps for ps in altPolySeq if ps['auth_chain_id'] == dstChainId):
                        _ps = copy.copy(ps)
                        _ps['chain_id'] = _ps['auth_chain_id'] = dstChainId
                        _altPolySeq.append(_ps)

    _coordAtomSite = None

    if coordAtomSite is not None:
        _coordAtomSite = copy.copy(coordAtomSite)

        for ps in polySeq:
            srcChainId = ps['auth_chain_id']
            if srcChainId in modelChainIdExt:
                for dstChainId in modelChainIdExt[ps['auth_chain_id']]:
                    for seqId in ps['auth_seq_id']:
                        seqKey = (srcChainId, seqId)
                        if seqKey in _coordAtomSite:
                            _seqKey = (dstChainId, seqId)
                            if _seqKey not in _coordAtomSite:
                                _coordAtomSite[_seqKey] = coordAtomSite[seqKey]

    _coordUnobsRes = None

    if coordUnobsRes is not None:
        _coordUnobsRes = copy.copy(coordUnobsRes)

        for ps in polySeq:
            srcChainId = ps['auth_chain_id']
            if srcChainId in modelChainIdExt:
                for dstChainId in modelChainIdExt[ps['auth_chain_id']]:
                    for seqId in ps['auth_seq_id']:
                        seqKey = (srcChainId, seqId)
                        if seqKey in coordUnobsRes:
                            _seqKey = (dstChainId, seqId)
                            if _seqKey not in _coordUnobsRes:
                                _coordUnobsRes[_seqKey] = coordUnobsRes[seqKey]

    _authToLabelSeq = None
    _labelToAuthSeq = None

    if authToLabelSeq is not None:
        _authToLabelSeq = copy.copy(authToLabelSeq)

        for ps in polySeq:
            srcChainId = ps['auth_chain_id']
            if srcChainId in modelChainIdExt:
                for dstChainId in modelChainIdExt[ps['auth_chain_id']]:
                    for seqId in ps['auth_seq_id']:
                        seqKey = (srcChainId, seqId)
                        if seqKey in authToLabelSeq:
                            seqVal = authToLabelSeq[seqKey]
                            _seqKey = (dstChainId, seqId)
                            if _seqKey not in _authToLabelSeq:
                                _authToLabelSeq[_seqKey] = (dstChainId, seqVal[1])

        _labelToAuthSeq = {v: k for k, v in _authToLabelSeq.items()}

    if authToStarSeq is not None:
        _authToStarSeq = copy.copy(authToStarSeq)

        maxAsmEntityId = max(item[0] for item in authToStarSeq.values()) + 1
        asmEntityIdExt = {}

        for ps in polySeq:
            srcChainId = ps['auth_chain_id']
            if srcChainId in modelChainIdExt:
                for dstChainId in modelChainIdExt[ps['auth_chain_id']]:
                    if dstChainId in asmEntityIdExt:
                        continue
                    asmEntityIdExt[dstChainId] = maxAsmEntityId
                    maxAsmEntityId += 1

        for ps in polySeq:
            srcChainId = ps['auth_chain_id']
            if srcChainId in modelChainIdExt:
                for dstChainId in modelChainIdExt[ps['auth_chain_id']]:
                    dstAsmEntityId = asmEntityIdExt[dstChainId]
                    for seqId, compId in zip(ps['auth_seq_id'], ps['comp_id']):
                        seqKey = (srcChainId, seqId, compId)
                        if seqKey in authToStarSeq:
                            seqVal = authToStarSeq[seqKey]
                            _seqKey = (dstChainId, seqId, compId)
                            if _seqKey not in _authToStarSeq:
                                _authToStarSeq[_seqKey] = (dstAsmEntityId, seqVal[1], seqVal[2], seqVal[3])

    return _polySeq, _altPolySeq, _coordAtomSite, _coordUnobsRes, _labelToAuthSeq, _authToLabelSeq, _authToStarSeq


def isIdenticalRestraint(atoms):
    """ Return whether restraint contains identical atom selection.
    """

    try:

        for a1, a2 in itertools.combinations(atoms, 2):
            if a1['chain_id'] == a2['chain_id'] and a1['seq_id'] == a2['seq_id'] and a1['atom_id'] == a2['atom_id']:
                return True

    except KeyError:
        pass

    return False


def isLongRangeRestraint(atoms, polySeq=None):
    """ Return whether restraint is neither an intra residue nor sequential residue restraint.
    """

    chainIds = [a['chain_id'] for a in atoms]

    if len(collections.Counter(chainIds).most_common()) > 1:
        return True

    seqIds = [a['seq_id'] for a in atoms]

    commonSeqId = collections.Counter(seqIds).most_common()

    if len(commonSeqId) == 1:
        return False

    for s1, s2 in itertools.combinations(commonSeqId, 2):
        if abs(s1[0] - s2[0]) > 1:
            if polySeq is None:
                return True

            # verify with label_seq_id scheme

            try:

                ps = next(ps for ps in polySeq if ps['auth_chain_id'] == chainIds[0])

                _seqIds = [ps['seq_id'][ps['auth_seq_id'].index(a['seq_id'])] for a in atoms]
                _commonSeqId = collections.Counter(_seqIds).most_common()
                for _s1, _s2 in itertools.combinations(_commonSeqId, 2):
                    if abs(_s1[0] - _s2[0]) > 1:
                        return True

            except Exception:
                return True

    return False


def getAltProtonIdInBondConstraint(atoms, csStat):
    """ Return alternative atom_id in swappable proton group, which involves in bond constraint (i.e. amino group in Watson-Crick pair).
    """

    if len(atoms) < 2:
        return None, None

    if any(a is None for a in atoms):
        return None, None

    for a in atoms:
        if 'chain_id' not in a or a['chain_id'] in emptyValue:
            return None, None
        if 'comp_id' not in a or a['comp_id'] in emptyValue:
            return None, None
        if 'atom_id' not in a or a['atom_id'] in emptyValue:
            return None, None

    chainIds = [a['chain_id'] for a in atoms]

    if len(collections.Counter(chainIds).most_common()) == 1:
        return None, None

    compId1 = atoms[0]['comp_id']
    compId2 = atoms[1]['comp_id']

    atomId1 = atoms[0]['atom_id']
    atomId2 = atoms[1]['atom_id']

    if atomId1[0] in protonBeginCode and atomId2[0] not in protonBeginCode:

        ambigCode1 = csStat.getMaxAmbigCodeWoSetId(compId1, atomId1)

        if ambigCode1 not in (2, 3):
            return None, None

        return csStat.getGeminalAtom(compId1, atomId1), None

    if atomId2[0] in protonBeginCode and atomId1[0] not in protonBeginCode:

        ambigCode2 = csStat.getMaxAmbigCodeWoSetId(compId2, atomId2)

        if ambigCode2 not in (2, 3):
            return None, None

        return None, csStat.getGeminalAtom(compId2, atomId2)

    return None, None


def isAsymmetricRangeRestraint(atoms, chainIdSet, symmetric):
    """ Return whether restraint is asymmetric.
    """

    lenAtoms = len(atoms)

    if len(set((frozenset(atom.items()) for atom in atoms))) != lenAtoms:  # reject identical atom
        return True

    lenChainIdSet = len(chainIdSet)

    chainIds = [a['chain_id'] for a in atoms]
    indices = [chainIdSet.index(c) for c in chainIds]

    for pos, index in enumerate(indices):
        if pos == lenAtoms - 1:
            break
        if index + 1 < lenChainIdSet:
            nextIndex = index + 1
        elif symmetric == 'circular':
            nextIndex = 0
        else:
            return True
        if indices[pos + 1] != nextIndex:
            return True

    seqIds = [a['seq_id'] for a in atoms]

    commonSeqId = collections.Counter(seqIds).most_common()

    if len(commonSeqId) == 1:
        return False

    for s1, s2 in itertools.combinations(commonSeqId, 2):
        if abs(s1[0] - s2[0]) > 1:
            return True

    return False


def hasIntraChainRestraint(atomSelectionSet):
    """ Return whether intra-chain distance restraints in the atom selection.
    """

    for atom1, atom2 in itertools.product(atomSelectionSet[0],
                                          atomSelectionSet[1]):
        if atom1['chain_id'] == atom2['chain_id']:
            return True, getRepIntraChainIds(atomSelectionSet)

    return False, None


def hasInterChainRestraint(atomSelectionSet):
    """ Return whether inter-chain distance restraints in the atom selection.
    """

    for atom1, atom2 in itertools.product(atomSelectionSet[0],
                                          atomSelectionSet[1]):
        if atom1['chain_id'] != atom2['chain_id']:
            return True

    return False


def getRepIntraChainIds(atomSelectionSet):
    """ Return representative set of chain id of intra-chain distance restraints in case of large assembly.
    """

    intraChainIds = set()
    for atom1, atom2 in itertools.product(atomSelectionSet[0],
                                          atomSelectionSet[1]):
        if atom1['chain_id'] == atom2['chain_id']:
            intraChainIds.add(atom1['chain_id'])

    if len(intraChainIds) > MAX_MAG_IDENT_ASYM_ID:
        for chainId in LARGE_ASYM_ID:
            if chainId in intraChainIds:
                return {chainId}

    return intraChainIds


def isAmbigAtomSelection(atoms, csStat):
    """ Return whether an atom selection involves heterogeneous atom groups.
    """

    if len(atoms) < 2:
        return False

    if any(a is None for a in atoms):
        return False

    for a in atoms:
        if 'chain_id' not in a or a['chain_id'] in emptyValue:
            return True
        if 'seq_id' not in a or a['seq_id'] in emptyValue:
            return True
        if 'comp_id' not in a or a['comp_id'] in emptyValue:
            return True
        if 'atom_id' not in a or a['atom_id'] in emptyValue:
            return True

    chainIds = [a['chain_id'] for a in atoms]

    if len(collections.Counter(chainIds).most_common()) > 1:
        return True

    seqIds = [a['seq_id'] for a in atoms]

    commonSeqId = collections.Counter(seqIds).most_common()

    if len(commonSeqId) > 1:
        return True

    atomIds = list(set(a['atom_id'] for a in atoms))

    commonAtomId = collections.Counter(atomIds).most_common()

    if len(commonAtomId) == 1:
        return False

    atomId0 = atomIds[0]
    compId = atoms[0]['comp_id']

    _protonsInGroup = csStat.getProtonsInSameGroup(compId, atomId0, True)
    geminalAtom = csStat.getGeminalAtom(compId, atomId0)

    if geminalAtom is not None:

        if atomId0[0] not in protonBeginCode:
            if set(atomIds) == {atomId0, geminalAtom}:
                return False

        if _protonsInGroup is not None:
            _protonsInGroup.append(geminalAtom)
        else:
            _protonsInGroup = [geminalAtom]

        geminalProtonsInGroup = csStat.getProtonsInSameGroup(compId, geminalAtom, True)
        if geminalProtonsInGroup is not None and len(geminalProtonsInGroup) > 0:
            _protonsInGroup.extend(geminalProtonsInGroup)

    if _protonsInGroup is None or len(_protonsInGroup) == 0:
        return True

    for atomId in atomIds[1:]:
        if atomId not in _protonsInGroup:
            return True

    return False


def getTypeOfDihedralRestraint(polypeptide, polynucleotide, carbohydrates, atoms):
    """ Return type of dihedral angle restraint.
    """

    chainIds = [a['chain_id'] for a in atoms]
    seqIds = [a['seq_id'] for a in atoms]

    if any('atom_id' not in a for a in atoms):
        return None

    atomIds = [a['atom_id'] for a in atoms]

    if len(collections.Counter(chainIds).most_common()) > 1:
        return None

    commonSeqId = collections.Counter(seqIds).most_common()

    lenCommonSeqId = len(commonSeqId)

    if polypeptide:

        if lenCommonSeqId == 2:

            phiPsiCommonAtomIds = ['N', 'CA', 'C']

            # PHI or PSI
            if commonSeqId[0][1] == 3 and commonSeqId[1][1] == 1:

                # PHI
                prevSeqId = commonSeqId[1][0]

                if commonSeqId[0][0] == prevSeqId + 1:

                    j = 0
                    if seqIds[j] == prevSeqId and atomIds[j] == 'C':
                        atomIds.pop(j)
                        if atomIds == phiPsiCommonAtomIds:
                            return 'PHI'

                # PSI
                nextSeqId = commonSeqId[1][0]

                if commonSeqId[0][0] == nextSeqId - 1:

                    j = 3
                    if seqIds[j] == nextSeqId and atomIds[j] == 'N':
                        atomIds.pop(j)
                        if atomIds == phiPsiCommonAtomIds:
                            return 'PSI'

            # OMEGA
            if atomIds[0] == 'CA' and atomIds[1] == 'N' and atomIds[2] == 'C' and atomIds[3] == 'CA'\
               and seqIds[0] == seqIds[1] and seqIds[1] - 1 == seqIds[2] and seqIds[2] == seqIds[3]:
                return 'OMEGA'

            if atomIds[0] == 'CA' and atomIds[1] == 'C' and atomIds[2] == 'N' and atomIds[3] == 'CA'\
               and seqIds[0] == seqIds[1] and seqIds[1] + 1 == seqIds[2] and seqIds[2] == seqIds[3]:
                return 'OMEGA'

            # OMEGA - modified CYANA definition
            if atomIds[0] == 'O' and atomIds[1] == 'C' and atomIds[2] == 'N'\
               and (atomIds[3] == 'H' or atomIds[3] == 'CD')\
               and seqIds[0] == seqIds[1] and seqIds[1] + 1 == seqIds[2] and seqIds[2] == seqIds[3]:
                return 'OMEGA'

        elif lenCommonSeqId == 1:

            testDataType = ['CHI1', 'CHI2', 'CHI3', 'CHI4', 'CHI5',
                            'CHI21', 'CHI22', 'CHI31', 'CHI32', 'CHI42']

            for dataType in testDataType:

                found = True

                for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES[dataType]):

                    if isinstance(angAtomId, str):
                        if atomId != angAtomId:
                            found = False
                            break

                    else:
                        if not angAtomId.match(atomId):
                            found = False
                            break

                if found:
                    return dataType

        testDataType = ['PHI', 'PSI', 'OMEGA',
                        'CHI1', 'CHI2', 'CHI3', 'CHI4', 'CHI5',
                        'CHI21', 'CHI22', 'CHI31', 'CHI32', 'CHI42']

        for dataType in testDataType:

            found = True

            for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES[dataType]):

                if isinstance(angAtomId, str):
                    if atomId != angAtomId:
                        found = False
                        break

                else:
                    if not angAtomId.match(atomId):
                        found = False
                        break

            if found:
                return None

    elif polynucleotide:

        if lenCommonSeqId == 3:

            # ETA or ETA'
            _seqIds = [s - o for s, o in zip(seqIds, KNOWN_ANGLE_SEQ_OFFSET['ETA'])]
            _commonSeqId = collections.Counter(_seqIds).most_common()

            if len(_commonSeqId) == 1:

                testDataType = ['ETA', "ETA'"]

                for dataType in testDataType:

                    found = True

                    for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES[dataType]):

                        if atomId != angAtomId:
                            found = False
                            break

                    if found:
                        return dataType

        elif lenCommonSeqId == 2:

            # ALPHA or EPSILON or ZETA or THETA or or THETA'
            testDataType = ['ALPHA', 'EPSILON', 'ZETA', 'THETA', "THETA'"]

            for dataType in testDataType:
                _seqIds = [s - o for s, o in zip(seqIds, KNOWN_ANGLE_SEQ_OFFSET[dataType])]
                _commonSeqId = collections.Counter(_seqIds).most_common()

                if len(_commonSeqId) == 1:

                    found = True

                    for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES[dataType]):

                        if atomId != angAtomId:
                            found = False
                            break

                    if found:
                        return dataType

        elif lenCommonSeqId == 1:

            if 'N1' in atomIds:

                found = True

                for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES['CHI']['Y']):

                    if atomId != angAtomId:
                        found = False
                        break

                if found:
                    return 'CHI'

            elif 'N9' in atomIds:

                found = True

                for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES['CHI']['R']):

                    if atomId != angAtomId:
                        found = False
                        break

                if found:
                    return 'CHI'

            else:

                # BETA or GAMMA or DELTA or NU0 or NU1 or NU2 or NU4
                testDataType = ['BETA', 'GAMMA', 'DELTA', 'NU0', 'NU1', 'NU2', 'NU3', 'NU4']

                for dataType in testDataType:

                    found = True

                    for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES[dataType]):

                        if atomId != angAtomId:
                            found = False
                            break

                    if found:
                        return dataType

        testDataType = ['ETA', "ETA'",
                        'ALPHA', 'EPSILON', 'ZETA', 'THETA', "THETA'",
                        'BETA', 'GAMMA', 'DELTA', 'NU0', 'NU1', 'NU2', 'NU3', 'NU4']

        for dataType in testDataType:

            found = True

            for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES[dataType]):

                if isinstance(angAtomId, str):
                    if atomId != angAtomId:
                        found = False
                        break

                else:
                    if not angAtomId.match(atomId):
                        found = False
                        break

            if found:
                return None

        if 'N1' in atomIds:

            found = True

            for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES['CHI']['Y']):

                if atomId != angAtomId:
                    found = False
                    break

            if found:
                return None

        elif 'N9' in atomIds:

            found = True

            for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES['CHI']['R']):

                if atomId != angAtomId:
                    found = False
                    break

            if found:
                return None

    elif carbohydrates:

        if lenCommonSeqId == 2:

            # PHI or PSI or OMEGA
            testDataType = ['PHI', 'PSI', 'OMEGA']

            for dataType in testDataType:
                seqId1 = seqIds[0]
                seqId4 = seqIds[3]

                if seqId1 > seqId4:
                    m = seqId1 - seqId4
                    _seqIds = [s - o * m for s, o in zip(seqIds, KNOWN_ANGLE_CARBO_SEQ_OFFSET[dataType])]
                    _commonSeqId = collections.Counter(_seqIds).most_common()

                    if len(_commonSeqId) == 1:

                        found = True

                        for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_CARBO_ATOM_NAMES[dataType]):

                            if isinstance(angAtomId, str):
                                if atomId != angAtomId:
                                    found = False
                                    break

                            else:
                                if not angAtomId.match(atomId):
                                    found = False
                                    break

                        if found:
                            return dataType

        testDataType = ['PHI', 'PSI', 'OMEGA']

        for dataType in testDataType:

            found = True

            for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_CARBO_ATOM_NAMES[dataType]):

                if isinstance(angAtomId, str):
                    if atomId != angAtomId:
                        found = False
                        break

                else:
                    if not angAtomId.match(atomId):
                        found = False
                        break

            if found:
                return None

    return '.' if lenCommonSeqId == 1 else None


def isLikePheOrTyr(compId, ccU):
    """ Return whether a given comp_id is amino acid with flippable symmetrical ring like phenylalanine or tryrosine.
    """

    if compId in ('PHE', 'TYR'):
        return True

    if ccU.updateChemCompDict(compId):
        _refAtomIdList = [cca[ccU.ccaAtomId] for cca in ccU.lastAtomList]
        if 'CD1' not in _refAtomIdList or 'CD2' not in _refAtomIdList:
            return False
        _compId = ccU.lastChemCompDict.get('_chem_comp.mon_nstd_parent_comp_id', '?')
        return _compId in ('PHE', 'TYR')

    return False


def getRdcCode(atoms):
    """ Return type of residual dipolar coupling restraint.
    """

    if len(atoms) != 2:
        return None

    if any(a is None for a in atoms):
        return None

    atom1 = atoms[0]
    atom2 = atoms[1]

    chain_id_1 = atom1['chain_id']
    chain_id_2 = atom2['chain_id']
    seq_id_1 = atom1['seq_id']
    seq_id_2 = atom2['seq_id']
    atom_id_1 = atom1['atom_id']
    atom_id_2 = atom2['atom_id']

    vector = {atom_id_1, atom_id_2}
    offset = abs(seq_id_1 - seq_id_2)

    if chain_id_1 == chain_id_2:
        if vector == {'H', 'C'} and offset == 1:
            return 'RDC_HNC'
        if vector == {'H', 'N'} and offset == 0:
            return 'RDC_NH'
        if vector == {'C', 'N'} and offset == 1:
            return 'RDC_CN_i_1'
        if vector == {'CA', 'HA'} and offset == 0:
            return 'RDC_CAHA'
        if vector == {'H', 'HA'} and offset == 0:
            return 'RDC_HNHA'
        if vector == {'H', 'HA'} and offset == 1:
            return 'RDC_HNHA_i_1'
        if vector == {'CA', 'C'} and offset == 0:
            return 'RDC_CAC'
        if vector == {'CA', 'N'} and offset == 0:
            return 'RDC_CAN'
        if atom_id_1[0] == atom_id_2[0]:
            if atom_id_1[0] in protonBeginCode:
                return 'RDC_HH'
            if atom_id_1[0] == 'C':
                return 'RDC_CC'
        if offset == 0:
            if atom1['comp_id'] == 'TRP' and vector == {'HE1', 'NE1'}:
                return 'RDC_NH'
            if atom1['comp_id'] == 'ARG' and vector == {'HE', 'NE'}:
                return 'RDC_NH'

    return 'RDC_other'


def startsWithPdbRecord(line):
    """ Return whether a given line string starts with legacy PDB records.
    """

    if any(line.startswith(pdb_record) for pdb_record in LEGACY_PDB_RECORDS):
        return True

    return any(line[:-1] == pdb_record[:-1] for pdb_record in LEGACY_PDB_RECORDS if pdb_record.endswith(' '))


def isCyclicPolymer(cR, polySeq, authAsymId, representativeModelId=1, modelNumName='PDB_model_num'):
    """ Return whether a given chain is cyclic polymer based on coordinate annotation.
    """

    if cR is None or polySeq is None:
        return False

    ps = next((ps for ps in polySeq if ps['auth_chain_id'] == authAsymId), None)

    if ps is None:
        return False

    labelAsymId = ps['chain_id']
    begAuthSeqId = ps['auth_seq_id'][0]
    endAuthSeqId = ps['auth_seq_id'][-1]
    begLabelSeqId = ps['seq_id'][0]
    endLabelSeqId = ps['seq_id'][-1]

    try:

        filterItems = [{'name': 'ptnr1_label_asym_id', 'type': 'str', 'value': labelAsymId},
                       {'name': 'ptnr2_label_asym_id', 'type': 'str', 'value': labelAsymId},
                       {'name': 'ptnr1_label_seq_id', 'type': 'int', 'value': begLabelSeqId},
                       {'name': 'ptnr2_label_seq_id', 'type': 'int', 'value': endLabelSeqId},
                       ]

        if cR.hasItem('struct_conn', 'pdbx_leaving_atom_flag'):
            filterItems.append({'name': 'pdbx_leaving_atom_flag', 'type': 'str', 'value': 'both'})

        struct_conn = cR.getDictListWithFilter('struct_conn',
                                               [{'name': 'conn_type_id', 'type': 'str'}],
                                               filterItems)

    except Exception:
        return False

    if len(struct_conn) == 0:

        try:

            close_contact = cR.getDictListWithFilter('pdbx_validate_close_contact',
                                                     [{'name': 'dist', 'type': 'float'}
                                                      ],
                                                     [{'name': modelNumName, 'type': 'int', 'value': representativeModelId},
                                                      {'name': 'auth_asym_id_1', 'type': 'str', 'value': authAsymId},
                                                      {'name': 'auth_seq_id_1', 'type': 'int', 'value': begAuthSeqId},
                                                      {'name': 'auth_atom_id_1', 'type': 'str', 'value': 'N'},
                                                      {'name': 'auth_asym_id_2', 'type': 'str', 'value': authAsymId},
                                                      {'name': 'auth_seq_id_2', 'type': 'int', 'value': endAuthSeqId},
                                                      {'name': 'auth_atom_id_2', 'type': 'str', 'value': 'C'}
                                                      ])

        except Exception:
            return False

        if len(close_contact) == 0:

            bond = getCoordBondLength(cR, labelAsymId, begLabelSeqId, 'N', labelAsymId, endLabelSeqId, 'C', modelNumName)

            if bond is None:
                return False

            distance = next((b['distance'] for b in bond if b['model_id'] == representativeModelId), None)

            if distance is None:
                return False

            return 1.2 < distance < 1.4

        return 1.2 < close_contact[0]['dist'] < 1.4

    return struct_conn[0]['conn_type_id'] == 'covale'


def getCoordBondLength(cR, labelAsymId1, labelSeqId1, labelAtomId1, labelAsymId2, labelSeqId2, labelAtomId2, modelNumName='PDB_model_num'):
    """ Return the bond length of given two CIF atoms.
        @return: the bond length
    """

    def to_np_array(a):
        """ Return Numpy array of a given Cartesian coordinate in {'x': float, 'y': float, 'z': float} format.
        """
        return numpy.asarray([a['x'], a['y'], a['z']], dtype=float)

    try:

        dataItems = [{'name': 'Cartn_x', 'type': 'float', 'alt_name': 'x'},
                     {'name': 'Cartn_y', 'type': 'float', 'alt_name': 'y'},
                     {'name': 'Cartn_z', 'type': 'float', 'alt_name': 'z'},
                     {'name': modelNumName, 'type': 'int', 'alt_name': 'model_id'}
                     ]

        atom_site_1 = cR.getDictListWithFilter('atom_site',
                                               dataItems,
                                               [{'name': 'label_asym_id', 'type': 'str', 'value': labelAsymId1},
                                                {'name': 'label_seq_id', 'type': 'int', 'value': labelSeqId1},
                                                {'name': 'label_atom_id', 'type': 'str', 'value': labelAtomId1},
                                                {'name': 'label_alt_id', 'type': 'enum', 'enum': ('A')}
                                                ])

        atom_site_2 = cR.getDictListWithFilter('atom_site',
                                               dataItems,
                                               [{'name': 'label_asym_id', 'type': 'str', 'value': labelAsymId2},
                                                {'name': 'label_seq_id', 'type': 'int', 'value': labelSeqId2},
                                                {'name': 'label_atom_id', 'type': 'str', 'value': labelAtomId2},
                                                {'name': 'label_alt_id', 'type': 'enum', 'enum': ('A')}
                                                ])

    except Exception:
        return None

    model_ids = set(a['model_id'] for a in atom_site_1) | set(a['model_id'] for a in atom_site_2)

    bond = []

    for model_id in model_ids:
        a_1 = next((a for a in atom_site_1 if a['model_id'] == model_id), None)
        a_2 = next((a for a in atom_site_2 if a['model_id'] == model_id), None)

        if a_1 is None or a_2 is None:
            continue

        bond.append({'model_id': model_id, 'distance': float(f"{numpy.linalg.norm(to_np_array(a_1) - to_np_array(a_2)):.3f}")})

    if len(bond) > 0:
        return bond

    return None


def getRestraintName(mrSubtype, title=False):
    """ Return human-readable restraint name for a given restraint subtype.
    """

    if mrSubtype.startswith('dist'):
        return "Distance restraints" if title else "distance restraints"
    if mrSubtype.startswith('dihed'):
        return "Dihedral angle restraints" if title else "dihedral angle restraints"
    if mrSubtype.startswith('rdc') and mrSubtype != 'rdc_raw_data':
        return "Residual dipolar coupling restraints" if title else "residual dipolar coupling restraints"
    if mrSubtype == 'rdc_raw_data':
        return "Residual dipolar coupling data" if title else "residual dipolar coupling data"
    if mrSubtype.startswith('plane'):
        return "Planarity constraints" if title else "planarity constraints"
    if mrSubtype.startswith('hbond'):
        return "Hydrogen bond restraints" if title else "hydrogen bond restraints"
    if mrSubtype.startswith('ssbond'):
        return "Disulfide bond constraints" if title else "disulfide bond constraints"
    if mrSubtype.startswith('fchiral'):
        return "Floating chiral stereo assignments" if title else "floating chiral stereo assignments"
    if mrSubtype.startswith('adist'):
        return "Anti-distance restraints" if title else "anti-distance restraints"
    if mrSubtype.startswith('jcoup'):
        return "Scalar J-coupling restraints" if title else "scalar J-coupling restraints"
    if mrSubtype.startswith('hvycs'):
        return "Carbon chemical shift restraints" if title else "carbon chemical shift restraints"
    if mrSubtype.startswith('procs'):
        return "Proton chemical shift restraints" if title else "proton chemical shift restraints"
    if mrSubtype.startswith('rama'):
        return "Dihedral angle database restraints" if title else "dihedral angle database restraints"
    if mrSubtype.startswith('radi'):
        return "Radius of gyration restraints" if title else "radius of gyration restraints"
    if mrSubtype.startswith('diff'):
        return "Diffusion anisotropy restraints" if title else "diffusion anisotropy restraints"
    if mrSubtype.startswith('nbase'):
        return "Nucleic acid base orientation restraints" if title else "nucleic acid base orientation restraints"
    if mrSubtype.startswith('csa'):
        return "Chemical shift anisotropy restraints" if title else "chemical shift anisotropy restraints"
    if mrSubtype.startswith('ang'):
        return "Angle databse restraints" if title else "angle database restraints"
    if mrSubtype.startswith('pre'):
        return "Paramagnetic relaxation enhancement restraints" if title else "paramagnetic relaxation enhancement restraints"
    if mrSubtype.startswith('pcs'):
        return "Pseudocontact shift restraints" if title else "pseudocontact shift restraints"
    if mrSubtype.startswith('prdc'):
        return "Paramagnetic RDC restraints" if title else "paramagnetic RDC restraints"
    if mrSubtype.startswith('pang'):
        return "Paramagnetic angle restraints" if title else "paramagnetic angle restraints"
    if mrSubtype.startswith('pccr'):
        return "Paramagnetic CCR restraints" if title else "paramagnetic CCR restraints"
    if mrSubtype.startswith('geo'):
        return "Coordinate geometry restraints" if title else "coordinate geometry restraints"
    if mrSubtype.startswith('noepk'):
        return "NOESY peak volume restraints"
    if mrSubtype.startswith('saxs'):
        return "Small angle X-ray scattering restraints" if title else "small angle X-ray scattering restraints"
    if mrSubtype == 'heteronucl_noe_data':
        return "Heteronuclear NOE data" if title else "heteronuclear NOE data"
    if mrSubtype == 'heteronucl_t1_data':
        return "Heteronuclear T1 relaxation data" if title else "heteronuclear T1 relaxation data"
    if mrSubtype == 'heteronucl_t2_data':
        return "Heteronuclear T2 relaxation data" if title else "heteronuclear T2 relaxation data"
    if mrSubtype == 'heteronucl_t1r_data':
        return "Heteronuclear T1rho relaxation data" if title else "heteronuclear T1rho relaxation data"
    if mrSubtype == 'order_param_data':
        return "Order parameters" if title else "order parameters"

    raise KeyError(f'Internal restraint subtype {mrSubtype!r} is not defined.')


def contentSubtypeOf(mrSubtype):
    """ Return legitimate content subtype of NmrDpUtility.py for a given internal restraint subtype.
    """

    if mrSubtype in ('dist', 'dihed', 'rdc', 'noepk', 'jcoup', 'hvycs', 'procs', 'csa', 'fchiral', 'saxs'):
        return mrSubtype + '_restraint'

    if mrSubtype == 'hbond':
        return 'dist_restraint'

    if mrSubtype == 'ssbond':
        return 'dist_restraint'

    if mrSubtype == 'prdc':
        return 'rdc_restraint'

    if mrSubtype == 'pcs':
        return 'csp_restraint'

    if mrSubtype == 'pre':
        return 'auto_relax_restraint'

    if mrSubtype == 'pccr':
        return 'ccr_dd_restraint'

    if mrSubtype in ('plane', 'adist', 'rama', 'radi', 'diff', 'nbase', 'ang', 'pang', 'geo'):
        return 'other_restraint'

    raise KeyError(f'Internal restraint subtype {mrSubtype!r} is not defined.')


def incListIdCounter(mrSubtype, listIdCounter, reduced=True):
    """ Increment list id counter for a given internal restraint subtype (default)/content subtype (reduced=False).
    """

    if len(listIdCounter) == 0:
        listIdCounter = {'dist_restraint': 0,
                         'dihed_restraint': 0,
                         'rdc_restraint': 0,
                         'noepk_restraint': 0,
                         'jcoup_restraint': 0,
                         'rdc_raw_data': 0,
                         'csa_restraint': 0,
                         'ddc_restraint': 0,
                         'hvycs_restraint': 0,
                         'procs_restraint': 0,
                         'csp_restraint': 0,
                         'auto_relax_restraint': 0,
                         'heteronucl_noe_data': 0,
                         'heteronucl_t1_data': 0,
                         'heteronucl_t2_data': 0,
                         'heteronucl_t1r_data': 0,
                         'order_param_data': 0,
                         'ccr_d_csa_restraint': 0,
                         'ccr_dd_restraint': 0,
                         'fchiral_restraint': 0,
                         'saxs_restraint': 0,
                         'other_restraint': 0
                         }

    contentSubtype = (contentSubtypeOf(mrSubtype) if reduced else mrSubtype) if mrSubtype is not None else 'other_restraint'

    if contentSubtype is None or contentSubtype not in listIdCounter:
        return listIdCounter

    listIdCounter[contentSubtype] += 1

    return listIdCounter


def decListIdCounter(mrSubtype, listIdCounter, reduced=True):
    """ Decrement list id counter for a given internal restraint subtype (default)/content subtype (reduced=False).
    """

    if len(listIdCounter) == 0:
        listIdCounter = {'dist_restraint': 0,
                         'dihed_restraint': 0,
                         'rdc_restraint': 0,
                         'noepk_restraint': 0,
                         'jcoup_restraint': 0,
                         'rdc_raw_data': 0,
                         'csa_restraint': 0,
                         'ddc_restraint': 0,
                         'hvycs_restraint': 0,
                         'procs_restraint': 0,
                         'csp_restraint': 0,
                         'auto_relax_restraint': 0,
                         'heteronucl_noe_data': 0,
                         'heteronucl_t1_data': 0,
                         'heteronucl_t2_data': 0,
                         'heteronucl_t1r_data': 0,
                         'order_param_data': 0,
                         'ccr_d_csa_restraint': 0,
                         'ccr_dd_restraint': 0,
                         'fchiral_restraint': 0,
                         'saxs_restraint': 0,
                         'other_restraint': 0
                         }

    contentSubtype = (contentSubtypeOf(mrSubtype) if reduced else mrSubtype) if mrSubtype is not None else 'other_restraint'

    if contentSubtype is None or contentSubtype not in listIdCounter:
        return listIdCounter

    listIdCounter[contentSubtype] -= 1

    return listIdCounter


def getSaveframe(mrSubtype, sf_framecode, listId=None, entryId=None, fileName=None,
                 constraintType=None, potentialType=None,
                 rdcCode=None, alignCenter=None, cyanaParameter=None, reduced=True):
    """ Return pynmrstar saveframe for a given internal restraint subtype (default)/content subtype (reduced=False).
        @return: pynmrstar saveframe
    """

    contentSubtype = (contentSubtypeOf(mrSubtype) if reduced else mrSubtype) if mrSubtype is not None else 'other_restraint'

    if contentSubtype is None:
        return None

    if contentSubtype not in NMR_STAR_SF_CATEGORIES:
        return None

    sf = pynmrstar.Saveframe.from_scratch(sf_framecode)
    sf.set_tag_prefix(NMR_STAR_SF_TAG_PREFIXES[contentSubtype])

    for sf_tag_item in NMR_STAR_SF_TAG_ITEMS[contentSubtype]:
        tag_item_name = sf_tag_item['name']

        if tag_item_name == 'Sf_category':
            sf.add_tag(tag_item_name, NMR_STAR_SF_CATEGORIES[contentSubtype])
        elif tag_item_name == 'Sf_framecode':
            sf.add_tag(tag_item_name, sf_framecode)
        elif tag_item_name == 'ID' and listId is not None:
            sf.add_tag(tag_item_name, listId)
        elif tag_item_name == 'Entry_ID' and entryId is not None:
            sf.add_tag(tag_item_name, entryId)
        elif tag_item_name == 'Data_file_name' and fileName is not None:
            sf.add_tag(tag_item_name, re.sub(r'-corrected$', '', fileName) if fileName.endswith('-corrected') else fileName)
        elif tag_item_name == 'Constraint_type' and (mrSubtype == 'hbond'
                                                     or (constraintType is not None
                                                         and constraintType == 'hydrogen bond')):
            sf.add_tag(tag_item_name, 'hydrogen bond')
        elif tag_item_name == 'Constraint_type' and (mrSubtype == 'ssbond'
                                                     or (constraintType is not None
                                                         and constraintType == 'disulfide bond')):
            sf.add_tag(tag_item_name, 'disulfide bond')
        elif tag_item_name == 'Constraint_type' and constraintType is not None and constraintType == 'diselenide bond':
            sf.add_tag(tag_item_name, 'diselenide bond')
        elif tag_item_name == 'Constraint_type' and constraintType is not None and constraintType == 'metal coordination':
            sf.add_tag(tag_item_name, 'metal coordination')
        elif tag_item_name == 'Constraint_type' and mrSubtype.startswith('rdc'):
            sf.add_tag(tag_item_name, 'RDC')
        elif tag_item_name == 'Constraint_type' and constraintType is not None:
            sf.add_tag(tag_item_name, constraintType)
        elif tag_item_name == 'Constraint_type' and mrSubtype.startswith('dist'):
            sf.add_tag(tag_item_name, 'NOE')
        elif tag_item_name == 'Potential_type':
            sf.add_tag(tag_item_name, potentialType)
        elif tag_item_name == 'Homonuclear_NOE_val_type' and mrSubtype.startswith('noepk'):
            sf.add_tag(tag_item_name, 'peak volume')
        elif tag_item_name == 'Val_units' and (mrSubtype.startswith('csa') or mrSubtype in ('pccr', 'ccr_dd_restraint')):
            sf.add_tag(tag_item_name, 'ppm')
        elif tag_item_name == 'Units' and (mrSubtype.startswith('hvycs') or mrSubtype.startswith('procs')):
            sf.add_tag(tag_item_name, 'ppm')
        elif tag_item_name == 'Type' and mrSubtype in ('pcs', 'csp_restraint'):
            sf.add_tag(tag_item_name, 'paramagnetic ligand binding')
        elif tag_item_name == 'Common_relaxation_type_name' and mrSubtype in ('pre', 'auto_relax_restraint'):
            sf.add_tag(tag_item_name, 'paramagnetic relaxation enhancement')
        elif tag_item_name == 'Relaxation_coherence_type' and mrSubtype in ('pre', 'auto_relax_restraint'):
            sf.add_tag(tag_item_name, "S+")
        elif tag_item_name == 'Relaxation_val_units' and mrSubtype in ('pre', 'auto_relax_restraint'):
            sf.add_tag(tag_item_name, 's-1')
        elif tag_item_name == 'Rex_units' and mrSubtype in ('pre', 'auto_relax_restraint'):
            sf.add_tag(tag_item_name, 's-1')
        elif tag_item_name == 'Definition' and contentSubtype == 'other_restraint' and constraintType is not None:
            sf.add_tag(tag_item_name, constraintType)
        elif tag_item_name == 'Tensor_auth_asym_ID' and mrSubtype in ('prdc', 'rdc_restraint') and alignCenter is not None:
            sf.add_tag(tag_item_name, alignCenter['chain_id'])
        elif tag_item_name == 'Tensor_auth_seq_ID' and mrSubtype in ('prdc', 'rdc_restraint') and alignCenter is not None:
            sf.add_tag(tag_item_name, alignCenter['seq_id'])
        elif tag_item_name == 'Tensor_auth_comp_ID' and mrSubtype in ('prdc', 'rdc_restraint') and alignCenter is not None:
            sf.add_tag(tag_item_name, alignCenter['comp_id'])
        elif tag_item_name == 'Tensor_magnitude' and mrSubtype.startswith('rdc') and cyanaParameter is not None:
            sf.add_tag(tag_item_name, cyanaParameter['magnitude'])
        elif tag_item_name == 'Tensor_rhombicity' and mrSubtype.startswith('rdc') and cyanaParameter is not None:
            sf.add_tag(tag_item_name, cyanaParameter['rhombicity'])
        elif tag_item_name == 'Details' and mrSubtype.startswith('rdc') and mrSubtype != 'rdc_raw_data' and rdcCode is not None:
            sf.add_tag(tag_item_name, rdcCode)
        elif tag_item_name == 'Details' and mrSubtype in ('pcs', 'csp_restraint') and cyanaParameter is not None:
            sf.add_tag(tag_item_name, f"Tensor_magnitude {cyanaParameter['magnitude']}, "
                       f"Tensor_rhombicity {cyanaParameter['rhombicity']}, "
                       f"Paramagnetic_center_seq_ID {cyanaParameter['orientation_center_seq_id']}")
        else:
            sf.add_tag(tag_item_name, '.')

    return sf


def getLoop(mrSubtype, reduced=True, hasInsCode=False):
    """ Return pynmrstart loop for a given internal restraint subtype (default)/content subtype (reduced=False)..
        @return: pynmrstar loop
    """

    contentSubtype = contentSubtypeOf(mrSubtype) if reduced else mrSubtype

    if contentSubtype is None:
        return None

    if contentSubtype not in NMR_STAR_LP_CATEGORIES:
        return None

    if contentSubtype == 'other_restraint' and reduced:
        return {'tags': [], 'data': []}  # dictionary for _Other_data_type_list.Text_data

    prefix = NMR_STAR_LP_CATEGORIES[contentSubtype] + '.'

    lp = pynmrstar.Loop.from_scratch()

    tags = [prefix + item['name'] for item in NMR_STAR_LP_KEY_ITEMS[contentSubtype]]
    if hasInsCode and contentSubtype in NMR_STAR_LP_DATA_ITEMS_INS_CODE:
        tags.extend([prefix + item['name'] for item in NMR_STAR_LP_DATA_ITEMS_INS_CODE[contentSubtype]])
    else:
        tags.extend([prefix + item['name'] for item in NMR_STAR_LP_DATA_ITEMS[contentSubtype]])

    for tag in tags:
        lp.add_tag(tag)

    return lp


def getAuxLoops(mrSubtype):
    """ Return pynmrstart auxiliary loops for a given internal restraint subtype.
        @return: pynmrstar loop
    """

    contentSubtype = contentSubtypeOf(mrSubtype)

    if contentSubtype is None:
        return None

    if contentSubtype not in NMR_STAR_AUX_LP_CATEGORIES:
        return None

    aux_lps = []

    for catName in NMR_STAR_AUX_LP_CATEGORIES[contentSubtype]:

        prefix = catName + '.'

        aux_lp = pynmrstar.Loop.from_scratch()

        tags = [prefix + item['name'] for item in NMR_STAR_AUX_LP_KEY_ITEMS[contentSubtype][catName]]
        tags.extend([prefix + item['name'] for item in NMR_STAR_AUX_LP_DATA_ITEMS[contentSubtype][catName]])

        for tag in tags:
            aux_lp.add_tag(tag)

        aux_lps.append(aux_lp)

    return aux_lps


def getStarAtom(authToStarSeq, offsetHolder, atom, aux_atom=None):
    """ Return NMR-STAR sequence including entity ID for a given auth atom of the cooridnates.
        @return: a dictionary of NMR-STAR sequence/entity, None otherwise
    """

    starAtom = copy.copy(atom)

    chainId = atom['chain_id']
    seqId = atom['seq_id']
    if 'comp_id' not in atom:
        atom['comp_id'] = starAtom['comp_id'] = None
    compId = atom['comp_id']
    seqKey = (chainId, seqId, compId)
    if 'atom_id' not in atom:
        starAtom['atom_id'] = None

    has_aux_atom = False
    if aux_atom is not None:
        auxChainId = aux_atom['chain_id']
        auxSeqId = aux_atom['seq_id']
        auxCompId = aux_atom.get('comp_id')
        if chainId == auxChainId and seqId != auxSeqId:
            auxSeqKey = (auxChainId, auxSeqId, auxCompId)
            has_aux_atom = True

    if seqKey in authToStarSeq and chainId not in offsetHolder:
        starAtom['chain_id'], starAtom['seq_id'], starAtom['entity_id'], _ = authToStarSeq[seqKey]
        return starAtom

    if chainId in offsetHolder:
        offset = offsetHolder[chainId]
        seqKey = (chainId, seqId + offset, compId)
        if has_aux_atom:
            auxSeqKey = (auxChainId, auxSeqId + offset, auxCompId)
        if seqKey in authToStarSeq and (not has_aux_atom or (has_aux_atom and auxSeqKey in authToStarSeq)):
            starAtom['chain_id'], starAtom['seq_id'], starAtom['entity_id'], _ = authToStarSeq[seqKey]
            atom['seq_id'] = seqId + offset
            return starAtom

    for offset in range(1, 1000):
        seqKey = (chainId, seqId + offset, compId)
        if has_aux_atom:
            auxSeqKey = (auxChainId, auxSeqId + offset, auxCompId)
        if seqKey in authToStarSeq and (not has_aux_atom or (has_aux_atom and auxSeqKey in authToStarSeq)):
            starAtom['chain_id'], starAtom['seq_id'], starAtom['entity_id'], _ = authToStarSeq[seqKey]
            offsetHolder[chainId] = offset
            atom['seq_id'] = seqId + offset
            return starAtom
        seqKey = (chainId, seqId - offset, compId)
        if has_aux_atom:
            auxSeqKey = (auxChainId, auxSeqId + offset, auxCompId)
        if seqKey in authToStarSeq and (not has_aux_atom or (has_aux_atom and auxSeqKey in authToStarSeq)):
            starAtom['chain_id'], starAtom['seq_id'], starAtom['entity_id'], _ = authToStarSeq[seqKey]
            offsetHolder[chainId] = -offset
            atom['seq_id'] = seqId - offset
            return starAtom

    _seqKey = next((_seqKey for _seqKey in authToStarSeq if chainId == _seqKey[0] and seqId == _seqKey[1]), None)
    if has_aux_atom:
        _auxSeqKey = next((_auxSeqKey for _auxSeqKey in authToStarSeq if auxChainId == _auxSeqKey[0] and auxSeqId == _auxSeqKey[1]), None)

    if _seqKey is not None and (not has_aux_atom or (has_aux_atom and _auxSeqKey is not None)):
        if compId in emptyValue or compId not in monDict3:
            starAtom['chain_id'], starAtom['seq_id'], starAtom['entity_id'], _ = authToStarSeq[_seqKey]
            if compId in emptyValue or compId != _seqKey[2]:
                atom['comp_id'] = starAtom['comp_id'] = _seqKey[2]
            return starAtom

    return None


def getInsCode(authToInsCode, offsetHolder, atom):
    """ Return PDB_ins_code for a given auth atom of the cooridnates.
        @return: PDB_ins_code
    """

    if authToInsCode is None:
        return None

    chainId = atom['chain_id']
    seqId = atom['seq_id']
    compId = atom.get('comp_id')
    seqKey = (chainId, seqId, compId)

    if seqKey in authToInsCode:
        return authToInsCode[seqKey]

    if chainId in offsetHolder:
        offset = offsetHolder[chainId]
        seqKey = (chainId, seqId + offset, compId)
        if seqKey in authToInsCode:
            return authToInsCode[seqKey]

    for offset in range(1, 1000):
        seqKey = (chainId, seqId + offset, compId)
        if seqKey in authToInsCode:
            offsetHolder[chainId] = offset
            return authToInsCode[seqKey]
        seqKey = (chainId, seqId - offset, compId)
        if seqKey in authToInsCode:
            offsetHolder[chainId] = -offset
            return authToInsCode[seqKey]

    _seqKey = next((_seqKey for _seqKey in authToInsCode if chainId == _seqKey[0] and seqId == _seqKey[1]), None)

    if _seqKey is not None:
        if compId in emptyValue or compId not in monDict3:
            if compId in emptyValue or compId != _seqKey[2]:
                atom['comp_id'] = _seqKey[2]
            return authToInsCode[_seqKey]

    return None


def getRow(mrSubtype, id, indexId, combinationId, memberId, code, listId, entryId, dstFunc,
           authToStarSeq, authToInsCode, offsetHolder,
           atom1, atom2=None, atom3=None, atom4=None, atom5=None):
    """ Return row data for a given internal restraint subtype.
        @return: data array
    """

    contentSubtype = contentSubtypeOf(mrSubtype)

    if contentSubtype is None:
        return None

    if contentSubtype == 'other_restraint':
        return None

    has_ins_code = authToInsCode is not None and contentSubtype in NMR_STAR_LP_DATA_ITEMS_INS_CODE

    key_size = len(NMR_STAR_LP_KEY_ITEMS[contentSubtype])
    data_size = len(NMR_STAR_LP_DATA_ITEMS_INS_CODE[contentSubtype]) if has_ins_code else len(NMR_STAR_LP_DATA_ITEMS[contentSubtype])

    float_row_idx = []

    row = [None] * (key_size + data_size)

    row[0] = id

    if combinationId == 'OR' or isinstance(memberId, int):
        if atom1 is not None:
            atom1 = copy.copy(atom1)
        if atom2 is not None:
            atom2 = copy.copy(atom2)
        if atom3 is not None:
            atom3 = copy.copy(atom3)
        if atom4 is not None:
            atom4 = copy.copy(atom4)
        if atom5 is not None:
            atom5 = copy.copy(atom5)

    star_atom1 = star_atom2 = star_atom3 = star_atom4 = star_atom4 = star_atom5 = None
    ins_code1 = ins_code2 = ins_code3 = ins_code4 = ins_code5 = None

    if atom1 is not None:
        star_atom1 = getStarAtom(authToStarSeq, offsetHolder, atom1, atom2)
        if 'atom_id' not in atom1:
            atom1['atom_id'] = None
        if has_ins_code:
            ins_code1 = getInsCode(authToInsCode, offsetHolder, atom1)
    if atom2 is not None:
        star_atom2 = getStarAtom(authToStarSeq, offsetHolder, atom2, atom3)
        if 'atom_id' not in atom2:
            atom2['atom_id'] = None
        if has_ins_code:
            ins_code2 = getInsCode(authToInsCode, offsetHolder, atom2)
    if atom3 is not None:
        star_atom3 = getStarAtom(authToStarSeq, offsetHolder, atom3, atom4)
        if 'atom_id' not in atom3:
            atom3['atom_id'] = None
        if has_ins_code:
            ins_code3 = getInsCode(authToInsCode, offsetHolder, atom3)
    if atom4 is not None:
        star_atom4 = getStarAtom(authToStarSeq, offsetHolder, atom4, atom5)
        if 'atom_id' not in atom4:
            atom4['atom_id'] = None
        if has_ins_code:
            ins_code4 = getInsCode(authToInsCode, offsetHolder, atom4)
    if atom5 is not None:
        star_atom5 = getStarAtom(authToStarSeq, offsetHolder, atom5)
        if 'atom_id' not in atom5:
            atom5['atom_id'] = None
        if has_ins_code:
            ins_code5 = getInsCode(authToInsCode, offsetHolder, atom5)

    if star_atom1 is None and star_atom2 is not None:  # procs
        row[1], row[2], row[3], row[4], row[5] =\
            star_atom2['chain_id'], star_atom2['entity_id'], star_atom2['seq_id'], star_atom2['comp_id'], star_atom2['atom_id']
    elif mrSubtype != 'fchiral':
        if star_atom1 is not None:
            row[1], row[2], row[3], row[4], row[5] =\
                star_atom1['chain_id'], star_atom1['entity_id'], star_atom1['seq_id'], star_atom1['comp_id'], star_atom1['atom_id']
        if star_atom2 is not None:
            row[6], row[7], row[8], row[9], row[10] =\
                star_atom2['chain_id'], star_atom2['entity_id'], star_atom2['seq_id'], star_atom2['comp_id'], star_atom2['atom_id']
    else:
        if star_atom1 is not None:
            row[1], row[2], row[3], row[4], row[5] =\
                star_atom1['chain_id'], star_atom1['entity_id'], star_atom1['seq_id'], star_atom1['comp_id'], star_atom1['auth_atom_id']
        if star_atom2 is not None:
            row[6], row[7], row[8], row[9], row[10] =\
                star_atom2['chain_id'], star_atom2['entity_id'], star_atom2['seq_id'], star_atom2['comp_id'], star_atom2['auth_atom_id']

    if mrSubtype in ('dist', 'dihed', 'rdc', 'hbond', 'ssbond'):
        row[key_size] = indexId

    row[-2] = listId
    row[-1] = entryId

    if mrSubtype in ('dist', 'hbond', 'ssbond'):
        row[key_size + 1] = combinationId
        row[key_size + 2] = memberId
        row[key_size + 3] = code
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size + 4] = dstFunc['target_value']
            float_row_idx.append(key_size + 4)
        if hasKeyValue(dstFunc, 'target_value_uncertainty'):
            row[key_size + 5] = dstFunc['target_value_uncertainty']
            float_row_idx.append(key_size + 5)
        if hasKeyValue(dstFunc, 'lower_linear_limit'):
            row[key_size + 6] = dstFunc['lower_linear_limit']
            float_row_idx.append(key_size + 6)
        if hasKeyValue(dstFunc, 'lower_limit'):
            row[key_size + 7] = dstFunc['lower_limit']
            float_row_idx.append(key_size + 7)
        if hasKeyValue(dstFunc, 'upper_limit'):
            row[key_size + 8] = dstFunc['upper_limit']
            float_row_idx.append(key_size + 8)
        if hasKeyValue(dstFunc, 'upper_linear_limit'):
            row[key_size + 9] = dstFunc['upper_linear_limit']
            float_row_idx.append(key_size + 9)
        if hasKeyValue(dstFunc, 'weight'):
            row[key_size + 10] = dstFunc['weight']
        # Distance_val

        row[key_size + 12], row[key_size + 13], row[key_size + 14], row[key_size + 15] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        if hasKeyValue(atom1, 'auth_atom_id'):
            row[key_size + 16] = atom1['auth_atom_id']
        row[key_size + 17], row[key_size + 18], row[key_size + 19], row[key_size + 20] =\
            atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']
        if hasKeyValue(atom2, 'auth_atom_id'):
            row[key_size + 21] = atom2['auth_atom_id']

        if has_ins_code:
            row[key_size + 22] = ins_code1
            row[key_size + 23] = ins_code2

    elif mrSubtype == 'dihed':
        if atom1 is not None and star_atom3 is not None:
            row[11], row[12], row[13], row[14], row[15] =\
                star_atom3['chain_id'], star_atom3['entity_id'], star_atom3['seq_id'], star_atom3['comp_id'], star_atom3['atom_id']
        elif star_atom5 is not None:  # PPA, phase angle of pseudorotation
            row[11], row[12], row[13], row[14] =\
                star_atom5['chain_id'], star_atom5['entity_id'], star_atom5['seq_id'], star_atom5['comp_id']
        if atom2 is not None and star_atom4 is not None:
            row[16], row[17], row[18], row[19], row[20] =\
                star_atom4['chain_id'], star_atom4['entity_id'], star_atom4['seq_id'], star_atom4['comp_id'], star_atom4['atom_id']
        elif star_atom5 is not None:  # PPA, phase angle of pseudorotation
            row[16], row[17], row[18], row[19] =\
                star_atom5['chain_id'], star_atom5['entity_id'], star_atom5['seq_id'], star_atom5['comp_id']

        row[key_size + 1] = combinationId
        row[key_size + 2] = code
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size + 3] = dstFunc['target_value']
            float_row_idx.append(key_size + 3)
        if hasKeyValue(dstFunc, 'target_value_uncertainty'):
            row[key_size + 4] = dstFunc['target_value_uncertainty']
            float_row_idx.append(key_size + 4)
        if hasKeyValue(dstFunc, 'lower_linear_limit'):
            row[key_size + 5] = dstFunc['lower_linear_limit']
            float_row_idx.append(key_size + 5)
        if hasKeyValue(dstFunc, 'lower_limit'):
            row[key_size + 6] = dstFunc['lower_limit']
            float_row_idx.append(key_size + 6)
        if hasKeyValue(dstFunc, 'upper_limit'):
            row[key_size + 7] = dstFunc['upper_limit']
            float_row_idx.append(key_size + 7)
        if hasKeyValue(dstFunc, 'upper_linear_limit'):
            row[key_size + 8] = dstFunc['upper_linear_limit']
            float_row_idx.append(key_size + 8)
        if hasKeyValue(dstFunc, 'weight'):
            row[key_size + 9] = dstFunc['weight']

        if atom1 is not None:
            row[key_size + 10], row[key_size + 11], row[key_size + 12], row[key_size + 13] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
            if hasKeyValue(atom1, 'auth_atom_id'):
                row[key_size + 14] = atom1['auth_atom_id']
        elif atom5 is not None:  # PPA, phase angle of pseudorotation
            row[key_size + 10], row[key_size + 11], row[key_size + 12] =\
                atom5['chain_id'], atom5['seq_id'], atom5['comp_id']
        if atom2 is not None:
            row[key_size + 15], row[key_size + 16], row[key_size + 17], row[key_size + 18] =\
                atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']
            if hasKeyValue(atom2, 'auth_atom_id'):
                row[key_size + 19] = atom2['auth_atom_id']
        elif atom5 is not None:  # PPA, phase angle of pseudorotation
            row[key_size + 15], row[key_size + 16], row[key_size + 17] =\
                atom5['chain_id'], atom5['seq_id'], atom5['comp_id']
        if atom3 is not None:
            row[key_size + 20], row[key_size + 21], row[key_size + 22], row[key_size + 23] =\
                atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id']
            if hasKeyValue(atom3, 'auth_atom_id'):
                row[key_size + 24] = atom3['auth_atom_id']
        elif atom5 is not None:  # PPA, phase angle of pseudorotation
            row[key_size + 20], row[key_size + 21], row[key_size + 22] =\
                atom5['chain_id'], atom5['seq_id'], atom5['comp_id']
        if atom4 is not None:
            row[key_size + 25], row[key_size + 26], row[key_size + 27], row[key_size + 28] =\
                atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id']
            if hasKeyValue(atom4, 'auth_atom_id'):
                row[key_size + 29] = atom4['auth_atom_id']
        elif atom5 is not None:  # PPA, phase angle of pseudorotation
            row[key_size + 25], row[key_size + 26], row[key_size + 27] =\
                atom5['chain_id'], atom5['seq_id'], atom5['comp_id']
            if hasKeyValue(atom5, 'auth_atom_id'):
                row[key_size + 29] = atom5['auth_atom_id']

        if has_ins_code:
            row[key_size + 30] = ins_code1 if atom1 is not None else ins_code5
            row[key_size + 31] = ins_code2 if atom2 is not None else ins_code5
            row[key_size + 32] = ins_code3 if atom3 is not None else ins_code5
            row[key_size + 33] = ins_code4 if atom4 is not None else ins_code5

    elif mrSubtype == 'rdc':
        row[key_size + 1] = combinationId
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size + 2] = dstFunc['target_value']
            float_row_idx.append(key_size + 2)
        if hasKeyValue(dstFunc, 'target_value_uncertainty'):
            row[key_size + 3] = dstFunc['target_value_uncertainty']
            float_row_idx.append(key_size + 3)
        if hasKeyValue(dstFunc, 'lower_linear_limit'):
            row[key_size + 4] = dstFunc['lower_linear_limit']
            float_row_idx.append(key_size + 4)
        if hasKeyValue(dstFunc, 'lower_limit'):
            row[key_size + 5] = dstFunc['lower_limit']
            float_row_idx.append(key_size + 5)
        if hasKeyValue(dstFunc, 'upper_limit'):
            row[key_size + 6] = dstFunc['upper_limit']
            float_row_idx.append(key_size + 6)
        if hasKeyValue(dstFunc, 'upper_linear_limit'):
            row[key_size + 7] = dstFunc['upper_linear_limit']
            float_row_idx.append(key_size + 7)
        if hasKeyValue(dstFunc, 'weight'):
            row[key_size + 8] = dstFunc['weight']
        # RDC_val
        # RDC_val_err
        # RDC_val_scale_factor
        # RDC_distance_depedent

        row[key_size + 13], row[key_size + 14], row[key_size + 15], row[key_size + 16] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        if hasKeyValue(atom1, 'auth_atom_id'):
            row[key_size + 17] = atom1['auth_atom_id']
        row[key_size + 18], row[key_size + 19], row[key_size + 20], row[key_size + 21] =\
            atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']
        if hasKeyValue(atom2, 'auth_atom_id'):
            row[key_size + 22] = atom2['auth_atom_id']

        if has_ins_code:
            row[key_size + 22] = ins_code1
            row[key_size + 23] = ins_code2

    elif mrSubtype == 'noepk':
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size] = dstFunc['target_value']
            float_row_idx.append(key_size)
        if hasKeyValue(dstFunc, 'target_value_uncertainty'):
            row[key_size + 1] = dstFunc['target_value_uncertainty']
            float_row_idx.append(key_size + 1)
        if hasKeyValue(dstFunc, 'lower_limit'):
            row[key_size + 2] = dstFunc['linear_limit']
            float_row_idx.append(key_size + 2)
        if hasKeyValue(dstFunc, 'upper_limit'):
            row[key_size + 3] = dstFunc['upper_limit']
            float_row_idx.append(key_size + 3)

        row[key_size + 4], row[key_size + 5], row[key_size + 6], row[key_size + 7] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        row[key_size + 8], row[key_size + 9], row[key_size + 10], row[key_size + 11] =\
            atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']

    elif mrSubtype == 'jcoup':
        if star_atom3 is not None:
            row[11], row[12], row[13], row[14], row[15] =\
                star_atom3['chain_id'], star_atom3['entity_id'], star_atom3['seq_id'], star_atom3['comp_id'], star_atom3['atom_id']
        if star_atom4 is not None:
            row[16], row[17], row[18], row[19], row[20] =\
                star_atom4['chain_id'], star_atom4['entity_id'], star_atom4['seq_id'], star_atom4['comp_id'], star_atom4['atom_id']

        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size] = dstFunc['target_value']
            float_row_idx.append(key_size)
        if hasKeyValue(dstFunc, 'target_value_uncertainty'):
            row[key_size + 1] = dstFunc['target_value_uncertainty']
            float_row_idx.append(key_size + 1)
        if hasKeyValue(dstFunc, 'lower_limit'):
            row[key_size + 2] = dstFunc['lower_limit']
            float_row_idx.append(key_size + 2)
        if hasKeyValue(dstFunc, 'upper_limit'):
            row[key_size + 3] = dstFunc['upper_limit']
            float_row_idx.append(key_size + 3)

        row[key_size + 4], row[key_size + 5], row[key_size + 6], row[key_size + 7] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        row[key_size + 8], row[key_size + 9], row[key_size + 10], row[key_size + 11] =\
            atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']
        row[key_size + 12], row[key_size + 13], row[key_size + 14], row[key_size + 15] =\
            atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id']
        row[key_size + 16], row[key_size + 17], row[key_size + 18], row[key_size + 19] =\
            atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id']

    elif mrSubtype == 'csa':
        row[key_size] = atomType = atom1['atom_id'][0]
        row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size + 2] = dstFunc['target_value']
            float_row_idx.append(key_size + 2)
        if hasKeyValue(dstFunc, 'target_value_uncertainty'):
            row[key_size + 3] = dstFunc['target_value_uncertainty']
            float_row_idx.append(key_size + 3)
        # Principal_value_sigma_11_val
        # Principal_value_sigma_22_val
        # Principal_value_sigma_33_val
        # Principal_Euler_angle_alpha_val
        # Principal_Euler_angle_beta_val
        # Principal_Euler_angle_gamma_val
        # Bond_length

        row[key_size + 11], row[key_size + 12], row[key_size + 13], row[key_size + 14] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']

    elif mrSubtype == 'hvycs':
        if star_atom3 is not None:
            row[11], row[12], row[13], row[14], row[15] =\
                star_atom3['chain_id'], star_atom3['entity_id'], star_atom3['seq_id'], star_atom3['comp_id'], star_atom3['atom_id']
        if star_atom4 is not None:
            row[16], row[17], row[18], row[19], row[20] =\
                star_atom4['chain_id'], star_atom4['entity_id'], star_atom4['seq_id'], star_atom4['comp_id'], star_atom4['atom_id']
        if star_atom5 is not None:
            row[21], row[22], row[23], row[24], row[25] =\
                star_atom5['chain_id'], star_atom5['entity_id'], star_atom5['seq_id'], star_atom5['comp_id'], star_atom5['atom_id']

        row[key_size] = dstFunc['ca_shift']
        # CA_chem_shift_val_err
        if hasKeyValue(dstFunc, 'cb_shift'):
            row[key_size + 2] = dstFunc['cb_shift']
        # CB_chem_shift_val_err
        row[key_size + 4], row[key_size + 5], row[key_size + 6], row[key_size + 7] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        row[key_size + 8], row[key_size + 9], row[key_size + 10], row[key_size + 11] =\
            atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']
        row[key_size + 12], row[key_size + 13], row[key_size + 14], row[key_size + 15] =\
            atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id']
        row[key_size + 16], row[key_size + 17], row[key_size + 18], row[key_size + 19] =\
            atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id']
        row[key_size + 20], row[key_size + 21], row[key_size + 22], row[key_size + 23] =\
            atom5['chain_id'], atom5['seq_id'], atom5['comp_id'], atom5['atom_id']

    elif mrSubtype == 'procs':
        row[key_size] = atomType = atom1['atom_id'][0]
        row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        row[key_size + 2] = dstFunc['obs_value'] if atom2 is None else dstFunc['obs_value_2']
        # Chem_shift_val_err

        if atom2 is None:
            row[key_size + 4], row[key_size + 5], row[key_size + 6], row[key_size + 7] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        else:
            row[key_size + 4], row[key_size + 5], row[key_size + 6], row[key_size + 7] =\
                atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']

    elif mrSubtype == 'pcs':
        row[key_size] = atomType = atom1['atom_id'][0]
        row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        # Chem_shift_val
        # Chem_shift_val_err
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size + 4] = dstFunc['target_value']
            float_row_idx.append(key_size + 4)
        if hasKeyValue(dstFunc, 'lower_value') and hasKeyValue(dstFunc, 'upper_value'):
            row[key_size + 5] = (dstFunc['upper_value'] - dstFunc['lower_value']) / 2.0
            float_row_idx.append(key_size + 5)

        row[key_size + 6], row[key_size + 7], row[key_size + 8], row[key_size + 9] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']

    elif mrSubtype == 'pre':
        row[key_size] = atomType = atom1['atom_id'][0]
        row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size + 2] = dstFunc['target_value']
            float_row_idx.append(key_size + 2)
        if hasKeyValue(dstFunc, 'lower_value') and hasKeyValue(dstFunc, 'upper_value'):
            row[key_size + 3] = (dstFunc['upper_value'] - dstFunc['lower_value']) / 2.0
            float_row_idx.append(key_size + 3)
        # Rex_val
        # Rex_val_err

        row[key_size + 6], row[key_size + 7], row[key_size + 8], row[key_size + 9] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']

    elif mrSubtype == 'pccr':
        if star_atom3 is not None:
            row[11], row[12], row[13], row[14], row[15] =\
                star_atom3['chain_id'], star_atom3['entity_id'], star_atom3['seq_id'], star_atom3['comp_id'], star_atom3['atom_id']
        if star_atom4 is not None:
            row[16], row[17], row[18], row[19], row[20] =\
                star_atom4['chain_id'], star_atom4['entity_id'], star_atom4['seq_id'], star_atom4['comp_id'], star_atom4['atom_id']

        row[key_size] = atom1['atom_id']
        # Dipole_1_atom_isotope_number_1
        # Dipole_1_atom_type_2
        # Dipole_1_atom_isotope_number_2
        row[key_size + 4] = atomType = atom3['atom_id'][0]
        row[key_size + 5] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        row[key_size + 6] = atomType = atom4['atom_id'][0]
        row[key_size + 7] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size + 8] = dstFunc['target_value']
            float_row_idx.append(key_size + 8)
        if hasKeyValue(dstFunc, 'lower_value') and hasKeyValue(dstFunc, 'upper_value'):
            row[key_size + 9] = (dstFunc['upper_value'] - dstFunc['lower_value']) / 2.0
            float_row_idx.append(key_size + 9)

        row[key_size + 10], row[key_size + 11], row[key_size + 12], row[key_size + 13] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        # Dipole_1_auth_entity_assembly_ID_2
        # Dipole_1_auth_seq_ID_2
        # Dipole_1_auth_comp_ID_2
        # Dipole_1_auth_atom_ID_2
        row[key_size + 18], row[key_size + 19], row[key_size + 20], row[key_size + 21] =\
            atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id']
        row[key_size + 22], row[key_size + 23], row[key_size + 24], row[key_size + 25] =\
            atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id']

    elif mrSubtype == 'fchiral':
        row[key_size] = code
        row[key_size + 1], row[key_size + 2], row[key_size + 3], row[key_size + 4] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['auth_atom_id']
        row[key_size + 5], row[key_size + 6], row[key_size + 7], row[key_size + 8] =\
            atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['auth_atom_id']

    elif mrSubtype == 'saxs':
        row[1] = code
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size] = dstFunc['target_value']
        if hasKeyValue(dstFunc, 'target_value_uncertainty'):
            row[key_size + 1] = dstFunc['target_value_uncertainty']
        if hasKeyValue(dstFunc, 'weight'):
            row[key_size + 2] = dstFunc['weight']

    if len(float_row_idx) > 0:
        max_eff_digits = 0
        for idx in float_row_idx:
            val = row[idx]
            if '.' in val and val[-1] == '0':
                period = val.index('.')
                last = len(val) - 1
                while val[last] == '0':
                    last -= 1
                eff_digits = last - period
                if eff_digits > 0 and eff_digits > max_eff_digits:
                    max_eff_digits = eff_digits
        for idx in float_row_idx:
            val = row[idx]
            if '.' in val and val[-1] == '0':
                first_digit = val.index('.') + 1
                eff_digits = len(val) - first_digit
                if 0 < max_eff_digits < eff_digits:
                    row[idx] = row[idx][0:first_digit + max_eff_digits]
                else:
                    row[idx] = row[idx][0:first_digit + 1]

    return row


def getDstFuncForHBond(atom1, atom2):
    """ Return default upper/lower limits for a hydrogen bond.
    """

    dstFunc = {"weight": "1.0"}

    atom_id_1_ = atom1['atom_id'][0]
    atom_id_2_ = atom2['atom_id'][0]

    if (atom_id_1_ == 'F' and atom_id_2_ in protonBeginCode) or (atom_id_2_ == 'F' and atom_id_1_ in protonBeginCode):
        dstFunc['lower_limit'] = "1.2"
        dstFunc['upper_limit'] = "1.5"

    elif (atom_id_1_ == 'F' and atom_id_2_ == 'F') or (atom_id_2_ == 'F' and atom_id_1_ == 'F'):
        dstFunc['lower_limit'] = "2.2"
        dstFunc['upper_limit'] = "2.5"

    elif (atom_id_1_ == 'O' and atom_id_2_ in protonBeginCode) or (atom_id_2_ == 'O' and atom_id_1_ in protonBeginCode):
        dstFunc['lower_limit'] = "1.5"
        dstFunc['upper_limit'] = "2.5"

    elif (atom_id_1_ == 'O' and atom_id_2_ == 'N') or (atom_id_2_ == 'O' and atom_id_1_ == 'N'):
        dstFunc['lower_limit'] = "2.5"
        dstFunc['upper_limit'] = "3.5"

    elif (atom_id_1_ == 'O' and atom_id_2_ == 'O') or (atom_id_2_ == 'O' and atom_id_1_ == 'O'):
        dstFunc['lower_limit'] = "2.5"
        dstFunc['upper_limit'] = "3.5"

    elif (atom_id_1_ == 'N' and atom_id_2_ in protonBeginCode) or (atom_id_2_ == 'N' and atom_id_1_ in protonBeginCode):
        dstFunc['lower_limit'] = "1.5"
        dstFunc['upper_limit'] = "2.5"

    elif (atom_id_1_ == 'N' and atom_id_2_ == 'N') or (atom_id_2_ == 'N' and atom_id_1_ == 'N'):
        dstFunc['lower_limit'] = "2.5"
        dstFunc['upper_limit'] = "3.5"

    return dstFunc


def getDstFuncForSsBond(atom1, atom2):
    """ Return default upper/lower limits for a disulfide bond.
    """

    dstFunc = {"weight": "1.0"}

    atom_id_1 = atom1['atom_id']
    atom_id_2 = atom2['atom_id']

    atom_id_1_ = atom_id_1[0]
    atom_id_2_ = atom_id_2[0]

    if atom_id_1_ == 'S' and atom_id_2_ == 'S' and not atom_id_1.startswith('SE') and not atom_id_2.startswith('SE'):
        dstFunc['lower_limit'] = "1.9"
        dstFunc['upper_limit'] = "2.3"

    elif atom_id_1.startswith('SE') and atom_id_2.startswith('SE'):
        dstFunc['lower_limit'] = "2.1"
        dstFunc['upper_limit'] = "2.6"

    return dstFunc


def getRowForStrMr(contentSubtype, id, indexId, memberId, code, listId, entryId,
                   originalTagNames, originalRow,
                   authToStarSeq, authToInsCode, offsetHolder,
                   atoms):
    """ Return row data for a given constraint subtype and corresponding NMR-STAR row.
        @return: data array
    """

    key_size = len(NMR_STAR_LP_KEY_ITEMS[contentSubtype])
    data_size = len(NMR_STAR_LP_DATA_ITEMS[contentSubtype])

    float_row_idx = []

    row = [None] * (key_size + data_size)

    row[0] = id

    atom_dim_num = len(atoms)

    atom1 = atoms[0]
    atom2 = atoms[1] if atom_dim_num > 1 else None
    atom3 = atoms[2] if atom_dim_num > 2 else None
    atom4 = atoms[3] if atom_dim_num > 3 else None
    atom5 = atoms[4] if atom_dim_num > 4 else None

    if code == 'OR' or isinstance(memberId, int):
        if atom1 is not None:
            atom1 = copy.copy(atom1)
        if atom2 is not None:
            atom2 = copy.copy(atom2)
        if atom3 is not None:
            atom3 = copy.copy(atom3)
        if atom4 is not None:
            atom4 = copy.copy(atom4)
        if atom5 is not None:
            atom5 = copy.copy(atom5)

    if isinstance(atom1, list):
        atom1 = atom1[0] if len(atom1) > 0 else None
    if atom2 is not None and isinstance(atom2, list):
        atom2 = atom2[0] if len(atom2) > 0 else None
    if atom3 is not None and isinstance(atom3, list):
        atom3 = atom3[0] if len(atom3) > 0 else None
    if atom4 is not None and isinstance(atom4, list):
        atom4 = atom4[0] if len(atom4) > 0 else None
    if atom5 is not None and isinstance(atom5, list):
        atom5 = atom5[0] if len(atom5) > 0 else None

    star_atom1 = star_atom2 = star_atom3 = star_atom4 = star_atom5 = None
    ins_code1 = ins_code2 = ins_code3 = ins_code4 = None

    if atom1 is not None:
        star_atom1 = getStarAtom(authToStarSeq, offsetHolder, atom1, atom2)
        if 'atom_id' not in atom1:
            atom1['atom_id'] = None
        ins_code1 = getInsCode(authToInsCode, offsetHolder, atom1)
    if atom2 is not None:
        star_atom2 = getStarAtom(authToStarSeq, offsetHolder, atom2, atom3)
        if 'atom_id' not in atom2:
            atom2['atom_id'] = None
        ins_code2 = getInsCode(authToInsCode, offsetHolder, atom2)
    if atom3 is not None:
        star_atom3 = getStarAtom(authToStarSeq, offsetHolder, atom3, atom4)
        if 'atom_id' not in atom3:
            atom3['atom_id'] = None
        ins_code3 = getInsCode(authToInsCode, offsetHolder, atom3)
    if atom4 is not None:
        star_atom4 = getStarAtom(authToStarSeq, offsetHolder, atom4, atom5)
        if 'atom_id' not in atom4:
            atom4['atom_id'] = None
        ins_code4 = getInsCode(authToInsCode, offsetHolder, atom4)
    if atom5 is not None:
        star_atom5 = getStarAtom(authToStarSeq, offsetHolder, atom5)
        if 'atom_id' not in atom5:
            atom5['atom_id'] = None

    if star_atom1 is None and star_atom2 is not None:  # procs
        row[1], row[2], row[3], row[4], row[5] =\
            star_atom2['chain_id'], star_atom2['entity_id'], star_atom2['seq_id'], star_atom2['comp_id'], star_atom2['atom_id']
    elif contentSubtype != 'fchiral_restraint':
        if star_atom1 is not None:
            row[1], row[2], row[3], row[4], row[5] =\
                star_atom1['chain_id'], star_atom1['entity_id'], star_atom1['seq_id'], star_atom1['comp_id'], star_atom1['atom_id']
        if star_atom2 is not None:
            row[6], row[7], row[8], row[9], row[10] =\
                star_atom2['chain_id'], star_atom2['entity_id'], star_atom2['seq_id'], star_atom2['comp_id'], star_atom2['atom_id']
    else:
        if star_atom1 is not None:
            row[1], row[2], row[3], row[4], row[5] =\
                star_atom1['chain_id'], star_atom1['entity_id'], star_atom1['seq_id'], star_atom1['comp_id'], star_atom1['auth_atom_id']
        if star_atom2 is not None:
            row[6], row[7], row[8], row[9], row[10] =\
                star_atom2['chain_id'], star_atom2['entity_id'], star_atom2['seq_id'], star_atom2['comp_id'], star_atom2['auth_atom_id']

    if contentSubtype in ('dist_restraint', 'dihed_restraint', 'rdc_restraint'):
        row[key_size] = indexId

    row[-2] = listId
    row[-1] = entryId

    def getRowValue(tag):
        if tag not in originalTagNames:
            return None

        val = originalRow[originalTagNames.index(tag)]

        if val in emptyValue:
            return None

        return val

    if contentSubtype == 'dist_restraint':
        val = getRowValue('Combination_ID')
        if val is not None:
            row[key_size + 1] = val

        row[key_size + 2] = memberId
        row[key_size + 3] = code

        val = getRowValue('Target_val')
        if val is not None:
            row[key_size + 4] = val
            float_row_idx.append(key_size + 4)
        val = getRowValue('Target_val_uncertainty')
        if val is not None:
            row[key_size + 5] = str(abs(float(val)))
            float_row_idx.append(key_size + 5)
        val = getRowValue('Lower_linear_limit')
        if val is not None:
            row[key_size + 6] = val
            float_row_idx.append(key_size + 6)
        val = getRowValue('Distance_lower_bound_val')
        if val is not None:
            row[key_size + 7] = val
            float_row_idx.append(key_size + 7)
        val = getRowValue('Distance_upper_bound_val')
        if val is not None:
            row[key_size + 8] = val
            float_row_idx.append(key_size + 8)
        val = getRowValue('Upper_linear_limit')
        if val is not None:
            row[key_size + 9] = str(abs(float(val)))
            float_row_idx.append(key_size + 9)
        val = getRowValue('Weight')
        if val is not None:
            row[key_size + 10] = val
        val = getRowValue('Distance_val')
        if val is not None:
            row[key_size + 11] = val

        if atom1 is not None:
            row[key_size + 12], row[key_size + 13], row[key_size + 14], row[key_size + 15] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        if hasKeyValue(atom1, 'auth_atom_id'):
            row[key_size + 16] = atom1['auth_atom_id']
        if atom2 is not None:
            row[key_size + 17], row[key_size + 18], row[key_size + 19], row[key_size + 20] =\
                atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']
        if hasKeyValue(atom2, 'auth_atom_id'):
            row[key_size + 21] = atom2['auth_atom_id']

        if authToInsCode is not None:
            row[key_size + 22] = ins_code1
            row[key_size + 23] = ins_code2

    elif contentSubtype == 'dihed_restraint':
        if star_atom3 is not None:
            row[11], row[12], row[13], row[14], row[15] =\
                star_atom3['chain_id'], star_atom3['entity_id'], star_atom3['seq_id'], star_atom3['comp_id'], star_atom3['atom_id']
        if star_atom4 is not None:
            row[16], row[17], row[18], row[19], row[20] =\
                star_atom4['chain_id'], star_atom4['entity_id'], star_atom4['seq_id'], star_atom4['comp_id'], star_atom4['atom_id']

        val = getRowValue('Combination_ID')
        if val is not None:
            row[key_size + 1] = val
        val = getRowValue('Torsion_angle_name')
        if val is not None:
            row[key_size + 2] = val
        val = getRowValue('Angle_target_val')
        if val is not None:
            row[key_size + 3] = val
            float_row_idx.append(key_size + 3)
        val = getRowValue('Angle_target_val_err')
        if val is not None:
            row[key_size + 4] = str(abs(float(val)))
            float_row_idx.append(key_size + 4)
        val = getRowValue('Angle_lower_linear_limit')
        if val is not None:
            row[key_size + 5] = val
            float_row_idx.append(key_size + 5)
        val = getRowValue('Angle_lower_bound_val')
        if val is not None:
            row[key_size + 6] = val
            float_row_idx.append(key_size + 6)
        val = getRowValue('Angle_upper_bound_val')
        if val is not None:
            row[key_size + 7] = val
            float_row_idx.append(key_size + 7)
        val = getRowValue('Angle_upper_linear_limit')
        if val is not None:
            row[key_size + 8] = val
            float_row_idx.append(key_size + 8)
        val = getRowValue('Weight')
        if val is not None:
            row[key_size + 9] = str(abs(float(val)))

        if atom1 is not None:
            row[key_size + 10], row[key_size + 11], row[key_size + 12], row[key_size + 13] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        if hasKeyValue(atom1, 'auth_atom_id'):
            row[key_size + 14] = atom1['auth_atom_id']
        if atom2 is not None:
            row[key_size + 15], row[key_size + 16], row[key_size + 17], row[key_size + 18] =\
                atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']
        if hasKeyValue(atom2, 'auth_atom_id'):
            row[key_size + 19] = atom2['auth_atom_id']
        if atom3 is not None:
            row[key_size + 20], row[key_size + 21], row[key_size + 22], row[key_size + 23] =\
                atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id']
        if hasKeyValue(atom3, 'auth_atom_id'):
            row[key_size + 24] = atom3['auth_atom_id']
        if atom4 is not None:
            row[key_size + 25], row[key_size + 26], row[key_size + 27], row[key_size + 28] =\
                atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id']
        if hasKeyValue(atom4, 'auth_atom_id'):
            row[key_size + 29] = atom4['auth_atom_id']

        if authToInsCode is not None:
            row[key_size + 30] = ins_code1
            row[key_size + 31] = ins_code2
            row[key_size + 32] = ins_code3
            row[key_size + 33] = ins_code4

    elif contentSubtype == 'rdc_restraint':
        val = getRowValue('Combination_ID')
        if val is not None:
            row[key_size + 1] = val
        val = getRowValue('Target_value')
        if val is not None:
            row[key_size + 2] = str(abs(float(val)))
            float_row_idx.append(key_size + 2)
        val = getRowValue('Target_value_uncertainty')
        if val is not None:
            row[key_size + 3] = val
            float_row_idx.append(key_size + 3)
        val = getRowValue('RDC_lower_linear_limit')
        if val is not None:
            row[key_size + 4] = val
            float_row_idx.append(key_size + 4)
        val = getRowValue('RDC_lower_bound')
        if val is not None:
            row[key_size + 5] = val
            float_row_idx.append(key_size + 5)
        val = getRowValue('RDC_upper_bound')
        if val is not None:
            row[key_size + 6] = val
            float_row_idx.append(key_size + 6)
        val = getRowValue('RDC_upper_linear_limit')
        if val is not None:
            row[key_size + 7] = val
            float_row_idx.append(key_size + 7)
        val = getRowValue('Weight')
        if val is not None:
            row[key_size + 8] = str(abs(float(val)))
        val = getRowValue('RDC_val')
        if val is not None:
            row[key_size + 9] = val
            float_row_idx.append(key_size + 9)
        val = getRowValue('RDC_val_err')
        if val is not None:
            row[key_size + 10] = str(abs(float(val)))
            float_row_idx.append(key_size + 10)
        val = getRowValue('RDC_val_scale_factor')
        if val is not None:
            row[key_size + 11] = str(abs(float(val)))
        val = getRowValue('RDC_distance_dependent')
        if val is not None:
            row[key_size + 12] = val

        if atom1 is not None:
            row[key_size + 13], row[key_size + 14], row[key_size + 15], row[key_size + 16] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        if hasKeyValue(atom1, 'auth_atom_id'):
            row[key_size + 17] = atom1['auth_atom_id']
        if atom2 is not None:
            row[key_size + 18], row[key_size + 19], row[key_size + 20], row[key_size + 21] =\
                atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']
        if hasKeyValue(atom2, 'auth_atom_id'):
            row[key_size + 22] = atom2['auth_atom_id']

        if authToInsCode is not None:
            row[key_size + 23] = ins_code1
            row[key_size + 24] = ins_code2

    elif contentSubtype == 'noepk_restraint':
        val = getRowValue('Val')
        if val is not None:
            row[key_size] = val
            float_row_idx.append(key_size)
        val = getRowValue('Val_err')
        if val is not None:
            row[key_size + 1] = str(abs(float(val)))
            float_row_idx.append(key_size + 1)
        val = getRowValue('Val_min')
        if val is not None:
            row[key_size + 2] = val
            float_row_idx.append(key_size + 2)
        val = getRowValue('Val_max')
        if val is not None:
            row[key_size + 3] = val
            float_row_idx.append(key_size + 3)

        if atom1 is not None:
            row[key_size + 4], row[key_size + 5], row[key_size + 6], row[key_size + 7] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        if atom2 is not None:
            row[key_size + 8], row[key_size + 9], row[key_size + 10], row[key_size + 11] =\
                atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']

    elif contentSubtype == 'jcoup_restraint':
        if star_atom3 is not None:
            row[11], row[12], row[13], row[14], row[15] =\
                star_atom3['chain_id'], star_atom3['entity_id'], star_atom3['seq_id'], star_atom3['comp_id'], star_atom3['atom_id']
        if star_atom4 is not None:
            row[16], row[17], row[18], row[19], row[20] =\
                star_atom4['chain_id'], star_atom4['entity_id'], star_atom4['seq_id'], star_atom4['comp_id'], star_atom4['atom_id']

        val = getRowValue('Coupling_constant_val')
        if val is not None:
            row[key_size] = val
            float_row_idx.append(key_size)
        val = getRowValue('Coupling_constant_err')
        if val is not None:
            row[key_size + 1] = str(abs(float(val)))
            float_row_idx.append(key_size + 1)
        val = getRowValue('Coupling_constant_lower_bound')
        if val is not None:
            row[key_size + 2] = val
            float_row_idx.append(key_size + 2)
        val = getRowValue('Coupling_constant_upper_bound')
        if val is not None:
            row[key_size + 3] = val
            float_row_idx.append(key_size + 3)

        if atom1 is not None:
            row[key_size + 4], row[key_size + 5], row[key_size + 6], row[key_size + 7] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        if atom2 is not None:
            row[key_size + 8], row[key_size + 9], row[key_size + 10], row[key_size + 11] =\
                atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']
        if atom3 is not None:
            row[key_size + 12], row[key_size + 13], row[key_size + 14], row[key_size + 15] =\
                atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id']
        if atom4 is not None:
            row[key_size + 16], row[key_size + 17], row[key_size + 18], row[key_size + 19] =\
                atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id']

    elif contentSubtype == 'rdc_raw_data':
        row[key_size] = getRdcCode([atom1, atom2])
        row[key_size + 1] = atomType = atom1['atom_id'][0]
        row[key_size + 2] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        val = getRowValue('Ambiguity_code_1')
        if val is not None and val in ('1', '2', '3'):
            row[key_size + 3] = val
        row[key_size + 4] = atomType = atom2['atom_id'][0]
        row[key_size + 5] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        val = getRowValue('Ambiguity_code_2')
        if val is not None and val in ('1', '2', '3'):
            row[key_size + 6] = val
            val = getRowValue('Val')
        if val is not None:
            row[key_size + 7] = val
            float_row_idx.append(key_size + 7)
        val = getRowValue('Val_err')
        if val is not None:
            row[key_size + 8] = str(abs(float(val)))
            float_row_idx.append(key_size + 8)
        val = getRowValue('Val_min')
        if val is not None:
            row[key_size + 9] = val
            float_row_idx.append(key_size + 9)
        val = getRowValue('Val_max')
        if val is not None:
            row[key_size + 10] = val
        val = getRowValue('Val_bond_length')
        if val is not None:
            row[key_size + 11] = val

        if atom1 is not None:
            row[key_size + 12], row[key_size + 13], row[key_size + 14], row[key_size + 15] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        if atom2 is not None:
            row[key_size + 16], row[key_size + 17], row[key_size + 18], row[key_size + 19] =\
                atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']

    elif contentSubtype == 'csa_restraint':
        row[key_size] = atomType = atom1['atom_id'][0]
        row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        val = getRowValue('Val')
        if val is not None:
            row[key_size + 2] = val
            float_row_idx.append(key_size + 2)
        val = getRowValue('Val_err')
        if val is not None:
            row[key_size + 3] = str(abs(float(val)))
            float_row_idx.append(key_size + 3)
        val = getRowValue('Principal_value_sigma_11_val')
        if val is not None:
            row[key_size + 4] = val
        val = getRowValue('Principal_value_sigma_22_val')
        if val is not None:
            row[key_size + 5] = val
        val = getRowValue('Principal_value_sigma_33_val')
        if val is not None:
            row[key_size + 6] = val
        val = getRowValue('Principal_Euler_angle_alpha_val')
        if val is not None:
            row[key_size + 7] = val
        val = getRowValue('Principal_Euler_angle_beta_val')
        if val is not None:
            row[key_size + 8] = val
        val = getRowValue('Principal_Euler_angle_gamma_val')
        if val is not None:
            row[key_size + 9] = val
        val = getRowValue('Bond_length')
        if val is not None:
            row[key_size + 10] = val

        if atom1 is not None:
            row[key_size + 11], row[key_size + 12], row[key_size + 13], row[key_size + 14] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']

    elif contentSubtype == 'ddc_restraint':
        val = getRowValue('Dipolar_coupling_code')
        if val is not None:
            row[key_size] = val
        if atom1 is not None:
            row[key_size + 1] = atomType = atom1['atom_id'][0]
            row[key_size + 2] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        val = getRowValue('Ambiguity_code_1')
        if val is not None and val in ('1', '2', '3'):
            row[key_size + 3] = val
        if atom2 is not None:
            row[key_size + 4] = atomType = atom2['atom_id'][0]
            row[key_size + 5] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        val = getRowValue('Ambiguity_code_2')
        if val is not None and val in ('1', '2', '3'):
            row[key_size + 6] = val
        val = getRowValue('Val')
        if val is not None:
            row[key_size + 7] = str(abs(float(val)))
            float_row_idx.append(key_size + 7)
        val = getRowValue('Val_err')
        if val is not None:
            row[key_size + 8] = val
            float_row_idx.append(key_size + 8)
        val = getRowValue('Val_min')
        if val is not None:
            row[key_size + 9] = val
            float_row_idx.append(key_size + 9)
        val = getRowValue('Val_max')
        if val is not None:
            row[key_size + 10] = val
            float_row_idx.append(key_size + 10)
        val = getRowValue('Principal_Euler_angle_alpha_val')
        if val is not None:
            row[key_size + 11] = val
        val = getRowValue('Principal_Euler_angle_beta_val')
        if val is not None:
            row[key_size + 12] = val
        val = getRowValue('Principal_Euler_angle_gamma_val')
        if val is not None:
            row[key_size + 13] = val

    elif contentSubtype == 'hvycs_restraint':
        if star_atom3 is not None:
            row[11], row[12], row[13], row[14], row[15] =\
                star_atom3['chain_id'], star_atom3['entity_id'], star_atom3['seq_id'], star_atom3['comp_id'], star_atom3['atom_id']
        if star_atom4 is not None:
            row[16], row[17], row[18], row[19], row[20] =\
                star_atom4['chain_id'], star_atom4['entity_id'], star_atom4['seq_id'], star_atom4['comp_id'], star_atom4['atom_id']
        if star_atom5 is not None:
            row[21], row[22], row[23], row[24], row[25] =\
                star_atom5['chain_id'], star_atom5['entity_id'], star_atom5['seq_id'], star_atom5['comp_id'], star_atom5['atom_id']

        val = getRowValue('CA_chem_shift_val')
        if val is not None:
            row[key_size] = val
            float_row_idx.append(key_size)
        val = getRowValue('CA_chem_shift_val_err')
        if val is not None:
            row[key_size + 1] = str(abs(float(val)))
            float_row_idx.append(key_size + 1)
        val = getRowValue('CB_chem_shift_val')
        if val is not None:
            row[key_size + 2] = val
            float_row_idx.append(key_size + 2)
        val = getRowValue('CB_chem_shift_val_err')
        if val is not None:
            row[key_size + 3] = str(abs(float(val)))
            float_row_idx.append(key_size + 3)

        if atom1 is not None:
            row[key_size + 4], row[key_size + 5], row[key_size + 6], row[key_size + 7] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        if atom2 is not None:
            row[key_size + 8], row[key_size + 9], row[key_size + 10], row[key_size + 11] =\
                atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']
        if atom3 is not None:
            row[key_size + 12], row[key_size + 13], row[key_size + 14], row[key_size + 15] =\
                atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id']
        if atom4 is not None:
            row[key_size + 16], row[key_size + 17], row[key_size + 18], row[key_size + 19] =\
                atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id']
        if atom5 is not None:
            row[key_size + 20], row[key_size + 21], row[key_size + 22], row[key_size + 23] =\
                atom5['chain_id'], atom5['seq_id'], atom5['comp_id'], atom5['atom_id']

    elif contentSubtype == 'procs_restraint':
        if atom1 is not None:
            row[key_size] = atomType = atom1['atom_id'][0]
            row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        val = getRowValue('Chem_shift_val')
        if val is not None:
            row[key_size + 2] = val
            float_row_idx.append(key_size + 2)
        val = getRowValue('Chem_shift_val_err')
        if val is not None:
            row[key_size + 3] = str(abs(float(val)))
            float_row_idx.append(key_size + 3)

        if atom1 is None:
            row[key_size + 4], row[key_size + 5], row[key_size + 6], row[key_size + 7] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']

    elif contentSubtype == 'csp_restraint':
        if atom1 is not None:
            row[key_size] = atomType = atom1['atom_id'][0]
            row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        val = getRowValue('Chem_shift_val')
        if val is not None:
            row[key_size + 2] = val
            float_row_idx.append(key_size + 2)
        val = getRowValue('Chem_shift_val_err')
        if val is not None:
            row[key_size + 3] = str(abs(float(val)))
            float_row_idx.append(key_size + 3)
        val = getRowValue('Difference_chem_shift_val')
        if val is not None:
            row[key_size + 4] = val
            float_row_idx.append(key_size + 4)
        val = getRowValue('Difference_chem_shift_val_err')
        if val is not None:
            row[key_size + 5] = str(abs(float(val)))
            float_row_idx.append(key_size + 5)

        if atom1 is not None:
            row[key_size + 6], row[key_size + 7], row[key_size + 8], row[key_size + 9] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']

    elif contentSubtype == 'auto_relax_restraint':
        if atom1 is not None:
            row[key_size] = atomType = atom1['atom_id'][0]
            row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        val = getRowValue('Auto_relaxation_val')
        if val is not None:
            row[key_size + 2] = val
            float_row_idx.append(key_size + 2)
        val = getRowValue('Auto_relaxation_val_err')
        if val is not None:
            row[key_size + 3] = str(abs(float(val)))
            float_row_idx.append(key_size + 3)
        val = getRowValue('Rex_val')
        if val is not None:
            row[key_size + 4] = val
            float_row_idx.append(key_size + 4)
        val = getRowValue('Rex_val_err')
        if val is not None:
            row[key_size + 5] = str(abs(float(val)))
            float_row_idx.append(key_size + 5)

        if atom1 is not None:
            row[key_size + 6], row[key_size + 7], row[key_size + 8], row[key_size + 9] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']

    elif contentSubtype == 'heteronucl_noe_data':
        if atom1 is not None:
            row[key_size] = atomType = atom1['atom_id'][0]
            row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        if atom2 is not None:
            row[key_size + 2] = atomType = atom2['atom_id'][0]
            row[key_size + 3] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        val = getRowValue('Val')
        if val is not None:
            row[key_size + 4] = val
            float_row_idx.append(key_size + 4)
        val = getRowValue('Val_err')
        if val is not None:
            row[key_size + 5] = val
            float_row_idx.append(key_size + 5)

        if atom1 is not None:
            row[key_size + 6], row[key_size + 7], row[key_size + 8], row[key_size + 9] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        if atom2 is not None:
            row[key_size + 10], row[key_size + 11], row[key_size + 12], row[key_size + 13] =\
                atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']

    elif contentSubtype == 'heteronucl_t1_data':
        if atom1 is not None:
            row[key_size] = atomType = atom1['atom_id'][0]
            row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        val = getRowValue('Val')
        if val is not None:
            row[key_size + 2] = val
            float_row_idx.append(key_size + 2)
        val = getRowValue('Val_err')
        if val is not None:
            row[key_size + 3] = val
            float_row_idx.append(key_size + 3)

        if atom1 is not None:
            row[key_size + 4], row[key_size + 5], row[key_size + 6], row[key_size + 7] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']

    elif contentSubtype == 'heteronucl_t2_data':
        if atom1 is not None:
            row[key_size] = atomType = atom1['atom_id'][0]
            row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        val = getRowValue('T2_val')
        if val is not None:
            row[key_size + 2] = val
            float_row_idx.append(key_size + 2)
        val = getRowValue('T2_val_err')
        if val is not None:
            row[key_size + 3] = val
            float_row_idx.append(key_size + 3)
        val = getRowValue('Rex_val')
        if val is not None:
            row[key_size + 4] = val
            float_row_idx.append(key_size + 4)
        val = getRowValue('Rex_err')
        if val is not None:
            row[key_size + 5] = val
            float_row_idx.append(key_size + 5)

        if atom1 is not None:
            row[key_size + 6], row[key_size + 7], row[key_size + 8], row[key_size + 9] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']

    elif contentSubtype == 'heteronucl_t1r_data':
        if atom1 is not None:
            row[key_size] = atomType = atom1['atom_id'][0]
            row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        val = getRowValue('T1rho_val')
        if val is not None:
            row[key_size + 2] = val
            float_row_idx.append(key_size + 2)
        val = getRowValue('T1rho_val_err')
        if val is not None:
            row[key_size + 3] = val
            float_row_idx.append(key_size + 3)
        val = getRowValue('Rex_val')
        if val is not None:
            row[key_size + 4] = val
            float_row_idx.append(key_size + 4)
        val = getRowValue('Rex_val_err')
        if val is not None:
            row[key_size + 5] = val
            float_row_idx.append(key_size + 5)

        if atom1 is not None:
            row[key_size + 6], row[key_size + 7], row[key_size + 8], row[key_size + 9] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']

    elif contentSubtype == 'order_param_data':
        if atom1 is not None:
            row[key_size] = atomType = atom1['atom_id'][0]
            row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        val = getRowValue('Order_param_val')
        if val is not None:
            row[key_size + 2] = val
            float_row_idx.append(key_size + 2)
        val = getRowValue('Order_param_val_fit_err')
        if val is not None:
            row[key_size + 3] = val
            float_row_idx.append(key_size + 3)
        val = getRowValue('Tau_e_val')
        if val is not None:
            row[key_size + 4] = val
            float_row_idx.append(key_size + 4)
        val = getRowValue('Tau_e_val_fit_err')
        if val is not None:
            row[key_size + 5] = val
            float_row_idx.append(key_size + 5)
        val = getRowValue('Tau_f_val')
        if val is not None:
            row[key_size + 6] = val
            float_row_idx.append(key_size + 6)
        val = getRowValue('Tau_f_val_fit_err')
        if val is not None:
            row[key_size + 7] = val
            float_row_idx.append(key_size + 7)
        val = getRowValue('Tau_s_val')
        if val is not None:
            row[key_size + 8] = val
            float_row_idx.append(key_size + 8)
        val = getRowValue('Tau_s_val_fit_err')
        if val is not None:
            row[key_size + 9] = val
            float_row_idx.append(key_size + 9)
        val = getRowValue('Rex_val')
        if val is not None:
            row[key_size + 10] = val
            float_row_idx.append(key_size + 10)
        val = getRowValue('Rex_val_fit_err')
        if val is not None:
            row[key_size + 11] = val
            float_row_idx.append(key_size + 11)
        val = getRowValue('Model_free_sum_squared_errs')
        if val is not None:
            row[key_size + 12] = val
            float_row_idx.append(key_size + 12)
        val = getRowValue('Model_fit')
        if val is not None:
            row[key_size + 13] = val
        val = getRowValue('Sf2_val')
        if val is not None:
            row[key_size + 14] = val
            float_row_idx.append(key_size + 14)
        val = getRowValue('Sf2_val_fit_err')
        if val is not None:
            row[key_size + 15] = val
            float_row_idx.append(key_size + 15)
        val = getRowValue('Ss2_val')
        if val is not None:
            row[key_size + 16] = val
            float_row_idx.append(key_size + 16)
        val = getRowValue('Ss2_val_fit_err')
        if val is not None:
            row[key_size + 17] = val
            float_row_idx.append(key_size + 17)
        val = getRowValue('SH2_val')
        if val is not None:
            row[key_size + 18] = val
            float_row_idx.append(key_size + 18)
        val = getRowValue('SH2_val_fit_err')
        if val is not None:
            row[key_size + 19] = val
            float_row_idx.append(key_size + 19)
        val = getRowValue('SN2_val')
        if val is not None:
            row[key_size + 20] = val
            float_row_idx.append(key_size + 20)
        val = getRowValue('SN2_val_fit_err')
        if val is not None:
            row[key_size + 21] = val
            float_row_idx.append(key_size + 21)

        if atom1 is not None:
            row[key_size + 22], row[key_size + 23], row[key_size + 24], row[key_size + 25] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']

    elif contentSubtype.startswith('ccr'):
        if star_atom3 is not None:
            row[11], row[12], row[13], row[14], row[15] =\
                star_atom3['chain_id'], star_atom3['entity_id'], star_atom3['seq_id'], star_atom3['comp_id'], star_atom3['atom_id']
        if star_atom4 is not None:
            row[16], row[17], row[18], row[19], row[20] =\
                star_atom4['chain_id'], star_atom4['entity_id'], star_atom4['seq_id'], star_atom4['comp_id'], star_atom4['atom_id']

        if atom1 is not None:
            row[key_size] = atomType = atom1['atom_id'][0]
            row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        if atom2 is not None:
            row[key_size + 2] = atomType = atom2['atom_id'][0]
            row[key_size + 3] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        if atom3 is not None:
            row[key_size + 4] = atomType = atom3['atom_id'][0]
            row[key_size + 5] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        if atom4 is not None:
            row[key_size + 6] = atomType = atom4['atom_id'][0]
            row[key_size + 7] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        val = getRowValue('Val')
        if val is not None:
            row[key_size + 8] = val
            float_row_idx.append(key_size + 8)
        val = getRowValue('Val_err')
        if val is not None:
            row[key_size + 9] = str(abs(float(val)))
            float_row_idx.append(key_size + 9)

        if atom1 is not None:
            row[key_size + 10], row[key_size + 11], row[key_size + 12], row[key_size + 13] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        if atom2 is not None:
            row[key_size + 14], row[key_size + 15], row[key_size + 16], row[key_size + 17] =\
                atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']
        if atom3 is not None:
            row[key_size + 18], row[key_size + 19], row[key_size + 20], row[key_size + 21] =\
                atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id']
        if atom4 is not None:
            row[key_size + 22], row[key_size + 23], row[key_size + 24], row[key_size + 25] =\
                atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id']

    elif contentSubtype == 'fchiral_restraint':
        val = getRowValue('Stereospecific_assignment_code')
        if val is not None:
            row[key_size] = val
        if atom1 is not None:
            row[key_size + 1], row[key_size + 2], row[key_size + 3], row[key_size + 4] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['auth_atom_id']
        if atom2 is not None:
            row[key_size + 5], row[key_size + 6], row[key_size + 7], row[key_size + 8] =\
                atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['auth_atom_id']

    elif contentSubtype == 'saxs_restraint':
        row[1] = code
        val = getRowValue('Intensity_val')
        if val is not None:
            row[key_size] = val
        val = getRowValue('Intensity_err_val')
        if val is not None:
            row[key_size + 1] = val
        val = getRowValue('Weight_val')
        if val is not None:
            row[key_size + 2] = str(abs(float(val)))

    elif contentSubtype == 'other_restraint':
        if atom1 is not None:
            row[key_size] = atomType = atom1['atom_id'][0]
            row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        val = getRowValue('Val')
        if val is not None:
            row[key_size + 2] = val
            float_row_idx.append(key_size + 2)
        val = getRowValue('Val_err')
        if val is not None:
            row[key_size + 3] = str(abs(float(val)))
            float_row_idx.append(key_size + 3)

    if len(float_row_idx) > 0:
        max_eff_digits = 0
        for idx in float_row_idx:
            val = row[idx]
            if '.' in val and val[-1] == '0':
                period = val.index('.')
                last = len(val) - 1
                while val[last] == '0':
                    last -= 1
                eff_digits = last - period
                if eff_digits > 0 and eff_digits > max_eff_digits:
                    max_eff_digits = eff_digits
        for idx in float_row_idx:
            val = row[idx]
            if '.' in val and val[-1] == '0':
                first_digit = val.index('.') + 1
                eff_digits = len(val) - first_digit
                if 0 < max_eff_digits < eff_digits:
                    row[idx] = row[idx][0:first_digit + max_eff_digits]
                else:
                    row[idx] = row[idx][0:first_digit + 1]

    return row


def getAuxRow(mrSubtype, catName, listId, entryId, inDict):
    """ Return aux row data for a given category.
        @return: data array
    """

    contentSubtype = contentSubtypeOf(mrSubtype)

    if contentSubtype is None:
        return None

    if contentSubtype not in NMR_STAR_AUX_LP_CATEGORIES:
        return None

    if catName not in NMR_STAR_AUX_LP_CATEGORIES[contentSubtype]:
        return None

    key_names = [key['name'] for key in NMR_STAR_AUX_LP_KEY_ITEMS[contentSubtype][catName]]
    data_names = [data['name'] for data in NMR_STAR_AUX_LP_DATA_ITEMS[contentSubtype][catName]]

    key_names.extend(data_names)

    row = [None] * len(key_names)

    row[-2] = listId
    row[-1] = entryId

    for k, v in inDict.items():
        if k in key_names:
            row[key_names.index(k)] = v

    return row


def assignCoordPolymerSequenceWithChainId(caC, nefT, refChainId, seqId, compId, atomId):
    """ Assign polymer sequences of the coordinates.
        @return possible assignments to the coordinate, warning message (None for valid case)
    """

    warningMessage = None

    polySeq = caC['polymer_sequence']
    altPolySeq = caC['alt_polymer_sequence']
    nonPoly = caC['non_polymer']
    branched = caC['branched']
    authToLabelSeq = caC['auth_to_label_seq']

    hasNonPoly = nonPoly is not None and len(nonPoly) > 0
    hasBranched = branched is not None and len(branched) > 0

    nonPolySeq = None

    chainAssign = set()
    _seqId = seqId

    for ps in polySeq:
        chainId, seqId = getRealChainSeqId(nefT.get_ccu(), ps, _seqId, compId)
        if refChainId != chainId:
            continue
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
            if compId in (cifCompId, origCompId):
                if len(nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                    chainAssign.add((chainId, seqId, cifCompId, True))
            elif len(nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
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
                        origCompId = ps['auth_comp_id'][idx]
                        if cifCompId != compId:
                            compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                            if compId in compIds:
                                cifCompId = compId
                                origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                                  if _seqId == seqId and _compId == compId)
                        if compId in (cifCompId, origCompId):
                            if len(nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((chainId, seqId_, cifCompId, True))
                            elif len(nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((chainId, seqId_, cifCompId, True))
                    except IndexError:
                        pass

    if hasNonPoly or hasBranched:

        if hasNonPoly and hasBranched:
            nonPolySeq = nonPoly
            nonPolySeq.extend(branched)
        elif hasNonPoly:
            nonPolySeq = nonPoly
        else:
            nonPolySeq = branched

        for np in nonPolySeq:
            chainId, seqId = getRealChainSeqId(nefT.get_ccu(), np, _seqId, compId, False)
            if refChainId != chainId:
                continue
            if seqId in np['auth_seq_id']:
                idx = np['auth_seq_id'].index(seqId)
                cifCompId = np['comp_id'][idx]
                origCompId = np['auth_comp_id'][idx]
                if 'alt_auth_seq_id' in np and seqId in np['auth_seq_id'] and seqId not in np['alt_auth_seq_id']:
                    seqId = next(_altSeqId for _seqId, _altSeqId in zip(np['auth_seq_id'], np['alt_auth_seq_id']) if _seqId == seqId)
                if compId in (cifCompId, origCompId):
                    if len(nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.add((chainId, seqId, cifCompId, False))
                elif len(nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                    chainAssign.add((chainId, seqId, cifCompId, False))

    if len(chainAssign) == 0:
        for ps in polySeq:
            chainId = ps['chain_id']
            if refChainId != chainId:
                continue
            seqKey = (chainId, _seqId)
            if seqKey in authToLabelSeq:
                _, seqId = authToLabelSeq[seqKey]
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
                    if compId in (cifCompId, origCompId):
                        if len(nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.add((ps['auth_chain_id'], _seqId, cifCompId, True))
                    elif len(nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.add((ps['auth_chain_id'], _seqId, cifCompId, True))

        if nonPolySeq is not None:
            for np in nonPolySeq:
                chainId = np['auth_chain_id']
                if refChainId != chainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in authToLabelSeq:
                    _, seqId = authToLabelSeq[seqKey]
                    if seqId in np['seq_id']:
                        idx = np['seq_id'].index(seqId)
                        cifCompId = np['comp_id'][idx]
                        origCompId = np['auth_comp_id'][idx]
                        if compId in (cifCompId, origCompId):
                            if len(nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((np['auth_chain_id'], _seqId, cifCompId, False))
                        elif len(nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.add((np['auth_chain_id'], _seqId, cifCompId, False))

    if len(chainAssign) == 0 and altPolySeq is not None:
        for ps in altPolySeq:
            chainId = ps['auth_chain_id']
            if refChainId != chainId:
                continue
            if _seqId in ps['auth_seq_id']:
                cifCompId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                if cifCompId != compId:
                    compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                    if compId in compIds:
                        cifCompId = compId
                chainAssign.add((chainId, _seqId, cifCompId, True))

    if len(chainAssign) == 0:
        if seqId == 1 or (refChainId, seqId - 1) in caC['coord_unobs_res']:
            if atomId in aminoProtonCode and atomId != 'H1':
                return assignCoordPolymerSequenceWithChainId(caC, nefT, refChainId, seqId, compId, 'H1')

        if seqId < 1 and len(polySeq) == 1:
            warningMessage = f"[Atom not found] "\
                f"{_seqId}:{compId}:{atomId} is not present in the coordinates. "\
                f"The residue number '{_seqId}' is not present in polymer sequence of chain {refChainId} of the coordinates. "\
                "Please update the sequence in the Macromolecules page."
        else:
            warningMessage = f"[Atom not found] "\
                f"{_seqId}:{compId}:{atomId} is not present in the coordinates."

    return list(chainAssign), warningMessage


def selectCoordAtoms(caC, nefT, chainAssign, seqId, compId, atomId, authAtomId, allowAmbig=True, enableWarning=True, preferPdbxAuthAtomName=False, offset=1):
    """ Select atoms of the coordinates.
        @return atom selection, warning mesage (None for valid case)
    """

    atomSelection = []

    _atomId = atomId

    if preferPdbxAuthAtomName and compId in caC['auth_atom_name_to_id'] and atomId in caC['auth_atom_name_to_id'][compId]:
        atomId = caC['auth_atom_name_to_id'][compId][atomId]

    for chainId, cifSeqId, cifCompId, isPolySeq in chainAssign:

        seqKey, coordAtomSite = getCoordAtomSiteOf(caC, chainId, cifSeqId, True)
        _atomId, _, details = nefT.get_valid_star_atom_in_xplor(cifCompId, atomId, leave_unmatched=True)
        if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
            _atomId, _, details = nefT.get_valid_star_atom_in_xplor(cifCompId, atomId[:-1], leave_unmatched=True)
            if atomId[-1].isdigit() and int(atomId[-1]) <= len(_atomId):
                _atomId = [_atomId[int(atomId[-1]) - 1]]

        if details is not None:
            ccU = nefT.get_ccu()
            _atomId_ = translateToStdAtomName(atomId, cifCompId, ccU=ccU)
            if _atomId_ != atomId:
                if atomId.startswith('HT') and len(_atomId_) == 2:
                    _atomId_ = 'H'
                __atomId = nefT.get_valid_star_atom_in_xplor(cifCompId, _atomId_)[0]
                if coordAtomSite is not None:
                    if any(_atomId_ for _atomId_ in __atomId if _atomId_ in coordAtomSite['atom_id']):
                        _atomId = __atomId
                    elif __atomId[0][0] in protonBeginCode:
                        __bondedTo = ccU.getBondedAtoms(cifCompId, __atomId[0])
                        if len(__bondedTo) > 0 and __bondedTo[0] in coordAtomSite['atom_id']:
                            _atomId = __atomId
            elif coordAtomSite is not None:
                _atomId = []

        if coordAtomSite is not None\
           and not any(_atomId_ for _atomId_ in _atomId if _atomId_ in coordAtomSite['atom_id'])\
           and atomId in coordAtomSite['atom_id']:
            _atomId = [atomId]

        if coordAtomSite is None and not isPolySeq:
            nonPoly = caC['non_polymer']
            branched = caC['branched']

            hasNonPoly = nonPoly is not None and len(nonPoly) > 0
            hasBranched = branched is not None and len(branched) > 0

            if hasNonPoly or hasBranched:
                if hasNonPoly and hasBranched:
                    nonPolySeq = nonPoly
                    nonPolySeq.extend(branched)
                elif hasNonPoly:
                    nonPolySeq = nonPoly
                else:
                    nonPolySeq = branched

                try:
                    for np in nonPolySeq:
                        if np['auth_chain_id'] == chainId and cifSeqId in np['auth_seq_id']:
                            cifSeqId = np['seq_id'][np['auth_seq_id'].index(cifSeqId)]
                            seqKey, coordAtomSite = getCoordAtomSiteOf(caC, chainId, cifSeqId, True)
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
            ps = next((ps for ps in caC['polymer_sequence'] if ps['auth_chain_id'] == chainId), None)
            if ps is not None:
                compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == cifSeqId]
                if compId in compIds:
                    insCode = True
                    cifCompId = compId
            if not multiChain and not insCode:
                if enableWarning:
                    warningMessage = f"[Sequence mismatch] "\
                        f"Residue name {compId!r} of the restraint does not match with {chainId}:{cifSeqId}:{cifCompId} of the coordinates."
                continue

        if lenAtomId == 0:
            if seqId == 1 and isPolySeq and cifCompId == 'ACE' and cifCompId != compId and offset == 0:
                return selectCoordAtoms(caC, nefT, chainAssign, seqId, compId, atomId, allowAmbig, enableWarning, preferPdbxAuthAtomName, offset=1)
            if enableWarning:
                warningMessage = f"[Invalid atom nomenclature] "\
                    f"{seqId}:{compId}:{atomId} is invalid atom nomenclature."
            continue
        if lenAtomId > 1 and not allowAmbig:
            if enableWarning:
                warningMessage = f"[Invalid atom selection] "\
                    f"Ambiguous atom selection '{seqId}:{compId}:{atomId}' is not allowed as a angle restraint."
            continue

        for cifAtomId in _atomId:
            _atomSelection = {'chain_id': chainId, 'seq_id': cifSeqId, 'comp_id': cifCompId,
                              'atom_id': cifAtomId, 'auth_atom_id': authAtomId}
            if _atomSelection not in atomSelection:
                atomSelection.append(_atomSelection)

            warningMessage = testCoordAtomIdConsistency(caC, nefT.get_ccu(), chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, enableWarning)

    return atomSelection, warningMessage


def getRealChainSeqId(ccU, polySeq, seqId, compId=None, isPolySeq=True):
    """ Return effective sequence key according to polymer sequence of the coordinates.
        @return: sequence key
    """

    if compId is not None:
        compId = translateToStdResName(compId, ccU)
    if seqId in polySeq['auth_seq_id']:
        if compId is None:
            return polySeq['auth_chain_id'], seqId
        idx = polySeq['auth_seq_id'].index(seqId)
        if compId in (polySeq['comp_id'][idx], polySeq['auth_comp_id'][idx]):
            return polySeq['auth_chain_id'], seqId
    return polySeq['chain_id' if isPolySeq else 'auth_chain_id'], seqId


def getCoordAtomSiteOf(caC, chainId, seqId, cifCheck=True, asis=True):
    """ Return sequence key and its atom list of the coordinates.
        @return: sequence key, atom list in the sequence
    """

    seqKey = (chainId, seqId)
    coordAtomSite = None
    if cifCheck:
        coordAtomSites = caC['coord_atom_site']
        if asis:
            if seqKey in coordAtomSites:
                coordAtomSite = coordAtomSites[seqKey]
            else:
                labelToAuthSeq = caC['label_to_auth_seq']
                if seqKey in labelToAuthSeq:
                    seqKey = labelToAuthSeq[seqKey]
                    if seqKey in coordAtomSites:
                        coordAtomSite = coordAtomSites[seqKey]
    return seqKey, coordAtomSite


def testCoordAtomIdConsistency(caC, ccU, chainId, seqId, compId, atomId, seqKey, coordAtomSite, enableWarning=True):
    """ Check existence of specified atom in the coordinates.
        @return: waring message (None for valid case)
    """

    found = False

    if coordAtomSite is not None:
        if atomId in coordAtomSite['atom_id']:
            found = True
        elif 'alt_atom_id' in coordAtomSite and atomId in coordAtomSite['alt_atom_id']:
            found = True
        else:
            _seqKey, _coordAtomSite = getCoordAtomSiteOf(caC, chainId, seqId, asis=False)
            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                if atomId in _coordAtomSite['atom_id']:
                    found = True
                    seqKey = _seqKey
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    seqKey = _seqKey

    else:
        _seqKey, _coordAtomSite = getCoordAtomSiteOf(caC, chainId, seqId, asis=False)
        if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
            if atomId in _coordAtomSite['atom_id']:
                found = True
                seqKey = _seqKey
            elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                found = True
                seqKey = _seqKey

    if found:
        return None

    _seqKey, _coordAtomSite = getCoordAtomSiteOf(caC, chainId, seqId, asis=False)
    if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
        if atomId in _coordAtomSite['atom_id']:
            found = True
            seqKey = _seqKey
        elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
            found = True
            seqKey = _seqKey

    if found:
        return None

    if ccU.updateChemCompDict(compId):
        cca = next((cca for cca in ccU.lastAtomList if cca[ccU.ccaAtomId] == atomId), None)
        if cca is not None and seqKey not in caC['coord_unobs_res'] and ccU.lastChemCompDict['_chem_comp.pdbx_release_status'] == 'REL':
            checked = False
            ps = next((ps for ps in caC['polymer_sequence'] if ps['auth_chain_id'] == chainId), None)
            if seqId == 1 or (chainId, seqId - 1) in caC['coord_unobs_res'] or (ps is not None and ps['auth_seq_id'][0] == seqId):
                if aminoProtonCode and atomId != 'H1':
                    testCoordAtomIdConsistency(caC, ccU, chainId, seqId, compId, 'H1', seqKey, coordAtomSite)
                    return None
                if atomId in aminoProtonCode or atomId == 'P' or atomId.startswith('HOP'):
                    checked = True
            if not checked:
                if atomId[0] in protonBeginCode:
                    bondedTo = ccU.getBondedAtoms(compId, atomId)
                    if len(bondedTo) > 0:
                        if coordAtomSite is not None and bondedTo[0] in coordAtomSite['atom_id'] and cca[ccU.ccaLeavingAtomFlag] != 'Y':
                            return f"[Hydrogen not instantiated] "\
                                f"{chainId}:{seqId}:{compId}:{atomId} is not properly instantiated in the coordinates. "\
                                "Please re-upload the model file."
                if enableWarning:
                    if chainId in LARGE_ASYM_ID:
                        return f"[Atom not found] "\
                            f"{chainId}:{seqId}:{compId}:{atomId} is not present in the coordinates."

    return None


def getDistConstraintType(atomSelectionSet, dstFunc, csStat, hint='.'):
    """ Return distance constraint type for _Constraint_file.Constraint_type tag value.
        @return 'hydrogen bond', 'disulfide bond', etc., None for unclassified distance constraint
    """

    if len(atomSelectionSet) != 2:
        return None

    atom1 = atomSelectionSet[0][0]
    atom2 = atomSelectionSet[1][0]

    if atom1 is None or atom2 is None:
        return None

    atom_id_1 = atom1['atom_id'] if 'atom_id' in atom1 else atom1['auth_atom_id']
    atom_id_2 = atom2['atom_id'] if 'atom_id' in atom2 else atom2['auth_atom_id']

    if atom_id_1 is None or atom_id_2 is None:
        return None

    if ('comp_id' in atom1 and atom1['comp_id'] == atom_id_1)\
       or ('comp_id' in atom2 and atom2['comp_id'] == atom_id_2):
        return 'metal coordination'

    upperLimit = 0.0
    if 'upper_limit' in dstFunc and dstFunc['upper_limit'] is not None:
        upperLimit = float(dstFunc['upper_limit'])
    lowerLimit = -1.0
    if 'lower_limit' in dstFunc and dstFunc['lower_limit'] is not None:
        lowerLimit = float(dstFunc['lower_limit'])

    if atom1['chain_id'] == atom2['chain_id'] and atom1['seq_id'] == atom2['seq_id']:
        if upperLimit >= DIST_AMBIG_UP or lowerLimit >= DIST_AMBIG_UP:
            return 'general distance'
        return None

    _hint = hint.lower()

    ambig = len(atomSelectionSet[0]) * len(atomSelectionSet[1]) > 1\
        and (isAmbigAtomSelection(atomSelectionSet[0], csStat)
             or isAmbigAtomSelection(atomSelectionSet[1], csStat))

    if atom1['chain_id'] != atom2['chain_id'] or ambig:
        if (upperLimit >= DIST_AMBIG_UP or ambig) and ('pre' in _hint or 'paramag' in _hint):
            return 'paramagnetic relaxation'
        if (upperLimit >= DIST_AMBIG_UP or ambig) and ('cidnp' in _hint):
            return 'photo cidnp'
        if (upperLimit <= DIST_AMBIG_LOW or upperLimit >= DIST_AMBIG_MED or ambig) and ('csp' in _hint or 'perturb' in _hint):
            return 'chemical shift perturbation'
        if (upperLimit <= DIST_AMBIG_LOW or upperLimit >= DIST_AMBIG_MED or ambig) and 'mutat' in _hint:
            return 'mutation'
        if (upperLimit <= DIST_AMBIG_LOW or upperLimit >= DIST_AMBIG_MED or ambig) and 'protect' in _hint:
            return 'hydrogen exchange protection'
        if atom1['chain_id'] != atom2['chain_id'] and 'symm' in _hint:
            return 'symmetry'

    if 'build' in _hint and 'up' in _hint:
        if 'roe' in _hint:
            return 'ROE build-up'
        return 'NOE build-up'

    if 'not' in _hint and 'seen' in _hint:
        if (upperLimit <= DIST_AMBIG_LOW or upperLimit >= DIST_AMBIG_MED):
            return 'NOE not seen'

    if 'roe' in _hint:
        return 'ROE'

    if upperLimit >= DIST_AMBIG_UP or lowerLimit >= DIST_AMBIG_UP:
        return 'general distance'

    atom_id_1_ = atom_id_1[0]
    atom_id_2_ = atom_id_2[0]

    if upperLimit <= DIST_AMBIG_LOW or upperLimit >= DIST_AMBIG_BND or ambig:

        if upperLimit >= DIST_AMBIG_BND:

            if (atom_id_1 == 'SE' and atom_id_2 == 'SE') or 'diselenide' in _hint:
                return 'general distance'

            if (atom_id_1 == 'SG' and atom_id_2 == 'SG') or ('disulfide' in _hint or ('ss' in _hint and 'bond' in _hint)):
                return 'general distance'

            if (atom_id_1_ == 'F' and atom_id_2_ in protonBeginCode) or (atom_id_2_ == 'F' and atom_id_1_ in protonBeginCode):
                return 'general distance'

            if (atom_id_1_ == 'F' and atom_id_2_ == 'F') or (atom_id_2_ == 'F' and atom_id_1_ == 'F'):
                return 'general distance'

            if (atom_id_1_ == 'O' and atom_id_2_ in protonBeginCode) or (atom_id_2_ == 'O' and atom_id_1_ in protonBeginCode):
                return 'general distance'

            if (atom_id_1_ == 'O' and atom_id_2_ == 'N') or (atom_id_2_ == 'O' and atom_id_1_ == 'N'):
                return 'general distance'

            if (atom_id_1_ == 'O' and atom_id_2_ == 'O') or (atom_id_2_ == 'O' and atom_id_1_ == 'O'):
                return 'general distance'

            if (atom_id_1_ == 'N' and atom_id_2_ in protonBeginCode) or (atom_id_2_ == 'N' and atom_id_1_ in protonBeginCode):
                return 'general distance'

            if (atom_id_1_ == 'N' and atom_id_2_ == 'N') or (atom_id_2_ == 'N' and atom_id_1_ == 'N'):
                return 'general distance'

        if upperLimit >= DIST_AMBIG_MED and lowerLimit <= 0.0:
            return 'general distance'

        return None

    if (atom_id_1 == 'SE' and atom_id_2 == 'SE') or 'diselenide' in _hint:
        return 'diselenide bond'

    if (atom_id_1 == 'SG' and atom_id_2 == 'SG') or ('disulfide' in _hint or ('ss' in _hint and 'bond' in _hint)):
        return 'disulfide bond'

    if (atom_id_1_ == 'F' and atom_id_2_ in protonBeginCode) or (atom_id_2_ == 'F' and atom_id_1_ in protonBeginCode):
        return 'hydrogen bond'

    if (atom_id_1_ == 'F' and atom_id_2_ == 'F') or (atom_id_2_ == 'F' and atom_id_1_ == 'F'):
        return 'hydrogen bond'

    if (atom_id_1_ == 'O' and atom_id_2_ in protonBeginCode) or (atom_id_2_ == 'O' and atom_id_1_ in protonBeginCode):
        return 'hydrogen bond'

    if (atom_id_1_ == 'O' and atom_id_2_ == 'N') or (atom_id_2_ == 'O' and atom_id_1_ == 'N'):
        return 'hydrogen bond'

    if (atom_id_1_ == 'O' and atom_id_2_ == 'O') or (atom_id_2_ == 'O' and atom_id_1_ == 'O'):
        return 'hydrogen bond'

    if (atom_id_1_ == 'N' and atom_id_2_ in protonBeginCode) or (atom_id_2_ == 'N' and atom_id_1_ in protonBeginCode):
        return 'hydrogen bond'

    if (atom_id_1_ == 'N' and atom_id_2_ == 'N') or (atom_id_2_ == 'N' and atom_id_1_ == 'N'):
        return 'hydrogen bond'

    return None


def getPotentialType(fileType, mrSubtype, dstFunc):
    """ Return NMR-STAR potential type for a given function.
        @return potential type, None for unmatched case
    """

    if 'lower_linear_limit' in dstFunc and 'upper_linear_limit' in dstFunc:
        return 'square-well-parabolic-linear'

    if 'lower_linear_limit' in dstFunc:
        return 'lower-bound-parabolic-linear'

    if 'upper_linear_limit' in dstFunc:
        return 'upper-bound-parabolic-linear'

    if 'lower_limit' in dstFunc and 'upper_limit' in dstFunc:
        return 'square-well-parabolic'

    if 'lower_limit' in dstFunc:
        return 'lower-bound-parabolic'

    if 'upper_limit' in dstFunc:
        return 'upper-bound-parabolic'

    if 'target_value' in dstFunc and fileType in ('nm-res-xpl', 'nm-res-cns', 'nmr-star') and mrSubtype == 'dist':
        return 'log-harmonic'

    if 'target_value' in dstFunc and mrSubtype in ('dist', 'dihed', 'rdc'):
        return 'parabolic'

    return None


def getPdbxNmrSoftwareName(name):
    """ Return _pdbx_nmr_software.name enumarated value for a given software name.
    """

    if name == 'AMBER':
        return 'Amber'
    if name == 'BIOSYM':
        return 'Discover'
    if name in 'ISD':
        return 'Inferential Structure Determination (ISD)'
    if name == 'ROSETTA':
        return 'Rosetta'
    if name == 'XPLOR-NIH':
        return 'X-PLOR NIH'
    if name == 'XPLOR-NIH/CNS':
        return 'X-PLOR NIH/CNS'
    return name  # 'CHARMM', 'CNS', 'CYANA', 'DYNAMO', 'PALES', 'TALOS', 'GROMACS', 'SYBYL'


def hasKeyValue(d=None, key=None):
    """ Return whether a given dictionary has effective value for a key.
        @return: True if d[key] has effective value, False otherwise
    """

    if d is None or key is None:
        return False

    if key in d:
        return d[key] is not None

    return False
