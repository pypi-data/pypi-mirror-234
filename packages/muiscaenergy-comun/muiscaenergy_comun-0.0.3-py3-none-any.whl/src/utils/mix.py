import pandas as pd


def parse_custom_freq(freq):
    """
    Parse a custom frequency string to a pandas Timedelta object. This function parses a custom frequency
    string that combines a number and a time unit. It supports time units 'T' for minutes, 'H' for hours, and 'D' for days.

    :param freq: A custom frequency string, e.g., '15T' for 15 minutes, '3H' for 3 hours, etc.
    :return: pd.Timedelta: A Timedelta object representing the parsed time duration.

    Example: parse_custom_freq('15T') returns a Timedelta object representing 15 minutes.
    """

    num = ""
    unit = ""

    for char in freq:
        if char.isdigit():
            num += char
        else:
            unit += char

    if not num:
        num = "1"

    if unit == 'T':
        return pd.Timedelta(minutes=int(num))
    elif unit == 'H':
        return pd.Timedelta(hours=int(num))
    elif unit == 'D':
        return pd.Timedelta(days=int(num))
    else:
        raise ValueError("Invalid value for 'freq'.")
