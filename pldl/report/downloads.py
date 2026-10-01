"""Render DownloadInfo / PL_DownloadInfo.

Today display.py is inconsistent: download_info / pl_download_info return strings while
pl_merge_timeline / metadata_history / pl_v_ids print directly, and it imports domain logic
(yt_utils.interpret_error_msg, merge_infos._merge_v_sort_key) while playlist_dl.py:1155
reaches back into display.ACTION_TAG[...].color to build its own lines.
"""
