__all__ = ['PlaylistDL']

import copy
import dataclasses
import itertools
import json
import os
import random
import time
from collections.abc import Callable, Hashable, Iterable
from typing import Literal, overload

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
    
    # FUTURE: base_info and _merge_flat serve the same purpose
    # only _merge_flat should have been used.
    # Having 2 sources of truth was an unnecessary complexity.
    # Ignoring videos should have been done via params of functions
    # that iterate through the videos.
    base_info:   _InfosEntry[PL_InfoDict] = None # type: ignore - set in init
    raw_flat:    _InfosEntry[PL_InfoDict] | None = None
    raw_v_infos: _InfosEntry[list[list[V_InfoDict]]] = None # type: ignore - set in init

    _merge_flat: _InfosEntry[PL_InfoDict] | None = None
    pl_info:     _InfosEntry[PL_InfoDict] | None = None
    merge_info:  _InfosEntry[PL_InfoDict] | None = None


def init_metadata(
        id: str,
        path_tmpls: Rel_PL_Resolved_CustomOuttmpl,
        history: PL_DownloadHistory|None = None,
        pointers: pldl_types._MetadataPointers|None = None
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
                preference_order: list[pldl_types._MetadataFiles_Lit] = [
                    '_merge_flat', 'latest_flat_info', 'latest_pl_info', 'latest_merge_info'
                ]
                pointers: list[tuple[str, int]|None] = [metadata['pointers'].get(k) for k in preference_order]
                for p in pointers:
                    if p is not None and not self._need_refresh(p[1]):
                        info: PL_InfoDict = utils.json_load(os.path.join(self._config.home, p[0]))
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

        for p_key in pldl_types._MetadataPointers.__optional_keys__:
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


    def __get_base_info_data(self, init_info: PL_InfoDict, init_is_latest_flat: bool) -> PL_InfoDict:
        # At this point no self._infos are initialized.

        # _init_info does not need a refresh. (see _get_init_info())
        # Assume init is written - if it was extracted, then it is already in raw_flat.
        if self._config.ident_type == Config_IdentType.PL_INFO_PATH \
           and self._config.base_info_type != 'any':
            utils.WARNING(
                f"The passed in info will only be used for metadata identification."
                f"To load using a specific infojson set: "
                f"{utils.hex("config.base_info_type = 'any'", fg=utils.WARN_COLOR)}")

        # don't warn if different epochs. eg if you wrote some flat infos, but then stopped.
        p_latest = self._metadata['pointers'].get('latest_flat_info')
        p_merge  = self._metadata['pointers'].get('_merge_flat')

        match self._config.base_info_type:
            case 'any':
                return init_info
            
            case 'latest_flat':
                if init_is_latest_flat: # extracted when getting init_info
                    return init_info
                # need to check against
                if p_latest and (not p_merge or p_merge[1] <= p_latest[1]) and not self._need_refresh(p_latest[1]):
                    return self.load('latest_flat_info')
                self.extract_flat_info()
                if not self._infos.raw_flat:
                    raise RuntimeError("raw_flat have been set in self._infos")
                return self._infos.raw_flat.data
                
            case 'merge_flat':
                if self._infos._merge_flat: # updated from init flat_info extraction
                    return self._infos._merge_flat.data
                if p_merge and not self._need_refresh(p_merge[1]):
                    data = self.load('_merge_flat')
                    self._infos._merge_flat = _InfosEntry(data,
                        pl_outtmpl=self._pl_outtmpls['_merged_flat_infojson'],
                        is_written=True, metadata_key='_merge_flat')
                    return data
                self.extract_flat_info() # has side effects on _merge_flat
                if not self._infos._merge_flat:
                    raise RuntimeError("_merge_flat should have been set in self._infos")
                return self._infos._merge_flat.data



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

        # initialize self._infos

        if not self._infos.raw_v_infos:
            self._infos.raw_v_infos = _InfosEntry([],
                self._pl_outtmpls['raw_video_infojson'],
                is_written=False, metadata_key=None)
        
        if data := self.load('_merge_flat', None):
            self._infos._merge_flat = _InfosEntry(data,
                pl_outtmpl=self._pl_outtmpls['_merged_flat_infojson'],
                is_written=True, metadata_key='_merge_flat')

        if init_is_latest_flat:
            self.add_raw_flat_info(yt_utils.copy_and_sanitize_info(init_info), self._config.write_flat, warn_no_init=False)
        
        if data := self.load('latest_merge_info', None):
            self._infos.merge_info = _InfosEntry(data,
                pl_outtmpl=self._pl_outtmpls['merge_infojson'],
                is_written=True, metadata_key='latest_merge_info')
        
        self._infos.base_info = _InfosEntry(
            yt_utils.copy_and_sanitize_info(self.__get_base_info_data(init_info, init_is_latest_flat)),
            pl_outtmpl=None, is_written=True, metadata_key=None)

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
    def write_info(
            self,
            info: _InfosEntry|None,
            collision_policy: utils.CollisionPolicies,
            alt_info: ANY_InfoDict|None = None,
            delete_prev: bool = False,
            _name: str = '',
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
        ident = _name or info.metadata_key or info.pl_outtmpl
        if delete_prev and not info.metadata_key:
            raise ValueError(f"Deleting the previous requires a metadata_key (for {ident})")
        if info.is_written == True and info.metadata_key != '_merge_flat':
            utils.WARNING(f"Already written. Skipping. (for {ident})")
            return None
        if info.pl_outtmpl is None:
            raise ValueError(f"pl_outtmpl was not found (for {ident})")

        if not utils.has_content(info.data):
            utils.WARNING(f"{info.metadata_key or _name} has no content. Not writing.")
            return None

        match info.metadata_key:
            case 'latest_pl_info' | 'latest_merge_info':
                epoch = yt_utils.get_latest_epoch(info.data)
                _dst = yt_utils.ytdlp_eval_tmpl(info.pl_outtmpl, info.data, {'epoch': epoch} | alt_info)

            case '_merge_flat' | 'latest_flat_info':
                epoch = yt_utils.get_epoch(info.data)
                _dst = yt_utils.ytdlp_eval_tmpl(info.pl_outtmpl, info.data, {'epoch': epoch} | alt_info)

            case _: 
                if isinstance(info.data, dict):
                    epoch = yt_utils.get_epoch(info.data)
                    _dst = yt_utils.ytdlp_eval_tmpl(info.pl_outtmpl, info.data, {'epoch': epoch} | alt_info)
                else:
                    # raw_v_infos
                    epoch = max(yt_utils.get_epoch(v_info)
                        for v_infos in info.data
                            for v_info in v_infos)
                    _dst = yt_utils.ytdlp_eval_tmpl(info.pl_outtmpl, {'epoch': epoch} | alt_info)

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
            if delete_prev and (stale_pointer := self._metadata['pointers'].get(info.metadata_key)):
                stale_path = os.path.join(self._config.home, stale_pointer[0])
                if pointer[0] != stale_pointer[0] and os.path.exists(stale_path):
                    os.unlink(stale_path)
                    print(utils.hex(f"Removed {ident or '\b'}: {stale_path}", fg="#ff60bd"))
            self._metadata['pointers'][info.metadata_key] = pointer

        print(utils.hex(f"Wrote {ident or '\b'} to: {dst}", fg="#70eeff"))
        
        return pointer

    def write_info_debug(
            self,
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
        if info_type not in pldl_types._MetadataPointers.__optional_keys__:
            raise ValueError(f"Unknown {info_type = }")

        types: dict[pldl_types._MetadataFiles_Lit, _InfosEntry|None] = {
            '_merge_flat': self._infos._merge_flat,
            'latest_flat_info': self._infos.raw_flat,
            'latest_pl_info': self._infos.pl_info,
            'latest_merge_info': self._infos.merge_info,
        }
        entry = types[info_type]
        if entry is not None:
            utils.WARNING(f"{info_type} is already loaded. Returning a copy to the data.")
            return entry.data
        
        pointer: tuple[str, int]|None = self._metadata['pointers'].get(info_type)
        if not pointer:
            if default is utils.RAISE_EXC:
                raise FileNotFoundError(f"{info_type} is not written according to metadata")
            return default # type: ignore - utils.RAISE_EXC is dealt with
        path, _epoch = pointer
        return utils.json_load(os.path.join(self._config.home, path), default)

    def get_best_info(self) -> PL_InfoDict:
        # note: or returns the first non falsey element
        return (self._infos.merge_info or
                self._infos.pl_info or
                self._infos.base_info).data

    # 
    # Handling raw infodicts
    # 
    
    def _update_merge_flat_with_flat_info(self, flat_info: PL_InfoDict, warn_no_init: bool):
        init_merge_flat: PL_InfoDict|None
        if self._infos._merge_flat:
            init_merge_flat = self._infos._merge_flat.data
        else:
            if warn_no_init:
                utils.WARNING("No init_merge_flat found")
            init_merge_flat = None # should have been loaded already

        self._infos._merge_flat = _InfosEntry(
            merge_infos.merge_pl_infos(
                [flat_info],
                merge_updaters.FLAT_MERGE_UPDATER,
                update_filter=self._config.update_filter,
                _init_merge_info=init_merge_flat),
            self._pl_outtmpls['_merged_flat_infojson'],
            is_written=False,
            metadata_key='_merge_flat')

    def _update_merge_flat_with_v_info(self, v_info: V_InfoDict):
        """ updates the keys in flat_info, adds v_timeline """
        if yt_utils.get_v_info_level(v_info) == V_InfoLevel.NONE:
            return
        
        if not self._infos._merge_flat:
            utils.WARNING("_merge_flat was not found. Try extracting flat or setting base_info_type to " \
                          "`latest_flat` or `merge_flat`. (Fixing this would require many edits)")
            return
        
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
            self._config.update_filter,
            _init_v_info=init_v_info,
            _init_v_timeline=merge_flat_info.get('merge_timeline', {}).get(v_id, {}))
        new_v_info['info_level'] = merge_flat_info['entries'][index].get('info_level', V_InfoLevel.NONE.name)

        for epoch in list(new_v_timeline.keys()):
            # this is very fragile, but it'll work
            entry = new_v_timeline[epoch]
            if 'better_info' in entry and entry['better_info'] != 'NONE -> FLAT': entry.pop('better_info')
            if 'unavailable' in entry: entry.pop('unavailable')
            if not entry:
                new_v_timeline.pop(epoch)
        merge_flat_info['entries'][index] = new_v_info
        merge_flat_info.setdefault('merge_timeline', {})[v_id] = new_v_timeline

    def add_raw_flat_info(self, raw_flat_info: PL_InfoDict, write: bool = False, warn_no_init: bool = True):
        self._infos.raw_flat = _InfosEntry(
            raw_flat_info, self._pl_outtmpls['raw_flat_infojson'],
            is_written=False, metadata_key='latest_flat_info')

        # write raw info asap
        if write:
            self.write_info(self._infos.raw_flat, collision_policy='mov new', delete_prev=False)

        # update _merge_flat
        self._update_merge_flat_with_flat_info(raw_flat_info, warn_no_init)

        return self._infos.raw_flat.data


    def filter_for_in_playlist[T](self, infos: list[T], id_key: Callable[[T], V_ID], warn: bool = False) -> list[T]:
        v_ids = set(self.get_v_ids(self._infos.base_info))
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
        
        match yt_utils.get_v_info_level(v_info):
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
        
    def _add_v_infos_to_archives(self, v_infos: list[V_InfoDict], pl_dl_info: PL_DownloadInfo|None):
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
                self._config.meta_dl_history_filter,
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
            for v_info in v_infos if yt_utils.get_v_info_level(v_info) == V_InfoLevel.DOWNLOAD}
        dl_keys_to_add = list(filter(lambda dl_key: dl_key not in self._yt_dlp_archive, dl_keys))
        if dl_keys_to_add:
            with open(self._pl_outtmpls['yt_dlp_archive'], 'a') as f:
                for ie, v_id in dl_keys_to_add:
                    f.write(f'{ie} {v_id}\n')
                    self._yt_dlp_archive.append((ie, v_id))
            print(utils.hex(f"Updated yt_dlp_archive: {self._pl_outtmpls['yt_dlp_archive']}", fg="#637f86"))

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
    
    def add_raw_v_infos(
            self,
            raw_v_infos: list[V_InfoDict] | list[list[V_InfoDict]],
            pl_dl_info: PL_DownloadInfo|None = None,
            write: bool = False,
            alt_info: ANY_InfoDict|None = None,
    ) -> list[V_InfoDict]:
        """
        Only adds v_infos whose id's are in the base_info playlist.
        Updates _infos.raw_v_infos, metadata['history'], and if necessary the yt_dlp_archive file
        Refreshes yt_dlp_archive dict
        Returns the `v_infos` that were added to `self._infos.raw_v_infos.data`,
        """
        
        if alt_info is None:
            alt_info = {}
        v_infos = PlaylistDL.flatten_raw_v_infos(raw_v_infos)

        # only add v_infos that are currently in base_info playlist
        # to add ones that are not, their id (or fake id) should be added prior with playlist manipulation
        v_infos = self.filter_for_in_playlist(v_infos, id_key=lambda i: i['id'], warn=True)
        
        self._infos.raw_v_infos.data.append(v_infos)
        self._infos.raw_v_infos.is_written = False
        if write:
            self.write_info(self._infos.raw_v_infos, collision_policy='rm old', alt_info=alt_info)
        for v_info in v_infos:
            self._update_merge_flat_with_v_info(v_info)

        self._add_v_infos_to_archives(v_infos, pl_dl_info)
        return v_infos

    # 
    # YT-DLP Extraction / Download + Helpers
    # 

    def extract_flat_info(self, write: bool|type[USE_CONFIG]=USE_CONFIG, cookiefile: str|None|type[USE_CONFIG] = USE_CONFIG):
        """
        Use yt-dlp to extract flat playlist info.
        Params override respective configs (write_flat, cookie_file/cookies_for_pl).
        Updates `_infos.raw_flat` and `_infos._merge_flat`
        """
        self.pre_yt_dlp_download()
        raw_flat_info = yt_utils.extract_flat_info(pl_url_or_id=self.id,
            opts=self.opts | {
                'cookiefile': cookiefile if cookiefile is not USE_CONFIG else \
                              self._config.cookie_file if self._config.cookies_for_pl else \
                              None,
                'download_archive': None}) # type: ignore - download flat info anyway!
        self.add_raw_flat_info(raw_flat_info, bool(write) or (write is USE_CONFIG and self._config.write_flat))
        if not self._infos.raw_flat:
            raise RuntimeError("raw_flat should have been written")
        return self._infos.raw_flat.data

    
    @staticmethod
    def _get_dl_result(v_info, success: bool) -> DL_Result:
        if not success:
            return DL_Result.FAIL
        if v_info is None:
            return DL_Result.CACHED # None is returned if download cache or cancelled.
        
        match yt_utils.get_v_info_level(v_info):
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
            write: bool|type[USE_CONFIG] = USE_CONFIG,
            cookiefile: str|None|type[USE_CONFIG] = USE_CONFIG,
            wrapper_match_filter: WrapperMatchFilter|type[USE_CONFIG] = USE_CONFIG,
            opts: YT_DLP_Params|type[USE_CONFIG] = USE_CONFIG,
            try_yt_even_if_unavailable: bool = True,
            wa: bool = True,
            order_manip: V_DL_OrderManip|None|type[USE_CONFIG] = USE_CONFIG,
    ):
        """ Returns the newly downloaded portion of the raw v_infos """
        self.pre_yt_dlp_download()

        history_ids = yt_utils.ids_from_history(self._metadata['history'])
        yt_dlp_archive_ids = yt_utils.ids_from_yt_dlp_archive(self._yt_dlp_archive)
        _wrapper_match_filter: WrapperMatchFilter = wrapper_match_filter if wrapper_match_filter is not USE_CONFIG \
                                               else self._config.wrapper_match_filter # type: ignore
        _opts: YT_DLP_Params = (
            self.opts if opts is USE_CONFIG else opts | {
            'cookiefile': cookiefile if cookiefile is not USE_CONFIG else \
                          self._config.cookie_file if self._config.cookies_for_vids else \
                          None}) # type: ignore
        _order_manip: V_DL_OrderManip|None = order_manip if order_manip is not USE_CONFIG else \
                                            self._config.video_dl_order_manip # type: ignore

    
        print("\n ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n"
                "  Downloading Playlist Videos \n"
                " ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n")

        v_infos, pl_dl_info = PlaylistDL._download_v_infos(
            self._infos.base_info.data,
            lambda pl_v_info, curr_pl_dl_info: _wrapper_match_filter(
                pl_v_info, curr_pl_dl_info,
                self._metadata['history'], history_ids,
                self._yt_dlp_archive, yt_dlp_archive_ids),
            opts=_opts,
            try_yt_even_if_unavailable=try_yt_even_if_unavailable,
            wa=wa,
            order_manip=_order_manip,
            sleep_interval=(
                self._config.opts.get('sleep_interval') or 0.2,
                self._config.opts.get('max_sleep_interval') or 1))

        write_v_infos = bool(write) or (write is USE_CONFIG and self._config.write_raw_v_infos)
        self.add_raw_v_infos(v_infos, pl_dl_info, write_v_infos, alt_info={'epoch': self.session_start_epoch})

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

    def download_v_info_generic(self, v_id: str, any_yt_dlp_url: str, download: bool, opts: YT_DLP_Params|None = None, write: bool|type[USE_CONFIG] = USE_CONFIG, cookiefile: str|None = None) -> tuple[V_InfoDict, DownloadInfo] | tuple[None, DownloadInfo]:
        """
        Only video downloads are added to metadata history.
        Added to raw_v_infos if DownloadError or there is a result.
        Normal Exceptions are just printed.

        Returns what was received from yt_dlp
        """
        self.pre_yt_dlp_download()

        if opts is None:
            opts = {}

        if v_id not in self.get_v_ids(self._infos.base_info):
            raise ValueError(f"{v_id} is not in the loaded playlist")
        
        v_info, dl_info = PlaylistDL._download_v_info_generic(
            v_id,
            any_yt_dlp_url,
            self.opts | opts | {'cookiefile': cookiefile},
            download)
        
        if v_info is None:
            return None, dl_info

        write_v_infos = bool(write) or (write is USE_CONFIG and self._config.write_flat)
        self.add_raw_v_infos([v_info], [dl_info], write_v_infos, alt_info={'epoch': self.session_start_epoch})
        return v_info, dl_info

    # 
    # Merge raw data
    # 

    # TODO: _make_pl_info and _make_merge_info should be @staticmethod's
    def _make_pl_info(self, base_pl_info: PL_InfoDict, raw_v_infos: list[V_InfoDict], clean_info_json: bool):
        pl_info = yt_utils.copy_and_sanitize_info(base_pl_info, clean_info_json)
        pl_info.pop('merge_timeline', None) # base_info may be merged (eg _merge_flat)

        if not raw_v_infos:
            return pl_info

        v_id_to_index = PlaylistDL.get_v_id_to_index(pl_info)

        for v_info in raw_v_infos:
            if v_info.get('id') not in v_id_to_index:
                utils.WARNING(f"SKIP: {yt_utils.get_v_display(v_info)} is not in the playlist.")
                continue
            i = v_id_to_index[v_info['id']]

            # merge_info is responsible for full info_level path
            pl_info['entries'][i], _v_timeline = merge_infos.merge_v_infos(
                [pl_info['entries'][i],
                 yt_utils.copy_and_sanitize_info(v_info, clean_info_json)],
                field_updater=merge_updaters.COMMON_UPDATER,
                update_filter=self._config.update_filter)
        
        yt_utils.fixup_pl_info(pl_info)
        return pl_info

    def make_pl_info(self, write: bool|type[USE_CONFIG] = USE_CONFIG, delete_prev: bool=False) -> PL_InfoDict:
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
            self._infos.base_info.data,
            [v_info for v_infos in self._infos.raw_v_infos.data for v_info in v_infos],
            self.opts.get('clean_infojson') or False)
        self._infos.pl_info = _InfosEntry(pl_info, self._pl_outtmpls['pl_infojson'], is_written=False, metadata_key='latest_pl_info')

        if write or (write is USE_CONFIG and self._config.write_pl_info):
            self.write_info(self._infos.pl_info, collision_policy='mov new',
                alt_info={'epoch': yt_utils.get_latest_epoch(pl_info)}, delete_prev=delete_prev)
        return pl_info


    def _make_merge_info(
            self,
            field_updater: merge_updaters.Signature,
            update_filter: Callable[[str], bool],
    ) -> PL_InfoDict:

        base_info = yt_utils.copy_and_sanitize_info((self._infos._merge_flat or self._infos.base_info).data)

        if self._infos.merge_info:
            init = yt_utils.copy_and_sanitize_info(self._infos.merge_info.data)
            pl_infos = [base_info]
        else:
            init = base_info
            pl_infos = []

        # Don't use stored `pl_info`
        # Recreating the pl_info is fast enough, so this is okay
        pl_infos.append(self._make_pl_info(
            self._infos.base_info.data,
            [v_info for v_infos in self._infos.raw_v_infos.data for v_info in v_infos],
            self.opts.get('clean_infojson') or False))

        # utils.json_dump(yt_utils.copy_and_sanitize_info(init), 'merge-test/init.json')
        # utils.json_dump(yt_utils.copy_and_sanitize_info(pl_infos), 'merge-test/pl_infos.json')
        
        return merge_infos.merge_pl_infos(pl_infos, field_updater, update_filter, init)
            
    def make_merge_info(
            self,
            write: bool | type[USE_CONFIG] = USE_CONFIG,
            delete_prev: bool = False,
            field_updater: merge_updaters.Signature|type[USE_CONFIG] = USE_CONFIG,
            update_filter: Callable[[str], bool]|list[str]|type[USE_CONFIG] = USE_CONFIG,
    ) -> PL_InfoDict:
        """
        Creates merge info using `init_ident` and the current run's pl_info.
        Returns the created merge info.
        
        May call ``make_pl_info()``.
        """

        merge_info = self._make_merge_info(
            self._config.field_updater if field_updater == USE_CONFIG else \
                field_updater, # type: ignore - USE_CONFIG is captured
            self._config.update_filter if update_filter == USE_CONFIG else \
                lambda k: k in update_filter if isinstance(update_filter, list) else \
                update_filter) # type: ignore - USE_CONFIG is captured)
        self._infos.merge_info = _InfosEntry(merge_info, self._pl_outtmpls['merge_infojson'], is_written=False, metadata_key='latest_merge_info')

        if write or (write is USE_CONFIG and self._config.write_merge):
            self.write_info(self._infos.merge_info, collision_policy='mov new',
                alt_info={'epoch': yt_utils.get_latest_epoch(merge_info)}, delete_prev=delete_prev)

        return merge_info


    # for general use
    # TODO: delete in the future. The user should only need to download raw infos.
    # pl_info/merge should be called/made automatically based on config.
    def download(
            self,
            order_manip: V_DL_OrderManip|None|type[USE_CONFIG] = USE_CONFIG,
            delete_prev_pl: bool = False,
            delete_prev_merge: bool = False,
    ):
        """ Calls the download functions based on configs """
        if self._config.write_raw_v_infos:
            self.download_v_infos(order_manip=order_manip)
        if self._config.write_pl_info:
            self.make_pl_info(delete_prev=delete_prev_pl)
        if self._config.write_merge:
            self.make_merge_info(delete_prev=delete_prev_merge)



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


    def _remove_video_impl(self, base_index: int | None, merge_index: int | None, mutate_merge_flat: bool):
        """Helper: Remove a video at given indices.

        Assumes validation is already done.
        Does NOT call fixup_pl_info - caller must call it after all operations.

        base_index and merge_index do not need to point to the same v_id
        """
        if base_index is not None:
            self._infos.base_info.data['entries'].pop(base_index)

        if mutate_merge_flat and self._infos._merge_flat and merge_index is not None:
            removed_entry = self._infos._merge_flat.data['entries'].pop(merge_index)
            PlaylistDL._add_update_to_merge_timeline(
                self._infos._merge_flat.data, removed_entry['id'],
                update_str=f'<REMOVE {yt_utils.get_v_display(removed_entry)}>')

    def remove_video(self, v_id: V_ID, mutate_merge_flat: bool = True):
        """Remove a video from the playlist by its ID.

        Args:
            v_id: Video ID to remove from the playlist.
            mutate_merge_flat: If True, also update _merge_flat for persistence.
                Requires config.base_info_type == 'merge_flat'.
                Adds `<REMOVE {v_display}>` update
        """

        base_v_ids = PlaylistDL.get_v_ids(self._infos.base_info)
        merge_v_ids = PlaylistDL.get_v_ids(self._infos._merge_flat) or []

        if v_id not in base_v_ids and v_id not in merge_v_ids:
            utils.WARNING(f"{v_id} is not in the playlist.")
            return

        base_index = base_v_ids.index(v_id) if v_id in base_v_ids else None
        merge_index = merge_v_ids.index(v_id) if v_id in merge_v_ids else None
        
        if base_index is not None or merge_index is not None:
            self._remove_video_impl(base_index, merge_index, mutate_merge_flat)

        yt_utils.fixup_pl_info(self._infos.base_info.data)
        if mutate_merge_flat and self._infos._merge_flat:
            yt_utils.fixup_pl_info(self._infos._merge_flat.data)

    def remove_videos(self, v_ids: Iterable[V_ID], mutate_merge_flat: bool = True):
        """Remove multiple videos from the playlist by their IDs.

        Videos are removed in reverse order (by position) to avoid index shifting issues.

        Args:
            v_ids: Video IDs to remove from the playlist.
            mutate_merge_flat: If True, also update _merge_flat for persistence.
                Requires config.base_info_type == 'merge_flat'.
                Adds `<REMOVE {v_display}>` update for each video
        """
        base_v_ids = PlaylistDL.get_v_ids(self._infos.base_info)
        merge_v_ids = PlaylistDL.get_v_ids(self._infos._merge_flat) or []

        # Find indices for all videos to remove
        base_indexes: list[int] = []
        merge_indexes: list[int] = []

        for v_id in set(v_ids):
            base_i = base_v_ids.index(v_id) if v_id in base_v_ids else None
            merge_i = merge_v_ids.index(v_id) if v_id in merge_v_ids else None

            if base_i is None and (not mutate_merge_flat or merge_i is None):
                utils.WARNING(f"{v_id} is not in the playlist.")
                continue
            if base_i  is not None: base_indexes.append(base_i)
            if merge_i is not None: merge_indexes.append(merge_i)

        # Sort by base_index descending to avoid index shifting issues
        base_indexes.sort(reverse=True)
        merge_indexes.sort(reverse=True)

        # indexes may be for different v_ids
        for base_i, merge_i in itertools.zip_longest(base_indexes, merge_indexes):
            self._remove_video_impl(base_i, merge_i, mutate_merge_flat)

        yt_utils.fixup_pl_info(self._infos.base_info.data)
        if mutate_merge_flat and self._infos._merge_flat:
            yt_utils.fixup_pl_info(self._infos._merge_flat.data)


    def _insert_video_impl(self, v_id: V_ID, index: int, mutate_merge_flat: bool):
        """Helper: Insert a video at given index.

        Assumes validation is already done.
        Does NOT call fixup_pl_info - caller must call it after all operations.
        """
        new_v_info = yt_utils.min_v_info(v_id, V_InfoLevel.NONE)

        self._infos.base_info.data['entries'].insert(index, copy.deepcopy(new_v_info))

        if mutate_merge_flat and self._infos._merge_flat:
            self._infos._merge_flat.data['entries'].insert(index, copy.deepcopy(new_v_info))
            PlaylistDL._add_update_to_merge_timeline(
                self._infos._merge_flat.data, v_id,
                update_str=f'<INSERT to={index+1}>')

    def insert_video(self, v_id: V_ID, position: int = 1, mutate_merge_flat: bool = True):
        """Insert a new video into the playlist at the specified position.

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
            mutate_merge_flat: If True, also update _merge_flat for persistence.
                Requires config.base_info_type == 'merge_flat'.
                Adds `<INSERT>` update
        """
        base_v_ids = PlaylistDL.get_v_ids(self._infos.base_info)
        merge_v_ids = PlaylistDL.get_v_ids(self._infos._merge_flat) or []

        if mutate_merge_flat and self._infos._merge_flat \
           and base_v_ids != merge_v_ids:
            raise AssertionError(
                f"Mismatch between base_info and _merge_flat v_ids\n"
                f"base_info   = {base_v_ids}\n"
                f"_merge_flat = {merge_v_ids}")

        if v_id in base_v_ids:
            raise ValueError(f"{v_id} is already in the playlist (check _merge_flat).")

        index = utils.position_to_index(position, len(base_v_ids))
        self._insert_video_impl(v_id, index, mutate_merge_flat)

        yt_utils.fixup_pl_info(self._infos.base_info.data)
        if mutate_merge_flat and self._infos._merge_flat:
            yt_utils.fixup_pl_info(self._infos._merge_flat.data)

    def insert_videos(self, v_ids: Iterable[V_ID], position: int = 1, mutate_merge_flat: bool = True):
        """Insert multiple videos into the playlist at the specified position.

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
            mutate_merge_flat: If True, also update _merge_flat for persistence.
                Requires config.base_info_type == 'merge_flat'.
                Adds `<INSERT>` update for each video
        """
        base_v_ids = PlaylistDL.get_v_ids(self._infos.base_info)
        merge_v_ids = PlaylistDL.get_v_ids(self._infos._merge_flat) or []

        if mutate_merge_flat and self._infos._merge_flat \
           and base_v_ids != merge_v_ids:
            raise AssertionError(
                f"Mismatch between base_info and _merge_flat v_ids\n"
                f"base_info   = {base_v_ids}\n"
                f"_merge_flat = {merge_v_ids}")

        # Convert to list to check for duplicates and allow multiple passes
        v_ids_list = list(v_ids)

        # Check for duplicates in input
        if len(v_ids_list) != len(set(v_ids_list)):
            duplicates = [x for x in set(v_ids_list) if v_ids_list.count(x) > 1]
            raise ValueError(
                f"All ids must be unique.\n"
                f"Duplicates: {sorted(duplicates)}")

        # Check for conflicts with existing videos
        conflicts = [v_id for v_id in v_ids_list if v_id in base_v_ids]
        if conflicts:
            raise ValueError(f"The following IDs are already in the playlist: {conflicts}")

        for offset, v_id in enumerate(v_ids_list):
            index = utils.position_to_index(position+offset, len(base_v_ids))
            self._insert_video_impl(v_id, index, mutate_merge_flat)
            # Update base_v_ids for next iteration's position calculation
            base_v_ids.insert(index, v_id)

        yt_utils.fixup_pl_info(self._infos.base_info.data)
        if mutate_merge_flat and self._infos._merge_flat:
            yt_utils.fixup_pl_info(self._infos._merge_flat.data)


    # TODO: Should update metadata in some way? That would also require updating how history is handled though...
    def _replace_video_impl(self, base_index: int|None, merge_index: int|None, v_id: V_ID, repl: V_ID, mutate_merge_flat: bool):
        """Helper: Replace a video ID at given indices.

        Assumes validation is already done.
        Does NOT call fixup_pl_info - caller must call it after all operations.
        """
        if base_index is not None:
            self._infos.base_info.data['entries'][base_index]['id'] = repl

        if mutate_merge_flat and self._infos._merge_flat and merge_index is not None:
            self._infos._merge_flat.data['entries'][merge_index]['id'] = repl
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
            mutate_merge_flat: If True, also update _merge_flat for persistence.
                Requires config.base_info_type == 'merge_flat'.
                Adds `<REPLACE ID from={v_id} to={repl}>` update
        """

        base_v_ids = PlaylistDL.get_v_ids(self._infos.base_info)
        merge_v_ids = PlaylistDL.get_v_ids(self._infos._merge_flat) or []

        if v_id not in base_v_ids and (not mutate_merge_flat or v_id not in merge_v_ids):
            raise ValueError(f"The target id {v_id} is not in the playlist.")

        base_index  = base_v_ids.index(v_id)  if v_id in base_v_ids  else None
        merge_index = merge_v_ids.index(v_id) if v_id in merge_v_ids else None
        if base_index is not None and repl in base_v_ids:
            raise ValueError(f"Replacement id {repl} is already in the 'base_info' playlist")
        if mutate_merge_flat and (merge_index is not None and repl in merge_v_ids):
            raise ValueError(f"Replacement id {repl} is already in the '_merge_flat' playlist")

        self._replace_video_impl(base_index, merge_index, v_id, repl, mutate_merge_flat)

        yt_utils.fixup_pl_info(self._infos.base_info.data)
        if mutate_merge_flat and self._infos._merge_flat:
            yt_utils.fixup_pl_info(self._infos._merge_flat.data)

    def replace_videos(self, replacements: Iterable[tuple[V_ID, V_ID]], mutate_merge_flat: bool = True):
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
            mutate_merge_flat: If True, also update _merge_flat for persistence.
                Requires config.base_info_type == 'merge_flat'.
                Adds `<REPLACE ID from={v_id} to={repl}>` update for each replacement
        """
        replacements_list = list(replacements)

        base_v_ids = PlaylistDL.get_v_ids(self._infos.base_info)
        merge_v_ids = PlaylistDL.get_v_ids(self._infos._merge_flat) or []

        # Simulate replacements to check for conflicts
        def simulate(sim_list: list[str], list_name: str):
            """ mutates passed in list """
            failed_ops: list[tuple[int, tuple[V_ID, V_ID]]] = []
            for i, (target, repl) in enumerate(replacements_list):
                if target not in sim_list:
                    failed_ops.append((i, (target, repl)))
                    continue
                target_index = sim_list.index(target)
                if repl in sim_list:
                    raise ValueError(
                        f"Replacement id {repl} is already in the '{list_name}' playlist "
                        f"at position {sim_list.index(repl) + 1} "
                        f"(target {target} is at position {target_index + 1})")
                sim_list[target_index] = repl
            return failed_ops

        base_fails = simulate(list(base_v_ids), 'base_info')
        if mutate_merge_flat and self._infos._merge_flat:
            merge_fails = simulate(list(merge_v_ids), '_merge_info')
            common_fails = sorted(set(base_fails).intersection(set(merge_fails)), key=lambda x: x[0])
        else:
            merge_fails = []
            common_fails = base_fails

        def format_fails(fails: list[tuple[int, tuple[V_ID, V_ID]]]):
            return '\n'.join(f"{i+1}. '{_from}' -> '{to}'" for i, (_from, to) in fails)
        if base_fails:
            utils.WARNING(f"Failed base_info replacements:\n{format_fails(base_fails)}")
        if merge_fails:
            utils.WARNING(f"Failed _merge_flat replacements:\n{format_fails(merge_fails)}")
        if common_fails:
            raise ValueError(f"Failed Replacements:\n{format_fails(common_fails)}")

        # Execute all replacements
        for target, repl in replacements_list:
            base_index = base_v_ids.index(target) if target in base_v_ids else None
            merge_index = merge_v_ids.index(target) if target in merge_v_ids else None
            self._replace_video_impl(base_index, merge_index, target, repl, mutate_merge_flat)
            # Update v_ids for next iteration
            if base_index is not None:  base_v_ids[base_index]   = repl
            if merge_index is not None: merge_v_ids[merge_index] = repl

        yt_utils.fixup_pl_info(self._infos.base_info.data)
        if mutate_merge_flat and self._infos._merge_flat:
            yt_utils.fixup_pl_info(self._infos._merge_flat.data)


    def move_video(self, v_id: V_ID, position: int, mutate_merge_flat: bool = True):
        """Move a video to a new position in the playlist.

        Position Behavior:

                 _ A _ B _ C _ D _
                 1   2   3   4   5 ...
            ... -5  -4  -3  -2  -1
        
        Args:
            v_id: Video ID to move.
            position: Target position. Clamped to valid range. Can be negative. `0` is invalid.
            mutate_merge_flat: If True, also update _merge_flat for persistence.
                Requires config.base_info_type == 'merge_flat'.
                Adds `<MOVE from={} to={}>` update (positions/1-indexed)
        """

        base_v_ids = PlaylistDL.get_v_ids(self._infos.base_info)
        merge_v_ids = PlaylistDL.get_v_ids(self._infos._merge_flat) or []

        if mutate_merge_flat and self._infos._merge_flat \
           and base_v_ids != merge_v_ids:
            raise AssertionError(
                f"Mismatch between base_info and _merge_flat v_ids\n"
                f"base_info   = {base_v_ids}\n"
                f"_merge_flat = {merge_v_ids}")
        
        if v_id not in base_v_ids:
            raise ValueError(f"The target id {v_id} is not in the playlist.")

        index = utils.position_to_index(position, len(base_v_ids)-1) # The -1 fixes removing first
        old_index = base_v_ids.index(v_id)
        if index == old_index:
            utils.WARNING(f"Tried to move {v_id} to its current position ({position})")
            return

        # Removing then adding works better than adding then removing duplicate.
        entry = self._infos.base_info.data['entries'].pop(old_index)
        self._infos.base_info.data['entries'].insert(index, entry)
        yt_utils.fixup_pl_info(self._infos.base_info.data)

        if mutate_merge_flat and self._infos._merge_flat:
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
            if self._infos._merge_flat:
                info = self._infos._merge_flat.data
            else:
                info = self.get_best_info()
        if isinstance(info, _InfosEntry):
            info = info.data
        
        print("\n ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n"
                "  Playlist Metadata History \n"
                " ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n")
        display.metadata_history(self._metadata['history'], info, PlaylistDL.get_v_ids(info), include_urls)
        print()

    def display_pl_merge_timeline(self, info: _InfosEntry[PL_InfoDict]|PL_InfoDict|None, include_urls: bool = True):
        if info is None:
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
        if not self._infos._merge_flat:
            utils.WARNING("_merge_flat was not found")
            return
        self.write_info(self._infos._merge_flat, collision_policy='rm old', delete_prev=True)

    def write_metadata_file(self):
        # TODO: Reorder 'history' keys by date
        utils.json_dump(self._metadata, self._pl_outtmpls['metadata'], on_collision='rm old')
        print(utils.hex(f"Updated metadata: {self._pl_outtmpls['metadata']}", fg="#637f86"))

    def empty_cookies(self):
        if self._config.cookie_file and os.path.exists(self._config.cookie_file):
            with open(self._config.cookie_file, 'w'):
                ...
            print(utils.hex(f"Emptied cookie file: {self._config.cookie_file}", fg="#ff60bd"))

    def close(self):
        # TODO: if self._config.write_pl_info or .write_merge are True
        # but they were never made, prompt to make/write them
        # individually: pl_info then merge_info.
        if self._config.empty_cookies:
            self.empty_cookies()
        self.write_merge_flat()
        
        self.write_metadata_file() # should be LAST

    def __enter__(self):
        # everything is handled by __init__()
        return self
    
    def __exit__(self, *args):
        self.close()
    