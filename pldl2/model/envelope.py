"""
An envelope around a byte-faithful payload.

v1 injected pldl's own fields -- `info_level`, `unavailable_msgs`, `playlist_epoch` -- directly
into the dict yt-dlp returned (yt_utils.py:127-130). Three costs followed, and all three go
away here:

  - `_merge_v_infos` had to `continue` on specific keys, and COMMON_UPDATER carried
    unreachable `no_update` entries for them -- "which keys are ours" was knowledge spread
    across three modules.
  - Any field a future yt-dlp release adds could collide with one of ours.
  - `data` was no longer what yt-dlp produced, so a stored entry could not be handed back to
    yt-dlp or compared against a fresh extraction.

Here pldl's fields live on the envelope and `data` stays exactly what the extractor returned.
Unwrapping is a pure projection, which is what makes the migration mechanically reversible
and lets it be gated on `data` round-tripping byte-identically.

`info_level` also stops being re-derived from content on every read. It is a real field with
one encode/decode pair -- which is the fix for a v1 file that stored the enum itself and
serialized it to `0`, becoming permanently un-re-addable (issue-1 #23).

A future SQLite index falls out of this shape for free: the envelope fields are the columns,
`data` is the blob.
"""
from __future__ import annotations

__all__ = ['VideoEntry', 'Capture']

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from pldl2.model.epoch import to_iso
from pldl2.model.infodicts import UnavailableMsg, V_ID
from pldl2.model.levels import V_InfoLevel, coerce_v_level, derive_v_info_level
from pldl2.model.schema import SCHEMA_VERSION


@dataclass(frozen=True, slots=True, kw_only=True)
class VideoEntry:
    """One video: pldl's fields, plus the extractor's output untouched in `data`."""

    id: V_ID
    info_level: V_InfoLevel
    data: Mapping[str, Any] = field(default_factory=dict)
    unavailable_msgs: tuple[UnavailableMsg, ...] = ()
    playlist_epoch: int | None = None

    @classmethod
    def wrap(cls, payload: Mapping[str, Any], *,
             info_level: V_InfoLevel | None = None) -> VideoEntry:
        """Build an envelope around a raw yt-dlp infodict.

        pldl keys already present in a v1 payload are lifted onto the envelope and stripped
        from `data`, so wrapping a v1 file yields the same shape as wrapping a fresh
        extraction. `info_level` is derived from content only when neither given nor declared.
        """
        declared = payload.get('info_level')
        if info_level is None:
            info_level = (coerce_v_level(declared) if declared is not None
                          else derive_v_info_level(payload))

        data = {k: v for k, v in payload.items()
                if k not in ('info_level', 'unavailable_msgs', 'playlist_epoch')}
        raw_msgs = payload.get('unavailable_msgs') or ()
        playlist_epoch = payload.get('playlist_epoch')

        return cls(
            id=str(payload.get('id', '')),
            info_level=info_level,
            data=data,
            unavailable_msgs=tuple(raw_msgs),
            playlist_epoch=playlist_epoch if isinstance(playlist_epoch, int) else None,
        )

    def unwrap(self) -> dict[str, Any]:
        """The payload exactly as it was wrapped. The inverse of `wrap` for `data`.

        Note this returns `data` alone -- it does **not** re-inject the pldl fields. That is
        deliberate: this is what gets handed back to yt-dlp or diffed against a fresh
        extraction, and it must be byte-faithful to what the extractor produced.
        """
        return dict(self.data)

    @property
    def epoch(self) -> int:
        value = self.data.get('epoch')
        return int(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else 0


@dataclass(frozen=True, slots=True, kw_only=True)
class Capture:
    """One stored file's worth of entries.

    v1's `_v_infos/*.json` was already a *batch* (a list of lists) and therefore already not
    valid yt-dlp infojson. The envelope makes that explicit rather than accidental, and gives
    the batch a place to record when it was taken.
    """

    epoch: int
    videos: tuple[VideoEntry, ...] = ()
    schema_version: int = SCHEMA_VERSION

    @property
    def at(self) -> str:
        return to_iso(self.epoch)

    def __len__(self) -> int:
        return len(self.videos)

    def get(self, v_id: V_ID) -> VideoEntry | None:
        for entry in self.videos:
            if entry.id == v_id:
                return entry
        return None

    def ids(self) -> tuple[V_ID, ...]:
        return tuple(entry.id for entry in self.videos)
