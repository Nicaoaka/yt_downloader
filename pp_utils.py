from pathlib import Path
import re

import utils
from yt_types import *



# Data helpers
NO_EPOCH = 0 # or less

def get_pl_v_info(pl_info: PL_InfoDict, v_idx: int):
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

        # custom
        'playlist_epoch': pl_info.get('epoch', NO_EPOCH)
    }

def get_latest_epoch(pl_info: PL_InfoDict) -> int:
    """ Max 'epoch' in pl_info and its entries.
    
    A negative epoch means the epoch wasn't found or all were malformed. """
    latest = max(
        pl_info.get('epoch', NO_EPOCH),
        *(entry.get('epoch', NO_EPOCH) for entry in pl_info['entries']))
    if latest <= NO_EPOCH:
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
