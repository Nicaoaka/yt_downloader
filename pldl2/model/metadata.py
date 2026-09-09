"""
`_metadata.json`: identity, resolved paths, and the download log.

Identity is the playlist id. `paths.playlist_dir` is **authoritative** -- written once at
creation and never recomputed from a title -- so renaming a playlist on YouTube records an
event rather than resolving the record to a different folder. `title` is kept only as the last
known value.

`history` is an ordered list. Each entry is one session, carrying an int `epoch` and the
videos it touched; each video may carry its own epoch, since a session can span many minutes
and backoff arithmetic should be about when a video was actually tried.
"""
from __future__ import annotations

__all__ = [  # noqa: RUF022
    'ROSTER_FILENAME', 'METADATA_FILENAME', 'ARCHIVE_FILENAME', 'PLAYLISTS_INDEX_FILENAME',
    'Paths', 'HistoryVideo', 'HistoryEntry', 'Metadata',
]

from collections.abc import Iterable
from dataclasses import dataclass, replace
from typing import Final

from pldl2.model.epoch import Epoch
from pldl2.model.infodicts import PL_ID, V_ID, DL_Action, DL_Result
from pldl2.model.schema import SCHEMA_VERSION

# Fixed names, not templates. These are the pldl-owned files, and the `_` means
# "pldl depends on this; edit it and you break the record".
ROSTER_FILENAME: Final = '_roster.json'
METADATA_FILENAME: Final = '_metadata.json'
ARCHIVE_FILENAME: Final = '_yt_dlp_archive.txt'
PLAYLISTS_INDEX_FILENAME: Final = '_playlists.json'
"""At `home`: playlist id -> directory, so a record is findable even if you rename the folder."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Paths:
    """Where this playlist's files live, relative to `home`.

    Templates use `\\` and are relative to the playlist folder, so `home` can be moved freely.
    Only the user-owned outputs are templated; the pldl-owned files have fixed names above.

    Templates are resolved by yt-dlp, so anything yt-dlp accepts works here, including
    arithmetic and format specs like `%(playlist_index + 1)d`.
    """

    playlist_dir: str
    """**Authoritative.** Set once at creation; a title change is an event, not a relocation."""
    link_file: str = 'Videos\\%(playlist_index + 1)d. %(title)s [%(id)s].%(ext)s'
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
    epoch: Epoch | None = None
    """When this video was tried. `None` means "the session's epoch".

    A session runs for many minutes, so a per-video epoch keeps a backoff from being off by
    the length of the session. Optional because it costs nothing to omit for a fast run.
    """

    def __post_init__(self) -> None:
        if self.epoch is not None and not isinstance(self.epoch, Epoch):
            object.__setattr__(self, 'epoch', Epoch(self.epoch))


@dataclass(frozen=True, slots=True, kw_only=True)
class HistoryEntry:
    """One session's download log."""

    epoch: Epoch
    videos: tuple[HistoryVideo, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.epoch, Epoch):
            object.__setattr__(self, 'epoch', Epoch(self.epoch))

    def epoch_of(self, video: HistoryVideo) -> Epoch:
        """A video's own epoch, falling back to the session's."""
        return video.epoch if video.epoch is not None else self.epoch


@dataclass(frozen=True, slots=True, kw_only=True)
class Metadata:
    """Identity, resolved paths and the download log."""

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

    def epochs_for(self, v_id: V_ID) -> tuple[Epoch, ...]:
        """Every epoch at which this video was touched, oldest first.

        Uses each video's own epoch where it has one. The backoff rules in policy/ are built
        on this; policy/ indexes it once per session rather than rescanning per video.
        """
        found = [entry.epoch_of(video)
                 for entry in self.history
                 for video in entry.videos
                 if video.id == v_id]
        return tuple(sorted(found))
