"""Roster / RosterEntry -- membership and order. **The one authoritative document.**

Replaces _merge_flat, renamed because that name is one word from merge_info and describes
two unrelated things. It also stopped being "a merged flat infodict": it is pldl's own
structure, with fields no flat extraction has.

Invariants that belong here:
  - a video that disappears from YouTube flips in_playlist to False and keeps its row forever
  - a video removed through the API loses its row (decision 9); the removal is a timeline event
  - in_playlist is set by exactly one operation -- folding a flat extraction in -- and is
    never derived anywhere else

Lives on disk at <playlist_dir>/_roster.json, always. No epoch in the name, no pointer.
"""
