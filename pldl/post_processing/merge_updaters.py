"""
Signiture (Callable[[V_InfoDict|dict, str, Any|type[NO_VALUE], bool], bool]):
Args:
    Merged_V_InfoDict (V_InfoDict|dict):
    key (str):
    value (Any|type[NO_VALUE]):
    is_latest (bool): Is from the latest v_info in the merge operation
Return:
    report_update (bool): Return True if there was a notable update. ``update_filter()`` will then be called with the key.

'info_level' and 'unavailable_msgs' should not be written to.
"""

from typing import Any

from pldl.pldl_types import *

def latest(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    if is_latest and v != NO_VALUE:
        info[k] = v
        return True
    return False

def latest_not_None(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    if v is None:
        return False
    return latest(info, k, v, is_latest)

def latest_only(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    if not is_latest:
        return False
    if v == NO_VALUE:
        info.pop(k)
    else:
        info[k] = v
    return True

def _unsafe_maximizer(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    if v is None or v == NO_VALUE:
        return False
    if (v or 0) > (info.get(k) or 0): # type: ignore - values may not define __gt__
        info[k] = v
        return True
    return False

def maximizer(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    try:
        return _unsafe_maximizer(info, k, v, is_latest)
    except Exception: # not sure what errors may appear
        return fill_empty(info, k, v, is_latest)

def fill_empty(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    if v is None or v == NO_VALUE:
        return False
    if is_latest or (k not in info or info[k] is None):
        info[k] = v
        return True
    return False

def latest_not_none_and_latest_unavail(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    if info.get(k, NO_VALUE) == v:
        return False
    
    match k:
        case 'yt_unavailable_msg' | 'wa_unavailable_msg':
            return latest_only(info, k, v, is_latest)
        case _:
            return latest_not_None(info, k, v, is_latest)
