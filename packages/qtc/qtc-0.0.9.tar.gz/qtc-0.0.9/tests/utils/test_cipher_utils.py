import unittest
import qtc.utils.cipher_utils as cu


class TestCipherUtils(unittest.TestCase):
    def test_intersperse(self):
        self.assertEqual(cu.intersperse('foo', 'bar'), 'fboaor')
        self.assertEqual(cu.intersperse('steven', '_-'), 's_t-e_v-e_n-')

    def test_to_salted(self):
        self.assertEqual(cu.to_salted(text='Hello World'), '1910190e0e553901061830')

    def test_from_salted(self):
        self.assertEqual(cu.from_salted(secret_str='1910190e0e553901061830'), 'Hello World')


if __name__ == '__main__':
    unittest.main()

