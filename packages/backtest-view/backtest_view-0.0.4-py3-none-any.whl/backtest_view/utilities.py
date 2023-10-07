import pandas as pd
from backtest_view.constants import Timeframe


def within_timestamp(
        timestamp1: pd.Timestamp,
        timestamp2: pd.Timestamp,
        timeframe=Timeframe
) -> bool:
    if timestamp1.year == timestamp2.year:
        if timeframe == Timeframe.YEAR:
            return True
        if timestamp1.month == timestamp2.month:
            if timeframe == Timeframe.MONTH:
                return True
            if timestamp1.day == timestamp2.day:
                if timeframe == Timeframe.DAY:
                    return True
                if timestamp1.hour == timestamp2.hour:
                    if timeframe == Timeframe.HOUR:
                        return True
                    if timestamp1.minute == timestamp2.minute:
                        if timeframe == Timeframe.MINUTE:
                            return True
    return False


def candles_to_seconds(count, timeframe):
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    return int(timeframe[:-1]) * seconds_per_unit[timeframe[-1]] * count
