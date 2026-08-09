# Turn the epochs in history in metadata into readable epochs.
# Test extraction/download from other sources

from pldl import *

config = PlaylistDL_Config(
    ident=r'LL',
    ident_type=Config_IdentType.PL_ID_OR_URL,
    # ident=r'Liked videos [LL]\_metadata.json',
    # ident_type=Config_IdentType.METADATA_PATH,
    home='', # (current working directory)

    cookie_file='secrets/cookie_file.txt',
    cookies_for_pl=True,
    cookies_for_vids=False,
    empty_cookies=True,
    
    write_flat=True,
    write_raw_v_infos=True,
    write_pl_info=True,
    write_merge=True,

    refresh_after= 7 * 24 * 3600,
    force_flat_extract=False,

    wrapper_match_filter=wrapper_match_filter_builder(
        max_extracts = 25,
        max_downloads = 5,
        quit_when_maxed = True,

        extract_match = lambda _: True, # extract whatever isn't downloaded
        download_match = lambda v: (
                 (v.get('view_count') or 0) < 250_000) # don't download popular videos
            and ((v.get('duration') or 0)   < 5 * 60), # don't download long videos

        overrides = {
            # DL_Action.USER:     [],
            # DL_Action.QUIT:     [],
            # DL_Action.SKIP:     [],
            # DL_Action.EXTRACT:  [],
            # DL_Action.DOWNLOAD: [],
        },

        fail_backoff_time = 7 * 24 * 3600,

        yt_unavailable_action = DL_Action.EXTRACT,
    ),
)

with PlaylistDL(config) as pldl:
    pldl.download(delete_prev_pl=True, delete_prev_merge=True)
    pldl.display_metadata_history()
    pldl.display_pl_merge_timeline(pldl._infos.merge_info)
