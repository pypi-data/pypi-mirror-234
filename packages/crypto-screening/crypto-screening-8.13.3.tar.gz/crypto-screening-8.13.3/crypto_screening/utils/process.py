# process.py

from typing import Iterable, List, Set, Optional, Dict

__all__ = [
    "find_string_value",
    "upper_string_values",
    "lower_string_values",
    "mutual_string_values",
    "string_in_values"
]

def find_string_value(value: str, values: Iterable[str]) -> str:
    """
    Finds the exchange in the exchanges.

    :param value: The name of the exchange.
    :param values: The exchanges to search in.

    :return: The valid exchange name.
    """

    if value in values:
        return value
    # end if

    if value.lower() in values:
        return value.lower()
    # end if

    if value.upper() in values:
        return value.upper()
    # end if

    for valid in values:
        if value.lower() == valid.lower():
            return valid
        # end if
    # end for

    return value
# end find_string_value

def string_in_values(value: str, values: Iterable[str]) -> bool:
    """
    Finds the exchange in the exchanges.

    :param value: The name of the exchange.
    :param values: The exchanges to search in.

    :return: The valid exchange name.
    """

    return find_string_value(value=value, values=values) in values
# end string_in_values

def upper_string_values(values: Iterable[str]) -> List[str]:
    """
    Converts all string values to upper case.

    :param values: The values to convert.

    :return: The converted values.
    """

    return [value.upper() for value in values]
# end upper_string_values

def lower_string_values(values: Iterable[str]) -> List[str]:
    """
    Converts all string values to upper case.

    :param values: The values to convert.

    :return: The converted values.
    """

    return [value.lower() for value in values]
# end lower_string_values

def mutual_string_values(
        data: Dict[str, Iterable[str]],
        minimum: Optional[int] = None,
        maximum: Optional[int] = None
) -> Dict[str, Set[str]]:
    """
    Collects the symbols from the exchanges.

    :param data: The exchanges' data.
    :param minimum: The minimum amount of counts for a value.
    :param maximum: The maximum amount of counts for a value.

    :return: The data of the exchanges.
    """

    if minimum is None:
        minimum = 2
    # end if

    if maximum is None:
        maximum = len(data) * max(len(list(values)) for values in data.values()) + 1
    # end if

    values = {}

    for key in data:
        for value in data[key]:
            values[value] = values.setdefault(value, 0) + 1
        # end for
    # end for

    return {
        key: {
            value for value in data[key]
            if minimum <= values.get(value, 0) <= maximum
        } for key in data
    }
# end mutual_exchanges_assets