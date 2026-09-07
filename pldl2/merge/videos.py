"""merge_v_infos -- fold per-video infodicts.

Must be **deterministic**: iterate keys sorted. Today the fold walks
`v_info.keys() | merge_info.keys()` (merge_infos.py:57), whose order varies with the hash
seed, and reorder_merge_info never orders the inner `updates` dict -- so identical inputs
produce different bytes on different runs (issue-1 #21). "Same inputs => byte-identical
output" is a test.
"""
