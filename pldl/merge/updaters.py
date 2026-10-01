"""
Per-field rules: which value wins, and whether the change is worth recording.

Two callables, deliberately named apart, because conflating them is easy and the consequences
are opposite -- one silently loses data, the other silently loses history:

    MergeUpdater(current, incoming) -> winner
        A binary operator over two `Candidate`s for one field. Returns the one that stands
        (or builds a new one). It never sees the dict or the key, and it never reports whether
        anything changed -- `resolve_into` derives that once, for every rule.

    TimelineFilter(key) -> record: bool
        Decides whether a change to `key` is written to the timeline. `view_count` moves every
        session and recording it would drown everything else; `title` moving is the whole
        point of keeping a record.

# ---- a candidate carries its own provenance ----

`Candidate(value, rank)` is a value together with the `Rank` -- `(epoch, level)` -- of the
source that supplied it. The fold keeps one per key, so the state a rule like
`latest_not_none` needs, *the rank of the source whose value counted for this key*, sits on
the value itself. A rank only moves when a value is accepted: a rejected `None`, or a source
that lacked the key, leaves the current candidate and its rank untouched, so it cannot block
an older source that does have the value.

    {epoch 1, data "First"}  {epoch 3, data None}  {epoch 2, data "Final"}   -> "Final"

That property is what makes every rule here stateless. There is no instance to reset between
videos, a module-constant table is safe to share, and the fold has no business logic of its
own -- it builds candidates, asks the rule, and writes the answer.

# ---- order ----

Final values do not depend on the order sources are folded in; the rules compare ranks, not
positions. The **timeline** does depend on it: a value that was never current is never
recorded, so folding out of chronological order loses intermediate states. The fold decides
the order; `model.rank` is the chronological one.

# ---- absent vs None ----

A key the input lacks is `NO_VALUE`, distinct from `None`: absent means "this extractor did not
say", `None` means "it said nothing is there". A winner whose value is `NO_VALUE` is **kept**
as a tombstone rather than deleted, so its rank survives: under `latest`, the newest source
saying "absent" must keep beating an older source that has a value, in whatever order the two
arrive. `values_of()` drops the tombstones when the fold projects the payload out.

# ---- what never reaches a table ----

The tables apply to the payload -- `VideoEntry.data` -- and nothing else. Envelope fields are
pldl's and their merge is structural, not policy: `id` is what the sources were grouped by,
`info_level` only rises, `unavailable_infos` is a union, `playlist_epoch` is the newest. The
fold owns them and a table cannot reach them, so no table needs a `keep` row to defend them.

# ---- the rules ----

    keep              never changes. The default of a whitelist table.
    latest            the newer candidate wins, even when that removes the key.
    latest_not_none   the newer candidate wins unless it is None or absent. The sensible
                      default: an extractor that omits a field is saying "I don't know", not
                      "it is empty".
    fill_absent       only fills a missing key. For values that should never move once known.
    maximum           only a larger value wins. For counters that should not appear to shrink.
    richest           the richer source wins; among equally rich, the newer. For fields a flat
                      extraction carries a poorer copy of, such as `thumbnails`.
    richest_not_none  `richest`, ignoring None and absent.

# ---- the tables ----

`MergeUpdaterMap` maps fields to rules. `table[key]` never fails: an unlisted key gets the
table's default. Building one from groups of keys raises if a key is listed twice, so two
rules can never silently disagree about the same field.

    COMMON_UPDATER  for a video's payload. `latest_not_none` by default; the exceptions are
                    the fields where a flat extraction carries a poorer copy, or where the
                    value describes what a *download* selected and a later extraction that
                    downloaded nothing must not overwrite it.
    ROSTER_UPDATER  for folding into the roster. A **whitelist** derived from the context
                    source tables, with `keep` as the default, so the roster only ever
                    accumulates the fields its context can hold and cannot drift into being a
                    second copy of the merge.
    PL_UPDATER      for the playlist's own payload. `latest_not_none` throughout: v1 took the
                    newest pl_info wholesale, None included, so this is the same policy with
                    the one guard every other field gets.

    COMMON_TIMELINE_KEYS  the fields whose changes are worth a timeline entry. The default
                    `TimelineFilter` is this set's `__contains__`.

# ---- open, and worth resolving with a test ----

Folding a video's own info into the roster gives that entry an epoch equal to its source, so
the two collide. v1 subtracted a second from the roster's copy to keep them distinguishable,
which works but splits one extraction across two timeline instants a second apart. Now that
several timeline entries may share an epoch and are ordered by `(epoch, level)`, ranking the
roster's copy below its source by *level* is available instead, and costs no fake time. Write
the test first and pick whichever reads correctly.
"""
from __future__ import annotations

__all__ = [  # noqa: RUF022
    'NO_VALUE', 'Candidate', 'ZERO_CANDIDATE',
    'MergeUpdater', 'TimelineUpdateFilter',
    'keep', 'latest', 'latest_not_none', 'fill_absent', 'maximum',
    'richest_latest', 'richest_latest_not_none',
    'MergeUpdaterMap', 'COMMON_UPDATER', 'ROSTER_UPDATER', 'PL_UPDATER', 'COMMON_TIMELINE_KEYS',
    'apply_updater', 'unwrap_candidates',
]

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from itertools import chain
from types import MappingProxyType
from typing import Any, Final, Literal, NamedTuple

from pldl.downloader import Rank
from pldl.roster import PLAYLIST_CONTEXT_SOURCES, VIDEO_CONTEXT_SOURCES


# ---- sentinels ----

class _FalsySentinelMeta(type):
    def __repr__(cls) -> str:
        return f'<{cls.__name__}>'

    def __bool__(cls) -> Literal[False]:
        return False


class NO_VALUE(metaclass=_FalsySentinelMeta):
    """Differentiate absent from `None`/default value.

    Falsy and never instantiated -- it is used as the class itself, so `is NO_VALUE` is the
    identity check and `if value:` treats it like any other empty value.
    """


# ---- candidates ----

class Candidate(NamedTuple):
    """A value and the rank of the source that supplied it."""

    value: Any
    """May be `NO_VALUE`: the source did not carry this key."""
    rank: Rank


ZERO_CANDIDATE: Final = Candidate(NO_VALUE, Rank(-1, -1))
"""What a key holds before any source has spoken. Ranks below every real source."""

type MergeUpdater = Callable[[Candidate, Candidate], Candidate]
"""`(current, incoming) -> winner`."""

type TimelineUpdateFilter = Callable[[str], bool]
"""`(key) -> record`. A frozenset's `__contains__` is a perfectly good one."""


def _blank(candidate: Candidate) -> bool:
    return candidate.value is NO_VALUE or candidate.value is None


# ---- the rules ----

def keep(current: Candidate, incoming: Candidate) -> Candidate:
    return current


def latest(current: Candidate, incoming: Candidate) -> Candidate:
    return incoming if incoming.rank >= current.rank else current


def latest_not_none(current: Candidate, incoming: Candidate) -> Candidate:
    return current if _blank(incoming) else latest(current, incoming)


def fill_absent(current: Candidate, incoming: Candidate) -> Candidate:
    return incoming if current.value is NO_VALUE else current


def maximum(current: Candidate, incoming: Candidate) -> Candidate:
    """A known value replaces an unknown one; otherwise the larger wins.

    Keeps the current value when the two do not compare -- a count that came back as a
    string is not a bigger count.
    """
    if _blank(incoming):
        return current
    if _blank(current):
        return incoming
    try:
        return incoming if incoming.value > current.value else current
    except TypeError:
        return current


def richest_latest(current: Candidate, incoming: Candidate) -> Candidate:
    """`latest` with the level compared first: `(level, epoch)` rather than `(epoch, level)`.

    Strict on level, so a DOWNLOAD-level value also outranks a fresher EXTRACT-level one.
    That is right for anything a download adds and harmless for the rest, since a downloaded
    video is rarely extracted again.
    """
    incoming_key = (incoming.rank.level, incoming.rank.epoch)
    current_key = (current.rank.level, current.rank.epoch)
    return incoming if incoming_key >= current_key else current


def richest_latest_not_none(current: Candidate, incoming: Candidate) -> Candidate:
    return current if _blank(incoming) else richest_latest(current, incoming)


# ---- the tables ----

@dataclass(frozen=True, slots=True)
class MergeUpdaterMap:
    """Which rule handles which field. Indexing never fails; unlisted keys get `default`."""

    updater_map: Mapping[str, MergeUpdater]
    default: MergeUpdater

    def __post_init__(self) -> None:
        object.__setattr__(self, 'updater_map', MappingProxyType(dict(self.updater_map)))

    @classmethod
    def grouped(cls, groups: Mapping[tuple[str, ...], MergeUpdater], *,
                default: MergeUpdater) -> MergeUpdaterMap:
        """From groups of keys sharing a rule, which is how a long table reads best.

        Raises if a key appears in two groups: a flat dict cannot hold a duplicate, but a
        grouped one can, and the second listing would silently win.
        """
        updater_map: dict[str, MergeUpdater] = {}
        for keys, updater in groups.items():
            for key in keys:
                if key in updater_map:
                    raise ValueError(f'{key!r} is listed under two updaters')
                updater_map[key] = updater
        return cls(updater_map, default)

    def __getitem__(self, key: str) -> MergeUpdater:
        return self.updater_map.get(key, self.default)

COMMON_UPDATER: Final = MergeUpdaterMap.grouped({
    # A flat entry's reference to a video it has not resolved. A real extraction supersedes
    # them -- by absence, since it carries none -- and a later flat cannot bring them back.
    ('_type', 'ie_key', 'url'): richest_latest,

    # A flat extraction carries four; a full extraction carries forty-five.
    ('thumbnails',): richest_latest_not_none,

    # What was selected -- and, for a download, what is on disk. A fresher extraction that
    # downloaded nothing must not end up describing a file that was never written. The
    # inventories these were selected from (`formats`, `subtitles`, `automatic_captions`)
    # stay on the default: every full extraction sees the same inventory, and the URLs in
    # them expire, so the newest is the useful one.
    ('ext', 'format', 'format_id', 'format_note', 'resolution', 'width', 'height', 'fps',
     'vcodec', 'acodec', 'abr', 'vbr', 'tbr', 'asr', 'audio_channels', 'dynamic_range',
     'aspect_ratio', 'protocol', 'container', 'language', 'filesize', 'filesize_approx',
     'requested_formats', 'requested_subtitles'): richest_latest_not_none,

    # Counts (`view_count`, `like_count`, ...) are deliberately left to the default rather
    # than `maximum`: a drop is information, and v1 made the same call.
}, default=latest_not_none)

_ROSTER_KEYS: Final = tuple(dict.fromkeys(chain.from_iterable(
    (*VIDEO_CONTEXT_SOURCES.values(), *PLAYLIST_CONTEXT_SOURCES.values()))))
"""Every payload key a context field can be read from, and nothing else."""

ROSTER_UPDATER: Final = MergeUpdaterMap.grouped({_ROSTER_KEYS: latest_not_none}, default=keep)

PL_UPDATER: Final = MergeUpdaterMap({}, default=latest_not_none)

COMMON_TIMELINE_KEYS: Final = frozenset({
    'title', 'description', 'categories', 'tags',
    'uploader', 'uploader_id', 'channel', 'creators', 'creator',
    'release_year', 'modified_date', 'availability', 'live_status',
    'extractor',
})
"""Changes worth an entry. Everything else moves too often (`view_count`), or describes the
extraction rather than the video (`formats`), or is derivable (`duration_string`). `extractor`
is here because a switch to a mirror is a fact about the video's fate."""


# ---- application ----

def apply_updater(merged: dict[str, Candidate], key: str, incoming: Candidate,
                 updater: MergeUpdater) -> bool:
    """Resolve one field in place. Returns whether the field's *value* changed.

    A `NO_VALUE` winner is stored, not popped: it is a tombstone whose rank keeps an older
    value from resurrecting the key. `values_of` is where it disappears.
    """
    current = merged.get(key, ZERO_CANDIDATE)
    winner = merged[key] = updater(current, incoming)
    return winner.value is not current.value and winner.value != current.value

def wrap_candidates(d: dict[str, Any], rank: Rank) -> dict[str, Candidate]:
    return {k: Candidate(v, rank) for k, v in d.items()}

def unwrap_candidates(merged: Mapping[str, Candidate]) -> dict[str, Any]:
    """The payload a fold produced: values only, with `NO_VALUE` dropped"""
    return {k: candidate.value for k, candidate in merged.items()
            if candidate.value is not NO_VALUE}
