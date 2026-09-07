"""MergeFieldUpdater and the updater tables: COMMON_UPDATER, FLAT_MERGE_UPDATER, PL_UPDATER.

Declared **once** here. Today the MergeFieldUpdater type is hand-copied four times inside
merge_infos.py (:27, :140, :215, :266) purely to avoid an import.

PL_UPDATER is new: playlist-level fields currently bypass the updater entirely and
pl_infos[0] wins, hardcoded (merge_infos.py:241). Default to today's newest-wins behaviour,
but make it visible and overridable.

The -1 epoch trick in __flat_merge_epoch_updater (30 lines of comment explaining a magic
decrement) becomes a named concept with a docstring and a test. Issue-1 #16 argues the
decrement splits one extraction across two timeline keys a second apart; with the epoch/at
split, ranking the roster fold below its source by *level* is the cleaner option.
"""
