from pathlib import Path
import re

from pldl.pldl_types import *

# Playlist file helper
# TODO: Test these 2 functions

def denumber_videos(video_dir: Path, video_tmpl: str, digits: int = 0):
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
        denumber_videos(v_dir, number_tmpl, digits)
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

