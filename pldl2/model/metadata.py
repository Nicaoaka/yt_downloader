"""
_metadata.json, schema v2: identity, resolved paths, and the download log.

Three changes from v1, each removing a whole failure class rather than a single bug.

**`pointers` is deleted.** One pointer to a fixed path is not a pointer, it is a filename --
the roster always lives at `_roster.json`. Every other pointer aimed at a file the user is now
free to delete. Dropping the block removes `delete_prev`, the orphan-file class, the
pointer/commit ordering hazard, and the "metadata with no pointers at all" state that v1
reached whenever a PL_INFO_PATH ident produced a fresh pl_info (issue-1 #12, confirmed:
`_merge_flat` came up None, every method then raised, and close() still wrote the file).

**`history` is an ordered list with an int `epoch` and an ISO-8601 local `at`.** v1 keyed it by
a local-time string, which forced a full re-sort of the dict on every write, a string parse on
every read, and silently merged two rows an hour apart in the DST fall-back hour.

**`paths.playlist_dir` is authoritative.** Written once at creation and never recomputed from a
title. v1 re-derived the folder from the freshly extracted title on every run, so a playlist
renamed on YouTube resolved to a *different folder* and the run started a fresh, empty record
beside the real one -- history at zero rows, archive not found, roster fresh, and a second
_metadata.json with nothing linking it to the first (issue-1 #2, confirmed).
"""
from __future__ import annotations

__all__ = [
    'ROSTER_FILENAME', 'METADATA_FILENAME', 'ARCHIVE_FILENAME', 'PLAYLISTS_INDEX_FILENAME',
    'Paths', 'HistoryVideo', 'HistoryEntry', 'Metadata',
]

from collections.abc import Iterable
from dataclasses import dataclass, field, replace

from pldl2.model.epoch import to_iso
from pldl2.model.infodicts import DL_Action, DL_Result, PL_ID, V_ID
from pldl2.model.schema import SCHEMA_VERSION

# Fixed names, not templates. These are the pldl-owned files, and the `_` means
# "pldl depends on this; edit it and you break the record".
ROSTER_FILENAME = '_roster.json'
METADATA_FILENAME = '_metadata.json'
ARCHIVE_FILENAME = '_yt_dlp_archive.txt'
PLAYLISTS_INDEX_FILENAME = '_playlists.json'
"""At `home`: playlist id -> directory, so a record is findable even if you rename the folder."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Paths:
    """Where this playlist's files live, relative to `home`.

    Templates use `\\` and are relative to the playlist folder, so `home` can be moved freely.
    Only the user-owned outputs are templated: the pldl-owned files have fixed names above.
    """

    playlist_dir: str
    """**Authoritative.** Set once at creation; a title change is an event, not a relocation."""
    link_file: str = 'Videos\\%(title)s [%(id)s].%(ext)s'
    raw_flat: str = 'flat\\%(epoch)s.flat.json'
    raw_v_infos: str = 'v_infos\\%(epoch)s.v_infos.json'
    merge_info: str = 'merges\\%(epoch)s.merge.json'


@dataclass(frozen=True, slots=True, kw_only=True)
class HistoryVideo:
    """One video's outcome in one session."""

    id: V_ID
    title: str | None = None
    action: DL_Action | None = None
    result: DL_Result | None = None
    errors: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True, kw_only=True)
class HistoryEntry:
    """One session's download log."""

    epoch: int
    videos: tuple[HistoryVideo, ...] = ()

    @property
    def at(self) -> str:
        return to_iso(self.epoch)


@dataclass(frozen=True, slots=True, kw_only=True)
class Metadata:
    """Identity, resolved paths and the download log. Everything a pointer used to hold."""

    id: PL_ID
    paths: Paths
    title: str | None = None
    """Last known. A change is recorded as an event, never acted on as a relocation."""
    history: tuple[HistoryEntry, ...] = ()
    schema_version: int = SCHEMA_VERSION

    def with_history(self, entries: Iterable[HistoryEntry]) -> Metadata:
        """A copy whose history is `entries`, oldest first."""
        return replace(self, history=tuple(sorted(entries, key=lambda e: e.epoch)))

    def record(self, entry: HistoryEntry) -> Metadata:
        """Append one session's log, keeping the list ordered."""
        return self.with_history((*self.history, entry))

    def latest(self) -> HistoryEntry | None:
        return self.history[-1] if self.history else None

    def epochs_for(self, v_id: V_ID) -> tuple[int, ...]:
        """Every session epoch that touched this video, oldest first.

        The backoff rules in policy/ are built on this. v1 rescanned the whole history per
        video inside the match filter, which is O(videos x history) per run; policy/ indexes
        this once per session instead.
        """
        return tuple(e.epoch for e in self.history
                     if any(v.id == v_id for v in e.videos))
