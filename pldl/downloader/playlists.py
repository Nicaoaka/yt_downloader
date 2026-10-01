"""
What one extraction captured.

`Capture` wraps one extraction's worth of `VideoEntry`s -- and, for a flat extraction, the
playlist's own top-level fields beside them, so a flat file and a per-video batch are the
same document with one slot empty.
"""
from __future__ import annotations

__all__ = ['Capture']

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from pldl.downloader.infodicts import PL_ID, V_ID, PL_InfoDict
from pldl.downloader.videos import VideoEntry
from pldl.model import SCHEMA_VERSION, Epoch, get_epoch

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
