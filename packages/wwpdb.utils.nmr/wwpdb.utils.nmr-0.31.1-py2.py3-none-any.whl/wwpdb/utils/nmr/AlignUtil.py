##
# File: AlignUtil.py
# Date: 18-Feb-2022
#
# Updates:
""" Utilities for pairwise alignment.
    @author: Masashi Yokochi
"""
import copy
import json
import re
import io
from itertools import zip_longest


# criterion for low sequence coverage
LOW_SEQ_COVERAGE = 0.3


# criterion for minimum sequence coverage when conflict occurs (NMR conventional deposition)
MIN_SEQ_COVERAGE_W_CONFLICT = 0.95


# empty value
emptyValue = (None, '', '.', '?', 'null', 'None')


# true value
trueValue = ('true', 't', 'yes', 'y', '1')


# taken from wwpdb.utils.align.SequenceReferenceData.py
monDict3 = {'ALA': 'A',
            'ARG': 'R',
            'ASN': 'N',
            'ASP': 'D',
            'ASX': 'B',
            'CYS': 'C',
            'GLN': 'Q',
            'GLU': 'E',
            'GLX': 'Z',
            'GLY': 'G',
            'HIS': 'H',
            'ILE': 'I',
            'LEU': 'L',
            'LYS': 'K',
            'MET': 'M',
            'PHE': 'F',
            'PRO': 'P',
            'SER': 'S',
            'THR': 'T',
            'TRP': 'W',
            'TYR': 'Y',
            'VAL': 'V',
            'DA': 'A',
            'DC': 'C',
            'DG': 'G',
            'DT': 'T',
            'DU': 'U',
            'DI': 'I',
            'A': 'A',
            'C': 'C',
            'G': 'G',
            'I': 'I',
            'T': 'T',
            'U': 'U'
            }

protonBeginCode = ('H', '1', '2', '3')
pseProBeginCode = ('H', 'Q', 'M', '1', '2', '3')
aminoProtonCode = ('H', 'HN', 'H1', 'H2', 'H3', 'HT1', 'HT2', 'HT3')
jcoupBbPairCode = ('N', 'H', 'CA', 'C')
rdcBbPairCode = ('N', 'H', 'CA')

LARGE_ASYM_ID = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
LEN_LARGE_ASYM_ID = len(LARGE_ASYM_ID)

# maximum number of magnetically identifiable chain IDs
MAX_MAG_IDENT_ASYM_ID = 2


def hasLargeInnerSeqGap(polySeq, seqIdName='seq_id'):
    """ Return whether large gap in a sequence.
    """

    _s = polySeq[seqIdName]

    for idx, seqId in enumerate(_s):
        if idx > 0 and seqId - _s[idx - 1] > 20:
            return True

    return False


def hasLargeSeqGap(polySeq1, polySeq2, seqIdName1='seq_id', seqIdName2='seq_id'):
    """ Return whether large gap in combined sequence of polySeq1 and polySeq2.
    """

    _s = sorted(set(polySeq1[seqIdName1]) | set(polySeq2[seqIdName2]))

    for idx, seqId in enumerate(_s):
        if idx > 0 and seqId - _s[idx - 1] > 20:
            return True

    return False


def fillInnerBlankCompId(polySeq, seqIdName='seq_id'):
    """ Fill inner blanked comp_ID.
    """

    _s = list(range(polySeq[seqIdName][0], polySeq[seqIdName][-1] + 1))
    _c = []

    for seqId in _s:
        if seqId in polySeq[seqIdName]:
            idx = polySeq[seqIdName].index(seqId)
            if idx < len(polySeq['comp_id']):
                _c.append(polySeq['comp_id'][idx])
            else:
                _c.append('.')
        else:
            _c.append('.')

    ps = {'chain_id': polySeq['chain_id'], 'seq_id': _s, 'comp_id': _c}
    if 'gap_in_auth_seq' in polySeq:
        ps['gap_in_auth_seq'] = polySeq['gap_in_auth_seq']

    return ps


def fillBlankCompId(polySeq1, polySeq2, seqIdName1='seq_id', seqIdName2='seq_id'):
    """ Fill blanked comp_ID in polySeq2 against polySeq1.
    """

    if seqIdName1 == seqIdName2:
        _s = sorted(set(polySeq1[seqIdName1]) | set(polySeq2[seqIdName2]))
    else:
        _s = polySeq2[seqIdName2]

    _c = []

    for seqId in _s:
        if seqId in polySeq2[seqIdName2]:
            idx = polySeq2[seqIdName2].index(seqId)
            if idx < len(polySeq2['comp_id']):
                _c.append(polySeq2['comp_id'][idx])
            else:
                _c.append('.')
        else:
            _c.append('.')

    ps = {'chain_id': polySeq2['chain_id'], seqIdName2: _s, 'comp_id': _c}
    if seqIdName2 == 'auth_seq_id':
        ps['seq_id'] = polySeq2['seq_id']
    if seqIdName2 == 'seq_id' and 'auth_seq_id' in polySeq2:
        ps['auth_seq_id'] = polySeq2['auth_seq_id']
    if 'gap_in_auth_seq' in polySeq2:
        ps['gap_in_auth_seq'] = polySeq2['gap_in_auth_seq']

    return ps


def fillBlankCompIdWithOffset(polySeq, offset, seqIdName='seq_id'):
    """ Fill blanked comp_ID with offset.
    """

    _s = list(range(polySeq[seqIdName][0] - offset, polySeq[seqIdName][-1] + 1))
    _c = []

    for seqId in _s:
        if seqId in polySeq[seqIdName]:
            idx = polySeq[seqIdName].index(seqId)
            if idx < len(polySeq['comp_id']):
                _c.append(polySeq['comp_id'][idx])
            else:
                _c.append('.')
        else:
            _c.append('.')

    ps = {'chain_id': polySeq['chain_id'], 'seq_id': _s, 'comp_id': _c}
    if 'gap_in_auth_seq' in polySeq:
        ps['gap_in_auth_seq'] = polySeq['gap_in_auth_seq']

    return ps


def beautifyPolySeq(polySeq1, polySeq2, seqIdName1='seq_id', seqIdName2='seq_id'):
    """ Truncate negative seq_IDs and insert spacing between the large gap.
    """

    _polySeq1 = fillBlankCompId(polySeq2, polySeq1, seqIdName2, seqIdName1)  # pylint: disable=arguments-out-of-order
    _polySeq2 = fillBlankCompId(polySeq1, polySeq2, seqIdName1, seqIdName2)  # pylint: disable=arguments-out-of-order

    if _polySeq1[seqIdName1] != _polySeq2[seqIdName2]:
        return _polySeq1, _polySeq2

    _s = [seqId for seqId in _polySeq1[seqIdName1] if seqId > 0]
    _c1 = [compId for seqId, compId
           in zip(_polySeq1[seqIdName1], _polySeq1['comp_id']) if seqId > 0]
    _c2 = [compId for seqId, compId
           in zip(_polySeq1[seqIdName1], _polySeq2['comp_id']) if seqId > 0]

    gapS = []
    gapP = []

    lenSpacer = 5  # DAOTHER-7465, issue #2

    for idx, seqId in enumerate(_s):
        if idx > 0 and seqId - _s[idx - 1] > 20:
            prevSeqId = _s[idx - 1]
            for sp in range(1, lenSpacer + 1):
                gapS.append(prevSeqId + sp)
                gapS.append(seqId - sp)
            gapP.append(idx)

    if len(gapS) == 0:
        ps1 = {'chain_id': _polySeq1['chain_id'], 'seq_id': _s, 'comp_id': _c1}
        ps2 = {'chain_id': _polySeq2['chain_id'], 'seq_id': _s, 'comp_id': _c2}

        if 'gap_in_auth_seq' in polySeq1:
            ps1['gap_in_auth_seq'] = polySeq1['gap_in_auth_seq']
        if 'gap_in_auth_seq' in polySeq2:
            ps2['gap_in_auth_seq'] = polySeq2['gap_in_auth_seq']

        return ps1, ps2

    _s.extend(gapS)
    _s.sort()

    for p in reversed(gapP):
        for sp in range(1, lenSpacer + 1):
            _c1.insert(p, '.')
            _c2.insert(p, '.')

    ps1 = {'chain_id': _polySeq1['chain_id'], 'seq_id': _s, 'comp_id': _c1}
    ps2 = {'chain_id': _polySeq2['chain_id'], 'seq_id': _s, 'comp_id': _c2}

    if 'gap_in_auth_seq' in polySeq1:
        ps1['gap_in_auth_seq'] = polySeq1['gap_in_auth_seq']
    if 'gap_in_auth_seq' in polySeq2:
        ps2['gap_in_auth_seq'] = polySeq2['gap_in_auth_seq']

    return ps1, ps2


def getMiddleCode(seqIdList1, seqIdList2):
    """ Return array of middle code of sequence alignment.
    """

    f = []

    for idx, seqId in enumerate(seqIdList1):
        f.append('|' if idx < len(seqIdList2) and seqId == seqIdList2[idx] and seqId != '.' else ' ')

    return ''.join(f)


def getGaugeCode(seqIdList, offset=0):
    """ Return gauge code for a give sequence.
    """

    if offset > 0:
        _seqIdList = list(range(1, offset + 1))
        for idx, seqId in enumerate(seqIdList):
            if idx < offset:
                continue
            _seqIdList.append(seqId)
        seqIdList = _seqIdList

    lenSeqId = len([seqId for seqId in seqIdList if seqId is not None])
    lenCode = 0

    chars = []

    for seqId in seqIdList:

        if seqId is None:
            chars.append('-')
            continue

        if seqId >= 0 and seqId % 10 == 0 and lenCode == 0:

            code = str(seqId)
            lenCode = len(code)

            for p in range(lenCode):
                chars.append(code[p])

        if lenCode > 0:
            lenCode -= 1
        else:
            chars.append('-')

    lenChars = len(chars)

    for idx, seqId in enumerate(seqIdList):

        if seqId is None or seqId % 10 != 0:
            continue

        code = str(seqId)
        lenCode = len(code)

        if idx - lenCode > 0:
            for p in range(lenCode):
                if idx + p - lenCode + 1 >= 0 and idx + p < lenChars:
                    chars[idx + p - lenCode + 1] = chars[idx + p]
                    chars[idx + p] = '-'

    if offset > 0:
        for p in range(offset):
            chars[p] = '-'

    gaugeCode = ''.join(chars)

    if lenSeqId == len(seqIdList):
        return gaugeCode[:lenSeqId]

    _lenSeqId = len(seqIdList)

    offset = 0
    for idx, seqId in enumerate(seqIdList):

        if seqId is None:
            p = idx + offset
            gaugeCode = gaugeCode[0:p] + ' ' + gaugeCode[p:]
            offset += 1

    return gaugeCode[:_lenSeqId]


def getScoreOfSeqAlign(myAlign):
    """ Return score of sequence alignment.
    """

    length = len(myAlign)

    aligned = [True] * length

    for p in range(length):
        myPr = myAlign[p]
        myPr0 = str(myPr[0])
        myPr1 = str(myPr[1])
        if myPr0 == '.' or myPr1 == '.':
            aligned[p] = False
        elif myPr0 != myPr1:
            pass
        else:
            break

    notAligned = True
    offset1 = 0
    offset2 = 0

    unmapped = 0
    conflict = 0
    matched = 0
    for p in range(length):
        myPr = myAlign[p]
        myPr0 = str(myPr[0])
        myPr1 = str(myPr[1])
        if myPr0 == '.' or myPr1 == '.':
            if notAligned and not aligned[p]:
                if myPr0 == '.' and myPr1 != '.'\
                   and offset2 == 0:  # DAOTHER-7421
                    offset1 += 1
                if myPr0 != '.' and myPr1 == '.'\
                   and offset1 == 0:  # DAOTHER-7421
                    offset2 += 1
                if myPr0 == '.' and myPr1 == '.':  # DAOTHER-7465
                    if offset2 == 0:
                        offset1 += 1
                    if offset1 == 0:
                        offset2 += 1
            unmapped += 1
        elif myPr0 != myPr1:
            conflict += 1
        else:
            notAligned = False
            matched += 1

    return matched, unmapped, conflict, offset1, offset2


def getOneLetterCode(compId):
    """ Convert comp_ID to 1-letter code.
    """

    compId = compId.upper()

    if compId in monDict3:
        return monDict3[compId]

    if compId in emptyValue:
        return '.'

    return 'X'


def getCanOneLetterCode(compId):
    """ Convert comp_ID to canonical 1-letter code.
    """

    compId = compId.upper()

    if compId in monDict3:
        return monDict3[compId]

    if compId in emptyValue:
        return '.'

    return f'({compId})'


def getOneLetterCodeSequence(compIdList):
    """ Convert array of comp_IDs to 1-letter code sequence.
    """

    f = []

    for compId in compIdList:
        f.append(getOneLetterCode(compId))

    return ''.join(f)


def getCanOneLetterCodeSequence(compIdList):
    """ Convert array of comp_IDs to canonical 1-letter code sequence.
    """

    f = []

    for compId in compIdList:
        f.append(getCanOneLetterCode(compId))

    return ''.join(f)


def letterToDigit(code, minDigit=0):
    """ Return digit from a given chain code.
    """

    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    unit = 1
    digit = 0

    for char in ''.join(reversed(code.lower())):

        if char.isdigit():
            digit += unit * int(char)
        elif char.isalpha():
            digit += unit * (alphabet.index(char) + 1)
        else:
            continue

        unit *= 27

    return digit if digit > minDigit else minDigit


def indexToLetter(index):
    """ Return chain code from a given index (0 based).
    """

    if index < 0:
        return '.'

    if index > 19683:
        index = index % 19683

    if index < 27:
        return str(chr(65 + index))

    if index < 729:
        return str(chr(64 + (index // 27)))\
            + str(chr(65 + (index % 27)))

    return str(chr(64 + (index // 729)))\
        + str(chr(64 + ((index % 729) // 27)))\
        + str(chr(65 + (index % 27)))


def getRestraintFormatName(fileType, ambig=False):
    """ Return restraint format name.
    """

    if fileType == 'nm-res-xpl':
        return 'XPLOR-NIH/CNS restraint' if ambig else 'XPLOR-NIH restraint'
    if fileType == 'nm-res-cns':
        return 'CNS/XPLOR-NIH restraint' if ambig else 'CNS restraint'
    if fileType == 'nm-res-amb':
        return 'AMBER restraint'
    if fileType == 'nm-aux-amb':
        return 'AMBER topology'
    if fileType == 'nm-res-cya':
        return 'CYANA restraint'
    if fileType == 'nm-res-ros':
        return 'ROSETTA restraint'
    if fileType == 'nm-res-bio':
        return 'BIOSYM restraint'
    if fileType == 'nm-res-gro':
        return 'GROMACS restraint'
    if fileType == 'nm-aux-gro':
        return 'GROMACS topology'
    if fileType == 'nm-res-dyn':
        return 'DYNAMO/PALES/TALOS restraint'
    if fileType == 'nm-res-syb':
        return 'SYBYL restraint'
    if fileType == 'nm-res-isd':
        return 'ISD restraint'
    if fileType == 'nm-res-cha':
        return 'CHARMM restraint'
    if fileType == 'nmr-star':
        return 'NMR-STAR data'
    if fileType == 'nm-res-mr':
        return 'MR data'
    return 'other restraint'


def updatePolySeqRst(polySeqRst, chainId, seqId, compId, authCompId=None):
    """ Update polymer sequence of the current MR file.
    """

    ps = next((ps for ps in polySeqRst if ps['chain_id'] == chainId), None)
    if ps is None:
        polySeqRst.append({'chain_id': chainId, 'seq_id': [], 'comp_id': [], 'auth_comp_id': []})
        ps = polySeqRst[-1]

    if seqId not in ps['seq_id']:
        ps['seq_id'].append(seqId)
        ps['comp_id'].append(compId)
        ps['auth_comp_id'].append(compId if authCompId is None else authCompId)


def updatePolySeqRstFromAtomSelectionSet(polySeqRst, atomSelectionSet):
    """ Update polymer sequence of the current MR file.
    """

    if len(atomSelectionSet) == 0:
        return

    for atomSelection in atomSelectionSet:
        if len(atomSelection) == 0:
            continue
        for atom in atomSelection:
            chainId = atom['chain_id']
            seqId = atom['seq_id']
            compId = atom.get('comp_id', '.')

            updatePolySeqRst(polySeqRst, chainId, seqId, compId)


def sortPolySeqRst(polySeqRst, nonPolyRemap=None):
    """ Sort polymer sequence of the current MR file by sequence number.
    """

    if polySeqRst is None:
        return

    if nonPolyRemap is None:

        for ps in polySeqRst:
            minSeqId = min(ps['seq_id'])
            maxSeqId = max(ps['seq_id'])

            _seqIds = list(range(minSeqId, maxSeqId + 1))
            _compIds = ["."] * (maxSeqId - minSeqId + 1)
            _authCompIds = ["."] * (maxSeqId - minSeqId + 1)

            for idx, seqId in enumerate(ps['seq_id']):
                _compIds[_seqIds.index(seqId)] = ps['comp_id'][idx]
                _authCompIds[_seqIds.index(seqId)] = ps['auth_comp_id'][idx]

            ps['seq_id'] = _seqIds
            ps['comp_id'] = _compIds
            ps['auth_comp_id'] = _authCompIds

    else:

        remapList = []

        for compId, compIdMap in nonPolyRemap.items():
            for seqIdMap in compIdMap.values():
                remapList.append({'chain_id': seqIdMap['chain_id'],
                                  'seq_id': seqIdMap['seq_id'],
                                  'comp_id': compId})

        for ps in polySeqRst:
            seqIds = [seqId for seqId in ps['seq_id']
                      if not any(item for item in remapList if item['chain_id'] == ps['chain_id'] and item['seq_id'] == seqId)]

            if len(seqIds) == 0:
                continue

            minSeqId = min(seqIds)
            maxSeqId = max(seqIds)

            _seqIds = list(range(minSeqId, maxSeqId + 1))
            _compIds = ["."] * (maxSeqId - minSeqId + 1)
            _authCompIds = ["."] * (maxSeqId - minSeqId + 1)

            for idx, seqId in enumerate(ps['seq_id']):
                if minSeqId <= seqId <= maxSeqId:
                    _compIds[_seqIds.index(seqId)] = ps['comp_id'][idx]
                    _authCompIds[_seqIds.index(seqId)] = ps['auth_comp_id'][idx]

            _endSeqIds = []
            _endCompIds = []
            _endAuthCompIds = []

            _begSeqIds = []
            _begCompIds = []
            _begAuthCompIds = []

            for item in remapList:
                if item['chain_id'] != ps['chain_id']:
                    continue
                seqId = item['seq_id']
                compId = item['comp_id']
                if seqId in ps['seq_id']:
                    authCompId = ps['auth_comp_id'][ps['seq_id'].index(seqId)]
                else:
                    authCompId = next(item['comp_id'] for item in remapList
                                      if item['chain_id'] == ps['chain_id'] and item['seq_id'] == seqId)
                if seqId > maxSeqId:
                    _endSeqIds.append(seqId)
                    _endCompIds.append(compId)
                    _endAuthCompIds.append(authCompId)
                elif seqId < minSeqId:
                    _begSeqIds.append(seqId)
                    _begCompIds.append(compId)
                    _begAuthCompIds.append(authCompId)

            if len(_begSeqIds) > 0:
                _begSeqIds.extend(_seqIds)
                _begCompIds.extend(_compIds)
                _begAuthCompIds.extend(_authCompIds)
                _seqIds = _begSeqIds
                _compIds = _begCompIds
                _authCompIds = _begAuthCompIds

            if len(_endSeqIds) > 0:
                _seqIds.extend(_endSeqIds)
                _compIds.extend(_endCompIds)
                _authCompIds.extend(_endAuthCompIds)

            ps['seq_id'] = _seqIds
            ps['comp_id'] = _compIds
            ps['auth_comp_id'] = _authCompIds


def stripPolySeqRst(polySeqRst):
    """ Strip polymer sequence of the current MR file.
    """

    if polySeqRst is None:
        return

    for ps in polySeqRst:
        seq_ids = copy.copy(ps['seq_id'])
        comp_ids = copy.copy(ps['comp_id'])

        has_auth_comp_id = 'auth_comp_id' in ps

        if has_auth_comp_id:
            auth_comp_ids = copy.copy(ps['auth_comp_id'])

        idx = 0
        while idx < len(seq_ids):
            if comp_ids[idx] != '.':
                break
            idx += 1

        if idx != 0:
            seq_ids = seq_ids[idx - 1:]
            comp_ids = comp_ids[idx - 1:]

            if has_auth_comp_id:
                auth_comp_ids = auth_comp_ids[idx - 1:]

        len_seq_ids = len(seq_ids)
        idx = len_seq_ids - 1
        while idx >= 0:
            if comp_ids[idx] != '.':
                break
            idx -= 1

        if idx != len_seq_ids - 1:
            seq_ids = seq_ids[:idx + 1]
            comp_ids = comp_ids[:idx + 1]

            if has_auth_comp_id:
                auth_comp_ids = auth_comp_ids[:idx + 1]

        if len(ps['seq_id']) != len(seq_ids):
            ps['seq_id'] = seq_ids
            ps['comp_id'] = comp_ids

            if has_auth_comp_id:
                ps['auth_comp_id'] = auth_comp_ids


def alignPolymerSequence(pA, polySeqModel, polySeqRst, conservative=True, resolvedMultimer=False):
    """ Align polymer sequence of the coordinates and restraints.
    """

    seqAlign = []
    compIdMapping = []

    if pA is None or polySeqModel is None or polySeqRst is None:
        return seqAlign, compIdMapping

    tabooList = []
    inhibitList = []

    hasMultimer = False

    truncated = None

    for i1, s1 in enumerate(polySeqModel):
        chain_id_name = 'auth_chain_id' if 'auth_chain_id' in s1 else 'chain_id'
        chain_id = s1[chain_id_name]

        if i1 >= LEN_LARGE_ASYM_ID:
            continue

        seq_id_name = 'auth_seq_id' if 'auth_seq_id' in s1 else 'seq_id'

        for i2, s2 in enumerate(polySeqRst):
            chain_id2 = s2['chain_id']

            if i2 >= LEN_LARGE_ASYM_ID:
                continue

            not_decided_s2_comp_id = any(c2 for c2 in s2['comp_id'] if c2.endswith('?'))  # AMBER/GROMACS topology
            if not_decided_s2_comp_id:
                s2 = copy.deepcopy(s2)
                s2['comp_id'] = [c2[:-1] if c2.endswith('?') else c2 for c2 in s2['comp_id']]

            pA.setReferenceSequence(s1['comp_id'], 'REF' + chain_id)
            pA.addTestSequence(s2['comp_id'], chain_id)
            pA.doAlign()

            myAlign = pA.getAlignment(chain_id)

            length = len(myAlign)

            if length == 0:
                tabooList.append({chain_id, chain_id2})
                continue

            _matched, unmapped, conflict, offset_1, offset_2 = getScoreOfSeqAlign(myAlign)

            if length == unmapped + conflict or _matched <= conflict:
                inhibitList.append({chain_id, chain_id2})
                continue

            if not_decided_s2_comp_id:  # AMBER/GROMACS topology
                idx2 = 0
                for i in range(length):
                    myPr = myAlign[i]
                    myPr0 = str(myPr[0])
                    myPr1 = str(myPr[1])
                    if myPr1 != '.':
                        while idx2 < len(s2['seq_id']):
                            if s2['comp_id'][idx2] == myPr1:
                                s2_seq_id = s2['seq_id'][idx2]
                                s2_auth_comp_id = s2['auth_comp_id'][idx2]
                                compIdMapping.append({'chain_id': chain_id2, 'seq_id': s2_seq_id,
                                                      'comp_id': myPr0, 'auth_comp_id': s2_auth_comp_id})
                                idx2 += 1
                                break

            _s1 = s1 if offset_1 == 0 else fillBlankCompIdWithOffset(s1, offset_1, seqIdName=seq_id_name)
            _s2 = s2 if offset_2 == 0 else fillBlankCompIdWithOffset(s2, offset_2)

            if conflict == 0:
                if hasLargeInnerSeqGap(_s2) and not hasLargeInnerSeqGap(_s1):
                    _s2 = fillInnerBlankCompId(_s2)

            _seq_id_name = 'auth_seq_id' if 'auth_seq_id' in _s1 else 'seq_id'

            if 'gap_in_auth_seq' in s1 and s1['gap_in_auth_seq']:

                for p in range(len(s1[seq_id_name]) - 1):
                    s_p = s1[seq_id_name][p]
                    s_q = s1[seq_id_name][p + 1]
                    if s_p is None or s_q is None or s_p not in s2['seq_id'] or s_q not in s2['seq_id']:
                        continue
                    if s_p + 1 != s_q:
                        beg = s2['seq_id'].index(s_p)
                        end = s2['seq_id'].index(s_q)
                        comp_ids = s2['comp_id'][beg + 1:end]
                        if not any(comp_id for comp_id in comp_ids if comp_id != '.'):
                            s2['seq_id'] = s2['seq_id'][:beg + 1] + s2['seq_id'][end:]
                            s2['comp_id'] = s2['comp_id'][:beg + 1] + s2['comp_id'][end:]
                            if 'auth_comp_id' in s2:
                                s2['auth_comp_id'] = s2['auth_comp_id'][:beg + 1] + s2['auth_comp_id'][end:]
                            s2['gap_in_auth_seq'] = True
                        beg = _s2['seq_id'].index(s_p)
                        end = _s2['seq_id'].index(s_q)
                        comp_ids = _s2['comp_id'][beg + 1:end]
                        if not any(comp_id for comp_id in comp_ids if comp_id != '.'):
                            _s2['seq_id'] = _s2['seq_id'][:beg + 1] + _s2['seq_id'][end:]
                            _s2['comp_id'] = _s2['comp_id'][:beg + 1] + _s2['comp_id'][end:]
                            if 'auth_comp_id' in _s2:
                                _s2['auth_comp_id'] = _s2['auth_comp_id'][:beg + 1] + _s2['auth_comp_id'][end:]
                            _s2['gap_in_auth_seq'] = True

            if conflict > 0 and hasLargeSeqGap(_s1, _s2, seqIdName1=_seq_id_name):
                __s1, __s2 = beautifyPolySeq(_s1, _s2, seqIdName1=_seq_id_name)

                if 'gap_in_auth_seq' in s1 and s1['gap_in_auth_seq']:

                    for p in range(len(s1[seq_id_name]) - 1):
                        s_p = s1[seq_id_name][p]
                        s_q = s1[seq_id_name][p + 1]
                        if s_p is None or s_q is None or s_p not in __s2['seq_id'] or s_q not in __s2['seq_id']:
                            continue
                        if s_p + 1 != s_q:
                            beg = __s2['seq_id'].index(s_p)
                            end = __s2['seq_id'].index(s_q)
                            comp_ids = __s2['comp_id'][beg + 1:end]
                            if not any(comp_id for comp_id in comp_ids if comp_id != '.'):
                                __s2['seq_id'] = __s2['seq_id'][:beg + 1] + __s2['seq_id'][end:]
                                __s2['comp_id'] = __s2['comp_id'][:beg + 1] + __s2['comp_id'][end:]
                                if 'auth_comp_id' in __s2:
                                    __s2['auth_comp_id'] = __s2['auth_comp_id'][:beg + 1] + __s2['auth_comp_id'][end:]
                                __s2['gap_in_auth_seq'] = True

                _s1_ = __s1
                _s2_ = __s2

                pA.setReferenceSequence(_s1_['comp_id'], 'REF' + chain_id)
                pA.addTestSequence(_s2_['comp_id'], chain_id)
                pA.doAlign()

                myAlign = pA.getAlignment(chain_id)

                length = len(myAlign)

                _matched, unmapped, _conflict, _offset_1, _offset_2 = getScoreOfSeqAlign(myAlign)

                if _conflict == 0 and len(__s2['comp_id']) - len(s2['comp_id']) == conflict:
                    conflict = 0
                    offset_1 = _offset_1
                    offset_2 = _offset_2
                    _s1 = __s1
                    _s2 = __s2

            if conflict == 0 and _matched > 0 and unmapped > 0 and 'gap_in_auth_seq' in s1 and s1['gap_in_auth_seq']:
                for p in range(len(s1[seq_id_name]) - 1):
                    s_p = s1[seq_id_name][p]
                    s_q = s1[seq_id_name][p + 1]
                    if s_p is None or s_q is None or s_p not in s2['seq_id'] or s_q not in s2['seq_id']:
                        continue
                    if s_p + 1 != s_q:
                        idx1 = 0
                        idx2 = 0
                        beg = -1
                        for i in range(length):
                            myPr = myAlign[i]
                            myPr0 = str(myPr[0])
                            myPr1 = str(myPr[1])
                            if idx1 < len(s1[seq_id_name]):
                                if s1[seq_id_name][idx1] == s_p:
                                    beg = idx2
                            if myPr0 != '.':
                                while idx1 < len(_s1['seq_id']):
                                    if _s1['comp_id'][idx1] == myPr0:
                                        idx1 += 1
                                        break
                                    idx1 += 1
                            if myPr1 != '.':
                                while idx2 < len(_s2['seq_id']):
                                    if _s2['comp_id'][idx2] == myPr1:
                                        idx2 += 1
                                        break
                                    idx2 += 1
                        if beg >= 0 and beg + 1 < len(_s2['seq_id']) and _s2['seq_id'][beg] == s_p and _s2['seq_id'][beg + 1] == s_p + 1:
                            beg = s2['seq_id'].index(s_p)
                            end = s2['seq_id'].index(s_q)
                            comp_ids = s2['comp_id'][beg + 1:end]
                            if not any(comp_id for comp_id in comp_ids if comp_id != '.'):
                                truncated = (s_p, s_q)
                                break

            _seq_id_name = 'auth_seq_id' if 'auth_seq_id' in _s1 else 'seq_id'

            if conflict > 0 and not hasLargeSeqGap(_s1, _s2, seqIdName1=_seq_id_name):
                tabooList.append({chain_id, chain_id2})

            ref_length = len(s1[seq_id_name])

            ref_code = getOneLetterCodeSequence(_s1['comp_id'])
            test_code = getOneLetterCodeSequence(_s2['comp_id'])
            mid_code = getMiddleCode(ref_code, test_code)
            ref_gauge_code = getGaugeCode(_s1['seq_id'])
            test_gauge_code = getGaugeCode(_s2['seq_id'])

            if any((__s1, __s2) for (__s1, __s2, __c1, __c2)
                   in zip(_s1['seq_id'], _s2['seq_id'], _s1['comp_id'], _s2['comp_id'])
                   if __c1 != '.' and __c2 != '.' and __c1 != __c2):
                seq_id1 = []
                seq_id2 = []
                comp_id1 = []
                comp_id2 = []
                idx1 = 0
                idx2 = 0
                for i in range(length):
                    myPr = myAlign[i]
                    myPr0 = str(myPr[0])
                    myPr1 = str(myPr[1])
                    if myPr0 != '.':
                        while idx1 < len(_s1['seq_id']):
                            if _s1['comp_id'][idx1] == myPr0:
                                seq_id1.append(_s1['seq_id'][idx1])
                                comp_id1.append(myPr0)
                                idx1 += 1
                                break
                            idx1 += 1
                    else:
                        seq_id1.append(None)
                        comp_id1.append('.')
                    if myPr1 != '.':
                        while idx2 < len(_s2['seq_id']):
                            if _s2['comp_id'][idx2] == myPr1:
                                seq_id2.append(_s2['seq_id'][idx2])
                                comp_id2.append(myPr1)
                                idx2 += 1
                                break
                            idx2 += 1
                    else:
                        seq_id2.append(None)
                        comp_id2.append('.')
                ref_code = getOneLetterCodeSequence(comp_id1)
                test_code = getOneLetterCodeSequence(comp_id2)
                mid_code = getMiddleCode(ref_code, test_code)
                ref_gauge_code = getGaugeCode(seq_id1, offset_1)
                test_gauge_code = getGaugeCode(seq_id2, offset_2)
                if ' ' in ref_gauge_code:
                    for p, g in enumerate(ref_gauge_code):
                        if g == ' ':
                            ref_code = ref_code[0:p] + '-' + ref_code[p + 1:]
                if ' ' in test_gauge_code:
                    for p, g in enumerate(test_gauge_code):
                        if g == ' ':
                            test_code = test_code[0:p] + '-' + test_code[p + 1:]

            matched = mid_code.count('|')

            seq_align = {'ref_chain_id': chain_id, 'test_chain_id': chain_id2, 'length': ref_length,
                         'matched': matched, 'conflict': conflict, 'unmapped': unmapped,
                         'sequence_coverage': float(f"{float(length - (unmapped + conflict)) / ref_length:.3f}"),
                         'ref_seq_id': _s1['seq_id'], 'test_seq_id': _s2['seq_id'],
                         'ref_gauge_code': ref_gauge_code, 'ref_code': ref_code, 'mid_code': mid_code,
                         'test_code': test_code, 'test_gauge_code': test_gauge_code}

            if 'auth_seq_id' in _s1:
                seq_align['ref_auth_seq_id'] = _s1['auth_seq_id']

            if 'identical_auth_chain_id' in s1:
                hasMultimer = True

            seqAlign.append(seq_align)

    if truncated is not None:
        s_p, s_q = truncated

        for s2 in polySeqRst:

            if s_p not in s2['seq_id'] or s_q not in s2['seq_id']:
                continue

            beg = s2['seq_id'].index(s_p)
            end = s2['seq_id'].index(s_q)
            comp_ids = s2['comp_id'][beg + 1:end]

            if not any(comp_id for comp_id in comp_ids if comp_id != '.'):
                s2['seq_id'] = s2['seq_id'][:beg + 1] + s2['seq_id'][end:]
                s2['comp_id'] = s2['comp_id'][:beg + 1] + s2['comp_id'][end:]
                if 'auth_comp_id' in s2:
                    s2['auth_comp_id'] = s2['auth_comp_id'][:beg + 1] + s2['auth_comp_id'][end:]
                s2['gap_in_auth_seq'] = True

        return alignPolymerSequence(pA, polySeqModel, polySeqRst, conservative, resolvedMultimer)

    if len(tabooList) > 0:
        _seqAlign = copy.copy(seqAlign)
        for sa in _seqAlign:
            if {sa['ref_chain_id'], sa['test_chain_id']} in tabooList:
                seqAlign.remove(sa)

    if len(inhibitList) > 0 and conservative:
        _seqAlign = copy.copy(seqAlign)
        for sa in _seqAlign:
            if {sa['ref_chain_id'], sa['test_chain_id']} in inhibitList:
                seqAlign.remove(sa)

    if hasMultimer and resolvedMultimer:
        _seqAlign = copy.copy(seqAlign)
        seqAlign = []
        for sa in _seqAlign:
            ref_chain_id = sa['ref_chain_id']
            test_chain_id = sa['test_chain_id']
            s1 = next(ps for ps in polySeqModel if ps['auth_chain_id'] == ref_chain_id)
            if 'identical_auth_chain_id' not in s1 or ref_chain_id == test_chain_id:
                seqAlign.append(sa)

    return seqAlign, compIdMapping


def alignPolymerSequenceWithConflicts(pA, polySeqModel, polySeqRst, conflictTh=1):
    """ Align polymer sequence of the coordinates and restraints allowing minor conflicts.
    """

    seqAlign = []
    compIdMapping = []

    if pA is None or polySeqModel is None or polySeqRst is None:
        return seqAlign, compIdMapping

    truncated = None

    for i1, s1 in enumerate(polySeqModel):
        chain_id_name = 'auth_chain_id' if 'auth_chain_id' in s1 else 'chain_id'
        chain_id = s1[chain_id_name]

        if i1 >= LEN_LARGE_ASYM_ID:
            continue

        seq_id_name = 'auth_seq_id' if 'auth_seq_id' in s1 else 'seq_id'

        for i2, s2 in enumerate(polySeqRst):
            chain_id2 = s2['chain_id']

            if i2 >= LEN_LARGE_ASYM_ID:
                continue

            not_decided_s2_comp_id = any(c2 for c2 in s2['comp_id'] if c2.endswith('?'))  # AMBER/GROMACS topology
            if not_decided_s2_comp_id:
                s2 = copy.deepcopy(s2)
                s2['comp_id'] = [c2[:-1] if c2.endswith('?') else c2 for c2 in s2['comp_id']]

            pA.setReferenceSequence(s1['comp_id'], 'REF' + chain_id)
            pA.addTestSequence(s2['comp_id'], chain_id)
            pA.doAlign()

            myAlign = pA.getAlignment(chain_id)

            length = len(myAlign)

            if length == 0:
                continue

            _matched, unmapped, conflict, offset_1, offset_2 = getScoreOfSeqAlign(myAlign)

            if length == unmapped + conflict or _matched <= conflict - conflictTh:
                continue

            if not_decided_s2_comp_id:  # AMBER/GROMACS topology
                idx2 = 0
                for i in range(length):
                    myPr = myAlign[i]
                    myPr0 = str(myPr[0])
                    myPr1 = str(myPr[1])
                    if myPr1 != '.':
                        while idx2 < len(s2['seq_id']):
                            if s2['comp_id'][idx2] == myPr1:
                                s2_seq_id = s2['seq_id'][idx2]
                                s2_auth_comp_id = s2['auth_comp_id'][idx2]
                                compIdMapping.append({'chain_id': chain_id2, 'seq_id': s2_seq_id,
                                                      'comp_id': myPr0, 'auth_comp_id': s2_auth_comp_id})
                                idx2 += 1
                                break

            _s1 = s1 if offset_1 == 0 else fillBlankCompIdWithOffset(s1, offset_1, seqIdName=seq_id_name)
            _s2 = s2 if offset_2 == 0 else fillBlankCompIdWithOffset(s2, offset_2)

            if conflict == 0:
                if hasLargeInnerSeqGap(_s2) and not hasLargeInnerSeqGap(_s1):
                    _s2 = fillInnerBlankCompId(_s2)

            _seq_id_name = 'auth_seq_id' if 'auth_seq_id' in _s1 else 'seq_id'

            if 'gap_in_auth_seq' in s1 and s1['gap_in_auth_seq']:

                for p in range(len(s1[seq_id_name]) - 1):
                    s_p = s1[seq_id_name][p]
                    s_q = s1[seq_id_name][p + 1]
                    if s_p is None or s_q is None or s_p not in s2['seq_id'] or s_q not in s2['seq_id']:
                        continue
                    if s_p + 1 != s_q:
                        beg = s2['seq_id'].index(s_p)
                        end = s2['seq_id'].index(s_q)
                        comp_ids = s2['comp_id'][beg + 1:end]
                        if not any(comp_id for comp_id in comp_ids if comp_id != '.'):
                            s2['seq_id'] = s2['seq_id'][:beg + 1] + s2['seq_id'][end:]
                            s2['comp_id'] = s2['comp_id'][:beg + 1] + s2['comp_id'][end:]
                            if 'auth_comp_id' in s2:
                                s2['auth_comp_id'] = s2['auth_comp_id'][:beg + 1] + s2['auth_comp_id'][end:]
                            s2['gap_in_auth_seq'] = True
                        beg = _s2['seq_id'].index(s_p)
                        end = _s2['seq_id'].index(s_q)
                        comp_ids = _s2['comp_id'][beg + 1:end]
                        if not any(comp_id for comp_id in comp_ids if comp_id != '.'):
                            _s2['seq_id'] = _s2['seq_id'][:beg + 1] + _s2['seq_id'][end:]
                            _s2['comp_id'] = _s2['comp_id'][:beg + 1] + _s2['comp_id'][end:]
                            if 'auth_comp_id' in _s2:
                                _s2['auth_comp_id'] = _s2['auth_comp_id'][:beg + 1] + _s2['auth_comp_id'][end:]
                            _s2['gap_in_auth_seq'] = True

            if conflict > 0 and hasLargeSeqGap(_s1, _s2, seqIdName1=_seq_id_name):
                __s1, __s2 = beautifyPolySeq(_s1, _s2, seqIdName1=_seq_id_name)

                if 'gap_in_auth_seq' in s1 and s1['gap_in_auth_seq']:

                    for p in range(len(s1[seq_id_name]) - 1):
                        s_p = s1[seq_id_name][p]
                        s_q = s1[seq_id_name][p + 1]
                        if s_p is None or s_q is None or s_p not in __s2['seq_id'] or s_q not in __s2['seq_id']:
                            continue
                        if s_p + 1 != s_q:
                            beg = __s2['seq_id'].index(s_p)
                            end = __s2['seq_id'].index(s_q)
                            comp_ids = __s2['comp_id'][beg + 1:end]
                            if not any(comp_id for comp_id in comp_ids if comp_id != '.'):
                                __s2['seq_id'] = __s2['seq_id'][:beg + 1] + __s2['seq_id'][end:]
                                __s2['comp_id'] = __s2['comp_id'][:beg + 1] + __s2['comp_id'][end:]
                                if 'auth_comp_id' in __s2:
                                    __s2['auth_comp_id'] = __s2['auth_comp_id'][:beg + 1] + __s2['auth_comp_id'][end:]
                                __s2['gap_in_auth_seq'] = True

                _s1_ = __s1
                _s2_ = __s2

                pA.setReferenceSequence(_s1_['comp_id'], 'REF' + chain_id)
                pA.addTestSequence(_s2_['comp_id'], chain_id)
                pA.doAlign()

                myAlign = pA.getAlignment(chain_id)

                length = len(myAlign)

                _matched, unmapped, _conflict, _offset_1, _offset_2 = getScoreOfSeqAlign(myAlign)

                if _conflict == 0 and len(__s2['comp_id']) - len(s2['comp_id']) == conflict:
                    conflict = 0
                    offset_1 = _offset_1
                    offset_2 = _offset_2
                    _s1 = __s1
                    _s2 = __s2

            if conflict == 0 and _matched > 0 and unmapped > 0 and 'gap_in_auth_seq' in s1 and s1['gap_in_auth_seq']:
                for p in range(len(s1[seq_id_name]) - 1):
                    s_p = s1[seq_id_name][p]
                    s_q = s1[seq_id_name][p + 1]
                    if s_p is None or s_q is None or s_p not in s2['seq_id'] or s_q not in s2['seq_id']:
                        continue
                    if s_p + 1 != s_q:
                        idx1 = 0
                        idx2 = 0
                        beg = -1
                        for i in range(length):
                            myPr = myAlign[i]
                            myPr0 = str(myPr[0])
                            myPr1 = str(myPr[1])
                            if idx1 < len(s1[seq_id_name]):
                                if s1[seq_id_name][idx1] == s_p:
                                    beg = idx2
                            if myPr0 != '.':
                                while idx1 < len(_s1['seq_id']):
                                    if _s1['comp_id'][idx1] == myPr0:
                                        idx1 += 1
                                        break
                                    idx1 += 1
                            if myPr1 != '.':
                                while idx2 < len(_s2['seq_id']):
                                    if _s2['comp_id'][idx2] == myPr1:
                                        idx2 += 1
                                        break
                                    idx2 += 1
                        if beg >= 0 and beg + 1 < len(_s2['seq_id']) and _s2['seq_id'][beg] == s_p and _s2['seq_id'][beg + 1] == s_p + 1:
                            beg = s2['seq_id'].index(s_p)
                            end = s2['seq_id'].index(s_q)
                            comp_ids = s2['comp_id'][beg + 1:end]
                            if not any(comp_id for comp_id in comp_ids if comp_id != '.'):
                                truncated = (s_p, s_q)
                                break

            if conflict > conflictTh:
                continue

            _seq_id_name = 'auth_seq_id' if 'auth_seq_id' in _s1 else 'seq_id'

            ref_length = len(s1[seq_id_name])

            ref_code = getOneLetterCodeSequence(_s1['comp_id'])
            test_code = getOneLetterCodeSequence(_s2['comp_id'])
            mid_code = getMiddleCode(ref_code, test_code)
            ref_gauge_code = getGaugeCode(_s1['seq_id'])
            test_gauge_code = getGaugeCode(_s2['seq_id'])

            if any((__s1, __s2) for (__s1, __s2, __c1, __c2)
                   in zip(_s1['seq_id'], _s2['seq_id'], _s1['comp_id'], _s2['comp_id'])
                   if __c1 != '.' and __c2 != '.' and __c1 != __c2):
                seq_id1 = []
                seq_id2 = []
                comp_id1 = []
                comp_id2 = []
                idx1 = 0
                idx2 = 0
                for i in range(length):
                    myPr = myAlign[i]
                    myPr0 = str(myPr[0])
                    myPr1 = str(myPr[1])
                    if myPr0 != '.':
                        while idx1 < len(_s1['seq_id']):
                            if _s1['comp_id'][idx1] == myPr0:
                                seq_id1.append(_s1['seq_id'][idx1])
                                comp_id1.append(myPr0)
                                idx1 += 1
                                break
                            idx1 += 1
                    else:
                        seq_id1.append(None)
                        comp_id1.append('.')
                    if myPr1 != '.':
                        while idx2 < len(_s2['seq_id']):
                            if _s2['comp_id'][idx2] == myPr1:
                                seq_id2.append(_s2['seq_id'][idx2])
                                comp_id2.append(myPr1)
                                idx2 += 1
                                break
                            idx2 += 1
                    else:
                        seq_id2.append(None)
                        comp_id2.append('.')
                ref_code = getOneLetterCodeSequence(comp_id1)
                test_code = getOneLetterCodeSequence(comp_id2)
                mid_code = getMiddleCode(ref_code, test_code)
                ref_gauge_code = getGaugeCode(seq_id1, offset_1)
                test_gauge_code = getGaugeCode(seq_id2, offset_2)
                if ' ' in ref_gauge_code:
                    for p, g in enumerate(ref_gauge_code):
                        if g == ' ':
                            ref_code = ref_code[0:p] + '-' + ref_code[p + 1:]
                if ' ' in test_gauge_code:
                    for p, g in enumerate(test_gauge_code):
                        if g == ' ':
                            test_code = test_code[0:p] + '-' + test_code[p + 1:]

            matched = mid_code.count('|')

            seq_align = {'ref_chain_id': chain_id, 'test_chain_id': chain_id2, 'length': ref_length,
                         'matched': matched, 'conflict': conflict, 'unmapped': unmapped,
                         'sequence_coverage': float(f"{float(length - (unmapped + conflict)) / ref_length:.3f}"),
                         'ref_seq_id': _s1['seq_id'], 'test_seq_id': _s2['seq_id'],
                         'ref_gauge_code': ref_gauge_code, 'ref_code': ref_code, 'mid_code': mid_code,
                         'test_code': test_code, 'test_gauge_code': test_gauge_code}

            if 'auth_seq_id' in _s1:
                seq_align['ref_auth_seq_id'] = _s1['auth_seq_id']

            seqAlign.append(seq_align)

    if truncated is not None:
        s_p, s_q = truncated

        for s2 in polySeqRst:

            if s_p not in s2['seq_id'] or s_q not in s2['seq_id']:
                continue

            beg = s2['seq_id'].index(s_p)
            end = s2['seq_id'].index(s_q)
            comp_ids = s2['comp_id'][beg + 1:end]

            if not any(comp_id for comp_id in comp_ids if comp_id != '.'):
                s2['seq_id'] = s2['seq_id'][:beg + 1] + s2['seq_id'][end:]
                s2['comp_id'] = s2['comp_id'][:beg + 1] + s2['comp_id'][end:]
                if 'auth_comp_id' in s2:
                    s2['auth_comp_id'] = s2['auth_comp_id'][:beg + 1] + s2['auth_comp_id'][end:]
                s2['gap_in_auth_seq'] = True

        return alignPolymerSequenceWithConflicts(pA, polySeqModel, polySeqRst, conflictTh=conflictTh)

    return seqAlign, compIdMapping


def assignPolymerSequence(pA, ccU, fileType, polySeqModel, polySeqRst, seqAlign):
    """ Assign polymer sequences of restraints.
    """

    if pA is None or polySeqModel is None or polySeqRst is None or seqAlign is None:
        return None, []

    warnings = []

    mrFormatName = getRestraintFormatName(fileType)
    _a_mr_format_name = 'the ' + mrFormatName

    mr_chains = len(polySeqRst) if len(polySeqRst) < LEN_LARGE_ASYM_ID else LEN_LARGE_ASYM_ID

    mat = []
    indices = []

    for i1, s1 in enumerate(polySeqModel):
        chain_id_name = 'auth_chain_id' if 'auth_chain_id' in s1 else 'chain_id'
        chain_id = s1[chain_id_name]

        if i1 >= LEN_LARGE_ASYM_ID:
            continue

        seq_id_name = 'auth_seq_id' if 'auth_seq_id' in s1 else 'seq_id'

        cost = [0 for i in range(mr_chains)]

        for i2, s2 in enumerate(polySeqRst):
            chain_id2 = s2['chain_id']

            if i2 >= LEN_LARGE_ASYM_ID:
                continue

            result = next((seq_align for seq_align in seqAlign
                           if seq_align['ref_chain_id'] == chain_id
                           and seq_align['test_chain_id'] == chain_id2), None)

            if result is not None:
                cost[polySeqRst.index(s2)] = result['unmapped'] + result['conflict'] - result['length']
                if result['length'] >= len(s1[seq_id_name]) - result['unmapped']:
                    indices.append((polySeqModel.index(s1), polySeqRst.index(s2)))

        mat.append(cost)

    chainAssign = []

    for row, col in indices:

        if mat[row][col] >= 0:

            has_row = has_col = False
            for _row, _col in indices:
                if mat[_row][_col] < 0:
                    if _row == row:
                        has_row = True
                    if _col == col:
                        has_col = True

            if has_row and has_col:
                continue

            _cif_chains = []
            for _row, _col in indices:
                if col == _col:
                    _cif_chains.append(polySeqModel[_row][chain_id_name])

            if len(_cif_chains) > 1:
                chain_id2 = polySeqRst[col]['chain_id']

                warnings.append(f"[Concatenated sequence] The chain ID {chain_id2!r} of the sequences in {_a_mr_format_name} file "
                                f"will be re-assigned to the chain IDs {_cif_chains} in the coordinates during biocuration.")

        chain_id = polySeqModel[row][chain_id_name]
        chain_id2 = polySeqRst[col]['chain_id']

        result = next(seq_align for seq_align in seqAlign
                      if seq_align['ref_chain_id'] == chain_id and seq_align['test_chain_id'] == chain_id2)

        if result['matched'] == 0:
            continue

        ca = {'ref_chain_id': chain_id, 'test_chain_id': chain_id2, 'length': result['length'],
              'matched': result['matched'], 'conflict': result['conflict'], 'unmapped': result['unmapped'],
              'sequence_coverage': result['sequence_coverage']}

        s1 = next(s for s in polySeqModel if s[chain_id_name] == chain_id)
        s2 = next(s for s in polySeqRst if s['chain_id'] == chain_id2)

        pA.setReferenceSequence(s1['comp_id'], 'REF' + chain_id)
        pA.addTestSequence(s2['comp_id'], chain_id)
        pA.doAlign()

        myAlign = pA.getAlignment(chain_id)

        length = len(myAlign)

        _matched, unmapped, conflict, offset_1, offset_2 = getScoreOfSeqAlign(myAlign)

        _s1 = s1 if offset_1 == 0 else fillBlankCompIdWithOffset(s1, offset_1, seqIdName=seq_id_name)
        _s2 = s2 if offset_2 == 0 else fillBlankCompIdWithOffset(s2, offset_2)

        if conflict == 0:
            if hasLargeInnerSeqGap(_s2) and not hasLargeInnerSeqGap(_s1):
                _s2 = fillInnerBlankCompId(_s2)

        _seq_id_name = 'auth_seq_id' if 'auth_seq_id' in _s1 else 'seq_id'

        if conflict > 0 and hasLargeSeqGap(_s1, _s2, seqIdName1=_seq_id_name):
            __s1, __s2 = beautifyPolySeq(_s1, _s2, seqIdName1=_seq_id_name)
            _s1 = __s1
            _s2 = __s2

            pA.setReferenceSequence(_s1['comp_id'], 'REF' + chain_id)
            pA.addTestSequence(_s2['comp_id'], chain_id)
            pA.doAlign()

            myAlign = pA.getAlignment(chain_id)

            length = len(myAlign)

            _matched, unmapped, _conflict, _, _ = getScoreOfSeqAlign(myAlign)

            if _conflict == 0 and len(__s2['comp_id']) - len(s2['comp_id']) == conflict:
                result['conflict'] = 0
                s2 = __s2

        if result['unmapped'] > 0 or result['conflict'] > 0:

            aligned = [True] * length
            seq_id1 = []
            seq_id2 = []

            j = 0
            for i in range(length):
                if str(myAlign[i][0]) != '.' and j < len(s1[seq_id_name]):
                    seq_id1.append(s1[seq_id_name][j])
                    j += 1
                else:
                    seq_id1.append(None)

            j = 0
            for i in range(length):
                if str(myAlign[i][1]) != '.' and j < len(s2['seq_id']):
                    seq_id2.append(s2['seq_id'][j])
                    j += 1
                else:
                    seq_id2.append(None)

            for i in range(length):
                myPr = myAlign[i]
                myPr0 = str(myPr[0])
                myPr1 = str(myPr[1])
                if myPr0 == '.' or myPr1 == '.':
                    aligned[i] = False
                elif myPr0 != myPr1:
                    pass
                else:
                    break

            for i in reversed(range(length)):
                myPr = myAlign[i]
                myPr0 = str(myPr[0])
                myPr1 = str(myPr[1])
                if myPr0 == '.' or myPr1 == '.':
                    aligned[i] = False
                elif myPr0 != myPr1:
                    pass
                else:
                    break

            _conflicts = 0

            for i in range(length):
                myPr = myAlign[i]
                if myPr[0] == myPr[1]:
                    continue

                cif_comp_id = str(myPr[0])
                mr_comp_id = str(myPr[1])

                if mr_comp_id == '.' and cif_comp_id != '.':
                    pass

                elif mr_comp_id != cif_comp_id and aligned[i]:
                    _conflicts += 1

            if fileType.startswith('nm-aux') and _conflicts > ca['unmapped'] and ca['sequence_coverage'] < MIN_SEQ_COVERAGE_W_CONFLICT:
                continue

            if _conflicts + offset_1 > _matched and ca['sequence_coverage'] < LOW_SEQ_COVERAGE:  # DAOTHER-7825 (2lyw)
                continue

            unmapped = []
            conflict = []

            for i in range(length):
                myPr = myAlign[i]
                if myPr[0] == myPr[1]:
                    continue

                cif_comp_id = str(myPr[0])
                mr_comp_id = str(myPr[1])

                if mr_comp_id == '.' and cif_comp_id != '.':

                    unmapped.append({'ref_seq_id': seq_id1[i], 'ref_comp_id': cif_comp_id})
                    # """ unmapped residue is not error """
                    # if not aligned[i]:

                    #     if not ccU.updateChemCompDict(cif_comp_id):
                    #         continue

                    #     if ccU.lastChemCompDict['_chem_comp.pdbx_release_status'] != 'REL':
                    #         continue

                    #     cif_seq_code = f"{chain_id}:{seq_id1[i]}:{cif_comp_id}"

                    #     warnings.append(f"[Sequence mismatch] {cif_seq_code} is not present "
                    #                     f"in {_a_mr_format_name} data (chain_id {chain_id2}).")
                    #
                elif mr_comp_id != cif_comp_id and aligned[i]:

                    comp_ids = [comp_id for seq_id, comp_id in zip(s1[_seq_id_name], s1['comp_id']) if seq_id == seq_id1[i]]

                    if mr_comp_id in comp_ids:
                        continue

                    conflict.append({'ref_seq_id': seq_id1[i], 'ref_comp_id': cif_comp_id,
                                     'test_seq_id': seq_id2[i], 'test_comp_id': mr_comp_id})

                    cif_seq_code = f"{chain_id}:{seq_id1[i]}:{cif_comp_id}"
                    if cif_comp_id == '.':
                        cif_seq_code += ', insertion error'
                    mr_seq_code = f"{chain_id2}:{seq_id2[i]}:{mr_comp_id}"
                    if mr_comp_id == '.':
                        mr_seq_code += ', insertion error'

                    if cif_comp_id != '.':

                        if not ccU.updateChemCompDict(cif_comp_id):
                            continue

                        if ccU.lastChemCompDict['_chem_comp.pdbx_release_status'] != 'REL':
                            continue

                        if getOneLetterCode(cif_comp_id) == 'X':
                            continue

                    warnings.append(f"[Sequence mismatch] Sequence alignment error between the coordinate ({cif_seq_code}) "
                                    f"and {_a_mr_format_name} data ({mr_seq_code}). "
                                    "Please verify the two sequences and re-upload the correct file(s) if required.")

            if len(unmapped) > 0:
                ca['unmapped_sequence'] = unmapped

            if len(conflict) > 0:
                ca['conflict_sequence'] = conflict
                ca['conflict'] = len(conflict)
                ca['unmapped'] = ca['unmapped'] - len(conflict)
                if ca['unmapped'] < 0:
                    ca['conflict'] -= ca['unmapped']
                    ca['unmapped'] = 0

                result['conflict'] = ca['conflict']
                result['unmapped'] = ca['unmapped']

        chainAssign.append(ca)

    if len(chainAssign) > 0 and len(polySeqModel) > 1:

        if any(s for s in polySeqModel if 'identical_auth_chain_id' in s):

            _chainAssign = copy.copy(chainAssign)

            for ca in _chainAssign:

                if ca['conflict'] > 0:
                    continue

                chain_id = ca['ref_chain_id']

                try:
                    identity = next(s['identical_auth_chain_id'] for s in polySeqModel
                                    if s['auth_chain_id'] == chain_id and 'identical_auth_chain_id' in s)

                    for chain_id in identity:

                        if not any(_ca for _ca in chainAssign if _ca['ref_chain_id'] == chain_id):
                            _ca = copy.copy(ca)
                            _ca['ref_chain_id'] = chain_id
                            chainAssign.append(_ca)

                            sa = next(sa for sa in seqAlign if sa['ref_chain_id'] == ca['ref_chain_id'])
                            _sa = copy.copy(sa)
                            _sa['ref_chain_id'] = chain_id
                            seqAlign.append(_sa)

                except StopIteration:
                    pass

    return chainAssign, warnings


def trimSequenceAlignment(seqAlign, chainAssign):
    """ Trim ineffective sequence alignments.
    """

    if seqAlign is None or chainAssign is None:
        return

    ineffSeqAlignIdx = list(range(len(seqAlign) - 1, -1, -1))

    for ca in chainAssign:
        ref_chain_id = ca['ref_chain_id']
        test_chain_id = ca['test_chain_id']

        effSeqAlignIdx = next((idx for idx, seq_align in enumerate(seqAlign)
                              if seq_align['ref_chain_id'] == ref_chain_id
                              and seq_align['test_chain_id'] == test_chain_id), None)

        if effSeqAlignIdx is not None and effSeqAlignIdx in ineffSeqAlignIdx:
            ineffSeqAlignIdx.remove(effSeqAlignIdx)

    if len(ineffSeqAlignIdx) > 0:
        for idx in ineffSeqAlignIdx:
            del seqAlign[idx]


def retrieveAtomIdentFromMRMap(mrAtomNameMapping, seqId, compId, atomId, coordAtomSite=None, ignoreSeqId=False):
    """ Retrieve atom identifiers from atom name mapping of public MR file.
    """

    elemName = atomId[0]

    mapping = [item for item in mrAtomNameMapping
               if (item['original_seq_id'] == seqId or ignoreSeqId)
               and compId in (item['original_comp_id'], item['auth_comp_id'])]

    if len(mapping) == 0:
        return seqId, compId, atomId

    if elemName in ('Q', 'M'):

        item = next((item for item in mapping
                     if item['original_atom_id'] == 'H' + atomId[1:] + '2'), None)

        if item is not None:

            if coordAtomSite is not None and item['auth_atom_id'] not in coordAtomSite['atom_id']:
                return seqId, compId, atomId

            return item['auth_seq_id'], item['auth_comp_id'], \
                item['auth_atom_id'][:-1] + '%' if item['auth_atom_id'][0].isalpha() else '%' + item['auth_atom_id'][1:]

        if len(atomId) > 1:

            item = next((item for item in mapping
                         if item['original_atom_id'] == '2H' + atomId[1:]), None)

            if item is not None:

                if coordAtomSite is not None and item['auth_atom_id'] not in coordAtomSite['atom_id']:
                    return seqId, compId, atomId

                return item['auth_seq_id'], item['auth_comp_id'], \
                    item['auth_atom_id'][:-1] + '%' if item['auth_atom_id'][0].isalpha() else '%' + item['auth_atom_id'][1:]

    if elemName == 'H' and atomId[-1] in ('1', '2', '3'):

        item = next((item for item in mapping
                     if item['original_atom_id'] == atomId), None)

        if item is None:

            _atomId = atomId[-1] + atomId[:-1]

            item = next((item for item in mapping
                         if item['original_atom_id'] == _atomId), None)

            if item is not None:

                if coordAtomSite is not None and item['auth_atom_id'] not in coordAtomSite['atom_id']:
                    return seqId, compId, atomId

                return item['auth_seq_id'], item['auth_comp_id'], item['auth_atom_id']

            if atomId[-1] == '1':
                _atomId = '3' + atomId[:-1]

                item = next((item for item in mapping
                             if item['original_atom_id'] == _atomId), None)

                if item is not None:

                    if coordAtomSite is not None and item['auth_atom_id'] not in coordAtomSite['atom_id']:
                        return seqId, compId, atomId

                    return item['auth_seq_id'], item['auth_comp_id'], item['auth_atom_id']

    if elemName == 'H' or (elemName in ('1', '2', '3') and len(atomId) > 1 and atomId[1] == 'H'):

        item = next((item for item in mapping
                     if item['original_atom_id'] == atomId), None)

        if item is not None:

            _atomId_ = item['auth_atom_id']

            if coordAtomSite is not None and _atomId_ not in coordAtomSite['atom_id']:

                total = 0
                for _atomId in coordAtomSite['atom_id']:
                    if _atomId.startswith(_atomId_):
                        total += 1

                if total == 1:
                    return item['auth_seq_id'], item['auth_comp_id'], \
                        next(_atomId for _atomId in coordAtomSite['atom_id'] if _atomId.startswith(_atomId_))

                return seqId, compId, atomId

            return item['auth_seq_id'], item['auth_comp_id'], _atomId_

        if coordAtomSite is not None and atomId not in coordAtomSite['atom_id']:

            total = 0
            for _atomId in coordAtomSite['atom_id']:
                if _atomId.startswith(atomId):
                    total += 1

            if total == 1:
                return mapping[0]['auth_seq_id'], mapping[0]['auth_comp_id'], \
                    next(_atomId for _atomId in coordAtomSite['atom_id'] if _atomId.startswith(atomId))

        return seqId, compId, atomId

    _atomId = 'H' + atomId[1:]

    item = next((item for item in mapping
                 if item['original_atom_id'] == _atomId), None)

    if item is not None:

        _atomId_ = elemName + item['auth_atom_id'][1:]

        if coordAtomSite is not None and _atomId not in coordAtomSite['atom_id']:

            total = 0
            for __atomId in coordAtomSite['atom_id']:
                if __atomId.startswith(_atomId_):
                    total += 1

            if total == 1:
                _atomId = next(_atomId for _atomId in coordAtomSite['atom_id'] if _atomId.startswith(_atomId_))
                return item['auth_seq_id'], item['auth_comp_id'], _atomId

            return seqId, compId, atomId

        return item['auth_seq_id'], item['auth_comp_id'], _atomId_

    _atomId = 'H' + atomId[1:] + '2'

    item = next((item for item in mapping
                 if item['original_atom_id'] == _atomId), None)

    if item is not None:

        _atomId_ = elemName + item['auth_atom_id'][1:-1]

        if coordAtomSite is not None and _atomId not in coordAtomSite['atom_id']:

            total = 0
            for __atomId in coordAtomSite['atom_id']:
                if __atomId.startswith(_atomId_):
                    total += 1

            if total == 1:
                _atomId = next(_atomId for _atomId in coordAtomSite['atom_id'] if _atomId.startswith(_atomId_))
                return item['auth_seq_id'], item['auth_comp_id'], _atomId

            return seqId, compId, atomId

        return item['auth_seq_id'], item['auth_comp_id'], _atomId_

    if atomId[-1] in ('1', '2'):

        order = int(atomId[-1]) - 1
        _atomId = 'H' + atomId[1:-1]

        item = next((item for item in mapping
                     if item['original_atom_id'] == _atomId), None)

        if item is not None:

            _atomId_ = elemName + item['auth_atom_id'][1:]

            if coordAtomSite is not None:
                candidate = sorted(__atomId for __atomId in coordAtomSite['atom_id'] if __atomId.startswith(_atomId_))

                if order < len(candidate):
                    return item['auth_seq_id'], item['auth_comp_id'], candidate[order]

        elif coordAtomSite is not None and atomId not in coordAtomSite['atom_id']:

            _atomId_ = atomId[:-1]

            candidate = sorted(__atomId for __atomId in coordAtomSite['atom_id'] if __atomId.startswith(_atomId_))

            if order < len(candidate):
                return item['auth_seq_id'], item['auth_comp_id'], candidate[order]

    if len(atomId) == 1:

        if coordAtomSite is not None and atomId not in coordAtomSite['atom_id']:

            total = 0
            for __atomId in coordAtomSite['atom_id']:
                if __atomId.startswith(atomId):
                    total += 1

            if total == 1:
                _atomId = next(_atomId for _atomId in coordAtomSite['atom_id'] if _atomId.startswith(atomId))
                return item['auth_seq_id'], item['auth_comp_id'], _atomId

    return seqId, compId, atomId


def retrieveAtomIdFromMRMap(mrAtomNameMapping, cifSeqId, cifCompId, atomId, coordAtomSite=None, ignoreSeqId=False):
    """ Retrieve atom_id from atom name mapping of public MR file.
    """

    elemName = atomId[0]

    mapping = [item for item in mrAtomNameMapping
               if (item['auth_seq_id'] == cifSeqId or ignoreSeqId)
               and cifCompId in (item['auth_comp_id'], item['original_comp_id'])]

    if len(mapping) == 0:
        return atomId

    if elemName in ('Q', 'M'):

        item = next((item for item in mapping
                     if item['original_atom_id'] in ('H' + atomId[1:] + '2', '2H' + atomId[1:])), None)

        if item is not None:

            if coordAtomSite is not None and item['auth_atom_id'] not in coordAtomSite['atom_id']:
                return atomId

            return item['auth_atom_id'][:-1] + '%' if item['auth_atom_id'][0].isalpha() else '%' + item['auth_atom_id'][1:]

        if len(atomId) > 1:

            item = next((item for item in mapping
                         if item['original_atom_id'] == '2H' + atomId[1:]), None)

            if item is not None:

                if coordAtomSite is not None and item['auth_atom_id'] not in coordAtomSite['atom_id']:
                    return atomId

                return item['auth_atom_id'][:-1] + '%' if item['auth_atom_id'][0].isalpha() else '%' + item['auth_atom_id'][1:]

    if elemName == 'H' and atomId[-1] in ('1', '2', '3'):

        item = next((item for item in mapping
                     if item['original_atom_id'] == atomId), None)

        if item is None:

            _atomId = atomId[-1] + atomId[:-1]

            item = next((item for item in mapping
                         if item['original_atom_id'] == _atomId), None)

            if item is not None:

                if coordAtomSite is not None and item['auth_atom_id'] not in coordAtomSite['atom_id']:
                    return atomId

                return item['auth_atom_id']

            if atomId[-1] == '1':
                _atomId = '3' + atomId[:-1]

                item = next((item for item in mapping
                             if item['original_atom_id'] == _atomId), None)

                if item is not None:

                    if coordAtomSite is not None and item['auth_atom_id'] not in coordAtomSite['atom_id']:
                        return atomId

                    return item['auth_atom_id']

    if elemName == 'H' or (elemName in ('1', '2', '3') and len(atomId) > 1 and atomId[1] == 'H'):

        item = next((item for item in mapping
                     if item['original_atom_id'] == atomId), None)

        if item is not None:

            _atomId_ = item['auth_atom_id']

            if coordAtomSite is not None and _atomId_ not in coordAtomSite['atom_id']:

                total = 0
                for _atomId in coordAtomSite['atom_id']:
                    if _atomId.startswith(_atomId_):
                        total += 1

                if total == 1:
                    return next(_atomId for _atomId in coordAtomSite['atom_id'] if _atomId.startswith(_atomId_))

                return atomId

            return _atomId_

        if coordAtomSite is not None and atomId not in coordAtomSite['atom_id']:

            total = 0
            for _atomId in coordAtomSite['atom_id']:
                if _atomId.startswith(atomId):
                    total += 1

            if total == 1:
                return next(_atomId for _atomId in coordAtomSite['atom_id'] if _atomId.startswith(atomId))

        return atomId

    _atomId = 'H' + atomId[1:]

    item = next((item for item in mapping
                 if item['original_atom_id'] == _atomId), None)

    if item is not None:
        _atomId_ = elemName + item['auth_atom_id'][1:]

        if coordAtomSite is not None and _atomId_ not in coordAtomSite['atom_id']:

            total = 0
            for __atomId in coordAtomSite['atom_id']:
                if __atomId.startswith(_atomId_):
                    total += 1

                if total == 1:
                    return next(_atomId for _atomId in coordAtomSite['atom_id'] if _atomId.startswith(_atomId_))

            return atomId

        return _atomId_

    _atomId = 'H' + atomId[1:] + '2'

    item = next((item for item in mapping
                 if item['original_atom_id'] == _atomId), None)

    if item is not None:
        _atomId_ = elemName + item['auth_atom_id'][1:-1]

        if coordAtomSite is not None and _atomId not in coordAtomSite['atom_id']:

            total = 0
            for __atomId in coordAtomSite['atom_id']:
                if __atomId.startswith(_atomId_):
                    total += 1

                if total == 1:
                    return next(_atomId for _atomId in coordAtomSite['atom_id'] if _atomId.startswith(_atomId_))

            return atomId

        return _atomId_

    if atomId[-1] in ('1', '2'):

        order = int(atomId[-1]) - 1
        _atomId = 'H' + atomId[1:-1]

        item = next((item for item in mapping
                     if item['original_atom_id'] == _atomId), None)

        if item is not None:

            _atomId_ = elemName + item['auth_atom_id'][1:]

            if coordAtomSite is not None:
                candidate = sorted(__atomId for __atomId in coordAtomSite['atom_id'] if __atomId.startswith(_atomId_))

                if order < len(candidate):
                    return candidate[order]

        elif coordAtomSite is not None and atomId not in coordAtomSite['atom_id']:

            _atomId_ = atomId[:-1]

            candidate = sorted(__atomId for __atomId in coordAtomSite['atom_id'] if __atomId.startswith(_atomId_))

            if order < len(candidate):
                return candidate[order]

    if len(atomId) == 1:

        if coordAtomSite is not None and atomId not in coordAtomSite['atom_id']:

            total = 0
            for __atomId in coordAtomSite['atom_id']:
                if __atomId.startswith(atomId):
                    total += 1

            if total == 1:
                _atomId = next(_atomId for _atomId in coordAtomSite['atom_id'] if _atomId.startswith(atomId))
                return _atomId

    return atomId


def retrieveRemappedSeqId(seqIdRemap, chainId, seqId):
    """ Retrieve seq_id from mapping dictionary based on sequence alignments.
    """

    try:

        if chainId is None:
            remap = next(remap for remap in seqIdRemap if seqId in remap['seq_id_dict'])
        else:
            remap = next(remap for remap in seqIdRemap if seqId in remap['seq_id_dict'] and remap['chain_id'] == chainId)

        return remap['chain_id'], remap['seq_id_dict'][seqId]

    except StopIteration:
        return None, None


def splitPolySeqRstForMultimers(pA, polySeqModel, polySeqRst, chainAssign):
    """ Split polymer sequence of the current MR file for multimers.
    """

    if polySeqModel is None or polySeqRst is None or chainAssign is None:
        return None, None

    target_chain_ids = {}
    for ca in chainAssign:
        if ca['conflict'] == 0 and ca['unmapped'] > 0:
            ref_chain_id = ca['ref_chain_id']
            test_chain_id = ca['test_chain_id']
            if test_chain_id not in target_chain_ids:
                target_chain_ids[test_chain_id] = []
            target_chain_ids[test_chain_id].append(ref_chain_id)

    if len(target_chain_ids) == 0:
        return None, None

    split = False

    _polySeqRst = copy.copy(polySeqRst)
    _chainIdMapping = {}

    for test_chain_id, ref_chain_ids in target_chain_ids.items():

        total_gaps = len(ref_chain_ids) - 1

        if total_gaps == 0:
            continue

        len_ref_ps = []

        for ref_chain_id in ref_chain_ids:
            ref_ps = next(ps for ps in polySeqModel if ps['auth_chain_id'] == ref_chain_id)
            len_ref_ps.append(len(ref_ps['seq_id']))

        sum_len_ref_ps = sum(len_ref_ps)

        test_ps = next(ps for ps in _polySeqRst if ps['chain_id'] == test_chain_id)
        len_test_ps = len(test_ps['seq_id'])

        if sum_len_ref_ps < len_test_ps or len_test_ps > sum_len_ref_ps / len(ref_chain_ids):
            half_gap = (len_test_ps - sum_len_ref_ps) // (total_gaps * 2) if sum_len_ref_ps < len_test_ps else 0

            _test_ps = copy.copy(test_ps)

            _polySeqRst.remove(test_ps)

            offset = 0

            for idx, ref_chain_id in enumerate(ref_chain_ids):
                ref_ps = next(ps for ps in polySeqModel if ps['auth_chain_id'] == ref_chain_id)
                half_len_ref_ps = len(ref_ps['seq_id']) // 2

                beg = offset
                end = offset + len(ref_ps['seq_id'])

                if len_test_ps - end < half_len_ref_ps or idx == total_gaps:
                    end = len_test_ps

                if beg >= len(_test_ps['seq_id']):
                    break

                while True:
                    if _test_ps['comp_id'][beg] != '.':
                        break
                    beg += 1
                    if beg == end:
                        return None, None

                end = beg + len(ref_ps['seq_id']) + half_gap

                if len_test_ps - end < half_len_ref_ps or idx == total_gaps:
                    end = len_test_ps

                while True:
                    if _test_ps['comp_id'][end - 1] != '.':
                        break
                    end -= 1
                    if end == beg:
                        return None, None

                _test_ps_ = {'chain_id': ref_chain_id,
                             'seq_id': _test_ps['seq_id'][beg:end],
                             'comp_id': _test_ps['comp_id'][beg:end]}

                pA.setReferenceSequence(ref_ps['comp_id'], 'REF' + ref_chain_id)
                pA.addTestSequence(_test_ps_['comp_id'], ref_chain_id)
                pA.doAlign()

                myAlign = pA.getAlignment(ref_chain_id)

                length = len(myAlign)

                if length == 0:
                    return None, None

                # _, _, conflict, _, _ = getScoreOfSeqAlign(myAlign)

                # if conflict > 0:
                #     return None, None

                _polySeqRst.append(_test_ps_)

                ref_seq_ids = []
                test_seq_ids = []
                idx1 = 0
                idx2 = 0
                for i in range(length):
                    myPr = myAlign[i]
                    myPr0 = str(myPr[0])
                    myPr1 = str(myPr[1])
                    if myPr0 != '.':
                        while idx1 < len(ref_ps['auth_seq_id']):
                            if ref_ps['comp_id'][idx1] == myPr0:
                                ref_seq_ids.append(ref_ps['auth_seq_id'][idx1])
                                idx1 += 1
                                break
                            idx1 += 1
                    else:
                        ref_seq_ids.append(None)
                    if myPr1 != '.':
                        while idx2 < len(_test_ps_['seq_id']):
                            if _test_ps_['comp_id'][idx2] == myPr1:
                                test_seq_ids.append(_test_ps_['seq_id'][idx2])
                                idx2 += 1
                                break
                            idx2 += 1
                    else:
                        test_seq_ids.append(None)

                offset_in_chain = next((test_seq_id - ref_seq_id for ref_seq_id, test_seq_id
                                        in zip(ref_seq_ids, test_seq_ids)
                                        if ref_seq_id is not None and test_seq_id is not None), None)
                for ref_seq_id, test_seq_id in zip(ref_seq_ids, test_seq_ids):
                    if ref_seq_id is not None:
                        if test_seq_id is not None:
                            offset_in_chain = test_seq_id - ref_seq_id
                            _chainIdMapping[test_seq_id] = {'chain_id': ref_chain_id,
                                                            'seq_id': ref_seq_id}
                        elif offset_in_chain is not None:
                            test_seq_id = ref_seq_id + offset_in_chain
                            _chainIdMapping[test_seq_id] = {'chain_id': ref_chain_id,
                                                            'seq_id': ref_seq_id}

                split = True

                offset = end + half_gap

    if not split:
        return None, None

    return _polySeqRst, _chainIdMapping


def splitPolySeqRstForExactNoes(pA, polySeqModel, polySeqRst, chainAssign):
    """ Split polymer sequence of the current MR file for eNOEs-guided multiple conformers.
    """

    if polySeqModel is None or polySeqRst is None or chainAssign is None:
        return None, None, None

    target_chain_ids = {}
    for ca in chainAssign:
        if ca['conflict'] == 0 and ca['unmapped'] > 0:
            ref_chain_id = ca['ref_chain_id']
            test_chain_id = ca['test_chain_id']
            if test_chain_id not in target_chain_ids:
                target_chain_ids[test_chain_id] = []
            target_chain_ids[test_chain_id].append(ref_chain_id)

    if len(target_chain_ids) == 0:
        return None, None, None

    split = False

    _polySeqRst = copy.copy(polySeqRst)
    _chainIdMapping = {}
    _modelChainIdExt = {}

    for test_chain_id, ref_chain_ids in target_chain_ids.items():

        total_gaps = len(ref_chain_ids) - 1

        if total_gaps != 0:
            continue

        ref_chain_id = ref_chain_ids[0]

        ref_ps = next(ps for ps in polySeqModel if ps['auth_chain_id'] == ref_chain_id)
        len_ref_ps = len(ref_ps['seq_id'])

        test_ps = next(ps for ps in _polySeqRst if ps['chain_id'] == test_chain_id)
        len_test_ps = len(test_ps['seq_id'])

        if len_ref_ps * 1.5 < len_test_ps:

            total_gaps = len_test_ps // len_ref_ps - 1
            if total_gaps == 0:
                total_gaps = 1

            half_gap = (len_test_ps - len_ref_ps * (total_gaps + 1)) // (total_gaps * 2) if len_ref_ps < len_test_ps else 0
            half_gap = max(half_gap, 0)

            _test_ps = copy.copy(test_ps)

            _polySeqRst.remove(test_ps)

            offset = 0

            for idx in range(total_gaps + 1):
                half_len_ref_ps = len_ref_ps // 2

                beg = offset
                end = offset + len_ref_ps

                if len_test_ps - end < half_len_ref_ps or idx == total_gaps:
                    end = len_test_ps

                if beg >= len(_test_ps['seq_id']):
                    break

                while True:
                    if _test_ps['comp_id'][beg] != '.':
                        break
                    beg += 1
                    if beg == end:
                        return None, None, None

                end = beg + len(ref_ps['seq_id']) + half_gap

                if len_test_ps - end < half_len_ref_ps or idx == total_gaps:
                    end = len_test_ps

                if idx == 0 and half_gap == 0:

                    pA.setReferenceSequence(ref_ps['comp_id'], 'REF' + ref_chain_id)
                    pA.addTestSequence(test_ps['comp_id'], ref_chain_id)
                    pA.doAlign()

                    myAlign = pA.getAlignment(ref_chain_id)

                    length = len(myAlign)

                    if length == 0:
                        return None, None, None

                    _, _, conflict, _, _ = getScoreOfSeqAlign(myAlign)

                    if conflict > 0:
                        return None, None, None

                    ref_seq_ids = []
                    test_seq_ids = []
                    idx1 = 0
                    idx2 = 0
                    for i in range(length):
                        myPr = myAlign[i]
                        myPr0 = str(myPr[0])
                        myPr1 = str(myPr[1])
                        if myPr0 != '.':
                            while idx1 < len(ref_ps['auth_seq_id']):
                                if ref_ps['comp_id'][idx1] == myPr0:
                                    ref_seq_ids.append(ref_ps['auth_seq_id'][idx1])
                                    idx1 += 1
                                    break
                                idx1 += 1
                        else:
                            ref_seq_ids.append(None)
                        if myPr1 != '.':
                            while idx2 < len(test_ps['seq_id']):
                                if test_ps['comp_id'][idx2] == myPr1:
                                    test_seq_ids.append(test_ps['seq_id'][idx2])
                                    idx2 += 1
                                    break
                                idx2 += 1
                        else:
                            test_seq_ids.append(None)

                    _test_seq_id = test_ps['seq_id'][0]
                    for ref_seq_id, test_seq_id in zip(ref_seq_ids, test_seq_ids):
                        if ref_seq_id is not None and test_seq_id is not None:
                            _test_seq_id = test_seq_id

                    end = test_ps['seq_id'].index(_test_seq_id) + 1

                while True:
                    if _test_ps['comp_id'][end - 1] != '.':
                        break
                    end -= 1
                    if end == beg:
                        return None, None, None

                _ref_chain_id = ref_chain_id + (str(idx + 1) if idx > 0 else '')

                _test_ps_ = {'chain_id': _ref_chain_id,
                             'seq_id': _test_ps['seq_id'][beg:end],
                             'comp_id': _test_ps['comp_id'][beg:end]}

                pA.setReferenceSequence(ref_ps['comp_id'], 'REF' + _ref_chain_id)
                pA.addTestSequence(_test_ps_['comp_id'], _ref_chain_id)
                pA.doAlign()

                myAlign = pA.getAlignment(_ref_chain_id)

                length = len(myAlign)

                if length == 0:
                    return None, None, None

                _, _, conflict, _, _ = getScoreOfSeqAlign(myAlign)

                if conflict > 0:
                    return None, None, None

                _polySeqRst.append(_test_ps_)

                ref_seq_ids = []
                test_seq_ids = []
                idx1 = 0
                idx2 = 0
                for i in range(length):
                    myPr = myAlign[i]
                    myPr0 = str(myPr[0])
                    myPr1 = str(myPr[1])
                    if myPr0 != '.':
                        while idx1 < len(ref_ps['auth_seq_id']):
                            if ref_ps['comp_id'][idx1] == myPr0:
                                ref_seq_ids.append(ref_ps['auth_seq_id'][idx1])
                                idx1 += 1
                                break
                            idx1 += 1
                    else:
                        ref_seq_ids.append(None)
                    if myPr1 != '.':
                        while idx2 < len(_test_ps_['seq_id']):
                            if _test_ps_['comp_id'][idx2] == myPr1:
                                test_seq_ids.append(_test_ps_['seq_id'][idx2])
                                idx2 += 1
                                break
                            idx2 += 1
                    else:
                        test_seq_ids.append(None)

                offset_in_chain = next((test_seq_id - ref_seq_id for ref_seq_id, test_seq_id
                                        in zip(ref_seq_ids, test_seq_ids)
                                        if ref_seq_id is not None and test_seq_id is not None), None)
                for ref_seq_id, test_seq_id in zip(ref_seq_ids, test_seq_ids):
                    if ref_seq_id is not None:
                        if test_seq_id is not None:
                            offset_in_chain = test_seq_id - ref_seq_id
                            _chainIdMapping[test_seq_id] = {'chain_id': _ref_chain_id,
                                                            'seq_id': ref_seq_id}
                        elif offset_in_chain is not None:
                            test_seq_id = ref_seq_id + offset_in_chain
                            _chainIdMapping[test_seq_id] = {'chain_id': _ref_chain_id,
                                                            'seq_id': ref_seq_id}

                if idx > 0:
                    if ref_chain_id not in _modelChainIdExt:
                        _modelChainIdExt[ref_chain_id] = []
                    _modelChainIdExt[ref_chain_id].append(_ref_chain_id)

                split = True

                offset = end + half_gap

    if not split:
        return None, None, None

    return _polySeqRst, _chainIdMapping, _modelChainIdExt


def retrieveRemappedChainId(chainIdRemap, seqId):
    """ Retrieve chain_id and seq_id from mapping dictionary based on sequence alignments.
    """

    if seqId not in chainIdRemap:
        return None, None

    remap = chainIdRemap[seqId]

    return remap['chain_id'], remap['seq_id']


def retrieveOriginalSeqIdFromMRMap(chainIdRemap, chainId, seqId):
    """ Retrieve the original seq_id from mapping dictionary based on sequence alignments.
    """
    return next((_seqId for _seqId, remap in chainIdRemap.items()
                 if remap['chain_id'] == chainId and remap['seq_id'] == seqId), seqId)


def splitPolySeqRstForNonPoly(ccU, nonPolyModel, polySeqRst, seqAlign, chainAssign):
    """ Split polymer sequence of the current MR file for non-polymer.
    """

    if polySeqRst is None or nonPolyModel is None or seqAlign is None or chainAssign is None:
        return None, None

    comp_ids = set()
    for np in nonPolyModel:
        for ref_comp_id in np['comp_id']:
            comp_ids.add(ref_comp_id)

    if len(comp_ids) == 0:
        return None, None

    alt_ref_comp_id_dict = {}

    for ref_comp_id in comp_ids:
        if not ccU.updateChemCompDict(ref_comp_id):
            continue

        parent_comp_id = ccU.lastChemCompDict.get('_chem_comp.mon_nstd_parent_comp_id', '?')

        if parent_comp_id not in emptyValue:
            alt_ref_comp_id_dict[parent_comp_id] = ref_comp_id

    comp_ids.clear()

    target_comp_ids = []

    for ca in chainAssign:
        if ca['conflict'] == 0 and ca['unmapped'] > 0:
            ref_chain_id = ca['ref_chain_id']
            test_chain_id = ca['test_chain_id']
            test_ps = next((ps for ps in polySeqRst if ps['chain_id'] == test_chain_id), None)
            if test_ps is None or 'auth_comp_id' not in test_ps:
                continue
            sa = next(sa for sa in seqAlign if sa['ref_chain_id'] == ref_chain_id and sa['test_chain_id'] == test_chain_id)

            for test_seq_id, mid_code in zip_longest(sa['test_seq_id'], sa['mid_code']):
                if mid_code in emptyValue:
                    test_comp_id, test_auth_comp_id = next((comp_id, auth_comp_id)
                                                           for seq_id, comp_id, auth_comp_id
                                                           in zip(test_ps['seq_id'], test_ps['comp_id'], test_ps['auth_comp_id'])
                                                           if seq_id == test_seq_id)
                    if getOneLetterCode(test_auth_comp_id) == 'X':
                        _test_auth_comp_id = alt_ref_comp_id_dict.get(test_comp_id, test_auth_comp_id)
                        candidate = []
                        for np in nonPolyModel:
                            _ref_chain_id = np['auth_chain_id']
                            seq_id_name = 'auth_seq_id' if 'auth_seq_id' in np else 'seq_id'

                            if _test_auth_comp_id in np['comp_id']:
                                for ref_seq_id, ref_comp_id in zip(np[seq_id_name], np['comp_id']):
                                    if _test_auth_comp_id == ref_comp_id:
                                        candidate.append({'chain_id': _ref_chain_id, 'seq_id': ref_seq_id})

                        if len(candidate) > 0:
                            comp_ids.add(test_auth_comp_id)
                            target_comp_ids.append({'chain_id': test_chain_id,
                                                    'seq_id': test_seq_id,
                                                    'comp_id': test_auth_comp_id,
                                                    'candidate': candidate
                                                    })

    if len(comp_ids) == 0:
        return None, None

    split = False

    _polySeqRst = copy.copy(polySeqRst)
    _nonPolyMapping = {}

    for comp_id in comp_ids:
        _nonPolyMapping[comp_id] = {}

        targets = [target for target in target_comp_ids if target['comp_id'] == comp_id]

        candidates = []
        for target in targets:
            for candidate in target['candidate']:
                if candidate not in candidates:
                    candidates.append(candidate)
            del target['candidate']

        for target, candidate in zip_longest(targets, candidates):

            if target is None or candidate is None:
                break

            test_chain_id = target['chain_id']
            test_seq_id = target['seq_id']

            test_ps = next(ps for ps in _polySeqRst if ps['chain_id'] == test_chain_id)

            if test_seq_id in test_ps['seq_id']:

                idx = test_ps['seq_id'].index(test_seq_id)

                del test_ps['seq_id'][idx]
                del test_ps['comp_id'][idx]

                _nonPolyMapping[comp_id][test_seq_id] = {'chain_id': candidate['chain_id'],
                                                         'seq_id': candidate['seq_id'],
                                                         'original_chain_id': test_chain_id}

            split = True

    if not split:
        return None, None

    stripPolySeqRst(_polySeqRst)

    return _polySeqRst, _nonPolyMapping


def retrieveRemappedNonPoly(nonPolyRemap, chainId, seqId, compId):
    """ Retrieve seq_id from mapping dictionary based on sequence alignments.
    """

    if compId not in nonPolyRemap or seqId not in nonPolyRemap[compId]:
        return None, None

    remap = nonPolyRemap[compId][seqId]

    if chainId is None or remap['original_chain_id'] == chainId:
        return remap['chain_id'], remap['seq_id']

    return None, None


def splitPolySeqRstForBranched(pA, polySeqModel, branchedModel, polySeqRst, chainAssign):
    """ Split polymer sequence of the current MR file for branched polymer.
    """

    if polySeqRst is None or polySeqModel is None or branchedModel is None or chainAssign is None:
        return None, None

    target_chain_ids = {}
    for ca in chainAssign:
        if ca['conflict'] == 0 and ca['unmapped'] > 0:
            ref_chain_id = ca['ref_chain_id']
            test_chain_id = ca['test_chain_id']

            test_ps = next((ps for ps in polySeqRst if ps['chain_id'] == test_chain_id), None)
            if test_ps is None:
                continue

            for bp in branchedModel:
                b_ref_chain_id = bp['auth_chain_id']

                pA.setReferenceSequence(bp['comp_id'], 'REF' + b_ref_chain_id)
                pA.addTestSequence(test_ps['comp_id'], b_ref_chain_id)
                pA.doAlign()

                myAlign = pA.getAlignment(b_ref_chain_id)

                length = len(myAlign)

                if length == 0:
                    continue

                matched, _, conflict, _, _ = getScoreOfSeqAlign(myAlign)

                if matched == 0 or conflict > 0:
                    continue

                if test_chain_id not in target_chain_ids:
                    target_chain_ids[test_chain_id] = []
                target_chain_ids[test_chain_id].append((ref_chain_id, b_ref_chain_id))

    if len(target_chain_ids) == 0:
        return None, None

    split = False

    _polySeqRst = copy.copy(polySeqRst)
    _branchedMapping = {}

    for test_chain_id, ref_chain_ids in target_chain_ids.items():

        if len(ref_chain_ids) == 0:
            continue

        test_ps = next(ps for ps in _polySeqRst if ps['chain_id'] == test_chain_id)
        _test_ps = copy.copy(test_ps)

        _split = False

        p = 0
        b_p = 0

        _ref_chain_ids = []
        for ref_chain_id in ref_chain_ids:
            if ref_chain_id[0] not in _ref_chain_ids:
                _ref_chain_ids.append(ref_chain_id[0])

        _b_ref_chain_ids = []
        for ref_chain_id in ref_chain_ids:
            if ref_chain_id[1] not in _ref_chain_ids:
                _b_ref_chain_ids.append(ref_chain_id[1])

        while True:

            ref_chain_id = _ref_chain_ids[p] if p < len(_ref_chain_ids) else None
            myAlign = None
            length = matched = conflict = 0

            if ref_chain_id is not None:

                ref_ps = next(ps for ps in polySeqModel if ps['auth_chain_id'] == ref_chain_id)

                pA.setReferenceSequence(ref_ps['comp_id'], 'REF' + ref_chain_id)
                pA.addTestSequence(_test_ps['comp_id'], ref_chain_id)
                pA.doAlign()

                myAlign = pA.getAlignment(ref_chain_id)

                length = len(myAlign)

                if length > 0:
                    matched, _, conflict, _, _ = getScoreOfSeqAlign(myAlign)

            b_ref_chain_id = _b_ref_chain_ids[b_p]if b_p < len(_b_ref_chain_ids) else None
            myAlignB = None
            b_length = b_matched = b_conflict = 0

            if b_ref_chain_id is not None:

                ref_bp = next(bp for bp in branchedModel if bp['auth_chain_id'] == b_ref_chain_id)

                pA.setReferenceSequence(ref_bp['comp_id'], 'REF' + b_ref_chain_id)
                pA.addTestSequence(_test_ps['comp_id'], b_ref_chain_id)
                pA.doAlign()

                myAlignB = pA.getAlignment(b_ref_chain_id)

                b_length = len(myAlignB)

                if b_length > 0:
                    b_matched, _, b_conflict, _, _ = getScoreOfSeqAlign(myAlignB)

            if length + b_length == 0 or matched + b_matched == 0 or conflict > 0 or b_conflict > 0:
                break

            if not _split:
                _polySeqRst.remove(test_ps)
                _split = True

            ref_seq_ids = []
            test_seq_ids = []
            idx1 = 0
            idx2 = 0

            b_ref_seq_ids = []
            b_test_seq_ids = []
            b_idx1 = 0
            b_idx2 = 0

            if matched > 0:

                for i in range(length):
                    myPr = myAlign[i]
                    myPr0 = str(myPr[0])
                    myPr1 = str(myPr[1])
                    if myPr0 != '.':
                        while idx1 < len(ref_ps['auth_seq_id']):
                            if ref_ps['comp_id'][idx1] == myPr0:
                                ref_seq_ids.append(ref_ps['auth_seq_id'][idx1])
                                idx1 += 1
                                break
                            idx1 += 1
                    else:
                        ref_seq_ids.append(None)
                    if myPr1 != '.':
                        while idx2 < len(_test_ps['seq_id']):
                            if _test_ps['comp_id'][idx2] == myPr1:
                                test_seq_ids.append(_test_ps['seq_id'][idx2])
                                idx2 += 1
                                break
                            idx2 += 1
                    else:
                        test_seq_ids.append(None)

            if b_matched > 0:

                for i in range(b_length):
                    myPr = myAlignB[i]
                    myPr0 = str(myPr[0])
                    myPr1 = str(myPr[1])
                    if myPr0 != '.':
                        while b_idx1 < len(ref_bp['auth_seq_id']):
                            if ref_bp['comp_id'][b_idx1] == myPr0:
                                b_ref_seq_ids.append(ref_bp['seq_id'][b_idx1])
                                b_idx1 += 1
                                break
                            b_idx1 += 1
                    else:
                        b_ref_seq_ids.append(None)
                    if myPr1 != '.':
                        while b_idx2 < len(_test_ps['seq_id']):
                            if _test_ps['comp_id'][b_idx2] == myPr1:
                                b_test_seq_ids.append(_test_ps['seq_id'][b_idx2])
                                b_idx2 += 1
                                break
                            b_idx2 += 1
                    else:
                        b_test_seq_ids.append(None)

            if matched > 0 and b_matched > 0:

                if idx2 < b_idx2:

                    first_seq_id = next(test_seq_id for test_seq_id in test_seq_ids if test_seq_id is not None)
                    last_seq_id = next(test_seq_id for test_seq_id in reversed(test_seq_ids) if test_seq_id is not None)

                    beg = _test_ps['seq_id'].index(first_seq_id)
                    end = _test_ps['seq_id'].index(last_seq_id)

                    _test_ps_ = {'chain_id': ref_chain_id,
                                 'seq_id': _test_ps['seq_id'][beg:end],
                                 'comp_id': _test_ps['comp_id'][beg:end]}

                    _polySeqRst.append(_test_ps_)

                    _test_ps['seq_id'] = _test_ps['seq_id'][end:]
                    _test_ps['comp_id'] = _test_ps['comp_id'][end:]

                    p += 1

                else:

                    last_seq_id = next(test_seq_id for test_seq_id in reversed(b_test_seq_ids) if test_seq_id is not None)

                    end = _test_ps['seq_id'].index(last_seq_id)

                    offset_in_chain = next((test_seq_id - ref_seq_id for ref_seq_id, test_seq_id
                                            in zip(b_ref_seq_ids, b_test_seq_ids)
                                            if ref_seq_id is not None and test_seq_id is not None), None)

                    for ref_seq_id, test_seq_id in zip(b_ref_seq_ids, b_test_seq_ids):
                        if ref_seq_id is not None:
                            if test_seq_id is not None:
                                offset_in_chain = test_seq_id - ref_seq_id
                                _branchedMapping[test_seq_id] = {'chain_id': b_ref_chain_id,
                                                                 'seq_id': ref_seq_id}
                            elif offset_in_chain is not None:
                                test_seq_id = ref_seq_id + offset_in_chain
                                _branchedMapping[test_seq_id] = {'chain_id': b_ref_chain_id,
                                                                 'seq_id': ref_seq_id}

                    _test_ps['seq_id'] = _test_ps['seq_id'][end:]
                    _test_ps['comp_id'] = _test_ps['comp_id'][end:]

                    b_p += 1

            elif matched > 0:

                first_seq_id = next(test_seq_id for test_seq_id in test_seq_ids if test_seq_id is not None)
                last_seq_id = next(test_seq_id for test_seq_id in reversed(test_seq_ids) if test_seq_id is not None)

                beg = _test_ps['seq_id'].index(first_seq_id)
                end = _test_ps['seq_id'].index(last_seq_id)

                _test_ps_ = {'chain_id': ref_chain_id,
                             'seq_id': _test_ps['seq_id'][beg:end],
                             'comp_id': _test_ps['comp_id'][beg:end]}

                _polySeqRst.append(_test_ps_)

                _test_ps['seq_id'] = _test_ps['seq_id'][end:]
                _test_ps['comp_id'] = _test_ps['comp_id'][end:]

                p += 1

            else:

                last_seq_id = next(test_seq_id for test_seq_id in reversed(b_test_seq_ids) if test_seq_id is not None)

                end = _test_ps['seq_id'].index(last_seq_id)

                for ref_seq_id, test_seq_id in zip(b_ref_seq_ids, b_test_seq_ids):
                    if ref_seq_id is not None:
                        if test_seq_id is not None:
                            offset_in_chain = test_seq_id - ref_seq_id
                            _branchedMapping[test_seq_id] = {'chain_id': b_ref_chain_id,
                                                             'seq_id': ref_seq_id}
                        elif offset_in_chain is not None:
                            test_seq_id = ref_seq_id + offset_in_chain
                            _branchedMapping[test_seq_id] = {'chain_id': b_ref_chain_id,
                                                             'seq_id': ref_seq_id}

                _test_ps['seq_id'] = _test_ps['seq_id'][end:]
                _test_ps['comp_id'] = _test_ps['comp_id'][end:]

                b_p += 1

            split = True

    if not split:
        return None, None

    return _polySeqRst, _branchedMapping


def getPrettyJson(data):
    """ Return pretty JSON string.
    """

    def getPrettyChunk(chunk):

        # string
        chunk_ = re.sub(r'",\s+', '", ', chunk)
        # number
        chunk__ = re.sub(r'(\d),\s+', r'\1, ', chunk_)
        # null, true, false
        chunk___ = re.sub(r'(null|true|false),\s+', r'\1, ', chunk__)

        return re.sub(r'(\s+)\[\s+([\S ]+)\s+\](,?)\n', r'\1[\2]\3\n', chunk___)

    lines = json.dumps(data, indent=2).split('\n')

    is_tag = []
    chunk = []

    with io.StringIO() as f:

        for line in lines:

            if '": ' in line:

                if f.tell() > 0:
                    is_tag.append(False)
                    chunk.append(f.getvalue())

                    f.truncate(0)
                    f.seek(0)

                is_tag.append(True)
                chunk.append(line)

            else:
                f.write(line + '\n')

        if f.tell() > 0:
            is_tag.append(False)
            chunk.append(f.getvalue())

            f.truncate(0)
            f.seek(0)

        for _is_tag, _chunk in zip(is_tag, chunk):
            f.write((_chunk + '\n') if _is_tag else getPrettyChunk(_chunk))

        return f.getvalue()
