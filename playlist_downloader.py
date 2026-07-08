__all__ = [
    'PlaylistDL',
    'PlaylistDL_Config', 'ConfigID_Type'
]

import os

from config import PlaylistDL_Config
from yt_types import *
import yt_types
import utils
import yt_utils
import yt_wrapper
import post_processing

import display



class PlaylistDL:
    def __init__(self, config: PlaylistDL_Config) -> None:
        self.config = config

        # Get Playlist Info

        self.pl_info, self.is_new_pl_info = self.get_init_info()
        self.pl_outtmpls = self.get_paths()

        self.old_metadata: Metadata|None = utils.json_load_typeddict(self.pl_outtmpls['metadata'], Metadata, default=None)
        self.metadata: Metadata = yt_types.empty_Metadata()
        self.metadata['id'] = self.pl_info['id']
        self.metadata['pl_epoch'] = self.pl_info.get('epoch', 0)
        self.metadata['history'] = {} if not self.old_metadata else self.old_metadata['history']
        self.metadata['path_tmpls'] = self._meta_outtmpls(self.config.home, self.pl_outtmpls)
        
        PlaylistDL._validate_metadata(self.old_metadata, self.metadata)
        # ``_validate_metadata()`` may raise an exception which will prevent the flat pl_info from being written.
        # This is intentional, but not ideal.
        # A way to have flat written anyway would be to write the flat pl_info to a temp folder.

        if config.write_flat and self.is_new_pl_info:
            self.metadata['latest_flat_info'] = yt_utils.ytdlp_eval_tmpl(self.pl_outtmpls['flat_infojson'], self.pl_info)
            utils.json_dump(self.pl_info, dst=self.metadata['latest_flat_info'], on_collision='mov new', auto_rename=True)
        
        self.history: PL_DownloadHistory = dict() if not self.old_metadata else self.old_metadata.get('history', dict())
        self.history_ids: ID_DownloadInfo = yt_utils.ids_from_history(self.history)
        
        self.ytdlp_archive: YT_DLP_DownloadArchive = yt_wrapper.load_yt_archive(self.metadata['path_tmpls']['ytdlp_archive'])
        self.ytdlp_archive_ids: list[V_ID] = yt_utils.ids_from_ytdlp_archive(self.ytdlp_archive)
        PlaylistDL._validate_dl_archive_sync(self.ytdlp_archive, self.metadata)

        # Playlist Video Extraction/Download

        self.opts = (
              self.config.opts
            | PlaylistDL.create_path_opts(self.config.home, self.pl_outtmpls)
            | {'cookiefile': self.config.cookie_file if self.config.cookies_for_vids else None}
        )
        self.config.edit_final_opts_in_place(self.opts)

        def wrapper_match_filter(pl_v_info: PL_V_InfoDict, curr_dl_info: PL_DownloadInfo):
            return self.config.wrapper_match_filter(pl_v_info, curr_dl_info,
                self.history,
                self.history_ids,
                self.ytdlp_archive,
                self.ytdlp_archive_ids,
            )

        pl_dl_info = yt_wrapper.download_pl_videos(
            pl_info              = self.pl_info,
            wrapper_match_filter = wrapper_match_filter,
            opts                 = self.opts)
        if self.config.empty_cookies and self.config.cookie_file:
            with open(self.config.cookie_file, 'w'): ... # clear cookie file
        
        id_dl_info = yt_utils.ids_from_pl_download_info(pl_dl_info)
        has_new_v_info = bool(id_dl_info['extract'] or id_dl_info['download'])
        if has_new_v_info:
            self.metadata['v_epoch'] = utils.epoch_now()
        self.metadata['history'][str(utils.epoch_now())] = pl_dl_info

        if self.config.write_pl_info:
            if not has_new_v_info:
                utils.WARNING("pl_info is the same as flat_info")
            self.metadata['latest_pl_info'] = yt_utils.eval_with_dif_epoch(
                self.pl_info,
                post_processing.get_latest_epoch(self.pl_info),
                self.pl_outtmpls['pl_infojson'])
            utils.json_dump(self.pl_info, self.metadata['latest_pl_info'])

        if self.config.write_merge:
            self.pl_info = self.get_merge_info()
            self.metadata['latest_merge_info'] = yt_utils.eval_with_dif_epoch(
                self.pl_info,
                post_processing.get_latest_epoch(self.pl_info),
                self.pl_outtmpls['merge_infojson'])
            if not self.config.merge_keep_one:
                utils.json_dump(self.pl_info, self.metadata['latest_merge_info'], on_collision='mov new')
            else:
                utils.json_dump(self.pl_info, self.metadata['latest_merge_info'], on_collision='rm old')
                if (self.old_metadata
                        and self.metadata['latest_merge_info'] != self.old_metadata['latest_merge_info']
                        and self.old_metadata['latest_merge_info']
                        and os.path.exists(self.old_metadata['latest_merge_info'])):
                    os.unlink(self.old_metadata['latest_merge_info'])

        utils.json_dump(self.metadata, self.pl_outtmpls['metadata'], 'rm old')
        display.pl_download_info(pl_dl_info, errors=True)


    def _need_refresh(self, epoch: int):
        time_since = utils.epoch_now() - epoch
        return time_since > self.config.refresh_after

    def get_init_info(self) -> tuple[PL_InfoDict, bool]:
        """
        Based on the config playlist identifier, do one of:
        - Extract flat info from id
        - Load past playlist info, extract if old
        - Load lastest_flat_path from metadata, extract if old

        Something is old if more than `refresh_after` time has passed since the stored epoch.
            (if no epoch, assume old)
        """

        def extract_flat_info(id: str):
            return yt_wrapper.extract_flat_info(id, opts= {} if self.config.cookies_for_pl else {'cookiefile': self.config.cookie_file})

        if self.config.ident_type == ConfigID_Type.PLAYLIST_ID:
            return extract_flat_info(self.config.ident), True
        
        elif self.config.ident_type == ConfigID_Type.PL_INFO_PATH:
            info: PL_InfoDict = utils.json_load_typeddict(self.config.ident, PL_InfoDict)
            if self._need_refresh(info.get('epoch', 0)):
                return extract_flat_info(info['id']), True
            return info, False
        
        elif self.config.ident_type == ConfigID_Type.METADATA_PATH:
            old_metadata: Metadata = utils.json_load_typeddict(self.config.ident, Metadata)
            
            if self._need_refresh(old_metadata['pl_epoch']):
                return extract_flat_info(old_metadata['id']), True
            
            # one should match old_metadata['pl_epoch']. If none match, extract new because the old_metadata is malformed.
            for k in ['latest_merge_info', 'latest_pl_info', 'latest_flat_info']:
                if p := old_metadata.get(k):
                    info = utils.json_load_typeddict(p, PL_InfoDict)
                    if info.get('epoch') == old_metadata['pl_epoch']:
                        return info, False
            utils.WARNING("Malformed metadata 'pl_epoch'")
            return extract_flat_info(old_metadata['id']), True
                
        raise ValueError("No playlist identificaiton found !!!\nCheck config.py validations")


    def get_paths(self) -> PL_Resolved_CustomOuttmpl:
        """ create resolved paths from config

        Returns:
            tuple[YT_DLP_Params, RequiredPaths]:
            - `paths`, `outtmpl`, and `download_path` Params
            - `RequiredPaths` are all absolute paths
        
        Defaults from `DEFAULT_OUTTMPL`, `OUTTMPL_TYPES` (in yt_dlp/utils/_utils.py)    
        field_reference: https://github.com/yt-dlp/yt-dlp#output-template
        """

        PATH_TMPLS = self.config.path_tmpls
        Home = self.config.home
        
        if callable(PATH_TMPLS['Playlist']):
            Playlist = PATH_TMPLS['Playlist'](self.pl_info)
        else:
            Playlist = yt_utils.ytdlp_eval_tmpl(PATH_TMPLS['Playlist'], self.pl_info)

        pl_outtmpls: PL_Resolved_CustomOuttmpl = {
            'Playlist':         os.path.join(Home, Playlist),

            'video_file':       os.path.join(Home, Playlist, PATH_TMPLS['video_file']),

            'flat_infojson':    os.path.join(Home, Playlist, PATH_TMPLS['flat_infojson']),
            'pl_infojson':      os.path.join(Home, Playlist, PATH_TMPLS['pl_infojson']),
            'merge_infojson':   os.path.join(Home, Playlist, PATH_TMPLS['merge_infojson']),

            'ytdlp_archive':    os.path.join(Home, Playlist, PATH_TMPLS['ytdlp_archive']),
            'metadata':         os.path.join(Home, Playlist, PATH_TMPLS['metadata']),
        }

        for k in CustomOuttmpl.__optional_keys__:
            if k in PATH_TMPLS:
                pl_outtmpls[k]= os.path.join(Home, Playlist, PATH_TMPLS[k])

        return pl_outtmpls
    
    @staticmethod
    def create_path_opts(home: str, pl_outtmpls: PL_Resolved_CustomOuttmpl) -> YT_DLP_Params:
        def rel_to_home(p: str):
            return os.path.relpath(p, home)

        opt_outpaths: YT_DLP_Params = {
            'paths': {'home': home}, # type: ignore - Home directory of all outtmpl (there's also `temp`)
            'outtmpl': {
                'default':  rel_to_home(pl_outtmpls['video_file']),
                # infojsons and metadata are custom
            },
            'download_archive': rel_to_home(pl_outtmpls['ytdlp_archive']),
        }
        for k in PL_Resolved_CustomOuttmpl.__optional_keys__:
            if k in pl_outtmpls:
                opt_outpaths['outtmpl'][k] = rel_to_home(pl_outtmpls[k]) # type: ignore - 'outtmpl' is defined as a dict.

        return opt_outpaths

    @staticmethod
    def _meta_outtmpls(home: str, pl_outtmpls: PL_Resolved_CustomOuttmpl) -> PL_Resolved_CustomOuttmpl:
        res: PL_Resolved_CustomOuttmpl = {} # type: ignore - init
        Playlist = pl_outtmpls['Playlist']
        for k, p in pl_outtmpls.items():
            if isinstance(p, str):
                res[k] = os.path.relpath(p, Playlist)
        res['Playlist'] = os.path.relpath(Playlist, home)
        return res


    @staticmethod
    def _validate_metadata(old_metadata: Metadata|None, current_metadata: Metadata):
        if not old_metadata:
            return
        
        for k in yt_types._MetadataFiles.__required_keys__:
            utils.assert_file(old_metadata['path_tmpls'][k], f'{k} (metadata)', or_None=True)

        if old_metadata['path_tmpls'] != current_metadata['path_tmpls']:
            raise ValueError(
                f"Old metadata's 'path_tmpls' does not match generated pl_outtmpls.\n"
                f"Old:\n{old_metadata['path_tmpls']}\n"
                f"Generated:\n{current_metadata['path_tmpls']}")

    @staticmethod
    def _validate_dl_archive_sync(yt_dlp_archive: YT_DLP_DownloadArchive, metadata: Metadata):
        ytdlp_dl = set(yt_utils.ids_from_ytdlp_archive(yt_dlp_archive))
        hist_dl = set(yt_utils.ids_from_history(metadata['history'])['download'])
        if ytdlp_dl != hist_dl:
            raise ValueError(f"Detected download state mismatch:\nytdlp-only: {ytdlp_dl - hist_dl}\nhist-only: {hist_dl - ytdlp_dl}")


    def get_merge_info(self) -> PL_InfoDict:
        infos = [self.pl_info]
        for k in self.config.merge_fallback_order:
            if not self.old_metadata:
                break
            if info_path := self.old_metadata.get(k):
                if info := utils.json_load_typeddict(info_path, PL_InfoDict, default=None):
                    infos.append(info)
                    break
        return post_processing.merge_pl_infos(infos)
        

