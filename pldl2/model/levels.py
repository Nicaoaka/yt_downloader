"""V_InfoLevel, PL_InfoLevel, derive_v_info_level, derive_pl_info_level -- and **rank(level, epoch)**.

rank() is the fix for the old tree's clearest layering smell: _merge_v_sort_key is private to
merge_infos, yet display.py:206 and reorder_infodict_keys.py:230 both reach in through
function-local imports to dodge a cycle. Promoted here, all three import it normally and the
merge_infos <-> reorder_infodict_keys cycle disappears.

Ranking rule to preserve: sort by (info_level, epoch) with a large multiplier on the level,
so a richer old extraction always outranks a poorer new one. IntEnum makes that sortable
without a lookup table.
"""
