import pandas as pd
import unittest
import qtc.utils.misc_utils as mu


class TestMiscUtils(unittest.TestCase):
    def test_iterable_to_tuple(self):
        input = 'Hello'
        output = mu.iterable_to_tuple(input, raw_type='str')
        self.assertEqual(output, ('Hello',))

        input = '5'
        output = mu.iterable_to_tuple(input, raw_type='int')
        self.assertEqual(output, (5,))

        input = 'Hello,World'
        output = mu.iterable_to_tuple(input, raw_type='str')
        self.assertEqual(output, ('Hello','World'))

        input = '5,3,-1,3,5,9'
        output = mu.iterable_to_tuple(input, raw_type='int')
        self.assertEqual(output, (5, 3, -1, 9))

        input = '5,3,-1,3,5,9'
        output = mu.iterable_to_tuple(input, raw_type='int', remove_duplicates=False)
        self.assertEqual(output, (5,3,-1,3,5,9))

        input = '5, -1,   3,9, 9'
        output = mu.iterable_to_tuple(input, raw_type='int')
        self.assertEqual(output, (5, -1, 3, 9))

        input = '5, -1,   3,9, 9'
        output = mu.iterable_to_tuple(input, raw_type='int')
        self.assertEqual(output, (5,-1,3,9))

        input = pd.Series([4,-2,9,'test'])
        output = mu.iterable_to_tuple(input, raw_type='str')
        self.assertEqual(output, ('4', '-2', '9', 'test'))

        input = -4
        output = mu.iterable_to_tuple(input, raw_type='int')
        self.assertEqual(output, (-4,))

    def test_iterable_to_db_str(self):
        input = '5, 3,-1,3,5,9'
        output = mu.iterable_to_db_str(input, raw_type='int')
        self.assertEqual(output, '(5,3,-1,9)')

        input = 'Hello,World'
        output = mu.iterable_to_db_str(input, raw_type='str')
        self.assertEqual(output, "('Hello','World')")


if __name__ == '__main__':
    unittest.main()
