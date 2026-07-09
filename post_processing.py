from collections import defaultdict
from pathlib import Path
import re
from enum import IntEnum
from typing import TypedDict, NotRequired

from yt_dlp import YoutubeDL

import utils
from merger import merge_ordered_lists
from yt_types import *
import yt_types
import yt_utils


# Data helpers

def get_pl_v_info(pl_info: PL_InfoDict, v_idx):
    return {
        'playlist_id':                  pl_info['id'],
        'playlist':                     pl_info['title'] or pl_info['id'],
        'playlist_count':               pl_info['playlist_count'],
        'n_entries':                    pl_info['playlist_count'],
        'playlist_index':               v_idx,
        'playlist_autonumber':          v_idx,
        'playlist_title':               pl_info['title'],
        'playlist_channel':             pl_info['channel'],
        'playlist_channel_id':          pl_info.get('channel_id'),
        'playlist_uploader':            pl_info['uploader'],
        'playlist_uploader_id':         pl_info['uploader_id'],
        'playlist_webpage_url':         pl_info.get('webpage_url') or pl_info.get('original_url') or pl_info.get('url'),
    }

def get_latest_epoch(pl_info: PL_InfoDict) -> int:
    latest = max(entry.get('epoch', 0) for entry in pl_info['entries'])
    latest = max(latest, pl_info.get('epoch', 0))
    if latest == 0:
        utils.WARNING(f"All epochs are malformed or missing: {latest}")
    return latest

def add_pl_info_to_entries(pl_info: PL_InfoDict):
    for i, entry in enumerate(pl_info['entries']):
        entry.update(get_pl_v_info(pl_info, i)) # type: ignore



# Playlist file helper
# TODO: Test these 2 functions

def denumber_videos(video_dir: str, video_tmpl: str, digits: int = 0):
    """Removes the index number from video files

    Args:
        video_dir (str): Videos directory
        v_tmpl (str): Video filename template. Defaults to `%(idx)s. %(name)s`.
        digits (int, optional): Expected number of digits (if 0 catch as many in a row as possible). Defaults to `0`.

    Raises:
        ValueError: For invalid `v_tmpl`
    """

    raise NotImplementedError(f"{denumber_videos.__name__} is not ready")

    __IDX = re.escape('__idx_placeholder')
    __NAME = re.escape('__name_placeholder')
    if __IDX in video_tmpl:
        raise ValueError(f"{repr(__IDX)} can't be in number_tmpl {repr(video_tmpl)}")
    if __NAME in video_tmpl:
        raise ValueError(f"{repr(__NAME)} can't be in number_tmpl {repr(video_tmpl)}")
    
    fmt = video_tmpl % {
        'idx': __IDX,
        'name': __NAME,
    }
    pattern = '^' + re.escape(fmt)\
                    .replace(__IDX, fr'(\d{{{digits}}}\d*)')\
                    .replace(__NAME, fr'(.+)') + '$'
    
    for v_path in video_dir.iterdir():
        match = re.match(pattern, v_path.name, re.VERBOSE)
        if not match:
            print(f"[UNRECOGNIZED or already DENUMBERED] {v_path.name}")
            continue

        _idx = match.group(1)
        denumbered_path = video_dir / match.group(2)
        if denumbered_path.exists():
            print(f"[WARNING] Denumbered file already exists ({v_path.name})")
            continue

        v_path.rename(denumbered_path)
        print(f"[INFO] renamed: {v_path.name} -> {denumbered_path.name}")

def number_videos(v_dir: Path, pl_info: PL_InfoDict, video_fn_tmpl: str, digits: int = 2, number_tmpl: str = '%(idx)s. %(name)s', denumber_before: bool = False):

    raise NotImplementedError(f"{number_videos.__name__} is not ready")

    if denumber_before:
        denumber_videos(v_dir, digits, number_tmpl)
    if not v_dir.exists():
        return
    
    for i, entry in enumerate(pl_info.get('entries', []), start=1):
        video_filename = utils.safely_resolve_path(video_fn_tmpl, entry) # type: ignore - entry is a dict
        denumbered_path: Path = v_dir / video_filename
        
        idx = str(i).zfill(digits)
        numbered_path = denumbered_path.with_name(
            utils.sanitize_str(number_tmpl, {'idx': idx, 'name': video_filename})
        )

        match (denumbered_path.exists(), numbered_path.exists()):
            case True, False: # expected case
                denumbered_path.rename(numbered_path)
                print(f"[INFO] {idx} renamed: {denumbered_path.name} -> {numbered_path.name}")
            case True, True:
                print(f"[WARNING] {idx} Both exist")
            case False, True:
                print(f"[WARNING] {idx} Already exists")
            case False, False:
                print(f"[Video {str(i).rjust(digits)} NOT FOUND] {denumbered_path.name}")



# Merging info
# TODO: Update view count (etc.) using max

class V_MergeInfo(TypedDict):
    better_info: NotRequired[_V_InfoLevel]
    unavailable: NotRequired[list[str]]
    updates: NotRequired[list]

def merge_v_infos(v_infos: list[V_InfoDict | PL_V_InfoDict]) -> tuple[V_InfoDict | PL_V_InfoDict, dict]:
    """ Will ignore __PL_V_InfoDict information.

    Does not copy v_info objects. Some input object references will be the same in the output! """
    if not v_infos:
        raise ValueError("Provide at least 1")
    
    v_infos = sorted(v_infos, key=lambda info: (info.get('epoch') or info.get('playlist_epoch') or 0), reverse=True)
    merge: V_InfoDict | PL_V_InfoDict = {} # type: ignore - init
    merge_info_level = _V_InfoLevel.NONE
    metadata: dict[yt_types.EPOCH_STR, V_MergeInfo] = defaultdict(dict) # type: ignore
    for k in ('yt_unavailable_msg', 'wa_unavailable_msg'):
        if k in v_infos[0]:
            merge[k] = v_infos[0].get(k)

    for i, v_info in enumerate(v_infos):
        V_EPOCH_KEY = f'{i} {v_info.get('epoch', 0)}'
        for k in ('yt_unavailable_msg', 'wa_unavailable_msg'):
            if k not in v_info:
                continue
            merge.setdefault('unavailable_msgs', [])
            merge['unavailable_msgs'].append({ # type: ignore - see line above
                'pl_epoch': v_info.get('playlist_epoch'),
                'epoch': v_info.get('epoch'),
                'msg': v_info.get(k),
            })
            
            metadata[V_EPOCH_KEY]['unavailable'] = metadata[V_EPOCH_KEY].get('unavailable', []) + [k]
        
        updates = []
        for k, v in v_info.items():
            if k in ('yt_unavailable_msg', 'wa_unavailable_msg'):
                continue # special case
            if utils.dict_set_if(merge, k, v): # type: ignore - res_entry is a dict
                updates.append(k)

        new_info_level = yt_utils.get_v_info_level(v_info)
        if not updates:
            continue
        if new_info_level >= merge_info_level:
            metadata[V_EPOCH_KEY]['better_info'] = new_info_level
            merge_info_level = new_info_level
        else:
            metadata[V_EPOCH_KEY]['updates'] = updates
    return merge, metadata

def merge_pl_infos(pl_infos: list[PL_InfoDict]) -> PL_InfoDict:
    """ Creates a new pl_info dict with the newest and largest info.

    Playlist info:
    - In general, prefer the newest pl_info
    - Manually updates the following to represent the combined version
        - playlist_count
        - entries
    - Add merge metadata
        - merge_info (dict[epoch, list[v_id]]): What changed and from when/what
    
    Entry info:
    - Use Newest
    - Replace `None` and absent values with previous info
        - May lead to impossible yt_dlp info_dict state - this limitation is ok
    - Add `unavailable_msgs`

    Args:
        pl_infos (list[PL_InfoDict]): Source pl_infos

    Returns:
        PL_InfoDict: The merged playlist info
    """

    if len(pl_infos) == 0:
        raise ValueError("Provide at least 1")
    if len({pl_info['id'] for pl_info in pl_infos}) > 1:
        raise ValueError(f"More than one playlist id found: { {pl_info['id'] for pl_info in pl_infos} }")
    
    
    pl_infos = sorted(pl_infos, key=lambda info: -info.get('epoch', 0))
    V_ID_ORDER = merge_ordered_lists([[entry['id'] for entry in pl_info['entries']] for pl_info in pl_infos])
    print(V_ID_ORDER)
    v_id_position = {v_id: i for i, v_id in enumerate(V_ID_ORDER)}

    pl_info: PL_InfoDict = utils.dict_without_keys(pl_infos[0], ['entries']) # type: ignore - init
    pl_info['playlist_count'] = len(V_ID_ORDER)
    
    entries: list[PL_V_InfoDict] = [
        {'id': v_id, 'playlist_index': i}
        for i, v_id in enumerate(V_ID_ORDER)] # type: ignore - init


    v_idx_map = [list() for _ in range(pl_info['playlist_count'])]
    for pl_idx, _pl in enumerate(pl_infos):
        for v_idx, _v in enumerate(_pl['entries']):
            pl_v_idx = v_id_position[_v['id']]
            _v |= {**get_pl_v_info(pl_info, pl_v_idx), 'playlist_epoch': _pl['epoch']} # type: ignore
            v_idx_map[pl_v_idx].append((pl_idx, v_idx))
    
    pl_meta = {}
    for i, idxs in enumerate(v_idx_map):
        if len(idxs) == 0: # shouldn't be possible
            print(f"\n\nMISSING IDXS for {V_ID_ORDER[i]} (i={i}).\n\n{v_idx_map}\n\n")
            continue
        entry, v_meta = merge_v_infos([pl_infos[pl]['entries'][v] for pl, v in idxs])
        entries[i] |= entry #type: ignore
        pl_meta[entry['id']] = v_meta

    pl_info['entries'] = entries
    pl_info['merge_info'] = pl_meta # overwrite existing
    return pl_info


