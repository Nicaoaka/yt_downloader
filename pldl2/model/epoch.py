"""
Time. **Ints are canonical; ISO-8601 local strings with an explicit offset are readable.**

Every durable timestamp is stored as both: `epoch` (unambiguous, sortable, arithmetic-safe)
and `at` (standard, human-readable, and in your timezone). Keeping both is what lets the
record be read by eye without any of the old ambiguity, because **the offset travels with
each timestamp** -- so DST is correct without touching a path template.

What this replaces, and why each mattered:

  - `to_readable_epoch` / `from_readable_epoch` used local wall-clock with no offset, so the
    two epochs an hour apart in the DST fall-back hour produce the same string and the
    reverse mapping keeps only the first. Those strings were **dict keys in files that are
    never rewritten**, so history rows and timeline entries from that hour merged into one
    bucket and backoff arithmetic was 3600s off for them (issue-1 #17, reproduced on this
    machine: 1793520600 and 1793524200 both give '2026-11-01__01-10-00').
  - The path templates hardcoded `epoch-25200`, with a comment admitting "This will need
    adjusting if you have daylight savings". `datetime.astimezone()` reads the *actual*
    offset in force at that instant, so half the year stops being an hour wrong.

The legacy readers are kept for exactly one caller, store/migrate.py, and are not part of
the v2 vocabulary.
"""
from __future__ import annotations

__all__ = [
    'epoch_now',
    'get_epoch', 'get_latest_epoch',
    'to_iso', 'from_iso',
    'to_file_stamp', 'FILE_STAMP_FMT',
    'to_legacy_key', 'from_legacy_key', 'LEGACY_KEY_FMT', 'MALFORMED_EPOCH_FMT',
]

import datetime
import re
import time
from typing import Any

FILE_STAMP_FMT = '%Y-%m-%d %H-%M-%S'
"""Local readable time for filenames. Matches what v1 wrote, so sorted globs still work."""

LEGACY_KEY_FMT = '%Y-%m-%d__%H-%M-%S'
"""v1's dict-key format for `history` and `merge_timeline`. Read-only, for the migrator."""

MALFORMED_EPOCH_FMT = '{} (malformed)'
"""v1 wrapped unusable epochs in this. Read-only, for the migrator."""


def epoch_now() -> int:
    return int(time.time())


def get_epoch(info: Any, default: int = 0) -> int:
    """An info's own epoch.

    v1 used `-epoch_now()` as the "not found" value, so a missing epoch became a large
    negative number that still compared and sorted like a real one. Here the default is
    explicit and the caller picks it.
    """
    value = info.get('epoch') if hasattr(info, 'get') else None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return default
    return int(value)


def get_latest_epoch(pl_info: Any, default: int = 0) -> int:
    """Max epoch across a playlist infodict and its entries."""
    epochs = [get_epoch(pl_info, default=None)]  # type: ignore[arg-type]
    for entry in (pl_info.get('entries') or []):
        epochs.append(get_epoch(entry, default=None))  # type: ignore[arg-type]
    found = [e for e in epochs if e is not None]
    return max(found) if found else default


# ------------------------------------------------------------------ canonical pair --

def _local(epoch: int) -> datetime.datetime:
    """Epoch -> an aware local datetime, for any epoch a 64-bit int can hold.

    Built in UTC and then converted, rather than via a naive `fromtimestamp(epoch)`. The
    naive form asks the platform to render local time directly and **raises OSError on
    Windows for epochs near 0**, because in a negative-offset zone the local time falls
    before 1970. That is the real reason v1 carried a MALFORMED_EPOCH_FMT wrapper and a
    "low epochs can be invalid because of timezones" guard; converting through UTC is
    arithmetic on an aware datetime and has no such hole.
    """
    return datetime.datetime.fromtimestamp(epoch, tz=datetime.UTC).astimezone()


def to_iso(epoch: int) -> str:
    """Epoch -> '2026-08-29T15:24:56-07:00'.

    `astimezone()` attaches the local zone's offset *as it was at that instant*, which is
    what makes this DST-correct and round-trippable.
    """
    return _local(epoch).isoformat()


def from_iso(at: str) -> int:
    """'2026-08-29T15:24:56-07:00' -> epoch. Exact inverse of to_iso()."""
    return int(datetime.datetime.fromisoformat(at).timestamp())


# --------------------------------------------------------------------- filenames --

def to_file_stamp(epoch: int) -> str:
    """Epoch -> '2026-08-29 15-24-56', for readable filenames.

    **Not injective**, and deliberately so: it stays readable and matches v1's filenames, at
    the cost of two instants one hour apart in the DST fall-back hour producing the same
    stamp. That is fine here and was not fine for v1's dict keys, because a filename
    collision is visible and resolvable at write time, whereas a silently merged dict key is
    neither. store/ is responsible for disambiguating; nothing may treat this as an id.
    """
    return _local(epoch).strftime(FILE_STAMP_FMT)


# ------------------------------------------------------------- v1 compatibility --

def to_legacy_key(epoch: int) -> str:
    """v1's readable key. Present so the migrator can regenerate a key and match it."""
    is_negative = epoch < 0
    if abs(epoch) <= 3600 * 24:
        return MALFORMED_EPOCH_FMT.replace('{}', str(epoch))
    formatted = (datetime.datetime.fromtimestamp(abs(epoch))
                 .astimezone(None).strftime(LEGACY_KEY_FMT))
    if is_negative:
        return MALFORMED_EPOCH_FMT.replace('{}', '-' + formatted)
    return formatted


def from_legacy_key(readable: str) -> int:
    """Parse a v1 readable key back to an epoch.

    Lossy for the DST fall-back hour -- that is the defect, not a bug in this reader. The
    migrator therefore treats a legacy key as a *best-effort* epoch and never as an identity.
    """
    malformed_re = ('^' + re.escape(MALFORMED_EPOCH_FMT.replace('{}', '__sub__'))
                    .replace('__sub__', '(-?)(.+)') + '$')
    low_epoch_re = ('^' + re.escape(MALFORMED_EPOCH_FMT.replace('{}', '__sub__'))
                    .replace('__sub__', r'(-?\d+)') + '$')

    if match := re.match(low_epoch_re, readable):
        return int(match.group(1))

    sign = 1
    if match := re.match(malformed_re, readable):
        sign = -1 if match.group(1) else 1
        readable = match.group(2)

    try:
        return sign * int(datetime.datetime.strptime(readable, LEGACY_KEY_FMT)
                          .astimezone(None).timestamp())
    except ValueError:
        pass

    try:
        return int(readable)
    except ValueError:
        raise ValueError(f'{readable!r} is not a recognized v1 readable epoch') from None
