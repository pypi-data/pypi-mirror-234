# symbols.py

import warnings
from typing import (
    Optional, Dict, Iterable, Set, Union, Tuple, Any, ClassVar
)

from attrs import define

from represent import Modifiers

from multithreading import Caller, multi_threaded_call

from crypto_screening.utils.process import (
    find_string_value, upper_string_values,
    mutual_string_values, string_in_values
)
from crypto_screening.exchanges import (
    EXCHANGES, EXCHANGE_NAMES, BUILTIN_EXCHANGES_SYMBOLS
)
from crypto_screening.symbols import (
    symbol_to_parts, adjust_symbol, Separator, Pair
)
from crypto_screening.validate import validate_exchange
from crypto_screening.collect.foundation.exchanges import exchanges_data

__all__ = [
    "exchanges_symbols",
    "mutual_exchanges_symbols",
    "include_symbols",
    "exclude_symbols",
    "exchange_symbols",
    "all_exchange_symbols",
    "matching_symbol_pair",
    "matching_symbol_pairs",
    "MarketSymbolSignature",
    "matching_symbol_signatures",
    "include_exchanges_symbols",
    "exclude_exchanges_symbols",
    "all_exchanges_symbols",
    "select_exchanges_symbols"
]

def include_symbols(
        symbols: Iterable[str],
        separator: Optional[str] = None,
        adjust: Optional[bool] = True,
        bases: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        included: Optional[Iterable[str]] = None
) -> Set[str]:
    """
    Removes all symbols with not matching base or quote.

    :param symbols: The symbols to filter.
    :param separator: The separator for the symbols.
    :param bases: The bases to include.
    :param adjust: The value to adjust the invalid exchanges.
    :param quotes: The quotes to include.
    :param included: The symbols to include.

    :return: The filtered symbols.
    """

    saved = set()

    quotes = upper_string_values(quotes or [])
    bases = upper_string_values(bases or [])
    included = upper_string_values(included or [])

    for symbol in symbols:
        if symbol in included:
            saved.add(symbol)

            continue
        # end if

        try:
            symbol = adjust_symbol(symbol=symbol, separator=separator)

        except ValueError as e:
            if adjust:
                continue

            else:
                raise e
            # end if
        # end try

        if symbol in included:
            saved.add(symbol)

            continue
        # end if

        base, quote = symbol_to_parts(
            symbol=symbol, separator=separator
        )

        if (
            string_in_values(value=base, values=bases) or
            string_in_values(value=quote, values=quotes)
        ):
            saved.add(symbol)
        # end if
    # end for

    return saved
# end include_symbols

def exclude_symbols(
        symbols: Iterable[str],
        separator: Optional[str] = None,
        adjust: Optional[bool] = True,
        bases: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Iterable[str]] = None
) -> Set[str]:
    """
    Removes all symbols with the matching base or quote.

    :param symbols: The symbols to filter.
    :param separator: The separator for the symbols.
    :param bases: The bases to exclude.
    :param quotes: The quotes to exclude.
    :param adjust: The value to adjust the invalid exchanges.
    :param excluded: The symbols to exclude.

    :return: The filtered symbols.
    """

    saved = set()

    quotes = upper_string_values(quotes or [])
    bases = upper_string_values(bases or [])
    excluded = upper_string_values(excluded or [])

    for symbol in symbols:
        if symbol in excluded:
            continue
        # end if

        try:
            symbol = adjust_symbol(symbol=symbol, separator=separator)

        except ValueError as e:
            if adjust:
                continue

            else:
                raise e
            # end if
        # end try

        if symbol in excluded:
            continue
        # end if

        base, quote = symbol_to_parts(symbol=symbol, separator=separator)

        if (
            string_in_values(value=base, values=bases) or
            string_in_values(value=quote, values=quotes)
        ):
            continue
        # end if

        saved.add(symbol)
    # end for

    return set(saved)
# end exclude_symbols

def include_exchanges_symbols(
        data: Dict[str, Iterable[str]],
        bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
) -> Dict[str, Set[str]]:
    """
    Removes all symbols with not matching base or quote.

    :param data: The data to filter.
    :param bases: The bases to include.
    :param quotes: The quotes to include.
    :param included: The symbols to include.

    :return: The filtered symbols.
    """

    if all(value is None for value in (bases, quotes, included)):
        return {exchange: set(symbols) for exchange, symbols in data.items()}
    # end if

    if not isinstance(quotes, dict):
        saved_quotes = quotes
        quotes = {exchange: saved_quotes for exchange in data}
    # end if

    if not isinstance(bases, dict):
        saved_bases = bases
        bases = {exchange: saved_bases for exchange in data}
    # end if

    if not isinstance(included, dict):
        saved_included = included
        included = {exchange: saved_included for exchange in data}
    # end if

    return {
        exchange: saved for exchange, symbols in data.items()
        if (
            saved := include_symbols(
                symbols=symbols,
                bases=bases.get(exchange, None),
                quotes=quotes.get(exchange, None),
                included=included.get(exchange, None)
            )
        )
    }
# end include_exchanges_symbols

def exclude_exchanges_symbols(
        data: Dict[str, Iterable[str]],
        bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
) -> Dict[str, Set[str]]:
    """
    Removes all symbols with the matching base or quote.

    :param data: The data to filter.
    :param bases: The bases to exclude.
    :param quotes: The quotes to exclude.
    :param excluded: The symbols to exclude.

    :return: The filtered symbols.
    """

    if all(value is None for value in (bases, quotes, excluded)):
        return {exchange: set(symbols) for exchange, symbols in data.items()}
    # end if

    if not isinstance(quotes, dict):
        saved_quotes = quotes
        quotes = {exchange: saved_quotes for exchange in data}
    # end if

    if not isinstance(bases, dict):
        saved_bases = bases
        bases = {exchange: saved_bases for exchange in data}
    # end if

    if not isinstance(excluded, dict):
        saved_excluded = excluded
        excluded = {exchange: saved_excluded for exchange in data}
    # end if

    return {
        exchange: saved for exchange, symbols in data.items()
        if (
            saved := exclude_symbols(
                symbols=symbols,
                bases=bases.get(exchange, None),
                quotes=quotes.get(exchange, None),
                excluded=excluded.get(exchange, None)
            )
        )
    }
# end exclude_exchanges_symbols

def all_exchange_symbols(
        exchange: str,
        separator: Optional[str] = None,
        adjust: Optional[bool] = True,
        test: Optional[bool] = False
) -> Set[str]:
    """
    Collects the symbols from the exchanges.

    :param exchange: The name of the exchange.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param test: Include test assets.

    :return: The data of the exchanges.
    """

    validate_exchange(exchange=exchange, exchanges=EXCHANGE_NAMES)

    try:
        found_symbols: Iterable[str] = EXCHANGES[
            find_string_value(value=exchange, values=EXCHANGES)
        ].symbols()

    except Exception as e:
        error_message = (
            f"Cannot fetch symbols of '{exchange}' exchange: {str(e)}."
        )

        if not adjust:
            raise RuntimeError(error_message)

        else:
            warnings.warn(error_message)

            return set()
        # end if
    # end try

    symbols = set()

    if separator is None:
        separator = Separator.value
    # end if

    for symbol in found_symbols:
        try:
            symbol = adjust_symbol(symbol=symbol, separator=separator)

            if symbol.count(separator) != 1:
                raise ValueError(
                    f"Invalid symbol structure: {symbol}. "
                    f"Symbol must contain only one separator."
                )
            # end if

        except ValueError as e:
            if adjust:
                continue

            else:
                raise e
            # end if
        # end try

        base, quote = symbol_to_parts(symbol=symbol, separator=separator)

        if (not test) and base.startswith("TEST") and quote.startswith("TEST"):
            continue
        # end if

        symbols.add(symbol)
    # end for

    return symbols
# end all_exchange_symbols

def all_exchanges_symbols(
        exchanges: Iterable[str],
        separator: Optional[str] = None,
        adjust: Optional[bool] = True,
        test: Optional[bool] = False
) -> Dict[str, Set[str]]:
    """
    Collects the symbols from the exchanges.

    :param exchanges: The name of the exchange.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param test: Include test assets.

    :return: The data of the exchanges.
    """

    results = multi_threaded_call(
        [
            Caller(
                target=all_exchange_symbols, kwargs=dict(
                    exchange=exchange, separator=separator,
                    adjust=adjust, test=test
                ), identifier=exchange
            ) for exchange in exchanges
        ]
    )

    return {
        exchange: results.result(exchange).returns
        for exchange in exchanges
    }
# end all_exchanges_symbols

def exchange_symbols(
        exchange: Optional[str] = None,
        separator: Optional[str] = None,
        adjust: Optional[bool] = True,
        bases: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        included: Optional[Iterable[str]] = None,
        excluded: Optional[Iterable[str]] = None
) -> Set[str]:
    """
    Collects the symbols from the exchanges.

    :param exchange: The name of the exchange.
    :param quotes: The quotes of the asset pairs.
    :param adjust: The value to adjust the invalid exchanges.
    :param bases: The bases of the asset pairs.
    :param separator: The separator of the assets.
    :param included: The symbols to include.
    :param excluded: The excluded symbols.

    :return: The data of the exchanges.
    """

    symbols = all_exchange_symbols(
        exchange=exchange, adjust=adjust, separator=separator
    )

    symbols = (
        symbols if all(value is None for value in (included, bases, quotes)) else
        include_symbols(
            symbols=symbols, included=included,
            bases=bases, quotes=quotes, separator=separator
        )
    )

    return symbols if excluded is None else exclude_symbols(
        symbols=symbols, excluded=excluded, separator=separator, adjust=adjust
    )
# end exchange_symbols

def exchanges_symbols(
        exchanges: Optional[Iterable[str]] = None,
        adjust: Optional[bool] = True,
        separator: Optional[str] = None,
        bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
) -> Dict[str, Set[str]]:
    """
    Collects the symbols from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded symbols.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param included: The symbols to include.
    :param bases: The bases of the asset pairs.

    :return: The data of the exchanges.
    """

    return exchanges_data(
        collector=exchange_symbols,
        exchanges=exchanges, quotes=quotes, excluded=excluded,
        adjust=adjust, separator=separator, included=included, bases=bases
    )
# end exchanges_symbols

def select_exchanges_symbols(
        data: Optional[Dict[str, Iterable[str]]] = None,
        exchanges: Optional[Iterable[str]] = None,
        bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
) -> Dict[str, Set[str]]:
    """
    Collects the symbols from the exchanges.

    :param data: The exchanges.
    :param exchanges: The exchange names to keep.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded symbols.
    :param included: The symbols to include.
    :param bases: The bases of the asset pairs.

    :return: The data of the exchanges.
    """

    if data is None:
        data = BUILTIN_EXCHANGES_SYMBOLS
    # end if

    if exchanges is not None:
        data = {
            exchange: symbols for exchange, symbols in data.items()
            if exchange in exchanges
        }
    # end if

    if bases is not None:
        data = include_exchanges_symbols(
            data=data, bases=bases
        )
    # end if

    if quotes is not None:
        data = include_exchanges_symbols(
            data=data, quotes=quotes
        )
    # end if

    if excluded is not None:
        data = exclude_exchanges_symbols(
            data=data, excluded=excluded
        )
    # end if

    if included is not None:
        data = exclude_exchanges_symbols(
            data=data, excluded=included
        )
    # end if

    return data
# end select_exchanges_symbols

def mutual_exchanges_symbols(
        exchanges: Optional[Iterable[str]] = None,
        adjust: Optional[bool] = True,
        separator: Optional[str] = None,
        bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        data: Optional[Dict[str, Iterable[str]]] = None
) -> Dict[str, Set[str]]:
    """
    Collects the symbols from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded symbols.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param data: The data to search in.
    :param included: The symbols to include.
    :param bases: The bases of the asset pairs.

    :return: The data of the exchanges.
    """

    return mutual_string_values(
        data=data or exchanges_symbols(
            exchanges=exchanges, quotes=quotes, excluded=excluded,
            adjust=adjust, separator=separator, included=included, bases=bases
        )
    )
# end mutual_exchanges_symbols

AssetMatches = Iterable[Iterable[str]]

def matching_symbol_pair(
        symbol1: str,
        symbol2: str, /, *,
        matches: Optional[AssetMatches] = None,
        separator: Optional[str] = None
) -> bool:
    """
    Checks if the symbols are valid with the matching currencies.

    :param symbol1: The first ticker.
    :param symbol2: The second ticker.
    :param matches: The currencies.
    :param separator: The separator of the assets.

    :return: The validation value for the symbols.
    """

    symbol1 = adjust_symbol(symbol=symbol1, separator=separator)
    symbol2 = adjust_symbol(symbol=symbol2, separator=separator)

    if symbol1 == symbol2:
        return True
    # end if

    asset1, currency1 = symbol_to_parts(symbol=symbol1, separator=separator)
    asset2, currency2 = symbol_to_parts(symbol=symbol2, separator=separator)

    if asset1 != asset2:
        return False
    # end if

    matches = matches or ()

    return any(
        (currency1 in match) and (currency2 in match)
        for match in matches
    )
# end matching_symbol_pair

ExchangeSymbolPairs = Set[Tuple[Tuple[str, str], Tuple[str, str]]]
ExchangesAssetMatches = Union[Dict[Iterable[str], AssetMatches], AssetMatches]

def matching_symbol_pairs(
        data: Dict[str, Iterable[str]],
        matches: Optional[ExchangesAssetMatches] = None,
        separator: Optional[str] = None
) -> ExchangeSymbolPairs:
    """
    Checks if the symbols are valid with the matching currencies.

    :param data: The symbols.
    :param matches: The currencies.
    :param separator: The separator of the assets.

    :return: The validation value for the symbols.
    """

    pairs = set()
    exchange_symbol_pairs = []

    for exchange, symbols in data.items():
        exchange_symbol_pairs.extend(
            [(exchange, symbol) for symbol in symbols]
        )
    # end for

    for exchange1, symbol1 in exchange_symbol_pairs:
        for exchange2, symbol2 in exchange_symbol_pairs:
            if exchange1 == exchange2:
                continue
            # end if

            match1 = ((exchange1, symbol1), (exchange2, symbol2))
            match2 = ((exchange2, symbol2), (exchange1, symbol1))

            if (match1 in pairs) or (match2 in pairs):
                continue
            # end if

            exchanges_matches = (
                matches if not isinstance(matches, dict) else
                [*matches.get(exchange1, []), *matches.get(exchange2, [])]
            )

            if (
                (exchange1 != exchange2) and
                matching_symbol_pair(
                    symbol1, symbol2,
                    matches=exchanges_matches or None,
                    separator=separator
                )
            ):
                pairs.add(match1)
                pairs.add(match2)
            # end if
        # end for
    # end for

    return pairs
# end matching_symbol_pairs

@define(slots=False, init=False, repr=False, eq=False, unsafe_hash=True)
class MarketSymbolSignature(Pair):
    """A class to represent the data for the execution of a trade."""

    __slots__ = "_exchange",

    __modifiers__ = Modifiers(**Pair.__modifiers__)
    __modifiers__.properties.append('exchange')

    EXCHANGE: ClassVar[str] = 'exchange'

    try:
        from typing import Self

    except ImportError:
        Self = Any
    # end try

    def __init__(
            self,
            exchange: str,
            base: str,
            quote: str,
            separator: Optional[str] = None
    ) -> None:
        """
        Defines the class attributes.

        :param exchange: The exchange name.
        :param base: The base asset.
        :param quote: The quote asset.
        :param separator: The symbol separator.
        """

        super().__init__(base=base, quote=quote, separator=separator)

        self._exchange = exchange
    # end __init__

    def __eq__(self, other: Any) -> bool:
        """
        Checks if the signatures are equal.

        :param other: The signature to compare.

        :return: The equality value.
        """

        if type(other) is not type(self):
            return NotImplemented
        # end if

        other: MarketSymbolSignature

        return (self is other) or (
            (self.exchange == other.exchange) and
            (self.base == other.base) and
            (self.quote == other.quote)
        )
    # end __eq__

    @property
    def exchange(self) -> str:
        """
        Returns the property value.

        :return: The exchange name.
        """

        return self._exchange
    # end exchange

    @classmethod
    def load(cls, data: Dict[str, str]) -> Self:
        """
        Creates a pair of assets from the data.

        :param data: The pair data.

        :return: The pair object.
        """

        return cls(
            exchange=data[cls.EXCHANGE],
            base=data[cls.BASE],
            quote=data[cls.QUOTE],
            separator=data.get(cls.SEPARATOR, None)
        )
    # end load

    def json(self) -> Dict[str, str]:
        """
        Converts the data into a json format.

        :return: The chain of assets.
        """

        return {
            self.EXCHANGE: self.exchange,
            **super().json()
        }
    # end json
# end MarketPairSignature

def matching_symbol_signatures(
        pairs: Optional[ExchangeSymbolPairs] = None,
        data: Optional[Dict[str, Iterable[str]]] = None,
        matches: Optional[ExchangesAssetMatches] = None,
        separator: Optional[str] = None
) -> Set[Tuple[MarketSymbolSignature, MarketSymbolSignature]]:
    """
    Checks if the screeners are valid with the matching currencies.

    :param data: The data for the pairs.
    :param pairs: The pairs' data.
    :param matches: The currencies.
    :param separator: The separator of the assets.

    :return: The validation value for the symbols.
    """

    if (data is None) and (pairs is None):
        raise ValueError(
            f"One of 'pairs' and 'data' parameters must be given, "
            f"when 'pairs' is superior to 'data'."
        )

    elif (not pairs) and (not data):
        return set()
    # end if

    new_pairs = []

    pairs = pairs or matching_symbol_pairs(
        data=data, matches=matches, separator=separator
    )

    for (exchange1, symbol1), (exchange2, symbol2) in pairs:
        asset1, currency1 = symbol_to_parts(symbol1)
        asset2, currency2 = symbol_to_parts(symbol2)

        new_pairs.append(
            (
                MarketSymbolSignature(
                    base=asset1, quote=currency1,
                    exchange=exchange1
                ),
                MarketSymbolSignature(
                    base=asset2, quote=currency2,
                    exchange=exchange2
                )
            )
        )
    # end for

    return set(new_pairs)
# end matching_symbol_signatures