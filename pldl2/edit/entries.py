"""remove / insert / replace / move over roster entries, as pure functions:

    def remove(entries, v_id)           -> EditResult
    def insert(entries, v_id, position) -> EditResult
    def replace(entries, v_id, repl)    -> EditResult
    def move(entries, v_id, position)   -> EditResult
    # EditResult = (new_entries, timeline_events, warnings)

Extracted whole from playlist_dl.py:1427-1718 (~290 lines that need nothing from downloads,
metadata or the network). PlaylistRecord applies an EditResult and records its events, which
also removes the third independent writer of merge_timeline.

Three confirmed defects become five-line unit tests here:
  #9  remove_videos gates on `if merge_i := index(...)`, so index 0 is falsy and the first
      video is never removed
  #10 insert_videos re-resolves position per id, so -1 raises on the second id and -2
      silently misorders. Resolve the anchor **once**, against the original list.
  #11 _add_update_to_merge_timeline writes "update" (str) but dedups on "updates" (dict), so
      the guard never fires and same-second edits overwrite each other
"""
