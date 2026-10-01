"""
Why an extractor could not get a video.

`ErrorClass` names the kind of failure. `UnavailableInfo` is one extractor's report that a
video could not be had, at one moment, and is what a video's record keeps.

Two distinctions carry the weight. Only UNAVAILABLE is permanent; anything ambiguous stays
retryable, because treating "we could not tell" as "it is gone" freezes a live video for the
length of a backoff. A private video is not a removed one: its owner can un-private it.
"""
from __future__ import annotations

__all__ = ['ErrorClass', 'UnavailableInfo']

from dataclasses import dataclass
from enum import StrEnum, auto

from pldl.model import Epoch


class ErrorClass(StrEnum):
    """What kind of failure an extractor error message describes."""

    TIMED_OUT = auto()
    POSTPROCESSING = auto()
    HTTP_403 = auto()
    RATE_LIMITED = auto()
    """HTTP 429. Same shape as 403: back off, do not mark anything unavailable."""
    NETWORK = auto()
    """DNS or connection failure. Says nothing about the video."""

    UNAVAILABLE = auto()
    """Gone for good: deleted, account terminated, ToS removal.

    The only class that is permanent. An id that lands here will not come back as that id.
    """
    PRIVATE = auto()
    """Exists, hidden. The creator can un-private it, and if it is your own video the right
    credentials reveal it -- so this must never be treated as permanent the way a takedown
    is."""
    NOT_ARCHIVED = auto()
    """A mirror does not hold this video *yet*.

    Says nothing about the video, only about that mirror's coverage, and coverage grows. A
    video the Wayback Machine has not indexed yet may be there next month, so this is worth
    retrying on a long backoff rather than recording as gone.
    """
    GEO_BLOCKED = auto()
    """Exists and plays for someone else, just not from here. Never 'unavailable'."""
    AUTH_REQUIRED = auto()
    """Available, but requires credentials: bot check, age gate, members-only."""
    NOT_FOUND = auto()
    """The target does not exist -- or is invisible without credentials. See `may_be_auth`."""

    UNRECOGNIZED = auto()
    """No pattern matched. Treat as available.

    Every occurrence is a gap in the pattern tables and should be surfaced loudly by report/
    and persisted, so the message can be read and a pattern added.
    """


# ---- unavailability ----

@dataclass(frozen=True, slots=True, kw_only=True)
class UnavailableInfo:
    """One extractor's report that a video could not be had, at one moment.

    A frozen dataclass rather than a TypedDict because it is pldl's own structure, not part
    of a yt-dlp payload -- and because the timeline deduplicates entries, which needs it to
    be hashable.
    """

    extractor: str
    """Which extractor said it: `youtube`, `web.archive:youtube`.

    Use the full key. Never a `yt`/`wa` shorthand, so comparisons against an extractor tag match
    without a translation table in between.
    """
    msg: str | None = None
    epoch: Epoch | None = None
    error_class: ErrorClass | None = None
    """The classification of `msg`, when it was classified. Lets a reader see *why* a video
    was unavailable without re-running the patterns."""

    def __post_init__(self) -> None:
        if self.epoch is not None and not isinstance(self.epoch, Epoch):
            object.__setattr__(self, 'epoch', Epoch(self.epoch))
