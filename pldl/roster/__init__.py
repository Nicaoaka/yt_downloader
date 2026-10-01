"""The roster: the one authoritative record of a playlist.

    roster.py    Roster / RosterEntry: membership, order, `in_playlist`, context
    timeline.py  what merging learned about each video, and when

The timeline lives here rather than in merge/ because the roster is what keeps it: merges are
regenerable, history is not. merge/ produces timeline entries and hands them back.
"""
from __future__ import annotations

from pldl.roster.roster import (
    PLAYLIST_CONTEXT_SOURCES,
    VIDEO_CONTEXT_SOURCES,
    PlaylistContext,
    Roster,
    RosterEntry,
    VideoContext,
)
from pldl.roster.timeline import FieldUpdate, MergeTimelineEntry, PlaylistTimeline, VideoTimeline

__all__ = [  # noqa: RUF022
    'Roster', 'RosterEntry', 'VideoContext', 'PlaylistContext',
    'VIDEO_CONTEXT_SOURCES', 'PLAYLIST_CONTEXT_SOURCES',
    'FieldUpdate', 'MergeTimelineEntry', 'VideoTimeline', 'PlaylistTimeline',
]
