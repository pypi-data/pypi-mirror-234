# screener.py

import os
import datetime as dt
from typing import Iterable, Optional, Dict, Union, Any, Set
import time

import pandas as pd

from represent import Modifiers

from market_break.dataset import (
    OHLCV_COLUMNS, load_dataset, save_dataset,
    ORDERBOOK_COLUMNS, create_dataset
)
from market_break.interval import validate_interval

from crypto_screening.dataset import (
    TICKERS_COLUMNS, TRADES_COLUMNS, bid_ask_to_ohlcv,
    bid_ask_to_tickers, trades_to_bid_ask, trades_to_tickers
)
from crypto_screening.symbols import adjust_symbol
from crypto_screening.validate import validate_exchange, validate_exchange_symbol
from crypto_screening.collect.symbols import all_exchange_symbols
from crypto_screening.foundation.state import WaitingState
from crypto_screening.foundation.data import DataCollector
from crypto_screening.foundation.protocols import BaseScreenerProtocol
from crypto_screening.foundation.waiting import (
    base_await_initialization, base_await_update, Condition
)

__all__ = [
    "BaseScreener",
    "OrderbookScreener",
    "TickersScreener",
    "OHLCVScreener",
    "TradesScreener"
]

class BaseScreener(DataCollector):
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
        The dataset of the market data.

    - memory:
        The memory size for the dataset.
    """

    __modifiers__ = Modifiers(properties=["symbol", "exchange"])

    MINIMUM_DELAY = 0.1

    NAME: Optional[str] = "BASE"
    COLUMNS: Iterable[str] = []

    SCREENER_NAME_TYPE_MATCHES: Dict[str, Set[Any]] = {}
    SCREENER_TYPE_NAME_MATCHES: Dict[Any, str] = {}

    __slots__ = "_saved", "_symbol", "_exchange", "_market", "memory"

    def __init__(
            self,
            symbol: str,
            exchange: str,
            memory: Optional[int] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            market: Optional[pd.DataFrame] = None,
    ) -> None:
        """
        Defines the class attributes.

        :param symbol: The symbol of the asset.
        :param exchange: The exchange to get source data from.
        :param location: The saving location for the data.
        :param memory: The memory limitation of the market dataset.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param market: The data for the market.
        """

        if not self.COLUMNS:
            raise ValueError(
                f"{repr(self)} must define a non-empty "
                f"'COLUMNS' instance or class attribute."
            )
        # end if

        super().__init__(location=location, cancel=cancel, delay=delay)

        self.register(name=self.NAME, base=type(self))

        self._exchange = self.validate_exchange(exchange=exchange)
        self._symbol = self.validate_exchange_symbol(
            exchange=self._exchange, symbol=symbol
        )
        self._market = self.validate_market(market=market)

        self.memory = memory

        self._saved = 0
    # end __init__

    @property
    def symbol(self) -> str:
        """
        Returns the property value.

        :return: The symbol.
        """

        return self._symbol
    # end symbol

    @property
    def exchange(self) -> str:
        """
        Returns the property value.

        :return: The exchange name.
        """

        return self._exchange
    # end exchange

    @property
    def market(self) -> pd.DataFrame:
        """
        Returns the property value.

        :return: The market dataset.
        """

        return self._market
    # end market

    @market.setter
    def market(self, value: pd.DataFrame) -> None:
        """
        Returns the property value.

        :return: The market dataset.
        """

        if not isinstance(value, pd.DataFrame):
            raise ValueError(
                f"Market dataset must be an instance of {pd.DataFrame}, "
                f"with matching columns to COLUMNS attribute."
            )
        # end if

        self._market = self.validate_market(value)
    # end market

    @staticmethod
    def validate_exchange(exchange: str) -> str:
        """
        Validates the symbol value.

        :param exchange: The exchange key.

        :return: The validates symbol.
        """

        return validate_exchange(exchange=exchange)
    # end validate_exchange

    @staticmethod
    def validate_exchange_symbol(exchange: str, symbol: Any) -> str:
        """
        Validates the symbol value.

        :param exchange: The exchange key.
        :param symbol: The key of the symbol.

        :return: The validates symbol.
        """

        return validate_exchange_symbol(
            exchange=exchange, symbol=symbol,
            symbols=all_exchange_symbols(exchange=exchange)
        )
    # end validate_exchange_symbol

    @classmethod
    def register(cls, name: str, base: Any) -> None:
        """
        Registers the base type as a screener type under the given name.

        :param name: The name for the type.
        :param base: The base type.
        """

        if name in cls.SCREENER_NAME_TYPE_MATCHES:
            first = list(cls.SCREENER_NAME_TYPE_MATCHES[name])[0]

            if not all(column in first.COLUMNS for column in base.COLUMNS):
                raise ValueError(
                    f"All market dataset columns of {base} {base.COLUMNS} "
                    f"must be inside the market dataset "
                    f"columns of {first} {first.COLUMNS}"
                )
                # end if
            # end for
        # end if

        cls.SCREENER_NAME_TYPE_MATCHES.setdefault(name, set()).add(base)
        cls.SCREENER_TYPE_NAME_MATCHES.setdefault(base, name)
    # end register

    def validate_market(self, market: Optional[Any] = None) -> pd.DataFrame:
        """
        Validates the value as a market dataset.

        :param market: The value to validate.

        :return: The valid value.
        """

        if market is None:
            market = create_dataset(self.COLUMNS)

        elif (
            (not isinstance(market, pd.DataFrame)) or
            (list(market.columns) != self.COLUMNS)
        ):
            raise ValueError(
                f"Market dataset must be an instance of {pd.DataFrame}, "
                f"with matching columns to COLUMNS attribute."
            )
        # end if

        return market
    # end validate_market

    def await_initialization(
            self,
            stop: Optional[Union[bool, int]] = False,
            delay: Optional[Union[float, dt.timedelta]] = None,
            cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
            condition: Optional[Condition] = None
    ) -> WaitingState[BaseScreenerProtocol]:
        """
        Waits for all the create_screeners to update.

        :param delay: The delay for the waiting.
        :param stop: The value to stop the screener objects.
        :param cancel: The time to cancel the waiting.
        :param condition: The condition to control the waiting outside the function.

        :returns: The total delay.
        """

        self: Union[BaseScreener, BaseScreenerProtocol]

        return base_await_initialization(
            self, stop=stop, delay=delay,
            cancel=cancel, condition=condition
        )
    # end await_initialization

    def await_update(
            self,
            stop: Optional[Union[bool, int]] = False,
            delay: Optional[Union[float, dt.timedelta]] = None,
            cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
            condition: Optional[Condition] = None
    ) -> WaitingState[BaseScreenerProtocol]:
        """
        Waits for all the create_screeners to update.

        :param delay: The delay for the waiting.
        :param stop: The value to stop the screener objects.
        :param cancel: The time to cancel the waiting.
        :param condition: The condition to control the waiting outside the function.

        :returns: The total delay.
        """

        self: Union[BaseScreener, BaseScreenerProtocol]

        return base_await_update(
            self, stop=stop, delay=delay,
            cancel=cancel, condition=condition
        )
    # end await_update

    def dataset_path(self, location: Optional[str] = None) -> str:
        """
        Creates the path to the saving file for the screener object.

        :param location: The saving location of the dataset.

        :return: The saving path for the dataset.
        """

        location = location or self.location

        if location is None:
            location = "."
        # end if

        return (
            f"{location}/"
            f"{self.exchange.lower()}/"
            f"{self.NAME}-"
            f"{adjust_symbol(self.symbol, separator='-')}.csv"
        )
    # end dataset_path

    def save_dataset(
            self,
            location: Optional[str] = None,
            append: Optional[bool] = True
    ) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        :param append: The value to append data to the file.
        """

        if len(self.market) == 0:
            return
        # end if

        path = self.dataset_path(location=location)

        if not os.path.exists(path):
            self._saved = 0
        # end if

        append = append and (not self.memory) and (self._saved > 5)

        if append:
            dataset = self.market.iloc[min(self._saved, len(self.market)):]

        else:
            dataset = self.market
        # end if

        save_dataset(
            dataset=dataset, append=append, path=path,
            headers=(not append) or (not self._saved)
        )

        if append:
            self._saved += len(dataset)
        # end if
    # end save_dataset

    def load_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        data = load_dataset(path=self.dataset_path(location=location))

        for index, data in zip(data.index[:], data.loc[:]):
            self.market.loc[index] = data
        # end for
    # end load_dataset

    def saving_loop(self) -> None:
        """Runs the process of the price screening."""

        self._saving = True

        while self.saving:
            delay = self.delay

            if isinstance(self.delay, dt.timedelta):
                delay = delay.total_seconds()
            # end if

            start = time.time()

            self.save_dataset()

            end = time.time()

            time.sleep(max(delay - (end - start), self.MINIMUM_DELAY))
        # end while
    # end saving_loop
# end BaseScreener

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