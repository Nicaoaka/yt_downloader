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

from typing import Any, Callable

from pldl.pldl_types import *

type Signature = Callable[[V_InfoDict | dict, str, Any | type[NO_VALUE], bool], bool]

def builder(k_to_func: dict[tuple[str, ...], Signature], default_func: Signature) -> Signature:
    flattened: dict[str, Signature] = {}
    for keys, func in k_to_func.items():
        for k in keys:
            if k in flattened:
                raise ValueError(f"{k} appears more than once in k_to_func keys")
            flattened[k] = func
    def res(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
        if k == v:
            return False
        return flattened.get(k, default_func)(info, k, v, is_latest)
    return res



def latest_exact(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    """ will pop if the latest value is absent """
    if not is_latest:
        return False
    if v == NO_VALUE:
        info.pop(k)
    else:
        info[k] = v
    return True


def fill_absent(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    if v == NO_VALUE:
        return False
    if k not in info:
        info[k] = v
        return True
    return False

def maximizer(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    try:
        if v is None or v == NO_VALUE:
            return False
        if (v or 0) > (info.get(k) or 0): # type: ignore - values may not define __gt__
            info[k] = v
            return True
        return False
    except Exception: # not sure what errors may appear
        return fill_absent(info, k, v, is_latest)


def latest_not_none_and_not_same(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    if v != NO_VALUE and is_latest and v is not None and v != info.get(k, NO_VALUE):
        info[k] = v
        return True
    return False


COMMON_UPDATER = builder(
    {
        ('yt_unavailable_msg', 'wa_unavailable_msg'): latest_exact,
        ('view_count', 'like_count', 'comment_count'): maximizer,
    },
    default_func=latest_not_none_and_not_same)
