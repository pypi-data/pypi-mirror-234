import pandas as pd


class Message:

    DT = 'datetime'
    DT_FROM = 'datetime_from'
    DT_TO = 'datetime_to'
    DT_UTC = 'datetime_utc'

    VAR = 'variable'
    VAL = 'value'

    COLUMNS = [DT_UTC, DT_FROM, DT_TO, VAR, VAL]


class TimeSeriesMessage(Message):

    def __init__(self):
        self.df = pd.DataFrame()

    def append_datetime(self, timeseries):
        self.df[Message.DT] = timeseries
        return self

    def append_datetime_from(self, timeseries):
        self.df[Message.DT_FROM] = timeseries
        return self

    def append_datetime_to(self, timeseries):
        self.df[Message.DT_TO] = timeseries
        return self

    def append_datetime_utc(self, timeseries):
        self.df[Message.DT_UTC] = timeseries
        return self

    def append_value(self, value):
        self.df[Message.VAL] = value
        return self

    def append(self, var, val):

        if len(var) == 1:
            self.df[Message.VAR] = var
            self.df[Message.VAL] = val

            return self

        temp_df = self.df.copy()
        for i, variable in enumerate(var):
            df_dummy = temp_df
            if i < 1:
                self.df[Message.VAR] = variable
                self.df[Message.VAL] = val[0]
                df_dummy = None
            else:
                df_dummy[Message.VAR] = variable
                df_dummy[Message.VAL] = val[i]

            self.df = pd.concat([self.df, df_dummy], ignore_index=True)

        return self
