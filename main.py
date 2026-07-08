from playlist_downloader import *
from config import *

config = PlaylistDL_Config(
    ident='',
    ident_type=ConfigID_Type.METADATA_PATH
)
PlaylistDL(config)