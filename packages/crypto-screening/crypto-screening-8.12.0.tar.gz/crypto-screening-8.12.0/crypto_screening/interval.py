# interval.py

from typing import Tuple, Union, Dict, Any, ClassVar, Optional
import datetime as dt

from attrs import define

from represent import represent, Modifiers


__all__ = [
    "interval_amount",
    "interval_time",
    "interval_total_time",
    "parts_to_interval",
    "interval_duration",
    "interval_to_parts",
    "validate_interval_parts",
    "validate_interval_amount",
    "validate_interval",
    "validate_interval_duration",
    "INTERVALS",
    "SECONDS",
    "MINUTES",
    "MONTHS",
    "HOURS",
    "DAYS",
    "YEARS",
    "WEEKS",
    "Interval",
    "is_valid_interval"
]

SECONDS = "s"
MINUTES = "m"
MONTHS = "mo"
HOURS = "h"
DAYS = "d"
YEARS = "y"
WEEKS = "w"

INTERVALS = {
    SECONDS: dt.timedelta(seconds=1),
    MINUTES: dt.timedelta(minutes=1),
    HOURS: dt.timedelta(hours=1),
    DAYS: dt.timedelta(days=1),
    WEEKS: dt.timedelta(days=7),
    MONTHS: dt.timedelta(days=30),
    YEARS: dt.timedelta(days=365)
}

def validate_interval_duration(duration: Any) -> str:
    """
    Validates the interval part.

    :param duration: The value to validate.

    :return: The valid interval part.
    """

    if not isinstance(duration, str) or duration not in INTERVALS:
        raise ValueError(
            f"Interval duration must be a non-empty "
            f"string from the options: {', '.join(INTERVALS)}, "
            f"not: {duration}"
        )
    # end if

    return duration
# end validate_interval_duration

def validate_interval_amount(amount: Optional[Any] = None) -> int:
    """
    Validates the interval part.

    :param amount: The value to validate.

    :return: The valid interval part.
    """

    if amount is None:
        amount = 1

    elif not isinstance(amount, int) or (amount <= 0):
        raise ValueError(
            f"Interval amount must be a positive "
            f"integer, not: {amount}"
        )
    # end if

    return amount
# end validate_interval_amount

def validate_interval_parts(amount: Any, duration: Optional[Any] = None) -> Tuple[int, str]:
    """
    Validates the interval parts.

    :param amount: The increment value to validate.
    :param duration: The duration value to validate.

    :return: The valid interval parts.
    """

    duration = validate_interval_duration(duration)
    amount = validate_interval_amount(amount)

    return amount, duration
# end validate_interval_parts

def validate_interval(interval: str) -> str:
    """
    Validates the interval parts.

    :param interval: The interval to validate..

    :return: The valid interval parts.
    """

    amount, duration = interval_to_parts(interval)

    validate_interval_duration(duration)
    validate_interval_amount(amount)

    return interval
# end validate_interval

def is_valid_interval(interval: str) -> bool:
    """
    Validates the interval value.

    :param interval: The interval for the data.

    :return: The validates value.
    """

    try:
        validate_interval(interval)

        return True

    except ValueError:
        return False
    # end try
# end is_valid_interval

@define(slots=False, init=False, repr=False, eq=False, unsafe_hash=True)
@represent
class Interval:
    """
    A class to represent a trading pair.

    This object represents a pair of assets that can be traded.

    attributes:

    - base:
        The asset to buy or sell.

    - quote:
        The asset to use to buy or sell.

    >>> from crypto_screening.interval import Interval
    >>>
    >>> one_day = Interval(1, "d")
    >>> five_seconds = Interval(5, "s")
    """

    __slots__ = "_amount", "_duration"

    __modifiers__ = Modifiers(excluded=["parts"])

    PERIODS: ClassVar[str] = 'periods'
    DURATION: ClassVar[str] = 'duration'

    try:
        from typing import Self

    except ImportError:
        Self = Any
    # end try

    def __init__(self, amount: int, duration: str) -> None:
        """
        Defines the class attributes.

        :param amount: The amount of periods for the interval.
        :param duration: The duration type for the interval.
        """

        amount, duration = validate_interval_parts(
            amount=amount, duration=duration
        )

        self._amount = amount
        self._duration = duration
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

        other: Interval

        return (self is other) or (
            (self.amount == other.amount) and
            (self.duration == other.duration)
        )
    # end __eq__

    @property
    def amount(self) -> int:
        """
        Returns the periods property.

        :return: The amount of periods in the interval.
        """

        return self._amount
    # end amount

    @property
    def duration(self) -> str:
        """
        Returns the duration property.

        :return: The duration in the interval.
        """

        return self._duration
    # end duration

    @classmethod
    def load(cls, data: Dict[str, Union[str, int]]) -> Self:
        """
        Creates a pair of assets from the data.

        :param data: The pair data.

        :return: The pair object.
        """

        return cls(
            amount=data[cls.PERIODS],
            duration=data[cls.DURATION]
        )
    # end load

    @property
    def parts(self) -> Tuple[int, str]:
        """
        Returns the property value.

        :return: The symbol.
        """

        return self._amount, self._duration
    # end parts

    def interval(self) -> str:
        """
        Returns the string for the interval.

        :return: The string.
        """

        return f"{self.amount}{self.duration}"
    # end __str__

    def json(self) -> Dict[str, Union[int, str]]:
        """
        Converts the data into a json format.

        :return: The chain of assets.
        """

        return {
            self.PERIODS: self.amount,
            self.DURATION: self.duration
        }
    # end json
# end Interval

def interval_amount(interval: str) -> int:
    """
    Extracts the number from the interval.

    :param interval: The interval to extract.

    :return: The number from the interval.
    """

    for kind in sorted(INTERVALS.keys(), key=lambda key: len(key), reverse=True):
        try:
            if kind not in interval:
                continue
            # end if

            return int(interval.replace(kind, ""))

        except (TypeError, EOFError):
            pass
        # end try
    # end for

    raise ValueError(f"Invalid interval value: {interval}.")
# end interval_amount

def interval_duration(interval: str) -> str:
    """
    Extracts the type from the interval.

    :param interval: The interval to extract.

    :return: The type from the interval.
    """

    return interval.replace(str(interval_amount(interval)), "")
# end interval_duration

def interval_time(interval: str) -> dt.timedelta:
    """
    Extracts the type from the interval.

    :param interval: The interval to extract.

    :return: The type from the interval.
    """

    try:
        return INTERVALS[interval_duration(interval)]

    except KeyError:
        raise ValueError(f"Invalid interval structure: {interval}.")
    # end try
# end interval_time

def interval_total_time(interval: str) -> dt.timedelta:
    """
    Extracts the type from the interval.

    :param interval: The interval to extract.

    :return: The type from the interval.
    """

    return interval_amount(interval) * interval_time(interval)
# end interval_total_time

def parts_to_interval(increment: str, duration: int) -> str:
    """
    Creates a valid interval from the parameters.

    :param increment: The increment type for the interval.
    :param duration: The duration of the interval.

    :return: The interval.
    """

    if increment not in INTERVALS:
        raise ValueError(
            f"Interval increment must be one of "
            f"{', '.join(INTERVALS.keys())}, not {increment}."
        )
    # end if

    return f"{duration}{increment}"
# end parts_to_interval

def interval_to_parts(interval: str) -> Tuple[int, str]:
    """
    Creates a valid interval from the parameters.

    :param interval: The interval to separate to its parts.

    :return: The interval parts.
    """

    amount = interval_amount(interval)

    return amount, interval.replace(str(amount), "")
# end parts_to_interval