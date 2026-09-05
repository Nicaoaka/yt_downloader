import os
import tempfile
import unittest
from pathlib import Path

from pldl.playlist_dl import PlaylistDL, _InfosEntry


class _TestConfig:
    def __init__(self, home: str):
        self.home = home

    def filter_all_info(self, _info):
        pass

    def filter_flat_info(self, _info):
        pass


class WriteInfoTests(unittest.TestCase):
    def test_delete_prev_removes_file_replaced_by_new_pointer(self):
        with tempfile.TemporaryDirectory() as home:
            previous_path = Path(home, "previous.json")
            previous_path.write_text("{}", encoding="utf-8")
            current_path = Path(home, "current.json")

            downloader = PlaylistDL.__new__(PlaylistDL)
            downloader._config = _TestConfig(home)
            downloader._metadata = {
                "pointers": {"latest_flat_info": ("previous.json", 1)}
            }
            info = _InfosEntry(
                data={"id": "playlist", "epoch": 2, "entries": []},
                pl_outtmpl=str(current_path),
                is_written=False,
                metadata_key="latest_flat_info",
            )

            downloader.write_info(
                info, collision_policy="mov new", delete_prev=True
            )

            self.assertFalse(previous_path.exists())
            self.assertTrue(current_path.exists())
            self.assertEqual(
                downloader._metadata["pointers"]["latest_flat_info"],
                (os.path.relpath(current_path, home), 2),
            )

    def test_delete_prev_preserves_new_file_when_paths_alias_same_file(self):
        with tempfile.TemporaryDirectory() as home:
            alias_dir = Path(home, "alias")
            alias_dir.mkdir()
            current_path = Path(home, "current.json")
            current_path.write_text("{}", encoding="utf-8")

            downloader = PlaylistDL.__new__(PlaylistDL)
            downloader._config = _TestConfig(home)
            downloader._metadata = {
                "pointers": {
                    "latest_flat_info": (os.path.join("alias", "..", "current.json"), 1)
                }
            }
            info = _InfosEntry(
                data={"id": "playlist", "epoch": 2, "entries": []},
                pl_outtmpl=str(current_path),
                is_written=False,
                metadata_key="latest_flat_info",
            )

            downloader.write_info(
                info, collision_policy="rm old", delete_prev=True
            )

            self.assertTrue(current_path.exists())
            self.assertEqual(
                downloader._metadata["pointers"]["latest_flat_info"],
                (os.path.relpath(current_path, home), 2),
            )


if __name__ == "__main__":
    unittest.main()
