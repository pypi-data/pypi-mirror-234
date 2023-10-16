import unittest
from unittest.mock import MagicMock


class TestKodiakLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        pass

    @classmethod
    def tearDownClass(self) -> None:
        pass


    def test_upper(self):
        x = MagicMock(return_value="1")
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()

