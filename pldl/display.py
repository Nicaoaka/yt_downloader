from yt_dlp.utils import DownloadError

from . import utils
from ._types import *



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
    __slots__ = ("text", "color", "rendered")

    def __init__(self, text: str, color: str, width: int = 8):
        self.text = text
        self.color = color
        self.rendered = utils.hex(text.center(width), bg=color)

    def __str__(self) -> str:
        return self.rendered


# Actions
ACTION_TAG: dict[DL_Action, _Tag] = {
    DL_Action.USER     : _Tag("USER INPUT", "#000000", width=10),
    DL_Action.QUIT     : _Tag("QUIT",       "#ffffff", width=10),
    DL_Action.SKIP     : _Tag("SKIP",       "#161616", width=10),
    DL_Action.EXTRACT  : _Tag("EXTRACT",    "#4ec9b0", width=10),
    DL_Action.DOWNLOAD : _Tag("DOWNLOAD",   "#6a9955", width=10),
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

def download_result(dl: DownloadInfo) -> _Tag:
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
    result_tag = download_result(dl)

    # only have id and title so don't use yt_utils.get_v_dispaly()
    v_display = f"[{dl['id']}] {dl['title'] if dl['title'] else '???'}"

    line = f"{action_tag} -> {result_tag} {utils.hex(v_display, fg=result_tag.color)}"

    if errors and 'errors' in dl:
        for e in dl['errors']:
            if isinstance(e, DownloadError):
                # This is an expected error, so print focusing on the error msg.
                line += ''.join(f"\n{utils.hex(f"yt_dlp.utils.DownloadError: {e.msg}", utils.EXC_COLOR)}")
            else:
                line += ''.join(f"\n{utils.format_exception(e)}" for e in dl['errors'])

    return line


def pl_download_info(pl_dl_info: PL_DownloadInfo, errors: bool) -> str:
    idx_width = len(str(len(pl_dl_info)))
    lines = []
    for i, dl_info in enumerate(pl_dl_info, start=1):
        lines.append(f"{i:>{idx_width}}. {download_info(dl_info, errors)}")
    return '\n'.join(lines)



def _make_pl_dl_info_combos() -> PL_DownloadInfo:
    errors = []
    try:
        raise ValueError("Hello")
    except Exception as e:
        errors = [e]
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
    pl_dl_info = _make_pl_dl_info_combos()
    print(pl_download_info(pl_dl_info, True))
    pass

if __name__ == "__main__":
    main()
