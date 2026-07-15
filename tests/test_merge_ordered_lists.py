import unittest
from pldl.utils.merge_ordered_lists import merge_ordered_lists


class TestMergeUtil(unittest.TestCase):

    def test_simple_cases(self):
        test_cases = [
            ('A Z AB'.split(), 'AZB'),
            ('AFG BC BCEF CDEF'.split(), 'ABCDEFG'),
            ('A B C'.split(), 'ABC'),
            ('W AB BC CD ZY YX XW'.split(), 'ZYXWABCD'),

            
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
        # TODO - This should be fixed
        test_cases = [
            ('BC CA AB CDA'.split(), 'BCDA'),
            ('BC CA CDA AB'.split(), 'BCDA'),
        ]

        for lists, expected in test_cases:
            with self.subTest(lists=lists):
                for _ in range(100): # run many times
                    result = merge_ordered_lists(lists)
                    joined = ''.join(result)
                    self.assertEqual(joined, expected)

    def test_set_iteration_order(self):
        # set iteration leads to different results based on inputs
        test_cases = [
            ('AB B_-A'.split(), 'AB_-'),
            ('AB B_A-'.split(), 'AB-_'),
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
        lists = [
            '1256890ABDE',
            '3456890ABDE',
            '7890ABCDEFG',
        ]
        expected = '1234567890ABCDEFG'

        result = merge_ordered_lists(lists)
        joined = ''.join(result)
        self.assertEqual(joined, expected)


if __name__ == '__main__':
    unittest.main()
