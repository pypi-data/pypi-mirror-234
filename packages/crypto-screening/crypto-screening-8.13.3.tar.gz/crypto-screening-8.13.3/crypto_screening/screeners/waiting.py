# waiting.py

import datetime as dt
from typing import (
    Optional, Union, Iterable
)

from crypto_screening.collect.screeners import gather_screeners
from crypto_screening.screeners.base import BaseScreener, BaseMarketScreener
from crypto_screening.foundation.state import WaitingState
from crypto_screening.foundation.waiting import (
    base_await_update, base_await_dynamic_initialization,
    base_await_initialization, base_await_dynamic_update,
    Condition
)

__all__ = [
    "await_dynamic_initialization",
    "await_update",
    "await_initialization",
    "await_dynamic_update",
    "WaitingState",
    "Condition"
]

def await_dynamic_initialization(
        screeners: Iterable[Union[BaseScreener, BaseMarketScreener]],
        stop: Optional[bool] = None,
        delay: Optional[Union[float, dt.timedelta]] = None,
        cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
        condition: Optional[Condition] = None
) -> WaitingState:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.,
    :param condition: The condition to control the waiting outside the function.

    :returns: The total delay.
    """

    return base_await_dynamic_initialization(
        screeners=screeners, stop=stop, delay=delay,
        cancel=cancel, gatherer=gather_screeners, condition=condition
    )
# end await_dynamic_initialization

def await_initialization(
        *screeners: Union[BaseScreener, BaseMarketScreener],
        stop: Optional[bool] = False,
        delay: Optional[Union[float, dt.timedelta]] = None,
        cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
        condition: Optional[Condition] = None
) -> WaitingState:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.,
    :param condition: The condition to control the waiting outside the function.

    :returns: The total delay.
    """

    return base_await_initialization(
        *screeners, stop=stop, delay=delay,
        cancel=cancel, gatherer=gather_screeners, condition=condition
    )
# end await_initialization

def await_dynamic_update(
        screeners: Iterable[Union[BaseScreener, BaseMarketScreener]],
        stop: Optional[bool] = False,
        delay: Optional[Union[float, dt.timedelta]] = None,
        cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
        condition: Optional[Condition] = None
) -> WaitingState:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.,
    :param condition: The condition to control the waiting outside the function.

    :returns: The total delay.
    """

    return base_await_dynamic_update(
        screeners=screeners, stop=stop, delay=delay,
        cancel=cancel, gatherer=gather_screeners, condition=condition
    )
# end await_dynamic_update

def await_update(
        *screeners: Union[BaseScreener, BaseMarketScreener],
        stop: Optional[bool] = False,
        delay: Optional[Union[float, dt.timedelta]] = None,
        cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
        condition: Optional[Condition] = None
) -> WaitingState:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.,
    :param condition: The condition to control the waiting outside the function.

    :returns: The total delay.
    """

    return base_await_update(
        *screeners, stop=stop, delay=delay,
        cancel=cancel, gatherer=gather_screeners, condition=condition
    )
# end await_update
