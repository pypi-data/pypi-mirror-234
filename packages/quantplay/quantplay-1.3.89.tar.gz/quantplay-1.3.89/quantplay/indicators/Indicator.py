from quantplay.indicators.atr import ATR
import talib
from talib import abstract
import numpy as np
class Indicator:
    def __init__(self):
        pass

    @staticmethod
    def ema(series, periods, fillna=False):
        if fillna:
            return series.ewm(span=periods, min_periods=0).mean()

        return series.ewm(span=periods, min_periods=periods).mean()


    @staticmethod
    def atr(high, low, close, timeperiod=14):
        return ATR.get_value(high, low, close, timeperiod=timeperiod)

    @staticmethod
    def add_candlestick_pattern(day_candles, pattern_list=None):
        patterns = talib.get_function_groups()['Pattern Recognition']
        if pattern_list is not None:
            patterns = pattern_list

        day_candles.loc[:, 'long_pattern'] = 0
        day_candles.loc[:, 'short_pattern'] = 0

        day_candles.loc[:, 'pattern'] = np.nan
        for pattern in patterns:
            p = abstract.Function(pattern)
            day_candles.loc[:, pattern] = p(day_candles.open,
                                            day_candles.high,
                                            day_candles.low,
                                            day_candles.close)
            day_candles.loc[:, 'pattern'] = np.where(day_candles[pattern] <= -100,
                                                     'SHORT_{}'.format(pattern),
                                                     day_candles.pattern)
            day_candles.loc[:, 'pattern'] = np.where(day_candles[pattern] >= 100,
                                                     'LONG_{}'.format(pattern),
                                                     day_candles.pattern)
            day_candles.loc[:, 'pattern_score'] = day_candles[pattern]
