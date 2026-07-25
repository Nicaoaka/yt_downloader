import unittest
from pldl.utils.utils import *
from pldl.yt_utils import *

class Tests(unittest.TestCase):

    def test_merge_objs(self):
        self.assertDictEqual(
            merge_objs({'a': 1}, {'b': 2}),
            {'a': 1, 'b': 2})
        self.assertDictEqual(
            merge_objs({'a': 1}, {'a': 2}),
            {'a': 2})

        self.assertDictEqual(
            merge_objs({'a': {'a': 1}}, {'a': {'b': 2}}),
            {'a': {'a': 1, 'b': 2}})
        self.assertDictEqual(
            merge_objs({'a': {'a': 1}}, {'a': {'a': 2}}),
            {'a': {'a': 2}})
        
        self.assertDictEqual(
            merge_objs({'a': {'a': 1}}, {'a': 2}),
            {'a': 2})
        self.assertDictEqual(
            merge_objs({'a': 1}, {'a': {'a': 2}}),
            {'a': {'a': 2}})
        
        self.assertListEqual(
            merge_objs([{'x': 1}], [{'x': 2}]),
            [{'x': 1}, {'x': 2}])
        self.assertDictEqual(
            merge_objs(
                merge_objs({}, {'merge_info': {'abc': {'1234': {'updates': ['hello']}}}}),
                {'merge_info': {'abc': {'1234': {'updates': ['bye']}}}}
            ), {'merge_info': {'abc': {'1234': {'updates': ['hello', 'bye']}}}})

    def test_has_content(self):
        self.assertEqual(has_content(""), False)
        self.assertEqual(has_content([]), False)
        self.assertEqual(has_content(set()), False)
        self.assertEqual(has_content(dict()), False)
        self.assertEqual(has_content([set()]), False)
        self.assertEqual(has_content([dict()]), False)
        self.assertEqual(has_content([[[[[[[]]]]]]]), False)
        self.assertEqual(has_content([[], [dict()], [], set()]), False)

        # any dict
        self.assertEqual(has_content('x'), True)
        self.assertEqual(has_content({'x': None}), True)
        self.assertEqual(has_content(['x']), True)
        self.assertEqual(has_content([['x']]), True)
        self.assertEqual(has_content([[], [[], 'x']]), True)

    def test_epoch(self):
        now = epoch_now()
        self.assertEqual(from_readable_epoch(to_readable_epoch(now)), now)
        self.assertEqual(from_readable_epoch(to_readable_epoch(0)), 0)
        self.assertEqual(from_readable_epoch(to_readable_epoch(-100)), -100)

def main():
    unittest.main()

if __name__ == "__main__":
    main()