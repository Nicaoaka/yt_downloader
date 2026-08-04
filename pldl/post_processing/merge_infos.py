__all__ = [
    'merge_v_infos', 'merge_pl_infos',
]

from collections import defaultdict
from typing import Any, Callable

from pldl.pldl_types import *
from pldl.utils import utils, merge_ordered_lists
from pldl import yt_utils

    
def _dedup_and_sort_unavail_msgs(msgs: list[UnavailableMsg]):
    return sorted(
        # Use tuple() to focus on the values themselves instead of the dict_value object
        utils.dedup(msgs, hash=lambda x: tuple(x.values())),
        key=lambda info: (info['epoch'] or 0) \
                        +(0.2 if info['type'] == 'yt' else 0.1 if info['type'] == 'wa' else 0),
        reverse=True)

def _get_unavailabe_timeline(unavail_msgs: list[UnavailableMsg]) -> V_MergeTimeline:
    timeline: V_MergeTimeline = defaultdict(dict) # type: ignore - init
    for msg in unavail_msgs:
        epoch = yt_utils.to_readable_epoch(msg['epoch'] if msg['epoch'] is not None else yt_utils.DEFAULT_EPOCH())
        timeline[epoch].setdefault('unavailable', []).append(f"{msg['type']}: {msg['msg']}")
    return timeline

def merge_v_infos(
        v_infos: list[V_InfoDict],
        field_updater: Callable[[V_InfoDict, str, Any|type[NO_VALUE], bool], bool],
        update_filter: Callable[[str], bool],
        _init: V_InfoDict|None = None,
    ) -> tuple[V_InfoDict, V_MergeTimeline]:
    """
    Does not copy v_info objects. Some input object references will be the same in the output!

    `info_level` and `unavailable_msgs` will be updated without concern for callbacks.

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
    
    if not v_infos and _init is None:
        raise ValueError("Provide at least 1 v_info")
    if not v_infos:
        return _init, {} # type: ignore - ok

    v_infos = sorted(v_infos, key=yt_utils.get_epoch) # oldest to newest
    merge_info: V_InfoDict = _init or {} # type: ignore - init

    curr_info_level = yt_utils.get_v_info_level(merge_info)
    unavailable_msgs = merge_info.get('unavailable_msgs', [])

    v_timeline: V_MergeTimeline = {}
    for v_info in v_infos:
        if v_info is _init:
            continue

        # setup
        epoch = yt_utils.to_readable_epoch(yt_utils.get_epoch(v_info))
        if epoch not in v_timeline:
            v_timeline[epoch] = {}
        _timeline = v_timeline[epoch]
        
        # updating v_info
        is_latest = v_info is v_infos[-1] \
            and (yt_utils.get_epoch(v_info) >= (yt_utils.get_epoch(_init) if _init else -float('inf')))
        for k in v_info.keys() | merge_info.keys():
            v = v_info.get(k, NO_VALUE)
            report_update = field_updater(merge_info, k, v, is_latest)
            if report_update and update_filter(k):
                if not 'updates' in _timeline:
                    _timeline['updates'] = list()
                if k not in _timeline['updates']:
                    _timeline['updates'].append(f'{k!r} -> {utils.truncate(repr(v), 750, end='... (see info dict)')}')

        # better_info
        new_info_level = yt_utils.get_v_info_level(v_info)
        if curr_info_level < new_info_level:
            merge_info['info_level'] = new_info_level.name
            if 'better_info' not in _timeline:
                _timeline['better_info'] = []
            _timeline['better_info'].append(f'{curr_info_level.name} -> {new_info_level.name}')
            curr_info_level = new_info_level

        # unavailable_msgs
        unavailable_msgs.extend(v_info.get('unavailable_msgs', []))
        for k in ('yt_unavailable_msg', 'wa_unavailable_msg', ):
            if k not in v_info:
                continue
            unavailable_msgs.append({
                'epoch': v_info.get('epoch'), # None is more expressive
                'msg': v_info.get(k),
                'type': k.removesuffix('_unavailable_msg'),
            })

    if unavailable_msgs:
        merge_info['unavailable_msgs'] = _dedup_and_sort_unavail_msgs(unavailable_msgs)
        v_timeline = utils.merge_objs(v_timeline, _get_unavailabe_timeline(merge_info['unavailable_msgs']), make_copy=False)
    return merge_info, v_timeline



def _get_v_paths(pl_v_ids, pl_infos):
    id_map = {v_id: i for i, v_id in enumerate(pl_v_ids)}
    v_id_to_paths: list[list[V_Path]] = [list() for _ in range(len(pl_v_ids))]
    for i, _pl in enumerate(pl_infos):
        for j, _v in enumerate(_pl['entries']):
            v_id_to_paths[id_map[_v['id']]].append( (i, j) )
    return v_id_to_paths

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
    pl_infos = sorted(pl_infos, key=yt_utils.get_epoch)
    if _init and _init not in pl_infos:
        pl_infos.append(_init)
    pl_infos = utils.dedup(pl_infos, id)

    if non_init_merge_infos := list(filter(
        lambda pl_info: pl_info is not _init and yt_utils.get_pl_info_level(pl_info) == yt_utils.PL_InfoLevel.MERGE, 
        pl_infos)):
        utils.WARNING(f"{len(non_init_merge_infos)} pl_info merge_timeline's will be omitted from merge_info.")
        utils.json_dump(yt_utils.copy_and_sanitize_info(non_init_merge_infos), 'bad_infos.json')
    
    if len(pl_infos) == 0:
        raise ValueError("Provide at least 1")
    if len({pl_info['id'] for pl_info in pl_infos}) > 1:
        raise ValueError(f"More than one playlist id found: { {pl_info['id'] for pl_info in pl_infos} }")

    # most recent pl_info has highest priority
    _init_pl_idx: int|None = None if not _init else pl_infos.index(_init)
    V_ID_ORDER = merge_ordered_lists([[entry['id'] for entry in pl_info['entries']] for pl_info in pl_infos])

    merge_info: PL_InfoDict = utils.dict_without_keys(pl_infos[-1], {'entries', 'merge_timeline'}) # type: ignore - init
    v_id_to_paths = _get_v_paths(V_ID_ORDER, pl_infos)

    entries: list[V_InfoDict] = [{'id': id} for id in range(len(V_ID_ORDER))] # type: ignore - correct type
    pl_timeline: PL_MergeTimeline = {} if _init_pl_idx is None else pl_infos[_init_pl_idx].get('merge_timeline', {})
    for i, v_paths in enumerate(v_id_to_paths):
        merge_entry, v_timeline = merge_v_infos(
            v_infos       = [pl_infos[pl]['entries'][v] for pl, v in v_paths if pl != _init_pl_idx],
            field_updater = field_updater,
            update_filter = update_filter,
            _init         = next((pl_infos[pl]['entries'][v] for pl, v in v_paths if pl == _init_pl_idx), None))
        
        entries[i] = merge_entry # type: ignore - __pl_v_info is correctly overwritten/set before returning
        if v_timeline:
            pl_timeline.setdefault(merge_entry['id'], {})
            pl_timeline[merge_entry['id']] = utils.merge_objs(pl_timeline[merge_entry['id']], v_timeline, make_copy=False)
    
    merge_info['entries'] = entries
    yt_utils.fixup_pl_info(merge_info)
    
    merge_info['merge_timeline'] = pl_timeline
    return merge_info
