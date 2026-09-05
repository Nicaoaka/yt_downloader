__all__ = [
    'PlaylistDL',
    'default_field_updater',
    'default_update_filter',
    'v_dl_order_manip_builder',
    'wrapper_match_filter_builder',
]

import copy
import dataclasses
import json
import os
import random
import time
from collections.abc import Callable, Hashable, Iterable
from typing import TYPE_CHECKING, Any, Literal, overload

from pldl import display, pldl_types, yt_utils
from pldl.config import (
    Config_IdentType,
    PlaylistDL_Config,
    V_DL_OrderManip,
    WrapperMatchFilter,
)
from pldl.pldl_types import *
from pldl.post_processing import (
    merge_infos,
    merge_updaters,
    reorder_infodict_keys,
)
from pldl.utils import utils

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison  # noqa: TC004


# FUTURE: This should be a util class with
# reading, writing, setting, copy, and have a __post_init__
# Then it could be inherited or composed for this yt-dlp use case.
@dataclasses.dataclass
class _InfosEntry[T]:
    data: T
    pl_outtmpl: str|None
    is_written: bool
    metadata_key: pldl_types._MetadataFiles_Lit | None

@dataclasses.dataclass
class _Infos:
    raw_flat:    _InfosEntry[PL_InfoDict] | None = None
    raw_v_infos: _InfosEntry[list[list[V_InfoDict]]] = None # type: ignore - set to [] default in init

    _merge_flat: _InfosEntry[PL_InfoDict] = None # type: ignore - set in init


def init_metadata(
        id: str,
        path_tmpls: Rel_PL_Resolved_CustomOuttmpl,
        history: PL_DownloadHistory|None = None,
        pointers: pldl_types.MetadataPointers|None = None
) -> Metadata:
    return {
        'id': id,
        'path_tmpls': path_tmpls,
        'pointers': pointers or {},
        'history': history or {},
    }

def sleep_random_seconds(lo: float, hi: float):
    x = random.uniform(lo, hi)
    caller = utils.get_caller_function()
    print(utils.hex(f"[{caller}] Sleeping for {x:.3} second ...", fg="#000436"), end='', flush=True)
    time.sleep(x)
    print()

class No_YT_DLP_Downloads(Exception):
    pass

class USE_CONFIG(utils.FalsySentinel):
    pass

# 
# Functions used in params
# (might fit better in config.py, not sure)
# 

DEBUG_FG = {
    "FAIL": "#ff5c4d",
    "403": "#ff8a3d",
    "MAX": "#e0c33d",
    "OVERRIDE": "#b48cf0",
    "DOWNLOAD": "#6a9955",
    "EXTRACT": "#4ec9b0",
    "SKIP_REASON": "#5c5c5c",
}

def v_dl_order_manip_builder(key: Callable[[V_InfoDict], SupportsRichComparison] = lambda _: 1, reverse: bool = False) -> V_DL_OrderManip:
    """ Uses key to sort the video infos """
    def v_dl_order_manip(pos_infos: list[tuple[int, V_InfoDict]]):
        v_infos = [info[1] for info in pos_infos]
        return utils.sort_by_other(
            pos_infos,
            v_infos,
            key=lambda v_info: key(v_info),
            reverse=reverse)
    return v_dl_order_manip

def wrapper_match_filter_builder(
    max_extracts: float = 10,  # >= 0
    max_downloads: float = 10, # >= 0
    max_fails: float = 1,      # >= 1

    # if True, keep going through videos hitting all overrides
    quit_when_maxed: bool = True,

    download_match: Callable[[V_InfoDict], bool] = lambda v_info: (v_info.get('view_count') or 0) < 1_000_000,
    extract_match: Callable[[V_InfoDict], bool]|None = None,

    overrides: dict[DL_Action, Iterable[V_ID]] | None = None,

    # will always quit if a 403 happens in the current session, unless set to 0.
    # does this belong in PlaylistDL_Config?
    http_403_backoff_time: int = 3 * 24 * 3600,
    fail_backoff_time: int = 7 * 24 * 3600,
    ignore_ambiguous_dl_errors: bool = True,

    yt_unavailable_action: DL_Action | None = DL_Action.DOWNLOAD,

    debug: bool = False,
):
    """ If `extract_match` is None (default), then it is the opposite of `download_match` """

    if overrides is None:
        overrides = {}
    if extract_match is None:
        extract_match = lambda pl_v_info: not download_match(pl_v_info)

    if max_downloads < 0:   raise ValueError(f"max_downloads must be >= 0 (got: {max_downloads})")
    if max_extracts < 0:    raise ValueError(f"max_extracts must be >= 0 (got: {max_extracts})")
    if max_fails < 1:       raise ValueError(f"max_fails must be >= 1 (got: {max_fails})")

    if max_downloads == max_extracts == 0:
        utils.WARNING("max_downloads and max_extracts are 0, only overrides will be used.")

    if http_403_backoff_time < 0: raise ValueError("Use 0 to indicate no backoff time.")
    if fail_backoff_time < 0: raise ValueError("Use 0 to indicate no backoff time.")

    _print = lambda *args, **kwargs: print(*args, **kwargs) if debug else \
             lambda *args, **kwargs: None

    def dl_info_had_http_403_error(dl_info: DownloadInfo):
        for err in dl_info.get('errors', []):
            if yt_utils.interpret_error_msg(str(err)) == ('http_403', False):
                return True
        return False

    def pl_dl_info_had_http_403_error(pl_dl_info: PL_DownloadInfo) -> bool:
        return any(dl_info_had_http_403_error(dl_info) for dl_info in pl_dl_info)
    
    _checked_http_403_backoff = False
    def latest_http_403_error_epoch(history: PL_DownloadHistory) -> float:
        """ `float('-inf')` means http_403 was not found """
        # TODO: This should be a function/property of PlaylistDL
        res = float('-inf')
        for readable_epoch, pl_dl_info in history.items():
            if pl_dl_info_had_http_403_error(pl_dl_info):
                epoch = yt_utils.from_readable_epoch(readable_epoch)
                res = epoch if res is None else max(res, epoch)
        return res

    def should_backoff(timestamp: float, backoff_time: float) -> bool:
        elapsed = utils.epoch_now() - timestamp
        return backoff_time >= elapsed

    def wrapper_match_filter(
        pl_v_info: V_InfoDict,
        curr_pl_dl_info: PL_DownloadInfo,
        history: PL_DownloadHistory,
        history_ids: ID_DownloadInfo,
        ytdlp: YT_DLP_DownloadArchive,
        ytdlp_ids: YT_DLP_DownloadArchive_IDs,
    ) -> DL_Action:
        
        nonlocal _checked_http_403_backoff, _print

        if http_403_backoff_time > 0:
            if not _checked_http_403_backoff:    
                _checked_http_403_backoff = True # checked once on first pass

                latest_http_403 = latest_http_403_error_epoch(history)
                time_since_latest_403 = utils.epoch_now() - latest_http_403
                if should_backoff(latest_http_403, http_403_backoff_time):
                    _print(utils.hex(
                        f"[403] HTTP 403 in history at "
                        f"{yt_utils.to_readable_epoch(int(latest_http_403))} "
                        f"({time_since_latest_403:,}s ago, backoff={http_403_backoff_time:,}s) -> QUIT",
                        fg=DEBUG_FG['403']))
                    return DL_Action.QUIT
            
            # new dl_info's are appended to the end of curr_dl_info 
            if curr_pl_dl_info and dl_info_had_http_403_error(curr_pl_dl_info[-1]):
                _print(utils.hex(
                    "[403] HTTP 403 in current session -> QUIT",
                    fg=DEBUG_FG['403']))
                return DL_Action.QUIT
        
        curr_pl_dl_ids = yt_utils.ids_from_pl_download_info(curr_pl_dl_info)

        DL_IS_MAXED =   len(curr_pl_dl_ids['download']) >= max_downloads
        EXT_IS_MAXED =  len(curr_pl_dl_ids['extract']) >= max_extracts
        FAIL_IS_MAXED = len(curr_pl_dl_ids['fail']) >= max_fails

        if quit_when_maxed:
            if DL_IS_MAXED and max_downloads != 0:
                _print(utils.hex(
                    f"[MAX] downloads {len(curr_pl_dl_ids['download'])}/{max_downloads} -> QUIT",
                    fg=DEBUG_FG['MAX']))
                return DL_Action.QUIT
            if EXT_IS_MAXED and max_extracts != 0:
                _print(utils.hex(
                    f"[MAX] extracts {len(curr_pl_dl_ids['extract'])}/{max_extracts} -> QUIT",
                    fg=DEBUG_FG['MAX']))
                return DL_Action.QUIT
            if FAIL_IS_MAXED:
                _print(utils.hex(
                    f"[MAX] fails {len(curr_pl_dl_ids['fail'])}/{max_fails} -> QUIT",
                    fg=DEBUG_FG['MAX']))
                return DL_Action.QUIT

        v_id = pl_v_info['id']
        likely_unavailable = pl_v_info.get('view_count') in (0, None)

        # A v_id should only appear in once among all overrides
        # On ties, see DL_Action definition for order (iteration is top to bottom)
        for action in DL_Action:
            if v_id in overrides.get(action, []):
                _print(utils.hex(
                    f"[OVERRIDE] {v_id} -> {action.name}",
                    fg=DEBUG_FG['OVERRIDE']))
                return action

        # Skip if failed and still in the backoff time
        # Applies to both download and extract
        yt_err = None
        wa_err = None
        for epoch in history:
            if yt_utils.from_readable_epoch(epoch) < (utils.epoch_now() - fail_backoff_time):
                continue
            for dl_info in history[epoch]:
                if dl_info['id'] != v_id or dl_info['result'] != DL_Result.FAIL:
                    continue

                if not ignore_ambiguous_dl_errors:
                    _print(utils.hex(
                        f"[FAIL] prior failure at {epoch!r} (ambiguous, not ignored): "
                        f"{dl_info.get('errors')} -> SKIP",
                        fg=DEBUG_FG['FAIL']))
                    return DL_Action.SKIP

                for e in dl_info.get('errors', []):
                    ident, _is_ie = yt_utils.interpret_error_msg(str(e))
                    match ident:
                        case 'youtube': yt_err = (epoch, str(e))
                        case 'web.archive:youtube': wa_err = (epoch, str(e))
                if yt_err and wa_err:
                    _print(utils.hex(
                        f"[FAIL] found errors for yt and web.archive -> SKIP\n"
                        f"       yt: {yt_err}\n"
                        f"       wa: {wa_err}",
                        fg=DEBUG_FG['FAIL']))
                    return DL_Action.SKIP


        # if a v_info could be downloaded or extracted,
        # download takes priority
        # unavailable ignores maxes

        ALREADY_DL = v_id in history_ids['download'] or v_id in ytdlp_ids
        ALREADY_EXT = v_id in history_ids['extract']
        candidates = (
            (DL_Action.DOWNLOAD, ALREADY_DL, DL_IS_MAXED, download_match),
            (DL_Action.EXTRACT, ALREADY_EXT, EXT_IS_MAXED, extract_match),
        )

        skip_reasons = []
        def _flush_skip_reasons():
            if skip_reasons:
                _print(utils.hex(
                    f"[SKIP] {v_id}: " + "; ".join(skip_reasons),
                    fg=DEBUG_FG['SKIP_REASON']))
        for action, already_done, is_maxed, match_fn in candidates:
            tag = action.name

            if already_done:
                skip_reasons.append(f"{tag} already done")
                continue
            if is_maxed:
                skip_reasons.append(f"{tag} maxed")
                continue

            if yt_unavailable_action == action and likely_unavailable:
                _flush_skip_reasons()
                _print(utils.hex(
                    f"[{action.name}] view_count={pl_v_info.get('view_count')!r} (likely unavailable) -> {action.name}",
                    fg=DEBUG_FG[action.name]))
                return action

            if match_fn(pl_v_info):
                _flush_skip_reasons()
                if hasattr(match_fn, '__name__') and match_fn.__name__ != '<lambda>':
                    _match_fn_name = match_fn.__name__
                else:
                    _match_fn_name = f'<{tag.lower()} match_fn>'
                _print(utils.hex(
                    f"[{action.name}] matched {_match_fn_name}",
                    fg=DEBUG_FG[action.name]))
                return action
            
            skip_reasons.append(f"{tag} no match")

        _flush_skip_reasons()
        return DL_Action.SKIP
    
    return wrapper_match_filter

default_wrapper_match_filter = wrapper_match_filter_builder()

def default_field_updater(info: V_InfoDict|dict, k: str, v: Any|type[NO_VALUE], is_latest: bool) -> bool:
    from pldl.post_processing import merge_updaters
    return merge_updaters.COMMON_UPDATER(info, k, v, is_latest)

def default_update_filter(k: str) -> bool:
    return k in {
        'title',
        'description', 'categories', 'tags',
        'uploader', 'uploader_id', 'channel', 'creators', 'creator',
        'release_year', 'modified_date', 'availability',
        'extractor',
    }

# 
# The main class
# 

class PlaylistDL:
    
    # Functions for __init__
    
    def __get_init_info(self) -> tuple[PL_InfoDict, bool]:
        """
        Returns (init_info, is_latest_flat_extract)

        Does not set anything
        """
        
        def extract_flat(id: str) -> PL_InfoDict:
            self.pre_yt_dlp_download()
            raw_flat_info = yt_utils.extract_flat_info(
                pl_url_or_id=id,
                opts={'cookiefile': self._config.cookie_file if self._config.cookies_for_pl else None})
            return raw_flat_info

        match self._config.ident_type:
            case Config_IdentType.PL_ID_OR_URL:
                return extract_flat(self._config.ident), True
            
            case Config_IdentType.PL_INFO_PATH:
                pl_info: PL_InfoDict = utils.json_load(self._config.ident)
                # TODO: This should require user confirmation.
                # The user picked a specific pl_info, they should be told if it wont be used.
                if self._need_refresh(yt_utils.get_epoch(pl_info)):
                    return extract_flat(pl_info['id']), True
                return pl_info, False
            
            case Config_IdentType.METADATA_PATH:
                metadata: Metadata = utils.json_load(self._config.ident)
                _merge_flat_pointer: pldl_types.MetadataPointer|None = metadata['pointers'].get('_merge_flat', None)
                if _merge_flat_pointer is not None:
                    rel_path, epoch = _merge_flat_pointer
                    if not self._need_refresh(epoch):
                        info: PL_InfoDict = utils.json_load(os.path.join(self._config.home, rel_path))
                        return info, False
                return extract_flat(metadata['id']), True
            
            case _:
                raise ValueError(f"Invalid playlist ident_type: {self._config.ident_type}")
                

    @staticmethod
    def get_pl_outtmpls(Home: str, outtmpls: CustomOuttmpl, pl_info: PL_InfoDict) -> Abs_PL_Resolved_CustomOuttmpl:
        """
        Create paths starting from config.home, with resolved Playlist segment.

        Returns:
            tuple[YT_DLP_Params, RequiredPaths]:
            - `paths`, `outtmpl`, and `download_path` Params
            - `RequiredPaths` are all absolute paths
        
        Defaults from `DEFAULT_OUTTMPL`, `OUTTMPL_TYPES` (in yt_dlp/utils/_utils.py)    
        field_reference: https://github.com/yt-dlp/yt-dlp#output-template
        """

        if callable(outtmpls['Playlist']):
            Playlist = outtmpls['Playlist'](pl_info)
        else:
            Playlist = yt_utils.ytdlp_eval_tmpl(outtmpls['Playlist'], pl_info)
        
        # download_archive is in the Playlist folder.
        pl_outtmpls: Abs_PL_Resolved_CustomOuttmpl = {
            **{k: os.path.join(Home, Playlist, p) for k, p in outtmpls.items() if isinstance(p, str)},
            'Playlist': os.path.join(Home, Playlist),
        } # type: ignore

        return pl_outtmpls

    @staticmethod
    def create_path_opts(home: str, pl_outtmpls: Abs_PL_Resolved_CustomOuttmpl) -> YT_DLP_Params:

        opt_outpaths: YT_DLP_Params = {
            'paths': {'home': home}, # type: ignore - Home directory of all outtmpl (there's also `temp`)
            'outtmpl': {
                'default': os.path.relpath(pl_outtmpls['video_file'], home),
                # infojsons and metadata are custom
            },
            'download_archive': pl_outtmpls['yt_dlp_archive'],
        }
        for k in PL_Resolved_CustomOuttmpl.__optional_keys__:
            if k in pl_outtmpls:
                opt_outpaths['outtmpl'][k] = os.path.relpath(pl_outtmpls[k], home) # type: ignore - 'outtmpl' is defined as a dict.

        return opt_outpaths

    @staticmethod
    def _load_or_make_metadata(pl_id: str, config: PlaylistDL_Config, pl_outtmpls: Abs_PL_Resolved_CustomOuttmpl) -> Metadata:
        curr_meta_paths: Rel_PL_Resolved_CustomOuttmpl = {
            k: os.path.relpath(p, config.home) # type: ignore - all values are strs
            for k, p in pl_outtmpls.items()}
        metadata: Metadata|None = utils.json_load(pl_outtmpls['metadata'], default=None)
        return (
            metadata or \
            init_metadata(
                id=pl_id,
                path_tmpls=curr_meta_paths,
            ))

    @staticmethod
    def _validate_metadata_config_sync(metadata: Metadata, config: PlaylistDL_Config, playlist_path: str|None = None):
        """ May raise KeyError, RuntimeError, or FileNotFoundError """

        if missing := utils.get_missing_typeddict_keys(metadata, Metadata): # type: ignore - Metadata is a TypedDict
            raise KeyError(f"Missing kvals: {missing}")

        for p_key in pldl_types.MetadataPointers.__optional_keys__:
            if metadata['pointers'].get(p_key) is None:
                continue

            rel_path, _epoch = metadata['pointers'][p_key]
            real_path = os.path.join(config.home, rel_path)
            utils.assert_file(real_path, f"{p_key} (metadata)", min_size=1)
        
        meta_path = os.path.join(config.home, metadata['path_tmpls'].get('Playlist', 'NA'), metadata['path_tmpls'].get('metadata', 'NA'))
        for k in metadata['path_tmpls'].keys() | config.path_tmpls.keys():

            if k not in metadata['path_tmpls']:
                raise KeyError(
                    f"Missing key in metadata: {{{k!r}: {config.path_tmpls[k]!r}}}\n"
                    f"Path: {meta_path}")
            if k not in config.path_tmpls:
                raise KeyError(
                    f"Extra key in metadata: {{{k!r}: {metadata['path_tmpls'][k]!r}}}\n"
                    f"Path: {meta_path}")
            
            if k == 'Playlist':
                if playlist_path is None:
                    # if the playlist has not been extracted yet
                    continue
                if metadata['path_tmpls'][k] != playlist_path:
                    raise KeyError(
                        f"`Playlist` was changed in outtmpl.\n"
                        f"metadata:  {metadata['path_tmpls'][k]}\n"
                        f"generated: {playlist_path}\n"
                        f"Path: {meta_path}")

            elif os.path.relpath(metadata['path_tmpls'][k], metadata['path_tmpls']['Playlist']) != config.path_tmpls[k]:
                raise KeyError(
                    f"Changed {k!r} in path_tmpls:\n"
                    f"metadata: {metadata['path_tmpls'][k]}\n"
                    f"config:   {config.path_tmpls[k]}\n"
                    f"Path: {meta_path}")

    @staticmethod
    def _load_yt_archive(p: str) -> YT_DLP_DownloadArchive:
        res = []
        if not os.path.exists(p):
            return res
        with open(p, 'r', encoding='utf-8') as f:
            for line_no, line in enumerate(f, start=1):
                if not line:
                    continue
                items = line.split()
                if len(items) != 2:
                    utils.WARNING(f"[yt_dlp archive] Unrecognized @ L{line_no}: {line}")
                    continue
                ie_key, v_id = items
                if not yt_utils.is_id_like(v_id, is_video=True):
                    utils.WARNING(f"[yt_dlp archive] Bad video id @ L{line_no}: {line}")
                    continue
                res.append( (ie_key, v_id) )
        return res

    @staticmethod
    def _validate_dl_archive_sync(
            yt_dlp_archive: YT_DLP_DownloadArchive,
            metadata: Metadata,
            yt_dlp_archive_path: str
    ):
        """ Updates metadata and yt_dlp_archive in-place if auto-fixed """

        hist_dl = set(yt_utils.ids_from_history(metadata['history'])['download'])
        ytdlp_dl = set(yt_utils.ids_from_yt_dlp_archive(yt_dlp_archive))

        if ytdlp_dl == hist_dl:
            return

        hist_missing = ytdlp_dl - hist_dl
        yt_dlp_missing = hist_dl - ytdlp_dl

        FIX_IE_KEY = 'pldl_sync_fix'

        now: READABLE_EPOCH_STR = yt_utils.to_readable_epoch(utils.epoch_now())
        hist_to_add: list[DownloadInfo] = [{
            'id': v_id,
            'title': None,
            'action': DL_Action.DOWNLOAD,
            'result': DL_Result.DOWNLOAD
        } for v_id in hist_missing]
        ytdlp_to_add: list[tuple[str, str]] = [(FIX_IE_KEY, v_id) for v_id in yt_dlp_missing]

        utils.WARNING(
            f"Detected download state mismatch:\n"
            f"yt_dlp-missing:  {utils.hex(yt_dlp_missing, fg=utils.WARN_COLOR)}\n"
            f"history-missing: {utils.hex(hist_missing,   fg=utils.WARN_COLOR)}")

        print(f"The following will be added to history[{now}]:")
        print(json.dumps(hist_to_add, indent=2, ensure_ascii=False, default=str))
        print()

        print(f"The following will be added to the yt-dlp archive ({yt_dlp_archive_path}):")
        print(''.join(f'{key} {v_id}\n' for key, v_id in ytdlp_to_add))
        print()
        print(f"yt-dlp will use {FIX_IE_KEY = }")
        
        if utils.input_string(['y', 'N'], 'Add missing downloads to both automatically? ') == 'N':
            raise RuntimeError("User chose to fix yt_dlp archive and metadata desync manually")

        metadata['history'].setdefault(now, []).extend(hist_to_add)
        with open(yt_dlp_archive_path, 'a') as f:
            for key, v_id in ytdlp_to_add:
                yt_dlp_archive.append((key, v_id))
                f.write(f'{key} {v_id}\n')


    def _update_merge_flat_with_pl_info(self, pl_info: PL_InfoDict, warn_no_init_merge: bool):
        init_merge_flat: PL_InfoDict|None
        if self._infos._merge_flat:
            init_merge_flat = self._infos._merge_flat.data
        else:
            if warn_no_init_merge:
                utils.WARNING("No init_merge_flat found")
            init_merge_flat = None

        self._infos._merge_flat = _InfosEntry(
            merge_infos.merge_pl_infos(
                [pl_info],
                [],
                merge_updaters.FLAT_MERGE_UPDATER,
                update_filter=default_update_filter,
                _init_merge_info=init_merge_flat),
            self._pl_outtmpls['_merged_flat_infojson'],
            is_written=False,
            metadata_key='_merge_flat')

    def _update_merge_flat_with_v_info(self, v_info: V_InfoDict):
        """ updates the keys in flat_info, adds v_timeline """

        # NONE can include errors, so add them anyway
        # if yt_utils.get_v_info_level(v_info) == V_InfoLevel.NONE:
        #     return
        
        v_id = v_info['id']
        merge_flat_info = self._infos._merge_flat.data

        index = next((i for i, entry in enumerate(merge_flat_info['entries']) if entry['id'] == v_id), None)
        if index is None:
            utils.WARNING(f"v_info {v_id} is not in _merge_flat")
            return
        init_v_info = None if index is None else merge_flat_info['entries'][index]

        new_v_info, new_v_timeline = merge_infos.merge_v_infos(
            [v_info],
            merge_updaters.FLAT_MERGE_UPDATER,
            default_update_filter,
            _init_v_info=init_v_info,
            _init_v_timeline=merge_flat_info.get('merge_timeline', {}).get(v_id, {}))
        if V_InfoLevel[new_v_info.get('info_level', V_InfoLevel.FLAT.name)] > V_InfoLevel.FLAT:
            new_v_info['info_level'] = V_InfoLevel.FLAT.name

        for epoch in list(new_v_timeline.keys()):
            # this is very fragile, but it'll work
            entry = new_v_timeline[epoch]
            if 'better_info' in entry and entry['better_info'] != 'NONE -> FLAT': entry.pop('better_info')
            if 'unavailable' in entry: entry.pop('unavailable')
            if not entry:
                new_v_timeline.pop(epoch)
        merge_flat_info['entries'][index] = new_v_info
        merge_flat_info.setdefault('merge_timeline', {})[v_id] = new_v_timeline

    # 
    # the init function
    # 

    def __setup(self):
        init_info, init_is_latest_flat = self.__get_init_info()
        
        self.id: str = init_info['id']
        self._pl_outtmpls = PlaylistDL.get_pl_outtmpls(self._config.home, self._config.path_tmpls, init_info)
        self.opts = self._config.opts | PlaylistDL.create_path_opts(self._config.home, self._pl_outtmpls)

        self._metadata = PlaylistDL._load_or_make_metadata(self.id, self._config, self._pl_outtmpls)
        PlaylistDL._validate_metadata_config_sync(self._metadata, self._config,
            os.path.relpath(self._pl_outtmpls['Playlist'], self._config.home))
        self._yt_dlp_archive = PlaylistDL._load_yt_archive(self._pl_outtmpls['yt_dlp_archive'])
        PlaylistDL._validate_dl_archive_sync(self._yt_dlp_archive, self._metadata, self._pl_outtmpls['yt_dlp_archive'])

        # initialize defaults for required self._infos

        self._infos.raw_v_infos = _InfosEntry([],
            self._pl_outtmpls['raw_video_infojson'],
            is_written=False, metadata_key=None)

        if not self._infos._merge_flat and (data := self.load('_merge_flat', None)):
            self._infos._merge_flat = _InfosEntry(
                data, self._pl_outtmpls['_merged_flat_infojson'],
                is_written=True, metadata_key='_merge_flat')

        if init_is_latest_flat:
            # also updates _merge_flat (correctly)
            self.add_raw_flat_info(
                yt_utils.copy_and_sanitize_info(init_info),
                self._config.write_raw_flat, warn_no_init_merge=False)
    
    def __init__(self, config: PlaylistDL_Config) -> None:
        # note: __close__ is not called if __init__ fails.

        self.session_start_epoch: int   = utils.epoch_now()
        self._config: PlaylistDL_Config = config

        # set in __setup()
        self.id: str
        self._pl_outtmpls: Abs_PL_Resolved_CustomOuttmpl
        self.opts: YT_DLP_Params
        self._metadata: Metadata
        self._yt_dlp_archive: YT_DLP_DownloadArchive
        self._infos = _Infos()

        # __init__ requires special handling because many critical properties are not available yet:
        # self._pl_outtmpls, self._metadata, self.infos.base_info.data
        self.__setup()

        # 
        # below this, any functions can be used.
        # 

        if self._infos.raw_flat is None and self._config.force_flat_extract:
            self.extract_flat_info()

    # 
    # API functions
    # 

    def pre_yt_dlp_download(self):
        if self._config._no_yt_dlp_downloads:
            raise No_YT_DLP_Downloads
        sleep_random_seconds(1, 2)

    def _need_refresh(self, epoch: float) -> bool:
        time_since = utils.epoch_now() - epoch
        return time_since > self._config.refresh_after

    @overload
    @staticmethod
    def get_v_ids(info_entry: _InfosEntry[PL_InfoDict]|PL_InfoDict) -> list[V_ID]: ...
    @overload
    @staticmethod
    def get_v_ids(info_entry: None) -> None: ...
    @staticmethod
    def get_v_ids(info_entry: _InfosEntry[PL_InfoDict]|PL_InfoDict|None) -> list[V_ID]|None:
        if not info_entry:
            return None
        if isinstance(info_entry, _InfosEntry):
            info_entry = info_entry.data
        return [entry['id'] for entry in info_entry['entries']]

    @overload
    @staticmethod
    def get_v_id_to_index(info_entry: _InfosEntry[PL_InfoDict]|PL_InfoDict) -> dict[V_ID, int]: ...
    @overload
    @staticmethod
    def get_v_id_to_index(info_entry: None) -> None: ...
    @staticmethod
    def get_v_id_to_index(info_entry: _InfosEntry[PL_InfoDict]|PL_InfoDict|None) -> dict[V_ID, int]|None:
        if not info_entry:
            return None
        if isinstance(info_entry, _InfosEntry):
            info_entry = info_entry.data
        return {entry['id']: i for i, entry in enumerate(info_entry['entries'])}

    @overload
    def get_filtered_data[T](self, info_entry: _InfosEntry[T]) -> T: ...
    @overload
    def get_filtered_data(self, info_entry: None) -> None: ...
    def get_filtered_data[T](self, info_entry: _InfosEntry[T]|None) -> T|None:
        if not info_entry:
            return None
        filtered_data = yt_utils.copy_and_sanitize_info(info_entry.data)
        self._config.filter_all_info(filtered_data)
        match info_entry.metadata_key:
            case 'latest_flat_info' | '_merge_flat':
                self._config.filter_flat_info(filtered_data) # type: ignore
            case 'latest_pl_info':
                self._config.filter_pl_info(filtered_data) # type: ignore
            case 'latest_merge_info':
                self._config.filter_merge_info(filtered_data) # type: ignore
        return filtered_data

    @staticmethod
    def reorder_keys(info, type: pldl_types._MetadataFiles_Lit | None):
        match type:
            case None:
                # workaround :sigh:
                if not isinstance(info, list): return
                for bulk in info:
                    if not isinstance(bulk, list): return
                    for v_info in bulk:
                        if not isinstance(v_info, dict): return
                        reorder_infodict_keys.reorder_v_infodict(v_info)
            case 'latest_flat_info' | "latest_pl_info":
                reorder_infodict_keys.reorder_pl_infodict(info)
            case '_merge_flat' | 'latest_merge_info':
                reorder_infodict_keys.reorder_merge_info(info)
            case _:
                utils.ERROR(f"Unknown type: {type}")

    # a set_info like write_info would be nice
    # it would remove the `if write and ...` boilerplate on each set
    # TODO: there should be a staticmethod version of this
    def write_info(
            self,
            info: _InfosEntry|None,
            collision_policy: utils.CollisionPolicies,
            alt_info: ANY_InfoDict|None = None,
            delete_prev: bool = False,
            _name: str = '',
            pl_outtmpl_override: str|None = None,
    ) -> tuple[str, int]|None:
        """
        Call with any info from `self._infos`. If the info.data is not a dict (raw_v_infos),
        including `alt_info = {'epoch': ...}` is recommended.
        """

        if alt_info is None:
            alt_info = {}
        if info is None:
            utils.ERROR("Info entry was not found")
            return None
        outtmpl: str|None = info.pl_outtmpl or pl_outtmpl_override
        ident = _name or info.metadata_key or outtmpl
        if delete_prev and not info.metadata_key:
            raise ValueError(f"Deleting the previous requires a metadata_key (for {ident})")
        if info.is_written == True and info.metadata_key != '_merge_flat':
            utils.WARNING(f"Already written. Skipping. (for {ident})")
            return None
        if outtmpl is None:
            raise ValueError(f"pl_outtmpl was not found (for {ident})")

        if not info.data or not utils.has_content(info.data):
            utils.WARNING(f"{info.metadata_key or _name} has no content. Not writing.")
            return None

        match info.metadata_key:
            case 'latest_pl_info' | 'latest_merge_info':
                epoch = yt_utils.get_latest_epoch(info.data)
                _dst = yt_utils.ytdlp_eval_tmpl(outtmpl, info.data, {'epoch': epoch} | alt_info)

            case '_merge_flat' | 'latest_flat_info':
                epoch = yt_utils.get_epoch(info.data)
                _dst = yt_utils.ytdlp_eval_tmpl(outtmpl, info.data, {'epoch': epoch} | alt_info)

            case _: 
                if isinstance(info.data, dict):
                    epoch = yt_utils.get_epoch(info.data)
                    _dst = yt_utils.ytdlp_eval_tmpl(outtmpl, info.data, {'epoch': epoch} | alt_info)
                else:
                    # raw_v_infos
                    epoch = max(yt_utils.get_epoch(v_info)
                        for v_infos in info.data
                            for v_info in v_infos)
                    _dst = yt_utils.ytdlp_eval_tmpl(outtmpl, {'epoch': epoch} | alt_info)

        to_write = self.get_filtered_data(info)
        PlaylistDL.reorder_keys(to_write, type=info.metadata_key)
        dst = utils.json_dump(to_write, _dst, collision_policy)
        if dst is None:
            # don't update because no write occurred
            return None
        dst = str(dst.absolute())

        info.is_written = True
        pointer = (os.path.relpath(dst, self._config.home), epoch)
        if info.metadata_key:
            prev_pointer = self._metadata['pointers'].get(info.metadata_key, ('', float('-inf')))
            newer_or_same = pointer[1] >= prev_pointer[1]

            if newer_or_same:
                self._metadata['pointers'][info.metadata_key] = pointer
                if delete_prev and prev_pointer[0]:
                    stale_path = os.path.join(self._config.home, prev_pointer[0])
                    if os.path.exists(stale_path) and not os.path.samefile(stale_path, dst):
                        os.unlink(stale_path)
                        print(utils.hex(f"Removed {ident or '\b'}: {stale_path}", fg="#ff60bd"))
            else:
                utils.WARNING(f"Not setting pointer for {ident} to new data because it is older than the current info")

        print(utils.hex(f"Wrote {ident or '\b'} to: {dst}", fg="#70eeff"))
        
        return pointer

    @staticmethod
    def write_info_debug(
            info: _InfosEntry|None,
            alt_info: ANY_InfoDict|None = None,
            on_collision: Literal['rm new', 'rm old', 'mov new', 'mov old'] = 'mov new',
            pl_outtmpl_override: str|None = None,
    ):
        if alt_info is None:
            alt_info = {}
        if info is None:
            utils.WARNING("info was None")
            return

        pl_outtmpl = info.pl_outtmpl or pl_outtmpl_override
        if pl_outtmpl is None:
            utils.WARNING(f"pl_outtmpl was not found (for {info.metadata_key})")
            return
        
        match info.metadata_key:
            case 'latest_pl_info' | 'latest_merge_info':
                epoch = yt_utils.get_latest_epoch(info.data)
                _dst = yt_utils.ytdlp_eval_tmpl(pl_outtmpl, info.data, {'epoch': epoch} | alt_info)

            case '_merge_flat' | 'latest_flat_info':
                epoch = yt_utils.get_epoch(info.data)
                _dst = yt_utils.ytdlp_eval_tmpl(pl_outtmpl, info.data, {'epoch': epoch} | alt_info)

            case _: # raw_v_infos
                if isinstance(info.data, dict):
                    epoch = yt_utils.get_epoch(info.data)
                    _dst = yt_utils.ytdlp_eval_tmpl(pl_outtmpl, info.data, {'epoch': epoch} | alt_info)
                else:
                    # can't use info.data to make path
                    epoch = yt_utils.get_epoch(alt_info)
                    _dst = yt_utils.ytdlp_eval_tmpl(pl_outtmpl, {'epoch': epoch} | alt_info)

        to_write = yt_utils.copy_and_sanitize_info(info.data)
        PlaylistDL.reorder_keys(to_write, type=info.metadata_key)
        dst = utils.json_dump(to_write, _dst, on_collision)
        print(utils.hex(f"Wrote {info.metadata_key or '\b'} to: {dst}", fg="#70eeff"))


    @overload
    def load(self, info_type: pldl_types._MetadataFiles_Lit, default: type[utils.RAISE_EXC] = utils.RAISE_EXC) -> PL_InfoDict: ...
    @overload
    def load[T](self, info_type: pldl_types._MetadataFiles_Lit, default: T) -> PL_InfoDict|T: ...
    def load[T](self, info_type: pldl_types._MetadataFiles_Lit, default: T|type[utils.RAISE_EXC] = utils.RAISE_EXC) -> PL_InfoDict|T:
        if info_type not in pldl_types.MetadataPointers.__optional_keys__:
            raise ValueError(f"Unknown {info_type = }")

        types: dict[pldl_types._MetadataFiles_Lit, _InfosEntry|None] = {
            '_merge_flat': self._infos._merge_flat,
            'latest_flat_info': self._infos.raw_flat,
            'latest_pl_info': None,
            'latest_merge_info': None,
        }
        pointer: tuple[str, int]|None = self._metadata['pointers'].get(info_type)
        entry = types[info_type]
        if entry is not None:
            utils.WARNING(f"{info_type} is already loaded. Returning a copy to the data.")
            return entry.data
        
        if not pointer:
            if default is utils.RAISE_EXC:
                raise FileNotFoundError(f"{info_type} is not written according to metadata")
            return default # type: ignore - utils.RAISE_EXC is dealt with
        path, _epoch = pointer
        return utils.json_load(os.path.join(self._config.home, path), default)

    # 
    # Handling raw infodicts
    # 

    def add_raw_flat_info(self, raw_flat_info: PL_InfoDict, write: bool, warn_no_init_merge: bool = True):
        if self.id != raw_flat_info['id']:
            raise ValueError(f"Playlist ids do not match: {self.id} != {raw_flat_info['id']}")
        
        self._infos.raw_flat = _InfosEntry(
            raw_flat_info, self._pl_outtmpls['raw_flat_infojson'],
            is_written=False, metadata_key='latest_flat_info')

        # write raw info asap
        if write:
            self.write_info(self._infos.raw_flat, collision_policy='mov new', delete_prev=False)

        # update _merge_flat
        self._update_merge_flat_with_pl_info(raw_flat_info, warn_no_init_merge)

        return self._infos.raw_flat.data


    @staticmethod
    def flatten_raw_v_infos(raw_v_infos: list[V_InfoDict] | list[list[V_InfoDict]]) -> list[V_InfoDict]:
        if not isinstance(raw_v_infos, list):
            raise TypeError("Expected list[V_InfoDict] | list[list[V_InfoDict]]")
        if raw_v_infos and isinstance(raw_v_infos[0], list):
            # raw_v_infos: list[list[V_InfoDict]]
            return [v_info for _v_infos in raw_v_infos for v_info in _v_infos] # type: ignore 
        else:
            # raw_v_infos: list[V_InfoDict]
            return raw_v_infos # type: ignore
    
    def filter_for_in_playlist[T](self, infos: list[T], id_key: Callable[[T], V_ID], warn: bool = False) -> list[T]:
        v_ids = set(self.get_v_ids(self._infos._merge_flat))
        res = []
        for info in infos:
            v_id = id_key(info)
            if v_id not in v_ids:
                if warn: utils.WARNING(f"{v_id} is not in the playlist")
                continue
            res.append(info)
        return res

    @staticmethod
    def get_dl_info_from_v_info(v_info: V_InfoDict) -> DownloadInfo:
        dl_info: DownloadInfo = {
            'id': v_info['id'],
            'title': v_info.get('title'),
            # temp values
            'action': DL_Action.USER,
            'result': DL_Result.UNRECOGNIZED,
        }

        for unavail_msg in v_info.get('unavailable_msgs', []):
            if msg := unavail_msg['msg']:
                dl_info.setdefault('errors', []).append(msg)
        
        match yt_utils.derive_v_info_level(v_info):
            case V_InfoLevel.DOWNLOAD:
                dl_info['action'] = DL_Action.DOWNLOAD
                dl_info['result'] = DL_Result.DOWNLOAD
            case V_InfoLevel.EXTRACT:
                dl_info['action'] = DL_Action.EXTRACT
                dl_info['result'] = DL_Result.EXTRACT
            case V_InfoLevel.FLAT | V_InfoLevel.NONE:
                dl_info['action'] = DL_Action.DOWNLOAD # default for unknown DL_Action
                dl_info['result'] = DL_Result.FAIL

        return dl_info
        
    def _add_v_infos_to_archives(self, v_infos: list[V_InfoDict], pl_dl_info: PL_DownloadInfo|None, dl_info_filter: Callable[[DownloadInfo], bool]):
        # update metadata
        def dl_info_hash(dl_info: DownloadInfo) -> Hashable:
            return (
                dl_info['id'],
                dl_info['title'],
                dl_info['action'],
                dl_info['result'],
                tuple(dl_info.get('errors', [])),
            )

        latest_epoch = max((yt_utils.get_epoch(info) for info in v_infos), default=None) or utils.epoch_now()
        filtered_pl_dl_info = list(filter(
                dl_info_filter,
                pl_dl_info or map(self.get_dl_info_from_v_info, v_infos)))
        if filtered_pl_dl_info:
            epoch_key = yt_utils.to_readable_epoch(latest_epoch)
            curr_pl_dl_info = self._metadata['history'].setdefault(epoch_key, [])
            self._metadata['history'][epoch_key] = utils.dedup(
                curr_pl_dl_info + filtered_pl_dl_info, hash=dl_info_hash)
        
        # update yt_dlp_archive
        self._yt_dlp_archive = PlaylistDL._load_yt_archive(self._pl_outtmpls['yt_dlp_archive'])
        dl_keys = {
            ((v_info.get('extractor_key') or 'pldl_unknown_ie').lower(), v_info['id'])
            for v_info in v_infos if yt_utils.derive_v_info_level(v_info) == V_InfoLevel.DOWNLOAD}
        dl_keys_to_add = list(filter(lambda dl_key: dl_key not in self._yt_dlp_archive, dl_keys))
        if dl_keys_to_add:
            os.makedirs(os.path.dirname(self._pl_outtmpls['yt_dlp_archive']), exist_ok=True)
            with open(self._pl_outtmpls['yt_dlp_archive'], 'a') as f:
                for ie, v_id in dl_keys_to_add:
                    f.write(f'{ie} {v_id}\n')
                    self._yt_dlp_archive.append((ie, v_id))
            print(utils.hex(f"Added {len(dl_keys_to_add)} ids to yt_dlp_archive: {self._pl_outtmpls['yt_dlp_archive']}", fg="#637f86"))

    def add_raw_v_infos(
            self,
            raw_v_infos: list[V_InfoDict] | list[list[V_InfoDict]],
            write: bool,
            pl_dl_info: PL_DownloadInfo|None = None,
            dl_info_filter: Callable[[DownloadInfo], bool]|None = None,
            alt_info: ANY_InfoDict|None = None,
    ) -> list[V_InfoDict]:
        """
        Only adds v_infos whose id's are in the base_info playlist.
        Updates _infos.raw_v_infos, metadata['history'], and if necessary the yt_dlp_archive file
        Refreshes yt_dlp_archive dict
        Returns the `v_infos` that were added to `self._infos.raw_v_infos.data`,
        """
        if dl_info_filter is None:
            dl_info_filter = self._config.meta_dl_history_filter
        if alt_info is None:
            alt_info = {}
        v_infos = PlaylistDL.flatten_raw_v_infos(raw_v_infos)

        # only add v_infos that are currently in base_info playlist
        # to add ones that are not, their id (or fake id) should be added prior with playlist manipulation
        v_infos = self.filter_for_in_playlist(v_infos, id_key=lambda i: i['id'], warn=True)
        
        self._infos.raw_v_infos.data.append(v_infos)
        self._infos.raw_v_infos.is_written = False
        if write:
            self.write_info(self._infos.raw_v_infos, collision_policy='rm old', alt_info=alt_info, _name='raw_v_infos')
        for v_info in v_infos:
            self._update_merge_flat_with_v_info(v_info)

        self._add_v_infos_to_archives(v_infos, pl_dl_info, dl_info_filter)
        return v_infos

    # 
    # YT-DLP Extraction / Download + Helpers
    # 

    def extract_flat_info(self, write: bool|type[USE_CONFIG] = USE_CONFIG, cookiefile: bool|str|type[USE_CONFIG] = USE_CONFIG):
        """
        Use yt-dlp to extract flat playlist info.
        Params override respective configs (write_flat, cookie_file/cookies_for_pl).
        Updates `_infos.raw_flat` and `_infos._merge_flat`
        """
        self.pre_yt_dlp_download()
        raw_flat_info = yt_utils.extract_flat_info(pl_url_or_id=self.id,
            opts=self.opts | {
                'cookiefile': cookiefile if isinstance(cookiefile, str) else \
                              self._config.cookie_file if \
                                (cookiefile is USE_CONFIG and self._config.cookies_for_pl) or \
                                bool(cookiefile) else \
                              None,
                'download_archive': None}) # download flat info even if in yt-dlp archive
        self.add_raw_flat_info(raw_flat_info, bool(write) or (write is USE_CONFIG and self._config.write_raw_flat))
        return raw_flat_info

    
    @staticmethod
    def _get_dl_result(v_info, success: bool) -> DL_Result:
        if not success:
            return DL_Result.FAIL
        if v_info is None:
            return DL_Result.CACHED # None is returned if download cache or cancelled.
        
        match yt_utils.derive_v_info_level(v_info):
            case V_InfoLevel.DOWNLOAD: return DL_Result.DOWNLOAD
            case V_InfoLevel.EXTRACT:  return DL_Result.EXTRACT
            case _:
                return DL_Result.UNRECOGNIZED

    @staticmethod
    def _get_action_from_user(entry: V_InfoDict):
        DL_MAP_NO_USER = {str(action).lower(): action for action in DL_Action if action not in (DL_Action.USER, )}

        # TODO: show useful entry info for action choices
        print(f"[TEMP]:\n{json.dumps(yt_utils.copy_and_sanitize_info(entry), indent=4, default=str, ensure_ascii=False)}")

        choice = utils.input_string(
            list(DL_MAP_NO_USER.keys()),
            "Pick a Download Option: ",
            prefix_options=True,
        )
        return DL_MAP_NO_USER[choice]
    
    @staticmethod
    def _download_v_infos(
            pl_info: PL_InfoDict[V_InfoDict],
            wrapper_match_filter: Callable[[V_InfoDict, PL_DownloadInfo], DL_Action],
            opts: YT_DLP_Params|None,
            try_yt_even_if_unavailable: bool,
            wa: bool,
            order_manip: V_DL_OrderManip|None,
            sleep_interval: tuple[float, float],
    ) -> tuple[list[V_InfoDict], PL_DownloadInfo]:
        """
        Extract (and download) videos. Return the extracted v_infos and download_info

        Args:
            wrapper_match_filter (Callable[[PL_V_InfoDict, PL_DownloadInfo], DL_Action]|None, optional):
                Called before downloading the video. Is given current playlist download information.
                Returns a download action to control the current playlist download.
                Defaults to None; this will extract and download every video not in the yt-dlp download archive.
            opts (YT_DLP_Params, optional): Extra opts used by ``download_video()``. Defaults to {}.
            try_yt_even_if_unavailable (bool, optional): Try Youtube even if it seems unavailable. Defaults to True.
            wa (bool, optional): Use archive.org if YouTube failed (fallback). Defaults to True.
            order_manip (Callable[[Iterable], Iterable], optional): Change video iteration order. Defaults to in order.
        """
        if opts is None:
            opts = {}
        default_order = order_manip is None
        if default_order:
            order_manip = lambda x: x # no manipulation
        
        extracted_v_infos: list[V_InfoDict] = []
        pl_dl_info: PL_DownloadInfo = []

        def get_pl_v_display(entry_pos: int, entry: V_InfoDict):
            num_entries = len(pl_info['entries'])
            stable_pos = f"{entry_pos:{len(str(num_entries))}}"
            if default_order:
                i_of_N = f"{stable_pos}/{num_entries}"
                return f"[{i_of_N}] {yt_utils.get_v_display(entry)}"
            else:
                return f"[{stable_pos}] {yt_utils.get_v_display(entry)}"

        try:
            for entry_pos, v_info in order_manip(list(enumerate(pl_info['entries'], start=1))):                
                action = wrapper_match_filter(v_info, pl_dl_info)

                pl_v_display = get_pl_v_display(entry_pos, v_info)

                if action == DL_Action.USER:
                    # DL_Action.USER should not be the action in dl_info, so overwrite `action`
                    action = PlaylistDL._get_action_from_user(v_info)

                pl_dl_info.append({
                    'id': v_info['id'],
                    'title': v_info.get('title'),
                    'action': action,
                    'result': DL_Result.CANCELLED,
                })

                if action == DL_Action.QUIT:
                    print(display.ACTION_TAG[DL_Action.QUIT].rendered,
                          utils.hex(pl_v_display, display.ACTION_TAG[action].color))
                    break
                elif action == DL_Action.SKIP:
                    print(display.ACTION_TAG[action].rendered,
                          utils.hex(pl_v_display, display.ACTION_TAG[action].color))
                    continue

                print('\n'+
                      display.ACTION_TAG[action].rendered,
                      utils.hex(pl_v_display, display.ACTION_TAG[action].color))
                sleep_random_seconds(*sleep_interval)

                new_v_info, errors, success = yt_utils.download_video(
                    v_info['id'],
                    opts     = opts,
                    yt       = try_yt_even_if_unavailable or yt_utils._maybe_available_on_yt(v_info),
                    wa       = wa,
                    download = (action == DL_Action.DOWNLOAD))

                if new_v_info:
                    new_v_info.setdefault('id', v_info['id'])
                    new_v_info.setdefault('epoch', utils.epoch_now())
                    new_v_info.setdefault('info_level', V_InfoLevel.NONE.name) # adding custom tags is okay
                    extracted_v_infos.append(new_v_info)
                
                pl_dl_info[-1] = {
                    'id': v_info['id'],
                    'title': (new_v_info or {}).get('title') or v_info.get('title'),
                    'action': action,
                    'result': PlaylistDL._get_dl_result(new_v_info, success),
                }

                if errors:
                    pl_dl_info[-1]['errors'] = list(map(str, errors))

                if new_v_info:
                    # rebuild in case of more info (eg extracted title)
                    pl_v_display = get_pl_v_display(entry_pos, new_v_info)
                result_tag = display.download_result_tag(pl_dl_info[-1])
                print(result_tag.rendered, utils.hex(pl_v_display, result_tag.color) + '\n')

        except KeyboardInterrupt: # quit, but keep alive
            print(utils.hex("    KEYBOARD INTERRUPT    ", bg='#ffffff'))
        except Exception as e:  # noqa: BLE001 - keep alive
            print(utils.format_exception(e))
        
        return extracted_v_infos, pl_dl_info

    def download_v_infos(
            self,
            wrapper_match_filter: WrapperMatchFilter = default_wrapper_match_filter,
            order_manip: V_DL_OrderManip|None = None,
            write: bool|type[USE_CONFIG] = USE_CONFIG,
            cookiefile: bool|str|type[USE_CONFIG] = USE_CONFIG,
            opts: YT_DLP_Params|type[USE_CONFIG] = USE_CONFIG,
            try_yt_even_if_unavailable: bool = True,
            wa: bool = True,
    ):
        """ Returns the newly downloaded portion of the raw v_infos """
        self.pre_yt_dlp_download()

        history_ids = yt_utils.ids_from_history(self._metadata['history'])
        yt_dlp_archive_ids = yt_utils.ids_from_yt_dlp_archive(self._yt_dlp_archive)
        _opts: YT_DLP_Params = (
            self.opts if opts is USE_CONFIG else opts |
            {'cookiefile':  cookiefile if isinstance(cookiefile, str) else \
                            self._config.cookie_file if \
                                (cookiefile is USE_CONFIG and self._config.cookies_for_vids) or \
                                bool(cookiefile) else \
                            None}) # type: ignore - opts is never USE_CONFIG

    
        print("\n ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n"
                "  Downloading Playlist Videos \n"
                " ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n")

        v_infos, pl_dl_info = PlaylistDL._download_v_infos(
            self._infos._merge_flat.data,
            lambda pl_v_info, curr_pl_dl_info: wrapper_match_filter(
                pl_v_info, curr_pl_dl_info,
                self._metadata['history'], history_ids,
                self._yt_dlp_archive, yt_dlp_archive_ids),
            opts=_opts,
            try_yt_even_if_unavailable=try_yt_even_if_unavailable,
            wa=wa,
            order_manip=order_manip,
            sleep_interval=(
                self._config.opts.get('sleep_interval') or 0.2,
                self._config.opts.get('max_sleep_interval') or 1))

        write_v_infos = bool(write) or (write is USE_CONFIG and self._config.write_raw_v_infos)
        self.add_raw_v_infos(v_infos, write_v_infos, pl_dl_info, alt_info={'epoch': self.session_start_epoch})

        print(display.pl_download_info(pl_dl_info, errors=True, header=True), end="\n\n")
        return v_infos, pl_dl_info


    @staticmethod
    def _download_v_info_generic(v_id: str, any_yt_dlp_url: str, opts: YT_DLP_Params, download: bool) -> tuple[V_InfoDict|None, DownloadInfo]:
        raw_epoch = utils.epoch_now()

        dl_info: DownloadInfo = {
            'id': v_id,
            'title': None,
            'action': DL_Action.DOWNLOAD if download else DL_Action.EXTRACT,
            'result': DL_Result.DOWNLOAD if download else DL_Result.EXTRACT,
        }

        print('\n'+
              utils.hex("<GENERIC>", fg="#CDFCFF"),
              display.ACTION_TAG[dl_info['action']].rendered,
              utils.hex(v_id, display.ACTION_TAG[dl_info['action']].color))
        v_info, error, success = yt_utils.download_video_generic(any_yt_dlp_url, opts, download=download)

        if error:
            dl_info['errors'] = [str(error)]
        if not success:
            dl_info['result'] = DL_Result.FAIL

        if v_info:
            v_info['id'] = v_id
            v_info.setdefault('epoch', raw_epoch)
            dl_info['title'] = v_info.get('title')
        
        print(utils.hex("<GENERIC>", fg="#CDFCFF"),
              display.download_info(dl_info, errors=True)+
              '\n')
        return v_info, dl_info

    def download_v_info_generic(
            self,
            v_id: str,
            any_yt_dlp_url: str,
            download: bool,
            opts: YT_DLP_Params|None = None,
            write: bool = True,
            cookiefile: bool|str = False,
    ) -> tuple[V_InfoDict, DownloadInfo] | tuple[None, DownloadInfo]:
        """
        Only video downloads are added to metadata history.
        Added to raw_v_infos if DownloadError or there is a result.
        Normal Exceptions are just printed.

        Returns what was received from yt_dlp
        """
        self.pre_yt_dlp_download()

        if opts is None:
            opts = {}

        if v_id not in self.get_v_ids(self._infos._merge_flat):
            raise ValueError(f"{v_id} is not in the loaded playlist")
        
        v_info, dl_info = PlaylistDL._download_v_info_generic(
            v_id,
            any_yt_dlp_url,
            self.opts | opts | {
                'cookiefile': cookiefile if isinstance(cookiefile, str) else \
                              self._config.cookie_file if cookiefile else \
                              None},
            download)
        
        if v_info is None:
            return None, dl_info

        self.add_raw_v_infos([v_info], write, [dl_info], alt_info={'epoch': self.session_start_epoch})
        return v_info, dl_info

    # 
    # Merge raw data
    # 

    @staticmethod
    def _make_pl_info(
            base_pl_info: PL_InfoDict,
            raw_v_infos: list[V_InfoDict],
            field_updater: merge_updaters.MergeFieldUpdater,
    ):
        pl_info: PL_InfoDict = yt_utils.copy_and_sanitize_info(base_pl_info)

        if not raw_v_infos:
            return pl_info

        merge_info = merge_infos.merge_pl_infos([base_pl_info], raw_v_infos, field_updater, lambda _: False)
        merge_info.pop('merge_timeline', None) # turn it back into pl_info
        merge_info['info_level'] = yt_utils.derive_pl_info_level(merge_info).name # should be 'NORMAL'
        return merge_info
    
    def make_pl_info(
            self,
            write: bool,
            delete_prev: bool = False,
            field_updater: merge_updaters.MergeFieldUpdater = default_field_updater,
    ) -> _InfosEntry[PL_InfoDict]:
        """
        Create pl_info from `base_info` and `raw_v_infos`.
        
        Videos with ids not in `base_info`, will be skipped.
        Only keeps the most recent v_info.
        Prefers raw_v_info over base_info.

        Returned object is also stored in `self._infos.pl_info.data`
        """
        if not utils.has_content(self._infos.raw_v_infos.data):
            utils.WARNING("No raw_v_infos were found. Raw video infos can be added with " \
                          "download_v_infos(), download_v_info_generic(), or add_raw_v_infos().")
        
        pl_info = self._make_pl_info(
            self._infos._merge_flat.data,
            [v_info for v_infos in self._infos.raw_v_infos.data for v_info in v_infos],
            field_updater)
        

        pl_info_entry = _InfosEntry(
            pl_info, self._pl_outtmpls['pl_infojson'],
            is_written=False, metadata_key='latest_pl_info')
        
        if write:
            self.write_info(pl_info_entry, collision_policy='mov new',
                alt_info={'epoch': yt_utils.get_latest_epoch(pl_info)}, delete_prev=delete_prev)
        return pl_info_entry


    @staticmethod
    def _make_merge_info(
            prev_merge_info: PL_InfoDict|None,
            pl_infos: list[PL_InfoDict],
            v_infos: list[V_InfoDict],
            field_updater: merge_updaters.MergeFieldUpdater,
            update_filter: Callable[[str], bool],
    ) -> PL_InfoDict:
        return merge_infos.merge_pl_infos(pl_infos, v_infos, field_updater, update_filter, prev_merge_info)

    def make_merge_info(
            self,
            write: bool,
            delete_prev: bool = False,
            field_updater: merge_updaters.MergeFieldUpdater = default_field_updater,
            update_filter: Callable[[str], bool]|list[str] = default_update_filter,
    ) -> _InfosEntry[PL_InfoDict]:
        """
        Creates merge info using `init_ident` and the current run's pl_info.
        Returns the created merge info entry.
        """

        merge_info = self._make_merge_info(
            self.load('latest_merge_info', None),
            [self._infos._merge_flat.data],
            PlaylistDL.flatten_raw_v_infos(self._infos.raw_v_infos.data),
            field_updater,
            (lambda k: k in update_filter) if isinstance(update_filter, list) else update_filter)

        merge_info_entry = _InfosEntry(
            merge_info, self._pl_outtmpls['merge_infojson'],
            is_written=False, metadata_key='latest_merge_info')
        
        if write:
            self.write_info(merge_info_entry, collision_policy='mov new',
                alt_info={'epoch': yt_utils.get_latest_epoch(merge_info)}, delete_prev=delete_prev)

        return merge_info_entry

    # 
    # Manipulation
    # Primarily effects base_info
    # Optionally mutate _merge_info for persistent changes
    # Does not update history or yt_dlp archive
    # Any new ids should be redownloaded/extracted from scratch
    #

    @staticmethod
    def _add_to_merge_timeline(info: PL_InfoDict, timeline: PL_MergeTimeline) -> None:
        """ Input timeline wins collisions """
        info.setdefault('merge_timeline', {})
        info['merge_timeline'] = utils.merge_objs(
            info.get('merge_timeline', {}),
            {'merge_timeline': timeline},
            make_copy=False)

    @staticmethod
    def _add_update_to_merge_timeline(info: PL_InfoDict, id: str, update_str: str, raw_epoch: int|None = None) -> None:
        """ Does not add if the update_str already exists. If epoch_str is None, use the current time """
        epoch = yt_utils.to_readable_epoch(int(raw_epoch) if raw_epoch is not None else utils.epoch_now())
        
        if update_str in info.get('merge_timeline', {}).get(id, {}).get(epoch, {}).get('updates', []):
            return
        info.setdefault('merge_timeline', {})
        info['merge_timeline'] = utils.merge_objs(
            info.get('merge_timeline', {}),
            {id: {epoch: {'update': update_str}}},
            make_copy=False)


    def _remove_video_impl(self, merge_index: int):
        """
        Removes video entry at given index and adds to merge_timeline

        Assumes validation is already done.
        Does NOT call fixup_pl_info - caller must call it after all operations.
        """
        removed_entry = self._infos._merge_flat.data['entries'].pop(merge_index)
        PlaylistDL._add_update_to_merge_timeline(
            self._infos._merge_flat.data, removed_entry['id'],
            update_str=f'<REMOVE {yt_utils.get_v_display(removed_entry)}>')

    def remove_video(self, v_id: V_ID):
        """ Remove a video from the playlist by its ID """

        merge_v_ids = PlaylistDL.get_v_ids(self._infos._merge_flat)

        if v_id not in merge_v_ids:
            utils.WARNING(f"{v_id} is not in the playlist.")
            return

        merge_index = merge_v_ids.index(v_id) if v_id in merge_v_ids else None
        
        if merge_index is not None:
            self._remove_video_impl(merge_index)
        yt_utils.fixup_pl_info(self._infos._merge_flat.data)

    def remove_videos(self, v_ids: Iterable[V_ID]):
        """Remove multiple videos from the playlist by their IDs.

        Videos are removed in reverse order (by position) to avoid index shifting issues.

        Args:
            v_ids: Video IDs to remove from the playlist.
        """
        merge_v_ids = PlaylistDL.get_v_ids(self._infos._merge_flat) or []

        # Find indices for all videos to remove
        merge_indexes: list[int] = []

        for v_id in set(v_ids):
            if merge_i := (merge_v_ids.index(v_id) if v_id in merge_v_ids else None):
                merge_indexes.append(merge_i)
            else:
                utils.WARNING(f"{v_id} is not in the playlist.")

        # Sort by base_index descending to avoid index shifting issues
        merge_indexes = list(set(merge_indexes))
        merge_indexes.sort(reverse=True)

        for merge_i in merge_indexes:
            self._remove_video_impl(merge_i)
        
        yt_utils.fixup_pl_info(self._infos._merge_flat.data)


    def _insert_video_impl(self, v_id: V_ID, index: int):
        """
        Insert a video at given index.

        Assumes validation is already done.
        Does NOT call fixup_pl_info - caller must call it after all operations.
        """
        new_v_info = yt_utils.min_v_info(v_id, V_InfoLevel.NONE)

        self._infos._merge_flat.data['entries'].insert(index, copy.deepcopy(new_v_info))
        PlaylistDL._add_update_to_merge_timeline(
            self._infos._merge_flat.data, v_id,
            update_str=f'<INSERT to={index+1}>')

    def insert_video(self, v_id: V_ID, position: int = 1):
        """
        Inserts a new video into the playlist at the specified position.

        By default adds to the start of the playlist (like YouTube).
        Like list.insert(), position can be negative and going out of bounds is
        clamped to the ends of the list.

        Position Behavior:

                 _ A _ B _ C _ D _
                 1   2   3   4   5 ...
            ... -5  -4  -3  -2  -1

        Args:
            v_id: Video ID to insert.
            position: Target position. Clamped to valid range. Can be negative. `0` is invalid.
                Defaults to 1 (start of playlist).
        """
        merge_v_ids = PlaylistDL.get_v_ids(self._infos._merge_flat) or []

        if v_id in merge_v_ids:
            raise ValueError(f"{v_id} is already in the playlist")

        index = utils.position_to_index(position, len(merge_v_ids))
        self._insert_video_impl(v_id, index)

        yt_utils.fixup_pl_info(self._infos._merge_flat.data)

    def insert_videos(self, v_ids: Iterable[V_ID], position: int = 1, mutate_merge_flat: bool = True):
        """
        Insert multiple videos into the playlist at the specified position.

        Videos are inserted such that the first video in the iterable ends up at
        the target position, the second at position+1, etc. The order in the
        iterable is preserved in the final playlist.

        This is equivalent to calling insert_video repeatedly while incrementing
        the position each time.

        Position Behavior:

                 _ A _ B _ C _ D _
                 1   2   3   4   5 ...
            ... -5  -4  -3  -2  -1

        Args:
            v_ids: Video IDs to insert. Order is preserved.
            position: Target position for the first video. Clamped to valid range.
                Can be negative. `0` is invalid. Defaults to 1 (start of playlist).
        """
        merge_v_ids = PlaylistDL.get_v_ids(self._infos._merge_flat) or []

        # Convert to list to check for duplicates and allow multiple passes
        to_insert = list(v_ids)

        # Check for duplicates in input
        if len(to_insert) != len(set(to_insert)):
            duplicates = [x for x in set(to_insert) if to_insert.count(x) > 1]
            raise ValueError(
                f"All ids must be unique.\n"
                f"Duplicates: {sorted(duplicates)}")

        # Check for conflicts with existing videos
        if conflicts := [v_id for v_id in to_insert if v_id in merge_v_ids]:
            raise ValueError(f"All ids must be new.\n"
                             f"Conflicts: {conflicts}")

        for offset, v_id in enumerate(to_insert):
            index = utils.position_to_index(position+offset, len(merge_v_ids) + offset)
            self._insert_video_impl(v_id, index)

        yt_utils.fixup_pl_info(self._infos._merge_flat.data)


    # TODO: Should update metadata in some way? That would also require updating how history is handled though...
    def _replace_video_impl(self, merge_index: int, v_id: V_ID, repl: V_ID):
        """
        Replace a video ID at given indices.

        Assumes validation is already done.
        Does NOT call fixup_pl_info - caller must call it after all operations.
        """

        self._infos._merge_flat.data['entries'][merge_index]['id'] = repl

        # Make it doubly linked
        PlaylistDL._add_update_to_merge_timeline(
            self._infos._merge_flat.data, v_id,
            update_str=f'<REPLACE ID from={v_id} to={repl}>')
        PlaylistDL._add_update_to_merge_timeline(
            self._infos._merge_flat.data, repl,
            update_str=f'<REPLACE ID from={v_id} to={repl}>')

    def replace_video(self, v_id: V_ID, repl: V_ID, mutate_merge_flat: bool = True):
        """Replace a video ID with a new ID while keeping the same position.

        Args:
            v_id: The target video ID to replace.
            repl: The replacement video ID.
        """
        merge_v_ids = PlaylistDL.get_v_ids(self._infos._merge_flat) or []

        if v_id not in merge_v_ids:
            raise ValueError(f"The target id {v_id} is not in the playlist.")

        merge_index = merge_v_ids.index(v_id)
        if merge_index is not None and repl in merge_v_ids:
            raise ValueError(f"Replacement id {repl} is already in the '_merge_flat' playlist")

        self._replace_video_impl(merge_index, v_id, repl)

        yt_utils.fixup_pl_info(self._infos._merge_flat.data)

    def replace_videos(self, replacements: Iterable[tuple[V_ID, V_ID]]):
        """Replace multiple video IDs with new IDs while keeping the same positions.

        Performs a two-pass validation:
        1. Check all targets exist in the playlist
        2. Check for conflicts: a replacement ID is either already in the playlist,
           or is used as a target in a later replacement

        The replacements are processed in order, so the order of the iterable matters.

        Args:
            replacements: Iterable of (target_id, replacement_id) tuples.
                Processed in order - a replacement_id can become a target in a
                later replacement in the same iterable.
        """
        replacements_list = list(replacements)

        merge_v_ids = PlaylistDL.get_v_ids(self._infos._merge_flat) or []

        # Simulate replacements to check for conflicts
        def validate(sim_list: list[str]):
            """ mutates passed in list """
            failed_ops: list[tuple[int, tuple[V_ID, V_ID]]] = []
            for i, (target, repl) in enumerate(replacements_list):
                if target not in sim_list:
                    raise ValueError(
                        f"Bulk Replacement index={i}\n"
                        f"Target id {target} is not in _merge_flat."
                        f"current: {sim_list}")
                target_index = sim_list.index(target)
                if repl in sim_list:
                    raise ValueError(
                        f"Bulk Replacement index={i}\n"
                        f"Replacement id {repl} is already in _merge_flat "
                        f"at position {sim_list.index(repl) + 1} "
                        f"(target {target} is at position {target_index + 1})\n"
                        f"current: {sim_list}")
                sim_list[target_index] = repl
            return failed_ops

        validate(list(merge_v_ids)) # use copy of merge_v_ids

        # Execute all replacements
        for target, repl in replacements_list:
            merge_index = merge_v_ids.index(target)
            self._replace_video_impl(merge_index, target, repl)
            # Update v_ids for next iteration
            if merge_index is not None:
                merge_v_ids[merge_index] = repl

        yt_utils.fixup_pl_info(self._infos._merge_flat.data)


    def move_video(self, v_id: V_ID, position: int):
        """Move a video to a new position in the playlist.

        Position Behavior:

                 _ A _ B _ C _ D _
                 1   2   3   4   5 ...
            ... -5  -4  -3  -2  -1
        
        Args:
            v_id: Video ID to move.
            position: Target position. Clamped to valid range. Can be negative. `0` is invalid.
        """

        merge_v_ids = PlaylistDL.get_v_ids(self._infos._merge_flat) or []

        if v_id not in merge_v_ids:
            raise ValueError(f"The target id {v_id} is not in the playlist.")

        index = utils.position_to_index(position, len(merge_v_ids)-1) # The -1 fixes removing first
        old_index = merge_v_ids.index(v_id)
        if index == old_index:
            # no need to warn
            # utils.WARNING(f"ove {v_id} to its current position ({position})")
            return

        # Removing then adding works better than adding then removing duplicate.
        entry = self._infos._merge_flat.data['entries'].pop(old_index)
        self._infos._merge_flat.data['entries'].insert(index, entry)
        yt_utils.fixup_pl_info(self._infos._merge_flat.data)
        PlaylistDL._add_update_to_merge_timeline(
            self._infos._merge_flat.data, v_id,
            update_str=f'<MOVE from={old_index+1} to={index+1}>')

    # 
    # Display
    # 

    def display_metadata_history(self, include_urls: bool = True, info: _InfosEntry[PL_InfoDict]|PL_InfoDict|None = None):
        if info is None:
            info = self._infos._merge_flat.data
        if isinstance(info, _InfosEntry):
            info = info.data
        
        print("\n ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n"
                "  Playlist Metadata History \n"
                " ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n")
        display.metadata_history(self._metadata['history'], info, PlaylistDL.get_v_ids(info), include_urls)
        print()

    @staticmethod
    def display_pl_merge_timeline(info: _InfosEntry[PL_InfoDict]|PL_InfoDict|None, include_urls: bool = True):
        if info is None:
            # allow None for caller's convenience
            utils.WARNING("Info is None")
            return
        if isinstance(info, _InfosEntry):
            info = info.data

        print("\n ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n"
                "  Playlist Merge Timeline \n"
                " ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n")
        display.pl_merge_timeline(info, PlaylistDL.get_v_ids(info), include_urls, warn_not_found=True)
        print()

    # 
    # Cleanup
    # 

    def write_merge_flat(self):
        self.write_info(self._infos._merge_flat, collision_policy='rm old', delete_prev=True)

    def write_metadata_file(self):
        reorder_infodict_keys.reorder_by_readable_epoch(self._metadata['history'])
        utils.json_dump(self._metadata, self._pl_outtmpls['metadata'], on_collision='rm old')
        print(utils.hex(f"Updated metadata: {self._pl_outtmpls['metadata']}", fg="#637f86"))

    def empty_cookies(self):
        if self._config.cookie_file and os.path.exists(self._config.cookie_file):
            with open(self._config.cookie_file, 'w'):
                ...
            print(utils.hex(f"Emptied cookie file: {self._config.cookie_file}", fg="#ff60bd"))

    def close(self):
        if self._config.empty_cookies:
            self.empty_cookies()
        self.write_merge_flat()
        
        self.write_metadata_file() # should be LAST

    def __enter__(self):
        # everything is handled by __init__()
        return self
    
    def __exit__(self, *args):
        self.close()
