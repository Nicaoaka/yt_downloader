"""Levels, derivation, and the ordering key.

`rank()` orders sources chronologically, with the level only separating two from the same
second.

Which value wins a field is not this module's business: that is per-field and belongs to the
merge's field updater, and which of those changes is written to the timeline belongs to its
update filter.
"""
import unittest

from pldl.downloader.levels import (
    V_InfoLevel,
    coerce_v_level,
    derive_v_info_level,
    rank,
)


class Ordering(unittest.TestCase):
    """rank() is a sort key: chronological, level only as a tiebreak."""

    def test_orders_chronologically(self):
        self.assertLess(rank(100, V_InfoLevel.FLAT), rank(200, V_InfoLevel.FLAT))

    def test_an_older_richer_source_ranks_lower(self):
        """The point of the change: history reads in the order it happened."""
        self.assertLess(
            rank(1_704_067_200, V_InfoLevel.DOWNLOAD),
            rank(1_788_000_000, V_InfoLevel.FLAT))

    def test_level_only_breaks_a_tie_within_one_second(self):
        self.assertLess(rank(100, V_InfoLevel.FLAT), rank(100, V_InfoLevel.DOWNLOAD))


class Coercion(unittest.TestCase):
    def test_is_total_over_its_input_type(self):
        cases = [
            (V_InfoLevel.EXTRACT, V_InfoLevel.EXTRACT),
            ('DOWNLOAD', V_InfoLevel.DOWNLOAD),
            (2, V_InfoLevel.EXTRACT),
            (None, V_InfoLevel.NONE),
            ('nonsense', V_InfoLevel.NONE),
            (99, V_InfoLevel.NONE),
            (-1, V_InfoLevel.NONE),
            ([], V_InfoLevel.NONE),
            (object(), V_InfoLevel.NONE),
        ]
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertIs(coerce_v_level(value), expected)


class Derivation(unittest.TestCase):
    def test_video_levels_from_content(self):
        cases = [
            ({}, V_InfoLevel.NONE),
            (None, V_InfoLevel.NONE),
            ({'id': 'a'}, V_InfoLevel.NONE),
            ({'id': 'a', 'channel': 'c'}, V_InfoLevel.FLAT),
            ({'id': 'a', 'extractor_key': 'YoutubeWebArchive'}, V_InfoLevel.FLAT),
            ({'id': 'a', 'channel': 'c', 'extractor': 'youtube'}, V_InfoLevel.EXTRACT),
            ({'id': 'a', 'extractor': 'youtube', 'requested_downloads': [{}]},
             V_InfoLevel.DOWNLOAD),
        ]
        for info, expected in cases:
            with self.subTest(info=info):
                self.assertIs(derive_v_info_level(info), expected)


if __name__ == '__main__':
    unittest.main()
