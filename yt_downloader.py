import json
from pathlib import Path
from typing import TYPE_CHECKING, Literal, TypedDict, Any, Required, NotRequired, Callable, Iterable
import re
from string import Formatter
import datetime
import copy

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, sanitize_filename, make_archive_id

if TYPE_CHECKING:
    from yt_dlp import _Params
    type _Archives = Literal['playlist', 'global'] | None

    # copied from yt_dlp then editted
    class _InfoDict(TypedDict):
        # age_limit: int
        availability: Literal["private", "premium_only", "subscriber_only", "needs_auth", "unlisted", "public"] | None
        # available_at: int
        # creator: str | None
        # comment_count: int | None
        # duration: int | None
        # formats: list[dict[str, Any]]
        id: Required[str]
        like_count: int | None
        # tags: list[str] | None
        thumbnail: str | None
        # timestamp: int | float | None 
        title: str | None
        uploader: str | None
        url: str | None

        # added (not custom)
        view_count: int
        channel: str | None
        channel_id: str | None
        uploader_id: str | None
        uploader: str | None
        channel_url: str | None
        uploader_url: str | None
        epoch: NotRequired[int]

        extractor_key: NotRequired[str]
        extractor: NotRequired[str]
        webpage_url: NotRequired[str]
        original_url: NotRequired[str]
        webpage_url_basename: NotRequired[str]
        webpage_url_domain: NotRequired[str]

    class _V_InfoDict(_InfoDict):
        # age_limit: int
        # available_at: int
        comment_count: int | None
        duration: int | None
        formats: list[dict[str, Any]]
        tags: NotRequired[list[str] | None]

        # manually added
        playlist: str | None
        playlist_index: int
        
        # custom
        unavailable_reason: NotRequired[str]

    # custom
    class _PL_InfoDict(_InfoDict):
        playlist_count: int
        modified_date: str
        entries: list[_V_InfoDict]
        tags: list[str] | None

__all__ = [
    'sanitize_filename',

    'truncate', 'dict_without_keys', 'dict_with_keys', 'get_unused_path', 'load_json', 'write_json',

    'display_video_ids', 'get_archiveorg_url', 'safely_format', 'is_unavailable', 'get_unavailable_ids',
    'denumber_videos', 'number_videos', 'union_pl_info',

    'YT_Downloader',
]



# utils
def truncate(s: str, max_len: int, end='...', *, end_in_max: bool = True, trunc_start: bool = False):
    # note some chars have modifiers/combine with others. eg 👈🏾 is '👈 🏾' and len(👨‍👩🏽‍👧‍👦) == 8
    # so if the modifer is cutoff, the char may change a solution to this is using the graphene library
    # to turn the str into a list of graphemes like 
    # ['T','h','i','s','👈🏾'] instead of ['T','h','i','s','👈',' 🏾']
    # https://stackoverflow.com/a/56282726
    # https://github.com/microsoft/vscode/issues/99629#issuecomment-831565509
    def _truncate(_s: str):
        if len(_s) <= max_len:
            return _s
        if end_in_max:
            return _s[:max_len-len(end)] + end
        return _s[:max_len] + end
    if not trunc_start:
        return _truncate(s)
    return _truncate(s[::-1])[::-1]

def dict_without_keys(d: dict, keys: Iterable):
    res = dict()
    for k, v in d.items():
        if k not in keys:
            res[k] = v
    return res

def dict_with_keys(d: dict, keys: Iterable, default: Any = KeyError):
    """ does not support defaultdict """
    res = dict()
    for k in keys:
        if default is KeyError and k not in d:
            raise KeyError(k) # mimic normal key error
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

def load_json(path: str|Path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(json_, path: str|Path, quiet: bool = False, replace: bool = False):
    """
    If there is an existing file, the old one will have its name changed and the new one will have the normal name.
    """
    path = Path(path)
    dir = path.parent
    dir.mkdir(parents=True, exist_ok=True)

    if replace and path.is_dir():
        raise RuntimeError(f"Found directory instead of file at {path}")
    
    if not replace and path.exists():
        new_path = get_unused_path(path)
        if not quiet:
            print(f"Changed old info filename:\n{repr(path.name)} to {repr(new_path.name)}")
        path.rename(new_path)

    with path.open('w', encoding='utf-8') as f:
        json.dump(json_, f, default=str)
    
    if not quiet:
        print(f"Wrote info to {path}")

def strftimestamp(epoch: int|None, strftime: str = "%d/%m/%Y @ %H:%M:%S"):
    """ If epoch is None returns "Unknown" """
    if not epoch:
        return "Unknown"
    return datetime.datetime.fromtimestamp(epoch).strftime(strftime)



# downloader utils
def display_video_ids(pl_info: _PL_InfoDict) -> None:
    video_ids = [entry['id'] for entry in pl_info.get('entries', [])]
    max_index_len = len(str(len(video_ids)))
    print(f"Got {len(video_ids)} IDs:")
    for i, id in enumerate(video_ids, 1):
        print(f"{str(i).rjust(max_index_len)}. {id}")

def get_archiveorg_url(url: str) -> str:
    return f'ytarchive:{url}'

def safely_format(template: str, format_map, format_: Literal['printf', 'fstring'] = 'printf') -> str:
    match format_:
        case 'printf':
            return sanitize_filename(template % format_map)
        case 'fstring':
            return sanitize_filename(template.format(**format_map))

def is_unavailable(info: _InfoDict) -> bool:
    return info.get('channel') is None

def get_unavailable_ids(pl_info: _PL_InfoDict) -> list[str]:
    unavailable_ids = list()
    for entry in pl_info['entries']:
        if is_unavailable(entry):
            unavailable_ids.append(entry['id'])
    return unavailable_ids

def denumber_videos(v_dir: Path, digits: int = 2, number_tmpl: str = '%(idx)s. %(name)s', quiet: bool = False):
    __IDX = re.escape('__idx_placeholder')
    __NAME = re.escape('__name_placeholder')
    if __IDX in number_tmpl:
        raise ValueError(f"{repr(__IDX)} can't be in number_tmpl {repr(number_tmpl)}")
    if __NAME in number_tmpl:
        raise ValueError(f"{repr(__NAME)} can't be in number_tmpl {repr(number_tmpl)}")
    
    fmt = number_tmpl % {
        'idx': __IDX,
        'name': __NAME,
    }
    pattern = '^' + re.escape(fmt)\
                    .replace(__IDX, fr'(\d{{{digits}}}\d*)')\
                    .replace(__NAME, fr'(.+)') + '$'
    
    for v_path in v_dir.iterdir():
        match = re.match(pattern, v_path.name, re.VERBOSE)
        if not match:
            if not quiet:
                print(f"[UNRECOGNIZED or already DENUMBERED] {v_path.name}")
            continue

        idx = match.group(1)
        denumbered_path = v_dir / match.group(2)
        if denumbered_path.exists():
            if not quiet:
                print(f"[WARNING] Denumbered file already exists ({v_path.name})")
            continue

        v_path.rename(denumbered_path)
        if not quiet:
            print(f"[INFO] renamed: {v_path.name} -> {denumbered_path.name}")

def number_videos(v_dir: Path, pl_info: _PL_InfoDict, video_fn_tmpl: str, digits: int = 2, number_tmpl: str = '%(idx)s. %(name)s', denumber_before: bool = False, quiet: bool = False):
    if denumber_before:
        denumber_videos(v_dir, digits, number_tmpl, quiet)
    if not v_dir.exists():
        return
    
    for i, entry in enumerate(pl_info.get('entries', []), start=1):
        video_filename = safely_format(video_fn_tmpl, entry)
        video_path: Path = v_dir / video_filename
        
        idx = str(i).zfill(digits)
        numbered_path = video_path.with_name(
            safely_format(number_tmpl, {'idx': idx, 'name': video_filename})
        )

        if video_path.exists():
            if not numbered_path.exists():
                video_path.rename(numbered_path)
                if not quiet:
                    print(f"[INFO] {idx} renamed: {video_path.name} -> {numbered_path.name}")
            elif not quiet:
                print(f"[WARNING] {idx} Numbered file already exists")
        else:
            if numbered_path.exists():
                if not quiet:
                    print(f"({idx})")
            elif not quiet:
                print(f"[NOT FOUND {str(i).rjust(digits)} ] {video_path.name}")

def union_pl_info(pl_infos: list[_PL_InfoDict], prioritize_newest: bool = True, quiet: bool = False, verbose: bool = False) -> _PL_InfoDict:
    """ Pure Function """
    
    pl_ids = {pl_info['id'] for pl_info in pl_infos}
    if len(pl_ids) > 1:
        raise ValueError(f"More than one id: {pl_ids}")
    
    # pick playlist info based on most recent (epoch)
    if prioritize_newest:
        # ones without epoch have the lowest priority
        pl_infos = sorted(pl_infos, key=lambda info: info.get('epoch', 0), reverse=True)
    new_pl_info = pl_infos.pop(0)

    # entries list starts at first index
    entry_ids = [entry['id'] for entry in new_pl_info['entries']]
    available = [not is_unavailable(entry) for entry in new_pl_info['entries']]
    for pl_info in pl_infos:
        to_add_ids = []
        to_add_entries = []
        to_add_available = []
        for entry in pl_info['entries']:
            id = entry['id']
            try:
                i = entry_ids.index(id)
                if not available[i]:
                    if not quiet and verbose:
                        print(f"UPDATE from {strftimestamp(pl_info.get('epoch', None))} - {entry['title']}")
                    new_pl_info['entries'][i].update(entry)
                    available[i] = True
                if not to_add_ids:
                    continue
                if not quiet and verbose:
                    print(f"ADD from {strftimestamp(pl_info.get('epoch', None))}:")
                    print(f"\t{',\n\t'.join(repr(entry['title']) for entry in to_add_entries)}")
                entry_ids[i:i] = to_add_ids
                new_pl_info['entries'][i:i] = to_add_entries
                available[i:i] = to_add_available
                to_add_ids.clear()
                to_add_entries.clear()
                to_add_available.clear()
            except ValueError:
                to_add_ids.append(id)
                to_add_entries.append(copy.deepcopy(entry))
                to_add_available.append(not is_unavailable(entry))
        entry_ids.extend(to_add_ids)
        new_pl_info['entries'].extend(to_add_entries)
        available.extend(to_add_available)
    
    new_pl_info['playlist_count'] = len(entry_ids)
    return new_pl_info

class YT_Downloader:
    YT_IE_KEY = ""
    WA_IE_KEY = ""

    @staticmethod
    def _default_pl_tmpl(info: _PL_InfoDict):
        return f'{info['title']} [{truncate(info['id'], 11, end_in_max=False, trunc_start=True)}]'
    
    @staticmethod
    def _load_ie_keys():
        if not YT_Downloader.YT_IE_KEY:
            from yt_dlp.extractor.youtube import YoutubeIE
            YT_Downloader.YT_IE_KEY = YoutubeIE.ie_key()
        if not YT_Downloader.WA_IE_KEY:
            from yt_dlp.extractor.archiveorg import YoutubeWebArchiveIE
            YT_Downloader.WA_IE_KEY = YoutubeWebArchiveIE.ie_key()

    def __init__(
            self,
            playlist_url_or_id: str = '',
            existing_flat_info_path: str|Path = '',
            existing_info_path: str|Path = '',

            archive: _Archives = 'playlist',
            quiet: bool = False,
            verbose: bool = False,
            clean_json: bool = False,
            min_sleep_interval: int = 3,
            max_sleep_interval: int = 10,
            rate_limit: int = 3_000_000, # in bytes

            # Recommended (path to binary files/.exe)
            ffmpeg_path: str|Path|None = None,
            cookie_file: str|Path|None = None, # set if privileged

            # Download location
            home_dir_path: str|Path = Path.cwd(),

            # if strings, printf-style ( %(key)s ) format must be used
            playlist_foldername_template: str|Callable[[_PL_InfoDict], str] = _default_pl_tmpl,
            # is used by yt_dlp, so no extra keys and no custom formatting function
            # technically it could be done but would be extra work
            video_filename_template: str = '%(title)s [%(id)s].%(ext)s',

            videos_foldername   = 'Videos',
            global_archive_filename = 'global_archive.txt', # in the BASE_PATH
            playlist_archive_filename = 'archive.txt',

            flat_info_filename  = 'flat_info.json',
            info_filename       = 'info.json',
        ) -> None:
        """
        will automatically run a flat download to get basic information

        use raw strings for paths
        note, max default path length on windows is 260 chars

        if a playlist name changes,
        please change the playlist's foldername before running the program
        or at least before downloading its videos

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

        self.pl_url_or_id = playlist_url_or_id
        self.home_dir_path = home_dir_path
        self.archive = archive
        self.ffmpeg_path = ffmpeg_path
        self.quiet = quiet
        self.verbose = verbose

        self.general_opts: _Params = {
            'ffmpeg_location': str(ffmpeg_path),
            'quiet': quiet,
            'verbose': verbose,
            'clean_infojson': clean_json,
            'sleep_interval': min_sleep_interval,
            'max_sleep_interval': max_sleep_interval,
            'ratelimit': rate_limit,
        }

        self.video_fn_tmpl = video_filename_template
        self.cookie_opt: _Params = {'cookiefile': str(cookie_file)} if cookie_file else {}
        self.flat_pl_info: _PL_InfoDict|None = None
        self.pl_info: _PL_InfoDict|None = None

        self.is_old_flat_info = bool(existing_flat_info_path)
        self.is_old_info = bool(existing_info_path)
        if existing_flat_info_path:
            self.flat_pl_info = load_json(existing_flat_info_path)
        if existing_info_path:
            self.pl_info = load_json(existing_info_path)
        
        self.best_info: _PL_InfoDict
        if not self.flat_pl_info and not self.pl_info:
            if not playlist_url_or_id:
                raise ValueError(
                    "Not enough information to work with.\n\n"
                    "Define any one of the following:\n"
                    "\t'playlist_url_or_id', 'existing_flat_info_path', or 'existing_info_path'")
            self.flat_pl_info = self._get_flat_pl_info()
            self.best_info = copy.deepcopy(self.flat_pl_info)
        else:
            self.best_info = copy.deepcopy(self.pl_info or self.flat_pl_info) # type: ignore - one has something fs

        # now we have some info, so get basic useful variables
        self.pl_id = self.best_info['id']

        if callable(playlist_foldername_template):
            self.pl_foldername = playlist_foldername_template(self.best_info)
        else:
            self.pl_foldername = safely_format(playlist_foldername_template, self.best_info)
        
        self.home_dir_path = Path(home_dir_path)
        self.pl_dir                 = self.home_dir_path / self.pl_foldername
        self.global_archive_path    = self.home_dir_path / global_archive_filename

        self.v_dir                  = self.pl_dir / videos_foldername
        self.flat_pl_info_path      = self.pl_dir / flat_info_filename
        self.pl_info_path           = self.pl_dir / info_filename
        self.pl_archive_path        = self.pl_dir / playlist_archive_filename

        self.pl_dir.mkdir(parents=True, exist_ok=True)
        self.v_dir.mkdir(parents=True, exist_ok=True)
        self.global_archive_path.touch()
        self.pl_archive_path.touch()
        
        if not self.is_old_flat_info and self.flat_pl_info:
            write_json(self.best_info, self.flat_pl_info_path, self.quiet)
        
        self.video_ids = [entry['id'] for entry in self.best_info['entries']]
        self.unavailable_ids = self.get_unavailable_ids()
        
        # update
        self.general_opts.update(
            paths = {'home': str(self.home_dir_path)}, # type: ignore
            outtmpl={
                'default': str(Path(self.pl_foldername, videos_foldername, video_filename_template)),
            })

        self.general_opts['download_archive'] = str(self.global_archive_path) if archive == 'global' else\
                                                str(self.pl_archive_path)     if archive == 'playlist' else\
                                                None

    @staticmethod
    def add_pl_info_to_entries(pl_info: _PL_InfoDict) -> None:
        for i, entry in enumerate(pl_info['entries']):
            entry['playlist'] = pl_info['title']
            entry['playlist_index'] = i
            if 'epoch' not in entry and 'epoch' in pl_info:
                entry['epoch'] = pl_info['epoch']

    def _get_flat_pl_info(self):
        if not self.pl_url_or_id:
            raise ValueError("self.pl_url_or_id must be defined")

        if not self.is_old_flat_info and self.flat_pl_info:
            return self.flat_pl_info

        with YoutubeDL(self.general_opts | self.cookie_opt | {
            "skip_download": 'True',
            'extract_flat': 'in_playlist',
            'ignoreerrors': True,
        }) as ydl:
            flat_pl_info: _PL_InfoDict = ydl.extract_info(self.pl_url_or_id, download=False) # type: ignore
        self.add_pl_info_to_entries(flat_pl_info)
        return flat_pl_info

    def extract_info_no_download(
            self,
            write_flat: bool = False,
            write_extract: bool = False,
            write_combined: bool = False,
            flat_fn: str = 'flat_info.json',
            extract_fn: str = 'extract.json',
            combined_fn: str = 'combined.json',
        ) -> _PL_InfoDict:

        if not self.is_old_flat_info and self.flat_pl_info:
            flat_pl_info = self.flat_pl_info
        else:
            flat_pl_info = self._get_flat_pl_info()
        
        if write_flat:
            write_json(flat_pl_info, self.pl_dir / flat_fn, self.quiet)

        with YoutubeDL(self.general_opts | self.cookie_opt) as ydl:
            extract_pl_info: _PL_InfoDict = ydl.extract_info(self.pl_id, download=False) # type: ignore
        if write_extract:
            write_json(extract_pl_info, self.pl_dir / extract_fn, self.quiet)
        
        combined = extract_pl_info # they are the same object
        for i in range(len(flat_pl_info['entries'])):
            if not combined['entries'][i]:
                combined['entries'][i] = flat_pl_info['entries'][i]
        if write_combined:
            write_json(combined, self.pl_dir / combined_fn, self.quiet)
        return combined

    def _download_video_yt(self, id: str, extract: bool):
        error = None
        v_info: dict|_V_InfoDict = dict()
        try:
            with YoutubeDL(self.general_opts) as ydl:
                if extract:
                    v_info.update(ydl.extract_info(id) or {})
                else:
                    ydl.download([id])
        except DownloadError as yt_err:
            error = repr(yt_err)
            offset = len('\x1b[0;31mERROR:\x1b[0m [youtube] 11_char_vid: Video unavailable. ')
            if yt_err.msg:
                v_info['unavailable_reason'] = yt_err.msg[offset:]
        return v_info, error
    
    def _download_video_wa(self, id: str, extract: bool):
        v_info: dict|_V_InfoDict = dict()
        error = None
        try:
            with YoutubeDL(self.general_opts) as ydl:
                if extract:
                    v_info.update(ydl.extract_info(get_archiveorg_url(id)) or {})
                else:
                    ydl.download([get_archiveorg_url(id)])
        except DownloadError as wa_err:
            error =[repr(wa_err)]
        return v_info, error

    def _download_pl_videos(
            self,
            extract: bool,
            archive_fallback: bool,
            try_unavailable_on_yt: bool,
        ):
        YT_Downloader._load_ie_keys()

        results = {
            YT_Downloader.YT_IE_KEY: [],
            YT_Downloader.WA_IE_KEY: [], 
            'failed': [],
            'errors': [],
        }

        # yt_dlp will already write in the archive it's given
        archive_path = self.pl_archive_path if self.archive == 'global' else self.global_archive_path
        f = open(archive_path, 'a')

        entries_info: list[_V_InfoDict|dict] = []
        try:
            for i, id in enumerate(self.video_ids):
                if not self.quiet:
                    print(f"{i+1}/{len(self.video_ids)}")
                
                is_available = id not in self.unavailable_ids
                if is_available or try_unavailable_on_yt:
                    v_info, error = self._download_video_yt(id, extract)
                    if not error:
                        results[YT_Downloader.YT_IE_KEY].append(id)
                        entries_info.append(v_info)
                        if v_info and self.archive:
                            f.write(make_archive_id(YT_Downloader.YT_IE_KEY, id)+'\n') # type: ignore
                        continue
                    else:
                        results['errors'].append(error)
                
                if archive_fallback:
                    v_info, error = self._download_video_wa(id, extract)
                    if not error:
                        results[YT_Downloader.WA_IE_KEY].append(id)
                        entries_info.append(v_info)
                        if v_info and self.archive:
                            f.write(make_archive_id(YT_Downloader.WA_IE_KEY, id)+'\n') # type: ignore
                        continue
                    else:
                        results['errors'].append(error)
                print(f"Download {i} failed for {id}")
                results['failed'].append(id)
        except KeyboardInterrupt as e:
            print(f"Exitted entries early because {repr(e)}")
        finally:
            f.close()
        
        for i, entry in enumerate(entries_info):
            self.best_info['entries'][i].update(entry)
        self.pl_info = copy.deepcopy(self.best_info)
        self.is_old_info = False
        return entries_info, results

    @staticmethod
    def display_download_results(results: dict[str, list[str]]):
        success = dict_without_keys(results, {'failed', 'errors'})

        print("\n\n" + " + " * 10)

        print("Download Results:")
        print("\tSuccessful downloads:")
        for ie_key, v_ids in success.items():
            print(f"\t{ie_key}: {v_ids}")

        print("\n\tFailed downloads:")
        print(f"\t\t{results['failed']}")

        print("\n\tErrors that occurred downloading:")
        print(f"\t\t{results['errors']}")

        print(' - ' * 20 + "\n\n")

    def download_playlist(
            self,
            extract: bool = True,
            archive_fallback: bool = True,
            try_unavailable_on_yt: bool = False,
            display_results: bool = True,
            write: bool = True,
        ):
        
        display_video_ids(self.best_info)
        n_videos = self.best_info.get('playlist_count', 0)
        if n_videos == 0:
            raise ValueError("Playlist is empty or no ids were found")
        
        print(f"Download {n_videos} videos?")
        input("Confirm?")

        entries_info, results = self._download_pl_videos(extract, archive_fallback, try_unavailable_on_yt)

        new_data = all(len(entry) == 0 for entry in entries_info)

        if display_results:
            self.display_download_results(results)
        
        if write:
            if not new_data:
                print("Nothing new was downloaded - everything was already archived or errored")
                input("Write anyway?")
            write_json(self.best_info, self.pl_info_path, self.quiet)

        return entries_info, results



    def number_videos(self, digits: int = 2, number_tmpl: str = '%(idx)s. %(name)s'):
        if not self.pl_info:
            raise ValueError("Video download information must be known")
        return number_videos(self.v_dir, self.best_info, self.video_fn_tmpl, digits, number_tmpl, self.quiet)

    def denumber_videos(self, digits: int = 2, number_tmpl: str = '%(idx)s. %(name)s'):
        return denumber_videos(self.v_dir, digits, number_tmpl, self.quiet)

    def get_unavailable_ids(self):
        return get_unavailable_ids(self.best_info)


    

