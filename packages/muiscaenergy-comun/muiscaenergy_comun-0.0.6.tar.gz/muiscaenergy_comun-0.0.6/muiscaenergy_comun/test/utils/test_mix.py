import unittest
import pandas as pd
from src.utils.mix import parse_custom_freq


class TestUtilMix(unittest.TestCase):

    def test_parse_custom_freq(self):
        freq = '15T'
        td = parse_custom_freq(freq)

        self.assertEqual(td, pd.Timedelta(minutes=15))


if __name__ == '__main__':
    unittest.main()

