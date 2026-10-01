"""
How much is known about a video, and how sources are ordered.

`V_InfoLevel` says how complete a video infodict is. It is declared on the infodict and
re-derivable from its content, so a file can be trusted or checked.

**`rank(epoch, level)` is an ordering key, not a resolution rule.** It sorts chronologically
and uses the level only to separate two sources from the same second. Which value wins a field
is per-field and belongs to the merge's field updater; which of those changes gets written to
the timeline belongs to its update filter. Three questions, three mechanisms -- collapsing the
last two into a global ordering rule is what makes a timeline stop recording change.
"""
from __future__ import annotations

__all__ = [  # noqa: RUF022
    'V_InfoLevel',
    'coerce_v_level', 'derive_v_info_level',
    'Rank', 'rank',
]

from collections.abc import Mapping
from enum import IntEnum
from typing import Any, NamedTuple

type _AnyInfo = Mapping[str, Any]


class V_InfoLevel(IntEnum):
    """How much is known about one video. Values must stay >= 0 and ordered."""
    NONE = 0
    FLAT = 1
    EXTRACT = 2
    DOWNLOAD = 3


def coerce_v_level(value: V_InfoLevel | str | int | None) -> V_InfoLevel:
    """Best-effort conversion to a V_InfoLevel. Anything unrecognized becomes NONE.

    v1-compat: recognizes int-serialized versions.
    """
    if isinstance(value, V_InfoLevel):
        return value
    if value is None:
        return V_InfoLevel.NONE
    if isinstance(value, str):
        return V_InfoLevel.__members__.get(value, V_InfoLevel.NONE)
    if isinstance(value, int) and not isinstance(value, bool):
        try:
            return V_InfoLevel(value)
        except ValueError:
            return V_InfoLevel.NONE
    return V_InfoLevel.NONE


# ---- derivation ----

def _maybe_available_on_yt(info: _AnyInfo) -> bool:
    """True if the video might still be on YouTube. Returns True when unsure.
    
    Only flat extraction infos should be passed in. Full extractions from alternate
    sources like WA will almost always force returning True.
    """
    # Note: Do not use 'ie_key'
    # Only occurs in flat extraction. Usually stale and only ever uses youtube
    if info.get('extractor_key') == 'YoutubeWebArchive':
        return True
    # Got in flat extraction. Other stats would also work (e.g. `duration`).
    return info.get('channel') is not None


def _has_extracted_info(info: _AnyInfo) -> bool:
    return bool(info.get('extractor'))


def _has_download_info(info: _AnyInfo) -> bool:
    return bool(info.get('requested_downloads'))


def derive_v_info_level(v_info: _AnyInfo | None) -> V_InfoLevel:
    """The level implied by the *content* of a video infodict. Pure."""
    if not v_info:
        return V_InfoLevel.NONE
    if _has_download_info(v_info):
        return V_InfoLevel.DOWNLOAD
    if _has_extracted_info(v_info):
        return V_InfoLevel.EXTRACT
    if _maybe_available_on_yt(v_info):
        return V_InfoLevel.FLAT
    return V_InfoLevel.NONE


# ---- ordering ----

class Rank(NamedTuple):
    """Where a source sits in the record's history.

    A NamedTuple, so it compares and sorts exactly like the plain tuple it replaces while
    the two components have names at every use site.
    """

    epoch: int
    level: int


def rank(epoch: int, info_level: V_InfoLevel | str | int | None) -> Rank:
    """Sort key: **chronological, with the level as a tiebreak**.

    Orders things -- a timeline for reading, entries in a written file, the infodicts a merge
    folds. It says *when*, and the level only separates two sources from the same second.

    It does **not** decide which value wins a field. That is per-field and belongs to the
    merge's field updater, which is the only thing that can express rules like "a view count
    only ever goes up" or "never overwrite a title with nothing". A single global "richer
    source wins" rule cannot say either, and applying one would also empty the timeline: if
    an old full extraction outranks every later refresh, almost nothing registers as a change
    and the record stops showing what changed over time.

    Arguments are in sort order, so the signature reads the way the key sorts. A tuple
    rather than a packed int, so there is no multiplier to get wrong and both components
    stay legible.
    """
    return Rank(epoch, coerce_v_level(info_level).value)
