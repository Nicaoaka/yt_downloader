__all__ = [
    'merge_v_infos', 'merge_pl_infos', 'Updater',
]

from collections import defaultdict
from typing import Any, Callable

from ..yt_types import *
from .. import utils
from .. import yt_utils


class NO_VALUE:
    def __bool__(self):
        return False

class Updater:
    """
    Callable[[Merged_V_InfoDict, key, value, is_latest], did_update]

    Make changes to `info` in-place. Return True if it was an `update`-worthy change.
    """

    @staticmethod
    def latest(info: V_InfoDict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
        if is_latest and v != NO_VALUE:
            info[k] = v
            return True
        return False

    @staticmethod
    def latest_not_None(info: V_InfoDict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
        if v is None:
            return False
        return Updater.latest(info, k, v, is_latest)

    @staticmethod
    def latest_only(info: V_InfoDict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
        if not is_latest:
            return False
        if v == NO_VALUE:
            info.pop(k)
        else:
            info[k] = v
        return True
    
    @staticmethod
    def _unsafe_maximizer(info: V_InfoDict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
        if v is None or v == NO_VALUE:
            return False
        if (v or 0) > (info.get(k) or 0): # type: ignore - values may not define __gt__
            info[k] = v
            return True
        return False

    @staticmethod
    def maximizer(info: V_InfoDict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
        try:
            return Updater._unsafe_maximizer(info, k, v, is_latest)
        except Exception: # not sure what errors may appear
            return Updater.fill_empty(info, k, v, is_latest)

    @staticmethod
    def fill_empty(info: V_InfoDict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
        if v is None or v == NO_VALUE:
            return False
        if is_latest or (k not in info or info[k] is None):
            info[k] = v
            return True
        return False

    @staticmethod
    def latest_not_none_and_latest_unavail(info: V_InfoDict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
        if info.get(k, NO_VALUE) == v:
            return False
        
        match k:
            case 'yt_unavailable_msg' | 'wa_unavailable_msg':
                return Updater.latest_only(info, k, v, is_latest)
            case _:
                return Updater.latest_not_None(info, k, v, is_latest)



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
            epoch = yt_utils.to_readable_epoch(yt_utils.get_epoch(v_info))
            timeline[epoch]['better_info'] = f'{merge_level.name} -> {level.name}'
            merge_level = level
    return timeline

def _get_unavailabe_timeline(unavail_msgs: list[UnavailableMsg]) -> V_MergeTimeline:
    timeline: V_MergeTimeline = defaultdict(dict) # type: ignore - init
    for msg in unavail_msgs:
        epoch = yt_utils.to_readable_epoch(msg['epoch'] or 0)
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
        field_updater: Callable[[V_InfoDict, str, Any|type[NO_VALUE], bool], bool],
        update_filter: Callable[[str], bool] = lambda _: True,
        _init: V_InfoDict|None = None,
    ) -> tuple[V_InfoDict, V_MergeTimeline]:
    """
    Does not copy v_info objects. Some input object references will be the same in the output!
    Args:
        v_infos: list of a single video id's info dicts. (Raise ValueError if not)
        field_updater (Callable[[Merged_V_InfoDict, key, value, is_latest], did_update]):
            Specify the policy for how fields should be
            updated (see `Updater` for examples). Defaults to updating keys
            to latest non-None values, with unavailable messages always
            reflecting the latest info.
        update_filter (Callable[[str], bool]): Choose what keys should be added to `updates` in the video's
            merge timeline. Defaults to no filtering.
        _init (V_InfoDict|None): Initial v_info. Can be in `v_infos`. Defaults to None.
    """

    ids = {info['id'] for info in v_infos}
    if _init is not None:
        ids.add(_init['id'])
    if len(ids) != 1 or ids == {None}: # don't allow None
        raise ValueError(f"Multiple ids found: {ids}")
    
    skip = [i for i, x in enumerate(v_infos) if x is _init]

    if not v_infos and _init is None:
        raise ValueError("Provide at least 1 v_info")
    if not v_infos:
        return _init, {} # type: ignore - ok

    v_infos = sorted(v_infos, key=yt_utils.get_epoch, reverse=True)
    _init_level = yt_utils.get_v_info_level(_init)
    merge_info: V_InfoDict = _init or {} # type: ignore - init
    updates = defaultdict(dict)
    for i, v_info in enumerate(v_infos):
        if i in skip:
            continue
        is_latest = v_info is v_infos[0] and (yt_utils.get_epoch(v_info) >= yt_utils.get_epoch(merge_info))
        for k in v_info.keys() | merge_info.keys():
            if field_updater(merge_info, k, v_info.get(k, NO_VALUE), is_latest):
                epoch = yt_utils.to_readable_epoch(yt_utils.get_epoch(v_info))
                if update_filter(k):
                    updates[epoch].setdefault('updates', set()).add(k)
    
    new_unavail_msgs = _get_unavailable_msgs(v_infos)
    merge_info['unavailable_msgs'] = _dedup_and_sort_unavail_msgs(merge_info.get('unavailable_msgs', []) + new_unavail_msgs)
    timeline = _get_v_timeline(v_infos, _init_level, merge_info['unavailable_msgs'])
    timeline = utils.dict_merge(timeline, updates)
    return merge_info, timeline

type V_Path = tuple[int, int]
def merge_pl_infos(
        pl_infos: list[PL_InfoDict],
        field_updater: Callable[[V_InfoDict, str, Any|type[NO_VALUE], bool], bool],
        update_filter: Callable[[str], bool] = lambda _: True,
        _init: PL_InfoDict|None = None,
) -> PL_InfoDict:
    """
    Args:
        pl_infos (list[PL_InfoDict]): The source pl_infos. List input order does not matter becaduse sorting is done at the start.
            All pl_infos should have the same playlist id.
        field_updater (Callable[[Merged_V_InfoDict, key, value, is_latest], did_update]):
            Specify the policy for how fields should be updated (see `Updater` for examples).
        update_filter (Callable[[str], bool]): Returns True to add key to timeline, False to omit.
            Used by ``merge_v_infos()``. Defaults showing all.
        _init (PL_InfoDict|None): Initial merge info. Its timeline will be preserved.

    Returns:
        PL_InfoDict: The merged playlist info
    
    Playlist video ordering:
    - Assumes newer pl_info is more accurate.
    - Newer orderings always have priority over old orderings. (In conflict, older is placed after new)

    Updates the following to represent the combined version
    - playlist_count (int):
    - entries (list[PL_V_InfoDict]):
    - merge_timeline (dict[V_ID, V_MergeInfo]): Preserves _init's and adds current merge operation's timeline.
    """
    pl_infos = sorted(pl_infos, key=yt_utils.get_epoch, reverse=True)
    if _init and _init not in pl_infos:
        pl_infos.append(_init)
    if len(pl_infos) == 0:
        raise ValueError("Provide at least 1")
    if len({pl_info['id'] for pl_info in pl_infos}) > 1:
        raise ValueError(f"More than one playlist id found: { {pl_info['id'] for pl_info in pl_infos} }")

    # most recent pl_info has highest priority
    _init_pl_idx: int|None = None if not _init else pl_infos.index(_init)
    V_ID_ORDER = utils.merge_ordered_lists([[entry['id'] for entry in pl_info['entries']] for pl_info in pl_infos])

    merge_info: PL_InfoDict = utils.dict_without_keys(pl_infos[0], {'entries', 'merge_timeline'}) # type: ignore - init
    merge_info['playlist_count'] = len(V_ID_ORDER)
    

    id_map = {v_id: i for i, v_id in enumerate(V_ID_ORDER)}
    v_id_to_paths: list[list[V_Path]] = [list() for _ in range(merge_info['playlist_count'])]
    for i, _pl in enumerate(pl_infos):
        for j, _v in enumerate(_pl['entries']):
            v_id_to_paths[id_map[_v['id']]].append( (i, j) )

    entries: list[PL_V_InfoDict] = [dict() for _ in range(len(V_ID_ORDER))] # type: ignore - init
    pl_timeline: PL_MergeTimeline = {} if _init_pl_idx is None else pl_infos[_init_pl_idx].get('merge_timeline', {})
    for i, v_paths in enumerate(v_id_to_paths):
        merge_entry, v_timeline = merge_v_infos(
            v_infos       = [pl_infos[pl]['entries'][v] for pl, v in v_paths if pl != _init_pl_idx],
            update_filter = update_filter,
            field_updater = field_updater,
            _init         = next((pl_infos[pl]['entries'][v] for pl, v in v_paths if pl == _init_pl_idx), None))
        
        entries[i] = merge_entry # type: ignore - __pl_v_info is correctly overwritten/set before returning
        if v_timeline:
            pl_timeline.setdefault(merge_entry['id'], {})
            pl_timeline[merge_entry['id']] = utils.dict_merge(pl_timeline[merge_entry['id']], v_timeline)
    
    merge_info['entries'] = entries
    yt_utils.add_pl_info_to_entries(merge_info)
    
    merge_info['merge_timeline'] = pl_timeline
    return merge_info
