"""
Classifying extractor errors, and `Issue`.

`classify()` turns a yt-dlp error string into an `ErrorClass` plus the extractor tag it came
from. It is pure: no printing, no I/O, total over its input. The single distinction it exists
to protect is `confirmed_unavailable` -- only a message that positively says the video is gone
counts. Anything ambiguous stays retryable, because treating "we could not tell" as "it is
gone" freezes a live video for the length of a backoff.

`Issue` is how the rest of the package reports a problem instead of raising or prompting. A
user-owned file that is missing, truncated or hand-mangled yields an `Issue` and the record
still opens, still answers queries and still commits.
"""
from __future__ import annotations

__all__ = [  # noqa: RUF022
    'ErrorClass', 'Classification', 'classify',
    'Severity', 'Issue',
    'MISC_ERRORS', 'AUTH_PATTERNS', 'GEO_PATTERNS', 'UNAVAILABLE_PATTERNS', 'NOT_FOUND_PATTERNS',
]

import re
from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import Any, Final


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
    """Clearly unavailable: takedown, private, deleted, not archived."""
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


MISC_ERRORS: Final[dict[str, ErrorClass]] = {
    r'.*Read timed out.*timeout=[\d\.]+': ErrorClass.TIMED_OUT,
    r'^Postprocessing.*': ErrorClass.POSTPROCESSING,
    r'.*HTTP Error 403: Forbidden': ErrorClass.HTTP_403,
    r'.*HTTP Error 429.*': ErrorClass.RATE_LIMITED,
    r'.*[Tt]oo [Mm]any [Rr]equests.*': ErrorClass.RATE_LIMITED,
    r'.*getaddrinfo failed.*': ErrorClass.NETWORK,
    r'.*[Nn]ame or service not known.*': ErrorClass.NETWORK,
    r'.*[Cc]onnection (refused|reset|aborted).*': ErrorClass.NETWORK,
}

AUTH_PATTERNS: Final[tuple[str, ...]] = (
    r".*[Ss]ign in to confirm you'?re not a bot.*",     # yt: bot check
    r'.*[Ss]ign in to confirm your age.*',              # yt: age gate
    r'.*[Jj]oin this channel.*members.*',               # yt: members-only
    r'.*available to this channel.*members.*',          # yt: members-only
)
"""Checked **before** UNAVAILABLE_PATTERNS, because an auth message can also mention
signing in.

Deliberately not here: yt-dlp's `Use --cookies...` hint. yt-dlp appends it to private-video
errors as well as to bot checks, so matching on it would match a confirmed-private video as
just needing credentials.
"""

GEO_PATTERNS: Final[tuple[str, ...]] = (
    r'.*not available in your country.*',
    r'.*blocked it in your country.*',
    r'.*not made this video available in your country.*',
    r'.*[Tt]his video is not available from your location.*',
)
"""Checked **before** UNAVAILABLE_PATTERNS: a geo-block message usually opens with
'Video unavailable.' and would otherwise be recorded as gone for good.
"""

UNAVAILABLE_PATTERNS: Final[tuple[str, ...]] = (
    r'.*[Vv]ideo unavailable.*',                              # yt: unavailable / takedown
    r'.*has been removed for violating.*Terms of Service.*',  # yt: ToS removal
    r'.*[Pp]rivate video.*',                                  # yt: private
    r'.*[Pp]lease sign in.*',                                 # yt: private video
    r'.*not archived or indexed.*',                           # wa: not indexed
)

NOT_FOUND_PATTERNS: Final[tuple[str, ...]] = (
    r'.*does not exist.*',
    r'.*[Nn]ot [Ff]ound.*',
)

_ANSI_RE: Final = re.compile(r'\x1b\[[0-9;]*m')
_TAG_RE: Final = re.compile(r'.*?\[([^\[\]]+?)\].*')
_PREFIX_RE: Final = re.compile(r'^\s*ERROR:\s*(.+)', re.DOTALL)


@dataclass(frozen=True, slots=True, kw_only=True)
class Classification:
    """The verdict on one error message."""

    error_class: ErrorClass
    message: str
    """The body, with any ANSI escapes and `ERROR:` prefix removed."""
    tag: str = ''
    """The extractor tag from the first [...] group: `youtube`, `web.archive:youtube`, ..."""
    may_be_auth: bool = False
    """Set on NOT_FOUND when the target was one only visible while signed in.

    yt-dlp reports a playlist you cannot see and a playlist that does not exist with the same
    words, so this records the ambiguity rather than resolving it. Claiming AUTH_REQUIRED here
    would assert something unknown; report/ is expected to name both possibilities.
    """

    @property
    def confirmed_unavailable(self) -> bool:
        """True only when the platform positively said the video is gone.

        Everything else -- auth, geo, not-found, unrecognized -- describes a video that may
        well still be there.
        """
        return self.error_class is ErrorClass.UNAVAILABLE

    @property
    def is_transient(self) -> bool:
        """True when retrying later is reasonable with no user action."""
        return self.error_class in (
            ErrorClass.TIMED_OUT, ErrorClass.HTTP_403, ErrorClass.RATE_LIMITED,
            ErrorClass.NETWORK, ErrorClass.UNRECOGNIZED)

    @property
    def needs_attention(self) -> bool:
        """True when this message should be surfaced and kept so a pattern can be added."""
        return self.error_class is ErrorClass.UNRECOGNIZED


def classify(message: str, *, expects_auth: bool = False) -> Classification:
    """Classify an extractor error message. Pure and total over its input.

    ANSI escapes are stripped by ytdlp/ at capture; an escaped or bare `ERROR:` prefix is
    tolerated here either way rather than treated as a problem.

    `expects_auth` says the call targeted something only visible while signed in (`LL`, `WL`,
    a private playlist). It does not change the class -- it marks the resulting NOT_FOUND as
    ambiguous via `may_be_auth`.
    """
    clean = _ANSI_RE.sub('', message)
    body = match.group(1) if (match := _PREFIX_RE.match(clean)) else clean
    tag = match.group(1) if (match := _TAG_RE.match(clean)) else ''

    def verdict(error_class: ErrorClass, *, may_be_auth: bool = False) -> Classification:
        return Classification(error_class=error_class, message=body, tag=tag,
                              may_be_auth=may_be_auth)

    for pattern, error_class in MISC_ERRORS.items():
        if re.match(pattern, body):
            return verdict(error_class)

    if any(re.match(p, body) for p in AUTH_PATTERNS):
        return verdict(ErrorClass.AUTH_REQUIRED)

    if any(re.match(p, body) for p in GEO_PATTERNS):
        return verdict(ErrorClass.GEO_BLOCKED)

    if any(re.match(p, body) for p in UNAVAILABLE_PATTERNS):
        return verdict(ErrorClass.UNAVAILABLE)

    if any(re.match(p, body) for p in NOT_FOUND_PATTERNS):
        return verdict(ErrorClass.NOT_FOUND, may_be_auth=expects_auth)

    return verdict(ErrorClass.UNRECOGNIZED)


# ---- issues ----

class Severity(StrEnum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    """The record cannot be trusted until this is resolved."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Issue:
    """Something wrong with the record, reported rather than raised or prompted about."""

    code: str
    """Stable, greppable identifier, e.g. `roster.missing`, `archive.desync`."""
    message: str
    severity: Severity = Severity.WARNING
    path: str | None = None
    detail: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        where = f' [{self.path}]' if self.path else ''
        return f'{self.severity.upper()}: {self.code}{where}: {self.message}'
