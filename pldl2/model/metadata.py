"""
`_metadata.json`: identity, resolved paths, and the download log.

Identity is the playlist id. `paths.playlist_dir` is **authoritative** -- written once at
creation and never recomputed from a title -- so renaming a playlist on YouTube records an
event rather than resolving the record to a different folder.

`history` is an ordered list of `SessionLog`, one per run. A session spans many minutes, so it
carries both `started` and `ended`, and each `VideoLog` carries the epoch at which that video
was actually tried. Backoff arithmetic reads those rather than guessing from the session.

Deliberate edits are not logged here. `history` answers "what network work happened"; the
roster's manipulation log answers "what did I change", and keeping them apart avoids two
sources of truth for the same act.
"""
from __future__ import annotations

__all__ = [  # noqa: RUF022
    'ROSTER_FILENAME', 'METADATA_FILENAME', 'ARCHIVE_FILENAME', 'PLAYLISTS_INDEX_FILENAME',
    'Paths', 'VideoLog', 'SessionLog', 'Metadata',
]

from collections.abc import Iterable
from dataclasses import dataclass, fields, replace
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

    @classmethod
    def template_fields(cls) -> frozenset[str]:
        """Every field that holds a template, which is all of them but `playlist_dir`.

        `playlist_dir` names the folder the others resolve inside, so it is resolved once at
        creation and stored, while a template is resolved per file. store/layout.py validates
        these; nothing else needs to tell them apart.
        """
        return frozenset(f.name for f in fields(cls) if f.name != 'playlist_dir')


@dataclass(frozen=True, slots=True, kw_only=True)
class VideoLog:
    """What one session did to one video, and when."""

    id: V_ID
    epoch: Epoch
    """When this video was tried. A session runs for many minutes, so this is not the
    session's own epoch and backoff should not treat it as such."""
    title: str | None = None
    action: DL_Action | None = None
    result: DL_Result | None = None
    errors: tuple[str, ...] = ()
    """Always present, empty when nothing went wrong, so readers never need a default."""

    def __post_init__(self) -> None:
        if not isinstance(self.epoch, Epoch):
            object.__setattr__(self, 'epoch', Epoch(self.epoch))


@dataclass(frozen=True, slots=True, kw_only=True)
class SessionLog:
    """One run's download log."""

    started: Epoch
    ended: Epoch | None = None
    """`None` while the session is still open, or if it died before closing cleanly."""
    videos: tuple[VideoLog, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.started, Epoch):
            object.__setattr__(self, 'started', Epoch(self.started))
        if self.ended is not None and not isinstance(self.ended, Epoch):
            object.__setattr__(self, 'ended', Epoch(self.ended))

    @property
    def duration(self) -> int | None:
        """Seconds the session ran, or None if it never closed."""
        return None if self.ended is None else int(self.ended) - int(self.started)

    def get(self, v_id: V_ID) -> VideoLog | None:
        for video in self.videos:
            if video.id == v_id:
                return video
        return None


@dataclass(frozen=True, slots=True, kw_only=True)
class Metadata:
    """Identity, resolved paths and the download log."""

    id: PL_ID
    paths: Paths
    title: str | None = None
    """Last known. A change is recorded as an event, never acted on as a relocation."""
    history: tuple[SessionLog, ...] = ()
    schema_version: int = SCHEMA_VERSION

    def with_history(self, sessions: Iterable[SessionLog]) -> Metadata:
        """A copy whose history is `sessions`, oldest first."""
        return replace(self, history=tuple(sorted(sessions, key=lambda s: s.started)))

    def record(self, session: SessionLog) -> Metadata:
        """Append one session's log, keeping the list ordered."""
        return self.with_history((*self.history, session))

    def latest(self) -> SessionLog | None:
        return self.history[-1] if self.history else None

    def epochs_for(self, v_id: V_ID) -> tuple[Epoch, ...]:
        """Every epoch at which this video was tried, oldest first.

        The backoff rules in policy/ are built on this; policy/ indexes it once per session
        rather than rescanning per video.
        """
        return tuple(sorted(video.epoch
                            for session in self.history
                            for video in session.videos
                            if video.id == v_id))
