"""What yt-dlp hands back, wrapped in pldl's envelope.

    infodicts.py  the yt-dlp payload shapes (TypedDicts) and id aliases
    levels.py     how much is known about a video, and `rank()`, the chronological sort key
    errors.py     why an extractor could not get a video
    videos.py     VideoEntry: pldl's fields around one video's infodict
    playlists.py  Capture: one extraction's worth of entries

**No module here imports yt_dlp** -- that import alone takes ~0.4 s, and nothing that only
reads or merges a record should pay for it. The code that actually calls yt-dlp gets its own
module, imported only by what downloads.
"""
from __future__ import annotations

from pldl.downloader.errors import ErrorClass, UnavailableInfo
from pldl.downloader.infodicts import (
    PL_ID,
    V_ID,
    ANY_InfoDict,
    PL_InfoDict,
    V_InfoDict,
    YT_DLP_InfoDict,
)
from pldl.downloader.levels import Rank, V_InfoLevel, coerce_v_level, derive_v_info_level, rank
from pldl.downloader.playlists import Capture
from pldl.downloader.videos import VideoEntry

__all__ = [  # noqa: RUF022
    'V_ID', 'PL_ID',
    'YT_DLP_InfoDict', 'V_InfoDict', 'PL_InfoDict', 'ANY_InfoDict',
    'V_InfoLevel', 'coerce_v_level', 'derive_v_info_level', 'Rank', 'rank',
    'ErrorClass', 'UnavailableInfo',
    'VideoEntry', 'Capture',
]
