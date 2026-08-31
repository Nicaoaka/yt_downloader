__all__ = [
    'merge_pl_infos',
    'merge_v_infos',
]

from collections import defaultdict
from collections.abc import Callable
from typing import Any

from pldl import yt_utils
from pldl.pldl_types import *
from pldl.utils import merge_ordered_lists, utils


def _dedup_and_sort_unavail_msgs(msgs: list[UnavailableMsg]):
    return sorted(
        # Use tuple() to focus on the values themselves instead of the dict_value object
        utils.dedup(msgs, hash=lambda x: (x['epoch'], x['msg'], x['type'])),
        key=lambda info: (info['epoch'] or 0) \
                        +(0.2 if info['type'] == 'yt' else
                          0.1 if info['type'] == 'wa' else
                          0),
        reverse=True)

def _merge_v_infos(
        v_infos: list[V_InfoDict],
        field_updater: Callable[[V_InfoDict, str, Any|type[NO_VALUE], bool], bool],
        update_filter: Callable[[str], bool],
        _init_v_info: V_InfoDict,
        _init_v_timeline: V_MergeTimeline,
) -> tuple[V_InfoDict, V_MergeTimeline]:

    merge_info: V_InfoDict = yt_utils.copy_and_sanitize_info(_init_v_info)
    v_timeline: V_MergeTimeline = yt_utils.copy_and_sanitize_info(_init_v_timeline)

    if merge_info and not v_infos:
        return merge_info, v_timeline

    # latest_epochs need to be stored on a key by key basis because
    # lower info_level lists (usu flat) can have a higher epoch than
    # higher info_level lists (usu download) while being seen first
    latest_epochs: defaultdict[str, float] = defaultdict(lambda: float('-inf'))

    # special keys
    merge_info_level = yt_utils.derive_v_info_level(merge_info)
    unavailable_msgs: list[UnavailableMsg] = []

    for v_info in yt_utils.copy_and_sanitize_info(v_infos):
        unavailable_msgs.extend(v_info.get('unavailable_msgs', []))
        
        curr_epoch = yt_utils.get_epoch(v_info)
        entry_key = yt_utils.to_readable_epoch(curr_epoch)
        timeline_entry: V_MergeTimelineEntry = v_timeline.setdefault(entry_key, {})
        

        updates = {}
        for k in v_info.keys() | merge_info.keys():
            if k in ('info_level', 'unavailable_msgs'):
                continue # handled separately
            v = v_info.get(k, NO_VALUE)

            is_latest = curr_epoch >= latest_epochs[k]
            if is_latest:
                latest_epochs[k] = curr_epoch
            
            report_update = field_updater(merge_info, k, v, is_latest)

            if report_update and update_filter(k):
                # doesn't truncate, could be added to update_filter maybe
                updates[str(k)] = str(v)

            # Debug: show keys and if it was added to 'updates'
            # a = report_update
            # b = update_filter(k)
            # print(f"{k:<25}   {utils.color_bool(a)} {utils.color_bool(b)}   {utils.color_bool(a and b)}")

        # better_info
        # check new merge_info V_InfoLevel (affected by field_updater)
        new_info_level = yt_utils.derive_v_info_level(merge_info, check=False)
        if merge_info_level < new_info_level:
            merge_info['info_level'] = new_info_level.name
            if update_filter('info_level'):
                updates['info_level'] = new_info_level.name
            timeline_entry['better_info'] = f'{merge_info_level.name} -> {new_info_level.name}'
            merge_info_level = new_info_level

        if updates:
            timeline_entry['updates'] = utils.merge_objs(timeline_entry.get('updates', {}), updates, True)
        if not timeline_entry:
            v_timeline.pop(entry_key)
        else:
            timeline_entry['info_level'] = merge_info_level.name

    unavailable_msgs = _dedup_and_sort_unavail_msgs(unavailable_msgs)
    for msg in unavailable_msgs:
        uanvail_epoch = yt_utils.to_readable_epoch(msg['epoch'] if msg['epoch'] is not None else yt_utils.DEFAULT_EPOCH())
        text = msg['msg'] or f'[{msg['type']}]' # the type should be surrounded in the first square bracket []
        msgs = v_timeline.setdefault(uanvail_epoch, {}).setdefault('unavailable', [])
        if text not in msgs:
            msgs.append(text)

    merge_info['unavailable_msgs'] = unavailable_msgs

    # RfS3-3A57OY - why is FLAT missing
    # qMuLtIC4w64 - why is it NONE and not FLAT
    # if v_infos[0]['id'] == 'RfS3-3A57OY':
    #     epoch = yt_utils.to_readable_epoch(utils.epoch_now())
    #     utils.json_dump(v_infos,    f'merge_test/{epoch}.v_infos.json',         indent=2)
    #     utils.json_dump(merge_info, f'merge_test/{epoch}.merge_v_infos.json',   indent=2)
    #     utils.json_dump(v_timeline, f'merge_test/{epoch}.v_timeline.json',      indent=2)
    #     import time
    #     time.sleep(1)

    return merge_info, v_timeline

def _merge_v_sort_key(info_level: V_InfoLevel|str|None, epoch: int) -> int:
    if info_level is None:
        info_level = V_InfoLevel.NONE
    try:
        if isinstance(info_level, str):
            info_level = V_InfoLevel[info_level]
    except KeyError:
        info_level = V_InfoLevel.NONE
    
    LARGE_TIME_DELTA = 10**12 # ~31,688 years
    return (info_level.value * LARGE_TIME_DELTA) + epoch

def _merge_v_sort_key_from_v_info(v_info: V_InfoDict|dict) -> int:
    """
    sort by 'info_level' then 'epoch'
    
    [V_InfoLevel: large int] [epoch: int]
    """
    return _merge_v_sort_key(
        v_info.get('info_level', V_InfoLevel.NONE.name),
        yt_utils.get_epoch(v_info))

def merge_v_infos(
        v_infos: list[V_InfoDict],
        field_updater: Callable[[V_InfoDict, str, Any|type[NO_VALUE], bool], bool],
        update_filter: Callable[[str], bool] = lambda _: False,
        _init_v_info: V_InfoDict|None = None,
        _init_v_timeline: V_MergeTimeline|None = None,
    ) -> tuple[V_InfoDict, V_MergeTimeline]:
    """
    Creates copies of all dict arguments
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
        _init_v_info (V_InfoDict|None): Initial v_info. Can be in `v_infos`. Defaults to None.
        _init_v_timeline (V_MergeTimeline|None): Initial V_MergeTimeline. Defaults to None.
    """

    if len(v_infos) == 0 and not _init_v_info:
        raise ValueError("Provide at least 1 v_info.")
    v_infos = v_infos.copy()
    if _init_v_info and _init_v_info not in v_infos:
        v_infos.append(_init_v_info)
    ids = {info['id'] for info in v_infos}
    if len(ids) != 1:
        raise ValueError(f"Multiple video ids found: {ids}")

    v_infos = utils.dedup(v_infos, id)

    v_infos = sorted(v_infos, key=_merge_v_sort_key_from_v_info)

    # DEBUG: Shows v_info order
    # print(v_infos[0]['id'], v_infos[0].get('title'))
    # for v_info in v_infos:
    #     print(_merge_v_sort_key(v_info), yt_utils.get_epoch(v_info), v_info.get('info_level'))
    # print(_init_v_timeline or {})
    # print()

    return _merge_v_infos(
        v_infos,
        field_updater,
        update_filter,
        _init_v_info or {'id': v_infos[0]['id'], 'info_level': V_InfoLevel.NONE.name},
        _init_v_timeline or {})


def _get_v_infos(pl_v_ids: list[V_ID], pl_infos: list[PL_InfoDict], pl_index_to_omit: int|None = None) -> dict[V_ID, list[V_InfoDict]]:
    """ 
    Looks through the pl_infos and returns a dict from video id to a list of copied v_infos from the pl_infos.

    If pl_index_to_omit is given, its v_infos are omitted in the return.
    """
    

    v_id_to_paths: dict[V_ID, list[V_InfoDict]] = {}
    for pl_info in pl_infos:
        for v_info in pl_info['entries']:
            if v_info['id'] in pl_v_ids:
                v_id_to_paths.setdefault(v_info['id'], [])
                if pl_index_to_omit is not None and v_info in pl_infos[pl_index_to_omit]['entries']:
                    continue
                v_id_to_paths[v_info['id']].append(yt_utils.copy_and_sanitize_info(v_info))

    if absent_v_ids := [v_id for v_id in pl_v_ids if v_id not in v_id_to_paths]:
        utils.WARNING(f"{absent_v_ids = }")
    
    return v_id_to_paths

def _merge_pl_infos(
        pl_infos: list[PL_InfoDict],
        extra_v_infos: list[V_InfoDict],
        field_updater: Callable[[V_InfoDict, str, Any|type[NO_VALUE], bool], bool],
        update_filter: Callable[[str], bool],
        _init_merge_info: PL_InfoDict|None,
) -> PL_InfoDict:
    
    V_ID_ORDER = merge_ordered_lists(
        [[entry['id']
            for entry in pl_info['entries']]
                for pl_info in pl_infos])


    id_to_infos = _get_v_infos(
        V_ID_ORDER, pl_infos,
        pl_index_to_omit=(None if _init_merge_info is None else pl_infos.index(_init_merge_info)))

    for v_info in extra_v_infos:
        id_to_infos[v_info['id']].append(v_info)

    _init_id_to_infos: dict[V_ID, V_InfoDict] = {}
    if _init_merge_info: _init_id_to_infos = {entry['id']: entry for entry in _init_merge_info['entries']}

    # set all playlist-only keys, except merge_timeline.
    merge_info: PL_InfoDict = {k: v for k, v in yt_utils.copy_and_sanitize_info(pl_infos[-1]).items()
                               if k not in {'entries', 'merge_timeline'}} # type: ignore - init
    merge_entries: list[V_InfoDict] = merge_info.setdefault('entries', [])
    merge_timeline: PL_MergeTimeline = merge_info.setdefault('merge_timeline', {})

    _init_pl_timeline: PL_MergeTimeline = {} if _init_merge_info is None else _init_merge_info.get('merge_timeline', {})
    for v_id in V_ID_ORDER:
        merge_entry, v_timeline = merge_v_infos(
            v_infos          = id_to_infos[v_id],
            field_updater    = field_updater,
            update_filter    = update_filter,
            _init_v_info     = _init_id_to_infos.get(v_id, None),
            _init_v_timeline = _init_pl_timeline.get(v_id, None))
        
        merge_entries.append(merge_entry)
        merge_timeline[v_id] = v_timeline
    
    yt_utils.fixup_pl_info(merge_info)
    return merge_info

def merge_pl_infos(
        pl_infos: list[PL_InfoDict],
        extra_v_infos: list[V_InfoDict],
        field_updater: Callable[[V_InfoDict, str, Any|type[NO_VALUE], bool], bool],
        update_filter: Callable[[str], bool],
        _init_merge_info: PL_InfoDict|None = None,
) -> PL_InfoDict:
    """
    Args:
        pl_infos (list[PL_InfoDict]): The source pl_infos. List input order does not matter because sorting is done at the start.
            All pl_infos should have the same playlist id.
        field_updater (Callable[[Merged_V_InfoDict, key, value, is_latest], did_update]):
            Specify the policy for how fields should be updated (see `Updater` for examples).
        update_filter (Callable[[str], bool]): Returns True to add key to timeline, False to omit.
            Used by ``merge_v_infos()``. Defaults showing all.
        _init_merge_info (PL_InfoDict|None): Initial merge info. Its timeline will be preserved.

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

    if len({pl_info['id'] for pl_info in pl_infos}) > 1:
        raise ValueError(f"More than one playlist id found: { {pl_info['id'] for pl_info in pl_infos} }")
    if len(pl_infos) == 0 and not _init_merge_info:
        raise ValueError("Provide at least 1")
    
    pl_infos = utils.dedup(pl_infos, id)
    def warn_non_init_merge():
        non_init_merge_infos = []
        for pl_info in pl_infos:
            if yt_utils.derive_pl_info_level(pl_info) == PL_InfoLevel.MERGE:
                non_init_merge_infos.append(pl_info)
        if non_init_merge_infos:
            from pldl.post_processing.reorder_infodict_keys import reorder_merge_info
            utils.WARNING(f"{len(non_init_merge_infos)} pl_info merge_timeline's will be omitted from merge_info.")
            ds = yt_utils.copy_and_sanitize_info(non_init_merge_infos)
            map(reorder_merge_info, ds)
            utils.json_dump(list(ds), 'omitted_merge_timeline_infos.json')
    warn_non_init_merge()

    if _init_merge_info and _init_merge_info not in pl_infos:
        pl_infos.append(_init_merge_info)

    # newest to oldest (highest priority to lowest)
    pl_infos = sorted(pl_infos, key=yt_utils.get_epoch, reverse=True)

    return _merge_pl_infos(pl_infos, extra_v_infos, field_updater, update_filter, _init_merge_info)
