"""Per-playlist Videos/ folders, linked to the pool, plus relink().

A global pool you cannot browse per-playlist is a regression, so this is on by default and
each playlist keeps a real, browsable folder that opens in any external player.

Strategy, falling back automatically and recording which was used:
  1. hardlink -- the default. No elevation on Windows, zero extra disk, every player treats
     it as an ordinary file. Same volume only.
  2. symlink  -- for a library on another volume. Needs Developer Mode or elevation.
  3. copy     -- last resort, explicit, warned about, since it defeats the point.

link_file is fully configurable per playlist and resolves against the video's infodict **plus
roster context**, so %(playlist_index)03d gives ordered browsing -- the feature
post_processing/_number_videos.py was written for and never delivered (both its functions
raise NotImplementedError on their first executable line).

relink() recomputes every link name from the current roster and recreates them. Nothing is
copied, nothing is downloaded, the pool never moves. That is also why changing link_file is
not a relocation at all.
"""
