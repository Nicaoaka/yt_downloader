"""
Designed for `import *`

Conveniently extract and download videos from any YouTube playlist you can view.
By default, try to download from `YouTube` and fallback on `InternetWebArchive`.

See `config.py` and `playlist_downloader.py`
"""

from pldl.pldl_types import *
from pldl import (
    pldl_types,
    pldl_type_extensions,
    yt_utils,
    display,
    post_processing,
)
from pldl.utils import *
from pldl.playlist_dl import PlaylistDL
from pldl.config import PlaylistDL_Config, Config_IdentType, wrapper_match_filter_builder
