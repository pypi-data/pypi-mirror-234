import unittest
from src.messages.base import TimeSeriesMessage as TSm
import pandas as pd
from datetime import datetime


class TestTimeSeriesMessage(unittest.TestCase):
    def setUp(self):
        self.ts_from = pd.date_range(start=datetime(2023, 9, 30, 12, 0, 0),
                                     end=datetime(2023, 10, 1, 11, 0, 0),
                                     freq='H',)
        self.ts = self.ts_from.copy()
        self.ts_to = self.ts_from + pd.Timedelta(hours=1)

    def test_msg_append(self):
        msg1 = (TSm()
                .append_datetime(self.ts))

        msg2 = (TSm()
                .append_datetime_from(self.ts_from)
                .append_datetime_to(self.ts_to)
                )

        variable = ['var1', 'var2']
        value = [[10] * 24, [20] * 24]
        msg3 = (TSm()
                .append_datetime_from(self.ts_from)
                .append_datetime_to(self.ts_to)
                .append(variable, value)
                )

        value = 2
        msg4 = (TSm()
                .append_datetime(self.ts)
                .append_value(value)
                )


if __name__ == '__main__':
    unittest.main()

