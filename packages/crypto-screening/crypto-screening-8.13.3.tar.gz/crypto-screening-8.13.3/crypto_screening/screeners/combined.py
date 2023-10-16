# combined.py

import datetime as dt
from abc import ABCMeta
from typing import (
    Dict, Optional, Iterable, Any, Union,
    List, Type, Callable, Protocol
)

from crypto_screening.screeners.base import BaseScreener
from crypto_screening.screeners.orderbook import (
    orderbook_market_screener, OrderbookScreener,
    OrderbookMarketRecorder, OrderbookMarketScreener
)
from crypto_screening.screeners.ohlcv import (
    ohlcv_market_screener, OHLCVScreener,
    OHLCVMarketScreener, OHLCVMarketRecorder,
    merge_screeners
)
from crypto_screening.screeners.trades import (
    trades_market_screener, TradesScreener,
    TradesMarketScreener, TradesMarketRecorder
)
from crypto_screening.screeners.tickers import (
    tickers_market_screener, TickersScreener,
    TickersMarketScreener, TickersMarketRecorder
)
from crypto_screening.screeners.callbacks.base import BaseCallback
from crypto_screening.screeners.recorder import (
    MarketScreener, MarketRecorder, MarketHandler
)

__all__ = [
    "CombinedMarketRecorder",
    "CombinedMarketScreener",
    "combined_market_screener",
    "CATEGORIES",
    "Category",
    "OrderbookCategory",
    "TradesCategory",
    "TickersCategory",
    "OHLCVCategory",
    "Categories"
]

RecorderParameters = Dict[str, Union[Iterable[str], Dict[str, Callable]]]

class Category(Protocol, metaclass=ABCMeta):
    """A class to represent a category."""

    __slots__ = ()

    screener: Type[BaseScreener]
    market: Type[MarketScreener]
    recorder: Type[MarketRecorder]
    compositor: Callable[..., MarketScreener]
# end Category

class OrderbookCategory(Category, metaclass=ABCMeta):
    """A class to represent a category."""

    __slots__ = ()

    screener = OrderbookScreener
    market = OrderbookMarketScreener
    recorder = OrderbookMarketRecorder
    compositor = orderbook_market_screener
# end OrderbookCategory

class TickersCategory(Category, metaclass=ABCMeta):
    """A class to represent a category."""

    __slots__ = ()

    screener = TickersScreener
    market = TickersMarketScreener
    recorder = TickersMarketRecorder
    compositor = tickers_market_screener
# end TickersCategory

class TradesCategory(Category, metaclass=ABCMeta):
    """A class to represent a category."""

    __slots__ = ()

    screener = TradesScreener
    market = TradesMarketScreener
    recorder = TradesMarketRecorder
    compositor = trades_market_screener
# end TradesCategory

class OHLCVCategory(Category, metaclass=ABCMeta):
    """A class to represent a category."""

    __slots__ = ()

    screener = OHLCVScreener
    market = OHLCVMarketScreener
    recorder = OHLCVMarketRecorder
    compositor = ohlcv_market_screener
# end OHLCVCategory

CATEGORIES = (
    OHLCVCategory,
    TradesCategory,
    TickersCategory,
    OrderbookCategory
)

class Categories:
    """A class to represent a collection of all categories."""

    orderbook = OrderbookCategory
    tickers = TickersCategory
    trades = TradesCategory
    ohlcv = OHLCVCategory
    categories = CATEGORIES
# end Categories

CategoryBase = Union[
    OHLCVCategory,
    TradesCategory,
    TickersCategory,
    OrderbookCategory
]

def gather(recorders: Iterable):
    """
    Gathers the functions to record the data.

    :param recorders: The data recorders.

    :return: The new data recorder function.
    """

    async def record(data: Any, timestamp: float) -> bool:
        """
        Records the data for the screeners.

        :param data: The data to record.
        :param timestamp: The timestamp of the data.

        :return: The boolean flag.
        """

        for recorder in recorders:
            await recorder(data, timestamp)
        # end for

        return True
    # end record

    return record
# end gather

class CombinedMarketRecorder(MarketRecorder):
    """
    A class to represent a crypto data feed recorder.
    This object passes the record method to the handler object to record
    the data fetched by the handler.

    Parameters:

    - recorders:
        The Recorder objects to contron and collect data from, into the markets.

    >>> from crypto_screening.screeners.combined import CombinedMarketRecorder
    >>>
    >>> recorder = CombinedMarketRecorder(...)
    """

    def __init__(self, recorders: Iterable[MarketRecorder]) -> None:
        """
        Defines the class attributes.

        :param recorders: The categories for the market screener.
        """

        screeners = []
        structure: Dict[str, List[str]] = {}

        for recorder in recorders:
            structure.update(recorder.structure())
            screeners.extend(recorder.screeners)
        # end for

        screeners = list(set(screeners))

        super().__init__(screeners=screeners)

        self.recorders = list(recorders)
    # end __init__

    def update_screeners(self) -> None:
        """Updates the records of the object."""

        super().update_screeners()

        for recorder in self.recorders:
            recorder.update_screeners()
        # end for
    # end update_screeners

    def parameters(self) -> RecorderParameters:
        """
        Returns the order book parameters.

        :return: The order book parameters.
        """

        channels = []
        callback_recorders = {}

        for recorder in self.recorders:
            channels.extend(recorder.parameters()["channels"])

            for key, value in recorder.parameters()["callbacks"].items():
                (
                    callback_recorders.
                    setdefault(key, []).
                    append(value)
                )
        # end for

        callbacks = {}

        for key, recorders in callback_recorders.items():
            callbacks[key] = gather(recorders)
        # end for

        return dict(
            channels=list(set(channels)),
            callbacks=callbacks,
            max_depth=1
        )
    # end parameters
# end CombinedMarketRecorder

class CombinedMarketScreener(MarketScreener):
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

    - handler:
        The handler object to handle the data feed.

    - recorder:
        The recorder object to record the data of the market from the feed.

    - screeners:
        The screener object to control and fill with data.

    - refresh:
        The duration of time between each refresh. 0 means no refresh.

    - amount:
        The amount of symbols for each symbols group for an exchange.

    - limited:
        The value to limit the running screeners to active exchanges.

    >>> from crypto_screening.screeners.combined import combined_market_screener
    >>>
    >>> structure = {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}
    >>>
    >>> screener = combined_market_screener(data=structure)
    >>> screener.run()
    """

    recorder: CombinedMarketRecorder

    def __init__(
            self,
            markets: Iterable[MarketScreener],
            recorder: CombinedMarketRecorder,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            refresh: Optional[Union[float, dt.timedelta, bool]] = None,
            limited: Optional[bool] = None,
            handler: Optional[MarketHandler] = None,
            amount: Optional[int] = None
    ) -> None:
        """
        Creates the class attributes.

        :param location: The saving location for the data.
        :param markets: The market screeners.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param limited: The value to limit the screeners to active only.
        :param refresh: The refresh time for rerunning.
        :param handler: The handler object for the market data.
        :param amount: The maximum amount of symbols for each feed.
        :param recorder: The recorder object for recording the data.
        """

        screeners = []

        for market in markets:
            screeners.extend(market.screeners)
        # end for

        super().__init__(
            location=location, cancel=cancel,
            delay=delay, recorder=recorder,
            screeners=screeners, handler=handler, limited=limited,
            amount=amount, refresh=refresh
        )

        self.markets = markets
    # end __init__

    def update_screeners(self) -> None:
        """Updates the records of the object."""

        super().update_screeners()

        self.recorder.update_screeners()
    # end update_screeners

    def merge_screeners(self) -> None:
        """Connects the screeners to the recording object."""

        merge_screeners(
            orderbook_screeners=self.orderbook_screeners,
            ohlcv_screeners=self.ohlcv_screeners
        )
    # end merge_screeners
# end CombinedMarketScreener

def combined_market_screener(
        data: Dict[str, Iterable[Union[str, Dict[str, Iterable[str]]]]],
        categories: Optional[Type[CategoryBase]] = None,
        location: Optional[str] = None,
        cancel: Optional[Union[float, dt.timedelta]] = None,
        delay: Optional[Union[float, dt.timedelta]] = None,
        limited: Optional[bool] = None,
        handler: Optional[MarketHandler] = None,
        amount: Optional[int] = None,
        memory: Optional[int] = None,
        callbacks: Optional[Iterable[BaseCallback]] = None,
        refresh: Optional[Union[float, dt.timedelta, bool]] = None,
        recorder: Optional[CombinedMarketRecorder] = None,
) -> CombinedMarketScreener:
    """
    Creates the market screener object for the data.

    :param data: The market data.
    :param categories: The categories for the markets.
    :param handler: The handler object for the market data.
    :param limited: The value to limit the screeners to active only.
    :param refresh: The refresh time for rerunning.
    :param amount: The maximum amount of symbols for each feed.
    :param recorder: The recorder object for recording the data.
    :param location: The saving location for the data.
    :param delay: The delay for the process.
    :param cancel: The cancel time for the loops.
    :param callbacks: The callbacks for the service.
    :param memory: The memory limitation of the market dataset.

    :return: The market screener object.
    """

    if categories is None:
        categories = CATEGORIES
    # end if

    categories = list(categories)

    markets: List[MarketScreener] = []

    if (OHLCVCategory in categories) and (OrderbookCategory in categories):
        categories.remove(OHLCVCategory)
        categories.remove(OrderbookCategory)

        orderbook_market = orderbook_market_screener(
            handler=handler, data=data, callbacks=callbacks,
            location=location, amount=amount, cancel=cancel,
            delay=delay, limited=limited, refresh=refresh, memory=memory
        )
        orderbook_market.recorder.disable()

        ohlcv_market = ohlcv_market_screener(
            handler=handler, data=data, callbacks=callbacks,
            location=location, amount=amount, cancel=cancel,
            delay=delay, limited=limited, refresh=refresh,
            memory=memory, screeners=orderbook_market.screeners
        )
        ohlcv_market.merge_screeners()

        markets.append(orderbook_market)
        markets.append(ohlcv_market)
    # end if

    markets.extend(
        category.compositor(
            handler=handler, data=data, callbacks=callbacks,
            location=location, amount=amount, cancel=cancel,
            delay=delay, limited=limited, refresh=refresh, memory=memory
        ) for category in set(categories)
    )

    market = CombinedMarketScreener(
        markets=markets, recorder=recorder or CombinedMarketRecorder(
            recorders=[market.recorder for market in markets]
        ), handler=handler, location=location, amount=amount, cancel=cancel,
        delay=delay, limited=limited, refresh=refresh
    )

    return market
# end combined_market_screener