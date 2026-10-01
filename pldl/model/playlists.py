"""
Playlist-shaped envelopes: what one extraction captured, and what merging made of them.

`Capture` wraps one extraction's worth of `VideoEntry`s -- and, for a flat extraction, the
playlist's own top-level fields beside them, so a flat file and a per-video batch are the
same document with one slot empty. `MergePlaylist` is the merged counterpart: the same two
payloads after folding, plus the level reached and the per-video timeline. Generated playlist
documents therefore never carry `info_level` or `merge_timeline` inside a payload, which is
what `_v1_PL_InfoDict_Addons` is deprecated in favor of.

The roster is not here. It is pldl's own document with no yt-dlp payload behind it; see
roster.py.
"""
from __future__ import annotations

__all__ = ['Capture', 'MergePlaylist']

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from pldl.model.epoch import Epoch, get_epoch
from pldl.model.infodicts import PL_ID, V_ID, PL_InfoDict
from pldl.model.levels import PL_InfoLevel
from pldl.model.schema import SCHEMA_VERSION
from pldl.model.timeline import PlaylistTimeline
from pldl.model.videos import VideoEntry

_PLDL_PLAYLIST_KEYS = ('info_level', 'merge_timeline')
"""v1-compat: keys v1 wrote into a playlist payload. Dropped when wrapping a flat extraction;
a raw flat has no level worth keeping and never had a timeline."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Capture:
    """One extraction's worth of entries, and the epoch it was taken at.

    A flat extraction also carries the playlist's own top-level fields in `playlist`; a
    per-video batch has none and leaves it `None`. Either way this is a batch, so it is not
    valid yt-dlp infojson and does not claim to be -- `unwrap_flat()` rebuilds the infodict a
    flat extraction came from, and individual entries unwrap to payloads that are.
    """

    epoch: Epoch
    playlist: Mapping[str, Any] | None = None
    """The flat extraction's top level, without `entries`. `None` for a per-video batch."""
    videos: tuple[VideoEntry, ...] = ()
    schema_version: int = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.epoch, Epoch):
            object.__setattr__(self, 'epoch', Epoch(self.epoch))
        if self.playlist is not None and not isinstance(self.playlist, MappingProxyType):
            object.__setattr__(self, 'playlist', MappingProxyType(dict(self.playlist)))

    @classmethod
    def wrap_flat(cls, pl_info: PL_InfoDict | Mapping[str, Any]) -> Capture:
        """v1-compat: Build a capture from a flat extraction as yt-dlp returned it.

        The entries are wrapped one by one; everything else is the playlist payload, minus
        the keys v1 used to write in.
        """
        return cls(
            epoch=get_epoch(pl_info),
            playlist={k: v for k, v in pl_info.items()
                      if k != 'entries' and k not in _PLDL_PLAYLIST_KEYS},
            videos=tuple(VideoEntry.wrap(entry) for entry in pl_info.get('entries') or ()),
        )

    def unwrap_flat(self) -> dict[str, Any]:
        """The flat extraction as one infodict again: playlist payload plus `entries`.

        Same content as what was wrapped; key order is the codec's business.
        """
        return {**(self.playlist or {}), 'entries': [entry.unwrap() for entry in self.videos]}

    @property
    def pl_id(self) -> PL_ID | None:
        return None if self.playlist is None else self.playlist.get('id')

    def __len__(self) -> int:
        return len(self.videos)

    def get(self, v_id: V_ID) -> VideoEntry | None:
        for entry in self.videos:
            if entry.id == v_id:
                return entry
        return None

    def ids(self) -> tuple[V_ID, ...]:
        return tuple(entry.id for entry in self.videos)


@dataclass(frozen=True, slots=True, kw_only=True)
class MergePlaylist:
    """The merged playlist: what `merge/` returns and `kinds.MERGE_INFO` stores.

    A `Capture` after folding. `playlist` and each entry's `data` are merged payloads, so
    they are pldl's synthesis rather than any one extractor's output, and no `unwrap` is
    offered -- there is no original to get back to. `videos` are in roster order.
    """

    id: PL_ID
    epoch: Epoch
    """The newest source folded in."""
    info_level: PL_InfoLevel
    playlist: Mapping[str, Any] = field(default_factory=dict)
    videos: tuple[VideoEntry, ...] = ()
    timeline: PlaylistTimeline = field(default_factory=dict)
    schema_version: int = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.epoch, Epoch):
            object.__setattr__(self, 'epoch', Epoch(self.epoch))
        if not isinstance(self.playlist, MappingProxyType):
            object.__setattr__(self, 'playlist', MappingProxyType(dict(self.playlist)))

    def __len__(self) -> int:
        return len(self.videos)

    def get(self, v_id: V_ID) -> VideoEntry | None:
        for entry in self.videos:
            if entry.id == v_id:
                return entry
        return None

    def ids(self) -> tuple[V_ID, ...]:
        return tuple(entry.id for entry in self.videos)
