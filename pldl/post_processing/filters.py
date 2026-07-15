from ..yt_types import *

def filter_v_info(v_info: V_InfoDict, keys: set) -> None:
    for k in keys:
        if k in v_info:
            v_info.pop(k)

def filter_pl_info(pl_info: PL_InfoDict, pl_keys: set, v_keys: set) -> None:
    for k in pl_keys:
        if k in pl_info:
            pl_info.pop(k)
    for v_info in pl_info['entries']:
        filter_v_info(v_info, v_keys)
