"""
1.  Update metadata path_templs to ALL be relative home
2.  Refactor playlist_downloader to the below
3.  If ident_type is Metadata and path_tmpls aren't given,
    config should use the path_tmpls found in the metadata file. 


I want to download a whole playlist at once
  - That's the whole point of the program :)

I want to merge all historical info with the newly extracted info
  - Use postprocessing.merge_pl_infos()

I want to download the playlist with ALL videos from past extracted flat_infos
  - Do a merge to always overwrite to newest while maintaining videos removed from the list
    If refresh timer is up, extract a new flat_info then merge with maintained
    MID_PRIORITY

I want to download videos from arbitrary urls that yt_dlp supports
  - TODO Pass in the pl info, then call ``download_video(url, v_ident)``
    Where `video_ident` is the `v_id` (on YouTube) or the playlist index in the loaded _base_info.
    HIGH_PRIORITY

I want to print a table of all videos given a fmt string
  - TODO Get all required fields from the fmt. Find defualts for all (eg None or 0).
    For each entry in the playlist, do `fmt % (v_info | pl_info | defaults)`
    Use ``yt_dlp.utils.render_table()`` and ``yt_dlp.utils.format_field()``
    But, nothing complicated. Any more is out of scope.
    LOW_PRIORITY

I want a GUI
    NO.

I want to be able to change the file structure after initial extracts.
    TODO Create a postprocessor. This may or may not be tricky.
    Do not automatically unlink the original until the generated one is validated.
    Requires a thorough path validator. Can be reused for PlaylistDL init.
    LOW_PRIORITY


Required: 
self._config
self._resolved_pl_paths (pl_outtmpls)
self._infos = dict[
    InfoType: Literal['ext_flat', 'ext_videos', 'cached_pl', 'cached_merge'],
    dict['data': InfoDict, 'loaded_from_path': bool, 'path': str] = {}
self.old_metadata: loaded | None
self.metadata: Generate from self.old_metadata 


@property
history: from self.metadata or self.old_metadata or None                NO_CACHE
yt_dlp_download_archive: load file from self.metadata                   NO_CACHE

generate_pl_info: from self._base_info and self.extracted_v_infos       NO_CACHE
generate_merge_info: from self.pl_info (prop) and merge                 NO_CACHE

Lazily cache the below in self._infos
If is_written is False (newly generated data) or path matches metadata pointer return the data
If is_written and doesn't match metadata pointer. Load metadata pointer.
If not in self._infos load with metadata or None
    flat_info
    v_infos
    archive_flat_info (base info):
    latest_flat_info (base info):
    latest_pl_info
    latest_merge_info

Init:
All Required + Metadata

Two types of info jsons:
RAW:
    flat_info (Flat_InfoDict): FOLDER 
    v_infos (list[v_info]):    FOLDER (v_infos are unordered),
PROCESSED:
    archive_flat_info (Flat_InfoDict): SINGLE 
    pl_info (Pl_InfoDict):    FOLDER or SINGLE 
    merge_info (Pl_InfoDict): FOLDER or SINGLE 

Note:
    All infojson filenames should include epoch (will be latest epoch in v_info or ``epoch_now()``).
    A readable epoch can be used.
Metadata Pointers:
    archive_flat_info, latest_flat_info, latest_pl_info, latest_merge_info

API: 
download() - calls download_playlist()

extract_flat_info() - force latest flat info (merge?)
extract_playlist() TODO - is it possible to get more information on the playlist itself?

download_video(id_or_url: str) -> V_InfoDict Near direct call to yt_wrapper.download_video
    Validate that video id is in the playlist, append result to extracted_v_infos 
download_playlist() Use yt_wrapper.download_playlist
download_video_alt(url, video_ident=None) Try download using any valid yt_dlp url. TODO
    Validate that the `ident` key or infodict at key=`id` matchs a video in the playlist.
    `id` in the infodict should be set the video id even if it is different.
    Append info to self.extracted_v_infos.
    Do we care if there is an exception: yes if the url is valid and it is associatted with a video id.

get_opts(include_cookies: bool)

Only useful if write isn't set in config.
    write_extracted_flat_info() -> bool
    write_extracted_v_infos() -> bool
    write_pl_info() -> bool
    write_merge_info() -> bool

Called Internally:
_write_latest_flat_info() -> bool
_write_metadata()
_load_latest(file_type) see if cached matches metadata; return cache or load or None


General Flow:
INIT:   Set `config`
        Load or extract `base_info`
        Load and validate both `metadata` and `ytdlp_download_archive` (Default None).

USER:   Should be able to run any API function.
        Configs should trigger automatic operations after each download 
        Emptying cookies should be done when the PlaylistDL is closed
"""