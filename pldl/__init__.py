"""
Designed for `import *`

Conveniently extract and download videos from any YouTube playlist you can view.
By default, try to download from `YouTube` and fallback on `InternetWebArchive`.

See `config.py` and `playlist_downloader.py`
"""

from pldl import (
    display,
    pldl_type_extensions,
    pldl_types,
    post_processing,
    yt_utils,
)
from pldl.config import *
from pldl.playlist_dl import *
from pldl.pldl_types import *
from pldl.utils import *
