"""pldl keeps a durable, historical record of a YouTube playlist.

It is organized as stages, in the order data flows through them:

    model/       generic building blocks: Epoch, the schema version
    downloader/  what yt-dlp hands back, wrapped: VideoEntry, Capture, levels, errors
    roster/      the authoritative record: membership, order, context, timeline
    merge/       folds many captures into one merged playlist and updates the roster

**A stage imports only from stages before it.** A type lives with the stage that produces it,
and is imported from that stage: `from pldl.downloader import VideoEntry`. Inside a stage,
modules import each other by submodule path.

No module in model/, downloader/, roster/ or merge/ imports yt_dlp.

Nothing is re-exported here yet.
"""
