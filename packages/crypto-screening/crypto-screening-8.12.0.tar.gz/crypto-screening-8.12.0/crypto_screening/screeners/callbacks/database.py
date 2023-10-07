# database.py

import datetime as dt
from typing import Optional, Any, Dict, Set, Tuple, Union

from crypto_screening.screeners.database import (
    create_engine, parts_to_database_table_name, DATATYPES,
    extract_database_table_names, create_engine_session, Engine,
    insert_database_record_rows
)
from crypto_screening.screeners.callbacks.base import BaseCallback

__all__ = [
    "DatabaseCallback"
]

class DatabaseCallback(BaseCallback):
    """A class to represent a callback."""

    CONNECTABLE: bool = True

    DATATYPES = DATATYPES

    def __init__(
            self,
            database: str,
            engine: Optional[Engine] = None,
            key: Optional[Any] = None,
            delay: Optional[Union[float, dt.timedelta]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param database: The path to the database.
        :param engine: The engine for the database.
        :param key: The key od the data.
        :param delay: The delay in handling.
        """

        super().__init__(key=key, delay=delay)

        self.database = database

        self.engine = engine

        if isinstance(self.engine, Engine):
            self._connected = True
        # end if

        self._session: Optional = None

        self.tables: Dict[Tuple[str, str, str, Optional[str]], str] = {}
        self.table_names: Optional[Set[str]] = None
    # end __init__

    async def handle(
            self,
            data: Dict[str, Any],
            timestamp: float,
            key: Optional[Any] = None) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        :param key: The key for the data type.

        :return: The validation value.
        """

        key, exchange, symbol, interval = (
            key or self.key, data[self.EXCHANGE],
            data[self.SYMBOL], data.get(self.INTERVAL, None)
        )

        table = None

        if (key, exchange, symbol, interval) not in self.tables:
            table = parts_to_database_table_name(
                name=key, exchange=exchange,
                symbol=symbol, interval=interval
            )

            self.tables[(key, exchange, symbol, interval)] = table
        # end if

        insert_database_record_rows(
            engine=self.engine, session=self._session,
            tables=self.table_names, data=data[self.DATA],
            exchange=exchange, symbol=symbol, create=True,
            name=key, interval=interval, commit=True
        )

        if table is not None:
            self.table_names.add(table)
        # end if

        if data[self.DATA]:
            return True

        else:
            return False
        # end if
    # end process

    async def start(self) -> None:
        """Connects to the socket service."""

        self.engine = self.engine or create_engine(self.database)

        self.table_names = (
            self.table_names or
            extract_database_table_names(engine=self.engine)
        )

        self._session = (
            self._session or
            create_engine_session(engine=self.engine)
        )
    # end start
# end DatabaseCallback