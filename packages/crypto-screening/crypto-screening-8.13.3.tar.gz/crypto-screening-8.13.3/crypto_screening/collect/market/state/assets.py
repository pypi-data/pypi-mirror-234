# assets.py

from abc import ABCMeta
import datetime as dt
from typing import (
    Iterable, Dict, Optional, Union,
    Any, List, Tuple, TypeVar, Type
)

from attrs import define

from represent import represent

import numpy as np
import pandas as pd

from market_break.dataset import index_to_datetime, create_dataset

from crypto_screening.foundation.screener import BaseScreener
from crypto_screening.symbols import symbol_to_parts, parts_to_symbol
from crypto_screening.collect.screeners import find_screeners
from crypto_screening.collect.market.state.base import (
    is_exchange_in_market_data, get_last_value, MarketState,
    dataset_to_data_rows, add_data_to_screeners, data_from_dataset,
    minimum_common_dataset_length, screener_dataset,
    add_data_to_symbols_screeners, adjusted_screener_dataset_length,
    sort_data, set_screener_dataset
)

__all__ = [
    "validate_assets_market_state_values_symbol",
    "assets_market_value",
    "is_symbol_in_assets_market_values",
    "assets_market_values",
    "assets_to_symbols_data",
    "assets_to_symbols_market_datasets",
    "assets_screeners",
    "assets_to_symbols_market_data",
    "add_assets_market_data_to_screeners",
    "merge_assets_market_data",
    "assets_datasets_to_assets_data",
    "screeners_to_assets_data",
    "assets_market_data",
    "assets_market_state_data",
    "merge_assets_market_states_data",
    "assets_to_symbols_screeners",
    "AssetsMarketState",
    "add_data_to_screeners",
    "sort_assets_market_data",
    "assets_market_datasets",
    "screeners_to_assets_datasets",
    "assets_market_datasets_to_screeners"
]

_V = TypeVar("_V")

Data = List[Tuple[dt.datetime, _V]]
AssetData = Data
AssetsData = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, _V]]]]]

def is_symbol_in_assets_market_values(
        exchange: str,
        symbol: str,
        data: AssetsData,
        separator: Optional[str] = None
) -> bool:
    """
    Checks if the symbol is in the values' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param data: The price data to process.
    :param separator: The separator of the assets.

    :return: The validation value.
    """

    if not is_exchange_in_market_data(exchange=exchange, values=data):
        return False
    # end if

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    if base not in data[exchange]:
        return False
    # end if

    if quote not in data[exchange][base]:
        return False
    # end if

    return not np.isnan(data[exchange][base][quote])
# end is_symbol_in_assets_market_prices

def validate_assets_market_state_values_symbol(
        exchange: str,
        symbol: str,
        data: AssetsData,
        separator: Optional[str] = None,
        provider: Optional[Any] = None
) -> None:
    """
    Checks if the symbol is in the values' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param separator: The separator of the assets.
    :param data: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    if exchange not in data:
        raise ValueError(
            f"exchange '{exchange}' is not found inside the values of"
            f"{f' of {repr(provider)}' if provider is not None else ''}. "
            f"Found exchanges for are: {', '.join(data.keys())}"
        )
    # end if

    if base not in data[exchange]:
        raise ValueError(
            f"base asset '{base}' is not found in '{exchange}' values of"
            f"{f' of {repr(provider)}' if provider is not None else ''}. "
            f"Found base '{exchange}' assets are: "
            f"{', '.join(data[exchange].keys())}"
        )
    # end if

    if quote not in data[exchange][base]:
        raise ValueError(
            f"quote asset '{quote}' is not found in the quote "
            f"assets of the '{base}' base asset in the values"
            f"{f' of {repr(provider)}' if provider is not None else ''}. "
            f"Found quote assets for the '{base}' base asset in "
            f"the values are: {', '.join(data[exchange][base].keys())}"
        )
    # end if
# end validate_assets_market_state_prices_symbol

def assets_market_values(
        exchange: str,
        symbol: str,
        data: AssetsData,
        separator: Optional[str] = None,
        provider: Optional[Any] = None
) -> List[Tuple[dt.datetime, _V]]:
    """
    Checks if the symbol is in the values' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param separator: The separator of the assets.
    :param data: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    validate_assets_market_state_values_symbol(
        symbol=symbol, data=data, exchange=exchange,
        separator=separator, provider=provider
    )

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    return data[exchange][base][quote]
# end assets_market_prices

def assets_market_value(
        exchange: str,
        symbol: str,
        data: AssetsData,
        separator: Optional[str] = None,
        provider: Optional[Any] = None
) -> Tuple[dt.datetime, _V]:
    """
    Checks if the symbol is in the values' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param separator: The separator of the assets.
    :param data: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    values = assets_market_values(
        symbol=symbol, data=data, exchange=exchange,
        separator=separator, provider=provider
    )

    return get_last_value(values)
# end assets_market_price

AssetsMarketData = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, Dict[str, _V]]]]]]

def assets_datasets_to_assets_data(
        datasets: Dict[str, Dict[str, Dict[str, pd.DataFrame]]]
) -> AssetsMarketData:
    """
    Converts the datasets structure to the structure of the data rows.

    :param datasets: The datasets to convert.

    :return: The new data.
    """

    return {
        exchange: {
            base: {
                quote: dataset_to_data_rows(dataset=dataset)
                for quote, dataset in quotes.items()
            } for base, quotes in bases.items()
        } for exchange, bases in datasets.items()
    }
# end assets_datasets_to_assets_data

def screeners_to_assets_datasets(
        screeners: Iterable[BaseScreener],
        separator: Optional[str] = None
) -> Dict[str, Dict[str, Dict[str, pd.DataFrame]]]:
    """
    Converts the datasets structure to the structure of the data rows.

    :param screeners: The screeners to process.
    :param separator: The separator for the symbols.

    :return: The new data.
    """

    results: Dict[str, Dict[str, Dict[str, pd.DataFrame]]] = {}

    for screener in screeners:
        base, quote = symbol_to_parts(screener.symbol, separator=separator)
        (
            results.
            setdefault(screener.exchange, {}).
            setdefault(base, {}).
            setdefault(quote, screener.market)
        )
    # end for

    return results
# end screeners_to_assets_datasets

def screeners_to_assets_data(
        screeners: Iterable[BaseScreener],
        separator: Optional[str] = None
) -> AssetsMarketData:
    """
    Converts the datasets structure to the structure of the data rows.

    :param screeners: The screeners to process.
    :param separator: The separator for the symbols.

    :return: The new data.
    """

    return assets_datasets_to_assets_data(
        screeners_to_assets_datasets(
            screeners=screeners, separator=separator
        )
    )
# end screeners_to_assets_data

def sort_assets_market_data(data: AssetsMarketData) -> None:
    """
    Sorts the data of the market.

    :param data: The data to sort.
    """

    for exchange, bases in data.items():
        for base, quotes in bases.items():
            for quote_data in quotes.values():
                sort_data(data=quote_data)
            # end for
        # end for
    # end for
# end sort_assets_market_data

def merge_assets_market_data(
        *data: AssetsMarketData, sort: Optional[bool] = True
) -> AssetsMarketData:
    """
    Concatenates the states of the market.

    :param data: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    new_data: AssetsMarketData = {}

    for data_packet in data:
        for exchange, bases in data_packet.items():
            for base, quotes in bases.items():
                for quote, prices in quotes.items():
                    (
                        new_data.setdefault(exchange, {}).
                        setdefault(base, {}).
                        setdefault(quote, []).
                        extend(prices)
                    )
                # end for
        # end for
    # end for

    if sort:
        sort_assets_market_data(data=new_data)
    # end if

    return new_data
# end merge_assets_ohlcv_market_states

SymbolsMarketDatasets = Dict[str, Dict[str, pd.DataFrame]]
AssetsMarketDatasets = Dict[str, Dict[str, Dict[str, pd.DataFrame]]]

def assets_to_symbols_market_datasets(
        datasets: AssetsMarketDatasets, separator: Optional[str] = None
) -> SymbolsMarketDatasets:
    """
    Converts the datasets structure from assets to symbols.

    :param datasets: The datasets to convert.
    :param separator: The separator for the symbols.

    :return: The result structure.
    """

    symbols_datasets: SymbolsMarketDatasets = {}

    for exchange, bases in datasets.items():
        for base, quotes in bases.items():
            for quote, dataset in quotes.items():
                symbol = parts_to_symbol(base, quote, separator=separator)
                (
                    symbols_datasets.
                    setdefault(exchange, {}).
                    setdefault(symbol, dataset)
                )
        # end for
    # end for

    return symbols_datasets
# end assets_to_symbols_market_datasets

SymbolData = List[Tuple[dt.datetime, _V]]
SymbolsData = Dict[str, Dict[str, SymbolData]]

def assets_to_symbols_data(
        data: AssetsData, separator: Optional[str] = None
) -> SymbolsData:
    """
    Converts an assets market values into a symbols market values.

    :param data: The source values.
    :param separator: The separator for the symbols.

    :return: The result values.
    """

    symbols_data: SymbolsData = {}

    for exchange, bases in data.items():
        for base, quotes in bases.items():
            for quote, quote_data in quotes.items():
                symbol = parts_to_symbol(base, quote, separator=separator)

                (
                    symbols_data.
                    setdefault(exchange, {}).
                    setdefault(symbol, []).
                    extend(quote_data)
                )
            # end for
        # end for
    # end for

    return symbols_data
# end assets_to_symbols_data

SymbolsMarketData = Dict[str, Dict[str, List[Tuple[dt.datetime, Dict[str, _V]]]]]

def assets_to_symbols_market_data(
        data: AssetsMarketData,
        separator: Optional[str] = None
) -> SymbolsMarketData:
    """
    Converts the structure of the market data from assets to symbols.

    :param data: The data to convert.
    :param separator: The separator for the symbols.

    :return: The data in the new structure
    """

    symbols_data: SymbolsMarketData = {}

    for exchange, bases in data.items():
        for base, quotes in bases.items():
            for quote, quote_data in quotes.items():
                symbol = parts_to_symbol(base, quote, separator=separator)

                (
                    symbols_data.
                    setdefault(exchange, {}).
                    setdefault(symbol, quote_data)
                )
            # end for
    # end for

    return symbols_data
# end assets_to_symbols_market_data

_S = TypeVar("_S")

AssetsScreeners = Dict[str, Dict[str, Dict[str, _S]]]

def assets_market_datasets_to_screeners(
        datasets: AssetsMarketDatasets,
        adjust: Optional[bool] = True,
        base: Optional[Type[_S]] = None,
        screeners: Optional[Iterable[_S]] = None,
        separator: Optional[str] = None
) -> AssetsScreeners:
    """
    Builds the screeners from the assets market datasets structure.

    :param datasets: The datasets for the screeners.
    :param adjust: The value to adjust the data.
    :param base: The base type for a screener.
    :param screeners: screeners to insert datasets into.
    :param separator: The symbols' separator.

    :return: The screeners.
    """

    if screeners is None:
        screeners = []
    # end if

    screener_base = base or BaseScreener

    new_screeners: AssetsScreeners = {}

    for exchange, bases in datasets.items():
        for base, quotes in bases.items():
            for quote, dataset in quotes.items():
                symbol = parts_to_symbol(base, quote, separator=separator)

                found_screeners = (
                    find_screeners(screeners, exchange=exchange, symbol=symbol) or
                    [screener_base(symbol=symbol, exchange=exchange)]
                )

                for screener in found_screeners:
                    set_screener_dataset(
                        screener=screener, dataset=dataset, adjust=adjust
                    )

                    (
                        new_screeners.setdefault(exchange, {}).
                        setdefault(base, {}).
                        setdefault(quote, screener)
                    )
                # end for
            # end for
    # end for

    return new_screeners
# end symbols_market_datasets_to_symbols_screeners

def assets_screeners(screeners: AssetsScreeners) -> List[Union[BaseScreener, _S]]:
    """
    Collects the screeners from the assets screeners structure.

    :param screeners: The screeners structure.

    :return: The screeners' collection.
    """

    screeners_collection = []

    for exchange, bases in screeners.items():
        for base, quotes in bases.items():
            for quote, screener in quotes.items():
                screeners_collection.append(screener)
            # end for
        # end for
    # end for

    return screeners_collection
# end assets_screeners

SymbolsScreeners = Dict[str, Dict[str, Union[BaseScreener, _S]]]

def assets_to_symbols_screeners(
        screeners: AssetsScreeners,
        separator: Optional[str] = None
) -> SymbolsScreeners:
    """
    Collects the screeners from the assets screeners structure.

    :param screeners: The screeners structure.
    :param separator: The separator for the symbols.

    :return: The screeners' collection.
    """

    data: SymbolsScreeners = {}

    for exchange, bases in screeners.items():
        for base, quotes in bases.items():
            for quote, screener in quotes.items():
                symbol = parts_to_symbol(base, quote, separator=separator)

                (
                    data.
                    setdefault(exchange, {}).
                    setdefault(symbol, screener)
                )
            # end for
        # end for
    # end for

    return data
# end assets_screeners

def add_assets_market_data_to_screeners(
        screeners: Iterable[BaseScreener],
        data: AssetsMarketData,
        separator: Optional[str] = None,
        adjust: Optional[bool] = True,
        force: Optional[bool] = False
) -> None:
    """
    Updates the data of the screeners with the symbols data.

    :param screeners: The screeners to update.
    :param data: The new data to add to the screeners.
    :param separator: The separator for the symbols.
    :param adjust: The value to adjust with screeners that are not found.
    :param force: The value to force the data into the screeners.
    """

    for exchange, bases in data.items():
        for base, quotes in bases.items():
            for quote, rows in quotes.items():
                symbol = parts_to_symbol(base, quote, separator=separator)

                add_data_to_symbols_screeners(
                    symbol=symbol, exchange=exchange,
                    screeners=screeners, data=rows,
                    force=force, adjust=adjust
                )
            # end for
        # end for
    # end for
# end add_assets_data_to_screeners

def assets_market_data(
        columns: Dict[str, str],
        data: Optional[Dict[str, AssetsData]] = None,
        sort: Optional[bool] = True
) -> AssetsMarketData:
    """
    Returns the structured data of the state.

    :param data: The values for the data collection.
    :param columns: The columns for the data.
    :param sort: The value to sort the data.

    :return: The data of the state.
    """

    data = data or {name: {} for name in columns}

    datasets: Dict[str, Dict[str, Dict[str, Dict[dt.datetime, Dict[str, _V]]]]] = {}

    for name, column in columns.items():
        for exchange, bases in data[name].items():
            for base, quotes in bases.items():
                for quote, quote_data in quotes.items():
                    for index, value in quote_data:
                        (
                            datasets.
                            setdefault(exchange, {}).
                            setdefault(base, {}).
                            setdefault(quote, {}).
                            setdefault(index_to_datetime(index), {}).
                            setdefault(column, value)
                        )
                    # end for
            # end for
        # end for
    # end for

    new_datasets: AssetsMarketData = {}

    for exchange, bases in datasets.items():
        for base, quotes in bases.items():
            for quote, quote_data in quotes.items():
                quote_data = list(quote_data.items())

                (
                    new_datasets.
                    setdefault(exchange, {}).
                    setdefault(base, {}).
                    setdefault(quote, quote_data)
                )

                if sort:
                    sort_data(data=quote_data)
                # end if
            # end for
        # end for
    # end for

    return new_datasets
# end assets_market_data

def assets_market_datasets(
        columns: Dict[str, str],
        data: Optional[Dict[str, AssetsData]] = None,
        sort: Optional[bool] = True
) -> AssetsMarketDatasets:
    """
    Returns the structured data of the state.

    :param data: The values for the data collection.
    :param columns: The columns for the data.
    :param sort: The value to sort the data.

    :return: The data of the state.
    """

    datasets: AssetsMarketDatasets = {}

    data = assets_market_data(columns=columns, data=data, sort=sort)

    for exchange, bases in data.items():
        for base, quotes in bases.items():
            for quote, rows in quotes.items():
                dataset = create_dataset(columns=columns)

                for index, row in rows:
                    dataset.loc[index] = row
                # end for
            # end for
        # end for
    # end for

    return datasets
# end assets_market_datasets

def assets_market_state_data(
        columns: Dict[str, str],
        screeners: Iterable[BaseScreener],
        data: Optional[Dict[str, AssetsData]] = None,
        separator: Optional[str] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> Dict[str, AssetsData]:
    """
    Fetches the values and relations between the assets.

    :param data: The values for the data collection.
    :param columns: The columns for the data.
    :param screeners: The price screeners.
    :param separator: The separator of the assets.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    data = data or {name: {} for name in columns}

    if (length is None) and (not adjust):
        length = minimum_common_dataset_length(
            columns=columns, screeners=screeners
        )
    # end if

    for screener in screeners:
        market = screener_dataset(columns=columns, screener=screener)

        length = adjusted_screener_dataset_length(
            screener=screener, dataset=market,
            adjust=adjust, length=length
        )

        base, quote = symbol_to_parts(
            symbol=screener.symbol, separator=separator
        )

        for name, column in columns.items():
            attribute_data = data_from_dataset(
                dataset=market, column=column,
                adjust=adjust, length=length
            )

            (
                data[name].
                setdefault(screener.exchange, {}).
                setdefault(base, {}).
                setdefault(quote, attribute_data)
            )
    # end for

    return data
# end assets_market_state

def merge_assets_market_states_data(
        states: Iterable[MarketState],
        data: Dict[str, AssetsData],
        sort: Optional[bool] = True
) -> Dict[str, AssetsData]:
    """
    Concatenates the states of the market.

    :param data: The values for the data collection.
    :param states: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    for state in states:
        for name in data:
            for exchange, bases in getattr(state, name).items():
                for base, quotes in bases.items():
                    for quote, quote_data in quotes.items():
                        (
                            data[name].setdefault(exchange, {}).
                            setdefault(base, {}).
                            setdefault(quote, []).
                            extend(quote_data)
                        )
                # end for
            # end for
        # end for
    # end for

    if sort:
        for attribute_data in data.values():
            sort_assets_market_data(data=attribute_data)
        # end for
    # end if

    return data
# end merge_assets_market_states

@define(repr=False)
@represent
class AssetsMarketState(MarketState, metaclass=ABCMeta):
    """
    A class to represent the current market state.

    This class is a base class for containers of structured market data,
    with assets structure.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.
    """

    def data(self) -> AssetsMarketData:
        """
        Returns the structured data of the state.

        :return: The data of the state.
        """

        return assets_market_data(
            columns=self.ATTRIBUTES,
            data={name: getattr(self, name) for name in self.ATTRIBUTES}
        )
    # end data

    def datasets(self) -> AssetsMarketDatasets:
        """
        Rebuilds the dataset from the market state.

        :return: The dataset of the state data.
        """

        return assets_market_datasets(
            columns=self.ATTRIBUTES,
            data={name: getattr(self, name) for name in self.ATTRIBUTES}
        )
    # end assets_market_state_to_datasets
# end AssetsMarketState