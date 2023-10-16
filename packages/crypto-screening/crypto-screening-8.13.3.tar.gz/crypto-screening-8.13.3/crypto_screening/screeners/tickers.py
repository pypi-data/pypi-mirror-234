# tickers.py

import datetime as dt
from typing import (
    Dict, Optional, Iterable, Union, List, Callable
)

import pandas as pd

from cryptofeed.types import Ticker
from cryptofeed.defines import TICKER

from crypto_screening.symbols import adjust_symbol
from crypto_screening.dataset import BIDS, ASKS, create_dataset
from crypto_screening.screeners.screener import TickersScreener
from crypto_screening.screeners.callbacks import BaseCallback
from crypto_screening.screeners.recorder import (
    MarketScreener, MarketRecorder, MarketHandler, record
)

__all__ = [
    "TickersMarketScreener",
    "TickersMarketRecorder",
    "TickersScreener",
    "tickers_market_screener",
    "create_tickers_market_dataset",
    "record_tickers",
    "create_tickers_screeners"
]

def create_tickers_market_dataset() -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :return: The dataframe.
    """

    return create_dataset(columns=TickersMarketRecorder.COLUMNS)
# end create_tickers_market_dataset

async def record_tickers(
        screeners: Iterable[TickersScreener],
        data: Ticker,
        timestamp: float,
        insert: Optional[bool] = True,
        callbacks: Optional[Iterable[BaseCallback]] = None
) -> bool:
    """
    Records the data from the crypto feed into the dataset.

    :param screeners: The screeners.
    :param data: The data from the exchange.
    :param timestamp: The time of the request.
    :param insert: The value to insert data into the datasets.
    :param callbacks: The callbacks for the service.

    :return: The validation value.
    """

    new_data = {
        BIDS: float(data.bid),
        ASKS: float(data.ask)
    }

    exchange = data.exchange.lower()
    symbol = adjust_symbol(symbol=data.symbol)

    return await record(
        screeners=screeners, data=new_data,
        insert=insert, callbacks=callbacks, key=TickersScreener.NAME,
        timestamp=timestamp, exchange=exchange, symbol=symbol
    )
# end record_tickers

RecorderParameters = Dict[str, Union[Iterable[str], Dict[str, Callable]]]

class TickersMarketRecorder(MarketRecorder):
    """
    A class to represent a crypto data feed recorder.
    This object passes the record method to the handler object to record
    the data fetched by the handler.

    Parameters:

    - screeners:
        The screeners to record data into their market datasets.

    - callbacks:
        The callbacks to run when collecting new data.

    >>> from crypto_screening.screeners.tickers import TickersMarketRecorder
    >>>
    >>> recorder = TickersMarketRecorder(...)
    """

    COLUMNS = TickersScreener.COLUMNS

    def parameters(self) -> RecorderParameters:
        """
        Returns the order book parameters.

        :return: The order book parameters.
        """

        return dict(
            channels=[TICKER],
            callbacks={TICKER: self.record},
            max_depth=1
        )
    # end parameters

    async def process(self, data: Ticker, timestamp: float) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        """

        exchange = data.exchange.lower()
        symbol = adjust_symbol(symbol=data.symbol)

        screeners = self.find_tickers_screeners(exchange=exchange, symbol=symbol)

        return await record_tickers(
            screeners=screeners, data=data, timestamp=timestamp,
            callbacks=self.callbacks, insert=self.insert
        )
    # end process
# end MarketOrdersRecorder

class TickersMarketScreener(MarketScreener):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.

    - handler:
        The handler object to handle the data feed.

    - recorder:
        The recorder object to record the data of the market from the feed.

    - screeners:
        The screener object to control and fill with data.

    - refresh:
        The duration of time between each refresh. 0 means no refresh.

    - amount:
        The amount of symbols for each symbols group for an exchange.

    - limited:
        The value to limit the running screeners to active exchanges.

    >>> from crypto_screening.screeners.tickers import tickers_market_screener
    >>>
    >>> structure = {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}
    >>>
    >>> screener = tickers_market_screener(data=structure)
    >>> screener.run()
    """

    screeners: List[TickersScreener]
    recorder: TickersMarketRecorder

    COLUMNS = TickersMarketRecorder.COLUMNS

    def __init__(
            self,
            recorder: TickersMarketRecorder,
            screeners: Optional[Iterable[TickersScreener]] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            refresh: Optional[Union[float, dt.timedelta, bool]] = None,
            limited: Optional[bool] = None,
            handler: Optional[MarketHandler] = None,
            amount: Optional[int] = None,
            insert: Optional[bool] = None
    ) -> None:
        """
        Creates the class attributes.

        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param limited: The value to limit the screeners to active only.
        :param refresh: The refresh time for rerunning.
        :param handler: The handler object for the market data.
        :param amount: The maximum amount of symbols for each feed.
        :param recorder: The recorder object for recording the data.
        :param insert: The value to insert data into the market datasets.
        """

        super().__init__(
            location=location, cancel=cancel, amount=amount,
            delay=delay, recorder=recorder, insert=insert, refresh=refresh,
            screeners=screeners, handler=handler, limited=limited
        )
    # end __init__
# end MarketOrderbookScreener

def create_tickers_screeners(
        data: Dict[str, Iterable[str]],
        location: Optional[str] = None,
        memory: Optional[int] = None,
        cancel: Optional[Union[float, dt.timedelta]] = None,
        delay: Optional[Union[float, dt.timedelta]] = None,
) -> List[TickersScreener]:
    """
    Defines the class attributes.

    :param data: The data for the screeners.
    :param location: The saving location for the data.
    :param cancel: The time to cancel the waiting.
    :param delay: The delay for the process.
    :param memory: The memory limitation of the market dataset.
    """

    screeners = []

    for exchange, symbols in data.items():
        for symbol in symbols:
            screeners.append(
                TickersScreener(
                    symbol=symbol, exchange=exchange, delay=delay,
                    location=location, cancel=cancel, memory=memory
                )
            )
        # end for
    # end for

    return screeners
# end create_tickers_screeners

def tickers_market_screener(
        data: Dict[str, Iterable[str]],
        location: Optional[str] = None,
        cancel: Optional[Union[float, dt.timedelta]] = None,
        delay: Optional[Union[float, dt.timedelta]] = None,
        limited: Optional[bool] = None,
        handler: Optional[MarketHandler] = None,
        amount: Optional[int] = None,
        memory: Optional[int] = None,
        callbacks: Optional[Iterable[BaseCallback]] = None,
        refresh: Optional[Union[float, dt.timedelta, bool]] = None,
        recorder: Optional[TickersMarketRecorder] = None,
        insert: Optional[bool] = None
) -> TickersMarketScreener:
    """
    Creates the market screener object for the data.

    :param data: The market data.
    :param handler: The handler object for the market data.
    :param limited: The value to limit the screeners to active only.
    :param refresh: The refresh time for rerunning.
    :param amount: The maximum amount of symbols for each feed.
    :param recorder: The recorder object for recording the data.
    :param location: The saving location for the data.
    :param delay: The delay for the process.
    :param cancel: The cancel time for the loops.
    :param callbacks: The callbacks for the service.
    :param insert: The value to insert data into the market datasets.
    :param memory: The memory limitation of the market dataset.

    :return: The market screener object.
    """

    screeners = create_tickers_screeners(
        data=data, location=location,
        cancel=cancel, delay=delay, memory=memory
    )

    return TickersMarketScreener(
        recorder=recorder or TickersMarketRecorder(
            screeners=screeners, callbacks=callbacks, insert=insert
        ), screeners=screeners, insert=insert,
        handler=handler, location=location, amount=amount,
        cancel=cancel, delay=delay, limited=limited, refresh=refresh
    )
# end tickers_market_screener