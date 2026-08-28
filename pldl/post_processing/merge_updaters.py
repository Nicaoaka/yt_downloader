"""
MergeFieldUpdater (Callable[[V_InfoDict|dict, str, Any|type[NO_VALUE], bool], bool]):
Args:
    Merged_V_InfoDict (V_InfoDict|dict):
    key (str):
    value (Any|type[NO_VALUE]):
    is_latest (bool): Is from the latest v_info in the merge operation
Return:
    report_update (bool): Return True if there was a notable update. ``update_filter()`` will then be called with the key.

'info_level' and 'unavailable_msgs' should not be written to.
"""

from collections.abc import Callable
from typing import Any

from pldl.pldl_types import *

type MergeFieldUpdater = Callable[[V_InfoDict | dict, str, Any | type[NO_VALUE], bool], bool]


def no_update(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    return False

def latest_exact(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    """ will pop if the latest value is absent """
    if not is_latest or info.get(k, NO_VALUE) == v:
        return False
    if v == NO_VALUE:
        info.pop(k)
    else:
        info[k] = v
    return True

def fill_absent(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    if v == NO_VALUE or info.get(k, NO_VALUE) == v:
        return False
    if k not in info:
        info[k] = v
        return True
    return False

def maximizer(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    if v is None or v == NO_VALUE or info.get(k, NO_VALUE) == v:
        return False
    try:
        if v > (info.get(k) or 0): # type: ignore - values may not define __gt__
            info[k] = v
            return True
        return False
    except Exception:  # noqa: BLE001 - not sure what errors may appear
        return fill_absent(info, k, v, is_latest)

def latest_not_none(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    if v == NO_VALUE or info.get(k, NO_VALUE) == v:
        return False
    if is_latest and v is not None:
        info[k] = v
        return True
    return False


def builder(k_to_func: dict[tuple[str, ...], MergeFieldUpdater], default_func: MergeFieldUpdater) -> MergeFieldUpdater:
    flattened: dict[str, MergeFieldUpdater] = {}
    for keys, func in k_to_func.items():
        for k in keys:
            if k in flattened:
                raise ValueError(f"{k} appears more than once in k_to_func keys")
            flattened[k] = func
    def res(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
        return flattened.get(k, default_func)(info, k, v, is_latest)
    return res


COMMON_UPDATER = builder(
    {
        # ('view_count', 'like_count', 'comment_count'): maximizer, # prefer ability to show decreasing over accuracy
        ('yt_unavailable_msg', 'wa_unavailable_msg'): latest_exact, # only last v_info extraction attempt
        ('info_level', 'unavailable_msgs' ): no_update, # handled by _merge_v_infos
        ('epoch', ): latest_not_none, # for _merge_v_infos
    },
    default_func=latest_not_none)




"""
Previously, the epoch was updated to stay aligned with the source pl_info,
in `post_processing._merge_v_infos()`. This isn't ideal because collisions can occur.
In fact, they occur in every case. If you extract or download, then create merge_info.
The merge flat will correctly update its fields to match the new info, including epoch.
With this, the merge_flat and the new info now have the same set of epochs.

Some possible fixes:

- Fix1: Use `utils.merge_infos`
    - Pro: accurate 'latest' infodict
    - Con: change ownership is ambiguous

- Fix2: Don't update epoch
    - Pro: simplest
    - Con: inaccurate `epoch` in merge

- Fix3: Subtract a small amount of time from the v_info epoch when updating merge_flat. (eg -= 1)
    - Pro: Stays accurate
    - Con: Could still conflict if another extract of the same id occurred that delta of time earlier
        Misaligned epochs from source info (worse for data integrity/lookup)
        Most complicated

Chose Fix3:
    It has the most accuracy.
    The epoch source missalignment wont effect how I am currently using the infojsons.

Note, extract and downlaod info will NOT have collisions between themselves because they are extracted
independently.
"""
def __flat_merge_epoch_updater(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    """made for `FLAT_MERGE_UPDATER`"""
    if v == NO_VALUE or info.get(k, NO_VALUE) == v:
        return False
    if isinstance(v, int) and is_latest:
        info[k] = v-1
        return True
    return False

FLAT_MERGE_UPDATER = builder(
    { 
        (
            'id', 'title', 'live_status', 'availability', 'channel', 'channel_id', 'channel_url', 'uploader',
            'uploader_id', 'uploader_url', 'creators', 'view_count', 'timestamp', 'duration',
            'thumbnails', 'url', '_type', 'ie_key', '__x_forwarded_for_ip', 'playlist_epoch',
        ): latest_not_none,
        ('epoch', ): __flat_merge_epoch_updater,
    },
    default_func=no_update)