# market.py

import datetime as dt
from abc import ABCMeta
from typing import Iterable, List, Optional, Union

from multithreading import Caller, multi_threaded_call


from crypto_screening.foundation.state import WaitingState
from crypto_screening.foundation.screener import BaseScreener
from crypto_screening.foundation.data import DataCollector
from crypto_screening.foundation.container import BaseScreenersContainer
from crypto_screening.foundation.waiting import (
    base_await_dynamic_initialization, base_await_dynamic_update, Condition
)

__all__ = [
    "BaseMarketScreener"
]

class BaseMarketScreener(DataCollector, BaseScreenersContainer, metaclass=ABCMeta):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.

    - screeners:
        The screener object to control and fill with data.
    """

    def __init__(
            self,
            screeners: Optional[Iterable[BaseScreener]] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        """

        DataCollector.__init__(self, location=location, cancel=cancel, delay=delay)

        BaseScreenersContainer.__init__(self, screeners=screeners)

        self._saving_screeners: List[BaseScreener] = []
    # end __init__

    def await_initialization(
            self,
            stop: Optional[Union[bool, int]] = False,
            delay: Optional[Union[float, dt.timedelta]] = None,
            cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
            condition: Optional[Condition] = None
    ) -> WaitingState[BaseScreener]:
        """
        Waits for all the create_screeners to update.

        :param delay: The delay for the waiting.
        :param stop: The value to stop the screener objects.
        :param cancel: The time to cancel the waiting.
        :param condition: The condition to control the waiting outside the function.

        :returns: The total delay.
        """

        return base_await_dynamic_initialization(
            self._screeners, stop=stop, delay=delay,
            cancel=cancel, condition=condition
        )
    # end await_initialization

    def await_update(
            self,
            stop: Optional[Union[bool, int]] = False,
            delay: Optional[Union[float, dt.timedelta]] = None,
            cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
            condition: Optional[Condition] = None
    ) -> WaitingState[BaseScreener]:
        """
        Waits for all the create_screeners to update.

        :param delay: The delay for the waiting.
        :param stop: The value to stop the screener objects.
        :param cancel: The time to cancel the waiting.
        :param condition: The condition to control the waiting outside the function.

        :returns: The total delay.
        """

        return base_await_dynamic_update(
            self._screeners, stop=stop, delay=delay,
            cancel=cancel, condition=condition
        )
    # end await_update

    def save_datasets(self, location: Optional[str] = None) -> None:
        """
        Runs the data handling loop.

        :param location: The saving location.
        """

        callers = []

        for screener in self.screeners:
            location = location or screener.location or self.location

            callers.append(
                Caller(
                    target=screener.save_dataset,
                    kwargs=dict(location=location)
                )
            )
        # end for

        multi_threaded_call(callers=callers)
    # end save_datasets

    def load_datasets(self, location: Optional[str] = None) -> None:
        """
        Runs the data handling loop.

        :param location: The saving location.
        """

        callers = []

        for screener in self.screeners:
            location = location or screener.location or self.location

            callers.append(
                Caller(
                    target=screener.load_dataset,
                    kwargs=dict(location=location)
                )
            )
        # end for

        multi_threaded_call(callers=callers)
    # end load_datasets

    def saving_loop(self) -> None:
        """Runs the process of the price screening."""

        for screener in self.screeners:
            if not screener.saving:
                screener.start_saving()

                self._saving_screeners.append(screener)
            # end if
        # end for
    # end saving_loop

    def stop_saving(self) -> None:
        """Stops the saving of the screeners."""

        for screener in self._saving_screeners:
            screener.stop_saving()
        # end for
    # end stop_saving
# end BaseMarketScreener