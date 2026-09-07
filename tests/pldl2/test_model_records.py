"""The roster, timeline, envelope, metadata and kind registry.

These carry the invariants the record depends on, so the tests are written as statements of
those invariants rather than as coverage of the methods.
"""
import dataclasses
import unittest

from pldl2.model.envelope import Capture, VideoEntry
from pldl2.model.epoch import from_iso
from pldl2.model.kinds import KINDS, InfoKind, Owner, PayloadShape, by_name, pldl_owned, user_owned
from pldl2.model.levels import V_InfoLevel
from pldl2.model.metadata import HistoryEntry, HistoryVideo, Metadata, Paths
from pldl2.model.roster import Roster, RosterEntry, fold_flat
from pldl2.model.timeline import BetterInfo, MergeTimelineEntry, entry_for, ordered, upsert


def _roster(*ids, epoch=1000):
    return Roster(
        id='PL_test',
        updated=epoch,
        entries=tuple(RosterEntry(id=i, first_seen=epoch, last_seen=epoch) for i in ids),
    )


class RosterQueries(unittest.TestCase):
    def test_index_of_returns_zero_not_falsy_none(self):
        """issue-1 #9: v1 gated on `if merge_i := index(...)`, so index 0 is falsy and the
        first video in a playlist could never be removed."""
        roster = _roster('a', 'b', 'c')
        self.assertEqual(roster.index_of('a'), 0)
        self.assertIsNone(roster.index_of('missing'))
        self.assertIsNotNone(roster.index_of('a'), 'must be distinguishable from absent')

    def test_ids_filters_by_membership(self):
        roster = _roster('a', 'b', 'c')
        roster = roster.with_entries([
            dataclasses.replace(roster.entries[0], in_playlist=True),
            dataclasses.replace(roster.entries[1], in_playlist=False),
            dataclasses.replace(roster.entries[2], in_playlist=True),
        ])
        self.assertEqual(roster.ids(), ('a', 'b', 'c'))
        self.assertEqual(roster.ids(in_playlist=True), ('a', 'c'))
        self.assertEqual(roster.ids(in_playlist=False), ('b',))

    def test_membership_and_lookup(self):
        roster = _roster('a', 'b')
        self.assertIn('a', roster)
        self.assertNotIn('z', roster)
        self.assertEqual(len(roster), 2)
        self.assertIsNone(roster.get('z'))
        self.assertEqual(roster.get('a').id, 'a')

    def test_is_frozen(self):
        with self.assertRaises(dataclasses.FrozenInstanceError):
            _roster('a').id = 'other'  # type: ignore[misc]


class FoldFlat(unittest.TestCase):
    """fold_flat is the only writer of in_playlist. These are its invariants."""

    def test_a_video_gone_from_youtube_keeps_its_row(self):
        """The 'never lose a video' promise. It flips a flag; it never drops a row."""
        roster = _roster('a', 'b', 'c', epoch=1000)
        folded = fold_flat(roster, ['a', 'c'], epoch=2000)

        self.assertEqual(folded.ids(), ('a', 'b', 'c'), 'b must still be present')
        self.assertFalse(folded.get('b').in_playlist)
        self.assertTrue(folded.get('a').in_playlist)

    def test_a_disappeared_video_keeps_its_last_seen(self):
        roster = _roster('a', 'b', epoch=1000)
        folded = fold_flat(roster, ['a'], epoch=2000)
        self.assertEqual(folded.get('b').last_seen, 1000, 'last_seen is when it was last there')
        self.assertEqual(folded.get('a').last_seen, 2000)

    def test_a_video_can_come_back(self):
        roster = fold_flat(_roster('a', 'b', epoch=1000), ['a'], epoch=2000)
        self.assertFalse(roster.get('b').in_playlist)

        returned = fold_flat(roster, ['a', 'b'], epoch=3000)
        self.assertTrue(returned.get('b').in_playlist)
        self.assertEqual(returned.get('b').last_seen, 3000)
        self.assertEqual(returned.get('b').first_seen, 1000, 'first_seen never moves')

    def test_new_ids_are_added(self):
        folded = fold_flat(_roster('a', epoch=1000), ['a', 'new'], epoch=2000)
        self.assertEqual(folded.ids(), ('a', 'new'))
        self.assertEqual(folded.get('new').first_seen, 2000)
        self.assertEqual(folded.get('new').last_seen, 2000)

    def test_titles_are_recorded_but_never_cleared(self):
        roster = Roster(id='p', entries=(RosterEntry(id='a', title='Original'),))
        kept = fold_flat(roster, ['a'], epoch=2000, titles={'a': None})
        self.assertEqual(kept.get('a').title, 'Original', 'a missing title must not erase one')

        updated = fold_flat(roster, ['a'], epoch=2000, titles={'a': 'Renamed'})
        self.assertEqual(updated.get('a').title, 'Renamed')

    def test_supplied_order_wins(self):
        folded = fold_flat(_roster('a', 'b', 'c'), ['a', 'b', 'c'], epoch=2000,
                           order=['c', 'a', 'b'])
        self.assertEqual(folded.ids(), ('c', 'a', 'b'))

    def test_an_order_that_omits_a_known_id_still_keeps_it(self):
        """Order reconciliation must never be able to delete a row."""
        folded = fold_flat(_roster('a', 'b', 'c'), ['a', 'c'], epoch=2000, order=['c', 'a'])
        self.assertEqual(set(folded.ids()), {'a', 'b', 'c'})
        self.assertEqual(folded.ids()[:2], ('c', 'a'))

    def test_updated_moves_forward_only(self):
        folded = fold_flat(_roster('a', epoch=5000), ['a'], epoch=1000)
        self.assertEqual(folded.updated, 5000)

    def test_folding_an_empty_extraction_marks_everything_gone(self):
        folded = fold_flat(_roster('a', 'b'), [], epoch=2000)
        self.assertEqual(folded.ids(), ('a', 'b'))
        self.assertEqual(folded.ids(in_playlist=True), ())


class Timeline(unittest.TestCase):
    def test_better_info_is_structured_not_a_string(self):
        """issue-1: v1 wrote 'FLAT -> EXTRACT' and display.py regexed it back into an enum."""
        better = BetterInfo(from_level=V_InfoLevel.FLAT, to_level=V_InfoLevel.EXTRACT)
        self.assertIs(better.from_level, V_InfoLevel.FLAT)
        self.assertIs(better.to_level, V_InfoLevel.EXTRACT)
        self.assertEqual(better.render(), 'FLAT -> EXTRACT')

    def test_same_epoch_updates_accumulate_rather_than_overwrite(self):
        """issue-1 #11: v1 wrote a singular 'update' string while readers looked for the
        plural 'updates' dict, so its dedup guard never fired and two edits in the same
        second collapsed to the last one."""
        timeline = ()
        timeline = upsert(timeline, MergeTimelineEntry(epoch=100, updates={'a': '<REMOVE>'}))
        timeline = upsert(timeline, MergeTimelineEntry(epoch=100, updates={'b': '<INSERT>'}))

        self.assertEqual(len(timeline), 1)
        self.assertEqual(dict(timeline[0].updates), {'a': '<REMOVE>', 'b': '<INSERT>'})

    def test_an_existing_entrys_recorded_level_never_moves(self):
        """issue-1 #6, confirmed: v1 restamped older entries with today's merged level, so a
        month-old FLAT entry read EXTRACT after the next merge and the flat step vanished."""
        timeline = (MergeTimelineEntry(epoch=100, info_level=V_InfoLevel.FLAT),)
        merged = upsert(timeline, MergeTimelineEntry(epoch=100, info_level=V_InfoLevel.EXTRACT,
                                                    updates={'x': 'y'}))
        self.assertIs(merged[0].info_level, V_InfoLevel.FLAT)
        self.assertEqual(dict(merged[0].updates), {'x': 'y'}, 'the new information still lands')

    def test_entries_are_frozen(self):
        entry = MergeTimelineEntry(epoch=100)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            entry.epoch = 200  # type: ignore[misc]

    def test_unavailable_messages_dedup(self):
        timeline = (MergeTimelineEntry(epoch=100, unavailable=('gone',)),)
        merged = upsert(timeline, MergeTimelineEntry(epoch=100, unavailable=('gone', 'also')))
        self.assertEqual(merged[0].unavailable, ('gone', 'also'))

    def test_ordering_and_lookup(self):
        timeline = ordered((MergeTimelineEntry(epoch=300), MergeTimelineEntry(epoch=100)))
        self.assertEqual([e.epoch for e in timeline], [100, 300])
        self.assertIsNotNone(entry_for(timeline, 300))
        self.assertIsNone(entry_for(timeline, 999))

    def test_empty_entries_are_identifiable(self):
        self.assertTrue(MergeTimelineEntry(epoch=1).is_empty())
        self.assertFalse(MergeTimelineEntry(epoch=1, updates={'a': 'b'}).is_empty())


class Envelope(unittest.TestCase):
    def test_data_stays_byte_faithful(self):
        payload = {'id': 'abc', 'title': 'T', 'channel': 'C', 'epoch': 5, 'extractor': 'youtube'}
        entry = VideoEntry.wrap(payload)
        self.assertEqual(entry.unwrap(), payload, 'nothing added, nothing dropped')

    def test_v1_pldl_keys_are_lifted_out_of_the_payload(self):
        """Wrapping a v1 file yields the same shape as wrapping a fresh extraction."""
        payload = {
            'id': 'abc', 'channel': 'C', 'extractor': 'youtube',
            'info_level': 'EXTRACT',
            'unavailable_msgs': [{'epoch': 1, 'msg': 'gone', 'type': 'youtube'}],
            'playlist_epoch': 999,
        }
        entry = VideoEntry.wrap(payload)

        self.assertIs(entry.info_level, V_InfoLevel.EXTRACT)
        self.assertEqual(entry.playlist_epoch, 999)
        self.assertEqual(len(entry.unavailable_msgs), 1)
        for pldl_key in ('info_level', 'unavailable_msgs', 'playlist_epoch'):
            self.assertNotIn(pldl_key, entry.unwrap(),
                             'pldl fields must not remain in the payload')

    def test_an_int_info_level_survives(self):
        """issue-1 #23: a v1 file can carry `"info_level": 0` and v1 could not re-add it."""
        entry = VideoEntry.wrap({'id': 'a', 'info_level': 0})
        self.assertIs(entry.info_level, V_InfoLevel.NONE)

    def test_level_is_derived_only_when_nothing_is_declared(self):
        self.assertIs(VideoEntry.wrap({'id': 'a', 'channel': 'c'}).info_level, V_InfoLevel.FLAT)
        self.assertIs(VideoEntry.wrap({'id': 'a'}).info_level, V_InfoLevel.NONE)
        self.assertIs(
            VideoEntry.wrap({'id': 'a'}, info_level=V_InfoLevel.DOWNLOAD).info_level,
            V_InfoLevel.DOWNLOAD, 'an explicit level wins over derivation')

    def test_capture_is_a_batch(self):
        capture = Capture(epoch=100, videos=(
            VideoEntry.wrap({'id': 'a'}), VideoEntry.wrap({'id': 'b'})))
        self.assertEqual(len(capture), 2)
        self.assertEqual(capture.ids(), ('a', 'b'))
        self.assertIsNotNone(capture.get('a'))
        self.assertIsNone(capture.get('zzz'))
        # Not asserted against a literal date: epoch 100 is 1969-12-31 in any negative-offset
        # zone, which is precisely the near-zero case _local() exists to survive.
        self.assertEqual(from_iso(capture.at), 100)


class MetadataRecord(unittest.TestCase):
    def _meta(self):
        return Metadata(id='PL_x', paths=Paths(playlist_dir='Some Playlist [PL_x]'))

    def test_history_stays_ordered_however_it_is_added(self):
        meta = self._meta().record(HistoryEntry(epoch=300)).record(HistoryEntry(epoch=100))
        self.assertEqual([e.epoch for e in meta.history], [100, 300])
        self.assertEqual(meta.latest().epoch, 300)

    def test_epochs_for_indexes_by_video(self):
        meta = self._meta().with_history([
            HistoryEntry(epoch=100, videos=(HistoryVideo(id='a'),)),
            HistoryEntry(epoch=200, videos=(HistoryVideo(id='b'),)),
            HistoryEntry(epoch=300, videos=(HistoryVideo(id='a'), HistoryVideo(id='b'))),
        ])
        self.assertEqual(meta.epochs_for('a'), (100, 300))
        self.assertEqual(meta.epochs_for('b'), (200, 300))
        self.assertEqual(meta.epochs_for('never'), ())

    def test_there_are_no_pointers(self):
        """The whole `pointers` block is gone; one pointer to a fixed path is a filename."""
        self.assertNotIn('pointers', {f.name for f in dataclasses.fields(Metadata)})

    def test_latest_on_an_empty_history(self):
        self.assertIsNone(self._meta().latest())


class KindRegistry(unittest.TestCase):
    def test_every_kind_declares_its_owner_consistently(self):
        for name, kind in KINDS.items():
            with self.subTest(kind=name):
                if kind.owner is Owner.PLDL:
                    self.assertTrue(kind.filename, 'pldl-owned files have fixed names')
                    self.assertTrue(kind.filename.startswith('_'),
                                    'the _ prefix means "pldl depends on this"')
                    self.assertFalse(kind.may_be_missing)
                else:
                    self.assertTrue(kind.tmpl_key, 'user-owned files are templated')
                    self.assertTrue(kind.may_be_missing,
                                    'user-owned files may vanish between runs')

    def test_the_registry_rejects_an_inconsistent_kind(self):
        with self.assertRaises(ValueError):
            InfoKind(name='bad', owner=Owner.PLDL, payload=PayloadShape.SINGLE)
        with self.assertRaises(ValueError):
            InfoKind(name='bad', owner=Owner.USER, payload=PayloadShape.SINGLE)

    def test_lookup_names_the_alternatives(self):
        self.assertIs(by_name('roster'), KINDS['roster'])
        with self.assertRaises(KeyError) as ctx:
            by_name('nope')
        self.assertIn('raw_flat', str(ctx.exception), 'the error should list what is known')

    def test_the_two_ownership_groups_partition_the_registry(self):
        self.assertEqual(len(user_owned()) + len(pldl_owned()), len(KINDS))
        self.assertEqual({k.name for k in pldl_owned()}, {'roster', 'metadata', 'archive'})

    def test_the_batch_kind_reads_the_newest_epoch(self):
        kind = by_name('raw_v_infos')
        self.assertEqual(kind.epoch_of({'videos': [{'epoch': 10}, {'epoch': 30}]}), 30)
        self.assertEqual(kind.epoch_of({'videos': []}), 0)


if __name__ == '__main__':
    unittest.main()
