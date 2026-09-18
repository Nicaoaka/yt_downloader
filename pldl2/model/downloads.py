"""
The download-control vocabulary: what policy decided, and what the session got back.

Not infodict shape -- nothing here comes from yt-dlp -- but L0 all the same, because
`metadata.VideoLog` records both, and policy/ and report/ read them.
"""
from __future__ import annotations

__all__ = [
    'DL_Action', 'DL_Result',
    # v1-compat
    '_v1_DownloadInfo', '_v1_Session_DownloadInfo',
]

from enum import StrEnum, auto
from typing import NotRequired, TypedDict


class DL_Action(StrEnum):
    """What to do with a video.

    Declaration order used to be load-bearing for override tie-breaks, documented only in a
    comment. policy/ gives rules an explicit `priority` instead, so nothing here depends on
    the order any more.
    """
    USER     = auto()
    QUIT     = auto()
    SKIP     = auto()
    EXTRACT  = auto()
    DOWNLOAD = auto()


class DL_Result(StrEnum):
    """What actually happened.

    CANCELLED and CACHED are separate: "already in the archive" and "the user stopped it" lead
    to different decisions on the next run, so collapsing them loses the distinction that
    matters.
    """
    CANCELLED    = auto()
    FAIL         = auto()
    UNRECOGNIZED = auto()
    CACHED       = auto()
    EXTRACT      = auto()
    DOWNLOAD     = auto()


# ---- v1-compat ----

class _v1_DownloadInfo(TypedDict):
    """DEPRECATED! One video's outcome, as v1 wrote it into `history`.

    v1-compat: `metadata.VideoLog` is the v2 shape. Kept so the migrator can read v1 history.
    """

    id: str
    title: str | None
    action: DL_Action
    result: DL_Result
    errors: NotRequired[list[str]]


type _v1_Session_DownloadInfo = list[_v1_DownloadInfo]
"""DEPRECATED! v1-compat: `metadata.SessionLog` is the v2 shape."""
