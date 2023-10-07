# ohlcv.py

from abc import ABCMeta
import datetime as dt
from typing import (
    Iterable, Dict, Optional, ClassVar, List, Tuple
)

from attrs import define

from represent import represent, Modifiers

import pandas as pd

from market_break.dataset import OPEN, HIGH, LOW, CLOSE, VOLUME

from crypto_screening.foundation.screener import BaseScreener
from crypto_screening.collect.market.state import (
    MarketState, assets_market_values, SymbolsMarketState,
    is_symbol_in_assets_market_values, symbols_market_values,
    is_symbol_in_symbols_market_values, merge_symbols_market_states_data,
    assets_to_symbols_data, assets_market_state_data,
    symbol_to_assets_data, symbols_market_state_data,
    merge_assets_market_states_data, AssetsMarketState
)

__all__ = [
    "symbols_ohlcv_market_state",
    "merge_assets_ohlcv_market_states",
    "merge_symbols_ohlcv_market_states",
    "assets_ohlcv_market_state",
    "AssetsOHLCVMarketState",
    "SymbolsOHLCVMarketState",
    "symbols_to_assets_ohlcv_market_state",
    "assets_to_symbols_ohlcv_market_state",
    "OHLCV_ATTRIBUTES"
]

AssetsPrices = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, float]]]]]
SymbolsPrices = Dict[str, Dict[str, List[Tuple[dt.datetime, float]]]]

OHLCV_ATTRIBUTES = {
    "opens": OPEN,
    "highs": HIGH,
    "lows": LOW,
    "closes": CLOSE,
    "volumes": VOLUME
}

@define(repr=False)
@represent
class OHLCVMarketState(MarketState, metaclass=ABCMeta):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.
    """

    __modifiers__: ClassVar[Modifiers] = Modifiers(**MarketState.__modifiers__)
    __modifiers__.excluded.extend(["open", "high", "low", "close", "volume"])

    ATTRIBUTES: ClassVar[Dict[str, str]] = OHLCV_ATTRIBUTES
# end OrderbookMarketBase

AssetsMarketData = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, Dict[str, float]]]]]]
AssetsMarketDatasets = Dict[str, Dict[str, Dict[str, pd.DataFrame]]]

@define(repr=False)
@represent
class AssetsOHLCVMarketState(OHLCVMarketState, AssetsMarketState):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - opens:
        The open price values of the symbol.

    - high:
        The open price values of the symbol.

    - low:
        The low price values of the symbol.

    - close:
        The close price values of the symbol.

    - volume:
        The volume price values of the symbol.

    >>> from crypto_screening.collect.market.ohlcv import assets_ohlcv_market_state
    >>>
    >>> state = assets_ohlcv_market_state(...)
    """

    opens: AssetsPrices
    highs: AssetsPrices
    lows: AssetsPrices
    closes: AssetsPrices
    volumes: AssetsPrices

    def open(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.
        :param separator: The separator of the assets.

        :return: The bid price for the symbol.
        """

        return assets_market_values(
            exchange=exchange, symbol=symbol, data=self.opens,
            separator=separator, provider=self
        )
    # end bid

    def high(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.
        :param separator: The separator of the assets.

        :return: The ask price for the symbol.
        """

        return assets_market_values(
            exchange=exchange, symbol=symbol, data=self.highs,
            separator=separator, provider=self
        )
    # end ask

    def low(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.
        :param separator: The separator of the assets.

        :return: The bid price for the symbol.
        """

        return assets_market_values(
            exchange=exchange, symbol=symbol, data=self.lows,
            separator=separator, provider=self
        )
    # end bid_volume

    def close(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.
        :param separator: The separator of the assets.

        :return: The ask price for the symbol.
        """

        return assets_market_values(
            exchange=exchange, symbol=symbol, data=self.closes,
            separator=separator, provider=self
        )
    # end ask_volume

    def volume(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.
        :param separator: The separator of the assets.

        :return: The ask price for the symbol.
        """

        return assets_market_values(
            exchange=exchange, symbol=symbol, data=self.closes,
            separator=separator, provider=self
        )
    # end ask_volume

    def in_open_prices(
            self,
            exchange: str,
            symbol: str,
            separator: Optional[str] = None
    ) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return is_symbol_in_assets_market_values(
            exchange=exchange, symbol=symbol,
            separator=separator, data=self.opens
        )
    # end in_bids_prices

    def in_high_prices(
            self,
            exchange: str,
            symbol: str,
            separator: Optional[str] = None
    ) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return is_symbol_in_assets_market_values(
            exchange=exchange, symbol=symbol,
            separator=separator, data=self.highs
        )
    # end in_asks_prices

    def in_low_prices(
            self,
            exchange: str,
            symbol: str,
            separator: Optional[str] = None
    ) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return is_symbol_in_assets_market_values(
            exchange=exchange, symbol=symbol,
            separator=separator, data=self.lows
        )
    # end in_bids_volume_prices

    def in_close_prices(
            self,
            exchange: str,
            symbol: str,
            separator: Optional[str] = None
    ) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return is_symbol_in_assets_market_values(
            exchange=exchange, symbol=symbol,
            separator=separator, data=self.closes
        )
    # end in_asks_volume_prices

    def in_volume_prices(
            self,
            exchange: str,
            symbol: str,
            separator: Optional[str] = None
    ) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return is_symbol_in_assets_market_values(
            exchange=exchange, symbol=symbol,
            separator=separator, data=self.volumes
        )
    # end in_asks_volume_prices
# end AssetsMarketStates

SymbolsMarketData = Dict[str, Dict[str, List[Tuple[dt.datetime, Dict[str, float]]]]]
SymbolsMarketDatasets = Dict[str, Dict[str, pd.DataFrame]]

@define(repr=False)
@represent
class SymbolsOHLCVMarketState(OHLCVMarketState, SymbolsMarketState):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - opens:
        The open price values of the symbol.

    - high:
        The open price values of the symbol.

    - low:
        The low price values of the symbol.

    - close:
        The close price values of the symbol.

    - volume:
        The volume price values of the symbol.

    >>> from crypto_screening.collect.market.ohlcv import symbols_ohlcv_market_state
    >>>
    >>> state = symbols_ohlcv_market_state(...)
    """

    opens: SymbolsPrices
    highs: SymbolsPrices
    lows: SymbolsPrices
    closes: SymbolsPrices
    volumes: SymbolsPrices

    def open(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.

        :return: The bid price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.opens, provider=self
        )
    # end open

    def high(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.highs, provider=self
        )
    # end high

    def low(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.

        :return: The bid price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.lows, provider=self
        )
    # end low

    def close(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.closes, provider=self
        )
    # end close

    def volume(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.volumes, provider=self
        )
    # end volume

    def in_open_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.opens
        )
    # end in_open_prices

    def in_high_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.highs
        )
    # end in_high_prices

    def in_low_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.lows
        )
    # end in_low_prices

    def in_close_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The in_asks_volume_prices value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.closes
        )
    # end in_close_prices

    def in_volume_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The in_asks_volume_prices value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.volumes
        )
    # end in_volume_prices
# end SymbolsMarketStates

def assets_ohlcv_market_state(
        screeners: Optional[Iterable[BaseScreener]] = None,
        separator: Optional[str] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> AssetsOHLCVMarketState:
    """
    Fetches the values and relations between the assets.

    :param screeners: The price screeners.
    :param separator: The separator of the assets.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    return AssetsOHLCVMarketState(
        screeners=screeners,
        **assets_market_state_data(
            columns=OHLCVMarketState.ATTRIBUTES,
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )
    )
# end assets_ohlcv_market_state

def symbols_ohlcv_market_state(
        screeners: Optional[Iterable[BaseScreener]] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> SymbolsOHLCVMarketState:
    """
    Fetches the values and relations between the assets.

    :param screeners: The price screeners.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    return SymbolsOHLCVMarketState(
        screeners=screeners,
        **symbols_market_state_data(
            columns=OHLCVMarketState.ATTRIBUTES, screeners=screeners,
            length=length, adjust=adjust
        )
    )
# end symbols_ohlcv_market_state

def merge_symbols_ohlcv_market_states(
        states: Iterable[SymbolsOHLCVMarketState], sort: Optional[bool] = True
) -> SymbolsOHLCVMarketState:
    """
    Concatenates the states of the market.

    :param states: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    screeners = set()

    for state in states:
        screeners.update(state.screeners)
    # end for

    return SymbolsOHLCVMarketState(
        screeners=screeners,
        **merge_symbols_market_states_data(
            states, data={
                name: {} for name in OHLCVMarketState.ATTRIBUTES
            }, sort=sort
        )
    )
# end merge_symbols_ohlcv_market_states

def merge_assets_ohlcv_market_states(
        states: Iterable[AssetsOHLCVMarketState], sort: Optional[bool] = True
) -> AssetsOHLCVMarketState:
    """
    Concatenates the states of the market.

    :param states: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    screeners = set()

    for state in states:
        screeners.update(state.screeners)
    # end for

    return AssetsOHLCVMarketState(
        screeners=screeners,
        **merge_assets_market_states_data(
            states, data={
                name: {} for name in OHLCVMarketState.ATTRIBUTES
            }, sort=sort
        )
    )
# end merge_assets_ohlcv_market_states

def assets_to_symbols_ohlcv_market_state(
        state: AssetsOHLCVMarketState,
        separator: Optional[str] = None
) -> SymbolsOHLCVMarketState:
    """
    Converts an assets market state into a symbols market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return SymbolsOHLCVMarketState(
        **{
            name: assets_to_symbols_data(
                data=getattr(state, name), separator=separator
            ) for name in OHLCVMarketState.ATTRIBUTES
        }
    )
# end assets_to_symbols_ohlcv_market_state

def symbols_to_assets_ohlcv_market_state(
        state: SymbolsOHLCVMarketState,
        separator: Optional[str] = None
) -> AssetsOHLCVMarketState:
    """
    Converts a symbols market state into an assets market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return AssetsOHLCVMarketState(
        **{
            name: symbol_to_assets_data(
                data=getattr(state, name), separator=separator
            ) for name in OHLCVMarketState.ATTRIBUTES
        }
    )
# end symbols_to_assets_ohlcv_market_state