# base.py

from abc import ABCMeta
import datetime as dt
from typing import (
    Iterable, Dict, Optional, Reversible,
    Any, ClassVar, List, Tuple, TypeVar
)

from attrs import define

from represent import represent, Modifiers

import pandas as pd

from market_break.dataset import (
    BIDS, ASKS, BIDS_VOLUME, ASKS_VOLUME, bid_ask_to_ohlcv,
    dataset_to_json, index_to_datetime
)

from crypto_screening.foundation.screener import (
    BaseScreener, TradesScreener, OrderbookScreener,
    OHLCVScreener, TickersScreener
)
from crypto_screening.collect.screeners import find_screeners

__all__ = [
    "is_exchange_in_market_data",
    "dataset_to_data_rows",
    "MarketState",
    "ORDERBOOK_ATTRIBUTES",
    "add_data_to_symbols_screeners",
    "add_data_to_screeners",
    "adjusted_dataset_length",
    "set_screener_dataset",
    "is_match",
    "screener_dataset",
    "get_last_value",
    "no_match_error",
    "is_ohlcv_orderbook_match",
    "minimum_common_dataset_length",
    "data_from_dataset",
    "adjusted_screener_dataset_length",
    "sort_data",
    "validate_market_state_attributes",
    "is_valid_state_attributes"
]

_V = TypeVar("_V")

Data = List[Tuple[dt.datetime, _V]]

def data_from_dataset(
        dataset: pd.DataFrame,
        column: str,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> Data:
    """
    Gets the data of the column from the dataset.

    :param dataset: The dataset to extract data from.
    :param column: The name of the data column.
    :param length: The length of data to extract.
    :param adjust: The value to adjust the length of the data.

    :return: The data of the column from the dataset in the right length.
    """

    length = adjusted_dataset_length(
        dataset=dataset, adjust=adjust, length=length
    )

    return list(
        zip(
            list(dataset.index[-length:]),
            list(dataset[column][-length:])
        )
    )
# end data_from_dataset

def is_exchange_in_market_data(exchange: str, values: Dict[str, Any]) -> None:
    """
    Checks if the exchange is in the values.

    :param exchange: The exchange name.
    :param values: The values.

    :return: The boolean flag.
    """

    return exchange not in values
# end is_exchange_in_market_prices

def get_last_value(values: Reversible[_V]) -> _V:
    """
    Gets the last value from the iterable.

    :param values: The values to extract the last from.

    :return: The last value.
    """

    for data in reversed(values):
        return data
    # end for

    raise ValueError(
        f"Cannot get the last value from an "
        f"empty datastructure: {values}"
    )
# end get_last_value

@define(repr=False)
@represent
class MarketState(metaclass=ABCMeta):
    """
    A class to represent the current market state.

    This class is a base class for containers of structured market data,
    with assets structure or symbols structure.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.
    """

    screeners: Iterable[BaseScreener]

    __modifiers__: ClassVar[Modifiers] = Modifiers(hidden=["screeners"])

    ATTRIBUTES: ClassVar[Dict[str, str]]

    def __hash__(self) -> int:
        """
        Returns the hash of the object.

        :return: The hash of the object.
        """

        return id(self)
    # end __hash__

    def __attrs_post_init__(self) -> None:
        """Defines the class attributes."""

        self.validate_market_state_attributes()

    # end __init__

    def validate_market_state_attributes(self) -> None:
        """Validates the market state's attributes."""

        validate_market_state_attributes(self)
    # end validate_market_state_attributes
# end MarketState

def validate_market_state_attributes(state: MarketState) -> None:
    """
    Validates the market state's attributes.

    :param state: The market state object.
    """

    if not hasattr(state, "ATTRIBUTES"):
        raise ValueError(
            f"'ATTRIBUTES' instance or class attribute "
            f"must be defined for: {repr(state)}"
        )

    elif not (
        isinstance(state.ATTRIBUTES, dict) and
        all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in state.ATTRIBUTES.items()
        )
    ):
        raise ValueError(
            f"'ATTRIBUTES' must de of type: {Dict[str, str]}, "
            f"not: {state.ATTRIBUTES}"
        )
    # end if

    missing = [
        attribute for attribute in state.ATTRIBUTES
        if not hasattr(state, attribute)
    ]

    if missing:
        raise ValueError(
            f"{repr(state)} must contain all attributes defined in "
            f"'ATTRIBUTES': {state.ATTRIBUTES}. "
            f"Missing attributes: {', '.join(missing)}"
        )
    # end if
# end validate_market_state_attributes

def is_valid_state_attributes(state: MarketState) -> bool:
    """
    Validates the market state's attributes.

    :param state: The market state object.

    :return: The value of validation.
    """

    try:
        validate_market_state_attributes(state)

        return True

    except ValueError:
        return False
    # end if
# end is_valid_state_attributes

def sort_data(data: Data) -> None:
    """
    Sorts the data of the market.

    :param data: The data to sort.
    """

    data.sort(key=lambda pair: pair[0])
# end sort_data

def dataset_to_data_rows(dataset: pd.DataFrame) -> List[Tuple[dt.datetime, Dict[str, Any]]]:
    """
    Converts the dataset into the data of the rows.

    :param dataset: The dataset.

    :return: The data structure.
    """

    data = dataset_to_json(dataset)

    return [
        (index_to_datetime(index), value)
        for index, (_, value) in zip(dataset.index, data)
    ]
# end dataset_to_data

_S = TypeVar(
    "_S",
    BaseScreener,
    OrderbookScreener,
    OHLCVScreener,
    TickersScreener,
    TradesScreener
)

ORDERBOOK_ATTRIBUTES = {
    "bids": BIDS,
    "asks": ASKS,
    "bids_volume": BIDS_VOLUME,
    "asks_volume": ASKS_VOLUME
}

def is_match(screener: BaseScreener, columns: Iterable[str]) -> bool:
    """
    Checks if the screener matches the columns of the data.

    :param screener: The screener object.
    :param columns: The columns.

    :return: The matching boolean flag.
    """

    return set(screener.market.columns) == set(columns)
# end is_match

def is_ohlcv_orderbook_match(screener: BaseScreener, columns: Iterable[str]) -> bool:
    """
    Checks if the screener matches the columns of the data.

    :param screener: The screener object.
    :param columns: The columns.

    :return: The matching boolean flag.
    """

    return (
        isinstance(screener, OHLCVScreener) and
        (set(columns) == set(ORDERBOOK_ATTRIBUTES.values()))
    )
# end is_ohlcv_orderbook_match

def no_match_error(screener: BaseScreener, columns: Iterable[str]) -> ValueError:
    """
    Checks if the screener matches the columns of the data.

    :param screener: The screener object.
    :param columns: The columns.

    :return: The matching boolean flag.
    """

    return ValueError(
        f"Unable to set dataset with columns: "
        f"{', '.join(set(columns))} to {type(screener)} object of "
        f"'{screener.exchange}' and symbol "
        f"'{screener.symbol}' to update its data. "
        f"Consider setting the 'adjust' parameter to {True}, ignore."
    )
# end no_match_error

def set_screener_dataset(
        screener: _S,
        dataset: pd.DataFrame,
        clean: Optional[bool] = False,
        replace: Optional[bool] = False,
        force: Optional[bool] = False,
        adjust: Optional[bool] = False
) -> None:
    """
    Sets the dataset for the screener, and return the screener.

    :param dataset: The dataset to insert to the screener.
    :param screener: The screener object.
    :param clean: The value to clean the dataset.
    :param replace: The value to replace the dataset.
    :param force: The value to force the dataset into the screener.
    :param adjust: The value to adjust when the data doesn't fit to the screener.

    :return: The screener object.
    """

    if is_ohlcv_orderbook_match(screener=screener, columns=dataset.columns):
        spread_dataset = dataset

        if isinstance(screener.orderbook_market, pd.DataFrame) and clean:
            screener.orderbook_market.drop(screener.orderbook_market.index, inplace=True)
        # end if

        if (screener.orderbook_market is None) or replace:
            screener.orderbook_market = spread_dataset

        else:
            for index, row in spread_dataset.iterrows():
                screener.orderbook_market[index] = row
            # end for
        # end if

        if isinstance(screener.market, pd.DataFrame) and clean:
            screener.market.drop(screener.market.index, inplace=True)
        # end if

        ohlcv_dataset = bid_ask_to_ohlcv(spread_dataset, interval=screener.interval)

        if (screener.market is None) or replace:
            screener.market = ohlcv_dataset

        else:
            for index, row in ohlcv_dataset:
                screener.market[index] = row
            # end for
        # end if

    elif not (force or is_match(screener=screener, columns=dataset.columns)):
        if not adjust:
            raise no_match_error(screener=screener, columns=dataset.columns)
        # end if

    else:
        if isinstance(screener.market, pd.DataFrame) and clean:
            screener.market.drop(screener.market.index, inplace=True)
        # end if

        if (screener.market is None) or replace:
            screener.market = dataset

        else:
            for index, row in dataset:
                screener.market[index] = row
            # end for
        # end if
    # end if
# end set_screener_dataset

def add_data_to_symbols_screeners(
        symbol: str,
        exchange: str,
        screeners: Iterable[BaseScreener],
        data: Data,
        adjust: Optional[bool] = True,
        force: Optional[bool] = False
) -> None:
    """
    Updates the data of the screeners with the symbols data.

    :param exchange: The xchange of the screeners.
    :param symbol: The symbol of the screeners.
    :param screeners: The screeners to update.
    :param data: The new data to add to the screeners.
    :param adjust: The value to adjust with screeners that are not found.
    :param force: The value to force the data into the screeners.
    """

    found_screeners = find_screeners(
        screeners, exchange=exchange, symbol=symbol
    )

    if (not found_screeners) and (not adjust):
        raise ValueError(
            f"Unable to find screeners with exchange "
            f"'{exchange}' and symbol '{symbol}' to update its data. "
            f"Consider setting the 'adjust' parameter to True, ignore."
        )
    # end if

    add_data_to_screeners(
        screeners=found_screeners, data=data,
        force=force, adjust=adjust
    )
# end add_data_to_symbols_screeners

def add_data_to_screeners(
        screeners: Iterable[BaseScreener],
        data: Data,
        adjust: Optional[bool] = True,
        force: Optional[bool] = False
) -> None:
    """
    Updates the data of the screeners with the symbols data.

    :param screeners: The screeners to update.
    :param data: The new data to add to the screeners.
    :param adjust: The value to adjust with screeners that are not found.
    :param force: The value to force the data into the screeners.
    """

    for screener in screeners:
        for index, row in data:
            if is_ohlcv_orderbook_match(screener=screener, columns=row.keys()):
                screener: OHLCVScreener

                screener.orderbook_market.loc[index] = row

            elif not (force or is_match(screener=screener, columns=row.keys())):
                if not adjust:
                    raise no_match_error(screener=screener, columns=row.keys())
                # end if

            else:
                screener.market.loc[index] = row
            # end if
        # end for
    # end for
# end add_data_to_screeners

def screener_dataset(
        columns: Dict[str, str], screener: BaseScreener
) -> pd.DataFrame:
    """
    Finds the minimum common length of all datasets.

    :param columns: The columns for the data.
    :param screener: The price screener.

    :return: The minimum common length.
    """

    return (
        screener.orderbook_market
        if (
            (columns == ORDERBOOK_ATTRIBUTES) and
            isinstance(screener, OHLCVScreener)
        ) else
        screener.market
    )
# end screener_dataset

def minimum_common_dataset_length(
        columns: Dict[str, str], screeners: Iterable[BaseScreener]
) -> int:
    """
    Finds the minimum common length of all datasets.

    :param columns: The columns for the data.
    :param screeners: The price screeners.

    :return: The minimum common length.
    """

    return min(
        [
            len(screener_dataset(columns=columns, screener=screener))
            for screener in screeners
        ]
    )
# end minimum_common_dataset_length

def adjusted_dataset_length(
        dataset: pd.DataFrame,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> int:
    """
    Finds the minimum common length of all datasets.

    :param dataset: The price dataset.
    :param length: The base length.
    :param adjust: The value to adjust the length.

    :return: The minimum common length.
    """

    if adjust and (length is None):
        length = len(dataset)

    elif adjust:
        length = min([len(dataset), length])
    # end if

    if length > len(dataset):
        raise ValueError(
            f"Data is not long enough for the requested length: {length}. "
            f"Consider using the 'adjust' parameter as {True}, "
            f"to adjust to the actual length of the data."
        )
    # end if

    return length
# end adjusted_dataset_length

def adjusted_screener_dataset_length(
        screener: BaseScreener,
        dataset: pd.DataFrame,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> int:
    """
    Finds the minimum common length of all datasets.

    :param screener: The screener object.
    :param dataset: The price dataset.
    :param length: The base length.
    :param adjust: The value to adjust the length.

    :return: The minimum common length.
    """

    try:
        return adjusted_dataset_length(
            dataset=dataset, adjust=adjust, length=length
        )

    except ValueError as e:
        raise ValueError(
            f"Data of '{screener.exchange}' "
            f"symbol in '{screener.symbol}' exchange: {e}"
        )
    # end try
# end adjusted_screener_dataset_length