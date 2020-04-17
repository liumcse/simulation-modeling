import unittest
from libs.utils import Utils


class TestUtils(unittest.TestCase):
    def test_round_float(self):
        self.assertEqual(27.778, Utils.round_float(27.777777778))


if __name__ == '__main__':
    unittest.main()
