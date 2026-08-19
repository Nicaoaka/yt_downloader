This project heavily relies on [yt-dlp](https://github.com/yt-dlp/yt-dlp).

# Setup

```ps
pip install -U "yt-dlp[default]
```
`yt-dlp` should be updated every so often to keep downloading working.

If you need cookies for your private playlists (e.g. Liked List, Watch Later),
you need to get your YouTube Cookies. The way I do it is through this chrome extension:
[Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc).

# Usage

See the `example.py` file.

Create a config using the `PlaylistDL_Config` dataclass.
Feed this into the PlaylistDL class.
In general, you can just call `.download()` to download and make files based on the config.

If a video is *only* found outside of youtube/webarchive, use `.download_v_info_generic()` prior to `.download()`.
Note that the video id should already be in the loaded base info of the PlaylistDL instance.

You can see the current states of v_infos based on the `_metadata.json`'s history or a merge pl_info.
You can use `display_metadata_history` or `display_pl_merge_timeline`.

# Structure
```
.
├── .gitignore                          
├── README.md                           
├── cli_to_api.py                       Get API opts from cli (yt-dlp is mainly a CLI).
├── example.py                          Example usage file.
├── pldl                                
│   ├── __init__.py                     
│   ├── config.py                       PlaylistDL config structure (PlaylistDL_Config)
│   ├── display.py                      Printing structured data
│   ├── playlist_dl.py                  Main file (PlaylistDL)
│   ├── pldl_type_extensions.py         More specific types. Useful if you know the extractors
│   │                                    and want type hinting.
│   ├── pldl_types.py                   Most of the types used throughout the repo.
│   │                                    (except InfoLevel which are in yt_utils.py)
│   ├── yt_utils.py                     All helpers that are related to pldl in particular or
│   │                                    depend on YoutubeDL
│   ├── post_processing                 
│   │   ├── __init__.py                 
│   │   ├── filters.py                  
│   │   ├── merge_infos.py              Merge pl/v_info
│   │   ├── merge_updaters.py           Updaters for merge_infos.py
│   │   │                                (could be moved to merge_infos.py)
│   │   ├── (_number_videos.py)         NOT WORKING - would add playlist number to files to order
│   │   │                                them in a file explorer. Follows user-defined format.
│   │   └── reorder_infodict_keys.py    Reorders keys in dicts for dumping to json
│   └── utils                           
│       ├── __init__.py                 
│       ├── merge_ordered_lists.py      Playlist v_id resolution
│       └── utils.py                    Helpers that don't have dependencies
├── tests                               
│   ├── __init__.py                     
│   ├── manual_merge_info_tests.py      (code written for testing)
│   ├── manual_pldl_manip_sb.py         (code written for testing)
│   ├── manual_sanitize_test.py         (code written for testing)
│   ├── test_merge_ordered_lists.py     For `pldl.utils.merge_ordered_lists.py`
│   └── test_utils.py                   For `pldl.utils.utils.py`
└── secrets                             
    └── cookie_file.txt                 Your cookie file. This should be empty besides
                                         when you are actually using it.
```    