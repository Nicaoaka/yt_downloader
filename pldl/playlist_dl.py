__all__ = ['PlaylistDL']

import os
import copy
from typing import Callable, Any, overload
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
                self.write_info(self._infos.raw_flat, 'mov new', name='raw flat')
            self.update_merge_flat_info([self._infos.raw_flat.data])
        
        self._infos.base_info = _InfosEntry(self._get_base_info_data(init_info), pl_outtmpl=None, is_written=True)

        # safe to do whatever now

        self.index_to_vid = [entry['id'] for entry in self._infos.base_info.data.get('entries', [])] # 0-indexed
        self.vid_to_index = {id_: i for i, id_ in enumerate(self.index_to_vid)}
        self.v_ids_set = set(self.index_to_vid)



    # 
    # API functions
    # 
    @overload
    def get_filtered_data[T](self, info: _InfosEntry[T]) -> T: ...
    @overload
    def get_filtered_data(self, info: None) -> None: ...
    def get_filtered_data[T](self, info: _InfosEntry[T]|None) -> T|None:
        if not info:
            return None
        filtered_data = yt_utils.copy_and_sanitize_info(info.data)
        self._config.filter_all_info(filtered_data)
        match info.metadata_key:
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
            self.write_info(self._infos.raw_flat, collision_policy='mov new', name='raw flat', delete_prev=delete_prev)
        self.update_merge_flat_info([self._infos.raw_flat.data])
        return self._infos.raw_flat.data

    def update_merge_flat_info(self, flat_infos: list[PL_InfoDict], delete_prev: bool = True) -> PL_InfoDict:
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
        
        pointer = self.write_info(self._infos._merge_flat, collision_policy='rm old', name='_merge_flat', delete_prev=delete_prev)
        if not pointer:
            raise RuntimeError("_merge_flat should always write.")
        
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
        if v_id not in self.v_ids_set:
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

        for i, v_info in enumerate(raw_v_infos):
            v_display = yt_utils.get_v_display(v_info)
            if not v_info.get('id'):
                utils.WARNING(f"SKIPPED: {i} {v_display} has no id")
                continue
            if v_info.get('id') not in self.v_ids_set:
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
            pl_info['entries'][i], _v_merge_timeline = merge_infos.merge_v_infos( # type: ignore - pl_v_info added later
                [pl_info['entries'][i], yt_utils.copy_and_sanitize_info(v_info, clean_info_json)],
                field_updater=merge_updaters.latest, update_filter=lambda _: False)

        yt_utils.add_pl_info_to_entries(pl_info)
        return pl_info

    def make_pl_info(self, write: bool|type[USE_CONFIG] = USE_CONFIG, delete_prev: bool=False) -> PL_InfoDict:
        """
        Create pl_info from `base_info` and `raw_v_infos`.
        
        Videos with ids not in `base_info`, will be skipped.
        Only keeps the most recent v_info.
        Prefers raw_v_info over base_info.
        Does not merge.
            TODO - create merge for keeping useful info

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
                name='pl_info', alt_info={'epoch': yt_utils.get_latest_epoch(pl_info)}, delete_prev=delete_prev)
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
                name='merge_info', alt_info={'epoch': yt_utils.get_latest_epoch(merge_info)}, delete_prev=delete_prev)

        return merge_info



    def download(self):
        """ This is the recommended call order for the download functions """
        if self._config.write_raw_v_infos:
            self.download_v_infos()
        if self._config.write_pl_info:
            self.make_pl_info()
        if self._config.write_merge:
            self.make_merge_info()



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

    def __enter__(self):
        # everythig is handeled by __init__()
        return self
    
    def __exit__(self, *args):
        self.close()
    