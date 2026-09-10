"""Playlist-order reconciliation.

The v1 suite, carried over unchanged against the ported module. It is the whole reason the
port can be trusted: `ordering.py` is v1's algorithm with three cleanups (a control-flow
`raise Warning` removed, private-attribute reach-ins replaced by accessors, and a mutable
default argument fixed), and nothing about its behaviour is meant to have moved.

The `'AB BC'`-style cases read as: each space-separated group is one list, highest priority
first, and the expected result is the reconciled order.
"""
import unittest
from pldl2.merge.ordering import merge_ordered_lists


class TestMergeUtil(unittest.TestCase):

    def test_simple_cases(self):
        test_cases = [
            ('A'.split(), 'A'),
            ('A B C'.split(), 'ABC'),
            ('AB BC'.split(), 'ABC'),
            ('ABC ABC'.split(), 'ABC'),
            ('A ABC ABCDE ABCDEFG'.split(), 'ABCDEFG'),
        ]

        for lists, expected in test_cases:
            with self.subTest(lists=lists):
                result = merge_ordered_lists(lists)
                joined = ''.join(result)
                self.assertEqual(joined, expected)

    def test_islands(self):
        test_cases = [
            ( 'A _ AB'.split(), 'AB_'),
            ('AB _ BC'.split(), 'ABC_'),
            ( 'B _ AB'.split(), 'AB_'),
            ('A_B - _CD _YZ'.split(), 'A_BCDYZ-'),
            ('_ AB BC CD ZY YX X_'.split(), 'ZYX_ABCD'),
        ]

        for lists, expected in test_cases:
            with self.subTest(lists=lists):
                result = merge_ordered_lists(lists)
                joined = ''.join(result)
                self.assertEqual(joined, expected)

    def test_conflicts(self):
        test_cases = [
            ('1234567890 0987654321'.split(), '1234567890'),
            ('AC BC CA'.split(), 'ABC'),
            ('CA BC AB'.split(), 'BCA'),
            ('AB 12B34A56'.split(), 'A12B3456'),
            ('AB BCA'.split(), 'ABC'),
        ]

        for lists, expected in test_cases:
            with self.subTest(lists=lists):
                result = merge_ordered_lists(lists)
                joined = ''.join(result)
                self.assertEqual(joined, expected)

    def test_deterministic(self):
        test_cases = [
            ('BC CA AB CDA'.split(), 'BCDA'),
            ('BC CA CDA AB'.split(), 'BCDA'),
        ]

        for lists, expected in test_cases:
            with self.subTest(lists=lists):
                result = merge_ordered_lists(lists)
                joined = ''.join(result)
                self.assertEqual(joined, expected)

    def test_iteration_order(self):
        test_cases = [
            ('AB B_-A'.split(), 'AB_-'),
            ('AB B_A-'.split(), 'AB_-'),
        ]

        for lists, expected in test_cases:
            with self.subTest(lists=lists):
                result = merge_ordered_lists(lists)
                joined = ''.join(result)
                self.assertEqual(joined, expected)

    def test_merge_patterns(self):
        test_cases = [
            ('AB BCDA'.split(), 'ABCD'),
            ('AB BCAD'.split(), 'ABCD'),
        ]

        for lists, expected in test_cases:
            with self.subTest(lists=lists):
                result = merge_ordered_lists(lists)
                joined = ''.join(result)
                self.assertEqual(joined, expected)

    def test_complex_merge(self):
        test_cases = [
            (
                ['1256890ABDE',
                 '3456890ABDE', 
                 '7890ABCDEFG'],
                '1234567890ABCDEFG'),
            (
                ['abcdefghi',
                 '12gh345cde67',
                 'AbcB',
                 'CdeD',],
                'a A bc C def 12 ghi 34567 B D'.replace(' ', '')),
            (
                ['abcde', '1d2', '3b4'],
                'a3bc1de24'),
            (
                ['1234567', 'A4B', 'a2b6c'],
                '1 a 23 A 45 b 67 B c'.replace(' ', '')),
            (
                'ABCD 1234 B_3'.split(),
                'ABCD12_34'.replace(' ', '')),
            (
                'ABC abc 1b2B3'.split(),
                'Aa1b2BCc3'.replace(' ', '')),
            (
                'ABC XYZ abcd b1B c2Y'.split(),
                'A ab1 BC X c2 YZ d'.replace(' ', '')),
        ]

        for lists, expected in test_cases:
            with self.subTest(lists=lists):
                result = merge_ordered_lists(lists)
                joined = ''.join(result)
                self.assertEqual(joined, expected)

if __name__ == '__main__':
    unittest.main()


class PortIsFaithful(unittest.TestCase):
    """The ported module and v1's must agree on everything, not just the curated cases.

    Delete this at the step-12 cutover, along with `pldl/`.
    """

    def test_matches_v1_on_random_inputs(self):
        import random

        from pldl.utils.merge_ordered_lists import (
            merge_ordered_lists as v1_merge_ordered_lists,
        )

        rng = random.Random(20260910)
        alphabet = 'abcdefgh'
        for _ in range(2000):
            lists = []
            for _ in range(rng.randint(0, 4)):
                items = rng.sample(alphabet, rng.randint(0, len(alphabet)))
                lists.append(items)
            with self.subTest(lists=lists):
                self.assertEqual(merge_ordered_lists(lists), v1_merge_ordered_lists(lists))

    def test_matches_v1_when_lists_disagree(self):
        """Conflict resolution is the part worth pinning: the newest list wins."""
        from pldl.utils.merge_ordered_lists import (
            merge_ordered_lists as v1_merge_ordered_lists,
        )

        cases = [
            ['ab', 'ba'],
            ['abc', 'cba'],
            ['ab', 'bc', 'ca'],
            ['abcd', 'dcba', 'bd'],
            ['ab', 'xyz', 'bc'],
        ]
        for case in cases:
            lists = [list(s) for s in case]
            with self.subTest(case=case):
                self.assertEqual(merge_ordered_lists(lists), v1_merge_ordered_lists(lists))
