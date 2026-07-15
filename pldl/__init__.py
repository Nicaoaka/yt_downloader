"""
Designed for `import *`

Conveniently extract and download videos from any YouTube playlist you can view.
By default, try to download from `YouTube` and fallback on `InternetWebArchive`.

See `config.py` and `playlist_downloader.py`
"""

from . import utils

from . import yt_utils
from .yt_types import *
from . import display
from .playlist_downloader import PlaylistDL
from .config import PlaylistDL_Config

from . import post_processing