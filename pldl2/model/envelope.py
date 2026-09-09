"""
Envelope pattern around a payload.

pldl's own fields sit on the envelope; `data` stays exactly what the extractor returned. That
separation is what lets a stored entry be handed back to yt-dlp or diffed against a fresh
extraction, and it means a field yt-dlp adds in a future release can never collide with one of
ours. Unwrapping is a pure projection.

`data` is typed `YT_DLP_InfoDict` rather than `V_InfoDict` on purpose: `V_InfoDict` is the
payload *plus* pldl's addon keys, so using it would re-admit `info_level` and friends as
legitimate payload keys, which is the exact conflation the envelope removes. `wrap()` accepts
the wider type (v1-compat: that is the shape a stored v1 file has) and produces the narrower.

In the future the envelope fields can be the columns of a SQLite DB with `data` as blobs.
"""
from __future__ import annotations

__all__ = ['VideoEntry', 'Capture']  # noqa: RUF022

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from pldl2.model.epoch import Epoch, get_epoch
from pldl2.model.infodicts import V_ID, UnavailableMsg, V_InfoDict, YT_DLP_InfoDict
from pldl2.model.levels import V_InfoLevel, coerce_v_level, derive_v_info_level
from pldl2.model.schema import SCHEMA_VERSION

_PLDL_PAYLOAD_KEYS = ('info_level', 'unavailable_msgs', 'playlist_epoch')
"""v1-compat: keys v1 wrote into the payload. Lifted onto the envelope when wrapping."""


@dataclass(frozen=True, slots=True, kw_only=True)
class VideoEntry:
    """One video: pldl's fields, plus the extractor's output untouched in `data`."""

    id: V_ID
    info_level: V_InfoLevel
    data: YT_DLP_InfoDict | Mapping[str, Any] = field(default_factory=dict)
    unavailable_msgs: tuple[UnavailableMsg, ...] = ()
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
        """Build an envelope around a raw yt-dlp infodict.

        `info_level` is taken from the argument, else from a declared value, else derived from
        content.

        v1-compat: pldl keys already inline in the payload are lifted onto the envelope and
        stripped from `data`, so wrapping a v1 file yields the same shape as wrapping a fresh
        extraction.
        """
        declared = payload.get('info_level')
        if info_level is None:
            info_level = (coerce_v_level(declared) if declared is not None
                          else derive_v_info_level(payload))

        playlist_epoch = payload.get('playlist_epoch')
        return cls(
            id=str(payload.get('id', '')),
            info_level=info_level,
            data={k: v for k, v in payload.items() if k not in _PLDL_PAYLOAD_KEYS},
            unavailable_msgs=tuple(payload.get('unavailable_msgs') or ()),
            playlist_epoch=(Epoch(playlist_epoch)
                            if isinstance(playlist_epoch, int)
                            and not isinstance(playlist_epoch, bool) else None),
        )

    def unwrap(self) -> dict[str, Any]:
        """The payload as it was wrapped, which is what the extractor produced.

        Returns `data` alone; it does **not** re-inject the envelope fields.
        """
        return dict(self.data)

    @property
    def epoch(self) -> Epoch:
        return get_epoch(self.data)


@dataclass(frozen=True, slots=True, kw_only=True)
class Capture:
    """One stored file's worth of entries, and the epoch it was taken at.

    A batch, so it is not valid yt-dlp infojson and does not claim to be. Individual entries
    unwrap back to payloads that are.
    """

    epoch: Epoch
    videos: tuple[VideoEntry, ...] = ()
    schema_version: int = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.epoch, Epoch):
            object.__setattr__(self, 'epoch', Epoch(self.epoch))

    def __len__(self) -> int:
        return len(self.videos)

    def get(self, v_id: V_ID) -> VideoEntry | None:
        for entry in self.videos:
            if entry.id == v_id:
                return entry
        return None

    def ids(self) -> tuple[V_ID, ...]:
        return tuple(entry.id for entry in self.videos)
