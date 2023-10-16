##
# File: CifReader.py derived from wwpdb.apps.ccmodule.io.ChemCompIo.py
# Date: 31-May-2010  John Westbrook
#
# Update:
# 06-Aug-2010 - jdw - Generalized construction of methods to apply to any category
#                     Add accessors for lists of dictionaries
# 12-May-2011 - rps - Added check for None when asking for category Object in __getDataList()
# 2012-10-24    RPS   Updated to reflect reorganization of modules in pdbx packages
# 23-Jul-2019   my  - forked original code to wwpdb.util.nmr.CifReader
# 30-Jul-2019   my  - add 'range-float' as filter item type
# 05-Aug-2019   my  - add 'enum' as filter item type
# 28-Jan-2020   my  - add 'withStructConf' option of getPolymerSequence
# 19-Mar-2020   my  - add hasItem()
# 24-Mar-2020   my  - add 'identical_chain_id' in results of getPolymerSequence()
# 15-Apr-2020   my  - add 'total_models' option of getPolymerSequence (DAOTHER-4060)
# 19-Apr-2020   my  - add random rotation test for detection of non-superimposed models (DAOTHER-4060)
# 08-May-2020   my  - make sure parse() is run only once (DAOTHER-5654)
# 20-Nov-2020   my  - additional support for insertion code in getPolymerSequence() (DAOTHER-6128)
# 29-Jun-2021   my  - add 'auth_chain_id', 'identical_auth_chain_id' in results of getPolymerSequence() if possible (DAOTHER-7108)
# 14-Jan-2022   my  - precise RMSD calculation with domain and medoid model identification (DAOTHER-4060, 7544)
# 02-Feb-2022   my  - add 'abs-int', 'abs-float', 'range-int', 'range-abs-int', 'range-abs-float' as filter item types and 'not_equal_to' range filter (NMR restraint remediation)
# 30-Mar-2022   my  - add support for _atom_site.label_alt_id (DAOTHER-4060, 7544, NMR restraint remediation)
# 06-Apr-2022   my  - add support for auth_comp_id (DAOTHER-7690)
# 04-Aug-2022   my  - detect sequence gaps in auth_seq_id, 'gap_in_auth_seq' (NMR restraint remediation)
# 10-Feb-2023   my  - add 'fetch_first_match' filter to process large assembly avoiding forced timeout (NMR restraint remediation)
# 14-Apr-2023   my  - enable to use cache datablock (NMR restraint remediation)
# 19-Apr-2023   my  - support multiple datablock (NMR restraint validation)
# 24-Apr-2023   my  - add 'default' attribute for data items (NMR restraint validation)
##
""" A collection of classes for parsing CIF files.
"""

import sys
import os
import math
import random
import itertools
import hashlib
import collections
import re
import copy
import inspect
import pickle

import numpy as np
from operator import itemgetter

from mmcif.io.PdbxReader import PdbxReader

from sklearn.cluster import DBSCAN
from rmsd.calculate_rmsd import (NAMES_ELEMENT, centroid, check_reflections, rmsd,  # noqa: F401 pylint: disable=no-name-in-module, import-error, unused-import
                                 kabsch_rmsd, quaternion_rmsd,
                                 reorder_hungarian, reorder_brute, reorder_distance)

# must be one of kabsch_rmsd, quaternion_rmsd, None
ROTATION_METHOD = quaternion_rmsd
# must be one of reorder_hungarian, reorder_brute, reorder_distance, None
REORDER_METHOD = reorder_hungarian
# scan through reflections in planes (e.g. Y transformed to -Y -> X, -Y, Z) and axis changes,
# (e.g. X and Z coords exchanged -> Z, Y, X). This will affect stereo-chemistry.
USE_REFLECTIONS = False
# scan through reflections in planes (e.g. Y transformed to -Y -> X, -Y, Z) and axis changes,
# (e.g. X and Z coords exchanged -> Z, Y, X). Stereo-chemistry will be kept.
USE_REFLECTIONS_KEEP_STEREO = False
REORDER = False

LEN_MAJOR_ASYM_ID = 26

SYMBOLS_ELEMENT = {k.upper(): v for k, v in NAMES_ELEMENT.items()}


def M(axis, theta):
    """ Return the rotation matrix associated with counterclockwise rotation about the given axis by theta radians.
    """

    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d

    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


def to_np_array(a):
    """ Return Numpy array of a given Cartesian coordinate in {'x': float, 'y': float, 'z': float} format.
    """

    return np.asarray([a['x'], a['y'], a['z']], dtype=float)


def get_coordinates(p):
    """ Convert list of atoms for RMSD calculation.
        @return: a vector set of the coordinates.
    """

    V = []

    for a in p:
        V.append(to_np_array(a))

    atoms = [SYMBOLS_ELEMENT[a['element']] for a in p]

    V = np.asarray(V)
    atoms = np.asarray(atoms)

    assert V.shape[0] == atoms.size

    return atoms, V


def calculate_rmsd(p, q):
    """ Calculate RMSD of two coordinates.
        @return: RMSD value
    """

    p_atoms, p_coord = get_coordinates(p)
    q_atoms, q_coord = get_coordinates(q)

    p_size = len(p_atoms)
    q_size = len(q_atoms)

    assert p_size > 0 and q_size > 0
    assert p_size == q_size
    assert p_coord.shape[0] == q_coord.shape[0]
    assert np.count_nonzero(p_atoms != q_atoms) == 0 or REORDER

    p_cent = centroid(p_coord)
    q_cent = centroid(q_coord)

    p_coord -= p_cent
    q_coord -= q_cent

    result_rmsd = None

    if USE_REFLECTIONS or USE_REFLECTIONS_KEEP_STEREO:
        if 'rmsd_method' in inspect.getfullargspec(check_reflections).args:  # API changed - detect
            result_rmsd, _, _, q_review = check_reflections(p_atoms, q_atoms,  # pylint: disable=unexpected-keyword-arg
                                                            p_coord, q_coord,
                                                            reorder_method=REORDER_METHOD,
                                                            rmsd_method=ROTATION_METHOD,
                                                            keep_stereo=USE_REFLECTIONS_KEEP_STEREO)
        else:
            result_rmsd, _, _, q_review = check_reflections(p_atoms, q_atoms,  # pylint: disable=unexpected-keyword-arg
                                                            p_coord, q_coord,
                                                            reorder_method=REORDER_METHOD,
                                                            rotation_method=ROTATION_METHOD,
                                                            keep_stereo=USE_REFLECTIONS_KEEP_STEREO)

    elif REORDER:
        q_review = REORDER_METHOD(p_atoms, q_atoms, p_coord, q_coord)
        q_coord = q_coord[q_review]
        q_atoms = q_atoms[q_review]
        assert np.count_nonzero(p_atoms != q_atoms) == 0

    if result_rmsd is not None:
        pass

    elif ROTATION_METHOD is None:
        result_rmsd = rmsd(p_coord, q_coord)

    else:
        result_rmsd = ROTATION_METHOD(p_coord, q_coord)

    return result_rmsd


class CifReader:
    """ Accessor methods for parsing CIF files.
    """

    def __init__(self, verbose=True, log=sys.stdout,
                 use_cache=True,
                 sub_dir_name_for_cache='.'):
        self.__verbose = verbose
        self.__lfh = log

        # whether to use cache file
        self.__use_cache = use_cache

        # sub_directory name for cache file
        self.__sub_dir_name_for_cache = sub_dir_name_for_cache

        # file path
        self.__filePath = None

        # current working directory path
        self.__dirPath = None

        # data block list
        self.__dBlockList = None

        # the primary data block
        self.__dBlock = None

        # hash code of current cif file
        self.__hashCode = None

        # cache file path
        self.__cachePath = None

        # preset values
        self.emptyValue = (None, '', '.', '?', 'null')
        self.trueValue = ('true', 't', 'yes', 'y', '1')

        # allowed item types
        self.itemTypes = ('str', 'bool',
                          'int', 'range-int', 'abs-int', 'range-abs-int',
                          'float', 'range-float', 'abs-float', 'range-abs-float',
                          'enum')

        # random rotation test for detection of non-superimposed models (DAOTHER-4060)
        self.__random_rotaion_test = False
        self.__single_model_rotation_test = True

        if self.__random_rotaion_test:
            self.__lfh.write("+WARNING- CifReader.__init__() Enabled random rotation test\n")
            self.__lfh.write(f"+WARNING- CifReader.__init__() Single model rotation test: {self.__single_model_rotation_test}\n")

        # clustering parameters for recognition of well-defined regions
        self.__min_features_for_clustering = 4
        self.__max_features_for_clustering = 10
        self.__min_samples_for_clustering = 2
        self.__max_samples_for_clustering = 6

        # minimum monomers for domain recognition
        self.__min_monomers_for_domain = 12

        assert self.__min_monomers_for_domain > 6  # must be greater than 6 to prevent the 6xHIS tag from being recognized as a well-defined region

        # criterion for cutoff RMSD value
        self.__rmsd_cutoff = 3.5

        self.__d_cutoff = self.__rmsd_cutoff ** 2

        # criterion for detection of exactly overlaid models
        self.__rmsd_overlaid_exactly = 0.01

    def parse(self, filePath, dirPath=None):
        """ Parse CIF file, and set internal active data block if possible.
            @return: True for success or False otherwise.
        """

        if dirPath is not None:
            if os.path.isdir(dirPath):
                self.__dirPath = dirPath

        if self.__dBlock is not None and self.__filePath == filePath:
            return True

        self.__dBlockList = self.__dBlock = self.__hashCode = None
        self.__filePath = filePath

        try:

            if not os.access(self.__filePath, os.R_OK):
                if self.__verbose:
                    self.__lfh.write(f"+ERROR- CifReader.parse() Missing file {self.__filePath}\n")
                return False

            if self.__use_cache:
                with open(self.__filePath, 'r', encoding='utf-8', errors='ignore') as ifh:
                    self.__hashCode = hashlib.md5(ifh.read().encode('utf-8')).hexdigest()

            return self.__setDataBlock(self.__getDataBlockFromFile())

        except Exception:
            if self.__verbose:
                self.__lfh.write(f"+ERROR- CifReader.parse() Missing file {self.__filePath}\n")
            return False

    def __getDataBlockFromFile(self, blockId=None):
        """ Worker method to read cif file and set the target datablock.
            If no blockId is provided return the first data block.
            @return: target data block
        """

        if self.__use_cache:

            if self.__dirPath is None:
                self.__dirPath = os.path.dirname(self.__filePath)

            cache_dir = os.path.join(self.__dirPath, self.__sub_dir_name_for_cache)

            if not os.path.isdir(cache_dir):
                os.makedirs(cache_dir)

            self.__cachePath = os.path.join(cache_dir, f"{self.__hashCode}{'' if blockId is None else '_' + blockId}.pkl")

            if os.path.exists(self.__cachePath):
                try:
                    with open(self.__cachePath, 'rb') as ifh:
                        dBlock = pickle.load(ifh)
                        if dBlock is not None:
                            return dBlock
                    os.remove(self.__cachePath)
                except Exception:
                    pass

        if self.__dBlockList is None:
            self.__dBlockList = []

            with open(self.__filePath, 'r', encoding='utf-8') as ifh:
                pRd = PdbxReader(ifh)
                pRd.read(self.__dBlockList)

        if blockId is not None:
            for dBlock in self.__dBlockList:
                if dBlock.getType() == 'data' and dBlock.getName() == blockId:
                    return dBlock

        else:
            for dBlock in self.__dBlockList:
                if dBlock.getType() == 'data':
                    return dBlock

        return None

    def __setDataBlock(self, dataBlock=None):
        """ Assigns the input data block as the active internal data block.
            @return: True for success or False otherwise.
        """

        ok = False

        try:

            if dataBlock.getType() == 'data':
                self.__dBlock = dataBlock
                ok = True
                if self.__use_cache and not os.path.exists(self.__cachePath):
                    with open(self.__cachePath, 'wb') as ofh:
                        pickle.dump(dataBlock, ofh)
            else:
                self.__dBlock = None

        except Exception:
            pass

        return ok

    def getFilePath(self):
        """ Return cif file path.
        """

        return self.__filePath

    def getHashCode(self):
        """ Return hash code of the cif file.
        """

        if self.__hashCode is None:
            with open(self.__filePath, 'r', encoding='utf-8', errors='ignore') as ifh:
                self.__hashCode = hashlib.md5(ifh.read().encode('utf-8')).hexdigest()

        return self.__hashCode

    def getDataBlockList(self):
        """ Return whole list of datablock.
        """

        return self.__dBlockList

    def getDataBlock(self, blockId=None):
        """ Return target datablock.
            Return None in case current blockId does not exist or no blockId does not match.
            @return: target data block
        """

        if self.__dBlock is None or self.__dBlock.getType() != 'data':
            return None

        if blockId is None and self.__dBlock.getName() == blockId:
            return self.__dBlock

        dBlock = self.__getDataBlockFromFile(blockId)

        return dBlock if self.__setDataBlock(dBlock) else None

    def hasCategory(self, catName, blockId=None):
        """ Return whether a given category exists.
        """

        if blockId is not None and self.__dBlock is not None and self.__dBlock.getName() != blockId:
            self.__setDataBlock(self.getDataBlock(blockId))

        if self.__dBlock is None:
            return False

        return catName in self.__dBlock.getObjNameList()

    def hasItem(self, catName, itName, blockId=None):
        """ Return whether a given item exists in a category.
        """

        if blockId is not None and self.__dBlock is not None and self.__dBlock.getName() != blockId:
            self.__setDataBlock(self.getDataBlock(blockId))

        if self.__dBlock is None:
            return False

        # get category object
        catObj = self.__dBlock.getObj(catName)

        if catObj is None:
            return False

        len_catName = len(catName) + 2

        return itName in [name[len_catName:] for name in catObj.getItemNameList()]

    def getItemTags(self, catName, blockId=None):
        """ Return item tag names of a given category.
        """

        if blockId is not None and self.__dBlock is not None and self.__dBlock.getName() != blockId:
            self.__setDataBlock(self.getDataBlock(blockId))

        if self.__dBlock is None:
            return []

        # get category object
        catObj = self.__dBlock.getObj(catName)

        if catObj is None:
            return []

        len_catName = len(catName) + 2

        return [name[len_catName:] for name in catObj.getItemNameList()]

    def getRowLength(self, catName, blockId=None):
        """ Return length of rows of a given category.
        """

        if blockId is not None and self.__dBlock is not None and self.__dBlock.getName() != blockId:
            self.__setDataBlock(self.getDataBlock(blockId))

        if self.__dBlock is None:
            return 0

        # get category object
        catObj = self.__dBlock.getObj(catName)

        if catObj is not None:
            return len(catObj.getRowList())

        return 0

    def getDictList(self, catName, blockId=None):
        """ Return a list of dictionaries of a given category.
        """

        dList = []

        if blockId is not None and self.__dBlock is not None and self.__dBlock.getName() != blockId:
            self.__setDataBlock(self.getDataBlock(blockId))

        if self.__dBlock is None:
            return dList

        # get category object
        catObj = self.__dBlock.getObj(catName)

        if catObj is not None:
            len_catName = len(catName) + 2

            # get column name index
            itDict = {}
            itNameList = catObj.getItemNameList()
            for idxIt, itName in enumerate(itNameList):
                itDict[itName[len_catName:]] = idxIt

            # get row list
            rowList = catObj.getRowList()

            for row in rowList:
                tD = {}
                for k, v in itDict.items():
                    tD[k] = row[v]
                dList.append(tD)

        return dList

    def getDictListWithFilter(self, catName, dataItems, filterItems=None, blockId=None):
        """ Return a list of dictionaries of a given category with filter.
        """

        dataNames = [d['name'] for d in dataItems]

        for d in dataItems:
            if d['type'] not in self.itemTypes:
                raise TypeError(f"Type {d['type']} of data item {d['name']} must be one of {self.itemTypes}.")

        if filterItems is not None:
            filterNames = [f['name'] for f in filterItems]

            for f in filterItems:
                if f['type'] not in self.itemTypes:
                    raise TypeError(f"Type {f['type']} of filter item {f['name']} must be one of {self.itemTypes}.")

        dList = []

        if blockId is not None and self.__dBlock is not None and self.__dBlock.getName() != blockId:
            self.__setDataBlock(self.getDataBlock(blockId))

        if self.__dBlock is None:
            return dList

        # get category object
        catObj = self.__dBlock.getObj(catName)

        if catObj is not None:
            len_catName = len(catName) + 2

            # get column name index
            colDict = {}
            fcolDict = {}
            fetchDict = {}  # 'fetch_first_match': True

            itNameList = [name[len_catName:] for name in catObj.getItemNameList()]

            for idxIt, itName in enumerate(itNameList):
                if itName in dataNames:
                    colDict[itName] = idxIt
                if filterItems is not None and itName in filterNames:
                    fcolDict[itName] = idxIt

            if set(dataNames) & set(itNameList) != set(dataNames):
                raise LookupError(f"Missing one of data items {dataNames}.")

            if filterItems is not None and set(filterNames) & set(itNameList) != set(filterNames):
                raise LookupError(f"Missing one of filter items {filterNames}.")

            # get row list
            rowList = catObj.getRowList()

            abort = False

            for row in rowList:
                keep = True
                if filterItems is not None:
                    for filterItem in filterItems:
                        name = filterItem['name']
                        val = row[fcolDict[name]]
                        if val in self.emptyValue:
                            if 'value' in filterItem and filterItem['value'] not in self.emptyValue:
                                keep = False
                                break
                        else:
                            filterItemType = filterItem['type']
                            if filterItemType in ('str', 'enum'):
                                pass
                            elif filterItemType == 'bool':
                                val = val.lower() in self.trueValue
                            elif filterItemType == 'int':
                                val = int(val)
                            elif filterItemType == 'float':
                                val = float(val)
                            elif filterItemType in ('abs-int', 'range-abs-int'):
                                val = abs(int(val))
                            else:  # 'range-float', 'range-abs-float'
                                val = abs(float(val))
                            if filterItemType in ('range-int', 'range-abs-int', 'range-float', 'range-abs-float'):
                                _range = filterItem['range']
                                if ('min_exclusive' in _range and val <= _range['min_exclusive'])\
                                   or ('min_inclusive' in _range and val < _range['min_inclusive'])\
                                   or ('max_inclusive' in _range and val > _range['max_inclusive'])\
                                   or ('max_exclusive' in _range and val >= _range['max_exclusive'])\
                                   or ('not_equal_to' in _range and val == _range['not_equal_to']):
                                    keep = False
                                    break
                            elif filterItemType == 'enum':
                                if val not in filterItem['enum']:
                                    keep = False
                                    break
                                if 'fetch_first_match' in filterItem and filterItem['fetch_first_match']:
                                    if name not in fetchDict:
                                        fetchDict[name] = val
                                    elif val != fetchDict[name]:
                                        keep = False
                                        abort = True
                                        break
                            else:
                                if val != filterItem['value']:
                                    keep = False
                                    break
                                if 'fetch_first_match' in filterItem and filterItem['fetch_first_match']:
                                    if name not in fetchDict:
                                        fetchDict[name] = val
                                    elif val != fetchDict[name]:
                                        keep = False
                                        abort = True
                                        break

                if keep:
                    tD = {}
                    for dataItem in dataItems:
                        val = row[colDict[dataItem['name']]]
                        if val in self.emptyValue:
                            val = None if 'default' not in dataItem else dataItem['default']
                        dataItemType = dataItem['type']
                        if dataItemType in ('str', 'enum'):
                            pass
                        elif dataItemType == 'bool':
                            val = val.lower() in self.trueValue
                        elif dataItemType == 'int' and val is not None:
                            val = int(val)
                        elif val is not None:
                            val = float(val)
                        if 'alt_name' in dataItem:
                            tD[dataItem['alt_name']] = val
                        else:
                            tD[dataItem['name']] = val
                    dList.append(tD)

                elif abort:
                    break

        return dList

    def getPolymerSequence(self, catName, keyItems, withStructConf=False, withRmsd=False, alias=False, total_models=1):
        """ Extracts sequence from a given loop in a CIF file
        """

        keyNames = [k['name'] for k in keyItems]

        len_key = len(keyItems)

        asm = []  # assembly of a loop

        if self.__dBlock is None:
            return asm

        # get category object
        catObj = self.__dBlock.getObj(catName)

        if catObj is not None:
            len_catName = len(catName) + 2

            # get column name index
            itDict = {}
            altDict = {}

            itNameList = [name[len_catName:] for name in catObj.getItemNameList()]

            for idxIt, itName in enumerate(itNameList):
                itDict[itName] = idxIt
                if itName in keyNames:
                    altDict[next(k['alt_name'] for k in keyItems if k['name'] == itName)] = idxIt

            if set(keyNames) & set(itDict.keys()) != set(keyNames):
                raise LookupError(f"Missing one of data items {keyNames}.")

            # get row list
            rowList = catObj.getRowList()

            for row in rowList:
                for j in range(len_key):
                    itCol = itDict[keyNames[j]]
                    if itCol < len(row) and row[itCol] in self.emptyValue:
                        if 'default' not in keyItems[j] or keyItems[j]['default'] not in self.emptyValue:
                            raise ValueError(f"{keyNames[j]} must not be empty.")

            compDict = {}
            seqDict = {}
            insCodeDict = {}
            labelSeqDict = {}

            authChainDict = {}

            chain_id_col = altDict['chain_id']
            seq_id_col = altDict['seq_id']
            comp_id_col = altDict['comp_id']
            ins_code_col = -1 if 'ins_code' not in altDict else altDict['ins_code']
            label_seq_col = seq_id_col if 'label_seq_id' not in altDict else altDict['label_seq_id']
            auth_chain_id_col = -1 if 'auth_chain_id' not in altDict else altDict['auth_chain_id']
            auth_seq_id_col = -1 if 'auth_seq_id' not in altDict else altDict['auth_seq_id']
            auth_comp_id_col = -1 if 'auth_comp_id' not in altDict else altDict['auth_comp_id']

            chainIds = sorted(set(row[chain_id_col] for row in rowList), key=lambda x: (len(x), x))

            if ins_code_col == -1:
                if catName == 'pdbx_nonpoly_scheme':
                    sortedSeq = sorted(set((row[chain_id_col], int(row[seq_id_col]), row[comp_id_col]) for row in rowList),
                                       key=itemgetter(1))
                else:
                    sortedSeq = sorted(set((row[chain_id_col], int(row[seq_id_col]), row[comp_id_col]) for row in rowList),
                                       key=lambda x: (len(x[0]), x[0], x[1]))

                keyDict = {(row[chain_id_col], int(row[seq_id_col])): row[comp_id_col] for row in rowList}

                for row in rowList:
                    key = (row[chain_id_col], int(row[seq_id_col]))
                    if keyDict[key] != row[comp_id_col]:
                        raise KeyError(f"Sequence must be unique. {itNameList[chain_id_col]} {row[chain_id_col]}, "
                                       f"{itNameList[seq_id_col]} {row[seq_id_col]}, "
                                       f"{itNameList[comp_id_col]} {row[comp_id_col]} vs {keyDict[key]}.")

                for c in chainIds:
                    compDict[c] = [x[2] for x in sortedSeq if x[0] == c]
                    seqDict[c] = [x[1] for x in sortedSeq if x[0] == c]

            else:
                if catName == 'pdbx_nonpoly_scheme':
                    sortedSeq = sorted(set((row[chain_id_col], int(row[seq_id_col]), row[ins_code_col], row[label_seq_col], row[comp_id_col]) for row in rowList),
                                       key=itemgetter(1))
                else:
                    if all(row[label_seq_col].isdigit() for row in rowList):
                        sortedSeq = sorted(set((row[chain_id_col], int(row[seq_id_col]), row[ins_code_col], int(row[label_seq_col]), row[comp_id_col]) for row in rowList),
                                           key=lambda x: (len(x[0]), x[0], x[3]))
                    else:
                        sortedSeq = sorted(set((row[chain_id_col], int(row[seq_id_col]), row[ins_code_col], row[label_seq_col], row[comp_id_col]) for row in rowList),
                                           key=lambda x: (len(x[0]), x[0], x[1]))

                keyDict = {(row[chain_id_col], int(row[seq_id_col]), row[ins_code_col], row[label_seq_col]): row[comp_id_col] for row in rowList}

                for row in rowList:
                    key = (row[chain_id_col], int(row[seq_id_col]), row[ins_code_col], row[label_seq_col])
                    if keyDict[key] != row[comp_id_col]:
                        raise KeyError(f"Sequence must be unique. {itNameList[chain_id_col]} {row[chain_id_col]}, "
                                       f"{itNameList[seq_id_col]} {row[seq_id_col]}, "
                                       f"{itNameList[ins_code_col]} {row[ins_code_col]}, "
                                       f"{itNameList[label_seq_col]} {row[label_seq_col]}, "
                                       f"{itNameList[comp_id_col]} {row[comp_id_col]} vs {keyDict[key]}.")

                for c in chainIds:
                    compDict[c] = [x[4] for x in sortedSeq if x[0] == c]
                    seqDict[c] = [x[1] for x in sortedSeq if x[0] == c]
                    insCodeDict[c] = [x[2] for x in sortedSeq if x[0] == c]
                    labelSeqDict[c] = [x[3] for x in sortedSeq if x[0] == c]

            chainIds = []
            for x in sortedSeq:
                if x[0] not in chainIds:
                    chainIds.append(x[0])

            if auth_chain_id_col != -1:
                for row in rowList:
                    c = row[chain_id_col]
                    if c not in authChainDict:
                        authChainDict[c] = row[auth_chain_id_col]

            large_model = catName == 'pdbx_poly_seq_scheme' and len(chainIds) > LEN_MAJOR_ASYM_ID

            entity_poly = self.getDictList('entity_poly')

            ca_rmsd = ca_well_defined_region = None
            polypeptide_chains = polypeptide_lengths = []

            for i, c in enumerate(chainIds):
                ent = {}  # entity

                ident = False
                if len(asm) > 0 and large_model:
                    _ent = asm[-1]
                    if 'identical_chain_id' in _ent and c in _ent['identical_chain_id']:
                        ident = True

                if ident:
                    ent = copy.copy(asm[-1])

                ent['chain_id'] = c
                if auth_chain_id_col != -1:
                    ent['auth_chain_id'] = authChainDict[c]

                if not ident:

                    ent['seq_id'] = seqDict[c]
                    ent['comp_id'] = compDict[c]
                    if c in insCodeDict:
                        if any(i for i in insCodeDict[c] if i not in self.emptyValue):
                            ent['ins_code'] = insCodeDict[c]
                        if any(s for s in labelSeqDict[c] if s not in self.emptyValue):
                            if c in labelSeqDict and all(isinstance(s, int) for s in labelSeqDict[c]):
                                ent['auth_seq_id'] = seqDict[c]
                                ent['label_seq_id'] = labelSeqDict[c]
                                ent['seq_id'] = ent['label_seq_id']

                    if auth_seq_id_col != -1:
                        ent['auth_seq_id'] = []
                        for s in seqDict[c]:
                            row = next((row for row in rowList if row[chain_id_col] == c and int(row[seq_id_col]) == s), None)
                            if row is not None:
                                if row[auth_seq_id_col] not in self.emptyValue:
                                    try:
                                        _s = int(row[auth_seq_id_col])
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

                    if auth_comp_id_col != -1:
                        ent['auth_comp_id'] = []
                        for s in seqDict[c]:
                            row = next((row for row in rowList if row[chain_id_col] == c and int(row[seq_id_col]) == s), None)
                            if row is not None:
                                comp_id = row[auth_comp_id_col]
                                if comp_id not in self.emptyValue:
                                    ent['auth_comp_id'].append(comp_id)
                                else:
                                    ent['auth_comp_id'].append('.')

                    if withStructConf and i < LEN_MAJOR_ASYM_ID:  # to process large assembly avoiding forced timeout
                        ent['struct_conf'] = self.__extractStructConf(c, seqDict[c])

                    etype = next((e['type'] for e in entity_poly if 'pdbx_strand_id' in e and c in e['pdbx_strand_id'].split(',')), None)

                    if withRmsd and etype is not None and total_models > 1 and i < LEN_MAJOR_ASYM_ID:  # to process large assembly avoiding forced timeout
                        ent['type'] = etype

                        randomM = None
                        if self.__random_rotaion_test:
                            randomM = {}
                            for model_id in range(1, total_models + 1):
                                axis = [random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)]
                                if self.__single_model_rotation_test:
                                    theta = 0.0 if model_id > 1 else np.pi / 4.0
                                else:
                                    theta = random.uniform(-np.pi, np.pi)
                                randomM[model_id] = M(axis, theta)

                        if 'polypeptide' in etype:

                            if ca_rmsd is None:

                                polypeptide_chains = [c]
                                polypeptide_lengths = [len(seqDict[c])]

                                for c2 in chainIds:

                                    if c2 == c:
                                        continue

                                    etype2 = next((e['type'] for e in entity_poly if 'pdbx_strand_id' in e and c2 in e['pdbx_strand_id'].split(',')), None)

                                    if etype2 is not None and 'polypeptide' in etype2:
                                        polypeptide_chains.append(c2)
                                        polypeptide_lengths.append(len(seqDict[c2]))

                                ca_atom_sites = self.getDictListWithFilter('atom_site',
                                                                           [{'name': 'Cartn_x', 'type': 'float', 'alt_name': 'x'},
                                                                            {'name': 'Cartn_y', 'type': 'float', 'alt_name': 'y'},
                                                                            {'name': 'Cartn_z', 'type': 'float', 'alt_name': 'z'},
                                                                            {'name': 'label_asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                                                                            {'name': 'label_seq_id', 'type': 'int', 'alt_name': 'seq_id'},
                                                                            {'name': 'ndb_model' if alias else 'pdbx_PDB_model_num', 'type': 'int', 'alt_name': 'model_id'},
                                                                            {'name': 'type_symbol', 'type': 'str', 'alt_name': 'element'}
                                                                            ],
                                                                           [{'name': 'label_asym_id', 'type': 'enum',
                                                                             'enum': polypeptide_chains},
                                                                            {'name': 'label_atom_id', 'type': 'str', 'value': 'CA'},
                                                                            {'name': 'label_alt_id', 'type': 'enum',
                                                                             'enum': ('A')},
                                                                            {'name': 'type_symbol', 'type': 'str', 'value': 'C'}])

                                co_atom_sites = self.getDictListWithFilter('atom_site',
                                                                           [{'name': 'Cartn_x', 'type': 'float', 'alt_name': 'x'},
                                                                            {'name': 'Cartn_y', 'type': 'float', 'alt_name': 'y'},
                                                                            {'name': 'Cartn_z', 'type': 'float', 'alt_name': 'z'},
                                                                            {'name': 'label_asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                                                                            {'name': 'label_seq_id', 'type': 'int', 'alt_name': 'seq_id'},
                                                                            {'name': 'ndb_model' if alias else 'pdbx_PDB_model_num', 'type': 'int', 'alt_name': 'model_id'},
                                                                            {'name': 'type_symbol', 'type': 'str', 'alt_name': 'element'}
                                                                            ],
                                                                           [{'name': 'label_asym_id', 'type': 'enum',
                                                                             'enum': polypeptide_chains},
                                                                            {'name': 'label_atom_id', 'type': 'str', 'value': 'C'},
                                                                            {'name': 'label_alt_id', 'type': 'enum',
                                                                             'enum': ('A')},
                                                                            {'name': 'type_symbol', 'type': 'str', 'value': 'C'}])

                                bb_atom_sites = self.getDictListWithFilter('atom_site',
                                                                           [{'name': 'Cartn_x', 'type': 'float', 'alt_name': 'x'},
                                                                            {'name': 'Cartn_y', 'type': 'float', 'alt_name': 'y'},
                                                                            {'name': 'Cartn_z', 'type': 'float', 'alt_name': 'z'},
                                                                            {'name': 'label_asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                                                                            {'name': 'label_seq_id', 'type': 'int', 'alt_name': 'seq_id'},
                                                                            {'name': 'ndb_model' if alias else 'pdbx_PDB_model_num', 'type': 'int', 'alt_name': 'model_id'},
                                                                            {'name': 'type_symbol', 'type': 'str', 'alt_name': 'element'}
                                                                            ],
                                                                           [{'name': 'label_asym_id', 'type': 'enum',
                                                                             'enum': polypeptide_chains},
                                                                            {'name': 'label_atom_id', 'type': 'str', 'value': 'N'},
                                                                            {'name': 'label_alt_id', 'type': 'enum',
                                                                             'enum': ('A')},
                                                                            {'name': 'type_symbol', 'type': 'str', 'value': 'N'}])

                                bb_atom_sites.extend(ca_atom_sites)
                                bb_atom_sites.extend(co_atom_sites)

                                ca_rmsd, ca_well_defined_region = self.__calculateRmsd(polypeptide_chains, polypeptide_lengths, total_models,
                                                                                       ca_atom_sites, bb_atom_sites, randomM)

                            if ca_rmsd is not None:
                                ent['ca_rmsd'] = ca_rmsd[polypeptide_chains.index(c)]
                            if ca_well_defined_region is not None:
                                ent['well_defined_region'] = ca_well_defined_region[polypeptide_chains.index(c)]

                        elif 'ribonucleotide' in etype:

                            p_atom_sites = self.getDictListWithFilter('atom_site',
                                                                      [{'name': 'Cartn_x', 'type': 'float', 'alt_name': 'x'},
                                                                       {'name': 'Cartn_y', 'type': 'float', 'alt_name': 'y'},
                                                                       {'name': 'Cartn_z', 'type': 'float', 'alt_name': 'z'},
                                                                       {'name': 'label_asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                                                                       {'name': 'label_seq_id', 'type': 'int', 'alt_name': 'seq_id'},
                                                                       {'name': 'ndb_model' if alias else 'pdbx_PDB_model_num', 'type': 'int', 'alt_name': 'model_id'},
                                                                       {'name': 'type_symbol', 'type': 'str', 'alt_name': 'element'}
                                                                       ],
                                                                      [{'name': 'label_asym_id', 'type': 'str', 'value': c},
                                                                       {'name': 'label_atom_id', 'type': 'str', 'value': 'P'},
                                                                       {'name': 'label_alt_id', 'type': 'enum',
                                                                        'enum': ('A')},
                                                                       {'name': 'type_symbol', 'type': 'str', 'value': 'P'}])

                            bb_atom_sites = self.getDictListWithFilter('atom_site',
                                                                       [{'name': 'Cartn_x', 'type': 'float', 'alt_name': 'x'},
                                                                        {'name': 'Cartn_y', 'type': 'float', 'alt_name': 'y'},
                                                                        {'name': 'Cartn_z', 'type': 'float', 'alt_name': 'z'},
                                                                        {'name': 'label_asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                                                                        {'name': 'label_seq_id', 'type': 'int', 'alt_name': 'seq_id'},
                                                                        {'name': 'ndb_model' if alias else 'pdbx_PDB_model_num', 'type': 'int', 'alt_name': 'model_id'},
                                                                        {'name': 'type_symbol', 'type': 'str', 'alt_name': 'element'}
                                                                        ],
                                                                       [{'name': 'label_asym_id', 'type': 'str', 'value': c},
                                                                        {'name': 'label_atom_id', 'type': 'enum',
                                                                         'enum': ("C5'", "C4'", "C3'")},
                                                                        {'name': 'label_alt_id', 'type': 'enum',
                                                                         'enum': ('A')},
                                                                        {'name': 'type_symbol', 'type': 'str', 'value': 'C'}])

                            bb_atom_sites.extend(p_atom_sites)

                            p_rmsd, p_well_defined_region = self.__calculateRmsd([c], [len(seqDict[c])], total_models,
                                                                                 p_atom_sites, bb_atom_sites, randomM)

                            if p_rmsd is not None:
                                ent['p_rmsd'] = p_rmsd[0]
                            if p_well_defined_region is not None:
                                ent['well_defined_region'] = p_well_defined_region[0]

                if len(chainIds) > 1:
                    identity = []
                    for _c in chainIds:
                        if _c == c:
                            continue
                        if compDict[_c] == compDict[c]:
                            identity.append(_c)
                    if len(identity) > 0:
                        ent['identical_chain_id'] = identity
                        if auth_chain_id_col != -1:
                            ent['identical_auth_chain_id'] = [authChainDict[c] for c in identity]

                asm.append(ent)

        return asm

    def __extractStructConf(self, chain_id, seq_ids):
        """ Extract structure conformational annotations.
        """

        ret = [None] * len(seq_ids)

        helix_id_name = 'pdbx_PDB_helix_id' if self.hasItem('struct_conf', 'pdbx_PDB_helix_id') else 'pdb_id'

        struct_conf = self.getDictListWithFilter('struct_conf',
                                                 [{'name': 'conf_type_id', 'type': 'str'},
                                                  {'name': helix_id_name, 'type': 'str', 'alt_name': 'helix_id'},
                                                  {'name': 'beg_label_seq_id', 'type': 'int'},
                                                  {'name': 'end_label_seq_id', 'type': 'int'}
                                                  ],
                                                 [{'name': 'beg_label_asym_id', 'type': 'str', 'value': chain_id},
                                                  {'name': 'end_label_asym_id', 'type': 'str', 'value': chain_id}
                                                  ])

        for sc in struct_conf:
            for seq_id in range(sc['beg_label_seq_id'], sc['end_label_seq_id'] + 1):
                if seq_id in seq_ids and sc['conf_type_id'] is not None and sc['helix_id'] is not None:
                    ret[seq_ids.index(seq_id)] = sc['conf_type_id'] + ':' + sc['helix_id']

        struct_sheet_range = self.getDictListWithFilter('struct_sheet_range',
                                                        [{'name': 'sheet_id', 'type': 'str'},
                                                         {'name': 'id', 'type': 'str'},
                                                         {'name': 'beg_label_seq_id', 'type': 'int'},
                                                         {'name': 'end_label_seq_id', 'type': 'int'}
                                                         ],
                                                        [{'name': 'beg_label_asym_id', 'type': 'str', 'value': chain_id},
                                                         {'name': 'end_label_asym_id', 'type': 'str', 'value': chain_id}
                                                         ])

        for ssr in struct_sheet_range:
            for seq_id in range(ssr['beg_label_seq_id'], ssr['end_label_seq_id'] + 1):
                if seq_id in seq_ids and ssr['sheet_id'] is not None and ssr['id'] is not None:
                    ret[seq_ids.index(seq_id)] = 'STRN:' + ssr['sheet_id'] + ':' + ssr['id']

        return ret

    def __calculateRmsd(self, chain_ids, lengths, total_models=1, atom_sites=None, bb_atom_sites=None, randomM=None):
        """ Calculate RMSD of alpha carbons/phosphates in the ensemble.
        """

        if atom_sites is None or bb_atom_sites is None:
            return None, None

        _atom_site_dict = {}
        for model_id in range(1, total_models + 1):
            _atom_site_dict[model_id] = [a for a in atom_sites if a['model_id'] == model_id]

        _bb_atom_site_dict = {}
        for model_id in range(1, total_models + 1):
            _bb_atom_site_dict[model_id] = [a for a in bb_atom_sites if a['model_id'] == model_id]

        size = len(_atom_site_dict[1])

        if size == 0:
            return None, None

        matrix_size = (size, size)

        d_avr = np.zeros(matrix_size, dtype=float)

        _total_models = 0

        for model_id in range(1, total_models + 1):

            _atom_site = _atom_site_dict[model_id]

            if len(_atom_site) == 0:
                continue

            _total_models += 1

            for a_i, a_j in itertools.combinations(_atom_site, 2):

                i = _atom_site.index(a_i)
                j = _atom_site.index(a_j)

                d = np.linalg.norm(to_np_array(a_i) - to_np_array(a_j))

                if i < j:
                    d_avr[i, j] += d
                else:
                    d_avr[j, i] += d

        if _total_models <= 1:
            return None, None

        factor = 1.0 / _total_models

        d_avr = np.multiply(d_avr, factor)

        d_var = np.zeros(matrix_size, dtype=float)

        for model_id in range(1, total_models + 1):

            _atom_site = _atom_site_dict[model_id]

            if len(_atom_site) == 0:
                continue

            for a_i, a_j in itertools.combinations(_atom_site, 2):

                i = _atom_site.index(a_i)
                j = _atom_site.index(a_j)

                d = np.linalg.norm(to_np_array(a_i) - to_np_array(a_j))

                if i < j:
                    d -= d_avr[i, j]
                    d_var[i, j] += d * d
                else:
                    d -= d_avr[j, i]
                    d_var[j, i] += d * d

        d_var = np.multiply(d_var, factor)

        max_d_var = np.max(d_var)

        if max_d_var > self.__d_cutoff:
            max_d_var = self.__d_cutoff

        d_ord = np.ones(matrix_size, dtype=float)

        if max_d_var > 0.0:

            for i, j in itertools.combinations(range(size), 2):

                if i < j:
                    q = max(1.0 - math.sqrt(d_var[i, j] / max_d_var), 0.0)
                else:
                    q = max(1.0 - math.sqrt(d_var[j, i] / max_d_var), 0.0)

                d_ord[i, j] = q
                d_ord[j, i] = q

        _, v = np.linalg.eig(d_ord)

        md5_set = set()

        abort = False

        min_score = 1000000.0
        min_result = None

        stop_min_samples = -1

        for min_samples in reversed(range(self.__min_samples_for_clustering, self.__max_samples_for_clustering + 1)):

            if min_samples == stop_min_samples:
                break

            for features in range(self.__min_features_for_clustering, self.__max_features_for_clustering + 1):

                x = np.delete(v, np.s_[features:], 1)

                if min_samples >= features:
                    continue

                for _epsilon in range(4, 11):

                    if abort:
                        break

                    epsilon = 2.0 ** (_epsilon / 2.0) / 100.0  # epsilon travels from 0.04 to 0.32

                    try:
                        db = DBSCAN(eps=epsilon, min_samples=min_samples).fit(x)
                    except ValueError:
                        db = DBSCAN(eps=epsilon, min_samples=min_samples).fit(np.real(x))

                    labels = db.labels_

                    list_labels = list(labels)
                    set_labels = set(labels)

                    n_clusters = len(set_labels) - (1 if -1 in set_labels else 0)
                    n_noise = list_labels.count(-1)

                    if n_clusters == 0 or n_clusters >= features - 2:
                        continue

                    md5 = hashlib.md5(str(list_labels).encode('utf-8'))

                    if md5 in md5_set:
                        continue

                    md5_set.add(md5)

                    result = {'features': features, 'min_samples': min_samples, 'epsilon': epsilon, 'clusters': n_clusters, 'noise': n_noise}

                    score = 0.0

                    for label in set_labels:

                        monomers = list_labels.count(label)

                        if monomers < self.__min_monomers_for_domain:
                            continue

                        fraction = float(monomers) / size

                        _rmsd = []

                        _atom_site_ref = _atom_site_dict[1]
                        _atom_site_p = [_a for _a, _l in zip(_atom_site_ref, list_labels) if _l == label]

                        # """
                        # if label != -1:
                        #     for chain_id in chain_ids:
                        #         seq_ids = sorted(set(a['seq_id'] for a in _atom_site_p if a['chain_id'] == chain_id))
                        #         if len(seq_ids) > 0:
                        #             gaps = seq_ids[-1] + 1 - seq_ids[0] - len(seq_ids)

                        #             if gaps > monomers:
                        #                 score = 0.0
                        #                 break
                        # """

                        for model_id in range(2, total_models + 1):

                            _atom_site_test = _atom_site_dict[model_id]

                            if len(_atom_site_test) == 0:
                                continue

                            _atom_site_q = [_a for _a, _l in zip(_atom_site_test, list_labels) if _l == label]

                            _rmsd.append(calculate_rmsd(_atom_site_p, _atom_site_q))

                        mean_rmsd = np.mean(np.array(_rmsd))

                        score += mean_rmsd * fraction

                    if score == 0.0:
                        continue

                    result['score'] = score

                    if n_clusters > 0 and stop_min_samples == -1:
                        stop_min_samples = min_samples - 2

                    if self.__verbose:
                        self.__lfh.write(f'{result}\n')

                    if score < min_score or (n_noise == 0 and min_score < self.__rmsd_overlaid_exactly):
                        min_score = score
                        min_result = result

                        if n_noise == 0 and min_score < self.__rmsd_overlaid_exactly:
                            abort = True

        if min_result is None:
            return None, None

        x = np.delete(v, np.s_[min_result['features']:], 1)

        try:
            db = DBSCAN(eps=min_result['epsilon'], min_samples=min_result['min_samples']).fit(x)
        except ValueError:
            db = DBSCAN(eps=min_result['epsilon'], min_samples=min_result['min_samples']).fit(np.real(x))

        labels = db.labels_

        list_labels = list(labels)
        domains = collections.Counter(list_labels).most_common()

        if domains[0][0] == -1:
            return None, None

        eff_labels = [label for label, count in domains if label != -1 and count >= self.__min_monomers_for_domain]
        eff_domain_id = {}

        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        if self.__verbose:
            self.__lfh.write(f"feature: {min_result['features']}, "
                             f"min_sample: {min_result['min_samples']}, epsilon: {min_result['epsilon']}, "
                             f"clusters: {n_clusters} (effective domains: {len(eff_labels)}), score: {min_score}\n")

        _chain_ids = [a['chain_id'] for a in _atom_site_dict[1]]
        _seq_ids = [a['seq_id'] for a in _atom_site_dict[1]]

        domain_id = 1
        for label, chain_id, seq_id in zip(labels, _chain_ids, _seq_ids):
            if label not in eff_labels:
                if self.__verbose:
                    self.__lfh.write(f"chain_id: {chain_id}, seq_id: {seq_id}, domain_id: -1\n")
            else:
                _label = int(label)
                if _label not in eff_domain_id:
                    eff_domain_id[_label] = domain_id
                    domain_id += 1
                if self.__verbose:
                    self.__lfh.write(f"chain_id: {chain_id}, seq_id: {seq_id}, domain_id: {eff_domain_id[_label]} label: {_label}\n")

        rlist = []
        for chain_id in chain_ids:
            rlist.append([])

        for ref_model_id in range(1, _total_models + 1):

            item = {'model_id': ref_model_id}
            _atom_site_ref = _atom_site_dict[ref_model_id]
            _bb_atom_site_ref = _bb_atom_site_dict[ref_model_id]

            dst_chain_ids = None
            min_label = -1
            min_core_rmsd = mean_align_rmsd = 1000000.0

            for label, count in domains:

                if label not in eff_labels:
                    break

                _label = int(label)

                _atom_site_p = [_a for _a, _l in zip(_atom_site_ref, list_labels) if _l == label]

                _dst_chain_ids = set(_a['chain_id'] for _a in _atom_site_p)
                _seq_keys = sorted(set((_a['chain_id'], _a['seq_id']) for _a in _atom_site_p),
                                   key=itemgetter(0, 1))
                _bb_atom_site_p = [_a for _a in _bb_atom_site_ref if (_a['chain_id'], _a['seq_id']) in _seq_keys]

                core_rmsd = []
                align_rmsd = []
                exact_overlaid_model_ids = []

                for test_model_id in range(1, _total_models + 1):

                    if ref_model_id == test_model_id:
                        continue

                    _atom_site_test = _atom_site_dict[test_model_id]
                    _atom_site_q = [_a for _a, _l in zip(_atom_site_test, list_labels) if _l == label]

                    _bb_atom_site_test = _bb_atom_site_dict[test_model_id]
                    _bb_atom_site_q = [_a for _a in _bb_atom_site_test if (_a['chain_id'], _a['seq_id']) in _seq_keys]

                    _core_rmsd = []

                    for idx in range(count):

                        ref_atom = _atom_site_p[idx]
                        test_atom = _atom_site_q[idx]

                        ref_v = to_np_array(ref_atom)
                        if self.__random_rotaion_test:
                            ref_v = np.dot(randomM[ref_model_id], ref_v)

                        test_v = to_np_array(test_atom)
                        if self.__random_rotaion_test:
                            test_v = np.dot(randomM[test_model_id], test_v)
                        d = test_v - ref_v
                        _core_rmsd.append(np.dot(d, d))

                    core_rmsd.append(math.sqrt(np.mean(np.array(_core_rmsd))))
                    _rmsd = calculate_rmsd(_bb_atom_site_p, _bb_atom_site_q)
                    align_rmsd.append(_rmsd)
                    if _rmsd < self.__rmsd_overlaid_exactly and ref_model_id < test_model_id:
                        exact_overlaid_model_ids.append({'ref_model_id': ref_model_id,
                                                         'test_model_id': test_model_id,
                                                         'rmsd_in_well_defined_region': float(f"{_rmsd:.4f}")})

                mean_core_rmsd = np.mean(np.array(core_rmsd))

                if mean_core_rmsd < min_core_rmsd:
                    dst_chain_ids = _dst_chain_ids
                    min_label = _label
                    min_core_rmsd = mean_core_rmsd
                    mean_align_rmsd = np.mean(np.array(align_rmsd))

            if min_label != -1:
                item['domain_id'] = eff_domain_id[min_label]
                item['raw_rmsd_in_well_defined_region'] = float(f"{min_core_rmsd:.4f}")
                item['rmsd_in_well_defined_region'] = float(f"{mean_align_rmsd:.4f}")
                if len(exact_overlaid_model_ids) > 0:
                    item['exactly_overlaid_model'] = exact_overlaid_model_ids
                for chain_id in dst_chain_ids:
                    rlist[chain_ids.index(chain_id)].append(item)

        dlist = []
        for chain_id in chain_ids:
            dlist.append([])

        seq_range_p = re.compile(r'^\[(-?\d+)-(-?\d+)\]$')

        for label in sorted(eff_labels):

            item = {}

            r = np.zeros((_total_models, _total_models), dtype=float)

            _rmsd = []

            for ref_model_id in range(1, _total_models):

                _atom_site_ref = _atom_site_dict[ref_model_id]
                _atom_site_p = [_a for _a, _l in zip(_atom_site_ref, list_labels) if _l == label]

                _bb_atom_site_ref = _bb_atom_site_dict[ref_model_id]
                _seq_keys = sorted(set((_a['chain_id'], _a['seq_id']) for _a in _atom_site_p),
                                   key=itemgetter(0, 1))
                _bb_atom_site_p = [_a for _a in _bb_atom_site_ref if (_a['chain_id'], _a['seq_id']) in _seq_keys]

                for test_model_id in range(2, _total_models + 1):

                    if ref_model_id >= test_model_id:
                        continue

                    # _atom_site_test = _atom_site_dict[test_model_id]
                    # _atom_site_q = [_a for _a, _l in zip(_atom_site_test, list_labels) if _l == label]

                    _bb_atom_site_test = _bb_atom_site_dict[test_model_id]
                    _bb_atom_site_q = [_a for _a in _bb_atom_site_test if (_a['chain_id'], _a['seq_id']) in _seq_keys]

                    _rmsd_ = calculate_rmsd(_bb_atom_site_p, _bb_atom_site_q)

                    r[ref_model_id - 1, test_model_id - 1] = _rmsd_
                    r[test_model_id - 1, ref_model_id - 1] = _rmsd_

                    _rmsd.append(_rmsd_)

            item['mean_rmsd'] = float(f"{np.mean(np.array(_rmsd)):.4f}")

            _, v = np.linalg.eig(r)
            x = np.delete(np.abs(v), np.s_[1:], 1)
            ref_model_id = int(np.argmin(x, axis=0)[0]) + 1

            item['medoid_model_id'] = ref_model_id

            _atom_site_ref = _atom_site_dict[ref_model_id]
            _atom_site_p = [_a for _a, _l in zip(_atom_site_ref, list_labels) if _l == label]
            _bb_atom_site_ref = _bb_atom_site_dict[ref_model_id]
            _seq_keys = sorted(set((_a['chain_id'], _a['seq_id']) for _a in _atom_site_p))
            _bb_atom_site_p = [_a for _a in _bb_atom_site_ref if (_a['chain_id'], _a['seq_id']) in _seq_keys]

            _rmsd = []

            for test_model_id in range(1, _total_models + 1):

                if ref_model_id == test_model_id:
                    continue

                # _atom_site_test = _atom_site_dict[test_model_id]
                # _atom_site_q = [_a for _a, _l in zip(_atom_site_test, list_labels) if _l == label]

                _bb_atom_site_test = _bb_atom_site_dict[test_model_id]
                _bb_atom_site_q = [_a for _a in _bb_atom_site_test if (_a['chain_id'], _a['seq_id']) in _seq_keys]

                _rmsd.append(calculate_rmsd(_bb_atom_site_p, _bb_atom_site_q))

            item['medoid_rmsd'] = float(f"{np.mean(np.array(_rmsd)):.4f}")

            _item = copy.copy(item)

            _label = int(label)

            dst_chain_ids = set(a['chain_id'] for a, l in zip(_atom_site_ref, list_labels) if l == label)  # noqa: E741
            seq_keys = sorted(set((a['chain_id'], a['seq_id']) for a, l in zip(_atom_site_ref, list_labels) if l == label),  # noqa: E741
                              key=itemgetter(0, 1))

            for chain_id in dst_chain_ids:
                seq_ids = [s for c, s in seq_keys if c == chain_id]
                count = len(seq_ids)

                _item['domain_id'] = eff_domain_id[_label]
                _item['number_of_monomers'] = count
                _item['seq_id'] = seq_ids
                gaps = seq_ids[-1] + 1 - seq_ids[0] - len(seq_ids)
                _item['number_of_gaps'] = gaps
                if gaps == 0:
                    seq_range = f"[{seq_ids[0]}-{seq_ids[-1]}]"
                else:
                    seq_range = f"[{seq_ids[0]}-"
                    for idx, seq_id in enumerate(seq_ids):
                        if idx > 0 and seq_id != seq_ids[idx - 1] + 1:
                            seq_range += f"{seq_ids[idx - 1]}],[{seq_id}-"
                    seq_range += f"{seq_ids[-1]}]"
                _seq_range = []
                for r in seq_range.split(','):
                    try:
                        g = seq_range_p.search(r).groups()
                        if g[0] != g[1]:
                            _seq_range.append(f"[{g[0]}-{g[1]}]")
                        else:
                            _seq_range.append(f"[{g[0]}]")
                    except AttributeError:
                        pass
                _item['range_of_seq_id'] = ','.join(_seq_range)
                _item['percent_of_core'] = float(f"{float(count) / lengths[chain_ids.index(chain_id)] * 100.0:.1f}")

                dlist[chain_ids.index(chain_id)].append(_item)

        if self.__verbose:
            self.__lfh.write(f"{dlist}\n")

        return rlist, dlist
