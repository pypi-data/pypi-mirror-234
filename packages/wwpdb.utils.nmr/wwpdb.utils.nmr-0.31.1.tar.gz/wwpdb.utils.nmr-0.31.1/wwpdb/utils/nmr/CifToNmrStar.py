##
# File: CifToNmrStar.py
# Date: 19-Jul-2021
#
# Updates:
# 13-Oct-2021  M. Yokochi - code revision according to PEP8 using Pylint (DAOTHER-7389, issue #5)
# 20-Apr-2022  M. Yokochi - enable to fix broken data block order of CIF formatted NMR-STAR using NMR-STAR schema (DAOTHER-7407, NMR restraint remediation)
# 28-Jul-2022  M. Yokochi - enable to fix format issue of CIF formatted NMR-STAR (You cannot have two loops with the same category in one saveframe. Category: '_Audit')
# 27-Sep-2022  M. Yokochi - auto fill list ID and entry ID (NMR restraint remediation)
# 13-Jun-2023  M. Yokochi - sort loops in a saveframe based on schema
##
""" Wrapper class for CIF to NMR-STAR converter.
    @author: Masashi Yokochi
"""
import sys
import os
import re
import pynmrstar
import pickle
import logging
import hashlib

from packaging import version
from operator import itemgetter

try:
    from wwpdb.utils.nmr.io.mmCIFUtil import mmCIFUtil
    from wwpdb.utils.nmr.AlignUtil import (emptyValue, trueValue)
except ImportError:
    from nmr.io.mmCIFUtil import mmCIFUtil
    from nmr.AlignUtil import (emptyValue, trueValue)


__pynmrstar_v3_3_1__ = version.parse(pynmrstar.__version__) >= version.parse("3.3.1")
__pynmrstar_v3_2__ = version.parse(pynmrstar.__version__) >= version.parse("3.2.0")
__pynmrstar_v3_1__ = version.parse(pynmrstar.__version__) >= version.parse("3.1.0")
__pynmrstar_v3__ = version.parse(pynmrstar.__version__) >= version.parse("3.0.0")

if __pynmrstar_v3_3_1__:
    logger = logging.getLogger('pynmrstar')
    logger.setLevel(logging.ERROR)
else:
    logging.getLogger().setLevel(logging.ERROR)  # set level for pynmrstar


class CifToNmrStar:
    """ Simple CIF to NMR-STAR converter.
    """

    def __init__(self, log=sys.stderr):
        self.__lfh = log

        # directory
        self.schema_dir = os.path.dirname(__file__) + '/nmr-star_schema/'

        def load_schema_from_pickle(file_name):
            """ Load NMR-STAR schema from pickle file.
            """

            if os.path.exists(file_name):

                with open(file_name, 'rb') as ifh:
                    return pickle.load(ifh)

            return None

        # NMR-STAR schema
        self.schema = load_schema_from_pickle(self.schema_dir + 'schema.pkl')

        # NMR-STAR schema order
        # self.schema_order = load_schema_from_pickle(self.schema_dir + 'schema_order.pkl')

        # NMR-STAR category order
        self.category_order = load_schema_from_pickle(self.schema_dir + 'category_order.pkl')

        if self.schema is None:
            schema = pynmrstar.Schema()  # network latency occurs if pickle resource files are not available
            self.schema = schema.schema
            self.category_order = schema.category_order

        # NEF category order
        self.category_order_nef = ['_nef_nmr_meta_data',
                                   '_nef_molecular_system',
                                   '_nef_chemical_shift_list',
                                   '_nef_distance_restraint_list',
                                   '_nef_dihedral_restraint_list',
                                   '_nef_rdc_restraint_list',
                                   '_nef_nmr_spectrum',
                                   '_nef_peak_restraint_links']

    def write_schema_as_pickles(self):
        """ Retrieve NMR-STAR schema from pynmrstar.Schema, then write schema objects as each pickle file.
        """

        def write_schema_as_pickle(obj, file_name):
            """ Write NMR-STAR schema as pickle file.
            """

            with open(file_name, 'wb') as ofh:
                pickle.dump(obj, ofh)

        schema = pynmrstar.Schema()  # retrieve the latest schema via interet access

        # print(schema.headers)
        with open(self.schema_dir + 'headers.txt', 'w') as ofh:
            for header in schema.headers:
                ofh.write(header + '\n')
        self.__lfh.write('headers.txt: Done.\n')

        # print(schema.schema)
        write_schema_as_pickle(schema.schema, self.schema_dir + 'schema.pkl')
        self.__lfh.write('schema.pkl: Done.\n')

        # print(schema.schema_order)
        write_schema_as_pickle(schema.schema_order, self.schema_dir + 'schema_order.pkl')
        self.__lfh.write('schema_order.pkl: Done.\n')

        # print(schema.category_order)
        write_schema_as_pickle(schema.category_order, self.schema_dir + 'category_order.pkl')
        self.__lfh.write('category_order.pkl: Done.\n')

        # print(schema.data_types)
        write_schema_as_pickle(schema.data_types, self.schema_dir + 'data_types.pkl')
        self.__lfh.write('data_types.pkl: Done.\n')

        with open(self.schema_dir + 'version.txt', 'w') as ofh:
            ofh.write(schema.version)
        self.__lfh.write(f"version: {schema.version}\n")

    def convert(self, cifPath=None, strPath=None, datablockName=None, maxRepeat=1):
        """ Convert CIF formatted NMR data file to normalized NMR-STAR file.
        """

        if cifPath is None or strPath is None:
            return False

        try:

            cifObj = mmCIFUtil(filePath=cifPath)

            block_name_list = cifObj.GetBlockIDList()

            if len(block_name_list) == 0:  # single loop
                return False

            entry_id = None

            strData = pynmrstar.Entry.from_scratch(datablockName if datablockName is not None else os.path.basename(cifPath))

            # check category order in CIF
            category_order = []
            previous_order = -1

            sf_category_counter = {}

            for block_name in block_name_list:

                dict_list = cifObj.GetDataBlock(block_name)

                ordered_block = True
                sf_category = ''

                for category, itVals in dict_list.items():
                    try:
                        current_order = self.category_order.index('_' + category)
                    except ValueError:
                        continue
                    # print(f"{block_name} {category} {current_order}")
                    item = {'block_name': block_name, 'category': category,
                            'category_order': current_order}
                    if current_order < previous_order:
                        ordered_block = False
                        for item2 in category_order:
                            if item2['block_name'] == block_name:
                                item2['ordered'] = False
                    item['ordered'] = ordered_block

                    item['sf_category_flag'] = False
                    for _item, _value in zip(itVals['Items'], itVals['Values'][0]):
                        tag = '_' + category + '.' + _item
                        tag = tag.lower()
                        if tag in self.schema:
                            sdict = {k: v for k, v in self.schema[tag].items() if v not in emptyValue}
                            if 'sf_category' not in item:
                                item['sf_category'] = sdict['SFCategory']
                            if 'super_category' not in item:
                                item['super_category'] = sdict['ADIT super category']
                            if 'Sf category flag' in sdict and sdict['Sf category flag'].lower() in trueValue:
                                item['sf_category_flag'] = True
                            if _item == 'Entry_ID' and entry_id in emptyValue:
                                entry_id = _value

                    if 'Sf_category' not in itVals['Items']:
                        _tag = '_' + category.lower() + '.sf_category'
                        if _tag in self.schema:
                            sdict = {k: v for k, v in self.schema[_tag].items() if v not in emptyValue}
                            if 'sf_category' not in item:
                                item['sf_category'] = sdict['SFCategory']
                            if 'super_category' not in item:
                                item['super_category'] = sdict['ADIT super category']
                            if 'Sf category flag' in sdict and sdict['Sf category flag'].lower() in trueValue:
                                item['sf_category_flag'] = True

                    if len(sf_category) == 0:
                        sf_category = item['sf_category']
                    elif sf_category != item['sf_category']:
                        for item2 in category_order:
                            if item2['block_name'] == block_name:
                                item2['ordered'] = False
                        item['ordered'] = False

                    if item not in category_order:
                        category_order.append(item)

                    if item['sf_category_flag']:
                        previous_order = current_order

            if entry_id in emptyValue:
                entry_id = block_name_list[0]

            _entry_id = entry_id.upper()

            if datablockName is None:
                strData.entry_id = f'cs_{entry_id.lower()}'

            # reorder
            category_order.sort(key=itemgetter('category_order'))

            # correct block name in case
            reserved_block_names = []
            prev_sf_category = ''
            prev_sf_block_name = ''
            for item in category_order:
                if item['ordered']:
                    continue
                block_name = item['block_name']
                if item['sf_category_flag']:
                    if item['sf_category'] == item['super_category']:
                        block_name = item['sf_category']
                    else:
                        list_id = 1
                        while True:
                            block_name = item['sf_category'] + '_' + str(list_id)
                            if block_name not in reserved_block_names:
                                break
                            list_id += 1
                    prev_sf_category = item['sf_category']
                    prev_sf_block_name = block_name
                else:
                    if item['sf_category'] == prev_sf_category:
                        block_name = prev_sf_block_name
                    else:
                        item['missing_sf_category'] = True
                        if item['sf_category'] == item['super_category']:
                            block_name = item['sf_category']
                        else:
                            list_id = 1
                            while True:
                                block_name = item['sf_category'] + '_' + str(list_id)
                                if block_name not in reserved_block_names:
                                    break
                                list_id += 1
                        prev_sf_category = item['sf_category']
                        prev_sf_block_name = block_name
                item['new_block_name'] = block_name

            ordered_block_names = []
            for item in category_order:
                block_name = item['new_block_name'] if 'new_block_name' in item else item['block_name']
                if block_name not in ordered_block_names:
                    ordered_block_names.append(block_name)

            _category_order = []
            for _block_name in ordered_block_names:
                count = 0
                for item in category_order:
                    block_name = item['new_block_name'] if 'new_block_name' in item else item['block_name']
                    if block_name == _block_name:
                        _category_order.append(item)
                        count += 1
                if count == 1:
                    last_item = _category_order[-1]
                    if not last_item['sf_category_flag'] and last_item['ordered']:
                        last_item['missing_sf_category'] = True
                        last_item['new_block_name'] = last_item['block_name']

            category_order = _category_order

            _sf_category = ''

            reserved_block_names = []
            sf = None
            for item in category_order:
                block_name = item['block_name']
                category = item['category']

                sf_category = item['sf_category']

                if item['sf_category_flag'] or ('missing_sf_category' in item and item['missing_sf_category']):
                    if sf_category not in sf_category_counter:
                        cur_list_id = 1
                    else:
                        cur_list_id = sf_category_counter[sf_category] + 1
                elif sf_category != _sf_category:
                    cur_list_id = 1

                _sf_category = sf_category

                sf_tag_prefix = next(v['Tag category'] for k, v in self.schema.items()
                                     if v['SFCategory'] == sf_category and v['Tag field'] == 'Sf_category')

                sf_category_counter[sf_category] = cur_list_id
                _cur_list_id = str(cur_list_id)

                if 'missing_sf_category' in item and item['missing_sf_category']:
                    new_block_name = item['new_block_name']

                    if new_block_name in reserved_block_names:
                        continue

                    if sf is not None:
                        strData.add_saveframe(sf)

                    sf = pynmrstar.Saveframe.from_scratch(new_block_name)
                    reserved_block_names.append(new_block_name)
                    sf.set_tag_prefix(sf_tag_prefix)
                    sf.add_tag('Sf_category', sf_category)
                    sf.add_tag('Sf_framecode', new_block_name)
                    sf.add_tag('Entry_ID', _entry_id)

                    if sf_category != item['super_category']:
                        sf.add_tag('ID', _cur_list_id)

                elif item['sf_category_flag']:
                    new_block_name = item['new_block_name'] if 'new_block_name' in item else block_name

                    if new_block_name in reserved_block_names:
                        continue

                    if sf is not None:
                        strData.add_saveframe(sf)

                    sf = pynmrstar.Saveframe.from_scratch(new_block_name)
                    reserved_block_names.append(new_block_name)
                    sf.set_tag_prefix(category)

                    dict_list = cifObj.GetDataBlock(block_name)
                    itVals = next(v for k, v in dict_list.items() if k == category)

                    sf.add_tag('Sf_category', sf_category)
                    sf.add_tag('Sf_framecode', new_block_name)
                    if sf_category != 'entry_information':
                        sf.add_tag('Entry_ID', _entry_id)
                        sf.add_tag('ID', _cur_list_id)
                    else:
                        sf.add_tag('ID', _entry_id)

                    for _item, value in zip(itVals['Items'], itVals['Values'][0]):
                        if _item not in ('Sf_category', 'Sf_framecode', 'Entry_ID', 'ID'):
                            sf.add_tag(_item, value)

                if not item['sf_category_flag']:
                    lp = pynmrstar.Loop.from_scratch(category)

                    dict_list = cifObj.GetDataBlock(block_name)
                    itVals = next(v for k, v in dict_list.items() if k == category)

                    list_id_idx = -1
                    entry_id_idx = -1

                    for idx, _item in enumerate(itVals['Items']):
                        lp.add_tag(_item)
                        if sf_category != item['super_category']:
                            tag = '_' + category + '.' + _item
                            tag = tag.lower()
                            if tag in self.schema:
                                sdict = {k: v for k, v in self.schema[tag].items() if v not in emptyValue}
                                if 'Parent tag' in sdict and sdict['Parent tag'] == '_' + sf_tag_prefix + '.ID':
                                    list_id_idx = idx
                        if _item == 'Entry_ID':
                            entry_id_idx = idx

                    for idx, _value in enumerate(itVals['Values']):
                        if list_id_idx != -1:
                            _value[list_id_idx] = _cur_list_id
                        if entry_id_idx != -1:
                            _value[entry_id_idx] = _entry_id
                        lp.add_data(_value)

                    sf.add_loop(lp)

            if sf is not None:
                strData.add_saveframe(sf)

            self.normalize(strData)

            if __pynmrstar_v3__:
                strData.write_to_file(strPath, show_comments=False, skip_empty_loops=True, skip_empty_tags=False)
            else:
                strData.write_to_file(strPath)

            return True

        except ValueError as e:

            sf_anonymous_pattern = re.compile(r'\s*save_\S+\s*')
            save_pattern = re.compile(r'\s*save_\s*')

            split_ext = os.path.splitext(cifPath)
            _cifPath = split_ext[0] + '-corrected' + ('' if len(split_ext) == 1 else split_ext[1])

            changed = False

            with open(cifPath, 'r') as ifh, \
                    open(_cifPath, 'w') as ofh:
                for line in ifh:
                    if sf_anonymous_pattern.match(line) or save_pattern.match(line):
                        ofh.write('#' + line)
                        changed = True
                    else:
                        ofh.write(line)

            if changed and maxRepeat > 0:
                return self.convert(_cifPath, strPath, datablockName, maxRepeat=maxRepeat - 1)

            try:
                os.remove(_cifPath)
            except OSError:
                pass

            self.__lfh.write(f"+ERROR- CifToNmrStar.convert() {str(e)}\n")

            return False

        except Exception as e:
            self.__lfh.write(f"+ERROR- CifToNmrStar.convert() {str(e)}\n")

            return False

    def set_entry_id(self, strData, entryId):
        """ Set entry ID without changing datablock name.
            @see: pynmrstar.entry
        """

        if strData is None:
            return

        if isinstance(strData, pynmrstar.Entry):

            for sf in strData.frame_list:
                filled = False

                for tag in sf.tags:
                    fqtn = (sf.tag_prefix + '.' + tag[0]).lower()

                    try:
                        if self.schema[fqtn]['entryIdFlg'] == 'Y':
                            tag[1] = entryId
                            filled = True
                            break
                    except KeyError:
                        pass

                if not filled:
                    entry_id_tag = 'ID' if sf.category == 'entry_information' else 'Entry_ID'

                    fqtn = (sf.tag_prefix + '.' + entry_id_tag).lower()

                    try:
                        if self.schema[fqtn]['entryIdFlg'] == 'Y':
                            sf.add_tag(entry_id_tag, entryId)
                    except KeyError:
                        pass

                for lp in sf.loops:
                    filled = False

                    for tag in lp.tags:
                        fqtn = (lp.category + '.' + tag).lower()

                        try:
                            if self.schema[fqtn]['entryIdFlg'] == 'Y' or tag == 'Entry_ID':
                                lp[tag] = [entryId] * len(lp[tag])
                                filled = True
                                break
                        except KeyError:
                            pass

                    if not filled:
                        entry_id_tag = lp.category + '.Entry_ID'

                        lp.add_tag(entry_id_tag)

                        for row in lp:
                            row.append(entryId)

        elif isinstance(strData, pynmrstar.Saveframe):

            sf = strData

            filled = False

            for tag in sf.tags:
                fqtn = (sf.tag_prefix + '.' + tag[0]).lower()

                try:
                    if self.schema[fqtn]['entryIdFlg'] == 'Y':
                        tag[1] = entryId
                        filled = True
                        break
                except KeyError:
                    pass

            if not filled:
                entry_id_tag = 'ID' if sf.category == 'entry_information' else 'Entry_ID'

                fqtn = (sf.tag_prefix + '.' + entry_id_tag).lower()

                try:
                    if self.schema[fqtn]['entryIdFlg'] == 'Y':
                        sf.add_tag(entry_id_tag, entryId)
                except KeyError:
                    pass

            for lp in sf.loops:
                filled = False

                for tag in lp.tags:
                    fqtn = (lp.category + '.' + tag).lower()

                    try:
                        if self.schema[fqtn]['entryIdFlg'] == 'Y' or tag == 'Entry_ID':
                            lp[tag] = [entryId] * len(lp[tag])
                            filled = True
                            break
                    except KeyError:
                        pass

                if not filled:
                    entry_id_tag = lp.category + '.Entry_ID'

                    lp.add_tag(entry_id_tag)

                    for row in lp:
                        row.append(entryId)

        elif isinstance(strData, pynmrstar.Loop):

            lp = strData

            filled = False

            for tag in lp.tags:
                fqtn = (lp.category + '.' + tag).lower()

                try:
                    if self.schema[fqtn]['entryIdFlg'] == 'Y' or tag == 'Entry_ID':
                        lp[tag] = [entryId] * len(lp[tag])
                        filled = True
                        break
                except KeyError:
                    pass

            if not filled:
                entry_id_tag = lp.category + '.Entry_ID'

                lp.add_tag(entry_id_tag)

                for row in lp:
                    row.append(entryId)

    def set_local_sf_id(self, strData, listId):
        """ Set list ID for a given saveframe or loop.
        """

        if strData is None:
            return

        if isinstance(strData, pynmrstar.Saveframe):

            sf = strData

            for tag in sf.tags:
                fqtn = (sf.tag_prefix + '.' + tag[0]).lower()

                try:
                    if self.schema[fqtn]['lclSfIdFlg'] == 'Y':
                        tag[1] = listId
                        break
                except KeyError:
                    pass

            for lp in sf.loops:

                for tag in lp.tags:
                    fqtn = (lp.category + '.' + tag).lower()

                    try:
                        if self.schema[fqtn]['lclSfIdFlg'] == 'Y':
                            lp[tag] = [listId] * len(lp[tag])
                            break
                    except KeyError:
                        pass

        elif isinstance(strData, pynmrstar.Loop):

            lp = strData

            for tag in lp.tags:
                fqtn = (lp.category + '.' + tag).lower()

                try:
                    if self.schema[fqtn]['lclSfIdFlg'] == 'Y':
                        lp[tag] = [listId] * len(lp[tag])
                        break
                except KeyError:
                    pass

    def normalize(self, strData):
        """ Wrapper function of normalize_str() and normalize_nef().
        """

        try:
            sf = strData.frame_list[0]
            if sf.category.startswith('nef'):
                return self.normalize_nef(strData)
            return self.normalize_str(strData)
        except (IndexError, AttributeError):
            return strData

    def normalize_str(self, strData):
        """ Sort saveframes, loops, and tags according to NMR-STAR schema.
            @see: pynmrstar.entry.normalize
        """

        def sf_key(sf):
            """ Helper function to sort the saveframes.
            Returns (category order, saveframe order) """

            # If not a real category, generate an artificial but stable order > the real saveframes
            try:
                category_order = self.category_order.index(sf.tag_prefix)
            except (ValueError, KeyError):
                if sf.category is None:
                    category_order = float('infinity')
                else:
                    category_order = len(self.category_order) + abs(int(hashlib.sha1(str(sf.category).encode()).hexdigest(), 16))

            # See if there is an ID tag, and it is a number
            saveframe_id = float('infinity')
            try:
                saveframe_id = int(sf.get_tag("ID")[0])
            except (ValueError, KeyError, IndexError, TypeError):
                # Either there is no ID, or it is not a number. By default it will sort at the end of saveframes of its
                # category. Note that the entry_information ID tag has a different meaning, but since there should
                # only ever be one saveframe of that category, the sort order for it can be any value.
                pass

            return category_order, saveframe_id

        def lp_key(lp):
            """ Helper function to sort the loops.
            Returns (category order) """

            try:
                category_order = self.category_order.index(lp.category)
            except (ValueError, KeyError):
                category_order = float('infinity')

            return category_order

        try:
            strData.frame_list.sort(key=sf_key)
        except Exception as e:
            self.__lfh.write(f"+ERROR- CifToNmrStar.normalize() {str(e)}\n")

        for sf in strData.frame_list:
            sf.sort_tags()
            if len(sf.loops) > 1:
                sf.loops.sort(key=lp_key)
            # Iterate through the loops
            for lp in sf:
                lp.sort_tags()

        return strData

    def normalize_nef(self, strData):
        """ Sort saveframes of NEF.
        """

        def sf_key(sf):
            """ Helper function to sort the saveframes.
            Returns (saveframe order) """

            try:
                category_order = self.category_order_nef.index(sf.tag_prefix)
            except (ValueError, KeyError):
                if sf.category is None:
                    category_order = float('infinity')
                else:
                    category_order = len(self.category_order_nef) + abs(int(hashlib.sha1(str(sf.category).encode()).hexdigest(), 16))

            return category_order

        try:
            strData.frame_list.sort(key=sf_key)
        except Exception as e:
            self.__lfh.write(f"+ERROR- CifToNmrStar.normalize_nef() {str(e)}\n")

        return strData
