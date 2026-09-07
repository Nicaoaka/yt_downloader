"""
The InfoKind registry: one frozen dataclass per file type the store knows how to write.

In v1 the taxonomy had no single definition. `metadata_key` was `match`-ed in three separate
methods -- `write_info:789`, `get_filtered_data:726`, `reorder_keys:736` -- so adding a sixth
info type meant editing those three *plus* `_Infos`, `MetadataPointers`, `_MetadataFiles_Lit`
and `default_path_tmpls`. Six places, none of which knew about the others.

**This is a container of strategies, not an object with read/write methods.** Giving each kind
its own I/O would recreate five little persistence implementations, which is precisely what
this rewrite deletes. `store.write(kind, info)` performs the I/O once and dispatches through
the kind's fields; the differences between kinds -- including `raw_v_infos` being a batch
rather than a single dict -- are expressed as *data* via `payload`. The registry stays
declarative, testable with no filesystem, and still one row per new kind.

`owner` replaces v1's `pointer_key`. With the roster at a fixed path nothing is pointed at any
more, and what the store actually needs per kind is whether it **may assume the file is still
there**:

    PLDL  pldl depends on this. Fixed filename, `_` prefix, never discovered, never deleted.
    USER  pldl generates it and then lets go. Templated name, found by globbing, and it may
          be pruned, moved or corrupted between runs without the record noticing.
"""
from __future__ import annotations

__all__ = ['Owner', 'PayloadShape', 'InfoKind', 'KINDS', 'by_name', 'user_owned', 'pldl_owned']

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import Any

from pldl2.model.epoch import get_epoch, get_latest_epoch
from pldl2.model.metadata import ARCHIVE_FILENAME, METADATA_FILENAME, ROSTER_FILENAME


class Owner(StrEnum):
    PLDL = auto()
    """Authoritative. Fixed name, `_` prefixed, must exist, must not be hand-edited."""
    USER = auto()
    """Generated then released. May vanish between runs; every read must tolerate absence."""


class PayloadShape(StrEnum):
    SINGLE = auto()
    """One document: a flat extraction, a merge."""
    BATCH = auto()
    """Many entries in one file. v1's `_v_infos/*.json` was already a list of lists, and
    therefore already not valid yt-dlp infojson -- the envelope makes that explicit."""
    OPAQUE = auto()
    """Not JSON at all: the yt-dlp download archive is a text file of `key id` lines."""


def _batch_epoch(payload: Any) -> int:
    """The newest epoch across a batch, or 0."""
    entries = payload.get('videos') if hasattr(payload, 'get') else payload
    epochs = [get_epoch(e) for e in (entries or ())]
    return max(epochs) if epochs else 0


@dataclass(frozen=True, slots=True, kw_only=True)
class InfoKind:
    """Everything the store needs to know about one file type."""

    name: str
    owner: Owner
    payload: PayloadShape

    filename: str | None = None
    """Set for PLDL-owned files, whose names are fixed and never templated."""
    tmpl_key: str | None = None
    """Set for USER-owned files: the attribute on `Paths` holding this kind's template."""

    epoch_of: Callable[[Any], int] = get_epoch
    """How to read this kind's own epoch. The 4-arm dispatch v1 spelled out twice."""

    reorder: Callable[[Any], Any] | None = None
    filter_of: Callable[[Any], Any] | None = None
    """Supplied by store/ and config respectively. Carried here so a new kind stays one row;
    typed loosely on purpose, since L0 must not import either of them."""

    description: str = ''

    def __post_init__(self) -> None:
        if self.owner is Owner.PLDL and not self.filename:
            raise ValueError(f'{self.name}: a PLDL-owned kind needs a fixed filename')
        if self.owner is Owner.USER and not self.tmpl_key:
            raise ValueError(f'{self.name}: a USER-owned kind needs a tmpl_key')

    @property
    def may_be_missing(self) -> bool:
        """True when a read must tolerate absence and report an Issue instead of raising."""
        return self.owner is Owner.USER


KINDS: Mapping[str, InfoKind] = {
    kind.name: kind for kind in (
        InfoKind(
            name='roster', owner=Owner.PLDL, payload=PayloadShape.SINGLE,
            filename=ROSTER_FILENAME,
            description='Membership and order. The one authoritative document.',
        ),
        InfoKind(
            name='metadata', owner=Owner.PLDL, payload=PayloadShape.SINGLE,
            filename=METADATA_FILENAME,
            description='Identity, resolved paths, download history.',
        ),
        InfoKind(
            name='archive', owner=Owner.PLDL, payload=PayloadShape.OPAQUE,
            filename=ARCHIVE_FILENAME,
            description="yt-dlp's download archive. Moves to the library when one is set.",
        ),
        InfoKind(
            name='raw_flat', owner=Owner.USER, payload=PayloadShape.SINGLE,
            tmpl_key='raw_flat',
            description='One flat extraction: ids and order only.',
        ),
        InfoKind(
            name='raw_v_infos', owner=Owner.USER, payload=PayloadShape.BATCH,
            tmpl_key='raw_v_infos', epoch_of=_batch_epoch,
            description="This session's per-video infodicts.",
        ),
        InfoKind(
            name='merge_info', owner=Owner.USER, payload=PayloadShape.SINGLE,
            tmpl_key='merge_info', epoch_of=get_latest_epoch,
            description='Full history merge, carrying the merge timeline.',
        ),
    )
}


def by_name(name: str) -> InfoKind:
    """Look up a kind, raising a clear error rather than a bare KeyError."""
    try:
        return KINDS[name]
    except KeyError:
        raise KeyError(
            f'unknown info kind {name!r}; known: {", ".join(sorted(KINDS))}') from None


def user_owned() -> tuple[InfoKind, ...]:
    """Kinds the user may prune. Everything discovered by globbing."""
    return tuple(k for k in KINDS.values() if k.owner is Owner.USER)


def pldl_owned() -> tuple[InfoKind, ...]:
    """Kinds pldl depends on. Fixed names, must exist."""
    return tuple(k for k in KINDS.values() if k.owner is Owner.PLDL)
