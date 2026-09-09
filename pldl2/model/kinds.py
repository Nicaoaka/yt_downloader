"""
One `InfoKind` per file type the store knows how to write.

**A container of strategies, not an object with read/write methods.** Giving each kind its own
I/O would recreate a small persistence implementation per file type. `store.write(kind, info)`
performs the I/O once and dispatches through the kind's fields; the differences between kinds,
including `raw_v_infos` being a batch rather than a single document, are expressed as *data*
via `payload`. The registry stays declarative, testable with no filesystem, and one row per
new kind.

Kinds are reached as **module constants** -- `kinds.ROSTER`, `kinds.RAW_FLAT` -- so a
misspelling is an AttributeError at import rather than a KeyError at runtime, and each carries
its own payload type. `KINDS` exists only for resolving a name read off disk.

`owner` is what the store needs to know before touching a file:

    PLDL  pldl depends on this. Fixed filename, `_` prefix, never discovered, never deleted.
    USER  pldl generates it and then lets go. Templated name, found by globbing, and it may
          be pruned, moved or corrupted between runs without the record noticing.
"""
from __future__ import annotations

__all__ = [  # noqa: RUF022
    'KindName', 'Owner', 'PayloadShape', 'InfoKind',
    'ROSTER', 'METADATA', 'ARCHIVE', 'RAW_FLAT', 'RAW_V_INFOS', 'MERGE_INFO',
    'KINDS', 'PATH_TEMPLATE_KEYS', 'by_name', 'user_owned', 'pldl_owned',
]

from collections.abc import Callable, Mapping
from dataclasses import dataclass, fields
from enum import StrEnum, auto
from typing import Any, Final

from pldl2.model.envelope import Capture
from pldl2.model.epoch import Epoch, get_epoch, get_latest_epoch
from pldl2.model.infodicts import PL_InfoDict
from pldl2.model.metadata import (
    ARCHIVE_FILENAME,
    METADATA_FILENAME,
    ROSTER_FILENAME,
    Metadata,
    Paths,
)
from pldl2.model.roster import Roster

PATH_TEMPLATE_KEYS: Final[frozenset[str]] = frozenset(
    f.name for f in fields(Paths) if f.name != 'playlist_dir')
"""Template fields on `Paths` a kind may point at. Derived from `Paths`, so it cannot drift."""


class KindName(StrEnum):
    ROSTER = auto()
    METADATA = auto()
    ARCHIVE = auto()
    RAW_FLAT = auto()
    RAW_V_INFOS = auto()
    MERGE_INFO = auto()


class Owner(StrEnum):
    PLDL = auto()
    """Authoritative. Fixed name, `_` prefixed, must exist, must not be hand-edited."""
    USER = auto()
    """Generated then released. May vanish between runs; every read must tolerate absence."""


class PayloadShape(StrEnum):
    SINGLE = auto()
    """One document: a flat extraction, a merge, the roster."""
    BATCH = auto()
    """Many entries in one file, so it is not valid yt-dlp infojson and never claims to be."""
    OPAQUE = auto()
    """Not JSON at all: the download archive is a text file of `key id` lines."""


def _batch_epoch(payload: Any) -> Epoch:
    """The newest epoch across a batch, or 0."""
    entries = payload.get('videos') if hasattr(payload, 'get') else payload
    epochs = [get_epoch(e) for e in (entries or ())]
    return Epoch(max(epochs)) if epochs else Epoch(0)


@dataclass(frozen=True, slots=True, kw_only=True)
class InfoKind[T]:
    """Everything the store needs to know about one file type.

    `T` is the payload this kind carries, so a call site holding `kinds.ROSTER` knows it is
    reading and writing a `Roster` rather than an untyped document.
    """

    name: KindName
    owner: Owner
    payload: PayloadShape

    filename: str | None = None
    """Set for PLDL-owned files, whose names are fixed and never templated."""
    tmpl_key: str | None = None
    """Set for USER-owned files: the field on `Paths` holding this kind's template."""

    epoch_of: Callable[[Any], int] = get_epoch
    """How to read this kind's own epoch."""

    reorder: Callable[[Any], Any] | None = None
    filter_of: Callable[[Any], Any] | None = None
    """Supplied by store/ and config respectively. Carried here so a new kind stays one row;
    typed loosely on purpose, since L0 must not import either of them."""

    description: str = ''

    def __post_init__(self) -> None:
        if self.owner is Owner.PLDL:
            if not self.filename:
                raise ValueError(f'{self.name}: a PLDL-owned kind needs a fixed filename')
            if not self.filename.startswith('_'):
                raise ValueError(f'{self.name}: a PLDL-owned filename must start with "_"')
        elif not self.tmpl_key:
            raise ValueError(f'{self.name}: a USER-owned kind needs a tmpl_key')

        if self.tmpl_key is not None and self.tmpl_key not in PATH_TEMPLATE_KEYS:
            raise ValueError(
                f'{self.name}: tmpl_key {self.tmpl_key!r} is not a template field on Paths; '
                f'known: {", ".join(sorted(PATH_TEMPLATE_KEYS))}')

    @property
    def may_be_missing(self) -> bool:
        """True when a read must tolerate absence and report an Issue instead of raising."""
        return self.owner is Owner.USER


ROSTER: Final[InfoKind[Roster]] = InfoKind(
    name=KindName.ROSTER, owner=Owner.PLDL, payload=PayloadShape.SINGLE,
    filename=ROSTER_FILENAME,
    description='Membership and order. The one authoritative document.',
)

METADATA: Final[InfoKind[Metadata]] = InfoKind(
    name=KindName.METADATA, owner=Owner.PLDL, payload=PayloadShape.SINGLE,
    filename=METADATA_FILENAME,
    description='Identity, resolved paths, download history.',
)

ARCHIVE: Final[InfoKind[list[str]]] = InfoKind(
    name=KindName.ARCHIVE, owner=Owner.PLDL, payload=PayloadShape.OPAQUE,
    filename=ARCHIVE_FILENAME,
    description="yt-dlp's download archive. Moves to the library when one is set.",
)

RAW_FLAT: Final[InfoKind[PL_InfoDict]] = InfoKind(
    name=KindName.RAW_FLAT, owner=Owner.USER, payload=PayloadShape.SINGLE,
    tmpl_key='raw_flat',
    description='One flat extraction: ids and order only.',
)

RAW_V_INFOS: Final[InfoKind[Capture]] = InfoKind(
    name=KindName.RAW_V_INFOS, owner=Owner.USER, payload=PayloadShape.BATCH,
    tmpl_key='raw_v_infos', epoch_of=_batch_epoch,
    description="A session's per-video infodicts.",
)

MERGE_INFO: Final[InfoKind[PL_InfoDict]] = InfoKind(
    name=KindName.MERGE_INFO, owner=Owner.USER, payload=PayloadShape.SINGLE,
    tmpl_key='merge_info', epoch_of=get_latest_epoch,
    description='Full history merge, carrying the merge timeline.',
)

KINDS: Final[Mapping[KindName, InfoKind[Any]]] = {
    kind.name: kind for kind in (ROSTER, METADATA, ARCHIVE, RAW_FLAT, RAW_V_INFOS, MERGE_INFO)
}
"""Name -> kind, for resolving a name read off disk. Prefer the module constants in code."""


def by_name(name: str) -> InfoKind[Any]:
    """Resolve a kind name read off disk, naming the alternatives when it fails."""
    try:
        return KINDS[KindName(name)]
    except ValueError:
        raise KeyError(f'unknown info kind {name!r}; '
                       f'known: {", ".join(k.value for k in KindName)}') from None


def user_owned() -> tuple[InfoKind[Any], ...]:
    """Kinds the user may prune. Everything discovered by globbing."""
    return tuple(k for k in KINDS.values() if k.owner is Owner.USER)


def pldl_owned() -> tuple[InfoKind[Any], ...]:
    """Kinds pldl depends on. Fixed names, must exist."""
    return tuple(k for k in KINDS.values() if k.owner is Owner.PLDL)
