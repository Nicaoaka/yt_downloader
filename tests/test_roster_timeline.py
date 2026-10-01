"""The timeline: chronological, deduplicated, and never rewritten."""
import unittest

from pldl.downloader import V_InfoLevel
from pldl.model import Epoch
from pldl.roster import FieldUpdate, MergeTimelineEntry, VideoTimeline


class Timeline(unittest.TestCase):
    def test_entries_at_the_same_epoch_all_survive(self):
        """Two distinct things can happen in one second; neither replaces the other."""
        timeline = (VideoTimeline()
                    .add(MergeTimelineEntry(epoch=Epoch(100),
                                            updates=(FieldUpdate(field='title', value='T'),)))
                    .add(MergeTimelineEntry(epoch=Epoch(100),
                                            updates=(FieldUpdate(field='duration', value='9'),))))
        self.assertEqual(len(timeline), 2)
        self.assertEqual(len(timeline.at_epoch(100)), 2)

    def test_identical_entries_collapse(self):
        entry = MergeTimelineEntry(epoch=Epoch(100),
                                   updates=(FieldUpdate(field='title', value='T'),))
        self.assertEqual(len(VideoTimeline().add(entry).add(entry)), 1)

    def test_order_is_chronological_with_level_as_tiebreak(self):
        timeline = VideoTimeline((
            MergeTimelineEntry(epoch=Epoch(300), info_level=V_InfoLevel.FLAT,
                               updates=(FieldUpdate(field='c', value='3'),)),
            MergeTimelineEntry(epoch=Epoch(100), info_level=V_InfoLevel.DOWNLOAD,
                               updates=(FieldUpdate(field='a', value='1'),)),
            MergeTimelineEntry(epoch=Epoch(100), info_level=V_InfoLevel.FLAT,
                               updates=(FieldUpdate(field='b', value='2'),)),
        ))
        self.assertEqual([int(e.epoch) for e in timeline], [100, 100, 300])
        self.assertEqual([e.info_level for e in timeline][:2],
                         [V_InfoLevel.FLAT, V_InfoLevel.DOWNLOAD],
                         'within one epoch, lower level first')

    def test_a_newer_poorer_entry_does_not_jump_ahead_of_an_older_richer_one(self):
        """Ordering by merge priority would put the 2026 flat before the 2024 download, and
        the recorded progression would read backwards."""
        timeline = VideoTimeline((
            MergeTimelineEntry(epoch=Epoch(1_788_000_000), info_level=V_InfoLevel.FLAT,
                               updates=(FieldUpdate(field='x', value='1'),)),
            MergeTimelineEntry(epoch=Epoch(1_704_067_200), info_level=V_InfoLevel.DOWNLOAD,
                               updates=(FieldUpdate(field='y', value='2'),)),
        ))
        self.assertEqual([int(e.epoch) for e in timeline], [1_704_067_200, 1_788_000_000])

    def test_levels_reads_out_the_recorded_progression(self):
        timeline = VideoTimeline((
            MergeTimelineEntry(epoch=Epoch(100), info_level=V_InfoLevel.FLAT,
                               updates=(FieldUpdate(field='a', value='1'),)),
            MergeTimelineEntry(epoch=Epoch(200), info_level=V_InfoLevel.DOWNLOAD,
                               updates=(FieldUpdate(field='b', value='2'),)),
            MergeTimelineEntry(epoch=Epoch(300),
                               updates=(FieldUpdate(field='c', value='3'),)),
        ))
        self.assertEqual(timeline.levels(), (V_InfoLevel.FLAT, V_InfoLevel.DOWNLOAD))


if __name__ == '__main__':
    unittest.main()
