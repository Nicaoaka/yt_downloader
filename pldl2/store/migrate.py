"""v1 -> v2 migration. **The only module that knows about v1**; the v1 reader is retained solely
for it.

    pldl2.migrate(playlist_dir, *, dry_run=True, backup=True)

Idempotent, dry-run by default (prints a diff via difflib.unified_diff), and copies the
_metadata.json / _merge_flat pair aside before touching anything.

Steps: metadata v1 -> v2 (pointers dropped, history to an ordered list, epochs to epoch+at);
_merge_flat -> _roster.json with in_playlist backfilled from the newest flat extraction;
infodicts wrapped in the envelope; _flat/ -> flat/, _v_infos/ -> v_infos/, loose merges ->
merges/.

Validated against a **copy** of data/Lists 8, and judged on the roster and the raw captures,
never on the merges -- the roster is the only thing that cannot be regenerated. relocate()
reuses this machinery: both are "rewrite the record's shape without changing its meaning".
"""
