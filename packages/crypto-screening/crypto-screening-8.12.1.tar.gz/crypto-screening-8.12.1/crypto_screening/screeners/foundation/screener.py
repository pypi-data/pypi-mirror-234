# screener.py

import os
import datetime as dt
from typing import Iterable, Optional, Dict, Union, Any, Set
import time

import pandas as pd

from represent import Modifiers

from crypto_screening.dataset import save_dataset, load_dataset, create_dataset
from crypto_screening.symbols import adjust_symbol
from crypto_screening.validate import validate_exchange, validate_exchange_symbol
from crypto_screening.collect.symbols import all_exchange_symbols
from crypto_screening.screeners.foundation.state import WaitingState
from crypto_screening.screeners.foundation.data import DataCollector
from crypto_screening.screeners.foundation.protocols import BaseScreenerProtocol
from crypto_screening.screeners.foundation.waiting import (
    base_await_initialization, base_await_update, Condition
)

__all__ = [
    "BaseScreener"
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