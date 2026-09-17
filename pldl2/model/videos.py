"""
Envelope pattern around a payload.

pldl's own fields sit on the envelope; `data` is exactly what the extractor returned.
This gives easier comparison and future-proofing for unstable or added yt-dlp infodict kvals.
Unwrapping to raw data is trivial.

Three envelopes, one shape. `VideoEntry` wraps one video. `Capture` wraps one extraction's
worth of them -- and, for a flat extraction, the playlist's own top-level fields beside them,
so a flat file and a per-video batch are the same document with one slot empty.
`MergeDocument` is the merged counterpart of a `Capture`: same two payloads after folding,
plus the level reached and the timeline. Generated playlist documents therefore never carry
`info_level` or `merge_timeline` inside the payload, which is what `_v1_PL_InfoDict_Addons`
is deprecated in favor of.

`data` is typed `YT_DLP_InfoDict` rather than `V_InfoDict` on purpose: `V_InfoDict` is the
payload *plus* pldl's addon keys, so using it would re-admit `info_level` and other custom keys
as legitimate payload keys, which is the purpose of the envelope design pattern. `wrap()` accepts
the wider type (v1-compat V_InfoDict) and produces the narrower.

In the future the envelope fields can be the columns of a SQLite DB with `data` as blobs.
"""
from __future__ import annotations

__all__ = ['VideoEntry', 'Capture', 'MergeDocument']  # noqa: RUF022

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from pldl2.model.epoch import Epoch, get_epoch
from pldl2.model.errors import UnavailableInfo
from pldl2.model.infodicts import PL_ID, V_ID, PL_InfoDict, V_InfoDict, YT_DLP_InfoDict
from pldl2.model.levels import (
    PL_InfoLevel,
    Rank,
    V_InfoLevel,
    coerce_v_level,
    derive_v_info_level,
    rank,
)
from pldl2.model.schema import SCHEMA_VERSION
from pldl2.model.timeline import PlaylistTimeline

_PLDL_PAYLOAD_KEYS = ('info_level', 'unavailable_msgs', 'playlist_epoch',
                      'yt_unavailable_msg', 'wa_unavailable_msg')
"""v1-compat: keys v1 wrote into a video payload. Lifted onto the envelope when wrapping.

The last two were v1's per-extractor copies of what `unavailable_msgs` already holds in
structured form; they are dropped rather than lifted."""

_PLDL_PLAYLIST_KEYS = ('info_level', 'merge_timeline')
"""v1-compat: keys v1 wrote into a playlist payload. Dropped when wrapping a flat extraction;
a raw flat has no level worth keeping and never had a timeline."""


@dataclass(frozen=True, slots=True, kw_only=True)
class VideoEntry:
    """One video: pldl's fields, plus the extractor's output untouched in `data`.

    Note: This is a snapshot/instantaneous data, aggregate kvals like `first_seen` and
    `last_seen` do not belong here.
    """

    id: V_ID
    info_level: V_InfoLevel
    data: YT_DLP_InfoDict | Mapping[str, Any] = field(default_factory=dict)
    unavailable_infos: tuple[UnavailableInfo, ...] = ()
    playlist_epoch: Epoch | None = None

    def __post_init__(self) -> None:
        # A read-only view, so `frozen` covers the payload and not just the reference to it.
        if not isinstance(self.data, MappingProxyType):
            object.__setattr__(self, 'data', MappingProxyType(dict(self.data)))
        if self.playlist_epoch is not None and not isinstance(self.playlist_epoch, Epoch):
            object.__setattr__(self, 'playlist_epoch', Epoch(self.playlist_epoch))

    @classmethod
    def wrap(cls, payload: V_InfoDict | Mapping[str, Any], *,
             info_level: V_InfoLevel | None = None) -> VideoEntry:
        """v1-compat: Build an envelope around a raw yt-dlp infodict.

        `info_level` is taken from the argument, else from a declared value, else derived from
        content.

        pldl keys already inline in the payload are lifted onto the envelope, so wrapping a v1
        file yields the same shape as wrapping a fresh extraction.
        """
        if info_level is None:
            declared = payload.get('info_level')
            info_level = (coerce_v_level(declared) if declared is not None
                          else derive_v_info_level(payload))

        playlist_epoch = payload.get('playlist_epoch')
        return cls(
            id=str(payload.get('id', '')),
            info_level=info_level,
            data={k: v for k, v in payload.items() if k not in _PLDL_PAYLOAD_KEYS},
            unavailable_infos=tuple(
                UnavailableInfo(
                    extractor=msg.get('type', ''),
                    msg=msg.get('msg'),
                    epoch=msg.get('epoch'),
                )
                for msg in payload.get('unavailable_msgs') or ()
            ),
            playlist_epoch=(Epoch(playlist_epoch)
                            if isinstance(playlist_epoch, int)
                            and not isinstance(playlist_epoch, bool) else None),
        )

    def unwrap(self) -> dict[str, Any]:
        """The payload as it was wrapped, which is what the extractor produced.

        Returns `data` alone; envelope fields are **not** re-injected.
        """
        return dict(self.data)

    @property
    def epoch(self) -> Epoch:
        return get_epoch(self.data)

    @property
    def rank(self) -> Rank:
        return rank(self.epoch, self.info_level)



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
class MergeDocument:
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
