# sockets.py

import json
from typing import Optional, Any, Union, Dict, Callable, List
import asyncio
import datetime as dt
from uuid import uuid4
from textwrap import wrap as _wrap

from crypto_screening.screeners.callbacks.base import BaseCallback

__all__ = [
    "SocketCallback"
]

def wrap(message: str, buffer: int) -> str:
    """
    Wraps the message with a spacing buffer for the buffer length.

    :param message: The string message.
    :param buffer: The buffer size.

    :return: The buffered padded message.
    """

    if len(message) > buffer:
        raise ValueError(f"Buffer {buffer} is too small.")
    # end wrap

    return message + (" " * (buffer - len(message)))
# end wrap

class SocketCallback(BaseCallback):
    """A class to represent a socket callback."""

    BUFFER = 1024

    TCP = 'tcp'

    REGULAR_FORMAT = 'regular'
    CHUNKED_FORMAT = 'chunked'

    FORMATS = (REGULAR_FORMAT, CHUNKED_FORMAT)

    FORMAT = 'format'
    TIMESTAMP = 'timestamp'
    NAME = 'name'
    KEY = 'key'
    PROTOCOL = 'protocol'
    CHUNKS = 'chunks'
    PART = 'part'
    ID = 'id'

    REGULAR_DATA_KEYS = (
        PROTOCOL, KEY, TIMESTAMP,
        BaseCallback.DATA, FORMAT, ID
    )
    CHUNKED_DATA_KEYS = (
        PROTOCOL, KEY, CHUNKS, TIMESTAMP,
        BaseCallback.DATA, FORMAT, PART, ID
    )

    FIRST_KEY = PROTOCOL
    LAST_KEY = ID

    CONNECTABLE = True

    def __init__(
            self,
            address: str,
            port: int,
            key: Optional[Any] = None,
            buffer: Optional[int] = None,
            delay: Optional[Union[float, dt.timedelta]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param address: The address of the socket.
        :param port: The port of the socket.
        :param key: The key od the data.
        :param buffer: The buffer size.
        :param delay: The delay in handling.
        """

        super().__init__(key=key, delay=delay)

        self.address = address
        self.port = port
        self.buffer = buffer or self.BUFFER

        self._connection: Optional[asyncio.StreamWriter] = None
        self._writer: Optional[Callable[[bytes], None]] = None
    # end __init__

    def wrap(self, message: str) -> str:
        """
        Wraps the message with a spacing buffer for the buffer length.

        :param message: The string message.

        :return: The buffered padded message.
        """

        return wrap(message=message, buffer=self.buffer)
    # end wrap

    def package(
            self,
            data: Dict[str, Any],
            key: str,
            timestamp: float,
            message_id: str
    ) -> List[bytes]:
        """
        Packages the data for the socket to send.

        :param data: The data to package for shipping.
        :param key: The key type of the data.
        :param timestamp: The time of the data.
        :param message_id: The message id.

        :return: The list of byte streams to send.
        """

        messages: List[str] = []

        data = json.dumps(
            {
                self.PROTOCOL: self.TCP,
                self.KEY: key,
                self.TIMESTAMP: timestamp,
                self.DATA: data,
                self.FORMAT: self.REGULAR_FORMAT,
                self.ID: message_id
            }
        )

        if len(data) > self.buffer:
            chunks = _wrap(data, max(self.buffer - 128, 128))

            for i, chunk in enumerate(chunks, start=1):
                messages.append(
                    json.dumps(
                        {
                            self.PROTOCOL: self.TCP,
                            self.KEY: key,
                            self.CHUNKS: len(chunks),
                            self.TIMESTAMP: timestamp,
                            self.FORMAT: self.CHUNKED_FORMAT,
                            self.DATA: chunk,
                            self.PART: i,
                            self.ID: message_id
                        }
                    )
                )
            # end for

        else:
            messages.append(data)
        # end if

        return [self.wrap(message).encode() for message in messages]
    # end package

    # noinspection PyTypeChecker
    async def start(self) -> None:
        """Connects to the socket service."""

        _, self._connection = await asyncio.open_connection(
            host=self.address, port=self.port, limit=self.buffer
        )

        # noinspection PyUnresolvedReferences
        self._writer = (
            self._connection.write
            if hasattr(self._connection, 'write') else
            self._connection.swrite
        )
    # end start

    async def handle(
            self,
            data: Dict[str, Any],
            timestamp: float,
            key: Optional[Any] = None
    ) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        :param key: The key for the data type.

        :return: The validation value.
        """

        for message in self.package(
            data=data, key=key or self.key,
            timestamp=float(timestamp), message_id=str(uuid4())
        ):
            self._writer(message)
        # end for

        return True
    # end process
# end SocketCallback