"""
Designed for `import *`

Conveniently extract and download videos from any YouTube playlist you can view.
By default, try to download from `YouTube` and fallback on `InternetWebArchive`.

See `config.py` and `playlist_downloader.py`
"""

from . import utils

from .yt_types import *
from . import yt_types
from . import yt_utils
from .playlist_dl import PlaylistDL
from .config import PlaylistDL_Config

from . import display
from . import post_processing