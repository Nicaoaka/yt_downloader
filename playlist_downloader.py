__all__ = ['PlaylistDL']

import os
import copy

from yt_types import *
import yt_types
import config
import utils
import yt_utils
import yt_wrapper
import post_processing

import display



class PlaylistDL:
    def __init__(self, config: config.PlaylistDL_Config) -> None:
        self.config = config

        # Get Playlist Info

        self.pl_info, self.new_pl_info = self._get_init_info()
        self.pl_outtmpls = self._get_paths()

        self.old_metadata: Metadata|None = utils.json_load_typeddict(self.pl_outtmpls['metadata'], Metadata, default=None)
        self.metadata: Metadata = copy.deepcopy(self.old_metadata) or yt_types.empty_Metadata()
        self.metadata['id'] = self.pl_info['id']
        self.metadata['pl_epoch'] = self.pl_info.get('epoch', 0)
        self.metadata['history'] = {} if not self.old_metadata else self.old_metadata['history']
        self.metadata['path_tmpls'] = self.meta_outtmpls(self.config.home, self.pl_outtmpls)
        
        self._validate_metadata()
        # ``_validate_metadata()`` may raise an exception which will prevent the flat pl_info from being written.
        # This is intentional, but not ideal.
        # A way to have flat written anyway would be to write the flat pl_info to a temp folder.

        if config.write_flat:
            self._write_flat_info()
        
        self.history: PL_DownloadHistory = dict() if not self.old_metadata else self.old_metadata.get('history', dict())
        self.history_ids: ID_DownloadInfo = yt_utils.ids_from_history(self.history)
        
        self.ytdlp_archive: YT_DLP_DownloadArchive = yt_wrapper.load_yt_archive(self.pl_outtmpls['ytdlp_archive'])
        self.ytdlp_archive_ids: YT_DLP_DownloadArchive_IDs = yt_utils.ids_from_ytdlp_archive(self.ytdlp_archive)
        PlaylistDL.validate_dl_archive_sync(self.ytdlp_archive, self.metadata)

        # Playlist Video Extraction/Download

        self.opts = (
              self.config.opts
            | PlaylistDL.create_path_opts(self.config.home, self.pl_outtmpls)
            | {'cookiefile': self.config.cookie_file if self.config.cookies_for_v else None}
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
        self.new_v_info = bool(id_dl_info['extract'] or id_dl_info['download'])

        if self.new_v_info:
            self.metadata['v_epoch'] = utils.epoch_now()
        self.metadata['history'][str(utils.epoch_now())] = pl_dl_info

        if self.config.write_pl_info:
            self._write_pl_info()
        
        if self.config.write_merge:
            self._write_merge_info()

        utils.json_dump(self.metadata, self.pl_outtmpls['metadata'], 'rm old')
        display.pl_download_info(pl_dl_info, errors=True)


    def _rel_to_Playlist(self, p: str):
        return os.path.relpath(p, self.pl_outtmpls['Playlist'])
    def _join_to_Playlist(self, p: str):
        return os.path.join(self.pl_outtmpls['Playlist'], p)


    def _need_refresh(self, epoch: int):
        time_since = utils.epoch_now() - epoch
        return time_since > self.config.refresh_after

    def _get_init_info(self) -> tuple[PL_InfoDict, bool]:
        """
        Based on the config playlist identifier, do one of:
        - Extract flat info from id
        - Load past playlist info, extract if old
        - Load lastest_flat_path from metadata, extract if old

        Something is old if more than `refresh_after` time has passed since the stored epoch.
            (if no epoch, assume old)
        """

        def extract_flat_info(id: str):
            return yt_wrapper.extract_flat_info(
                pl_url_or_id=id,
                opts={'cookiefile': self.config.cookie_file if self.config.cookies_for_pl else None})

        if self.config.ident_type == Config_IdentType.PLAYLIST_ID:
            return extract_flat_info(self.config.ident), True
        
        elif self.config.ident_type == Config_IdentType.PL_INFO_PATH:
            info: PL_InfoDict = utils.json_load_typeddict(self.config.ident, PL_InfoDict)
            if self._need_refresh(info.get('epoch', 0)):
                return extract_flat_info(info['id']), True
            return info, False
        
        elif self.config.ident_type == Config_IdentType.METADATA_PATH:
            old_metadata: Metadata = utils.json_load_typeddict(self.config.ident, Metadata)
            
            if self._need_refresh(old_metadata['pl_epoch']):
                return extract_flat_info(old_metadata['id']), True
            
            # One should match old_metadata['pl_epoch'].
            # Find the most recent smallest one.
            # The best info should be made using merging in post.
            for k in ['latest_flat_info', 'latest_pl_info', 'latest_merge_info']:
                if p := old_metadata.get(k):
                    info = utils.json_load_typeddict(os.path.join(self.config.home, old_metadata['path_tmpls']['Playlist'], p), PL_InfoDict)
                    if info.get('epoch') == old_metadata['pl_epoch']:
                        return info, False
            raise ValueError("Malformed metadata 'pl_epoch'")
        
        raise ValueError("No playlist identificaiton found !!!\nCheck config.py validations")


    def _get_paths(self) -> PL_Resolved_CustomOuttmpl:
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
            'download_archive': pl_outtmpls['ytdlp_archive'],
        }
        for k in PL_Resolved_CustomOuttmpl.__optional_keys__:
            if k in pl_outtmpls:
                opt_outpaths['outtmpl'][k] = rel_to_home(pl_outtmpls[k]) # type: ignore - 'outtmpl' is defined as a dict.

        return opt_outpaths

    @staticmethod
    def meta_outtmpls(home: str, pl_outtmpls: PL_Resolved_CustomOuttmpl) -> PL_Resolved_CustomOuttmpl:
        res: PL_Resolved_CustomOuttmpl = {} # type: ignore - init
        Playlist = pl_outtmpls['Playlist']
        for k, p in pl_outtmpls.items():
            if isinstance(p, str):
                res[k] = os.path.relpath(p, Playlist)
        res['Playlist'] = os.path.relpath(Playlist, home)
        return res


    def _validate_metadata(self):
        if not self.old_metadata:
            return
        
        if self.config.ident_type != Config_IdentType.METADATA_PATH:
            config.validate_metdata(self.old_metadata, self.config)

        if self.old_metadata['path_tmpls'] != self.metadata['path_tmpls']:
            raise ValueError(
                f"Found changed `Playlist` outtmpl.\n"
                f"{self.old_metadata['path_tmpls']['Playlist']} -> {self.metadata['path_tmpls']['Playlist']}")

    @staticmethod
    def validate_dl_archive_sync(yt_dlp_archive: YT_DLP_DownloadArchive, metadata: Metadata):
        ytdlp_dl = set(yt_utils.ids_from_ytdlp_archive(yt_dlp_archive))
        hist_dl = set(yt_utils.ids_from_history(metadata['history'])['download'])
        if ytdlp_dl != hist_dl:
            raise ValueError(
                f"Detected download state mismatch:\n"
                f"ytdlp-only: {ytdlp_dl - hist_dl}\n"
                f"hist-only: {hist_dl - ytdlp_dl}")


    def _write_flat_info(self):
        if not self.new_pl_info:
            return

        self.metadata['latest_flat_info'] = yt_utils.ytdlp_eval_tmpl(self.pl_outtmpls['flat_infojson'], self.pl_info)
        self.metadata['latest_flat_info'] = self._rel_to_Playlist(self.metadata['latest_flat_info'])
        utils.json_dump(
            self.pl_info,
            self._join_to_Playlist(self.metadata['latest_flat_info']),
            on_collision='mov old',
            auto_rename=True)


    def _write_pl_info(self):
        if not self.new_pl_info and not self.new_v_info:
            return
        
        self.metadata['latest_pl_info'] = yt_utils.eval_with_dif_epoch(
            self.pl_info,
            post_processing.get_latest_epoch(self.pl_info),
            self.pl_outtmpls['pl_infojson'])
        self.metadata['latest_pl_info'] = self._rel_to_Playlist(self.metadata['latest_pl_info'])
        utils.json_dump(
            self.pl_info,
            self._join_to_Playlist(self.metadata['latest_pl_info']),
            on_collision = 'mov old')


    def _get_prev_best_info(self) -> PL_InfoDict|None:
        if not self.old_metadata:
            utils.WARNING("No metadata found. Merge will be the same as playlist info.")
            return None
        for k in self.config.merge_fallback_order:
            if info := utils.json_load_typeddict(self._join_to_Playlist(self.old_metadata.get(k, None)), PL_InfoDict, default=None):
                return info
        utils.WARNING("No info found in metadata. Merge will be the same as playlist info.")
        return None

    def _write_merge_info(self):
        if not self.new_pl_info and not self.new_v_info:
            return
        if last_best_info := self._get_prev_best_info():
            self.pl_info = post_processing.merge_pl_infos([self.pl_info, last_best_info])
        self.metadata['latest_merge_info'] = yt_utils.eval_with_dif_epoch(
            self.pl_info,
            post_processing.get_latest_epoch(self.pl_info),
            self.pl_outtmpls['merge_infojson'])
        self.metadata['latest_merge_info'] = self._rel_to_Playlist(self.metadata['latest_merge_info'])
        utils.json_dump(
            self.pl_info,
            self._join_to_Playlist(self.metadata['latest_merge_info']),
            on_collision='rm old' if self.config.merge_keep_one else 'mov old')
        
        if (self.config.merge_keep_one
                and self.old_metadata
                and self.old_metadata['latest_merge_info']
                and self.metadata['latest_merge_info'] != self.old_metadata['latest_merge_info']
                and os.path.exists(self._join_to_Playlist(self.old_metadata['latest_merge_info']))):
            os.unlink(self._join_to_Playlist(self.old_metadata['latest_merge_info']))
