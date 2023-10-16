from muiscaenergy_comun.src.messages.base import TimeSeriesMessage as TSm
from muiscaenergy_comun.src.utils.mix import parse_custom_freq

from timezonefinder import TimezoneFinder
from datetime import datetime
import pandas as pd


def get_timeseries(ts_from: datetime = None,
                   ts_to: datetime = None,
                   freq: str = 'H',
                   lat=None,
                   lon=None,
                   tz=None):
    """
    Generate time series data for a given parameters.
    Range (ts_from, ts_to) and frequency (freq) of the series are required parameters.
    Location by latitude and longitude (lat, lon) or time zone (tz) are optional parameters.

    :param ts_from: Start date and time for the time series.
    :param ts_to: End date and time for the time series.
    :param freq: Frequency unit for the time series. Default is 'H' (hours).
    :param lat: Latitude for geographical time zone information.
    :param lon: Longitude for geographical time zone information.
    :param tz: Time zone identifier.
    :return: An Object containing the generated time series.
    To access its dataframe, add ".df" to the object.
    """

    if freq is None or (ts_from and ts_to) is None:
        raise ValueError("ts_from, ts_to, and freq parameters are required.")

    if lat and lon:
        tz = TimezoneFinder().timezone_at(lng=lon, lat=lat)
        ts_from = pd.date_range(start=pd.to_datetime(ts_from),
                                end=pd.to_datetime(ts_to),
                                freq=freq,
                                tz=tz)
        ts_to = ts_from + pd.Timedelta(parse_custom_freq(freq=freq))
        ts_utc = ts_from.tz_convert('UTC')

        msg_out = (TSm()
                   .append_datetime_from(ts_from)
                   .append_datetime_to(ts_to)
                   .append_datetime_utc(ts_utc)
                   )

        return msg_out

    if tz:
        ts_from = pd.date_range(start=pd.to_datetime(ts_from),
                                end=pd.to_datetime(ts_to),
                                freq=freq,
                                tz=tz)
        ts_to = ts_from + pd.Timedelta(parse_custom_freq(freq=freq))
        ts_utc = ts_from.tz_convert('UTC')

        msg_out = (TSm()
                   .append_datetime_from(ts_from)
                   .append_datetime_to(ts_to)
                   .append_datetime_utc(ts_utc)
                   )

        return msg_out

    ts = pd.date_range(start=pd.to_datetime(ts_from),
                       end=pd.to_datetime(ts_to),
                       freq=freq,)

    msg_out = TSm().append_datetime(ts)

    return msg_out
