"""
How much is known about a video, and how competing values are ranked.

`V_InfoLevel` and `PL_InfoLevel` say how complete an infodict is. Both are declared on the
infodict and re-derivable from its content, so a file can be trusted or checked.

**`rank(level, epoch)` is the merge's resolution rule.** Level dominates and epoch breaks ties
within a level, so a richer old extraction always beats a poorer new one -- a flat refresh
never overwrites what a full download knew. It resolves *fields*, not order: the merge folds
its inputs chronologically and picks each field by rank, which keeps the timeline reading as
history while still storing the best available value. Doing it the other way round, ranking
the input list, makes a newer flat entry appear before an older extraction and the recorded
progression reads backwards.

Derivation is pure and never reports. `v_level_mismatch()` returns a disagreement between the
declared and derived level as a value, leaving it to the caller to decide whether that is
worth surfacing.
"""
from __future__ import annotations

__all__ = [  # noqa: RUF022
    'V_InfoLevel', 'PL_InfoLevel',
    'coerce_v_level', 'coerce_pl_level',
    'derive_v_info_level', 'derive_pl_info_level',
    'v_level_mismatch', 'pl_level_mismatch',
    'rank', 'rank_of',
    'LARGE_TIME_DELTA',
]

from collections.abc import Mapping
from enum import IntEnum
from typing import Any

type _AnyInfo = Mapping[str, Any]


class V_InfoLevel(IntEnum):
    """How much is known about one video. Values must stay >= 0 and ordered."""
    NONE = 0
    FLAT = 1
    EXTRACT = 2
    DOWNLOAD = 3


class PL_InfoLevel(IntEnum):
    """How much is known about a playlist document."""
    NONE = 0
    FLAT = 1
    MERGE_FLAT = 2
    NORMAL = 3
    MERGE = 4


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


def coerce_pl_level(value: PL_InfoLevel | str | int | None) -> PL_InfoLevel:
    """Best-effort conversion to a PL_InfoLevel. Anything unrecognized becomes NONE.
    
    v1-compat: recognizes int-serialized versions.
    """
    if isinstance(value, PL_InfoLevel):
        return value
    if value is None:
        return PL_InfoLevel.NONE
    if isinstance(value, str):
        return PL_InfoLevel.__members__.get(value, PL_InfoLevel.NONE)
    if isinstance(value, int) and not isinstance(value, bool):
        try:
            return PL_InfoLevel(value)
        except ValueError:
            return PL_InfoLevel.NONE
    return PL_InfoLevel.NONE


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


def derive_pl_info_level(pl_info: _AnyInfo | None) -> PL_InfoLevel:
    """The level implied by the *content* of a playlist infodict. Pure."""
    if not pl_info:
        return PL_InfoLevel.NONE
    has_extracts = any(derive_v_info_level(entry) >= V_InfoLevel.EXTRACT
                       for entry in pl_info.get('entries', []))
    has_merge_timeline = 'merge_timeline' in pl_info
    match has_extracts, has_merge_timeline:
        case False, False: return PL_InfoLevel.FLAT
        case False, True:  return PL_InfoLevel.MERGE_FLAT
        case True, False:  return PL_InfoLevel.NORMAL
        case _:            return PL_InfoLevel.MERGE


def v_level_mismatch(v_info: _AnyInfo | None) -> tuple[str, V_InfoLevel] | None:
    """returns (declared, derived) when a video infodict's stated level disagrees with its content.

    None when they agree, when v_info is None, or 'info_level' is None.
    """
    if not v_info:
        return None
    declared = v_info.get('info_level')
    if declared is None:
        return None
    derived = derive_v_info_level(v_info)
    if str(declared) == derived.name:
        return None
    return str(declared), derived


def pl_level_mismatch(pl_info: _AnyInfo | None) -> tuple[str, PL_InfoLevel] | None:
    """returns (declared, derived) when a playlist infodict's stated level disagrees with content.
    
    None when they agree, when pl_info is None, or 'info_level' is None.
    """
    if not pl_info:
        return None
    declared = pl_info.get('info_level')
    if declared is None:
        return None
    derived = derive_pl_info_level(pl_info)
    if str(declared) == derived.name:
        return None
    return str(declared), derived


# ---- ranking ----

LARGE_TIME_DELTA = 10**12
"""~31,688 years. Big enough that no realistic epoch spread can bridge one level."""


def rank(info_level: V_InfoLevel | str | int | None, epoch: int) -> int:
    """Sort key: level dominates, epoch breaks ties within a level.

    **A richer old extraction always outranks a poorer new one.** That is the whole point --
    a flat refresh must never overwrite a full download's fields just because it happened
    later.
    """
    return (coerce_v_level(info_level).value * LARGE_TIME_DELTA) + epoch


def rank_of(v_info: _AnyInfo, epoch: int | None = None) -> int:
    """rank() applied to an infodict, taking its declared level and its own epoch.

    The declared level is used rather than the derived one so that ranking stays cheap and
    matches what the old sort key did.
    """
    if epoch is None:
        epoch = int(v_info.get('epoch', 0) or 0)
    return rank(v_info.get('info_level'), epoch)
