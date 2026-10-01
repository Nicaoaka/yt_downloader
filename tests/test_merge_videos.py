"""The per-video fold: hand-authored cases where the right answer is obvious by inspection.

These own correctness. Parity against `data/Lists 8` says only that the port is faithful; a
case here says the merge is *right*.
"""
import unittest
from itertools import permutations

from pldl.merge.updaters import MergeUpdaterMap, latest
from pldl.merge.videos import REMOVED, merge_v_infos
from pldl.downloader import UnavailableInfo, V_InfoLevel, VideoEntry
from pldl.model import Epoch

NONE, FLAT, EXTRACT, DOWNLOAD = V_InfoLevel


def V(epoch, level=FLAT, *, id='v', unavailable=(), playlist_epoch=None, **data) -> VideoEntry:
    """A source: `epoch` and `id` go into the payload the way yt-dlp puts them there."""
    return VideoEntry(id=id, info_level=level, data={'id': id, 'epoch': epoch, **data},
                      unavailable_infos=tuple(unavailable), playlist_epoch=playlist_epoch)


def updates_at(timeline, epoch) -> dict[str, str]:
    return {u.field: u.value for e in timeline.at_epoch(epoch) for u in e.updates}


class FlatThenFull(unittest.TestCase):
    FLAT_SRC = V(100, FLAT, title='T', channel='C', view_count=100)
    FULL_SRC = V(200, EXTRACT, title='T', channel='C', view_count=150,
                 description='D', extractor='youtube')

    def setUp(self):
        self.merged, self.timeline = merge_v_infos([self.FLAT_SRC, self.FULL_SRC])

    def test_values_are_the_union_with_the_newest_winning(self):
        self.assertEqual(self.merged.data, {
            'id': 'v', 'epoch': 200, 'title': 'T', 'channel': 'C', 'view_count': 150,
            'description': 'D', 'extractor': 'youtube',
        })
        self.assertEqual(self.merged.epoch, 200)

    def test_the_level_rises_and_the_rise_is_recorded_where_it_happened(self):
        self.assertIs(self.merged.info_level, EXTRACT)
        self.assertEqual(self.timeline.levels(), (FLAT, EXTRACT))
        first, second = self.timeline
        self.assertEqual((first.prev_info_level, first.info_level), (NONE, FLAT))
        self.assertEqual((second.prev_info_level, second.info_level), (FLAT, EXTRACT))
        self.assertEqual(second.render_better_info(), 'FLAT -> EXTRACT')

    def test_the_first_observation_of_a_field_is_an_update(self):
        self.assertEqual(updates_at(self.timeline, 100), {'title': 'T', 'channel': 'C'})

    def test_only_what_changed_and_is_worth_recording_is_recorded(self):
        """`title` did not move; `view_count` moved but is churn."""
        self.assertEqual(updates_at(self.timeline, 200),
                         {'description': 'D', 'extractor': 'youtube'})


class Changes(unittest.TestCase):
    def test_a_title_change_is_recorded_once_at_its_instant(self):
        merged, timeline = merge_v_infos([V(100, title='T1'), V(200, title='T1'), V(300, title='T2')])
        self.assertEqual(merged.data['title'], 'T2')
        self.assertEqual([e.epoch for e in timeline], [100, 300],
                         'the refresh that taught nothing left no trace')
        self.assertEqual(updates_at(timeline, 300), {'title': 'T2'})

    def test_a_dead_video_keeps_its_title_and_leaves_no_trace(self):
        """A flat extraction of a removed video says `title: None, channel: None`."""
        merged, timeline = merge_v_infos([
            V(100, EXTRACT, title='T', channel='C'),
            V(200, FLAT, title=None, channel=None),
        ])
        self.assertEqual((merged.data['title'], merged.data['channel']), ('T', 'C'))
        self.assertIs(merged.info_level, EXTRACT, 'a poorer source cannot lower the level')
        self.assertEqual([e.epoch for e in timeline], [100])

    def test_a_flat_reference_is_gone_once_the_video_is_resolved(self):
        merged, _ = merge_v_infos([
            V(100, FLAT, _type='url', ie_key='Youtube', title='T'),
            V(200, EXTRACT, title='T', extractor='youtube'),
            V(300, FLAT, _type='url', ie_key='Youtube', title='T'),
        ])
        self.assertNotIn('_type', merged.data)
        self.assertNotIn('ie_key', merged.data)

    def test_a_removal_renders_as_removed(self):
        merged, timeline = merge_v_infos(
            [V(100, title='T'), V(200)],
            merge_updater_map=MergeUpdaterMap({}, default=latest),
            tl_update_filter=lambda key: key == 'title')
        self.assertNotIn('title', merged.data)
        self.assertEqual(updates_at(timeline, 200), {'title': REMOVED})


class Unavailability(unittest.TestCase):
    YT = UnavailableInfo(extractor='youtube', msg='Private video', epoch=Epoch(290))
    WA = UnavailableInfo(extractor='web.archive:youtube', msg='not archived', epoch=Epoch(395))

    def test_reports_accumulate_dedupe_and_sit_at_their_own_epoch(self):
        merged, timeline = merge_v_infos([
            V(100, EXTRACT, title='T'),
            V(300, NONE, unavailable=(self.YT,)),           # capture written at 300, failure at 290
            V(400, NONE, unavailable=(self.YT, self.WA)),   # YT reported again: one fact, not two
        ])
        self.assertEqual(merged.unavailable_infos, (self.YT, self.WA))
        self.assertEqual([e.epoch for e in timeline], [100, 290, 395])
        self.assertEqual(timeline.at_epoch(290)[0].unavailable_infos, (self.YT,))
        self.assertEqual(merged.data['title'], 'T', 'a failed attempt says nothing about the data')
        self.assertIs(merged.info_level, EXTRACT)

    def test_a_report_without_its_own_epoch_takes_the_captures(self):
        undated = UnavailableInfo(extractor='youtube', msg='gone')
        _, timeline = merge_v_infos([V(500, NONE, unavailable=(undated,))])
        self.assertEqual([e.epoch for e in timeline], [500])


class Continuing(unittest.TestCase):
    FIRST = (V(100, FLAT, title='T', channel='C'),
             V(200, EXTRACT, title='T', channel='C', description='D'))

    def setUp(self):
        self.m1, self.t1 = merge_v_infos(self.FIRST)

    def test_old_entries_are_untouched_and_new_ones_appended(self):
        m2, t2 = merge_v_infos([V(300, FLAT, title='T2', channel='C')],
                               init_v_entry=self.m1, init_v_timeline=self.t1)
        self.assertEqual(t2.entries[:len(self.t1)], self.t1.entries, 'history is read-only')
        self.assertEqual([e.epoch for e in t2], [100, 200, 300])
        self.assertEqual(updates_at(t2, 300), {'title': 'T2'})
        self.assertEqual(m2.data['title'], 'T2')
        self.assertEqual(m2.data['description'], 'D', 'the flat did not say; the merge still knows')
        self.assertIs(m2.info_level, EXTRACT)
        self.assertIsNone(t2[-1].prev_info_level, 'the level did not move, so no rise is claimed')

    def test_folding_a_capture_already_folded_changes_nothing(self):
        m2, t2 = merge_v_infos([self.FIRST[1]], init_v_entry=self.m1, init_v_timeline=self.t1)
        self.assertEqual(m2, self.m1)
        self.assertEqual(t2, self.t1)

    def test_nothing_new_returns_the_previous_merge_as_it_was(self):
        m2, t2 = merge_v_infos([], init_v_entry=self.m1, init_v_timeline=self.t1)
        self.assertIs(m2, self.m1)
        self.assertIs(t2, self.t1)

    def test_a_previous_merge_is_seeded_at_its_own_rank(self):
        """An older capture folded in later cannot overwrite what a newer merge knows."""
        m2, _ = merge_v_infos([V(50, FLAT, title='ancient', channel='C')], init_v_entry=self.m1)
        self.assertEqual(m2.data['title'], 'T')


class Order(unittest.TestCase):
    SOURCES = (V(100, FLAT, title='A'), V(300, EXTRACT, title='C', description='D'),
               V(200, FLAT, title='B'))

    def test_final_values_do_not_depend_on_fold_order(self):
        results = [merge_v_infos(list(p), sort_key=None)[0] for p in permutations(self.SOURCES)]
        for merged in results[1:]:
            self.assertEqual(merged, results[0])
        self.assertEqual((results[0].data['title'], results[0].data['description']), ('C', 'D'))
        self.assertIs(results[0].info_level, EXTRACT)

    def test_the_default_order_is_chronological_so_the_timeline_is_complete(self):
        _, timeline = merge_v_infos(list(self.SOURCES))
        self.assertEqual([updates_at(timeline, e)['title'] for e in (100, 200, 300)], ['A', 'B', 'C'])

    def test_as_given_folds_as_given(self):
        _, timeline = merge_v_infos(list(self.SOURCES), sort_key=None)
        self.assertEqual({e.epoch for e in timeline}, {100, 300}, 'B was never current')


class Determinism(unittest.TestCase):
    def test_same_inputs_same_output_including_key_order(self):
        a = [V(100, title='T', channel='C', description='D')]
        b = [VideoEntry(id='v', info_level=FLAT,
                        data={'description': 'D', 'channel': 'C', 'title': 'T', 'epoch': 100, 'id': 'v'})]
        ma, ta = merge_v_infos(a)
        mb, tb = merge_v_infos(b)
        self.assertEqual(ma, mb)
        self.assertEqual(list(ma.data), list(mb.data), 'keys are iterated sorted')
        self.assertEqual(ta, tb)


class Errors(unittest.TestCase):
    def test_mixed_ids_are_refused(self):
        with self.assertRaises(ValueError):
            merge_v_infos([V(1, id='a'), V(2, id='b')])
        with self.assertRaises(ValueError):
            merge_v_infos([V(1, id='a')], init_v_entry=V(0, id='b'))


if __name__ == '__main__':
    unittest.main()
