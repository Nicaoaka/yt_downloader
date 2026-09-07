"""
Error classification (pure) and `Issue`, the value that replaces prompting.

v1's `interpret_error_msg` did three jobs on the hot path of both the download filter and the
display layer: it regex-stripped ANSI escapes out of yt-dlp error strings, warned on stdout
when its pattern missed, and coloured its own warning. Stripping moves to ytdlp/ (once, at
capture); classification lands here as a pure function over text.

Two defects this closes:

  - **The verdict is a value the caller must handle.** v1 returned `(reason, is_unavailable)`
    and `wrapper_match_filter` discarded the second element, so a bot-check -- which the
    function itself labelled "NOT confirmed-unavailable" -- was recorded as a confirmed
    failure and froze an available video for the full 7-day backoff (issue-1 #18, confirmed:
    the bot-check message classifies as ('youtube', False) and the filter still returns skip).
    `Classification` makes the distinction a field with a name.
  - **AUTH_REQUIRED exists.** yt-dlp reports a private playlist you cannot see as "playlist
    does not exist", so 'LL' with bad cookies produces an error pointing at the wrong thing
    entirely. Belt-and-braces for the ytdlp/cookies.py pre-flight, which cannot catch cookies
    that expire *during* a long session.

`Issue` is the other half: store/ reports problems rather than prompting. v1's
`_validate_dl_archive_sync` printed a diff, blocked on `input_string`, raised, appended to a
file and mutated two arguments -- inside a constructor. Returning `list[Issue]` is what makes
the store testable at all.
"""
from __future__ import annotations

__all__ = [
    'ErrorClass', 'Classification', 'classify',
    'Severity', 'Issue',
    'MISC_ERRORS', 'UNAVAILABLE_PATTERNS', 'AUTH_PATTERNS',
]

import re
from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import Any


class ErrorClass(StrEnum):
    """What kind of failure a yt-dlp error message describes."""

    TIMED_OUT = auto()
    POSTPROCESSING = auto()
    HTTP_403 = auto()
    UNAVAILABLE = auto()
    """Confirmed gone on that platform: takedown, private, deleted, not archived."""
    AUTH_REQUIRED = auto()
    """Reachable, but not without credentials: bot check, age gate, members-only."""
    UNRECOGNIZED = auto()
    """No pattern matched. **Not** the same as unavailable -- treat as transient."""


MISC_ERRORS: dict[str, ErrorClass] = {
    r'.*Read timed out.*timeout=[\d\.]+': ErrorClass.TIMED_OUT,
    r'^Postprocessing.*': ErrorClass.POSTPROCESSING,
    r'.*HTTP Error 403: Forbidden': ErrorClass.HTTP_403,
}

AUTH_PATTERNS: tuple[str, ...] = (
    r".*[Ss]ign in to confirm you'?re not a bot.*",     # yt: bot check
    r'.*[Ss]ign in to confirm your age.*',              # yt: age gate
    r'.*[Jj]oin this channel.*members.*',               # yt: members-only
    r'.*available to this channel.*members.*',          # yt: members-only
)
"""Checked **before** UNAVAILABLE_PATTERNS, because an auth message can also mention
signing in.

Deliberately *not* here: a bare 'Use --cookies...' hint. yt-dlp appends it to private-video
errors as well as to bot checks, so matching on it would reclassify a confirmed-private
video as merely needing credentials -- the exact opposite of the truth. The discriminator
is the specific reason, never the hint.
"""

UNAVAILABLE_PATTERNS: tuple[str, ...] = (
    r'.*[Vv]ideo unavailable.*',                             # yt: unavailable / takedown
    r'.*has been removed for violating.*Terms of Service.*',  # yt: ToS removal
    r'.*[Pp]rivate video.*',                                 # yt: private
    r'.*[Pp]lease sign in.*',                                # yt: private video
    r'.*not archived or indexed.*',                          # wa: not indexed
)

_ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')
_TAG_RE = re.compile(r'.*?\[([^\[\]]+?)\].*')
_PREFIX_RE = re.compile(r'^\s*ERROR:\s*(.+)', re.DOTALL)
_NOT_FOUND_RE = re.compile(r'.*(?:does not exist|not found|Unable to recognize).*', re.IGNORECASE)


@dataclass(frozen=True, slots=True, kw_only=True)
class Classification:
    """The verdict on one error message."""

    error_class: ErrorClass
    message: str
    """The body, with any ERROR: prefix removed."""
    tag: str = ''
    """The extractor tag from the first [...] group: 'youtube', 'web.archive:youtube', ...."""

    @property
    def confirmed_unavailable(self) -> bool:
        """True only when the platform positively said the video is gone.

        AUTH_REQUIRED and UNRECOGNIZED are deliberately False: both describe a video that may
        well still be there, and treating them as confirmed is what freezes a live video for
        a week.
        """
        return self.error_class is ErrorClass.UNAVAILABLE

    @property
    def is_transient(self) -> bool:
        """True when retrying later is reasonable without any user action."""
        return self.error_class in (
            ErrorClass.TIMED_OUT, ErrorClass.HTTP_403, ErrorClass.UNRECOGNIZED)


def classify(message: str, *, expects_auth: bool = False) -> Classification:
    """Classify a yt-dlp error message. Pure: no printing, no I/O, total over its input.

    `message` is expected to have had ANSI escapes stripped by ytdlp/ at capture, but an
    escaped or unescaped `ERROR:` prefix is tolerated either way rather than warned about.

    `expects_auth` says the call targeted something only visible when signed in ('LL', 'WL',
    a private playlist). It turns a bare "does not exist" -- which is what yt-dlp says for a
    private playlist you cannot see -- into AUTH_REQUIRED, so the reported cause is the
    credential rather than the playlist.
    """
    clean = _ANSI_RE.sub('', message)
    body = match.group(1) if (match := _PREFIX_RE.match(clean)) else clean
    tag = match.group(1) if (match := _TAG_RE.match(clean)) else ''

    for pattern, error_class in MISC_ERRORS.items():
        if re.match(pattern, body):
            return Classification(error_class=error_class, message=body, tag=tag)

    if any(re.match(p, body) for p in AUTH_PATTERNS):
        return Classification(error_class=ErrorClass.AUTH_REQUIRED, message=body, tag=tag)

    if expects_auth and _NOT_FOUND_RE.match(body):
        return Classification(error_class=ErrorClass.AUTH_REQUIRED, message=body, tag=tag)

    if any(re.match(p, body) for p in UNAVAILABLE_PATTERNS):
        return Classification(error_class=ErrorClass.UNAVAILABLE, message=body, tag=tag)

    return Classification(error_class=ErrorClass.UNRECOGNIZED, message=body, tag=tag)


# ----------------------------------------------------------------------- issues --

class Severity(StrEnum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    """The record cannot be trusted until this is resolved."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Issue:
    """Something wrong with the record, reported rather than raised or prompted about.

    A user-owned file that is missing, truncated or hand-mangled produces an Issue and the
    record still opens, still answers queries from the roster, and still commits. Only the
    roster itself is allowed to make opening fail.
    """

    code: str
    """Stable, greppable identifier, e.g. 'roster.missing', 'archive.desync'."""
    message: str
    severity: Severity = Severity.WARNING
    path: str | None = None
    detail: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        where = f' [{self.path}]' if self.path else ''
        return f'{self.severity.upper()}: {self.code}{where}: {self.message}'
