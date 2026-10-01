"""The playlist fold: the roster decides who and in what order, captures supply values."""
import unittest

from pldl2.merge.playlists import merge_pl_infos, update_roster
from pldl2.model import (
    Capture,
    Epoch,
    MergePlaylist,
    PL_InfoLevel,
    Roster,
    V_InfoLevel,
    VideoEntry,
)

NONE, FLAT, EXTRACT, DOWNLOAD = V_InfoLevel


def flat(epoch, ids, **playlist) -> Capture:
    """A flat extraction as yt-dlp returns it: the playlist's own fields plus every entry."""
    return Capture.wrap_flat({
        'id': 'PL_x', '_type': 'playlist', 'title': 'PL', 'epoch': epoch, **playlist,
        'entries': [{'id': i, '_type': 'url', 'title': f'T-{i}', 'channel': 'C', 'epoch': epoch}
                    for i in ids],
    })


def batch(epoch, ids, level=EXTRACT, **data) -> Capture:
    """A per-video batch: whatever this session extracted, and no playlist payload."""
    return Capture(epoch=epoch, videos=tuple(
        VideoEntry(id=i, info_level=level,
                   data={'id': i, 'epoch': epoch, 'title': f'FULL-{i}', 'channel': 'C',
                         'extractor': 'youtube', **data})
        for i in ids))


class UpdateRoster(unittest.TestCase):
    def test_a_first_extraction_populates_membership_order_and_context(self):
        roster = update_roster(Roster(id='PL_x'), [flat(1000, ['a', 'b', 'c'])])
        self.assertEqual(roster.ids(), ('a', 'b', 'c'))
        self.assertEqual(roster.ids(in_playlist=True), ('a', 'b', 'c'))
        self.assertEqual(roster.last_updated, 1000)
        self.assertEqual(roster.get('a').context['title'], 'T-a')
        self.assertEqual(roster.context['title'], 'PL')

    def test_a_reorder_upstream_wins_and_a_removed_video_keeps_its_place(self):
        roster = update_roster(Roster(id='PL_x'), [flat(1000, ['a', 'b', 'c'])])
        roster = update_roster(roster, [flat(2000, ['c', 'a'])])
        self.assertEqual(roster.ids(in_playlist=True), ('c', 'a'))
        self.assertIn('b', roster.ids(), 'a video gone from YouTube keeps its row')
        self.assertEqual(roster.ids()[:2], ('c', 'a'), 'the newest snapshot decides order')

    def test_a_per_video_batch_never_decides_membership(self):
        """The bug this guard exists for: a batch holds what this session extracted, so
        treating it as a listing would flip every video it does not mention to gone."""
        roster = update_roster(Roster(id='PL_x'), [flat(1000, ['a', 'b', 'c'])])
        after = update_roster(roster, [batch(2000, ['a'])])
        self.assertEqual(after.ids(in_playlist=True), ('a', 'b', 'c'))
        self.assertEqual(after.last_updated, 1000, 'only a flat extraction moves last_updated')

    def test_context_comes_from_every_capture_and_the_newest_wins(self):
        roster = update_roster(Roster(id='PL_x'), [flat(1000, ['a'])])
        self.assertEqual(roster.get('a').context['title'], 'T-a')
        roster = update_roster(roster, [batch(2000, ['a'])])
        self.assertEqual(roster.get('a').context['title'], 'FULL-a',
                         'a full extraction is a fresher fact about the title')

    def test_context_within_one_call_does_not_depend_on_capture_order(self):
        forwards = update_roster(Roster(id='PL_x'), [flat(1000, ['a']), batch(2000, ['a'])])
        backwards = update_roster(Roster(id='PL_x'), [batch(2000, ['a']), flat(1000, ['a'])])
        self.assertEqual(forwards.get('a').context, backwards.get('a').context)
        self.assertEqual(forwards.get('a').context['title'], 'FULL-a')

    def test_a_later_call_replaces_context_even_with_older_captures(self):
        """Known and documented: the roster stores a context value without the rank of the
        source that supplied it, so resolution cannot reach back across calls. Pass a
        session's captures together. Nothing may depend on context for correctness."""
        roster = update_roster(Roster(id='PL_x'), [flat(2000, ['a'])])
        stale = update_roster(roster, [batch(1000, ['a'])])
        self.assertEqual(stale.get('a').context['title'], 'FULL-a')

    def test_context_is_only_the_declared_fields(self):
        roster = update_roster(
            update_roster(Roster(id='PL_x'), [flat(1000, ['a'])]),
            [batch(2000, ['a'], description='D', formats=[1, 2, 3])])
        self.assertNotIn('formats', roster.get('a').context)
        self.assertNotIn('description', roster.get('a').context,
                         'the roster is not a second copy of the merge')

    def test_a_video_the_roster_does_not_know_contributes_no_context(self):
        roster = update_roster(Roster(id='PL_x'), [flat(1000, ['a'])])
        after = update_roster(roster, [batch(2000, ['zzz'])])
        self.assertEqual(after.ids(), ('a',))

    def test_no_captures_is_a_no_op(self):
        roster = update_roster(Roster(id='PL_x'), [flat(1000, ['a', 'b'])])
        self.assertEqual(update_roster(roster, []), roster)


class MergePlInfos(unittest.TestCase):
    def setUp(self):
        self.roster = update_roster(Roster(id='PL_x'), [flat(1000, ['a', 'b', 'c'])])

    def test_membership_and_order_come_from_the_roster(self):
        report = merge_pl_infos(self.roster, [batch(2000, ['c', 'a'])])
        self.assertEqual(report.merged.ids(), ('a', 'b', 'c'), "the roster's order, not the capture's")
        self.assertEqual(report.merged.id, 'PL_x')

    def test_an_id_the_roster_does_not_know_is_reported_not_raised(self):
        """A removal followed by a merge looks exactly like this, so it is ordinary."""
        report = merge_pl_infos(self.roster, [batch(2000, ['a', 'zzz'])])
        self.assertEqual(report.omitted, {'zzz': 1})
        self.assertNotIn('zzz', report.merged.ids())

    def test_a_video_with_no_sources_keeps_its_row(self):
        report = merge_pl_infos(self.roster, [batch(2000, ['a'])])
        b = report.merged.get('b')
        self.assertIs(b.info_level, NONE)
        self.assertEqual(dict(b.data), {'id': 'b'}, 'nothing is fabricated for it')

    def test_values_are_folded_per_video(self):
        report = merge_pl_infos(self.roster, [flat(1000, ['a', 'b', 'c']), batch(2000, ['a'])])
        a = report.merged.get('a')
        self.assertIs(a.info_level, EXTRACT)
        self.assertEqual(a.data['title'], 'FULL-a')
        self.assertEqual(a.data['channel'], 'C')
        self.assertNotIn('_type', a.data, 'the flat reference is superseded by a real extraction')

    def test_the_timeline_is_seeded_from_the_roster_not_the_previous_merge(self):
        """The roster is durable and merges are regenerable, so history must not live only in
        a file the user is invited to delete."""
        first = merge_pl_infos(self.roster, [flat(1000, ['a', 'b', 'c'])])
        roster = self.roster.with_timeline(first.merged.timeline)

        second = merge_pl_infos(roster, [batch(2000, ['a'])], previous=first.merged)
        self.assertEqual([e.epoch for e in second.merged.timeline['a']], [1000, 2000])

        # Same merge with the merges pruned: the roster still carries what was learned.
        pruned = merge_pl_infos(roster, [batch(2000, ['a'])])
        self.assertEqual([e.epoch for e in pruned.merged.timeline['a']], [1000, 2000])

    def test_previous_carries_values_that_the_captures_no_longer_supply(self):
        first = merge_pl_infos(self.roster, [batch(1000, ['a'], description='D')])
        second = merge_pl_infos(self.roster, [], previous=first.merged)
        self.assertEqual(second.merged.get('a').data['description'], 'D')

    def test_the_playlists_own_payload_is_folded_too(self):
        report = merge_pl_infos(self.roster, [flat(1000, ['a'], title='Old'),
                                              flat(2000, ['a'], title='New')])
        self.assertEqual(report.merged.playlist['title'], 'New')
        self.assertNotIn('entries', report.merged.playlist)
        self.assertNotIn('merge_timeline', report.merged.playlist,
                         'the timeline is an envelope field, never a payload key')

    def test_epoch_is_the_newest_source_folded(self):
        report = merge_pl_infos(self.roster, [batch(2000, ['a']), batch(5000, ['b'])])
        self.assertEqual(report.merged.epoch, 5000)
        self.assertIsInstance(report.merged.epoch, Epoch)

    def test_level_reflects_what_was_reached(self):
        flat_only = merge_pl_infos(self.roster, [flat(1000, ['a', 'b', 'c'])])
        self.assertIs(flat_only.merged.info_level, PL_InfoLevel.MERGE_FLAT)
        with_full = merge_pl_infos(self.roster, [batch(2000, ['a'])])
        self.assertIs(with_full.merged.info_level, PL_InfoLevel.MERGE)

    def test_merging_nothing_at_all_still_produces_the_roster_shape(self):
        report = merge_pl_infos(self.roster, [])
        self.assertIsInstance(report.merged, MergePlaylist)
        self.assertEqual(report.merged.ids(), ('a', 'b', 'c'))
        self.assertEqual(report.merged.epoch, self.roster.last_updated)

    def test_it_writes_nothing_and_mutates_nothing(self):
        before = self.roster
        merge_pl_infos(self.roster, [batch(2000, ['a'])])
        self.assertEqual(before, self.roster)


if __name__ == '__main__':
    unittest.main()
