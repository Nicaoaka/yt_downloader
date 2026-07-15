import unittest
from pldl.utils.utils import *

class Tests(unittest.TestCase):

    def test_dict_merge(self):
        self.assertDictEqual(
            dict_merge({'a': 1}, {'b': 2}),
            {'a': 1, 'b': 2})
        self.assertDictEqual(
            dict_merge({'a': 1}, {'a': 2}),
            {'a': 2})

        self.assertDictEqual(
            dict_merge({'a': {'a': 1}}, {'a': {'b': 2}}),
            {'a': {'a': 1, 'b': 2}})
        self.assertDictEqual(
            dict_merge({'a': {'a': 1}}, {'a': {'a': 2}}),
            {'a': {'a': 2}})
        
        self.assertDictEqual(
            dict_merge({'a': {'a': 1}}, {'a': 2}),
            {'a': 2})
        self.assertDictEqual(
            dict_merge({'a': 1}, {'a': {'a': 2}}),
            {'a': {'a': 2}})

    def test_epoch(self):
        now = epoch_now()
        self.assertEqual(from_readable_epoch(to_readable_epoch(now)), now)
        self.assertEqual(from_readable_epoch(to_readable_epoch(0)), 0)
        self.assertEqual(from_readable_epoch(to_readable_epoch(-100)), -100)

def main():
    unittest.main()

if __name__ == "__main__":
    main()