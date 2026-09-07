"""Rules as an ordered list, so **precedence is list order** -- explicit and reorderable --
instead of a hardcoded chain.

    class Rule(Protocol):
        def __call__(self, video: V_InfoDict, ctx: DecisionContext) -> Decision | None: ...

    DownloadPolicy(limits=Limits(...),
                   rules=[Http403Backoff(...), FailBackoff(...), Overrides({...}), Match(...)])

Replaces wrapper_match_filter_builder: a 217-line module-level factory with 12 parameters, 6
nested helpers and a nonlocal flag that makes the filter non-reentrant. Its own comments say
"(might fit better in config.py, not sure)" and "TODO: This should be a function/property of
PlaylistDL".

DL_Action declaration order is currently load-bearing for override tie-breaks, documented
only in a comment -- that becomes an explicit `priority` field. Keep a match_filter(...)
shorthand for today's ergonomics.
"""
