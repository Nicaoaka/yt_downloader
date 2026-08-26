import re
from collections import Counter, defaultdict

from yt_dlp.utils import DownloadError

from pldl import yt_utils
from pldl.pldl_types import *
from pldl.utils import utils


def pl_v_ids(pl_info: PL_InfoDict) -> None:
    """ Prints video ids from pl_info in a formatted way

    <#ids> IDs:
     1. 123456789012
     2. 123456789012
    ...
    10. 123456789012
    ...

    Args:
        pl_info (_PL_InfoDict): Every entry should have something set for `id`
    """
    video_ids = [entry['id'] for entry in pl_info.get('entries', [])]
    _max_index_len = len(str(len(video_ids)))
    print(f"{len(video_ids)} IDs:")
    for i, id in enumerate(video_ids, 1):
        print(f"{str(i).rjust(_max_index_len)}. {id}")

class _Tag:
    __slots__ = ("text", "color", "rendered")  # noqa: RUF023

    def __init__(self, text: str, color: str, width: int = 8):
        self.text = text
        self.color = color
        self.rendered = utils.hex(text.center(width), bg=color)

    def __str__(self) -> str:
        return self.rendered


# Actions
ACTION_TAG: dict[DL_Action, _Tag] = {
    DL_Action.USER     : _Tag("USER", "#000000"),
    DL_Action.QUIT     : _Tag("QUIT", "#ffffff"),
    DL_Action.SKIP     : _Tag("SKIP", "#161616"),
    DL_Action.EXTRACT  : _Tag("EXTR", "#4ec9b0"),
    DL_Action.DOWNLOAD : _Tag("DWLD", "#6a9955"),
}

# Raw results (used when the result is reported "as-is")
RESULT_TAG: dict[DL_Result, _Tag] = {
    DL_Result.UNRECOGNIZED : _Tag("????",   "#ffffff"),
    DL_Result.FAIL         : _Tag("FAIL",   "#ff3826"),
    DL_Result.CANCELLED    : _Tag("CANCEL", "#161616"),
    DL_Result.CACHED       : _Tag("CACHED", "#2d4123"),
    DL_Result.EXTRACT      : _Tag("EXTR",   "#4ec9b0"),
    DL_Result.DOWNLOAD     : _Tag("DWLD",   "#6a9955"),
}

# Derived/outcome tags (not 1:1 with a DL_Result - depend on action+result combo)
IMPOSSIBLE = _Tag("IMP!", "#0000ac")

V_INFO_LEVEL: dict[V_InfoLevel, _Tag] = {
    V_InfoLevel.NONE     : _Tag("n", "#2b1d1d", 3),
    V_InfoLevel.FLAT     : _Tag("F", "#838383", 3),
    V_InfoLevel.EXTRACT  : _Tag("EXTR", "#4ec9b0"),
    V_InfoLevel.DOWNLOAD : _Tag("DWLD", "#6a9955"),
}

def download_result_tag(dl: DownloadInfo) -> _Tag:
    """Reconcile action + result into the single outcome tag to display."""
    action, result = dl['action'], dl['result']

    match action:
        case DL_Action.USER:
            # USER is not a valid action to have reached a result stage.
            return IMPOSSIBLE

        case DL_Action.QUIT | DL_Action.SKIP:
            # Quitting/skipping should always resolve as CANCELLED.
            return RESULT_TAG[DL_Result.CANCELLED] if result == DL_Result.CANCELLED else IMPOSSIBLE

        case DL_Action.EXTRACT:
            return RESULT_TAG[result]

        case DL_Action.DOWNLOAD:
            if result == DL_Result.DOWNLOAD:
                return RESULT_TAG[DL_Result.DOWNLOAD]
            if result == DL_Result.CACHED:
                return RESULT_TAG[DL_Result.CACHED]
            if result == DL_Result.EXTRACT:
                return RESULT_TAG[DL_Result.FAIL]
            return RESULT_TAG[result]

        case _:
            return IMPOSSIBLE


def download_info(dl: DownloadInfo, errors: bool) -> str:
    action_tag = ACTION_TAG[dl['action']]
    result_tag = download_result_tag(dl)

    # only have id and title so don't use yt_utils.get_v_dispaly()
    v_display = f"[{dl['id']}] {dl['title'] if dl['title'] else '???'}"

    line = f"{action_tag} -> {result_tag} {utils.hex(v_display, fg=result_tag.color)}"

    if errors and 'errors' in dl:
        for e in dl['errors']:
            if isinstance(e, DownloadError):
                # This is an expected error, so print focusing on the error msg.
                line += "\n" + utils.hex(f"yt_dlp.utils.DownloadError: {e.msg}", utils.EXC_COLOR)
            elif isinstance(e, BaseException):
                line += "\n" + utils.format_exception(e)
            else:
                line += "\n" + utils.hex(f"yt_dlp.utils.DownloadError: {e}", utils.EXC_COLOR)

    return line


def pl_download_info(pl_dl_info: PL_DownloadInfo, errors: bool, header: bool) -> str:
    res = ""
    if header:
        res += ("\n"
                " ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ \n"
                "  Playlist Videos Download Info  \n"
                " ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ \n"
                "\n")
    idx_width = len(str(len(pl_dl_info)))
    lines = []
    for i, dl_info in enumerate(pl_dl_info, start=1):
        lines.append(f"{i:>{idx_width}}. {download_info(dl_info, errors)}")
    return res + '\n'.join(lines)


def _warn_if_duplicates(v_ids: list[V_ID]):
    counts = Counter(v_ids)
    duplicates = {v_id: count for v_id, count in counts.items() if count > 1}
    if not duplicates:
        return ""
    amount = sum(duplicates.values()) - len(duplicates)
    utils.WARNING(
        f"There are {amount} duplicates.\n"
        f"Duplicated v_id counts:\n"
        f"{duplicates}",
        caller_offset=1)

def _print_per_id(pl_info: PL_InfoDict, v_ids: list[V_ID], id_prints: list[str], ident_colors: list[str | None] | None = None, include_urls: bool = False, warn_duplicates: bool = True):
    if ident_colors is None:
        ident_colors = []
    if len(v_ids) != len(id_prints):
        raise ValueError(f"v_ids and id_prints ({len(v_ids)} != {len(id_prints)}) must have same length")
    if len(ident_colors) not in (0, len(v_ids)):
        raise ValueError(f"v_ids and index_colors ({len(v_ids)} != {len(ident_colors)}) must have same length")

    if warn_duplicates:
        _warn_if_duplicates(v_ids)

    DEFAULT_IDENT_COLOR = "#2E2E2E"
    for i in range(len(ident_colors)):
        if not ident_colors[i]:
            ident_colors[i] = DEFAULT_IDENT_COLOR
    if len(ident_colors) == 0:
        ident_colors = [DEFAULT_IDENT_COLOR*len(v_ids)]

    pl_ids = {entry['id']: i for i, entry in enumerate(pl_info['entries'])}
    for i, (v_id, v_print, _color) in enumerate(zip(v_ids, id_prints, ident_colors), start=1):
        pl_v_info: V_InfoDict = pl_info['entries'][pl_ids[v_id]] if v_id in pl_ids else {'id': v_id}
        ident = utils.hex(f"{i:>4}. {v_id}", fg=_color)
        extractor: str|None = utils.first_non_default(
            pl_v_info, ['extractor_key', 'extractor', 'ie_key'],
            default_values=[None], default_return=None)

        # videos that failed both will use their youtube url.
        url = (
            '' if extractor is None else
            yt_utils.get_yt_video_url(v_id) if extractor.lower() in ('youtube', 'yt') else
            yt_utils.get_archiveorg_url(v_id) if extractor.lower() in 
                ('youtubewebarchive', 'web.archive:youtube', 'wa') else
            '')
        
        if url: url = f" ({url})"
        if not include_urls: url = ""
        ident_alt = utils.hex(
            utils.first_non_default(pl_v_info, ['title', 'alt_title'], default_values=[None], default_return='???') +  
            " by " +
            utils.first_non_default(pl_v_info, ['channel', 'uploader_id', 'uploader', 'artist', 'creator'], default_values=[None], default_return='???') +
            url,
            fg=_color)
        print(ident, v_print, ident_alt)


ERR_TRUNC = 15
UNKNOWN_IE_TRUNC = 15

def _v_merge_timeline(v_tl: V_MergeTimeline) -> tuple[str, str]:
    """
    Does not detect manipulation
    
    Creates rows like:
     n  yt  EXTR   yt|wa  FAIL  
    """
    v_info_level = V_InfoLevel.NONE
    res: str = V_INFO_LEVEL[v_info_level].rendered
    had_fails = False
    for readable_epoch in sorted(v_tl.keys(), key=yt_utils.from_readable_epoch):
        entry = v_tl[readable_epoch]

        if entry.get('unavailable'):
            excs = []
            for msg in entry.get('unavailable', []):
                unavail_type, is_ie = yt_utils.interpret_error_msg(msg)
                if not is_ie:
                    excs.append(utils.hex(utils.truncate(unavail_type, ERR_TRUNC, end="-"), "#FFEB91"))
                    continue
                match unavail_type:
                    case 'youtube'|'yt':             excs.append(utils.hex('yt', "#FF9191"))
                    case 'web.archive:youtube'|'wa': excs.append(utils.hex('wa', "#6ABCFF"))
                    case _: excs.append(utils.hex(utils.truncate(unavail_type, UNKNOWN_IE_TRUNC, end="-"), "#DC3CFC"))
            res += " "+ " ".join(excs)
            had_fails = True
        
        if match := re.match(r'(.+) -> (.+)', entry.get('better_info', '')):
            name = match.groups()[1]
            if name in V_InfoLevel._member_names_:
                new_level = V_InfoLevel[name]
                if new_level > v_info_level:
                    res += V_INFO_LEVEL[new_level].rendered
                    v_info_level = new_level

    if had_fails and v_info_level not in (V_InfoLevel.EXTRACT, V_InfoLevel.DOWNLOAD):
        return res +""+ RESULT_TAG[DL_Result.FAIL].rendered, RESULT_TAG[DL_Result.FAIL].color
    return res, V_INFO_LEVEL[v_info_level].color

def _pl_merge_timeline(pl_info: PL_InfoDict, v_ids: list[V_ID], warn_not_found: bool = True) -> tuple[list[str], list[str|None]]:
    """ Does not handle manipulations """
    _results: dict[V_ID, tuple[str, str|None]] = {}
    pl_ids = {entry['id']: i for i, entry in enumerate(pl_info['entries'])}
    for v_id in v_ids:
        if v_id in _results:
            continue
        if v_id not in pl_ids:
            if warn_not_found: _results[v_id] = (utils.WARNING(f"{v_id} - not found", auto_print=False), None)
            else:              _results[v_id] = ('', None)
            continue
        _results[v_id] = _v_merge_timeline(pl_info.get('merge_timeline', {}).get(v_id, {}))
    return [_results[v_id][0] for v_id in v_ids], [_results[v_id][1] for v_id in v_ids]

def pl_merge_timeline(pl_info: PL_InfoDict, v_ids: list[V_ID], include_urls: bool = True, warn_not_found: bool = True) -> None:
    _print_per_id(pl_info, v_ids, *_pl_merge_timeline(pl_info, v_ids, warn_not_found), include_urls)


def _metadata_history(pl_dl_history: PL_DownloadHistory, v_ids: list[V_ID]) -> tuple[list[str], list[str|None]]:

    v_id_set = set(v_ids)
    results: dict[V_ID, dict] = defaultdict(lambda: {
        'str': V_INFO_LEVEL[V_InfoLevel.NONE].rendered,
        'best_info_level': V_InfoLevel.NONE,
        'failing': False,
        'color': None})
    
    for epoch in sorted(pl_dl_history, key=yt_utils.from_readable_epoch):
        for dl_info in pl_dl_history[epoch]:
            v_id = dl_info['id']
            if v_id not in v_id_set:
                continue

            excs = []
            for error in dl_info.get('errors', []):
                unavail_type, is_ie = yt_utils.interpret_error_msg(str(error))
                if not is_ie:
                    excs.append(utils.hex(utils.truncate(unavail_type, ERR_TRUNC, end='-'), "#FFEB91"))
                    continue
                match unavail_type:
                    case 'youtube':             excs.append(utils.hex("yt", "#FF9191"))
                    case 'web.archive:youtube': excs.append(utils.hex("wa", "#6ABCFF"))
                    case ie:                    excs.append(utils.hex(utils.truncate(ie, UNKNOWN_IE_TRUNC, end='-'),  "#DC3CFC"))
            if excs:
                results[v_id]['str'] += " " + " ".join(excs)

            dl_result = DL_Result[dl_info['result'].upper()]
            results[v_id]['failing'] = dl_result == DL_Result.FAIL
            if not results[v_id]['failing']:
                results[v_id]['str'] += RESULT_TAG[dl_result].rendered

            # color
            info_level = V_InfoLevel.DOWNLOAD if dl_result == DL_Result.DOWNLOAD else \
                     V_InfoLevel.EXTRACT if dl_result == DL_Result.EXTRACT else \
                     V_InfoLevel.NONE # don't assume flat
            if info_level > results[v_id]['best_info_level']:
                results[v_id]['best_info_level'] = info_level
                results[v_id]['color'] = V_INFO_LEVEL[info_level].color
            if results[v_id]['best_info_level'] <= V_InfoLevel.FLAT and dl_info.get('errors'):
                results[v_id]['color'] = RESULT_TAG[DL_Result.FAIL].color

    for v_id in set(v_ids):
        if results[v_id]['str'] == V_INFO_LEVEL[V_InfoLevel.NONE].rendered:
            continue
        if results[v_id]['failing']:
            results[v_id]['str'] += RESULT_TAG[DL_Result.FAIL].rendered

    return (
        [results[v_id]['str'] for v_id in v_ids],
        [results[v_id]['color'] for v_id in v_ids]
    )

def metadata_history(pl_dl_history: PL_DownloadHistory, pl_info: PL_InfoDict, v_ids: list[V_ID], include_urls: bool = True):
    """ Does not handle manipulations """
    _print_per_id(pl_info, v_ids, *_metadata_history(pl_dl_history, v_ids), include_urls)



def _make_pl_dl_info_combos() -> PL_DownloadInfo:
    errors = []
    try:
        raise ValueError("Hello")
    except Exception as e:  # noqa: BLE001
        errors = [str(e)]
    infos: PL_DownloadInfo = []
    for with_errors in [True, False]:
        for i, a in enumerate(DL_Action):
            for j, r in enumerate(DL_Result):
                infos.append({
                    'id': f"{i}x{j}",
                    'title': f"{a}-{r}",
                    'action': a,
                    'result': r,
                })
                if with_errors:
                    infos[-1]['errors'] = errors
    return infos

def main():
    # pl_dl_info = _make_pl_dl_info_combos()
    # print(pl_download_info(pl_dl_info, True))
    pl_info: PL_InfoDict = utils.json_load(r'c:\Users\nicol\Videos\yt-dlp\Liked videos [LL]\2026-07-31 01-22-05.merge.json')
    ids = [entry['id'] for entry in pl_info['entries']]
    _pl_merge_timeline(pl_info, ids)

if __name__ == "__main__":
    main()
