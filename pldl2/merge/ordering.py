"""Reconcile disagreeing snapshot orders into one playlist order.

**Carry pldl/utils/merge_ordered_lists.py over nearly verbatim, with its tests** -- 425
lines, zero pldl imports, no I/O, already the best module in the repo. Only cleanup: the
private-attribute reach-ins at :263, :308, :381, and the `raise Warning` used as a control
signal at :104.

Note on graphlib.TopologicalSorter: worth reading, but **not** a drop-in. It raises
CycleError, whereas dropping the offending edge is this algorithm's entire point. Useful as
an oracle in tests on cycle-free inputs.
"""
