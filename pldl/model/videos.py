"""
One video, as an envelope around the extractor's payload.

pldl's own fields sit on the envelope; `data` is exactly what the extractor returned.
This gives easier comparison and future-proofing for unstable or added yt-dlp infodict kvals.
Unwrapping to raw data is trivial. The playlist-shaped envelopes -- a `Capture` and a
`MergePlaylist` -- are in playlists.py and hold these.

`data` is typed `YT_DLP_InfoDict` rather than `V_InfoDict` on purpose: `V_InfoDict` is the
payload *plus* pldl's addon keys, so using it would re-admit `info_level` and other custom keys
as legitimate payload keys, which is the purpose of the envelope design pattern. `wrap()` accepts
the wider type (v1-compat V_InfoDict) and produces the narrower.

In the future the envelope fields can be the columns of a SQLite DB with `data` as blobs.
"""
from __future__ import annotations

__all__ = ['VideoEntry']

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from pldl.model.epoch import Epoch, get_epoch
from pldl.model.errors import UnavailableInfo
from pldl.model.infodicts import V_ID, V_InfoDict, YT_DLP_InfoDict
from pldl.model.levels import (
    Rank,
    V_InfoLevel,
    coerce_v_level,
    derive_v_info_level,
    rank,
)

_PLDL_PAYLOAD_KEYS = ('info_level', 'unavailable_msgs', 'playlist_epoch',
                      'yt_unavailable_msg', 'wa_unavailable_msg')
"""v1-compat: keys v1 wrote into a video payload. Lifted onto the envelope when wrapping.

The last two were v1's per-extractor copies of what `unavailable_msgs` already holds in
structured form; they are dropped rather than lifted."""


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
