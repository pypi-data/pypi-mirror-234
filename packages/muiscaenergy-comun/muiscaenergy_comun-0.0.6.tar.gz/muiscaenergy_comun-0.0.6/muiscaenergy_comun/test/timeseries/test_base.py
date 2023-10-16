import unittest
from datetime import datetime
from src.timeseries.base import get_timeseries
from src.messages.base import TimeSeriesMessage as TSm


class TestGetTimeseries(unittest.TestCase):

    def setUp(self):
        self.ts_from = datetime(2023, 9, 30, 12, 0, 0)
        self.ts_to = datetime(2023, 10, 1, 11, 0, 0)
        self.freq = 'H'
        self.lat = 52.5200
        self.lon = 13.4050
        self.tz = 'America/Los_Angeles'

    def test_get_timeseries(self):
        msg1 = get_timeseries(ts_from=self.ts_from,
                              ts_to=self.ts_to,
                              freq=self.freq)
        self.assertIsInstance(msg1, TSm)

        msg2 = get_timeseries(ts_from=self.ts_from,
                              ts_to=self.ts_to,
                              freq=self.freq,
                              lat=self.lat,
                              lon=self.lon)
        self.assertIsInstance(msg2, TSm)

        msg3 = get_timeseries(ts_from=self.ts_from,
                              ts_to=self.ts_to,
                              freq=self.freq,
                              tz=self.tz)
        self.assertIsInstance(msg3, TSm)


if __name__ == '__main__':
    unittest.main()
