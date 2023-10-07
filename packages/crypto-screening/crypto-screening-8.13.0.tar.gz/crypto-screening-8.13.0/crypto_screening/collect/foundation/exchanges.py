# exchanges.py

from typing import (
    Optional, Dict, Iterable,
    Callable, Union, TypeVar, Any
)

from multithreading import Caller, multi_threaded_call

from crypto_screening.exchanges import EXCHANGE_NAMES
from crypto_screening.validate import validate_exchange
from crypto_screening.utils.process import (
    find_string_value, lower_string_values, string_in_values
)

__all__ = [
    "exchanges_data",
    "exchanges_values"
]

ExchangesData = Union[Dict[str, Iterable[str]], Iterable[str]]

def exchanges_values(
        exchanges: Iterable[str],
        values: Optional[ExchangesData] = None
) -> Dict[str, Iterable[str]]:
    """
    Collects the values to the structure of the exchanges.

    :param exchanges: The exchanges for the structure.
    :param values: The values to process.

    :return: The structured exchanges' data.
    """

    values_data = []

    values = values or {}

    if values:
        values_data = values
    # end if

    if (
        values and
        all(isinstance(value, str) for value in values) and
        not isinstance(values, dict)
    ):
        values = {exchange: values_data for exchange in exchanges}
    # end if

    return values
# end exchanges_values

def exchange_value(
        exchange: str,
        values: Union[Any, Dict[str, Any]],
        default: Optional[Any] = None
) -> Any:
    """
    Finds the value of the exchange or returns the default.

    :param exchange: The exchange name.
    :param values: The values of the exchanges.
    :param default: The default value.

    :return: The value of the exchange.
    """

    return (
        (values[exchange] if exchange in values else default)
        if isinstance(values, dict) else values
    )
# end exchange_value

_R = TypeVar("_R")

Collector = Callable[
    [
        str,
        Optional[str],
        Optional[bool],
        Optional[Iterable[str]],
        Optional[Iterable[str]],
        Optional[Iterable[str]],
        Optional[Iterable[str]]
    ], _R
]

def exchanges_data(
        collector: Collector,
        adjust: Optional[bool] = True,
        separator: Optional[str] = None,
        exchanges: Optional[Iterable[str]] = None,
        bases: Optional[ExchangesData] = None,
        quotes: Optional[ExchangesData] = None,
        included: Optional[ExchangesData] = None,
        excluded: Optional[ExchangesData] = None
) -> Dict[str, _R]:
    """
    Collects the symbols from the exchanges.

    :param collector: The collector function to collect data from an exchange.
    :param exchanges: The exchanges.
    :param bases: The bases of the asset pairs.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param quotes: The quotes of the asset pairs.
    :param included: The symbols to include.
    :param excluded: The excluded symbols.
    :param bases: The bases of the asset pairs.

    :return: The data of the exchanges.
    """

    exchanges = lower_string_values(exchanges or EXCHANGE_NAMES)

    bases = exchanges_values(exchanges=exchanges, values=bases)
    quotes = exchanges_values(exchanges=exchanges, values=quotes)
    included = exchanges_values(exchanges=exchanges, values=included)
    excluded = exchanges_values(exchanges=exchanges, values=excluded)

    markets = []

    for exchange in exchanges:
        if not string_in_values(value=exchange, values=EXCHANGE_NAMES):
            if adjust:
                continue

            else:
                validate_exchange(exchange=exchange, exchanges=EXCHANGE_NAMES)
            # end if
        # end if

        markets.append(exchange)
    # end for

    callers = []
    data: Dict[str, Caller] = {}

    for exchange in markets:
        saved_exchange = exchange

        exchange = find_string_value(value=exchange, values=exchanges)

        exchange_bases = exchange_value(exchange=exchange, values=bases)
        exchange_quotes = exchange_value(exchange=exchange, values=quotes)
        exchange_included = exchange_value(exchange=exchange, values=included)
        exchange_excluded = exchange_value(exchange=exchange, values=excluded)

        caller = Caller(
            target=collector,
            kwargs=dict(
                exchange=saved_exchange,
                separator=separator,
                adjust=adjust,
                quotes=exchange_quotes,
                bases=exchange_bases,
                included=exchange_included,
                excluded=exchange_excluded
            )
        )

        callers.append(caller)
        data[exchange] = caller
    # end for

    multi_threaded_call(callers=callers)

    return {
        key: value.result.returns
        for key, value in data.items() if value
    }
# end exchanges_data