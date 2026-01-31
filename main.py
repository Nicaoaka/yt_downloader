import json
from pathlib import Path
from typing import TYPE_CHECKING, Literal, TypedDict, Any, Required, NotRequired, Callable
import re
from string import Formatter
import datetime




from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, sanitize_filename

if TYPE_CHECKING:
    from yt_dlp import _Params
    type _Archives = Literal['playlist', 'global'] | None

    # copied from yt_dlp
    class _InfoDict(TypedDict):
        age_limit: int
        availability: Literal["private", "premium_only", "subscriber_only", "needs_auth", "unlisted", "public"] | None
        available_at: int
        creator: str | None
        comment_count: int | None
        duration: int | None
        formats: list[dict[str, Any]] | None
        id: Required[str]
        like_count: int | None
        tags: list[str] | None
        thumbnail: str | None
        timestamp: int | float | None
        title: str | None
        uploader: str | None
        url: str | None

        # custom
        is_unavailable: NotRequired[bool]
        unavailable_reason: NotRequired[str]

    # custom
    class _PL_InfoDict(_InfoDict):
        playlist_count: int
        entries: list[_InfoDict]

    type _id = str
    type _IE_Key = str

# # Recommended (path to binary files/.exe)
# FFMPEG_LOCATION: str|Path   = r'C:\ffmpeg-master-latest-win64-gpl\bin'
# COOKIE_FILE: str|Path = ""

# # If previously downloaded (file should exist) (relative to CWD or absolute)
# FLAT_INFO_FILE: str|Path|None   = r''
# INFO_LOCATION: str|Path|None    = r''

# CLEAN_JSON: bool                = False

# QUIET: bool                     = False
# VERBOSE: bool                   = False
# VERBOSE_SCRIPT: bool            = True

# MIN_SLEEP_INTERVAL              = 3
# MAX_SLEEP_INTERVAL              = 15
# BYTES_RATE_LIMIT                = 10_000_000

# # Download location
# BASE_PATH: str|Path             = CWD # not dynamic
# PLAYLIST_FOLDER_TMPL: str       = '{title:.15} [{id:.10}]' # relative to playlist
# VIDEO_FILE_TMPL: str            = '{title} [{id}].{ext}' # relative to individual video

# # enable both to fix number order
# DENUMBER_VIDEOS: bool           = False
# NUMBER_VIDEOS: bool             = True
# DIGITS: int                     = 2
# NUMBER_FMT: str                 = "%(idx)s. %(name)s"
# # idx and name (eg "%(idx)s. %(name)s")

# """
# BASE_PATH
#     GLOBAL_ARCHIVE_FN
#     PLAYLIST_FOLDER
#         PLAYLIST_ARCHIVE_FN
#         FLAT_FN
#         INFO_FN
#         VIDEOS_FOLDERNAME
#             0123. <vid file tmpl>       # example of 4 digits
# """
# VIDEOS_FOLDERNAME   = 'Videos'
# GLOBAL_ARCHIVE_FN   = 'global_archive.txt' # in the BASE_PATH
# PLAYLIST_ARCHIVE_FN = 'archive.txt'

# FLAT_INFO_FN        = 'flat_info.json'
# INFO_FN             = 'info.json'
# EXTRACT_FN          = 'extract.json'
# COMBINED_FN         = 'combined.json'










# def safely_resolve_path(path: str|Path, data: _InfoDict|dict[str, str] = {}, *, restricted: bool = False) -> str:
#     path = Path(path)
#     sanitizer = lambda s: sanitize_filename(s, restricted)
#     sanitized_parts = [sanitizer(part % data) for part in path.parts]
#     if os.name == 'nt' and path.drive:
#         sanitized_parts[0] = path.drive + '\\' # isn't added for some reason
#     return str(Path(*sanitized_parts).resolve())


# utils
def dict_with_keys(d: dict, keys: list, default: Any = KeyError):
    res = dict()
    for k in keys:
        if default is KeyError:
            res[k] = d[k]
        else:
            res[k] = d.get(k, default)
    return res

def get_unused_path(
        p: Path,
        fmt: str = "{stem} ({i}){suffix}",
        extra_format_map: dict[str, str] = {},
        default_value: str|None = None,
        filename_sanitizer: Callable[[str], str] = sanitize_filename) -> Path:
    """
    :param p: Path to file
    :param fmt: Use f-string format, must include a field for `i`
    :param extra_format_map: Extra field values, `i` wont be overridden
    :param default_value: Defaults for extra_format_map (not necessary for default fmt)
    :param filename_sanitizer: Path name will pass through this to swap out illegal characters (values use )
    
    :return: Path to a unused filename following the fmt

    ```
    derived format_map:
        name                    | p.name     <test.mp4>
        stem filename basename  | p.stem     <test>.mp4
        suffix ext              | p.suffix   test<.mp4>  includes .  
        i                       | iteration number)
        now                     | dd-mm-YYYY_HH.MM.SS
        now_micro               | dd-mm-YYYY_HH.MM.SS.ffffff
    ```
    """

    # Formatter().prase(string)
    # returns tuple[text, field, format_spec, conversion]
    _fields = set(map(lambda x: x[1], Formatter().parse(fmt)))
    fields: set[str] = _fields.difference({None}) # type: ignore
    del _fields
    
    format_map: dict[str, str] = {
        'name': p.name,
        'stem': p.stem, 'filename': p.stem, 'basename': p.stem,
        'suffix': p.suffix, 'ext': p.suffix,
        'i': 0,
    } | extra_format_map # extra overrides derived
    
    if 'now' in fields or 'now_micro' in fields:
        now = datetime.datetime.now()
        if 'now' in fields:
            format_map.setdefault('now', now.strftime(r"%d-%m-%Y_%H.%M.%S"))
        if 'now_micro' in fields:
            format_map.setdefault('now_micro', now.strftime(r"%d-%m-%Y_%H.%M.%S.%f"))
    
    missing = list(filter(lambda field: field not in format_map, fields))
    if missing:
        if default_value is None:
            raise ValueError(f"Undefined keys in fmt:\n\t{', '.join(missing)}")
        format_map.update({k: default_value for k in missing})
    
    # required so it wont loop infinitely
    i = 0
    if 'i' not in fields:
        raise ValueError(f"i must be a field in the template\nCurrent template: {repr(fmt)}")

    # if p.exitsts() == False, don't return early because
    # the user should be aware of any issues or missing keys
    #   if the intent is to have possible missing keys, default_value should be set
    while p.exists():
        i += 1
        format_map['i'] = str(i)
        new_name = fmt.format_map(format_map)
        p = p.with_name(filename_sanitizer(new_name))
    
    return p

def load_json(location):
    with open(location, 'r', encoding='utf-8') as f:
        return json.load(f)

def display_video_ids(pl_info: _InfoDict):
    video_ids = [entry['id'] for entry in pl_info.get('entries', [])]
    max_index_len = len(str(len(video_ids)))
    print(f"Got {len(video_ids)} IDs:")
    for i, id in enumerate(video_ids, 1):
        print(f"{str(i).rjust(max_index_len)}. {id}")
    return pl_info

def get_archiveorg_url(url: str):
    return f'ytarchive:{url}'

def get_name(template: str, format_map):
    return sanitize_filename(template.format(**format_map))


class Downloader:
    YT_IE_KEY: str = ""
    WA_IE_KEY: str = ""

    def __init__(
            self,
            playlist_url_or_id: str,
            existing_flat_info_path: str|Path|None = None,
            existing_info_path: str|Path|None = None,

            archive: _Archives = 'playlist',
            quiet: bool = False,
            verbose: bool = False,
            clean_json: bool = False,
            min_sleep_interval: int = 3,
            max_sleep_interval: int = 10,
            rate_limit: int = 15_000_000, # in bytes
            # Recommended (path to binary files/.exe)
            ffmpeg_path: str|Path|None = None,
            cookie_file: str|Path|None = None, # set if privileged

            # Download location
            base_path: str|Path             = Path.cwd(),
            playlist_foldername: str|Callable[[_PL_InfoDict], str] = '{title:.20} [{id:.15}]', # relative to base (ids can be super long so truncated)
            video_fn: str                   = '{title:.20} [{id}].{ext}', # relative to individual video

            videos_foldername   = 'Videos',
            global_archive_fn   = 'global_archive.txt', # in the BASE_PATH
            playlist_archive_fn = 'archive.txt',

            flat_info_fn        = 'flat_info.json',
            info_fn             = 'info.json',
        ) -> None:
        """
        if a playlist name changes, please change the playlist's foldername before running the program or at least before downloading its videos

        ```
        BASE_PATH
            GLOBAL_ARCHIVE_FN
            PLAYLIST_FOLDER
                PLAYLIST_ARCHIVE_FN
                FLAT_FN
                INFO_FN
                VIDEOS_FOLDERNAME
                    0123. <vid file tmpl>       # example of 4 digits
        ```
        """

        self.base_path = base_path
        self.archive = archive
        self.ffmpeg_path = ffmpeg_path

        self.general_opts: _Params = {
            'ffmpeg_location': str(ffmpeg_path),
            'quiet': quiet,
            'verbose': verbose,
            'clean_infojson': clean_json,
            'sleep_interval': min_sleep_interval,
            'max_sleep_interval': max_sleep_interval,
            'ratelimit': rate_limit,
        }

        self.cookie_opt: _Params = {'cookiefile': str(cookie_file) or None}
        self.flat_pl_info: _PL_InfoDict|None = None
        self.pl_info: _PL_InfoDict|None = None

        self.is_old_flat_info = existing_flat_info_path is not None
        self.is_old_info = existing_info_path is not None
        if existing_flat_info_path:
            self.flat_pl_info = load_json(existing_flat_info_path)
        if existing_info_path:
            self.pl_info = load_json(existing_info_path)
        
        self.best_info: _PL_InfoDict
        if not self.flat_pl_info and not self.pl_info:
            if not playlist_url_or_id:
                raise ValueError("No data to work with")
            self.flat_pl_info = self._get_flat_pl_info()
            self.best_info = self.flat_pl_info
        else:
            self.best_info = self.pl_info or self.flat_pl_info # type: ignore - one has something fs

        # now we have some info, so get basic useful variables
        self.pl_id = self.best_info['id']

        if callable(playlist_foldername):
            self.pl_foldername = playlist_foldername(self.best_info)
        else:
            self.pl_foldername = get_name(playlist_foldername, self.flat_pl_info)
        
        self.base_path = Path(base_path)
        self.pl_dir                 = self.base_path / self.pl_foldername
        self.global_archive_path    = self.base_path / global_archive_fn

        self.v_dir                  = self.pl_dir / videos_foldername
        self.flat_pl_info_path      = self.pl_dir / flat_info_fn
        self.pl_info_path           = self.pl_dir / info_fn
        self.pl_archive_path        = self.pl_dir / playlist_archive_fn
        
        if not self.is_old_flat_info and self.flat_pl_info:
            self.write_info_json(self.best_info, self.flat_pl_info_path)
        
        self.video_ids = [entry['id'] for entry in self.best_info['entries']]
        self.unavailable_ids = self.get_unavailable_ids()
        
        # update
        self.general_opts.update(
            paths = {'home': str(self.base_path)}, # type: ignore
            outtmpl={
                'default': str(Path(self.pl_foldername, videos_foldername, video_fn)),
            })

        self.general_opts['download_archive'] = str(self.global_archive_path) if archive == 'global' else\
                                                str(self.pl_archive_path)     if archive == 'playlist' else\
                                                None
        
    
    def write_info_json(self, info: _InfoDict, path: Path):
        """
        default dir is self.pl_dir
        If there is an existing file, the old one will have its name changed and the new one will have the normal name.
        """

        dir = path.parent
        dir.mkdir(parents=True, exist_ok=True)
        
        if path.exists():
            new_name = get_unused_path(path).name
            if not self.general_opts.get('quiet'):
                print(f"Changed old info filename:\n{repr(path.name)} to {repr(new_name)}")
            path.rename(new_name)

        with path.open('w', encoding='utf-8') as f:
            json.dump(info, f, default=str)
        
        print(f"Wrote info to {path}")
    

    def _get_flat_pl_info(self) -> _PL_InfoDict:

        if not self.is_old_flat_info and self.flat_pl_info:
            return self.flat_pl_info

        with YoutubeDL(self.general_opts | self.cookie_opt | {
            "skip_download": 'True',
            'extract_flat': 'in_playlist',
            'ignoreerrors': True,
        }) as ydl:
            flat_pl_info = ydl.extract_info(self.pl_id, download=False)

        return flat_pl_info # type: ignore
    

    def extract_info_no_download(
            self,
            write_flat: bool = False,
            write_extract: bool = False,
            write_combined: bool = False,
            flat_fn: str = 'flat_info.json',
            extract_fn: str = 'extract.json',
            combined_fn: str = 'combined.json',
        ) -> _PL_InfoDict:

        flat_pl_info = self._get_flat_pl_info()
        if write_flat:
            self.write_info_json(flat_pl_info, self.pl_dir / flat_fn)

        with YoutubeDL(self.general_opts | self.cookie_opt) as ydl:
            extract_pl_info: _PL_InfoDict = ydl.extract_info(self.pl_id, download=False) # type: ignore
        if write_extract:
            self.write_info_json(extract_pl_info, self.pl_dir / extract_fn)
        
        combined = extract_pl_info # they are the same object
        for i in range(len(flat_pl_info['entries'])):
            if not combined['entries'][i]:
                combined['entries'][i] = flat_pl_info['entries'][i]
                combined['entries'][i]['is_unavailable'] = True
            else:
                combined['entries'][i]['is_unavailable'] = False
        if write_combined:
            self.write_info_json(combined, self.pl_dir / combined_fn)
        return combined

    @staticmethod
    def _load_ie_keys():
        if not Downloader.YT_IE_KEY:
            print("Getting Youtube ie_key")
            from yt_dlp.extractor.youtube import YoutubeIE
            Downloader.YT_IE_KEY = YoutubeIE.ie_key()
        if not Downloader.WA_IE_KEY:
            print("Getting YoutubeWebArchive ie_key")
            from yt_dlp.extractor.archiveorg import YoutubeWebArchiveIE
            Downloader.WA_IE_KEY = YoutubeWebArchiveIE.ie_key()

    def _download_video_yt(self, id: str, extract: bool):
        error = None
        v_info = dict()
        try:
            with YoutubeDL(self.general_opts) as ydl:
                if extract:
                    v_info: _InfoDict|dict = ydl.extract_info(id) # type: ignore
                else:
                    ydl.download([id])
        except DownloadError as yt_err:
            error = repr(yt_err)
            offset = len('\x1b[0;31mERROR:\x1b[0m [youtube] 11_char_vid: Video unavailable. ')
            if yt_err.msg:
                v_info['unavailable_reason'] = yt_err.msg[offset:]
        return v_info, error
    
    def _download_video_wa(self, id: str, extract: bool):
        v_info = dict()
        error = None
        try:
            with YoutubeDL(self.general_opts) as ydl:
                if extract:
                    v_info.update(ydl.extract_info(get_archiveorg_url(id)) or {})
                else:
                    ydl.download([get_archiveorg_url(id)])
        except DownloadError as ytwa_err:
            error =[repr(ytwa_err)]
        return v_info, error

    def _download_pl_videos(
            self,
            extract: bool = True,
            archive_fallback: bool = True,
            try_unavailable_on_yt: bool = False,
        ):
        Downloader._load_ie_keys()

        results = {
            Downloader.YT_IE_KEY: [],
            Downloader.WA_IE_KEY: [], 
            'failed': [],
            'errors': [],
        } # type: ignore
        
        entries_infos: list[_InfoDict|dict] = []
        try:
            for i, id in enumerate(self.video_ids):
                if not self.general_opts.get('quiet'):
                    print(f"Downloading video {i}/{len(self.video_ids)}")
                is_available = id not in self.unavailable_ids
                if is_available or try_unavailable_on_yt:
                    v_info, error = self._download_video_yt(id, extract)
                    if not error:
                        results[Downloader.YT_IE_KEY].append(id)
                        entries_infos.append(v_info)
                        continue
                    else:
                        results['errors'].append(error)
                if archive_fallback:
                    v_info, error = self._download_video_wa(id, extract)
                    if not error:
                        results[Downloader.WA_IE_KEY].append(id)
                        entries_infos.append(v_info)
                        continue
                    else:
                        results['errors'].append(error)
                print(f"Download {i} failed for {id}")
                results['failed'].append(id)
        except Exception as e:
            print(f"Exitted entries early because {repr(e)}")
        finally:
            self._append_to_archives(dict_with_keys(results, [Downloader.YT_IE_KEY, Downloader.WA_IE_KEY]))

        if not self.general_opts.get('quiet'):
            if results['failed']:
                print(f"Failed downloads: {results['failed']}")
            if results['errors']:
                for e in results['errors']:
                    print(repr(e))

        return entries_infos, results



    # using pl_info
    def _append_to_archives(self, results: dict[_IE_Key, list[_id]], no_duplicates: bool = False):

        # yt_dlp will write to the other archive
        archives_to_write_to = []
        match(self.archive):
            case 'global':
                archives_to_write_to = [self.pl_archive_path]
            case 'playlist':
                archives_to_write_to = [self.global_archive_path]
            case None:
                return

        new_lines: dict[str, dict[str, list[str]]] = {}
        for archive_path in archives_to_write_to:
            download_archive = set()
            archive_path.touch(exist_ok=True)
            with archive_path.open('+r', encoding='utf-8') as f:
                for line in f.readlines():
                    line = line.removesuffix('\n') # remove '\n'
                    if line.count(' ') != 1 or line.startswith('#'): # allow comments
                        continue
                    ie, id = line.split()
                    if (ie, id) in download_archive:
                        continue
                    download_archive.add((ie, id))

                new_in_archive: dict[str, list[str]] = dict()
                new_lines[archive_path.name] = new_in_archive
                for ie_key, ids in results.items():
                    ids: list[str]
                    new_in_archive[ie_key] = list()
                    for id in ids:
                        if no_duplicates and (ie_key, id) in download_archive:
                            continue
                        # note: this is the yt-dlp format.
                        # see yt_dlp/utils/_utils.py make_archive_id
                        new_line = f'{ie_key.lower()} {id}'
                        new_in_archive[ie_key].append(new_line)
                        if not self.general_opts.get('quiet'):
                            print(f"Added {repr(new_line)} to {archive_path.name}")
                        f.write(new_line + '\n') # add trailing '\n'
        return new_lines
    
    # enable both to fix number order
    # denumber_videos: bool           = False,
    # NUMBER_VIDEOS: bool             = True,
    # DIGITS: int                     = 2,
    # NUMBER_FMT: str                 = '{idx}. {name}",
    def number_videos(self, digits: int = 2, number_template: str = '{idx}. {name}'):
        if not self.v_dir.exists():
            return
        
        for i, entry in enumerate(self.pl_info.get('entries', []), start=1):
            video_filename = get_name(VIDEO_FILE_TMPL, entry)
            video_path: Path = self.v_dir / video_filename
            
            idx = str(i).zfill(DIGITS)
            numbered_path = video_path.with_name(
                get_name(number_template, {'idx': idx, 'name': video_filename})
            )

            if video_path.exists():
                if not numbered_path.exists():
                    video_path.rename(numbered_path)
                    if VERBOSE_SCRIPT:
                        print(f"[INFO] {idx} renamed: {video_path.name} -> {numbered_path.name}")
                else:
                    print(f"[WARNING] {idx} Numbered file already exists")
            else:
                if numbered_path.exists():
                    if VERBOSE_SCRIPT:
                        print(f"({idx})")
                else:
                    print(f"[NOT FOUND {str(i).rjust(DIGITS)} ] {video_path.name}")

    def denumber_files(playlist_foldername):
        """ Removes NUMBER_FMT from all files in the playlist's Videos folder """
        video_dir = Path(BASE_PATH, playlist_foldername, VIDEOS_FOLDERNAME)
        if not video_dir.exists():
            return
        
        __IDX = '__idx_placeholder'
        __NAME = '__name_placeholder'
        if __IDX in NUMBER_FMT:
            raise ValueError(f"{repr(__IDX)} can't be in NUMBER_FMT {repr(NUMBER_FMT)}")
        if __NAME in NUMBER_FMT:
            raise ValueError(f"{repr(__NAME)} can't be in NUMBER_FMT {repr(NUMBER_FMT)}")
        
        fmt = NUMBER_FMT % {
            'idx': __IDX,
            'name': __NAME,
        }
        pattern = fr'''^
            {re.escape(fmt)
                .replace(__IDX, fr'(\d{{{DIGITS}}}\d*)')
                .replace(__NAME, fr'(.+)')}
        $
        '''
        
        for v_path in video_dir.iterdir():
            match = re.match(pattern, v_path.name, re.VERBOSE)
            if match:
                idx = match.group(1)
                denumbered_path = video_dir / match.group(2)
                if not denumbered_path.exists():
                    v_path.rename(denumbered_path)
                    if VERBOSE_SCRIPT:
                        print(f"[INFO] renamed: {v_path.name} -> {denumbered_path.name}")
                else:
                    print(f"[WARNING] Denumbered file already exists ({v_path.name})")
            else:
                print(f"[UNRECOGNIZED or already DENUMBERED] {v_path.name}")

    def get_unavailable_ids(self):
        unavailable_ids = list()
        for entry in self.flat_pl_info['entries']:
            if 'is_unavailable' in entry:
                if entry['is_unavailable'] == True:
                    unavailable_ids.append(entry['id'])
            elif entry['availability'] is None:
                unavailable_ids.append(entry['id'])
        return unavailable_ids

    def download_playlist(self):
        playlist_foldername = get_name(PLAYLIST_FOLDER_TMPL, pl_info)
        print(f"\nFlat playlist info downloaded to:\n"
                f"\t{str(Path(BASE_PATH, playlist_foldername, INFO_FN))}\n")

        display_video_ids(pl_info)
        n_videos = pl_info.get('playlist_count', 0)
        if n_videos == 0:
            raise ValueError("Playlist is empty or no ids were found")
        print(f"Download {n_videos} videos?")
        input("Confirm?")

        entries_info, results = _download_pl_videos(pl_info, extract=True)
        for i, entry in enumerate(entries_info):
            pl_info['entries'][i].update(entry)
        self.write_info_json(pl_info, INFO_FN)

        return pl_info, results

    def union_newest(pl_infos: list[_PL_InfoDict]) -> _PL_InfoDict:
        pl_ids = {pl_info['id'] for pl_info in pl_infos}
        if len(pl_ids) > 1:
            raise ValueError(f"More than one id: {pl_ids}")
        
        # pick playlist info based on most recent (epoch)
        pl_infos = sorted(pl_infos, key=lambda info: info.get('epoch', 0), reverse=True)
        new_pl_info = pl_infos.pop(0)

        # entries list starts at first index
        entry_ids = [entry['id'] for entry in new_pl_info['entries']]
        for pl_info in pl_infos:
            prev_id_idx = -1
            for entry in pl_info['entries']:
                entry_id = entry['id']
                if entry_id in entry_ids:
                    prev_id_idx = entry_ids.index(entry_id)
                    continue
                entry_id_idx = prev_id_idx + 1
                new_pl_info['entries'].insert(entry_id_idx, entry)
                prev_id_idx = entry_id_idx
        
        new_pl_info['playlist_count'] = len(entry_ids)
        return new_pl_info





def main():

    # playlists MUST have unique titles!!!

    if DOWNLOAD:
        pl_info, results = download_playlist()
    else:
        if INFO_LOCATION:
            pl_info = load_json(INFO_LOCATION)
        else:
            pl_info = extract_info_no_download(True, True, True)

    playlist_foldername = get_name(PLAYLIST_FOLDER_TMPL, pl_info)
    playlist_dir_path = Path(BASE_PATH, playlist_foldername)
    video_dir_path = playlist_dir_path / VIDEOS_FOLDERNAME
    playlist_archive_path = playlist_dir_path / PLAYLIST_ARCHIVE_FN
    
    video_ids = [entry['id'] for entry in pl_info['entries']]
    unavailable_ids = get_unavailable_ids(pl_info)

    if DENUMBER_VIDEOS:
        denumber_files(playlist_foldername)
    elif NUMBER_VIDEOS:
        denumber_files(playlist_foldername)
        number_files(pl_info)

    # do something with the pl_info

    



if __name__ == "__main__":
    main()
