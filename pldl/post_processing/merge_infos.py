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
        utils.dedup(msgs, hash=lambda x: tuple((x['epoch'], x['msg'], x['type']))),
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
    
    merge_info_level = yt_utils.get_v_info_level(merge_info)
    unavailable_msgs: list[UnavailableMsg] = []

    for v_info in yt_utils.copy_and_sanitize_info(v_infos):
        unavailable_msgs.extend(v_info.get('unavailable_msgs', []))

        # nothing below should aggregate init info

        epoch = yt_utils.to_readable_epoch(yt_utils.get_epoch(v_info))
        timeline_entry = v_timeline.setdefault(epoch, {})
        
        # updating v_info
        is_latest = yt_utils.get_epoch(v_info) >= yt_utils.get_epoch(v_infos[-1])

        updates = {}
        for k in v_info.keys() | merge_info.keys():
            if k == 'info_level':
                continue
            v = v_info.get(k, NO_VALUE)
            report_update = field_updater(merge_info, k, v, is_latest)
            if report_update and update_filter(k):
                # doesn't truncate, could be added to update_filter maybe
                updates[k] = v

        # better_info
        new_info_level = yt_utils.get_v_info_level(v_info)
        if merge_info_level < new_info_level:
            merge_info['info_level'] = new_info_level.name
            if update_filter('info_level'):
                updates['info_level'] = new_info_level.name
            timeline_entry['better_info'] = f'{merge_info_level.name} -> {new_info_level.name}'
            merge_info_level = new_info_level

        if updates:
            timeline_updates = timeline_entry.setdefault('updates', {})
            timeline_updates |= updates
        if not timeline_entry:
            v_timeline.pop(epoch)

    for msg in _dedup_and_sort_unavail_msgs(unavailable_msgs):
        uanvail_epoch = yt_utils.to_readable_epoch(msg['epoch'] if msg['epoch'] is not None else yt_utils.DEFAULT_EPOCH())
        text = f"{msg['type']}: {msg['msg']}"
        msgs = v_timeline.setdefault(uanvail_epoch, {}).setdefault('unavailable', [])
        if text not in msgs:
            msgs.append(text)

    return merge_info, v_timeline

def merge_v_infos(
        v_infos: list[V_InfoDict],
        field_updater: Callable[[V_InfoDict, str, Any|type[NO_VALUE], bool], bool],
        update_filter: Callable[[str], bool],
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
    v_infos = sorted(v_infos, key=yt_utils.get_epoch) # oldest to newest

    return _merge_v_infos(
        v_infos,
        field_updater,
        update_filter,
        _init_v_info or {'id': v_infos[-1]['id'], 'info_level': yt_utils.V_InfoLevel.NONE.name},
        _init_v_timeline or dict())


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
        field_updater: Callable[[V_InfoDict, str, Any|type[NO_VALUE], bool], bool],
        update_filter: Callable[[str], bool],
        _init_merge_info: PL_InfoDict|None = None,
) -> PL_InfoDict:
    """
    Args:
        pl_infos (list[PL_InfoDict]): The source pl_infos. List input order does not matter becaduse sorting is done at the start.
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
            if yt_utils.get_pl_info_level(pl_info) == yt_utils.PL_InfoLevel.MERGE:
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
    pl_infos = sorted(pl_infos, key=yt_utils.get_epoch)

    return _merge_pl_infos(pl_infos, field_updater, update_filter, _init_merge_info)
