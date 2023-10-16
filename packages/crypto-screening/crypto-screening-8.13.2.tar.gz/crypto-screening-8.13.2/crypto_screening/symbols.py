# symbols.py

from typing import (
    Optional, Tuple, Dict, Any, Iterable, Set, ClassVar
)

from attrs import define

from represent import represent, Modifiers

__all__ = [
    "Pair",
    "symbol_to_pair",
    "symbol_to_parts",
    "pair_to_symbol",
    "parts_to_symbol",
    "reverse_symbol",
    "reverse_pair",
    "adjust_symbol",
    "parts_to_pair",
    "pair_to_parts",
    "symbols_to_parts",
    "parts_to_symbol_parts",
    "parts_to_symbol_parts",
    "assets_to_symbols",
    "parts_to_symbols",
    "Separator",
    "validate_separator"
]

class Separator:
    """A class to contain the separator value."""

    value = "/"
# end Separator

def validate_separator(separator: Optional[Any] = None) -> str:
    """
    Validates the separator value.

    :param separator: The value to validate.

    :return: The valid separator.
    """

    if separator is None:
        separator = Separator.value
    # end if

    if not isinstance(separator, str):
        raise ValueError(
            f"Separator must be a non-empty string, not: {separator}"
        )
    # end if

    if separator == "":
        raise ValueError("Separator must not be an empty string.")
    # end if

    return separator
# end validate_separator

def validate_base(base: Any) -> str:
    """
    Validates the symbol part.

    :param base: The part to validate.

    :return: The valid symbol part.
    """

    if not isinstance(base, str) or not base:
        raise ValueError(
            f"Symbol base asset must be a "
            f"non-empty string, not: {base}"
        )
    # end if

    return base
# end validate_base

def validate_quote(quote: Any) -> str:
    """
    Validates the symbol part.

    :param quote: The part to validate.

    :return: The valid symbol part.
    """

    if not isinstance(quote, str) or not quote:
        raise ValueError(
            f"Symbol quote asset must be a "
            f"non-empty string, not: {quote}"
        )
    # end if

    return quote
# end validate_quote

def validate_symbol_parts(
        base: Any, quote: Any, separator: Optional[Any] = None
) -> Tuple[str, str, str]:
    """
    Validates the symbol parts.

    :param separator: The value to validate.
    :param base: The base part to validate.
    :param quote: The quote part to validate.

    :return: The valid symbol parts.
    """

    separator = validate_separator(separator)
    base = validate_base(base)
    quote = validate_quote(quote)

    return base, quote, separator
# end validate_quote

@define(slots=False, init=False, repr=False, eq=False, unsafe_hash=True)
@represent
class Pair:
    """
    A class to represent a trading pair.

    This object represents a pair of assets that can be traded.

    attributes:

    - base:
        The asset to buy or sell.

    - quote:
        The asset to use to buy or sell.

    >>> from crypto_screening.symbols import Pair
    >>>
    >>> pair = Pair("BTC", "USD")
    """

    __modifiers__ = Modifiers(properties=['base', 'quote'])

    __slots__ = "_base", "_quote", "separator"

    BASE: ClassVar[str] = 'base'
    QUOTE: ClassVar[str] = 'quote'
    SEPARATOR: ClassVar[str] = 'separator'

    try:
        from typing import Self

    except ImportError:
        Self = Any
    # end try

    def __init__(self, base: str, quote: str, separator: Optional[str] = None) -> None:
        """
        Defines the class attributes.

        :param base: The base asset of the trading pair.
        :param quote: The target asset of the trading pair.
        :param separator: The symbol separator.
        """

        base, quote, separator = validate_symbol_parts(
            base=base, quote=quote, separator=separator
        )

        self._base = base
        self._quote = quote

        self.separator = separator
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

        other: Pair

        return (self is other) or (
            (self.base == other.base) and
            (self.quote == other.quote)
        )
    # end __eq__

    @property
    def base(self) -> str:
        """
        Returns the property value.

        :return: The base name.
        """

        return self._base
    # end base

    @property
    def quote(self) -> str:
        """
        Returns the property value.

        :return: The base name.
        """

        return self._quote
    # end quote

    @property
    def parts(self) -> Tuple[str, str]:
        """
        Returns the property value.

        :return: The symbol.
        """

        return self._base, self._quote
    # end parts

    @property
    def symbol(self) -> str:
        """
        Returns the property value.

        :return: The symbol.
        """

        return parts_to_symbol(
            self._base, self._quote, separator=self.separator
        )
    # end symbol

    @classmethod
    def load(cls, data: Dict[str, str]) -> Self:
        """
        Creates a pair of assets from the data.

        :param data: The pair data.

        :return: The pair object.
        """

        return cls(
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

        return {self.BASE: self.base, self.QUOTE: self.quote}
    # end json
# end Pair

def pair_to_symbol(pair: Pair, separator: Optional[str] = None) -> str:
    """
    Converts a pair of assets into a symbol.

    :param pair: The pair of assets.
    :param separator: The separator of the assets.

    :return: The symbol.
    """

    return f"{pair.base}{validate_separator(separator)}{pair.quote}"
# end pair_to_symbol

def parts_to_symbol(base: str, quote: str, separator: Optional[str] = None) -> str:
    """
    Converts a pair of assets into a symbol.

    :param base: The base assets.
    :param quote: The quote assets.
    :param separator: The separator of the assets.

    :return: The symbol.
    """

    base, quote, separator = validate_symbol_parts(
        base=base, quote=quote, separator=separator
    )

    return f"{base}{separator}{quote}"
# end parts_to_symbol

def symbol_to_pair(symbol: str, separator: Optional[str] = None) -> Pair:
    """
    Converts a pair of assets into a symbol.

    :param symbol: The symbol to convert into a pair object.
    :param separator: The separator of the assets.

    :return: The symbol.
    """

    separator = validate_separator(separator)

    if separator not in symbol:
        symbol = adjust_symbol(symbol, separator=separator)
    # end if

    count = symbol.count(separator)

    if count == 1:
        base, quote = symbol.split(separator)

    elif count == 0:
        raise ValueError(
            f"Cannot separate symbol '{symbol}' because "
            f"the given separator '{separator}' is not in the symbol."
        )

    else:
        raise ValueError(
            f"Cannot separate symbol '{symbol}' because "
            f"the given separator '{separator}' is present more than once."
        )
    # end if

    return Pair(base=base, quote=quote)
# end symbol_to_pair

def parts_to_pair(base: str, quote: str) -> Pair:
    """
    Converts a pair of assets into a symbol.

    :param base: The base assets.
    :param quote: The quote assets.

    :return: The symbol.
    """

    return Pair(base, quote)
# end parts_to_pair

def symbol_to_parts(symbol: str, separator: Optional[str] = None) -> Tuple[str, str]:
    """
    Converts a pair of assets into a symbol.

    :param symbol: The symbol to convert into a pair object.
    :param separator: The separator of the assets.

    :return: The symbol.
    """

    return symbol_to_pair(symbol=symbol, separator=separator).parts
# end symbol_to_parts

def reverse_symbol(symbol: str, separator: Optional[str] = None) -> str:
    """
    Converts a pair of assets into a symbol.

    :param symbol: The symbol to convert into a pair object.
    :param separator: The separator of the assets.

    :return: The symbol.
    """

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    return parts_to_symbol(base=quote, quote=base)
# end reverse_symbol

def reverse_pair(pair: Pair, separator: Optional[str] = None) -> Pair:
    """
    Converts a pair of assets into a symbol.

    :param pair: The pair of assets.
    :param separator: The separator of the assets.

    :return: The symbol.
    """

    return symbol_to_pair(
        reverse_symbol(
            symbol=pair_to_symbol(pair=pair, separator=separator),
            separator=separator
        )
    )
# end symbol_to_parts

def pair_to_parts(pair: Pair) -> Tuple[str, str]:
    """
    Converts a pair of assets into a symbol.

    :param pair: The pair of assets.

    :return: The symbol.
    """

    return pair.base, pair.quote
# end pair_to_parts

def adjust_symbol(symbol: str, separator: Optional[str] = None) -> str:
    """
    Adjusts the symbol of the asset.

    :param symbol: The symbol of the asset to adjust.
    :param separator: The separator of the assets.

    :return: The adjusted asset symbol.
    """

    separator = validate_separator(separator)

    saved = symbol

    for char in "\"!@#$%^&*()_+-=,.|:`~/\\'":
        symbol = symbol.replace(char, " ")
    # end for

    parts = [part.upper() for part in symbol.split(" ") if part]

    try:
        return parts_to_symbol(*parts, separator=separator)

    except TypeError:
        raise ValueError(
            f"Cannot adjust symbol: {saved} "
            f"with separator: {separator}."
        )
    # end try
# end adjust_symbol

def symbols_to_parts(symbols: Dict[str, Dict[str, Any]]) -> Tuple[Set[str], Set[str]]:
    """
    Collects the bases and quotes of the symbols.

    :param symbols: The symbols to separate.

    :return: The separated bases and quotes.
    """

    quotes = set()
    bases = set()

    for base in symbols:
        bases.add(base)

        for quote in symbols[base]:
            quotes.add(quote)
        # end for
    # end for

    return bases, quotes
# end symbols_to_parts

def parts_to_symbol_parts(
        bases: Iterable[str], quotes: Iterable[str]
) -> Set[Tuple[str, str]]:
    """
    Collects the bases and quotes of the symbols.

    :param bases: The bases to join.
    :param quotes: The quotes to join.

    :return: The joined symbols.
    """

    pairs = set()

    for base in bases:
        for quote in quotes:
            if (base, quote) not in pairs:
                pairs.add((base, quote))
            # end if
        # end for
    # end for

    return pairs
# end parts_to_symbol_parts

def parts_to_symbols(
        bases: Iterable[str], quotes: Iterable[str]
) -> Set[str]:
    """
    Collects the bases and quotes of the symbols.

    :param bases: The bases to join.
    :param quotes: The quotes to join.

    :return: The joined symbols.
    """

    return {
        parts_to_symbol(*parts) for parts in
        (parts_to_symbol_parts(bases, quotes))
    }
# end parts_to_symbols

def assets_to_symbols(assets: Iterable[str]) -> Set[str]:
    """
    Creates the symbols from the assets.

    :param assets: The asset to build the symbols from.

    :return: The list of symbols.
    """

    symbols = set()

    for base in assets:
        for quote in assets:
            symbol = parts_to_symbol(base, quote)

            if (base != quote) and (reverse_symbol(symbol) not in symbols):
                symbols.add(symbol)
            # end if
        # end for
    # end for

    return symbols
# end assets_to_symbols