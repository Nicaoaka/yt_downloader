import unittest
from pldl.utils.merge_ordered_lists import merge_ordered_lists


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
