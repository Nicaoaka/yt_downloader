"""
Designed for `import *`

Conveniently extract and download videos from any YouTube playlist you can view.
By default, try to download from `YouTube` and fallback on `InternetWebArchive`.

See `config.py` and `playlist_downloader.py`
"""


from ._types import *
from . import (
    utils,
    yt_utils,
    display,
    post_processing
)
from .playlist_dl import PlaylistDL
from .config import PlaylistDL_Config
