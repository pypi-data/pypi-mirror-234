import numpy as np
import time
import pandas as pd
class ATR:
    def __init__(self):
        pass

    @staticmethod
    def get_value(high,low, close, timeperiod=14):
        tr1 = (high - low)
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        atr = tr.rolling(timeperiod, min_periods=1).mean()
        return(atr)


if __name__ == "__main__":
    pass