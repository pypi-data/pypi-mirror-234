# container.py

from typing import Iterable, List, Type, TypeVar, Optional, Dict, Set


from represent import represent

from crypto_screening.foundation.screener import BaseScreener, OHLCVScreener

__all__ = [
    "BaseScreener",
    "BaseScreenersContainer",
    "screeners_table",
    "BaseFrozenScreenersContainer"
]

_S = TypeVar("_S")

ScreenersTable = Dict[
    Optional[Type[BaseScreener]],
    Dict[
        Optional[str],
        Dict[Optional[str], Dict[Optional[str], Set[BaseScreener]]]
    ]
]

def screeners_table(
        screeners: Iterable[BaseScreener],
        table: Optional[ScreenersTable] = None
) -> ScreenersTable:
    """
    Inserts all the screeners into the table.

    :param screeners: The screeners to insert into the table.
    :param table: The table to use for the data.

    :return: The screeners table.
    """

    if table is None:
        table = {}
    # end if

    if not isinstance(screeners, set):
        screeners = set(screeners)
    # end if

    for screener in screeners:
        lists = []

        for interval in {
            (
                screener.interval
                if isinstance(screener, OHLCVScreener) else None
            ), None
        }:
            lists.extend(
                [
                    (
                        table.
                        setdefault(type(screener), {}).
                        setdefault(screener.exchange, {}).
                        setdefault(screener.symbol, {}).
                        setdefault(interval, set())
                    ),
                    (
                        table.
                        setdefault(None, {}).
                        setdefault(screener.exchange, {}).
                        setdefault(screener.symbol, {}).
                        setdefault(interval, set())
                    ),
                    (
                        table.
                        setdefault(type(screener), {}).
                        setdefault(None, {}).
                        setdefault(screener.symbol, {}).
                        setdefault(interval, set())
                    ),
                    (
                        table.
                        setdefault(type(screener), {}).
                        setdefault(screener.exchange, {}).
                        setdefault(None, {}).
                        setdefault(interval, set())
                    ),
                    (
                        table.
                        setdefault(None, {}).
                        setdefault(None, {}).
                        setdefault(screener.symbol, {}).
                        setdefault(interval, set())
                    ),
                    (
                        table.
                        setdefault(None, {}).
                        setdefault(screener.exchange, {}).
                        setdefault(None, {}).
                        setdefault(interval, set())
                    ),
                    (
                        table.
                        setdefault(type(screener), {}).
                        setdefault(None, {}).
                        setdefault(None, {}).
                        setdefault(interval, set())
                    ),
                    (
                        table.
                        setdefault(None, {}).
                        setdefault(None, {}).
                        setdefault(None, {}).
                        setdefault(interval, set())
                    )
                ]
            )
        # end for

        for screeners_list in lists:
            screeners_list.add(screener)
        # end for
    # end for

    return table
# end screeners_table

@represent
class BaseFrozenScreenersContainer:
    """
    A class to represent a multi-exchange multi-pairs crypto data screener.
    Using this class enables extracting screener objects and screeners
    data by the exchange name and the symbol of the pair.

    parameters:

    - screeners:
        The screener objects to form a market.

    >>> from crypto_screening.foundation.container import (
    >>>     BaseFrozenScreenersContainer, BaseScreener
    >>> )
    >>>
    >>> container = BaseFrozenScreenersContainer(
    >>>     screeners=[BaseScreener(exchange="binance", symbol="BTC/USDT")]
    >>> )
    """

    def __init__(self, screeners: Iterable[BaseScreener]) -> None:
        """
        Defines the class attributes.

        :param screeners: The data screener object.
        """

        screeners = set(screeners)

        self._screeners = list(screeners)

        self._table = screeners_table(screeners)
    # end __init__

    @property
    def screeners(self) -> List[BaseScreener]:
        """
        Returns a list of all the screeners.

        :return: The screeners.
        """

        return list(self._screeners)
    # end screeners

    def structure(self) -> Dict[str, List[str]]:
        """
        Returns the structure of the market data.

        :return: The structure of the market.
        """

        return {
            exchange: [symbol for symbol in symbols if symbol is not None]
            for exchange, symbols in self._table[None].items()
            if exchange is not None
        }
    # end structure

    def map(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Returns the structure of the market data.

        :return: The structure of the market.
        """

        return {
            exchange: {
                symbol: [interval for interval in intervals if interval is not None]
                for symbol, intervals in symbols.items() if symbol is not None
            }
            for exchange, symbols in self._table[None].items()
            if exchange is not None
        }
    # end map

    def table(self) -> Dict[str, Dict[str, Dict[str, Set[BaseScreener]]]]:
        """
        Returns the structure of the market data.

        :return: The structure of the market.
        """

        return {
            exchange: {
                symbol: {
                    interval: set(screeners)
                    for interval, screeners in intervals.items() if interval is not None
                } for symbol, intervals in symbols.items() if symbol is not None
            } for exchange, symbols in self._table[None].items()
            if exchange is not None
        }
    # end table

    def find_screeners(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            base: Optional[Type[_S]] = None,
            interval: Optional[str] = None,
            adjust: Optional[bool] = True
    ) -> List[_S]:
        """
        Returns the data by according to the parameters.

        :param base: The base type of the screener.
        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param interval: The interval for the search.
        :param adjust: The value to adjust for the screeners.

        :return: The data.
        """

        try:
            return list(self._table[base][exchange][symbol][interval])

        except KeyError:
            if not adjust:
                raise ValueError(
                    f"Cannot find screeners  matching to "
                    f"type - {base}, exchange - {exchange}, "
                    f"symbol - {symbol}, interval - {interval} "
                    f"inside {repr(self)}"
                )
            # end if
        # end try

        return []
    # end find_screeners

    def find_screener(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            base: Optional[Type[_S]] = None,
            interval: Optional[str] = None,
            index: Optional[int] = None,
            adjust: Optional[bool] = False
    ) -> _S:
        """
        Returns the data by according to the parameters.

        :param base: The base type of the screener.
        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param interval: The interval for the search.
        :param index: The index of the screener in the list.
        :param adjust: The value to adjust for the screeners.

        :return: The data.
        """

        try:
            return self.find_screeners(
                exchange=exchange, symbol=symbol,
                base=base, interval=interval, adjust=adjust
            )[index or 0]

        except IndexError:
            if not adjust:
                raise IndexError(
                    f"Cannot find screeners matching to "
                    f"type - {base}, exchange - {exchange}, "
                    f"symbol - {symbol}, interval - {interval}, "
                    f"index - {index} inside {repr(self)}"
                )
            # end if
        # end try
    # end find_orderbook_screener

    def screener_in_market(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            base: Optional[Type[_S]] = None,
            interval: Optional[str] = None
    ) -> bool:
        """
        Returns the data by according to the parameters.

        :param base: The base type of the screener.
        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param interval: The interval to search.

        :return: The data.
        """

        try:
            self.find_screener(
                exchange=exchange, symbol=symbol,
                base=base, interval=interval
            )

            return True

        except ValueError:
            return False
        # end try
    # end screener_in_market
# end MappedScreenersContainer

@represent
class BaseScreenersContainer(BaseFrozenScreenersContainer):
    """
    A class to represent a multi-exchange multi-pairs crypto data screener.
    Using this class enables extracting screener objects and screeners
    data by the exchange name and the symbol of the pair.

    parameters:

    - screeners:
        The screener objects to form a market.

    >>> container = BaseScreenersContainer(
    >>>     screeners=[BaseScreener(exchange="binance", symbol="BTC/USDT")]
    >>> )
    """

    def update_screeners(self) -> None:
        """Updates the records of the object."""
    # end update_screeners

    def add(
            self,
            screeners: Iterable[BaseScreener],
            adjust: Optional[bool] = True,
            update: Optional[bool] = True
    ) -> None:
        """
        Updates the data with the new screeners.

        :param screeners: The new screeners to add.
        :param adjust: The value to adjust for screeners.
        :param update: The value to update.
        """

        existing_screeners = set(self._screeners)

        new_screeners = set()

        for screener in screeners:
            if screener not in existing_screeners:
                new_screeners.add(screener)

            elif not adjust:
                raise ValueError(
                    f"Cannot add screener {repr(screener)} to "
                    f"{repr(self)} because it is already present."
                )
            # end if
        # end for

        self._screeners.extend(new_screeners)

        screeners_table(new_screeners, table=self._table)

        if update:
            self.update_screeners()
        # end if
    # end add

    def remove(
            self,
            screeners: Iterable[BaseScreener],
            adjust: Optional[bool] = True,
            update: Optional[bool] = True
    ) -> None:
        """
        Updates the data with the new screeners.

        :param screeners: The new screeners to add.
        :param adjust: The value to adjust for screeners.
        :param update: The value to update.
        """

        existing_screeners = set(self._screeners)

        for screener in screeners:
            if screener in existing_screeners:
                self._screeners.remove(screener)

            elif not adjust:
                raise ValueError(
                    f"Cannot remove screener {repr(screener)} from "
                    f"{repr(self)} because it is not present."
                )
            # end if
        # end for

        self._table.clear()

        screeners_table(self._screeners, table=self._table)

        if update:
            self.update_screeners()
        # end if
    # end remove

    def clear(self, update: Optional[bool] = True) -> None:
        """
        clears the screeners from the container.

        :param update: The value to update.
        """

        self._table.clear()
        self._screeners.clear()

        if update:
            self.update_screeners()
        # end if
    # end clear
# end BaseScreenersContainer