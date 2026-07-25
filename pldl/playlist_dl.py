__all__ = ['PlaylistDL']

import os
import copy
from typing import Callable, Any, overload, Mapping, Iterable
import pprint
import dataclasses

from .utils import utils
from .config import PlaylistDL_Config, Config_IdentType
from ._types import *
from . import _types
from . import yt_utils
from . import yt_utils

from . import display
from .post_processing import merge_infos
from .post_processing import merge_updaters



@dataclasses.dataclass
class _InfosEntry[T]:
    data: T
    pl_outtmpl: str|None
    is_written: bool
    metadata_key: _types._MetadataFiles_Lit | None = None

@dataclasses.dataclass
class _Infos:
    base_info:   _InfosEntry[PL_InfoDict] = None # type: ignore - temporary
    raw_flat:    _InfosEntry[PL_InfoDict] | None = None
    raw_v_infos: _InfosEntry[list[list[V_InfoDict]]] | None = None
    # No enforced order. Associatted pl_dl_info is in self._metadata['history']

    _merge_flat: _InfosEntry[PL_InfoDict] | None = None
    pl_info:     _InfosEntry[PL_InfoDict] | None = None
    merge_info:  _InfosEntry[PL_InfoDict] | None = None


def init_metadata(
        id: str,
        path_tmpls: PL_Resolved_CustomOuttmpl,
        history: PL_DownloadHistory|None = None,
        pointers: _types._MetadataPointers|None = None
) -> Metadata:
    return {
        'id': id,
        'path_tmpls': path_tmpls,
        'pointers': pointers or {},
        'history': history or {},
    }

class USE_CONFIG(utils.FalsySentinel):
    pass

class PlaylistDL:
    
    # Functions meant only __init__ really needs

    def _need_refresh(self, epoch: float):
        time_since = utils.epoch_now() - epoch
        return time_since > self._config.refresh_after

    def __get_init_info(self) -> PL_InfoDict:
        """ Load if possible and update if necessary. May set self._infos.raw_flat """
        
        def extract_flat(id: str) -> PL_InfoDict:
            raw_flat_info = yt_utils.extract_flat_info(
                pl_url_or_id=id,
                opts={'cookiefile': self._config.cookie_file if self._config.cookies_for_pl else None})
            if not raw_flat_info:
                raise RuntimeError(f"Extracting Flat info from {id} returned `None`")
            self._infos.raw_flat = _InfosEntry(data=raw_flat_info, pl_outtmpl=None, is_written=False, metadata_key='latest_flat_info') # temporary
            return self._infos.raw_flat.data

        match self._config.ident_type:
            case Config_IdentType.PL_ID_OR_URL:
                return extract_flat(self._config.ident)
            
            case Config_IdentType.PL_INFO_PATH:
                pl_info: PL_InfoDict = utils.json_load(self._config.ident)
                if self._need_refresh(yt_utils.get_epoch(pl_info)):
                    return extract_flat(pl_info['id'])
                return pl_info
            
            case Config_IdentType.METADATA_PATH:
                metadata: Metadata = utils.json_load(self._config.ident)
                preference_order: list[_types._MetadataFiles_Lit] = [
                    '_merge_flat', 'latest_flat_info', 'latest_pl_info', 'latest_merge_info'
                ]
                pointers: list[tuple[str, int]|None] = [metadata['pointers'].get(k) for k in preference_order]
                latest_pointer = max(pointers, key=lambda x: -float('inf') if x is None else x[1])
                if latest_pointer is None:
                    return extract_flat(metadata['id'])
                pl_info: PL_InfoDict = utils.json_load(os.path.join(self._config.home, latest_pointer[0]))
                if self._need_refresh(yt_utils.get_epoch(pl_info)):
                    return extract_flat(metadata['id'])
                return pl_info
            
            case _:
                raise ValueError(f"Invalid playlist ident_type: {self._config.ident_type}")
                

    @staticmethod
    def get_pl_outtmpls(Home: str, outtmpls: CustomOuttmpl, pl_info: PL_InfoDict) -> PL_Resolved_CustomOuttmpl:
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
        pl_outtmpls: PL_Resolved_CustomOuttmpl = {
            **{k: os.path.join(Home, Playlist, p) for k, p in outtmpls.items() if isinstance(p, str)},
            'Playlist': os.path.join(Home, Playlist),
        } # type: ignore

        return pl_outtmpls

    @staticmethod
    def create_path_opts(home: str, pl_outtmpls: PL_Resolved_CustomOuttmpl) -> YT_DLP_Params:

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
    def validate_metadata_sync(old_metadata: Metadata, pl_outtmpls: PL_Resolved_CustomOuttmpl, _config: PlaylistDL_Config):
        if not old_metadata:
            return
        
        yt_utils.validate_metdata_config_sync(old_metadata, _config)
        
        if old_metadata['path_tmpls'] != pl_outtmpls:
            raise RuntimeError(
                f"Found changed `Playlist` outtmpl.\n"
                f"old:\n{pprint.pformat(old_metadata['path_tmpls'], width=200)}\n"
                f"current:\n{pprint.pformat(pl_outtmpls, width=200)}")

    def _get_and_validate_metadata(self) -> Metadata:
        curr_meta_paths: PL_Resolved_CustomOuttmpl = {
            k: os.path.relpath(p, self._config.home) for k, p in self._pl_outtmpls.items()} # type: ignore

        old_metadata: Metadata|None = utils.json_load(self._pl_outtmpls['metadata'], default=None)
        if old_metadata is not None:
            PlaylistDL.validate_metadata_sync(old_metadata, curr_meta_paths, self._config) # raise Exceptions!

        
        return (
            copy.deepcopy(old_metadata) or \
            init_metadata(
                id=self.id,
                path_tmpls=curr_meta_paths,
            ))


    @staticmethod
    def validate_yt_dlp_archive_sync(yt_dlp_archive: YT_DLP_DownloadArchive, metadata: Metadata):
        ytdlp_dl = set(yt_utils.ids_from_yt_dlp_archive(yt_dlp_archive))
        hist_dl = set(yt_utils.ids_from_history(metadata['history'])['download'])
        if ytdlp_dl != hist_dl:
            raise RuntimeError(
                f"Detected download state mismatch:\n"
                f"ytdlp-only: {ytdlp_dl - hist_dl}\n"
                f"hist-only: {hist_dl - ytdlp_dl}")
    
    def _get_and_validate_yt_dlp_archive(self):
        path = self._pl_outtmpls['yt_dlp_archive']
        yt_dlp_archive = yt_utils.load_yt_archive(path)
        PlaylistDL.validate_yt_dlp_archive_sync(yt_dlp_archive, self._metadata)
        return yt_dlp_archive


    def _get_base_info_data(self, _init_info: PL_InfoDict) -> PL_InfoDict:

        # _init_info does not need a refresh. (see _get_init_info())
        # Assume init is written - if it was extracted, then it is already in raw_flat.
        if self._config.ident_type == Config_IdentType.PL_INFO_PATH and self._config.base_info_type != 'any':
            utils.WARNING(
                f"The passed in info will only be used for metadata identification.\n"
                f"To load using a specific infojson set:\n"
                f"config.base_info_type = 'any'")
        
        p_latest = self._metadata['pointers'].get('latest_flat_info')
        p_merge  = self._metadata['pointers'].get('_merge_flat')
        
        match self._config.base_info_type:
            case 'any':
                return _init_info
            
            case 'latest_flat':
                if self._infos.raw_flat: # extracted when getting init_info
                    return self._infos.raw_flat.data
                # need to check against 
                if p_latest and (not p_merge or p_merge[1] <= p_latest[1]) and not self._need_refresh(p_latest[1]):
                    return self.load('latest_flat_info')
                return self.extract_flat_info()
                
            case 'merge_flat':
                if self._infos._merge_flat: # updated from init flat_info extraction
                    return self._infos._merge_flat.data
                if p_merge and not self._need_refresh(p_merge[1]):
                    return self.load('_merge_flat')
                self.extract_flat_info() # has side effects on _merge_flat
                if not self._infos._merge_flat:
                    raise RuntimeError("_merge_flat should be written and set in self._infos")
                return self._infos._merge_flat.data



    # 
    # the init function
    # 

    def __init__(self, config: PlaylistDL_Config) -> None:
        self.session_start_epoch = utils.epoch_now()
        self._config = config

        self._infos = _Infos() # type: ignore - base_info None assignment is known and temporary
        init_info = self.__get_init_info() # may set self._infos.raw_flat
        
        self.id: str = init_info['id']
        self._pl_outtmpls = PlaylistDL.get_pl_outtmpls(self._config.home, self._config.path_tmpls, init_info)
        self.opts = self._config.opts | self.create_path_opts(self._config.home, self._pl_outtmpls)

        self._metadata = self._get_and_validate_metadata()
        self._yt_dlp_archive = self._get_and_validate_yt_dlp_archive()

        # __init__ requires special handling because pl_outtmpls weren't available yet
        # namely, self.__get_init_info().
        # Write after validations to prevent writing in a bad state.
        if self._infos.raw_flat:
            self._infos.raw_flat.pl_outtmpl = self._pl_outtmpls['raw_flat_infojson']
            if self._config.write_flat:
                self.write_info(self._infos.raw_flat, 'mov new')
            self.update_merge_flat_info([self._infos.raw_flat.data])
        
        self._infos.base_info = _InfosEntry(self._get_base_info_data(init_info), pl_outtmpl=None, is_written=True)

        # safe to do whatever now



    # 
    # API functions
    # 

    @overload
    @staticmethod
    def get_v_ids(info_entry: _InfosEntry[PL_InfoDict]) -> list[V_ID]: ...
    @overload
    @staticmethod
    def get_v_ids(info_entry: None) -> None: ...
    @staticmethod
    def get_v_ids(info_entry: _InfosEntry[PL_InfoDict]|None) -> list[V_ID]|None:
        if not info_entry:
            return None
        return [entry['id'] for entry in info_entry.data['entries']]

    @overload
    @staticmethod
    def get_v_id_to_index(info_entry: _InfosEntry[PL_InfoDict]) -> dict[V_ID, int]: ...
    @overload
    @staticmethod
    def get_v_id_to_index(info_entry: None) -> None: ...
    @staticmethod
    def get_v_id_to_index(info_entry: _InfosEntry[PL_InfoDict]|None) -> dict[V_ID, int]|None:
        if not info_entry:
            return None
        return {entry['id']: i for i, entry in enumerate(info_entry.data['entries'])}

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


    def write_info(
            self,
            info: _InfosEntry|None,
            collision_policy: utils.CollisionPolicies,
            name: str = '',
            alt_info: ANY_InfoDict = {},
            delete_prev: bool = False
    ) -> tuple[str, int]|None:
        """
        Call with any info from `self._infos`. If the info.data is not a dict (raw_v_infos),
        including `alt_info = {'epoch': ...}` is recommended.
        """

        if info is None:
            utils.ERROR("Info entry was not found")
            return None
        ident = name or info.metadata_key or info.pl_outtmpl
        if delete_prev and not info.metadata_key:
            raise ValueError(f"Deleting the previous requires a metadata_key (for {ident})")
        if info.is_written == True:
            utils.WARNING(f"Already written. Skipping. (for {ident})")
            return None
        if info.pl_outtmpl is None:
            raise ValueError(f"pl_outtmpl was not found (for {ident})")

        if not utils.has_content(info.data):
            utils.WARNING(f"{info.metadata_key or name} has no content. Writing anyway.")

        if delete_prev:
            match collision_policy:
                case 'mov new': collision_policy = 'rm new'
                case 'mov old': collision_policy = 'rm old'
        
        if isinstance(info.data, dict):
            epoch = yt_utils.get_epoch(info.data)
            if alt_info:
                _dst = yt_utils.eval_tmpl_with_alt_data(info.pl_outtmpl, info.data, alt_info)
            else:
                _dst = yt_utils.ytdlp_eval_tmpl(info.pl_outtmpl, info.data)
        else:
            epoch = yt_utils.get_epoch(alt_info)
            _dst = yt_utils.ytdlp_eval_tmpl(info.pl_outtmpl, alt_info) # can't use info.data to make path
        
        dst = utils.json_dump(self.get_filtered_data(info), _dst, collision_policy)
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
                    print(utils.hex(f"Removed {name or info.metadata_key or '\b'}: {stale_path}", fg="#c80053"))
            self._metadata['pointers'][info.metadata_key] = pointer

        print(utils.hex(f"Wrote {name or info.metadata_key or '\b'} to: {dst}", fg="#c800c8"))
        
        return pointer


    def load[T](self, info_type: _types._MetadataFiles_Lit, default: Any|T = utils.RAISE_EXC) -> Any|T:
        if info_type not in _types._MetadataPointers.__optional_keys__:
            raise ValueError(f"Unknown {info_type = }")
        
        pointer: tuple[str, int]|None = self._metadata['pointers'].get(info_type)
        if not pointer:
            if default is utils.RAISE_EXC:
                raise FileNotFoundError(f"{info_type} is not written according to metadata")
            return default
        path, _epoch = pointer
        return utils.json_load(os.path.join(self._config.home, path), default)


    def extract_flat_info(self, write: bool|type[USE_CONFIG]=USE_CONFIG, delete_prev: bool=False, cookiefile: str|None|type[USE_CONFIG] = USE_CONFIG) -> PL_InfoDict:
        """
        Updates `raw_flat`, `_merge_flat`, and `_metadata`

        Always calls update_merge_flat_info().
        """
        raw_flat_info = yt_utils.extract_flat_info(pl_url_or_id=self.id,
            opts=self.opts | {
                'cookiefile': cookiefile if cookiefile is not USE_CONFIG else \
                              self._config.cookie_file if self._config.cookies_for_vids else \
                              None}) # type: ignore
        self._infos.raw_flat = _InfosEntry(raw_flat_info, self._pl_outtmpls['raw_flat_infojson'], is_written=False, metadata_key='latest_flat_info')

        if write or (write is USE_CONFIG and self._config.write_flat):
            self.write_info(self._infos.raw_flat, collision_policy='mov new', delete_prev=delete_prev)
        self.update_merge_flat_info([self._infos.raw_flat.data])
        return self._infos.raw_flat.data

    def update_merge_flat_info(self, flat_infos: list[PL_InfoDict]) -> PL_InfoDict:
        """
        Updates `_merge_flat`, and `_metadata`
        """
        if self._infos._merge_flat:
            init_merge_flat = self._infos._merge_flat.data
        else:
            init_merge_flat: PL_InfoDict|None = self.load('_merge_flat', default=None)

        self._infos._merge_flat = _InfosEntry(
            merge_infos.merge_pl_infos(flat_infos, merge_updaters.latest_only, _init=init_merge_flat),
            self._pl_outtmpls['_merged_flat_infojson'],
            is_written=False,
            metadata_key='_merge_flat')
        
        return self._infos._merge_flat.data


    @staticmethod
    def _get_dl_result(v_info, success: bool) -> DL_Result:
        if not success:
            return DL_Result.FAIL
        if v_info is None:
            return DL_Result.CACHED # None is returned if download cache or cancelled.
        
        match yt_utils.get_v_info_level(v_info):
            case yt_utils.V_InfoLevel.DOWNLOAD: return DL_Result.DOWNLOAD
            case yt_utils.V_InfoLevel.EXTRACT:  return DL_Result.EXTRACT
            case _:
                return DL_Result.UNRECOGNIZED

    @staticmethod
    def _get_action_from_user(entry: V_InfoDict):
        DL_MAP_NO_USER = {str(action).lower(): action for action in DL_Action if action not in (DL_Action.USER, )}

        # TODO: show useful entry info for action choices
        print(f"[TEMP]:\n{pprint.pformat(entry, indent=4)}")

        choice = utils.input_string(
            list(DL_MAP_NO_USER.keys()),
            f"Pick a Download Option: ",
            prefix_options=True,
        )
        return DL_MAP_NO_USER[choice]
    
    @staticmethod
    def _download_v_infos(
            pl_info: PL_InfoDict[V_InfoDict],
            wrapper_match_filter: Callable[[V_InfoDict, PL_DownloadInfo], DL_Action]|None = None,
            opts: YT_DLP_Params = {},
            try_yt_if_unavailable: bool = True,
            wa: bool = True,
    ) -> tuple[list[V_InfoDict], PL_DownloadInfo]:
        """
        Extract (and download) videos. Return the extracted v_infos and download_info

        Args:
            wrapper_match_filter (Callable[[PL_V_InfoDict, PL_DownloadInfo], DL_Action]|None, optional):
                Called before downloading the video. Is given current playlist download information.
                Returns a download action to control the current playlist download.
                Defaults to None; this will extract and download every video not in the yt-dlp download archive.
            opts (YT_DLP_Params, optional): Extra opts used by ``download_video()``. Defaults to {}.
            try_yt_if_unavailable (bool, optional): Try Youtube even if it seems unavailable. Defaults to True.
            wa (bool, optional): Use archive.org if YouTube failed (fallback). Defaults to True.
        """
        extracted_v_infos: list[V_InfoDict] = []
        pl_dl_info: PL_DownloadInfo = []

        N = len(pl_info['entries'])

        try:
            for i, entry in enumerate(pl_info['entries']):
                action = DL_Action.DOWNLOAD
                if wrapper_match_filter is not None:
                    action = wrapper_match_filter(entry, pl_dl_info)
                
                i_of_N = f"{i+1:{len(str(N))}}/{N}"
                pl_v_display = f"[{i_of_N}] {yt_utils.get_v_display(entry)}"

                if action == DL_Action.USER:
                    action = PlaylistDL._get_action_from_user(entry)

                # do not add DL_Action.USER to dl_info
                pl_dl_info.append({
                    'id': entry['id'],
                    'title': entry.get('title'),
                    'action': action,
                    'result': DL_Result.CANCELLED,
                })

                if action == DL_Action.QUIT:
                    print(display.ACTION_TAG[DL_Action.QUIT].rendered + ' ' + utils.hex(pl_v_display, display.ACTION_TAG[action].color))
                    break
                elif action == DL_Action.SKIP:
                    print(display.ACTION_TAG[action].rendered + ' ' + utils.hex(pl_v_display, display.ACTION_TAG[action].color))
                    continue

                print()
                print(display.ACTION_TAG[action].rendered + ' ' + utils.hex(pl_v_display, display.ACTION_TAG[action].color))

                # v_info, errors, success = {}, [], True
                v_info, errors, success = yt_utils.download_video(
                    entry['id'],
                    opts=opts,
                    yt = try_yt_if_unavailable or yt_utils._maybe_available_on_yt(entry),
                    wa = wa,
                    download = (action == DL_Action.DOWNLOAD)
                )
                
                pl_dl_info[-1] = {
                    'id': entry['id'],
                    'title': (v_info or entry).get('title'),
                    'action': action,
                    'result': PlaylistDL._get_dl_result(v_info, success),
                }
                if errors:
                    pl_dl_info[-1]['errors'] = errors

                result_tag = display.download_result(pl_dl_info[-1])
                print(result_tag.rendered + ' ' + utils.hex(pl_v_display, result_tag.color))
                print()
                
                if v_info:
                    v_info.setdefault('id', entry['id'])
                    v_info.setdefault('epoch', utils.epoch_now())
                    extracted_v_infos.append(v_info)
        except KeyboardInterrupt:
            print(utils.hex("    KEYBOARD INTERRUPT    ", bg='#ffffff'))
        except Exception as e:
            print(utils.format_exception(e))
        
        return extracted_v_infos, pl_dl_info

    def download_v_infos(self, write: bool|type[USE_CONFIG] = USE_CONFIG, cookiefile: str|None|type[USE_CONFIG] = USE_CONFIG):
        """ Returns the newly downloaded portion of the raw v_infos """
        history_ids = yt_utils.ids_from_history(self._metadata['history'])
        yt_dlp_archive_ids = yt_utils.ids_from_yt_dlp_archive(self._yt_dlp_archive)

        print("\n ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n"
                "  Downloading Playlist Videos \n"
                " ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n")
        
        v_infos, pl_dl_info = PlaylistDL._download_v_infos(
            self._infos.base_info.data,
            lambda pl_v_info, pl_dl_info: self._config.wrapper_match_filter(
                pl_v_info, pl_dl_info,
                self._metadata['history'], history_ids,
                self._yt_dlp_archive, yt_dlp_archive_ids),
            opts=self.opts | {
                'cookiefile': cookiefile if cookiefile is not USE_CONFIG else \
                              self._config.cookie_file if self._config.cookies_for_vids else \
                              None}) # type: ignore
                
        if self._infos.raw_v_infos:
            self._infos.raw_v_infos.data.append(v_infos) # type: ignore - V_InfoDict
            self._infos.raw_v_infos.is_written = False
        else:
            self._infos.raw_v_infos = _InfosEntry([v_infos], self._pl_outtmpls['raw_video_infojson'], is_written=False) # type: ignore - V_InfoDict
        
        epoch: int = max((yt_utils.get_epoch(info) for info in v_infos), default=None) or utils.epoch_now()

        print("\n ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ \n"
                "  Playlist Videos Download Info  \n"
                " ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ \n")
        print(display.pl_download_info(pl_dl_info, errors=True))
        print()
        
        if write or (write is USE_CONFIG and self._config.write_raw_v_infos):
            self.write_info(self._infos.raw_v_infos, collision_policy='rm old', name='raw_v_infos', alt_info={'epoch': self.session_start_epoch})
        
        # special metadata
        self._metadata['history'][str(epoch)] = list(filter(self._config.meta_dl_history_filter, pl_dl_info))

        return v_infos, pl_dl_info


    @staticmethod
    def _download_v_info_generic(v_id: str, any_yt_dlp_url: str, opts: YT_DLP_Params) -> V_InfoDict|Exception|None:
        result: V_InfoDict|Exception|None = yt_utils.download_video_alt(any_yt_dlp_url, opts) # type: ignore
        epoch = utils.epoch_now() # no associatted v_info
        
        if not result:
            return None
        elif isinstance(result, Exception):
            return result
        
        if isinstance(result, str): # YoutubeDL.DownloadError
            result = {
                'id': v_id,
                'epoch': epoch,
                'unavailable_msgs': [{
                    'epoch': epoch,
                    'msg': result,
                    'type': utils.get_domain(any_yt_dlp_url) or any_yt_dlp_url,
                }],
            }
        else:
            result.setdefault('epoch', epoch)
            result['id'] = v_id
        return result

    def download_v_info_generic(self, v_id: str, any_yt_dlp_url: str, opts: YT_DLP_Params, write: bool|type[USE_CONFIG] = USE_CONFIG, cookiefile: str|None = None):
        """
        Only video downloads are added to metadata history.
        Added to raw_v_infos if DownloadError or there is a result.
        Normal Exceptions are just printed.

        Returns what was recieved from yt_dlp
        """
        if v_id not in self.get_v_ids(self._infos.base_info):
            raise ValueError(f"{v_id} is not in the loaded playlist")
        
        result = PlaylistDL._download_v_info_generic(v_id, any_yt_dlp_url, opts | {'cookiefile': cookiefile})
        if result is None:
            return
        elif isinstance(result, Exception):
            print(utils.format_exception(result))
            return result
        
        if not self._infos.raw_v_infos:
            self._infos.raw_v_infos = _InfosEntry([], self._pl_outtmpls['raw_video_infojson'], is_written=False)

        self._infos.raw_v_infos.data.append([result])
        if write or (write is USE_CONFIG and self._config.write_raw_v_infos):
            self.write_info(self._infos.raw_v_infos, collision_policy='rm old', name='raw_v_infos', alt_info={'epoch': self.session_start_epoch})
        return result


    def add_raw_v_infos(self, raw_v_infos: list[V_InfoDict]) -> list[V_InfoDict]:
        """ Returns the `raw_v_infos` that were added to `self._infos.raw_v_infos.data` """
        if not self._infos.raw_v_infos:
            self._infos.raw_v_infos = _InfosEntry([], self._pl_outtmpls['raw_video_infojson'], is_written=True)
        self._infos.raw_v_infos.data.append([])

        v_ids = set(self.get_v_ids(self._infos.base_info))
        for i, v_info in enumerate(raw_v_infos):
            v_display = yt_utils.get_v_display(v_info)
            if not v_info.get('id'):
                utils.WARNING(f"SKIPPED: {i} {v_display} has no id")
                continue
            if v_info.get('id') not in v_ids:
                utils.WARNING(f"SKIPPED: {i} {v_display} is not in the playlist")
                continue
            self._infos.raw_v_infos.data[-1].append(v_info)
        return self._infos.raw_v_infos.data[-1]
    

    @staticmethod
    def _make_pl_info(base_pl_info: PL_InfoDict, raw_v_infos: list[V_InfoDict], clean_info_json: bool):
        pl_info = yt_utils.copy_and_sanitize_info(base_pl_info, clean_info_json)
        if not raw_v_infos:
            return pl_info

        index_to_vid = [entry['id'] for entry in pl_info['entries']]
        vid_to_index = {id_: i for i, id_ in enumerate(index_to_vid)}

        for v_info in raw_v_infos:
            if v_info.get('id') not in index_to_vid:
                utils.WARNING(f"SKIP: {yt_utils.get_v_display(v_info)} is not in the playlist.")
                continue
            i = vid_to_index[v_info['id']]
            pl_info['entries'][i], _v_merge_timeline = merge_infos.merge_v_infos(
                [pl_info['entries'][i], yt_utils.copy_and_sanitize_info(v_info, clean_info_json)],
                field_updater=merge_updaters.latest, update_filter=lambda _: False)
            # TODO: Check if this merge udpater is actually a good fit

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
        if not self._infos.raw_v_infos:
            print("No raw_v_infos found. Downloading video infos using self.download_v_infos()")
            self.download_v_infos()
        raw_v_infos = []
        if self._infos.raw_v_infos:
            for v_infos in self._infos.raw_v_infos.data:
                raw_v_infos.extend(v_infos)
        clean_info_json = self.opts.get('clean_infojson') or False
        
        pl_info = PlaylistDL._make_pl_info(self._infos.base_info.data, raw_v_infos, clean_info_json)
        self._infos.pl_info = _InfosEntry(pl_info, self._pl_outtmpls['pl_infojson'], is_written=False, metadata_key='latest_pl_info')

        if write or (write is USE_CONFIG and self._config.write_pl_info):
            self.write_info(self._infos.pl_info, collision_policy='mov new',
                alt_info={'epoch': yt_utils.get_latest_epoch(pl_info)}, delete_prev=delete_prev)
        return pl_info
        

    def make_merge_info(
            self,
            write: bool | type[USE_CONFIG] = USE_CONFIG,
            delete_prev: bool = False,
            init_ident: PL_InfoDict | list[_types._MetadataFiles_Lit] = ['latest_merge_info', 'latest_pl_info', 'latest_flat_info', '_merge_flat'],
            field_updater: Callable[[V_InfoDict, str, Any|type[merge_infos.NO_VALUE], bool],bool] = merge_updaters.latest_not_none_and_latest_unavail,
            update_filter: Callable[[str], bool]|list = [
                'title',
                'description', 'categories', 'tags',
                'uploader', 'uploader_id', 'channel', 'creators', 'creator',
                'release_year', 'modified_date', 'availability',
                'duration',
                'extractor'
            ],
    ) -> PL_InfoDict:
        """
        Creates merge info using `init_ident` and the current run's pl_info.
        Returns the created merge info.
        
        May call ``make_pl_info()``, which may call ``download_v_infos()``.
        """
        init: PL_InfoDict|None = None
        if isinstance(init_ident, list):
            for file_type in init_ident:
                init = self.load(file_type, default=None)
                if init is not None:
                    break
        else:
            init = init_ident

        if not self._infos.pl_info:
            print("No pl_info found. Creating pl_info using self.make_pl_info()")
            self.make_pl_info()
            if not self._infos.pl_info: raise RuntimeError("Failed to make pl_info")

        if isinstance(update_filter, list):
            # need to put in a different variable
            __update_filter = lambda k: k in update_filter
        else:
            __update_filter = update_filter

        merge_info = merge_infos.merge_pl_infos(
            [yt_utils.copy_and_sanitize_info(self._infos.pl_info.data)],
            field_updater, __update_filter, _init=init)
        self._infos.merge_info = _InfosEntry(merge_info, self._pl_outtmpls['merge_infojson'], is_written=False, metadata_key='latest_merge_info')

        if write or (write is USE_CONFIG and self._config.write_merge):
            self.write_info(self._infos.merge_info, collision_policy='mov new',
                alt_info={'epoch': yt_utils.get_latest_epoch(merge_info)}, delete_prev=delete_prev)

        return merge_info



    def download(self):
        """ This is the recommended call order for the download functions """
        if self._config.write_raw_v_infos:
            self.download_v_infos()
        if self._config.write_pl_info:
            self.make_pl_info()
        if self._config.write_merge:
            self.make_merge_info()



    # 
    # Manipulation
    # Primarily effects base_info,
    # optionally mutate _merge_info for permanent changes
    #

    @staticmethod
    def add_to_merge_timeline(info: PL_InfoDict, timeline: PL_MergeTimeline):
        """ Input timeline wins collisions """
        utils.merge_objs(info, {'merge_timeline': timeline}, repr) # type: ignore

    @staticmethod
    def add_update_to_merge_timeline(info: PL_InfoDict, id: str, update_str: str, epoch_str: EPOCH_STR|None = None):
        """ Does not add if the update_str already exists. If epoch_str is None, use the current time """
        if epoch_str is None:
            epoch_str = yt_utils.to_readable_epoch(utils.epoch_now())
        if update_str in info.get('merge_timeline', {}).get(id, {}).get(epoch_str, {}).get('updates', []):
            return
        utils.merge_objs(info, {'merge_timeline': {id: {epoch_str: {'update': update_str}}}})

    __MUTATE_MERGE_FLAT_REQ_MSG = "To mutate_merge_flat (for persistence), the config.base_info_type must be 'merge_flat'"

    def remove(self, ids: Iterable[V_ID], mutate_merge_flat: bool = False):
        """Remove videos from the playlist by their IDs.

        Args:
            ids: Video IDs to remove from the playlist.
            mutate_merge_flat: If True, also update _merge_flat for persistence.
                Requires config.base_info_type == 'merge_flat'.

        Raises:
            ValueError: If mutate_merge_flat=True but base_info_type is not 'merge_flat'.
        """
        if mutate_merge_flat and self._config.base_info_type != 'merge_flat':
            raise ValueError(PlaylistDL.__MUTATE_MERGE_FLAT_REQ_MSG)

        ids_to_remove = set(ids)
        base_v_ids = set(self.get_v_ids(self._infos.base_info))
        extra = ids_to_remove - base_v_ids
        if mutate_merge_flat and self._infos._merge_flat:
            extra -= set(self.get_v_ids(self._infos._merge_flat))
        if extra:
            utils.WARNING(f"The ids {extra} are not in the playlist")

        self._infos.base_info.data['entries'] = [
            entry for entry in self._infos.base_info.data['entries']
            if entry['id'] not in ids_to_remove
        ]
        yt_utils.fixup_pl_info(self._infos.base_info.data)

        if mutate_merge_flat and self._infos._merge_flat:
            # Collect removed ids for timeline updates before modifying _merge_flat
            removed_ids = [entry['id'] for entry in self._infos._merge_flat.data['entries'] if entry['id'] in ids_to_remove]

            self._infos._merge_flat.data['entries'] = [
                entry for entry in self._infos._merge_flat.data['entries']
                if entry['id'] not in ids_to_remove
            ]
            yt_utils.fixup_pl_info(self._infos._merge_flat.data)

            for v_id in removed_ids:
                PlaylistDL.add_update_to_merge_timeline(self._infos._merge_flat.data, v_id, update_str='<REMOVE>')

    def insert(self, v_ids: Iterable[V_ID], index: int = 0, mutate_merge_flat: bool = False):
        """Insert new videos into the playlist at the specified index.

        By default adds to the start of the playlist (index=0, like YouTube).
        Like list.insert(), index can be negative and going out of bounds is
        clamped to the ends of the list.

        Args:
            v_ids: Video IDs to insert.
            index: Position to insert at. Defaults to 0 (start of playlist).
            mutate_merge_flat: If True, also update _merge_flat for persistence.
                Requires config.base_info_type == 'merge_flat'.

        Raises:
            ValueError: If mutate_merge_flat=True but base_info_type is not 'merge_flat',
                or if any of the v_ids are already in the playlist.
            AssertionError: If base_info and _merge_flat v_ids are out of sync.
        """
        if mutate_merge_flat and self._config.base_info_type != 'merge_flat':
            raise ValueError(PlaylistDL.__MUTATE_MERGE_FLAT_REQ_MSG)

        to_add = list(v_ids)
        v_ids = PlaylistDL.get_v_ids(self._infos.base_info)
        if mutate_merge_flat and self._infos._merge_flat \
           and v_ids != PlaylistDL.get_v_ids(self._infos._merge_flat):
            raise AssertionError(
                f"Mismatch between base_info and _merge_flat v_ids\n"
                f"base_info = {v_ids}\n"
                f"_merge_flat = {PlaylistDL.get_v_ids(self._infos._merge_flat)}")

        common_ids = list(filter(lambda x: x in set(v_ids), to_add))
        if common_ids:
            raise ValueError(f"The ids {common_ids} are already in the playlist")

        index = utils.insert_index_clamp(index, len(v_ids))

        new_v_infos = [yt_utils.min_v_info(id, yt_utils.V_InfoLevel.NONE) for id in to_add]
        self._infos.base_info.data['entries'][index:index] = new_v_infos
        yt_utils.fixup_pl_info(self._infos.base_info.data)

        if mutate_merge_flat and self._infos._merge_flat:
            self._infos._merge_flat.data['entries'][index:index] = copy.deepcopy(new_v_infos)
            yt_utils.fixup_pl_info(self._infos._merge_flat.data)
            for v_id in to_add:
                PlaylistDL.add_update_to_merge_timeline(self._infos._merge_flat.data, v_id, update_str='<INSERT>')

    def replace(self, replacements: Iterable[tuple[V_ID, V_ID]], mutate_merge_flat: bool = False):
        """Replace video IDs with new IDs while keeping the same positions.

        Args:
            replacements: Iterable of (old_id, new_id) tuples specifying replacements.
                The new_id must not already be in the playlist (unless it's being
                replaced in the same batch).
            mutate_merge_flat: If True, also update _merge_flat for persistence.
                Requires config.base_info_type == 'merge_flat'.

        Raises:
            ValueError: If mutate_merge_flat=True but base_info_type is not 'merge_flat',
                if an old_id is not in the playlist, or if a new_id already exists.
            AssertionError: If base_info and _merge_flat v_ids are out of sync.
        """
        if mutate_merge_flat and self._config.base_info_type != 'merge_flat':
            raise ValueError(PlaylistDL.__MUTATE_MERGE_FLAT_REQ_MSG)

        replacements = list(replacements)
        base_v_ids = PlaylistDL.get_v_ids(self._infos.base_info)

        if mutate_merge_flat and self._infos._merge_flat \
           and base_v_ids != PlaylistDL.get_v_ids(self._infos._merge_flat):
            raise AssertionError(
                f"Mismatch between base_info and _merge_flat v_ids\n"
                f"base_info = {base_v_ids}\n"
                f"_merge_flat = {PlaylistDL.get_v_ids(self._infos._merge_flat)}")

        old_ids = {old_id for old_id, _ in replacements}
        new_ids = {new_id for _, new_id in replacements}

        # Check for overlap between old and new (same id being replaced and used as target)
        overlap = old_ids & new_ids
        if overlap:
            raise ValueError(f"The ids {overlap} cannot be both old and new in replacements")

        # Check old_ids exist
        missing_old = old_ids - set(base_v_ids)
        if missing_old:
            raise ValueError(f"The old_ids {missing_old} are not in the playlist")

        # Check new_ids don't exist (excluding those being replaced)
        existing_new = new_ids - set(base_v_ids) - old_ids
        if existing_new:
            raise ValueError(f"The new_ids {existing_new} are already in the playlist")

        # Build id map for base_info
        old_to_new = {old_id: new_id for old_id, new_id in replacements}
        for entry in self._infos.base_info.data['entries']:
            if entry['id'] in old_ids:
                old_id = entry['id']
                entry['id'] = old_to_new[old_id]
        yt_utils.fixup_pl_info(self._infos.base_info.data)

        if mutate_merge_flat and self._infos._merge_flat:
            for entry in self._infos._merge_flat.data['entries']:
                if entry['id'] in old_ids:
                    old_id = entry['id']
                    new_id = old_to_new[old_id]
                    entry['id'] = new_id
                    PlaylistDL.add_update_to_merge_timeline(
                        self._infos._merge_flat.data, new_id,
                        update_str=f'<REPLACE from={old_id} to={new_id}>')
            yt_utils.fixup_pl_info(self._infos._merge_flat.data)

    def move(self, v_id: V_ID, index: int, mutate_merge_flat: bool = False):
        """Move a video to a new position in the playlist.
        
        # 0-indexed !!!

        Args:
            v_id: Video ID to move.
            index: Target position. Clamped to valid range. Can be negative.
            mutate_merge_flat: If True, also update _merge_flat for persistence.
                Requires config.base_info_type == 'merge_flat'.

        Raises:
            ValueError: If mutate_merge_flat=True but base_info_type is not 'merge_flat',
                or if v_id is not in the playlist.
            AssertionError: If base_info and _merge_flat v_ids are out of sync.
        """
        if mutate_merge_flat and self._config.base_info_type != 'merge_flat':
            raise ValueError(PlaylistDL.__MUTATE_MERGE_FLAT_REQ_MSG)

        base_entries = self._infos.base_info.data['entries']
        base_v_ids = PlaylistDL.get_v_ids(self._infos.base_info)

        if mutate_merge_flat and self._infos._merge_flat \
           and base_v_ids != PlaylistDL.get_v_ids(self._infos._merge_flat):
            raise AssertionError(
                f"Mismatch between base_info and _merge_flat v_ids\n"
                f"base_info = {base_v_ids}\n"
                f"_merge_flat = {PlaylistDL.get_v_ids(self._infos._merge_flat)}")

        if v_id not in base_v_ids:
            raise ValueError(f"{v_id} is not in the playlist")

        # Find current index
        old_index = base_v_ids.index(v_id)
        index = utils.insert_index_clamp(index, len(base_entries))

        # Remove from old position and insert at new position
        entry = base_entries.pop(old_index)
        base_entries.insert(index, entry)
        yt_utils.fixup_pl_info(self._infos.base_info.data)

        if mutate_merge_flat and self._infos._merge_flat:
            merge_entries = self._infos._merge_flat.data['entries']
            merge_v_ids = PlaylistDL.get_v_ids(self._infos._merge_flat)

            old_index = merge_v_ids.index(v_id)
            entry = merge_entries.pop(old_index)
            merge_entries.insert(index, entry)
            yt_utils.fixup_pl_info(self._infos._merge_flat.data)
            PlaylistDL.add_update_to_merge_timeline(
                self._infos._merge_flat.data, v_id,
                update_str=f'<MOVE from={old_index} to={index}>')



    # 
    # Cleanup
    # 

    def write_metadata_file(self):
        print(utils.hex(f"Updated metadata: {self._pl_outtmpls['metadata']}", fg="#c800c8"))
        utils.json_dump(self._metadata, self._pl_outtmpls['metadata'], on_collision='rm old')

    def empty_cookies(self):
        if self._config.cookie_file and os.path.exists(self._config.cookie_file):
            with open(self._config.cookie_file, 'w'):
                ...
            print(utils.hex(f"Emptied cookie file: {self._config.cookie_file}", fg="#c80053"))

    def close(self):
        self.write_metadata_file()
        if self._config.empty_cookies:
            self.empty_cookies()
        pointer = self.write_info(self._infos._merge_flat, collision_policy='rm old', delete_prev=True)
        if not pointer:
            utils.WARNING("_merge_flat failed to write.")

    def __enter__(self):
        # everythig is handeled by __init__()
        return self
    
    def __exit__(self, *args):
        self.close()
    