# experiment.py

from typing import Iterable, List, Tuple, Optional

from attrs import define

import pandas as pd
import numpy as np

from market_break.process import array

__all__ = [
    "buy_sell_signals",
    "long_short_results",
    "TradingRecord",
    "ShortTradingRecord",
    "LongTradingRecord"
]

def buy_sell_signals(
        data: Iterable[float], up: Iterable[int], down: Iterable[int]
) -> Tuple[List[int], List[int]]:
    """
    Calculates the buy and sell signals from the trends.

    :param data: The data for the indicator.
    :param up: The up-trends indexes.
    :param down: The down-trends indexes.

    :return: The buy and sell indexes.
    """

    buy = []
    sell = []

    for i in range(len(pd.Series(data))):
        if (i in up) and (len(buy) == len(sell)):
            buy.append(i)

        elif (i in down) and (len(buy) > len(sell)):
            sell.append(i)
        # end if
    # end for

    return buy, sell
# end buy_sell_signals

@define
class TradingRecord:
    """A class to represent the trading record."""

    returns: np.ndarray
    entries: np.ndarray
    exits: np.ndarray
    data: Iterable[float]
    buy: Iterable[int]
    sell: Iterable[int]
    long: Optional[bool] = True
    short: Optional[bool] = True
    volume: Optional[float] = 1.0
    fee: Optional[float] = 0.0
    take: Optional[float] = None
    stop: Optional[float] = None
# end TradingRecord

class LongTradingRecord(TradingRecord):
    """A class to represent the trading record."""
# end LongTradingRecord

class ShortTradingRecord(TradingRecord):
    """A class to represent the trading record."""
# end ShortTradingRecord

# noinspection PyShadowingNames
def long_short_results(
        data: Iterable[float],
        buy: Iterable[int],
        sell: Iterable[int],
        volume: Optional[float] = 1.0,
        fee: Optional[float] = 0.0,
        take: Optional[float] = None,
        stop: Optional[float] = None
) -> Tuple[LongTradingRecord, ShortTradingRecord]:
    """
    Calculates the long and short signals from the indexes.

    :param data: The data for the indicator.
    :param buy: The buy indexes.
    :param sell: The sell indexes.
    :param volume: The initial investment volume.
    :param fee: The fee for an action.
    :param take: The take profit threshold.
    :param stop: The stop loss threshold.

    :return: The long and short indexes.
    """

    long_returns = [volume]
    short_returns = [volume]

    is_long = False
    is_short = False

    last_long = 0
    last_short = 0

    long_entries = []
    short_entries = []
    long_exits = []
    short_exits = []

    data = array(data)

    short_value = lambda i: (
        short_returns[-1] +
        ((-(data[i] - data[i - 1]) / data[i - 1]) * (1 - fee))
    )
    long_value = lambda i: (
        long_returns[-1] +
        (((data[i] - data[i - 1]) / data[i - 1]) * (1 - fee))
    )

    for i in range(1, len(pd.Series(data))):
        if is_long and (
            ((take is not None) and (last_long * take <= data[i])) or
            ((stop is not None) and (last_long * (1 - stop) >= data[i]))
        ):
            long_exits.append(i)

            is_long = False

            long_returns.append(long_value(i))
            short_returns.append(short_returns[-1])

            continue
        # end if

        if is_short and (
            ((take is not None) and (last_short * take >= data[i])) or
            ((stop is not None) and (last_short * (1 - stop) <= data[i]))
        ):
            short_exits.append(i)

            is_short = False

            short_returns.append(short_value(i))
            long_returns.append(long_returns[-1])

            continue
        # end if

        if is_long or (i in buy):
            is_short = False

            short_exits.append(i)

            long_returns.append(long_value(i))

            if not is_long:
                long_entries.append(i)

                is_long = True

                last_long = data[i]
            # end if

        else:
            long_returns.append(long_returns[-1])
        # end if

        if is_short or (i in sell):
            is_long = False

            long_exits.append(i)

            short_returns.append(short_value(i))

            if not is_short:
                short_entries.append(i)

                is_short = True

                last_short = data[i]
            # end if

        else:
            short_returns.append(short_returns[-1])
        # end if
    # end for

    return (
        LongTradingRecord(
            returns=np.array(long_returns).astype(float),
            entries=np.array(long_entries).astype(int),
            exits=np.array(long_exits).astype(int),
            data=data, buy=buy, sell=sell, volume=volume,
            fee=fee, take=take, stop=stop
        ),
        ShortTradingRecord(
            returns=np.array(short_returns).astype(float),
            entries=np.array(short_entries).astype(int),
            exits=np.array(short_exits).astype(int),
            data=data, buy=buy, sell=sell, volume=volume,
            fee=fee, take=take, stop=stop
        )
    )
# end long_short_results