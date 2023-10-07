# screener.py

import os
import datetime as dt
from typing import Optional, Union

import pandas as pd

from crypto_screening.dataset import (
    OHLCV_COLUMNS, load_dataset, save_dataset,
    ORDERBOOK_COLUMNS, TICKERS_COLUMNS, TRADES_COLUMNS,
    bid_ask_to_ohlcv, bid_ask_to_tickers, trades_to_bid_ask,
    trades_to_tickers
)
from crypto_screening.interval import validate_interval
from crypto_screening.screeners.foundation.screener import BaseScreener

__all__ = [
    "BaseScreener",
    "OrderbookScreener",
    "TickersScreener",
    "OHLCVScreener",
    "TradesScreener"
]

class OrderbookScreener(BaseScreener):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - symbol:
        The symbol of an asset to screen.

    - exchange:
        The key of the exchange platform to screen data from.

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.

    - market:
        The dataset of the market data as BID/ASK spread.

    - memory:
        The memory size for the dataset.
    """

    NAME = "ORDERBOOK"

    COLUMNS = ORDERBOOK_COLUMNS

    __slots__ = ()

    @property
    def orderbook_market(self) -> pd.DataFrame:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.market
    # end orderbook_market

    def ohlcv_screener(self, interval: Optional[str] = None) -> "OHLCVScreener":
        """
        Creates the OHLCV screener object.

        :param interval: The interval to use for the data.

        :return: The OHLCV screener.
        """

        if interval is None:
            interval = "1m"
        # end if

        return OHLCVScreener(
            symbol=self.symbol, exchange=self.exchange, location=self.location,
            cancel=self.cancel, delay=self.delay, interval=interval,
            market=bid_ask_to_ohlcv(self.orderbook_market, interval=interval),
            orderbook_market=self.market
        )
    # end ohlcv_screener

    def tickers_screener(self) -> "TickersScreener":
        """
        Creates the tickers screener object.

        :return: The tickers' screener.
        """

        return TickersScreener(
            symbol=self.symbol, exchange=self.exchange, location=self.location,
            cancel=self.cancel, delay=self.delay,
            market=bid_ask_to_tickers(self.market)
        )
    # end tickers_screener
# end OrderbookScreener

class TickersScreener(BaseScreener):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - symbol:
        The symbol of an asset to screen.

    - exchange:
        The key of the exchange platform to screen data from.

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.

    - market:
        The dataset of the market data as orders.

    - memory:
        The memory size for the dataset.
    """

    NAME = "TICKERS"

    COLUMNS = TICKERS_COLUMNS

    __slots__ = ()

    @property
    def tickers_market(self) -> pd.DataFrame:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.market
    # end tickers_market
# end TickersScreener

class TradesScreener(BaseScreener):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - symbol:
        The symbol of an asset to screen.

    - exchange:
        The key of the exchange platform to screen data from.

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.

    - market:
        The dataset of the market data as trades.

    - memory:
        The memory size for the dataset.
    """

    NAME = "TRADES"

    COLUMNS = TRADES_COLUMNS

    __slots__ = ()

    @property
    def trades_market(self) -> pd.DataFrame:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.market
    # end trades_market

    def orderbook_screener(self) -> OrderbookScreener:
        """
        Creates the orderbook screener object.

        :return: The orderbook screener.
        """

        return OrderbookScreener(
            symbol=self.symbol, exchange=self.exchange, location=self.location,
            cancel=self.cancel, delay=self.delay,
            market=trades_to_bid_ask(self.market)
        )
    # end orderbook_screener

    def tickers_screener(self) -> "TickersScreener":
        """
        Creates the tickers screener object.

        :return: The tickers' screener.
        """

        return TickersScreener(
            symbol=self.symbol, exchange=self.exchange, location=self.location,
            cancel=self.cancel, delay=self.delay,
            market=trades_to_tickers(self.market)
        )
    # end tickers_screener
# end TradesScreener

class OHLCVScreener(BaseScreener):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - symbol:
        The symbol of an asset to screen.

    - exchange:
        The key of the exchange platform to screen data from.

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.

    - interval:
        The interval for the data structure of OHLCV.

    - market:
        The dataset of the market data as OHLCV.

    - orderbook_market:
        The dataset of the market data as BID/ASK spread.

    - memory:
        The memory size for the dataset.
    """

    INTERVAL = "1m"
    NAME = "OHLCV"

    COLUMNS = OHLCV_COLUMNS

    __slots__ = "_interval", "orderbook_market", "_saved_orderbook"

    def __init__(
            self,
            symbol: str,
            exchange: str,
            memory: Optional[int] = None,
            interval: Optional[str] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            market: Optional[pd.DataFrame] = None,
            orderbook_market: Optional[pd.DataFrame] = None
    ) -> None:
        """
        Defines the class attributes.

        :param symbol: The symbol of the asset.
        :param interval: The interval for the data.
        :param exchange: The exchange to get source data from.
        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param memory: The memory limitation of the market dataset.
        :param market: The data for the market.
        :param orderbook_market: The base market dataset.
        """

        super().__init__(
            symbol=symbol, exchange=exchange, location=location,
            cancel=cancel, delay=delay, market=market, memory=memory
        )

        self._interval = self.validate_interval(interval or self.INTERVAL)

        self.orderbook_market = orderbook_market

        self._saved_orderbook = 0
    # end __init__

    @staticmethod
    def validate_interval(interval: str) -> str:
        """
        Validates the symbol value.

        :param interval: The interval for the data.

        :return: The validates symbol.
        """

        return validate_interval(interval=interval)
    # end validate_interval

    @property
    def interval(self) -> str:
        """
        Returns the value of the interval of the market.

        :return: The market data interval.
        """

        return self._interval
    # end interval

    @property
    def ohlcv_market(self) -> pd.DataFrame:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.market
    # end ohlcv_market

    def orderbook_dataset_path(self, location: Optional[str] = None) -> str:
        """
        Creates the path to the saving file for the screener object.

        :param location: The saving location of the dataset.

        :return: The saving path for the dataset.
        """

        return (
            self.dataset_path(location=location).
            replace(self.NAME, OrderbookScreener.NAME)
        )
    # end orderbook_dataset_path

    def save_orderbook_dataset(
            self,
            location: Optional[str] = None,
            append: Optional[bool] = True
    ) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        :param append: The value to append data to the file.
        """

        market = self.orderbook_market

        if len(market) == 0:
            return
        # end if

        path = self.dataset_path(location=location)

        if not os.path.exists(path):
            self._saved_orderbook = 0
        # end if

        append = append and (not self.memory) and (self._saved_orderbook > 5)

        if append:
            dataset = market.iloc[min(self._saved_orderbook, len(market)):]

        else:
            dataset = market
        # end if

        save_dataset(
            dataset=dataset, append=append, path=path,
            headers=(not append) or (not self._saved_orderbook)
        )

        if append:
            self._saved_orderbook += len(dataset)
        # end if
    # end save_orderbook_dataset

    def ohlcv_dataset_path(self, location: Optional[str] = None) -> str:
        """
        Creates the path to the saving file for the screener object.

        :param location: The saving location of the dataset.

        :return: The saving path for the dataset.
        """

        return self.dataset_path(location=location)
    # end ohlcv_dataset_path

    def save_ohlcv_dataset(
            self,
            location: Optional[str] = None,
            append: Optional[bool] = True
    ) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        :param append: The value to append data to the file.
        """

        BaseScreener.save_dataset(self, location=location, append=append)
    # end save_ohlcv_dataset

    def save_datasets(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        self.save_ohlcv_dataset(location=location)
        self.save_orderbook_dataset(location=location)
    # end save_datasets

    def load_ohlcv_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        BaseScreener.load_dataset(self, location=location)
    # end load_ohlcv_dataset

    def load_orderbook_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        data = load_dataset(path=self.orderbook_dataset_path(location=location))

        for index, data in zip(data.index[:], data.loc[:]):
            self.orderbook_market.loc[index] = data
        # end for
    # end load_orderbook_dataset

    def load_datasets(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        self.load_ohlcv_dataset(location=location)
        self.load_orderbook_dataset(location=location)
    # end load_datasets

    def orderbook_screener(self) -> OrderbookScreener:
        """
        Creates the orderbook screener object.

        :return: The orderbook screener.
        """

        return OrderbookScreener(
            symbol=self.symbol, exchange=self.exchange, location=self.location,
            cancel=self.cancel, delay=self.delay, market=self.orderbook_market
        )
    # end orderbook_screener
# end OHLCVScreener