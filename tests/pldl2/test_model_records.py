"""The roster, timeline, envelope, metadata and kind registry.

These carry the invariants the record depends on, so the tests are written as statements of
those invariants rather than as coverage of the methods.
"""
import dataclasses
import unittest

from pldl2.model import kinds as kinds_module
from pldl2.model.envelope import Capture, VideoEntry
from pldl2.model.epoch import Epoch
from pldl2.model.kinds import (
    KINDS,
    PATH_TEMPLATE_KEYS,
    InfoKind,
    KindName,
    Owner,
    PayloadShape,
    by_name,
    pldl_owned,
    user_owned,
)
from pldl2.model.levels import V_InfoLevel
from pldl2.model.metadata import HistoryEntry, HistoryVideo, Metadata, Paths
from pldl2.model.roster import Roster, RosterEntry, fold_flat
from pldl2.model.timeline import (
    BetterInfo,
    FieldUpdate,
    Manipulation,
    ManipulationKind,
    MergeTimelineEntry,
    VideoTimeline,
)


def _roster(*ids, epoch=1000):
    return Roster(
        id='PL_test',
        updated=epoch,
        entries=tuple(RosterEntry(id=i, first_seen=epoch, last_seen=epoch) for i in ids),
    )


class RosterQueries(unittest.TestCase):
    def test_index_of_returns_zero_distinguishably_from_absent(self):
        roster = _roster('a', 'b', 'c')
        self.assertEqual(roster.index_of('a'), 0)
        self.assertIsNone(roster.index_of('missing'))
        self.assertIsNotNone(roster.index_of('a'))

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

    def test_epochs_are_coerced(self):
        """Plain ints passed in become Epoch, so `.iso` is always available downstream."""
        roster = Roster(id='p', updated=1000, entries=(RosterEntry(id='a', last_seen=5),))
        self.assertIsInstance(roster.updated, Epoch)
        self.assertIsInstance(roster.entries[0].first_seen, Epoch)
        self.assertIsInstance(roster.entries[0].last_seen, Epoch)
        self.assertEqual(Epoch.from_iso(roster.updated.iso), 1000)


class FoldFlat(unittest.TestCase):
    """fold_flat is the only writer of in_playlist. These are its invariants."""

    def test_a_video_gone_from_youtube_keeps_its_row(self):
        roster = _roster('a', 'b', 'c', epoch=1000)
        folded = fold_flat(roster, ['a', 'c'], epoch=2000)

        self.assertEqual(folded.ids(), ('a', 'b', 'c'), 'b must still be present')
        self.assertFalse(folded.get('b').in_playlist)
        self.assertTrue(folded.get('a').in_playlist)

    def test_a_disappeared_video_keeps_its_last_seen(self):
        folded = fold_flat(_roster('a', 'b', epoch=1000), ['a'], epoch=2000)
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
        self.assertEqual(fold_flat(_roster('a', epoch=5000), ['a'], epoch=1000).updated, 5000)

    def test_folding_an_empty_extraction_marks_everything_gone(self):
        folded = fold_flat(_roster('a', 'b'), [], epoch=2000)
        self.assertEqual(folded.ids(), ('a', 'b'))
        self.assertEqual(folded.ids(in_playlist=True), ())


class RosterContext(unittest.TestCase):
    """Best-effort context: recorded when offered, never cleared, never authoritative."""

    def test_context_is_taken_from_the_flat_entry(self):
        folded = fold_flat(_roster(), ['a'], epoch=2000, infos={
            'a': {'id': 'a', 'title': 'A Video', 'channel': 'Some Channel', 'duration': 42}})
        entry = folded.get('a')
        self.assertEqual(entry.title, 'A Video')
        self.assertEqual(entry.uploader, 'Some Channel')
        self.assertEqual(entry.duration, 42)

    def test_uploader_falls_back_across_the_names_youtube_uses(self):
        for key in ('uploader', 'channel', 'creator'):
            with self.subTest(key=key):
                folded = fold_flat(_roster(), ['a'], epoch=1, infos={'a': {'id': 'a', key: 'X'}})
                self.assertEqual(folded.get('a').uploader, 'X')

    def test_a_missing_key_never_clears_a_known_value(self):
        roster = Roster(id='p', entries=(RosterEntry(id='a', title='Original', uploader='U'),))
        folded = fold_flat(roster, ['a'], epoch=2000, infos={'a': {'id': 'a'}})
        self.assertEqual(folded.get('a').title, 'Original')
        self.assertEqual(folded.get('a').uploader, 'U')

    def test_a_present_key_updates(self):
        roster = Roster(id='p', entries=(RosterEntry(id='a', title='Original'),))
        folded = fold_flat(roster, ['a'], epoch=2000, infos={'a': {'id': 'a', 'title': 'New'}})
        self.assertEqual(folded.get('a').title, 'New')


class Timeline(unittest.TestCase):
    def test_better_info_is_structured_not_a_string(self):
        better = BetterInfo(from_level=V_InfoLevel.FLAT, to_level=V_InfoLevel.EXTRACT)
        self.assertIs(better.from_level, V_InfoLevel.FLAT)
        self.assertEqual(better.render(), 'FLAT -> EXTRACT')

    def test_entries_at_the_same_epoch_all_survive(self):
        """Two distinct things can happen in one second; neither replaces the other."""
        timeline = VideoTimeline()
        timeline = timeline.add(MergeTimelineEntry(
            epoch=Epoch(100), updates=(FieldUpdate(field='title', value='T'),)))
        timeline = timeline.add(MergeTimelineEntry(
            epoch=Epoch(100),
            manipulations=(Manipulation(kind=ManipulationKind.INSERT, detail='to=1'),)))

        self.assertEqual(len(timeline), 2)
        self.assertEqual(len(timeline.at_epoch(100)), 2)

    def test_identical_entries_collapse(self):
        entry = MergeTimelineEntry(epoch=Epoch(100),
                                   updates=(FieldUpdate(field='title', value='T'),))
        self.assertEqual(len(VideoTimeline().add(entry).add(entry)), 1)

    def test_entries_are_hashable(self):
        """Dedup needs it, so nothing in an entry may be an unhashable container."""
        entry = MergeTimelineEntry(
            epoch=Epoch(1),
            updates=(FieldUpdate(field='a', value='b'),),
            manipulations=(Manipulation(kind=ManipulationKind.MOVE),),
            unavailable=('gone',))
        self.assertEqual(len({entry, entry}), 1)

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
        """Ordering by merge priority instead would put the 2026 flat before the 2024
        download, and the recorded progression would read backwards."""
        timeline = VideoTimeline((
            MergeTimelineEntry(epoch=Epoch(1_788_000_000), info_level=V_InfoLevel.FLAT,
                               updates=(FieldUpdate(field='x', value='1'),)),
            MergeTimelineEntry(epoch=Epoch(1_704_067_200), info_level=V_InfoLevel.DOWNLOAD,
                               updates=(FieldUpdate(field='y', value='2'),)),
        ))
        self.assertEqual([int(e.epoch) for e in timeline], [1_704_067_200, 1_788_000_000])

    def test_manipulations_are_separate_from_field_updates(self):
        """An update means the upstream data changed; a manipulation means you changed the
        record. One bag for both leaves a reader unable to tell them apart."""
        entry = MergeTimelineEntry(
            epoch=Epoch(1),
            updates=(FieldUpdate(field='title', value='New Title'),),
            manipulations=(Manipulation(kind=ManipulationKind.REMOVE),))
        self.assertEqual(len(entry.updates), 1)
        self.assertEqual(len(entry.manipulations), 1)
        self.assertEqual(entry.manipulations[0].render(), '<REMOVE>')
        self.assertEqual(
            Manipulation(kind=ManipulationKind.REPLACE, detail='from=b to=c').render(),
            '<REPLACE from=b to=c>')

    def test_entries_are_frozen(self):
        with self.assertRaises(dataclasses.FrozenInstanceError):
            MergeTimelineEntry(epoch=Epoch(100)).epoch = Epoch(200)  # type: ignore[misc]

    def test_empty_entries_are_identifiable(self):
        self.assertTrue(MergeTimelineEntry(epoch=Epoch(1)).is_empty())
        self.assertFalse(MergeTimelineEntry(
            epoch=Epoch(1), updates=(FieldUpdate(field='a', value='b'),)).is_empty())
        self.assertFalse(MergeTimelineEntry(
            epoch=Epoch(1),
            manipulations=(Manipulation(kind=ManipulationKind.MOVE),)).is_empty())

    def test_epoch_is_coerced(self):
        self.assertIsInstance(MergeTimelineEntry(epoch=100).epoch, Epoch)

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


class Envelope(unittest.TestCase):
    def test_data_stays_byte_faithful(self):
        payload = {'id': 'abc', 'title': 'T', 'channel': 'C', 'epoch': 5, 'extractor': 'youtube'}
        self.assertEqual(VideoEntry.wrap(payload).unwrap(), payload)

    def test_pldl_keys_are_lifted_out_of_the_payload(self):
        payload = {
            'id': 'abc', 'channel': 'C', 'extractor': 'youtube',
            'info_level': 'EXTRACT',
            'unavailable_msgs': [{'epoch': 1, 'msg': 'gone', 'type': 'youtube'}],
            'playlist_epoch': 999,
        }
        entry = VideoEntry.wrap(payload)

        self.assertIs(entry.info_level, V_InfoLevel.EXTRACT)
        self.assertEqual(entry.playlist_epoch, 999)
        self.assertIsInstance(entry.playlist_epoch, Epoch)
        self.assertEqual(len(entry.unavailable_msgs), 1)
        for pldl_key in ('info_level', 'unavailable_msgs', 'playlist_epoch'):
            self.assertNotIn(pldl_key, entry.unwrap())

    def test_data_is_read_only_at_runtime(self):
        """`frozen` protects the reference; the payload needs protecting too."""
        entry = VideoEntry.wrap({'id': 'a', 'title': 'T'})
        with self.assertRaises(TypeError):
            entry.data['title'] = 'changed'  # type: ignore[index]

    def test_mutating_the_source_dict_does_not_reach_inside(self):
        payload = {'id': 'a', 'title': 'T'}
        entry = VideoEntry.wrap(payload)
        payload['title'] = 'changed'
        self.assertEqual(entry.data['title'], 'T')

    def test_an_int_info_level_survives(self):
        self.assertIs(VideoEntry.wrap({'id': 'a', 'info_level': 0}).info_level, V_InfoLevel.NONE)

    def test_level_is_derived_only_when_nothing_is_declared(self):
        self.assertIs(VideoEntry.wrap({'id': 'a', 'channel': 'c'}).info_level, V_InfoLevel.FLAT)
        self.assertIs(VideoEntry.wrap({'id': 'a'}).info_level, V_InfoLevel.NONE)
        self.assertIs(
            VideoEntry.wrap({'id': 'a'}, info_level=V_InfoLevel.DOWNLOAD).info_level,
            V_InfoLevel.DOWNLOAD, 'an explicit level wins over derivation')

    def test_entry_epoch_reads_the_payload(self):
        self.assertEqual(VideoEntry.wrap({'id': 'a', 'epoch': 77}).epoch, 77)
        self.assertEqual(VideoEntry.wrap({'id': 'a'}).epoch, 0)

    def test_capture_is_a_batch(self):
        capture = Capture(epoch=Epoch(100), videos=(
            VideoEntry.wrap({'id': 'a'}), VideoEntry.wrap({'id': 'b'})))
        self.assertEqual(len(capture), 2)
        self.assertEqual(capture.ids(), ('a', 'b'))
        self.assertIsNotNone(capture.get('a'))
        self.assertIsNone(capture.get('zzz'))
        self.assertEqual(Epoch.from_iso(capture.epoch.iso), 100)


class MetadataRecord(unittest.TestCase):
    def _meta(self):
        return Metadata(id='PL_x', paths=Paths(playlist_dir='Some Playlist [PL_x]'))

    def test_history_stays_ordered_however_it_is_added(self):
        meta = self._meta().record(HistoryEntry(epoch=Epoch(300))).record(
            HistoryEntry(epoch=Epoch(100)))
        self.assertEqual([int(e.epoch) for e in meta.history], [100, 300])
        self.assertEqual(meta.latest().epoch, 300)

    def test_epochs_for_indexes_by_video(self):
        meta = self._meta().with_history([
            HistoryEntry(epoch=Epoch(100), videos=(HistoryVideo(id='a'),)),
            HistoryEntry(epoch=Epoch(200), videos=(HistoryVideo(id='b'),)),
            HistoryEntry(epoch=Epoch(300), videos=(HistoryVideo(id='a'), HistoryVideo(id='b'))),
        ])
        self.assertEqual(meta.epochs_for('a'), (100, 300))
        self.assertEqual(meta.epochs_for('b'), (200, 300))
        self.assertEqual(meta.epochs_for('never'), ())

    def test_a_videos_own_epoch_wins_over_the_sessions(self):
        """A session runs for many minutes, so backoff should use when the video was tried."""
        meta = self._meta().with_history([
            HistoryEntry(epoch=Epoch(1000), videos=(
                HistoryVideo(id='a', epoch=Epoch(1400)),
                HistoryVideo(id='b'),
            )),
        ])
        self.assertEqual(meta.epochs_for('a'), (1400,))
        self.assertEqual(meta.epochs_for('b'), (1000,), 'falls back to the session epoch')

    def test_there_are_no_pointers(self):
        self.assertNotIn('pointers', {f.name for f in dataclasses.fields(Metadata)})

    def test_latest_on_an_empty_history(self):
        self.assertIsNone(self._meta().latest())

    def test_path_templates_may_use_yt_dlp_expressions(self):
        """Templates are resolved by yt-dlp, so arithmetic and format specs are legal."""
        self.assertIn('%(playlist_index + 1)d', Paths(playlist_dir='x').link_file)


class KindRegistry(unittest.TestCase):
    def test_kinds_are_reachable_as_module_constants(self):
        """A misspelling is then an AttributeError at import, not a KeyError at runtime."""
        self.assertIs(kinds_module.ROSTER, KINDS[KindName.ROSTER])
        self.assertIs(kinds_module.RAW_FLAT, KINDS[KindName.RAW_FLAT])
        with self.assertRaises(AttributeError):
            _ = kinds_module.ARHCIVE  # noqa: B018 - the typo is the point

    def test_every_kind_declares_its_owner_consistently(self):
        for name, kind in KINDS.items():
            with self.subTest(kind=name):
                if kind.owner is Owner.PLDL:
                    self.assertTrue(kind.filename.startswith('_'))
                    self.assertFalse(kind.may_be_missing)
                else:
                    self.assertIn(kind.tmpl_key, PATH_TEMPLATE_KEYS)
                    self.assertTrue(kind.may_be_missing)

    def test_a_tmpl_key_must_name_a_real_template_field(self):
        """Validated against Paths itself, so the two cannot drift apart."""
        with self.assertRaises(ValueError) as ctx:
            InfoKind(name=KindName.RAW_FLAT, owner=Owner.USER,
                     payload=PayloadShape.SINGLE, tmpl_key='raw_flta')
        self.assertIn('raw_flta', str(ctx.exception))

    def test_playlist_dir_is_not_a_template_key(self):
        """It names the folder, not a file inside it."""
        self.assertNotIn('playlist_dir', PATH_TEMPLATE_KEYS)

    def test_the_registry_rejects_an_inconsistent_kind(self):
        with self.assertRaises(ValueError):
            InfoKind(name=KindName.ROSTER, owner=Owner.PLDL, payload=PayloadShape.SINGLE)
        with self.assertRaises(ValueError):
            InfoKind(name=KindName.RAW_FLAT, owner=Owner.USER, payload=PayloadShape.SINGLE)
        with self.assertRaises(ValueError):
            InfoKind(name=KindName.ROSTER, owner=Owner.PLDL,
                     payload=PayloadShape.SINGLE, filename='roster.json')

    def test_lookup_by_name_names_the_alternatives(self):
        self.assertIs(by_name('roster'), kinds_module.ROSTER)
        with self.assertRaises(KeyError) as ctx:
            by_name('nope')
        self.assertIn('raw_flat', str(ctx.exception))

    def test_the_two_ownership_groups_partition_the_registry(self):
        self.assertEqual(len(user_owned()) + len(pldl_owned()), len(KINDS))
        self.assertEqual({k.name for k in pldl_owned()},
                         {KindName.ROSTER, KindName.METADATA, KindName.ARCHIVE})

    def test_the_batch_kind_reads_the_newest_epoch(self):
        self.assertEqual(
            kinds_module.RAW_V_INFOS.epoch_of({'videos': [{'epoch': 10}, {'epoch': 30}]}), 30)
        self.assertEqual(kinds_module.RAW_V_INFOS.epoch_of({'videos': []}), 0)


if __name__ == '__main__':
    unittest.main()
