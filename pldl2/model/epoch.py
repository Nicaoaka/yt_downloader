"""
Time. **An epoch int is the only stored form; every readable form is derived from it.**

Nothing carries a timestamp twice. Written files may render an `at` beside an epoch for the
person reading the JSON, but that is the encoder's doing and never a second field to keep in
sync. ISO-8601 is the readable form because it carries the timezone offset, which makes it
unambiguous across DST without a custom template.

`Epoch` is an `int` subclass, extended with the conversion properties.
Note: Arithmetic on an `Epoch` will return an `int`. Wrap the result if you need the
properties back.

The legacy readers (`v1_*`) **should only be used by** store/migrate.py.
"""
from __future__ import annotations

__all__ = [  # noqa: RUF022
    'Epoch', 'EPOCH_ZERO',
    'get_epoch', 'get_latest_epoch',
    'to_iso', 'from_iso', 'to_file_stamp',
    'FILE_STAMP_FMT',
    'v1_to_readable_epoch', 'v1_from_readable_epoch',
    'LEGACY_KEY_FMT', 'MALFORMED_EPOCH_FMT',
]

import datetime
import re
import time
from typing import Any, Final, Self

FILE_STAMP_FMT: Final = '%Y-%m-%d %H-%M-%S'
"""Local readable time for filenames. Chosen so a lexicographic sort is chronological."""


class Epoch(int):
    """A point in time: Unix seconds, with the conversions attached.

    Being an `int` subclass is the point. It compares and sorts against the raw epochs in
    yt-dlp payloads, `json.dumps` writes it as a number with no encoder, and `isinstance(x,
    int)` stays true, so it is substitutable anywhere a plain epoch was expected.
    """

    __slots__ = ()

    @classmethod
    def now(cls) -> Self:
        return cls(time.time())

    @classmethod
    def from_iso(cls, at: str) -> Self:
        """`2026-08-29T15:24:56-07:00` -> Epoch"""
        return cls(datetime.datetime.fromisoformat(at).timestamp())

    @property
    def local(self) -> datetime.datetime:
        """An aware local datetime, for any epoch a 64-bit int can hold.

        Built in UTC and then converted rather than via a naive `fromtimestamp(epoch)`. The
        naive form asks the platform to render local time directly and raises OSError on
        Windows for epochs near 0, because in a negative-offset zone the local time falls
        before 1970. `astimezone()` attaches the local offset *as it was at that instant*, so
        DST is accounted for without any fixed offset in a template.
        """
        return datetime.datetime.fromtimestamp(self, tz=datetime.UTC).astimezone()

    @property
    def iso(self) -> str:
        """`2026-08-29T15:24:56-07:00`. The canonical readable form."""
        return self.local.isoformat()

    @property
    def file_stamp(self) -> str:
        """`2026-08-29 15-24-56`, for readable filenames.

        **Ambiguous by design**: it carries no offset, so the two instants an hour apart in
        the DST fall-back hour produce the same stamp. That is acceptable for a filename,
        where a collision is visible and resolvable at write time, and unacceptable for a key,
        which is why nothing is keyed by it. store/ disambiguates; never treat it as an id.
        """
        return self.local.strftime(FILE_STAMP_FMT)

    def __repr__(self) -> str:
        return f'Epoch({int(self)} = {self.iso})'


EPOCH_ZERO: Final[Epoch] = Epoch(0)
"""The zero epoch, as a shared constant.

Use this as a dataclass field default rather than `Epoch(0)`. Both are safe, since Epoch is
immutable, but a call in a default trips RUF009 and a name reference does not.
"""


def _raw_epoch(info: Any) -> int | None:
    """An infodict's `epoch` when it holds a usable number, else None.

    `bool` is excluded deliberately: it is an `int` subclass, so `True` would have returned 1.
    """
    value = info.get('epoch') if hasattr(info, 'get') else None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return int(value)


def get_epoch(info: Any, default: int = 0) -> Epoch:
    """Get an infodict's own epoch."""
    value = _raw_epoch(info)
    return Epoch(default if value is None else value)


def get_latest_epoch(pl_info: Any, default: int = 0) -> Epoch:
    """Max epoch across a playlist infodict and its entries."""
    entries = pl_info.get('entries') if hasattr(pl_info, 'get') else None
    found = [e for e in (_raw_epoch(info) for info in (pl_info, *(entries or ())))
             if e is not None]
    return Epoch(max(found) if found else default)


# ---- conversions for raw ints ----

def to_iso(epoch: int) -> str:
    """Epoch -> `2026-08-29T15:24:56-07:00`"""
    return Epoch(epoch).iso


def from_iso(at: str) -> Epoch:
    """`2026-08-29T15:24:56-07:00` -> Epoch"""
    return Epoch.from_iso(at)


def to_file_stamp(epoch: int) -> str:
    """Epoch -> `2026-08-29 15-24-56`. See `Epoch.file_stamp`."""
    return Epoch(epoch).file_stamp


# ---- v1-compat ----

LEGACY_KEY_FMT: Final = '%Y-%m-%d__%H-%M-%S'
"""v1's dict-key format for `history` and `merge_timeline`. Read-only, for the migrator."""

MALFORMED_EPOCH_FMT: Final = '{} (malformed)'
"""v1 wrapped unusable epochs in this. Read-only, for the migrator."""

_TMP_RE_SUB: Final = '__sub__'
# assert _TMP_RE_SUB not in MALFORMED_EPOCH_FMT # pretty obvious and fmts are stable
"""'__sub__' is used as a temporary value and must not be in `MALFORMED_EPOCH_FMT`"""


def v1_to_readable_epoch(epoch: int) -> str:
    """v1's readable key. Present so the migrator can regenerate a key and match it."""
    is_negative = epoch < 0
    if abs(epoch) <= 3600 * 24:
        return MALFORMED_EPOCH_FMT.replace('{}', str(epoch))
    formatted = (datetime.datetime.fromtimestamp(abs(epoch))
                 .astimezone(None).strftime(LEGACY_KEY_FMT))
    if is_negative:
        return MALFORMED_EPOCH_FMT.replace('{}', '-' + formatted)
    return formatted


def v1_from_readable_epoch(readable: str) -> Epoch:
    """Parse a v1 readable key back to an epoch.

    Lossy across the DST fall-back hour, because the format it parses carries no offset. The
    migrator therefore treats a legacy key as a best-effort epoch and never as an identity.
    """
    malformed_re = ('^' + re.escape(MALFORMED_EPOCH_FMT.replace('{}', _TMP_RE_SUB))
                    .replace(_TMP_RE_SUB, '(-?)(.+)') + '$')
    low_epoch_re = ('^' + re.escape(MALFORMED_EPOCH_FMT.replace('{}', _TMP_RE_SUB))
                    .replace(_TMP_RE_SUB, r'(-?\d+)') + '$')

    if match := re.match(low_epoch_re, readable):
        return Epoch(match.group(1))

    sign = 1
    if match := re.match(malformed_re, readable):
        sign = -1 if match.group(1) else 1
        readable = match.group(2)

    try:
        return Epoch(sign * int(datetime.datetime.strptime(readable, LEGACY_KEY_FMT)
                                .astimezone(None).timestamp()))
    except ValueError:
        pass

    try:
        return Epoch(readable)
    except ValueError:
        raise ValueError(f'{readable!r} is not a recognized v1 readable epoch') from None
