"""Wrapping what yt-dlp returns: the payload stays byte-faithful, pldl's fields move out."""
import unittest

from pldl.downloader import Capture, UnavailableInfo, V_InfoLevel, VideoEntry
from pldl.model import Epoch


FLAT_PL_INFO = {
    'id': 'PL_x', '_type': 'playlist', 'title': 'Some Playlist', 'uploader': 'U',
    'playlist_count': 2, 'epoch': 500, 'extractor': 'youtube:tab',
    'info_level': 'FLAT',
    'entries': [
        {'id': 'a', '_type': 'url', 'title': 'A', 'channel': 'C', 'info_level': 'FLAT'},
        {'id': 'b', '_type': 'url', 'title': 'B', 'channel': None},
    ],
}


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
            'yt_unavailable_msg': 'gone', 'wa_unavailable_msg': None,
        }
        entry = VideoEntry.wrap(payload)

        self.assertIs(entry.info_level, V_InfoLevel.EXTRACT)
        self.assertEqual(entry.playlist_epoch, 999)
        self.assertIsInstance(entry.playlist_epoch, Epoch)
        self.assertEqual(
            entry.unavailable_infos,
            (UnavailableInfo(extractor='youtube', msg='gone', epoch=Epoch(1)),),
        )
        for pldl_key in ('info_level', 'unavailable_msgs', 'playlist_epoch',
                         'yt_unavailable_msg', 'wa_unavailable_msg'):
            self.assertNotIn(pldl_key, entry.unwrap())

    def test_an_int_info_level_survives(self):
        self.assertIs(VideoEntry.wrap({'id': 'a', 'info_level': 0}).info_level, V_InfoLevel.NONE)

    def test_level_is_derived_only_when_nothing_is_declared(self):
        self.assertIs(VideoEntry.wrap({'id': 'a', 'channel': 'c'}).info_level, V_InfoLevel.FLAT)
        self.assertIs(VideoEntry.wrap({'id': 'a'}).info_level, V_InfoLevel.NONE)
        self.assertIs(
            VideoEntry.wrap({'id': 'a'}, info_level=V_InfoLevel.DOWNLOAD).info_level,
            V_InfoLevel.DOWNLOAD, 'an explicit level wins over derivation')

    def test_capture_is_a_batch(self):
        capture = Capture(epoch=Epoch(100), videos=(
            VideoEntry.wrap({'id': 'a'}), VideoEntry.wrap({'id': 'b'})))
        self.assertEqual(len(capture), 2)
        self.assertEqual(capture.ids(), ('a', 'b'))
        self.assertIsNotNone(capture.get('a'))
        self.assertIsNone(capture.get('zzz'))
        self.assertEqual(Epoch.from_iso(capture.epoch.iso), 100)
        self.assertIsNone(capture.playlist, 'a per-video batch has no playlist payload')
        self.assertIsNone(capture.pl_id)

    def test_a_flat_extraction_wraps_into_the_same_envelope(self):
        capture = Capture.wrap_flat(FLAT_PL_INFO)
        self.assertEqual(capture.epoch, 500)
        self.assertEqual(capture.pl_id, 'PL_x')
        self.assertEqual(capture.ids(), ('a', 'b'))
        self.assertEqual(capture.playlist['title'], 'Some Playlist')
        self.assertNotIn('entries', capture.playlist)
        self.assertNotIn('info_level', capture.playlist, 'v1 key dropped')
        self.assertIs(capture.get('a').info_level, V_InfoLevel.FLAT)
        self.assertNotIn('info_level', capture.get('a').data, 'lifted onto the entry envelope')

    def test_a_flat_extraction_unwraps_to_what_yt_dlp_returned(self):
        expected = {k: v for k, v in FLAT_PL_INFO.items() if k != 'info_level'}
        expected['entries'] = [{k: v for k, v in e.items() if k != 'info_level'}
                               for e in expected['entries']]
        self.assertEqual(Capture.wrap_flat(FLAT_PL_INFO).unwrap_flat(), expected)


if __name__ == '__main__':
    unittest.main()
