# protocols.py

import datetime as dt
from typing import Protocol, List, Union

import pandas as pd

__all__ = [
    "BaseScreenerProtocol",
    "BaseMarketScreenerProtocol",
    "DataCollectorProtocol"
]

class DataCollectorProtocol(Protocol):
    """A class for the base data collector protocol."""

    location: str

    delay: Union[float, dt.timedelta]
    cancel: Union[float, dt.timedelta]
# end DataCollectorProtocol

class BaseScreenerProtocol(DataCollectorProtocol):
    """A class for the base screener protocol."""

    symbol: str
    exchange: str

    market: pd.DataFrame
# end BaseScreenerProtocol

class BaseMarketScreenerProtocol(DataCollectorProtocol):
    """A class for the base multi-screener protocol."""

    screeners: List[BaseScreenerProtocol]
# end BaseMarketScreenerProtocol