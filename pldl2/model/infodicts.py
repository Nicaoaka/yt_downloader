"""The yt-dlp payload shape, as TypedDicts, plus DownloadInfo / UnavailableMsg and sentinels.

TypedDict is right here and a dataclass is not: this is foreign data with ~200 optional keys
whose shape changes between yt-dlp releases. It types the keys we care about, costs nothing
at runtime, copies and validates nothing, and a key yt-dlp adds tomorrow simply flows
through -- which is what keeps `data` byte-faithful. Use typing.NotRequired per key rather
than total=False, and typing.ReadOnly for keys nothing should reassign.

Lift near-verbatim from pldl/pldl_types.py, already the cleanest module in the old tree.
"""
