##
# File: ChemCompUtil.py
# Date: 18-Feb-2022
#
# Updates:
# 27-Apr-2022  M. Yokochi - enable to use cached data for standard residues
# 11-Nov-2022  M. Yokochi - add getProtonsInSameGroup() (NMR restraint remediation)
# 13-Jun-2023  M. Yokochi - add getEffectiveFormulaWeight()
##
""" Wrapper class for retrieving chemical component dictionary.
    @author: Masashi Yokochi
"""
import os
import sys
import pickle

from rmsd.calculate_rmsd import NAMES_ELEMENT, ELEMENT_WEIGHTS  # noqa: F401 pylint: disable=no-name-in-module, import-error, unused-import


try:
    from wwpdb.utils.config.ConfigInfo import getSiteId
    from wwpdb.utils.config.ConfigInfoApp import ConfigInfoAppCc
    from wwpdb.utils.nmr.io.ChemCompIo import ChemCompReader
    from wwpdb.utils.nmr.AlignUtil import (monDict3,
                                           protonBeginCode)
    cICc = ConfigInfoAppCc(getSiteId())
    CC_CVS_PATH = cICc.get_site_cc_cvs_path()
except ImportError:
    from nmr.io.ChemCompIo import ChemCompReader
    from nmr.AlignUtil import (monDict3,
                               protonBeginCode)
    CC_CVS_PATH = os.path.dirname(__file__) + '/ligand_dict'  # need to setup 'ligand_dict' CCD resource for NMR restraint processing


class ChemCompUtil:
    """ Wrapper class for retrieving chemical component dictionary.
    """

    def __init__(self, verbose=False, log=sys.stderr):

        # pickle file name of cached dictionary for standard residues
        self.__cacheFile = os.path.dirname(__file__) + '/chem_comp_util/std_chem_comp.pkl'

        self.__ccR = ChemCompReader(verbose, log)
        self.__ccR.setCachePath(CC_CVS_PATH)

        self.lastCompId = None
        self.lastStatus = False
        self.lastChemCompDict = None
        self.lastAtomList = None
        self.lastBonds = None

        # taken from wwpdb.apps.ccmodule.io.ChemCompIo
        _chemCompAtomDict = [
            ('_chem_comp_atom.comp_id', '%s', 'str', ''),
            ('_chem_comp_atom.atom_id', '%s', 'str', ''),
            ('_chem_comp_atom.alt_atom_id', '%s', 'str', ''),
            ('_chem_comp_atom.type_symbol', '%s', 'str', ''),
            ('_chem_comp_atom.charge', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_align', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_aromatic_flag', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_leaving_atom_flag', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_stereo_config', '%s', 'str', ''),
            ('_chem_comp_atom.model_Cartn_x', '%s', 'str', ''),
            ('_chem_comp_atom.model_Cartn_y', '%s', 'str', ''),
            ('_chem_comp_atom.model_Cartn_z', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_model_Cartn_x_ideal', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_model_Cartn_y_ideal', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_model_Cartn_z_ideal', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_component_atom_id', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_component_comp_id', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_ordinal', '%s', 'str', ' ')
        ]

        atomId = next(d for d in _chemCompAtomDict if d[0] == '_chem_comp_atom.atom_id')
        self.ccaAtomId = _chemCompAtomDict.index(atomId)

        aromaticFlag = next(d for d in _chemCompAtomDict if d[0] == '_chem_comp_atom.pdbx_aromatic_flag')
        self.ccaAromaticFlag = _chemCompAtomDict.index(aromaticFlag)

        leavingAtomFlag = next(d for d in _chemCompAtomDict if d[0] == '_chem_comp_atom.pdbx_leaving_atom_flag')
        self.ccaLeavingAtomFlag = _chemCompAtomDict.index(leavingAtomFlag)

        typeSymbol = next(d for d in _chemCompAtomDict if d[0] == '_chem_comp_atom.type_symbol')
        self.ccaTypeSymbol = _chemCompAtomDict.index(typeSymbol)

        cartnX = next(d for d in _chemCompAtomDict if d[0] == '_chem_comp_atom.model_Cartn_x')
        cartnY = next(d for d in _chemCompAtomDict if d[0] == '_chem_comp_atom.model_Cartn_y')
        cartnZ = next(d for d in _chemCompAtomDict if d[0] == '_chem_comp_atom.model_Cartn_z')
        self.ccaCartnX = _chemCompAtomDict.index(cartnX)
        self.ccaCartnY = _chemCompAtomDict.index(cartnY)
        self.ccaCartnZ = _chemCompAtomDict.index(cartnZ)

        # taken from wwpdb.apps.ccmodule.io.ChemCompIo
        _chemCompBondDict = [
            ('_chem_comp_bond.comp_id', '%s', 'str', ''),
            ('_chem_comp_bond.atom_id_1', '%s', 'str', ''),
            ('_chem_comp_bond.atom_id_2', '%s', 'str', ''),
            ('_chem_comp_bond.value_order', '%s', 'str', ''),
            ('_chem_comp_bond.pdbx_aromatic_flag', '%s', 'str', ''),
            ('_chem_comp_bond.pdbx_stereo_config', '%s', 'str', ''),
            ('_chem_comp_bond.pdbx_ordinal', '%s', 'str', '')
        ]

        atomId1 = next(d for d in _chemCompBondDict if d[0] == '_chem_comp_bond.atom_id_1')
        self.ccbAtomId1 = _chemCompBondDict.index(atomId1)

        atomId2 = next(d for d in _chemCompBondDict if d[0] == '_chem_comp_bond.atom_id_2')
        self.ccbAtomId2 = _chemCompBondDict.index(atomId2)

        aromaticFlag = next(d for d in _chemCompBondDict if d[0] == '_chem_comp_bond.pdbx_aromatic_flag')
        self.ccbAromaticFlag = _chemCompBondDict.index(aromaticFlag)

        def load_dict_from_pickle(file_name):
            """ Load cached dictionary from pickle file.
            """

            if os.path.exists(file_name):

                with open(file_name, 'rb') as ifh:
                    return pickle.load(ifh)

            return {}

        self.__cachedDict = load_dict_from_pickle(self.__cacheFile)
        self.__failedCompId = []

    def updateChemCompDict(self, compId):
        """ Update CCD information for a given comp_id.
            @return: True for successfully update CCD information or False for the case a given comp_id does not exist in CCD
        """

        if compId is None:
            return False

        compId = compId.upper()

        if compId in self.__failedCompId:
            return False

        if compId != self.lastCompId:
            self.lastStatus = False if '_' in compId else self.__ccR.setCompId(compId)
            self.lastCompId = compId

            if self.lastStatus:
                if compId in self.__cachedDict:
                    self.lastChemCompDict = self.__cachedDict[compId]['chem_comp']
                    self.lastAtomList = self.__cachedDict[compId]['chem_comp_atom']
                    self.lastBonds = self.__cachedDict[compId]['chem_comp_bond']
                else:
                    self.lastChemCompDict = self.__ccR.getChemCompDict()
                    self.lastAtomList = self.__ccR.getAtomList()
                    self.lastBonds = self.__ccR.getBonds()
                    self.__cachedDict[compId] = {'chem_comp': self.lastChemCompDict,
                                                 'chem_comp_atom': self.lastAtomList,
                                                 'chem_comp_bond': self.lastBonds}

            else:
                self.__failedCompId.append(compId)

        return self.lastStatus

    def getMethylAtoms(self, compId):
        """ Return atoms in methyl group of a given comp_id.
        """

        if compId != self.lastCompId and not self.updateChemCompDict(compId):
            return []

        atmList = []

        carbons = (a[self.ccaAtomId] for a in self.lastAtomList if a[self.ccaTypeSymbol] == 'C')

        for carbon in carbons:
            protons = [(b[self.ccbAtomId1] if b[self.ccbAtomId1] != carbon else b[self.ccbAtomId2])
                       for b in self.lastBonds
                       if (b[self.ccbAtomId1] == carbon and b[self.ccbAtomId2][0] in protonBeginCode)
                       or (b[self.ccbAtomId2] == carbon and b[self.ccbAtomId1][0] in protonBeginCode)]
            if len(protons) != 3:
                continue
            atmList.append(carbon)
            atmList.extend(protons)

        return atmList

    def getRepMethylProtons(self, compId):
        """ Return representative protons in methyl group of a given comp_id.
        """

        if compId != self.lastCompId and not self.updateChemCompDict(compId):
            return []

        atmList = []

        carbons = (a[self.ccaAtomId] for a in self.lastAtomList if a[self.ccaTypeSymbol] == 'C')

        for carbon in carbons:
            protons = [(b[self.ccbAtomId1] if b[self.ccbAtomId1] != carbon else b[self.ccbAtomId2])
                       for b in self.lastBonds
                       if (b[self.ccbAtomId1] == carbon and b[self.ccbAtomId2][0] in protonBeginCode)
                       or (b[self.ccbAtomId2] == carbon and b[self.ccbAtomId1][0] in protonBeginCode)]
            if len(protons) != 3:
                continue
            atmList.append(protons[0])

        return atmList

    def getNonRepMethylProtons(self, compId):
        """ Return non-representative protons in methyl group of a given comp_id.
        """

        if compId != self.lastCompId and not self.updateChemCompDict(compId):
            return []

        atmList = []

        carbons = (a[self.ccaAtomId] for a in self.lastAtomList if a[self.ccaTypeSymbol] == 'C')

        for carbon in carbons:
            protons = [(b[self.ccbAtomId1] if b[self.ccbAtomId1] != carbon else b[self.ccbAtomId2])
                       for b in self.lastBonds
                       if (b[self.ccbAtomId1] == carbon and b[self.ccbAtomId2][0] in protonBeginCode)
                       or (b[self.ccbAtomId2] == carbon and b[self.ccbAtomId1][0] in protonBeginCode)]
            if len(protons) != 3:
                continue
            atmList.extend(protons[1:])

        return atmList

    def getBondedAtoms(self, compId, atomId):
        """ Return bonded atoms to a given atom.
        """

        if compId != self.lastCompId and not self.updateChemCompDict(compId):
            return []

        return [(b[self.ccbAtomId1] if b[self.ccbAtomId1] != atomId else b[self.ccbAtomId2])
                for b in self.lastBonds if atomId in (b[self.ccbAtomId1], b[self.ccbAtomId2])]

    def getProtonsInSameGroup(self, compId, atomId, exclSelf=False):
        """ Return protons in the same group of a given comp_id and atom_id.
        """

        if compId != self.lastCompId and not self.updateChemCompDict(compId):
            return []

        allProtons = [a[self.ccaAtomId] for a in self.lastAtomList if a[self.ccaTypeSymbol] == 'H']

        if atomId not in allProtons:
            return []

        bondedTo = self.getBondedAtoms(compId, atomId)[0]
        attached = self.getBondedAtoms(compId, bondedTo)

        return [p for p in attached if p in allProtons and ((exclSelf and p != atomId) or not exclSelf)]

    def hasBond(self, compId, atomId1, atomId2):
        """ Return whether given two atoms are connected by a covalent bond.
        """
        return atomId2 in self.getBondedAtoms(compId, atomId1)

    def getEffectiveFormulaWeight(self, compId):
        """ Return effective formula weight of a given comp_id.
        """

        if not self.updateChemCompDict(compId):
            return 0.0

        if '_chem_comp.formula_weight' not in self.lastChemCompDict:
            return 0.0

        fw = float(self.lastChemCompDict['_chem_comp.formula_weight'])

        leavingTypeSymbols = [a[self.ccaTypeSymbol] for a in self.lastAtomList if a[self.ccaLeavingAtomFlag] == 'Y']

        try:

            for symbol in leavingTypeSymbols:
                fw -= ELEMENT_WEIGHTS[NAMES_ELEMENT[symbol.title()]]

        except KeyError:
            return 0.0

        return fw

    def write_std_dict_as_pickle(self):
        """ Write dictionary for standard residues as pickle file.
        """

        for compId in monDict3:
            self.updateChemCompDict(compId)

        def write_dict_as_pickle(obj, file_name):
            """ Write dictionary as pickle file.
            """

            if isinstance(obj, dict):

                with open(file_name, 'wb') as ofh:
                    pickle.dump(obj, ofh)

        write_dict_as_pickle(self.__cachedDict, self.__cacheFile)
