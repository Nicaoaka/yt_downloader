import enum
from collections import defaultdict
from typing import Any

from pp_utils import add_pl_info_to_entries, NO_EPOCH
from merger import merge_ordered_lists
from yt_types import *
import utils
import yt_utils

import display


# Merging info

class MergeStrategies(enum.Enum):
    LATEST       = enum.auto()
    MAX          = enum.auto()
    LATEST_OR_FILL_NONE = enum.auto()

FIELD_STRATEGIES: dict[str, MergeStrategies] = {
    'yt_unavailable_msg': MergeStrategies.LATEST,
    'wa_unavailable_msg': MergeStrategies.LATEST,
    'view_count':         MergeStrategies.MAX,
}
assert all(k in V_InfoDict.__required_keys__ | V_InfoDict.__optional_keys__ for k in FIELD_STRATEGIES.keys())

class NO_DEFAULT:
    def __bool__(self):
        return False

def _apply_field(info: V_InfoDict, k: str, v: Any|type[NO_DEFAULT], is_latest: bool) -> bool:
    """ in-place on `info`, returns if a change occurred """
    # skip if they are the same. Nothing to update
    if info.get(k, NO_DEFAULT) == v:
        return False
    
    match FIELD_STRATEGIES.get(k, MergeStrategies.LATEST_OR_FILL_NONE):
        case MergeStrategies.LATEST:
            if is_latest:
                if v == NO_DEFAULT:
                    info.pop(k)
                else:
                    info[k] = v
                return True
            
        case MergeStrategies.MAX:
            try:
                if v is None or v == NO_DEFAULT:
                    return False
                if (v or 0) > (info.get(k) or 0): # type: ignore - v may not support __gt__ 
                    info[k] = v
                    return True
            except Exception as e:
                print(display.exc(e) + "\n\nCheck for malformed `MergeStrategies.MAX` in `FIELD_STRATEGIES`")
        
        case MergeStrategies.LATEST_OR_FILL_NONE:
            if v is None or v == NO_DEFAULT:
                return False
            if is_latest or k not in info or info[k] is None:
                info[k] = v
                return True
    return False

def _get_unavailable_msgs(v_infos: list[V_InfoDict]) -> list[UnavailableMsg]:
    res: list[UnavailableMsg] = []
    for v_info in v_infos:
        if not v_info:
            continue
        for k in ('yt_unavailable_msg', 'wa_unavailable_msg'):
            if k not in v_info:
                continue
            res.append({
                'epoch': v_info.get('epoch'), # None is more expressive
                'msg': v_info.get(k),
                'type': k.removesuffix('_unavailable_msg')
            })
        res.extend(v_info.get('unavailable_msgs', []))
    return _dedup_and_sort_unavail_msgs(res)

def _dedup_and_sort_unavail_msgs(msgs: list[UnavailableMsg]):
    return sorted(
        utils.dedup(msgs, hash=lambda x: str(x['epoch']) + str(x['type'])),
        key=lambda um: (um['epoch'] or 0) + (0.5 if um['type'] == 'yt' else 0),
        reverse=True)


def _get_info_level_timeline(v_infos: list[V_InfoDict], merge_level: _V_InfoLevel) -> V_MergeTimeline:
    """
    Returns V_MergeTimeline relative to _init.
        such that: `full v timeline = {..., **return}`

    Note: If better info is found by going back in time,
    it is possible that the output will go forward and backwards in time.
    This is okay because info levels have a defined order
    and there will not be duplicate transitions.
    """
    timeline: V_MergeTimeline = defaultdict(dict) # type: ignore - init
    for v_info in v_infos:
        level = yt_utils.get_v_info_level(v_info)
        if level > merge_level:
            epoch = utils.to_readable_epoch(v_info.get('epoch', NO_EPOCH))
            timeline[epoch]['better_info'] = f'{merge_level.name} -> {level.name}'
            merge_level = level
    return timeline

def _get_unavailabe_timeline(unavail_msgs: list[UnavailableMsg]) -> V_MergeTimeline:
    timeline: V_MergeTimeline = defaultdict(dict) # type: ignore - init
    for msg in unavail_msgs:
        epoch = utils.to_readable_epoch(msg['epoch'] or 0)
        timeline[epoch].setdefault('unavailable', []).append(f"{msg['type']}: {msg['msg']}")
    return timeline

def _get_v_timeline(
        v_infos: list[V_InfoDict],
        merge_level: _V_InfoLevel,
        unavail_msgs: list[UnavailableMsg],
) -> V_MergeTimeline:
    return utils.dict_merge(
        _get_info_level_timeline(v_infos, merge_level),
        _get_unavailabe_timeline(unavail_msgs)
    )


def merge_v_infos(
        v_infos: list[V_InfoDict],
        _init: V_InfoDict|None = None,
    ) -> tuple[V_InfoDict, V_MergeTimeline]:
    """ Will ignore __PL_V_InfoDict information.

        Prefer the newest, add any new info.
        - Replace `None` and absent values with previous info
            - May lead to impossible yt_dlp info_dict state - this limitation is ok
        - Add `unavailable_msgs` for past 
        - `yt_unavailable_msg` and `wa_unavailable_msg`

        `_init` should not be in `v_infos` to prevent duplicate unavailable messages

        Does not copy v_info objects. Some input object references will be the same in the output! """
    if not v_infos and _init is None:
        raise ValueError("Provide at least 1 v_info")
    if not v_infos:
        return _init, {} # type: ignore - ok
    
    v_infos = sorted(v_infos, key=lambda info: info.get('epoch', NO_EPOCH), reverse=True)
    _init_level = yt_utils.get_v_info_level(_init)
    merge_info: V_InfoDict = _init or {} # type: ignore - init
    updates = defaultdict(dict)
    for v_info in v_infos:
        is_latest = v_info is v_infos[0] and (v_info.get('epoch', NO_EPOCH) >= merge_info.get('epoch', NO_EPOCH))
        for k in v_info.keys() | merge_info.keys():
            if _apply_field(merge_info, k, v_info.get(k, NO_DEFAULT), is_latest):
                epoch = utils.to_readable_epoch(v_info.get('epoch', NO_EPOCH))
                updates[epoch].setdefault('updates', set()).add(k)
    
    new_unavail_msgs = _get_unavailable_msgs(v_infos)
    merge_info['unavailable_msgs'] = _dedup_and_sort_unavail_msgs(merge_info.get('unavailable_msgs', []) + new_unavail_msgs)
    timeline = _get_v_timeline(v_infos, _init_level, merge_info['unavailable_msgs'])
    timeline = utils.dict_merge(timeline, updates)
    return merge_info, timeline


def merge_pl_infos(pl_infos: list[PL_InfoDict]) -> PL_InfoDict:
    """
    Returns a pl_info dict with the newest and most info based on the past in pl_infos.
    
    Assumes newer pl_info is more accurate.
    Newer orderings always have priority over old orderings. (In conflict, older is placed after new)
    Merges videoes using ``merge_v_infos()``

    Updates the following to represent the combined version
    - playlist_count
    - entries
    - merge_timeline (dict[V_ID, V_MergeInfo]): What changed and from when.
        - (Limitation) Can only store the current and one of the pl_infos meta. Storing more than one is exponential and complex.

    Args:
        pl_infos (list[PL_InfoDict]): The source pl_infos. List order does not matter becaduse sorting is done at the start. Should all be the same playlist.

    Returns:
        PL_InfoDict: The merged playlist info
    """

    if len(pl_infos) == 0:
        raise ValueError("Provide at least 1")
    if len({pl_info['id'] for pl_info in pl_infos}) > 1:
        raise ValueError(f"More than one playlist id found: { {pl_info['id'] for pl_info in pl_infos} }")

    # most recent pl_info has highest priority
    pl_infos = sorted(pl_infos, key=lambda info: info.get('epoch', NO_EPOCH), reverse=True)
    V_ID_ORDER = merge_ordered_lists([[entry['id'] for entry in pl_info['entries']] for pl_info in pl_infos])

    merge_info: PL_InfoDict = utils.dict_without_keys(pl_infos[0], {'entries', 'merge_timeline'}) # type: ignore - init
    merge_info['playlist_count'] = len(V_ID_ORDER)
    
    past_merge_pl_idx: int|None = None
    for i, pl_info in enumerate(pl_infos):
        if yt_utils.get_pl_info_level(pl_info) == _PL_InfoLevel.MERGED:
            if past_merge_pl_idx is not None:
                utils.WARNING(f"Found more than 1 merge info. Will only include current operation")
                past_merge_pl_idx = None
                break
            past_merge_pl_idx = i

    id_map = {v_id: i for i, v_id in enumerate(V_ID_ORDER)}
    path_lists = [list() for _ in range(merge_info['playlist_count'])]
    for i, _pl in enumerate(pl_infos):
        for j, _v in enumerate(_pl['entries']):
            path_lists[id_map[_v['id']]].append( (i, j) )

    entries: list[PL_V_InfoDict] = [dict() for _ in range(len(V_ID_ORDER))] # type: ignore - init
    pl_timeline: PL_MergeTimeline = {} if past_merge_pl_idx is None else pl_infos[past_merge_pl_idx].get('merge_timeline', {})
    for i, pl_v_list in enumerate(path_lists):
        
        past_merge_pl_v = None
        for pl_v in pl_v_list:
            if pl_v[0] == past_merge_pl_idx:
                past_merge_pl_v = pl_v
                break
        entry, v_timeline = merge_v_infos(
            [pl_infos[pl]['entries'][v] for pl, v in pl_v_list if (past_merge_pl_v is None or pl != past_merge_pl_v[0])],
            _init=pl_infos[past_merge_pl_v[0]]['entries'][past_merge_pl_v[1]] if past_merge_pl_v is not None else None)
        entries[i] = entry # type: ignore - __pl_v_info is correctly overwritten/set before returning
        if v_timeline:
            pl_timeline.setdefault(entry['id'], {})
            pl_timeline[entry['id']] = utils.dict_merge(pl_timeline[entry['id']], v_timeline)
    
    merge_info['entries'] = entries
    add_pl_info_to_entries(merge_info)
    
    merge_info['merge_timeline'] = pl_timeline
    return merge_info
