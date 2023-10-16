# screeners.py

from typing import (
    Optional, Dict, Iterable, TypeVar,
    Set, Union, Tuple, Type, List
)

from attrs import define

import pandas as pd

from crypto_screening.symbols import symbol_to_parts
from crypto_screening.utils.process import string_in_values
from crypto_screening.collect.symbols import (
    matching_symbol_pair, MarketSymbolSignature, exchanges_symbols
)
from crypto_screening.foundation.screener import BaseScreener
from crypto_screening.foundation.market import BaseMarketScreener
from crypto_screening.foundation.screener import OHLCVScreener

__all__ = [
    "matching_screener_signatures",
    "matching_screener_pair",
    "matching_screener_pairs",
    "MarketScreenerSignature",
    "find_screeners",
    "running_nonempty_screeners",
    "remove_empty_screeners",
    "structure_exchanges_symbols",
    "structure_exchanges_symbols_screeners",
    "structure_exchanges_symbols_screener",
    "gather_screeners",
    "exchanges_symbols_screeners",
    "structure_exchanges_assets_screener",
    "structure_exchanges_assets_screeners",
    "structure_exchanges_symbols_dataset",
    "structure_exchanges_symbols_datasets",
    "nonempty_screeners",
    "running_screeners",
    "find_screener",
    "structure_exchanges_assets_datasets",
    "structure_exchanges_assets_dataset",
    "structure_exchanges_assets",
    "deconstruct_screeners_structure",
    "structure_exchanges_assets_sorted_screeners",
    "structure_exchanges_symbols_sorted_screeners"
]

AssetMatches = Iterable[Iterable[str]]

def matching_screener_pair(
        screener1: BaseScreener,
        screener2: BaseScreener, /, *,
        matches: Optional[AssetMatches] = None,
        separator: Optional[str] = None
) -> bool:
    """
    Checks if the symbols are valid with the matching currencies.

    :param screener1: The first ticker.
    :param screener2: The second ticker.
    :param matches: The currencies.
    :param separator: The separator of the assets.

    :return: The validation value for the symbols.
    """

    return (
        (screener1.exchange != screener2.exchange) and
        matching_symbol_pair(
            screener1.symbol, screener2.symbol,
            matches=matches, separator=separator
        )
    )
# end matching_screener_pair

ExchangesAssetMatches = Union[Dict[Iterable[str], AssetMatches], AssetMatches]

def matching_screener_pairs(
        screeners: Iterable[BaseScreener],
        matches: Optional[ExchangesAssetMatches] = None,
        separator: Optional[str] = None,
        empty: Optional[bool] = True
) -> Set[Tuple[BaseScreener, BaseScreener]]:
    """
    Checks if the screeners are valid with the matching currencies.

    :param screeners: The screeners.
    :param matches: The currencies.
    :param separator: The separator of the assets.
    :param empty: Allows empty screeners.

    :return: The validation value for the symbols.
    """

    pairs: Set[Tuple[BaseScreener, BaseScreener]] = set()

    if not empty:
        screeners = remove_empty_screeners(screeners=screeners)
    # end if

    for screener1 in screeners:
        for screener2 in screeners:
            exchanges_matches = (
                matches
                if not isinstance(matches, dict) else
                [
                    *matches.get(screener1.exchange, []),
                    *matches.get(screener2.exchange, [])
                ]
            )

            if matching_screener_pair(
                screener1, screener2,
                matches=exchanges_matches or None,
                separator=separator
            ):
                pairs.add((screener1, screener2))
            # end if
        # end for
    # end for

    return set(pairs)
# end matching_screener_pairs

@define(init=False, repr=False, slots=False, eq=False, unsafe_hash=True)
class MarketScreenerSignature(MarketSymbolSignature):
    """A class to represent the data for the execution of a trade."""

    __slots__ = "screener",

    def __init__(
            self,
            exchange: str,
            base: str,
            quote: str,
            screener: Optional[BaseScreener] = None,
            separator: Optional[str] = None
    ) -> None:
        """
        Defines the class attributes.

        :param exchange: The exchange name.
        :param base: The base asset.
        :param quote: The quote asset.
        :param screener: The screener object.
        """

        super().__init__(
            exchange=exchange, base=base,
            quote=quote, separator=separator
        )

        self.screener = screener
    # end __init__
# end MarketScreenerSignature

def matching_screener_signatures(
        data: Optional[Set[Tuple[BaseScreener, BaseScreener]]] = None,
        screeners: Optional[Iterable[BaseScreener]] = None,
        matches: Optional[ExchangesAssetMatches] = None,
        separator: Optional[str] = None,
        empty: Optional[bool] = True
) -> Set[Tuple[MarketScreenerSignature, MarketScreenerSignature]]:
    """
    Checks if the screeners are valid with the matching currencies.

    :param data: The data for the pairs.
    :param screeners: The screeners.
    :param matches: The currencies.
    :param separator: The separator of the assets.
    :param empty: Allows empty screeners.

    :return: The validation value for the symbols.
    """

    if (data is None) and (screeners is None):
        raise ValueError(
            f"One of 'screeners' and 'data' parameters must be given, "
            f"when 'data' is superior to 'screeners'."
        )

    elif (not screeners) and (not data):
        return set()
    # end if

    pairs: Set[Tuple[MarketScreenerSignature, MarketScreenerSignature]] = set()

    data = data or matching_screener_pairs(
        screeners=screeners, matches=matches,
        separator=separator, empty=empty
    )

    for screener1, screener2 in data:
        asset1, currency1 = symbol_to_parts(screener1.symbol)
        asset2, currency2 = symbol_to_parts(screener2.symbol)

        pairs.add(
            (
                MarketScreenerSignature(
                    base=asset1, quote=currency1,
                    exchange=screener1.exchange,
                    screener=screener1
                ),
                MarketScreenerSignature(
                    base=asset2, quote=currency2,
                    exchange=screener2.exchange,
                    screener=screener2
                )
            )
        )
    # end for

    return set(pairs)
# end matching_screener_signatures

def nonempty_screeners(
        screeners: Iterable[Union[BaseScreener, BaseMarketScreener]]
) -> Set[Union[BaseScreener, BaseMarketScreener]]:
    """
    Returns a list of all the live create_screeners.

    :param screeners: The create_screeners to search from.

    :return: A list the live create_screeners.
    """

    return {
        screener for screener in screeners
        if (
            (
                isinstance(screener, BaseMarketScreener) and
                nonempty_screeners(screener.screeners)
            ) or
            (
                (len(screener.market) > 0) and
                isinstance(screener, BaseScreener)
            )
        )
    }
# end nonempty_screeners

def running_nonempty_screeners(
        screeners: Iterable[Union[BaseScreener, BaseMarketScreener]]
) -> Set[Union[BaseScreener, BaseMarketScreener]]:
    """
    Returns a list of all the live create_screeners.

    :param screeners: The create_screeners to search from.

    :return: A list the live create_screeners.
    """

    return {
        screener for screener in screeners
        if (
            (
                isinstance(screener, BaseMarketScreener) and
                running_nonempty_screeners(screener.screeners)
            ) or
            (
                screener.screening and
                (len(screener.market) > 0) and
                isinstance(screener, BaseScreener)
            )
        )
    }
# end running_nonempty_screeners

def running_screeners(
        screeners: Iterable[Union[BaseScreener, BaseMarketScreener]]
) -> Set[Union[BaseScreener, BaseMarketScreener]]:
    """
    Returns a list of all the live create_screeners.

    :param screeners: The create_screeners to search from.

    :return: A list the live create_screeners.
    """

    return {
        screener for screener in screeners
        if (
            (
                isinstance(screener, BaseMarketScreener) and
                running_screeners(screener.screeners)
            ) or
            (
                screener.screening and
                isinstance(screener, BaseScreener)
            )
        )
    }
# end running_screeners

_S = TypeVar("_S")

def find_screeners(
        screeners: Iterable[_S],
        base: Optional[Type[_S]] = None,
        exchange: Optional[str] = None,
        symbol: Optional[str] = None,
        interval: Optional[str] = None
) -> List[_S]:
    """
    Finds all the screeners with the matching exchange and symbol key.

    :param screeners: The screeners to process.
    :param base: The base type for the screeners.
    :param exchange: The exchange key for the symbol.
    :param symbol: The pair symbol to search its screeners.
    :param interval: The interval of the screener.

    :return: The matching screeners.
    """

    return [
        screener for screener in screeners
        if (
            ((base is None) or (isinstance(screener, base))) and
            ((symbol is None) or (screener.symbol.lower() == symbol.lower())) and
            ((exchange is None) or (exchange.lower() == screener.exchange.lower())) and
            (
                (interval is None) or
                (
                    isinstance(screener, OHLCVScreener) and
                    (screener.interval.lower() == interval.lower())
                )
            )
        )
    ]
# end find_screeners

def find_screener(
        screeners: Iterable[_S],
        base: Optional[Type[_S]] = None,
        exchange: Optional[str] = None,
        symbol: Optional[str] = None,
        interval: Optional[str] = None,
        index: Optional[int] = None
) -> _S:
    """
    Finds all the screeners with the matching exchange and symbol key.

    :param screeners: The screeners to process.
    :param base: The base type for the screeners.
    :param exchange: The exchange key for the symbol.
    :param symbol: The pair symbol to search its screeners.
    :param interval: The interval of the screener.
    :param index: The index for the screener.

    :return: The matching screeners.
    """

    found_screeners = find_screeners(
        screeners=screeners, base=base, exchange=exchange,
        symbol=symbol, interval=interval
    )

    if not found_screeners:
        raise ValueError(
            f"Cannot find screeners  matching to "
            f"type - {base}, exchange - {exchange}, "
            f"symbol - {symbol}, interval - {interval}."
        )
    # end if

    try:
        return found_screeners[index or 0]

    except IndexError:
        raise IndexError(
            f"Cannot find screeners matching to "
            f"type - {base}, exchange - {exchange}, "
            f"symbol - {symbol}, interval - {interval}, "
            f"index - {index}."
        )
    # end try
# end find_screeners

def remove_empty_screeners(screeners: Iterable[BaseScreener]) -> Set[BaseScreener]:
    """
    Removes the empty screeners.

    :param screeners: The screeners of the assets and exchanges.
    """

    return {
        screener for screener in screeners
        if len(screener.market) > 0
    }
# end remove_empty_screeners

def gather_screeners(
        screeners: Iterable[Union[BaseScreener, BaseMarketScreener]]
) -> Set[BaseScreener]:
    """
    Gathers the base screeners.

    :param screeners: The screeners to process.

    :return: The gathered base screeners.
    """

    checked_screeners: Set[BaseScreener] = set()

    for screener in screeners:
        if isinstance(screener, BaseScreener):
            checked_screeners.add(screener)

        elif isinstance(screener, BaseMarketScreener):
            checked_screeners.update(screener.screeners)
        # end if
    # end for

    return checked_screeners
# end gather_screeners

def exchanges_symbols_screeners(
        screeners: Iterable[BaseScreener],
        exchanges: Optional[Iterable[str]] = None,
        adjust: Optional[bool] = True,
        separator: Optional[str] = None,
        bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
) -> Set[BaseScreener]:
    """
    Collects the symbols from the exchanges.

    :param screeners: The screeners to collect.
    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded symbols.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param included: The symbols to include.
    :param bases: The bases of the asset pairs.

    :return: The data of the exchanges.
    """

    if exchanges is None:
        exchanges = {screener.exchange for screener in screeners}
    # end if

    if (not screeners) or (not exchanges):
        return set()
    # end if

    found_exchanges_symbols = exchanges_symbols(
        exchanges=set(exchanges), adjust=adjust, separator=separator,
        bases=bases, quotes=quotes, included=included, excluded=excluded
    )

    return {
        screener for screener in screeners
        if (
            string_in_values(
                value=screener.exchange, values=found_exchanges_symbols
            )
            and
            string_in_values(
                value=screener.symbol,
                values=found_exchanges_symbols[screener.exchange]
            )
        )
    }
# end exchanges_symbols_screeners

def structure_exchanges_symbols(screeners: Iterable[BaseScreener]) -> Dict[str, Set[str]]:
    """
    Collects the structure of the screeners exchanges and symbols.

    :param screeners: The screeners to process.

    :return: The collected structure of exchanges and symbols.
    """

    data: Dict[str, Set[str]] = {}

    for screener in screeners:
        data.setdefault(screener.exchange, set()).add(screener.symbol)
    # end for

    return data
# end structure_exchanges_symbols

def structure_exchanges_assets(
        screeners: Iterable[BaseScreener],
        separator: Optional[str] = None
) -> Dict[str, Dict[str, Set[str]]]:
    """
    Collects the structure of the screeners exchanges and symbols.

    :param screeners: The screeners to process.
    :param separator: The separator for the symbols.

    :return: The collected structure of exchanges and symbols.
    """

    data: Dict[str, Dict[str, Set[str]]] = {}

    for screener in screeners:
        base, quote = symbol_to_parts(screener.symbol, separator=separator)
        (
            data.
            setdefault(screener.exchange, {}).
            setdefault(base, set()).
            add(quote)
        )
    # end for

    return data
# end structure_exchanges_symbols

def structure_exchanges_symbols_screeners(
        screeners: Iterable[BaseScreener]
) -> Dict[str, Dict[str, Set[BaseScreener]]]:
    """
    Structures the screener objects by exchanges and symbols

    :param screeners: The screeners to structure.

    :return: The structure of the screeners.
    """

    structure: Dict[str, Dict[str, Set[BaseScreener]]] = {}

    for screener in screeners:
        (
            structure.
            setdefault(screener.exchange, {}).
            setdefault(screener.symbol, set())
        ).add(screener)
    # end for

    return structure
# end structure_exchanges_symbols_screeners

def structure_exchanges_symbols_sorted_screeners(
        screeners: Iterable[BaseScreener],
        types: Iterable[Type[BaseScreener]],
        amount: Optional[int] = None,
        adjust: Optional[bool] = True
) -> Dict[str, Dict[str, List[BaseScreener]]]:
    """
    Structures the screener objects by exchanges and symbols

    :param screeners: The screeners to structure.
    :param types: The order of types of screeners.
    :param amount: The amount of screeners in each sort.
    :param adjust: The value to adjust for amounts inconsistency.

    :return: The structure of the screeners.
    """

    types = list(types)

    if amount > len(types):
        raise ValueError(
            f"Amount must be less than or equal "
            f"to the length of types, with is "
            f"{len(types)}, but got amount {amount}."
        )
    # end if

    structure: Dict[str, Dict[str, List[BaseScreener]]] = {}

    collections = []

    for screener in screeners:
        if type(screener) not in types:
            continue
        # end if

        collection = (
            structure.
            setdefault(screener.exchange, {}).
            setdefault(screener.symbol, [])
        )
        collections.append(collection)
        collection.append(screener)
    # end for

    for collection in collections:
        if (not adjust) and (len(collections) < amount):
            raise ValueError(
                f"Not enough screeners of exchange: "
                f"{collection[0].exchange} and symbol: "
                f"{collection[0].symbol}, and types: "
                f"{', '.join(t.__name__ for t in types)} "
                f"to reach the amount of {amount}. "
                f"Consider setting the 'adjust' parameter to True."
            )
        # end if

        collection.sort(key=lambda s: types.index(type(s)))

        for _ in range(len(collection) - amount):
            collection.pop(-1)
        # end for
    # end if

    return structure
# end structure_exchanges_symbols_screeners

def structure_exchanges_assets_sorted_screeners(
        screeners: Iterable[BaseScreener],
        types: Iterable[Type[BaseScreener]],
        separator: Optional[str] = None,
        amount: Optional[int] = None,
        adjust: Optional[bool] = True
) -> Dict[str, Dict[str, Dict[str, List[BaseScreener]]]]:
    """
    Structures the screener objects by exchanges and symbols

    :param screeners: The screeners to structure.
    :param types: The order of types of screeners.
    :param separator: The separator for the symbols.
    :param amount: The amount of screeners in each sort.
    :param adjust: The value to adjust for amounts inconsistency.

    :return: The structure of the screeners.
    """

    types = list(types)

    if amount > len(types):
        raise ValueError(
            f"Amount must be less than or equal "
            f"to the length of types, with is "
            f"{len(types)}, but got amount {amount}."
        )
    # end if

    structure: Dict[str, Dict[str, Dict[str, List[BaseScreener]]]] = {}

    collections = []

    for screener in screeners:
        if type(screener) not in types:
            continue
        # end if

        base, quote = symbol_to_parts(screener.symbol, separator=separator)

        collection = (
            structure.
            setdefault(screener.exchange, {}).
            setdefault(base, {}).
            setdefault(quote, [])
        )
        collections.append(collection)
        collection.append(screener)
    # end for

    for collection in collections:
        if (not adjust) and (len(collections) < amount):
            raise ValueError(
                f"Not enough screeners of exchange: "
                f"{collection[0].exchange} and symbol: "
                f"{collection[0].symbol}, and types: "
                f"{', '.join(t.__name__ for t in types)} "
                f"to reach the amount of {amount}. "
                f"Consider setting the 'adjust' parameter to True."
            )
        # end if

        collection.sort(key=lambda s: types.index(type(s)))

        for _ in range(len(collection) - amount):
            collection.pop(-1)
        # end for
    # end if

    return structure
# end structure_exchanges_symbols_screeners

def structure_exchanges_symbols_screener(
        screeners: Iterable[BaseScreener]
) -> Dict[str, Dict[str, BaseScreener]]:
    """
    Structures the screener objects by exchanges and symbols

    :param screeners: The screeners to structure.

    :return: The structure of the screeners.
    """

    structure: Dict[str, Dict[str, BaseScreener]] = {}

    for screener in screeners:
        (
            structure.
            setdefault(screener.exchange, {}).
            setdefault(screener.symbol, screener)
        )
    # end for

    return structure
# end structure_exchanges_symbols_screener

def structure_exchanges_assets_screeners(
        screeners: Iterable[BaseScreener],
        separator: Optional[str] = None
) -> Dict[str, Dict[str, Dict[str, Set[BaseScreener]]]]:
    """
    Converts the datasets structure to the structure of the data rows.

    :param screeners: The screeners to process.
    :param separator: The separator for the symbols.

    :return: The new data.
    """

    results: Dict[str, Dict[str, Dict[str, Set[BaseScreener]]]] = {}

    for screener in screeners:
        base, quote = symbol_to_parts(screener.symbol, separator=separator)
        (
            results.
            setdefault(screener.exchange, {}).
            setdefault(base, {}).
            setdefault(quote, set()).
            add(screener)
        )
    # end for

    return results
# end structure_exchanges_assets_screeners

def structure_exchanges_assets_screener(
        screeners: Iterable[BaseScreener],
        separator: Optional[str] = None
) -> Dict[str, Dict[str, Dict[str, BaseScreener]]]:
    """
    Converts the datasets structure to the structure of the data rows.

    :param screeners: The screeners to process.
    :param separator: The separator for the symbols.

    :return: The new data.
    """

    results: Dict[str, Dict[str, Dict[str, BaseScreener]]] = {}

    for screener in screeners:
        base, quote = symbol_to_parts(screener.symbol, separator=separator)
        (
            results.
            setdefault(screener.exchange, {}).
            setdefault(base, {}).
            setdefault(quote, screener)
        )
    # end for

    return results
# end structure_exchanges_assets_screeners

def structure_exchanges_symbols_datasets(
        screeners: Iterable[BaseScreener]
) -> Dict[str, Dict[str, Set[pd.DataFrame]]]:
    """
    Converts the datasets structure to the structure of the data rows.

    :param screeners: The screeners to process.

    :return: The new data.
    """

    results: Dict[str, Dict[str, Set[pd.DataFrame]]] = {}

    for screener in screeners:
        (
            results.
            setdefault(screener.exchange, {}).
            setdefault(screener.symbol, set()).
            add(screener.market)
        )
    # end for

    return results
# end structure_exchanges_symbols_datasets

def structure_exchanges_symbols_dataset(
        screeners: Iterable[BaseScreener]
) -> Dict[str, Dict[str, pd.DataFrame]]:
    """
    Converts the datasets structure to the structure of the data rows.

    :param screeners: The screeners to process.

    :return: The new data.
    """

    results: Dict[str, Dict[str, pd.DataFrame]] = {}

    for screener in screeners:
        (
            results.
            setdefault(screener.exchange, {}).
            setdefault(screener.symbol, screener.market)
        )
    # end for

    return results
# end structure_exchanges_symbols_dataset

def structure_exchanges_assets_datasets(
        screeners: Iterable[BaseScreener],
        separator: Optional[str] = None
) -> Dict[str, Dict[str, Dict[str, Set[pd.DataFrame]]]]:
    """
    Converts the datasets structure to the structure of the data rows.

    :param screeners: The screeners to process.
    :param separator: The separator for the symbols.

    :return: The new data.
    """

    results: Dict[str, Dict[str, Dict[str, Set[pd.DataFrame]]]] = {}

    for screener in screeners:
        base, quote = symbol_to_parts(screener.symbol, separator=separator)
        (
            results.
            setdefault(screener.exchange, {}).
            setdefault(base, {}).
            setdefault(quote, set()).
            add(screener.market)
        )
    # end for

    return results
# end structure_exchanges_symbols_dataset

def structure_exchanges_assets_dataset(
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
# end structure_exchanges_assets_datasets

def deconstruct_screeners_structure(
        structure: Union[BaseScreener, Tuple, List, Set, Dict],
        screeners: Optional[Set[BaseScreener]] = None
) -> Set[BaseScreener]:
    """
    Collects all screeners from the structure.

    :param structure: The structure to collect screeners from.
    :param screeners: The screeners' collection.

    :return: The collected screeners.
    """

    if screeners is None:
        screeners = set()
    # end if

    if isinstance(structure, BaseScreener):
        screeners.add(structure)

    elif isinstance(structure, (tuple, list, set)):
        for value in structure:
            if isinstance(value, BaseScreener):
                screeners.add(value)

            else:
                deconstruct_screeners_structure(value, screeners=screeners)
            # end if
        # end for

    elif isinstance(structure, dict):
        for key, value in structure.items():
            if isinstance(key, BaseScreener):
                screeners.add(key)

            else:
                deconstruct_screeners_structure(key, screeners=screeners)
            # end if

            if isinstance(value, BaseScreener):
                screeners.add(value)

            else:
                deconstruct_screeners_structure(value, screeners=screeners)
            # end if
        # end for
    # end if

    return screeners
# end deconstruct_screeners_structure