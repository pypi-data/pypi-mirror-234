# base.py

import time
import asyncio
import threading
import datetime as dt
import warnings
from typing import Optional, Any, Union, Dict, List, Tuple, Iterable

__all__ = [
    "BaseCallback",
    "callback_data",
    "execute_callbacks"
]

CallbackData = List[Tuple[float, Dict[str, Optional[Union[str, bool, float]]]]]

def callback_data(
        data: CallbackData,
        exchange: str,
        symbol: str,
        interval: Optional[str] = None
) -> Dict[str, Union[str, CallbackData]]:
    """
    Wraps the data for the callback.

    :param data: The data to wrap.
    :param exchange: The source exchange of the data.
    :param symbol: The symbol of the data.
    :param interval: The interval of the data.

    :return: The wrapped data.
    """

    return {
        BaseCallback.DATA: data,
        BaseCallback.EXCHANGE: exchange,
        BaseCallback.SYMBOL: symbol,
        BaseCallback.INTERVAL: interval
    }
# end callback_data

class BaseCallback:
    """A class to represent a callback."""

    DATA_KEY = None
    CONNECTABLE = False
    ADJUSTABLE = True

    DATA = 'data'
    EXCHANGE = 'exchange'
    SYMBOL = 'symbol'
    INTERVAL = 'interval'

    DELAY = 0.001

    def __init__(
            self,
            key: Optional[Any] = None,
            delay: Optional[Union[float, dt.timedelta]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param key: The key od the data.
        :param delay: The delay in handling.
        """

        if key is None:
            key = self.DATA_KEY
        # end if

        if delay is None:
            delay = self.DELAY
        # end if

        self.key = key
        self.delay = delay

        self.awaiting: List[Dict[str, Any]] = []
        self.exceptions: List[Tuple[Exception, Any]] = []

        self._handling_processes: List[threading.Thread] = []

        self._connected = False
        self._handling = False
        self._running = True
    # end __init__

    @property
    def handling(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._handling
    # end handling

    @property
    def running(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return (
            self._running and
            ((self.connected and self.connectable) or (not self.connectable))
        )
    # end running

    @property
    def connected(self) -> bool:
        """
        Checks if the connection was created.

        :return: The existence of a connection.
        """

        return self._connected
    # end connected

    @property
    def connectable(self) -> bool:
        """
        Checks if the connection was created.

        :return: The existence of a connection.
        """

        return self.CONNECTABLE
    # end connectable

    @property
    def adjustable(self) -> bool:
        """
        Checks if the connection was created.

        :return: The existence of a connection.
        """

        return self.ADJUSTABLE
    # end adjustable

    async def start(self) -> None:
        """Connects to the socket service."""
    # end start

    async def connect(self) -> None:
        """Connects to the socket service."""

        if self.connected:
            warnings.warn(f"{repr(self)} callback is already connected.")

            return
        # end if

        try:
            await self.start()

            self._connected = True
            self._running = True

        except Exception as e:
            if self.adjustable:
                warnings.warn(f"{type(e)}: {str(e)}")

            else:
                raise e
            # end if
        # end try
    # end connect

    async def prepare(self) -> None:
        """Connects to the socket service."""

        if self.connectable and (not self.connected):
            await self.connect()
        # end if
    # end prepare

    def handling_loop(self) -> None:
        """Handles the requests."""

        self._handling = True

        while self.handling:
            try:
                self.awaiting.append(self.awaiting.pop(0))

            except IndexError:
                delay = self.delay

                if isinstance(delay, dt.timedelta):
                    delay = delay.total_seconds()
                # end if

                time.sleep(delay)
            # end try
        # end while
    # end handling_loop

    def start_handling(self) -> None:
        """Starts the screening process."""

        handling_process = threading.Thread(
            target=lambda: self.handling_loop()
        )

        self._handling_processes.append(handling_process)

        handling_process.start()
    # end start_handling

    def stop_handling(self) -> None:
        """Stops the handling process."""

        if self.handling:
            self._handling = False

            self._handling_processes.clear()
        # end if
    # end stop_handling

    def enable(self) -> None:
        """Stops the handling process."""

        self._running = True
    # end enable

    def disable(self) -> None:
        """Stops the handling process."""

        self._running = False
    # end stop_running

    def stop_running(self) -> None:
        """Stops the screening process."""

        self.disable()
    # end stop_running

    def stop(self) -> None:
        """Stops the screening process."""

        self.stop_handling()
        self.stop_running()
    # end stop

    def terminate(self) -> None:
        """Stops the screening process."""

        self.stop()
    # end terminate

    async def handle(self, data: Any, timestamp: float, key: Optional[Any] = None) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        :param key: The key for the data type.

        :return: The validation value.
        """
    # end handle

    async def exception(self, exception: Exception, data: Any) -> bool:
        """
        Records and handles the exception.

        :param data: The data from the exchange.
        :param exception: The exception object.

        :return: The validation value.
        """

        self.exceptions.append((exception, data))

        if self.adjustable:
            warnings.warn(f"{type(exception)}: {str(exception)}")

            return False

        else:
            raise exception
        # end if
    # end exception

    async def _handle(self, **kwargs: Any) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param kwargs: Any keyword arguments.

        :return: The validation value.
        """

        try:
            return await self.handle(**kwargs)

        except Exception as e:
            return await self.exception(exception=e, data=kwargs)
        # end try
    # end _handle

    async def record(self, data: Any, timestamp: float, key: Optional[Any] = None) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        :param key: The key for the data type.

        :return: The validation value.
        """

        await self.prepare()

        if (self.connectable and (not self.connected)) or (not self.running):
            return False
        # end if

        return await self._handle(data=data, timestamp=timestamp, key=key)
    # end record

    def run(self, handlers: Optional[int] = None) -> None:
        """
        Runs the process of the price screening.

        :param handlers: The amount of handlers to create.
        """

        if handlers is None:
            handlers = 1
        # end if

        if handlers:
            self._handling = True
        # end if

        for _ in range(handlers):
            self.start_handling()
        # end for
    # end run
# end BaseCallback

async def execute_callbacks(
        callbacks: Iterable[BaseCallback],
        key: str,
        timestamp: float,
        data: CallbackData,
        exchange: str,
        symbol: str,
        interval: Optional[str] = None
) -> None:
    """
    Wraps the data for the callback.

    :param callbacks: The callbacks to execute.
    :param key: The call type key.
    :param timestamp: The timestamp of the source data.
    :param data: The data to wrap.
    :param exchange: The source exchange of the data.
    :param symbol: The symbol of the data.
    :param interval: The interval of the data.

    :return: The wrapped data.
    """

    payload = callback_data(
        data=data, exchange=exchange,
        symbol=symbol, interval=interval
    )

    await asyncio.gather(
        *(
            callback.record(payload, timestamp, key=key)
            for callback in callbacks or []
        )
    )
# end execute_callbacks