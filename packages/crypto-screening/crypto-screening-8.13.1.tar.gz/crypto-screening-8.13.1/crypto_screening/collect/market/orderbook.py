# orderbook.py

from abc import ABCMeta
import datetime as dt
from typing import (
    Iterable, Dict, Optional, ClassVar, List, Tuple
)

from attrs import define

from represent import represent, Modifiers

import pandas as pd

from crypto_screening.foundation.screener import BaseScreener
from crypto_screening.collect.market.state.base import ORDERBOOK_ATTRIBUTES
from crypto_screening.collect.market.state import (
    MarketState, assets_market_values, AssetsMarketState,
    is_symbol_in_assets_market_values, symbols_market_values,
    is_symbol_in_symbols_market_values, merge_symbols_market_states_data,
    assets_to_symbols_data, assets_market_state_data,
    symbol_to_assets_data, symbols_market_state_data,
    merge_assets_market_states_data, SymbolsMarketState
)

__all__ = [
    "symbols_orderbook_market_state",
    "merge_assets_orderbook_market_states",
    "merge_symbols_orderbook_market_states",
    "assets_orderbook_market_state",
    "AssetsOrderbookMarketState",
    "SymbolsOrderbookMarketState",
    "symbols_to_assets_orderbook_market_state",
    "assets_to_symbols_orderbook_market_state",
    "ORDERBOOK_ATTRIBUTES"
]

AssetsPrices = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, float]]]]]
SymbolsPrices = Dict[str, Dict[str, List[Tuple[dt.datetime, float]]]]

@define(repr=False)
@represent
class OrderbookMarketState(MarketState, metaclass=ABCMeta):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.
    """

    __modifiers__: ClassVar[Modifiers] = Modifiers(
        **MarketState.__modifiers__
    )
    __modifiers__.excluded.extend(["bids", "asks", "bids_volume", "asks_volume"])

    ATTRIBUTES: ClassVar[Dict[str, str]] = ORDERBOOK_ATTRIBUTES
# end OrderbookMarketBase

@define(repr=False)
@represent
class AssetsOrderbookMarketState(OrderbookMarketState, AssetsMarketState):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - bids:
        The bids values of the assets.

    - asks:
        The asks values of the assets.

    - bids_volume:
        The bids volume values of the assets.

    - asks_volume:
        The asks volume values of the assets.

    >>> from crypto_screening.collect.market.orderbook import assets_orderbook_market_state
    >>>
    >>> state = assets_orderbook_market_state(...)
    """

    bids: AssetsPrices
    asks: AssetsPrices
    bids_volume: AssetsPrices
    asks_volume: AssetsPrices

    def bid(
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
            exchange=exchange, symbol=symbol, data=self.bids,
            separator=separator, provider=self
        )
    # end bid

    def ask(
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
            exchange=exchange, symbol=symbol, data=self.asks,
            separator=separator, provider=self
        )
    # end ask

    def bid_volume(
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
            exchange=exchange, symbol=symbol, data=self.bids_volume,
            separator=separator, provider=self
        )
    # end bid_volume

    def ask_volume(
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
            exchange=exchange, symbol=symbol, data=self.asks_volume,
            separator=separator, provider=self
        )
    # end ask_volume

    def in_bids_prices(
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
            separator=separator, data=self.bids
        )
    # end in_bids_prices

    def in_asks_prices(
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
            separator=separator, data=self.asks
        )
    # end in_asks_prices

    def in_bids_volume_prices(
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
            separator=separator, data=self.bids_volume
        )
    # end in_bids_volume_prices

    def in_asks_volume_prices(
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
            separator=separator, data=self.asks_volume
        )
    # end in_asks_volume_prices
# end AssetsMarketStates

SymbolsMarketData = Dict[str, Dict[str, List[Tuple[dt.datetime, Dict[str, float]]]]]
SymbolsMarketDatasets = Dict[str, Dict[str, pd.DataFrame]]

@define(repr=False)
@represent
class SymbolsOrderbookMarketState(OrderbookMarketState, SymbolsMarketState):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - bids:
        The bids values of the assets.

    - asks:
        The asks values of the assets.

    - bids_volume:
        The bids volume values of the assets.

    - asks_volume:
        The asks volume values of the assets.

    >>> from crypto_screening.collect.market.orderbook import symbols_orderbook_market_state
    >>>
    >>> state = symbols_orderbook_market_state(...)
    """

    bids: SymbolsPrices
    asks: SymbolsPrices
    bids_volume: SymbolsPrices
    asks_volume: SymbolsPrices

    def bid(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.

        :return: The bid price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.bids, provider=self
        )
    # end bid

    def ask(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.asks, provider=self
        )
    # end ask

    def bid_volume(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.

        :return: The bid price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.bids_volume, provider=self
        )
    # end bid_volume

    def ask_volume(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.asks_volume, provider=self
        )
    # end ask_volume

    def in_bids_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.bids
        )
    # end in_bids_prices

    def in_asks_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.asks
        )
    # end in_asks_prices

    def in_bids_volume_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.bids_volume
        )
    # end in_bids_volume_prices

    def in_asks_volume_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The in_asks_volume_prices value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.asks_volume
        )
    # end in_asks_volume_prices
# end SymbolsMarketStates

def assets_orderbook_market_state(
        screeners: Optional[Iterable[BaseScreener]] = None,
        separator: Optional[str] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> AssetsOrderbookMarketState:
    """
    Fetches the values and relations between the assets.

    :param screeners: The price screeners.
    :param separator: The separator of the assets.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    return AssetsOrderbookMarketState(
        screeners=screeners,
        **assets_market_state_data(
            columns=OrderbookMarketState.ATTRIBUTES,
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )
    )
# end assets_orderbook_market_state

def symbols_orderbook_market_state(
        screeners: Optional[Iterable[BaseScreener]] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> SymbolsOrderbookMarketState:
    """
    Fetches the values and relations between the assets.

    :param screeners: The price screeners.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    return SymbolsOrderbookMarketState(
        screeners=screeners,
        **symbols_market_state_data(
            columns=OrderbookMarketState.ATTRIBUTES, screeners=screeners,
            length=length, adjust=adjust
        )
    )
# end symbols_orderbook_market_state

def merge_symbols_orderbook_market_states(
        states: Iterable[SymbolsOrderbookMarketState], sort: Optional[bool] = True
) -> SymbolsOrderbookMarketState:
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

    return SymbolsOrderbookMarketState(
        screeners=screeners,
        **merge_symbols_market_states_data(
            states, data={
                name: {} for name in OrderbookMarketState.ATTRIBUTES
            }, sort=sort
        )
    )
# end merge_symbols_orderbook_market_states

def merge_assets_orderbook_market_states(
        states: Iterable[AssetsOrderbookMarketState], sort: Optional[bool] = True
) -> AssetsOrderbookMarketState:
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

    return AssetsOrderbookMarketState(
        screeners=screeners,
        **merge_assets_market_states_data(
            states, data={
                name: {} for name in OrderbookMarketState.ATTRIBUTES
            }, sort=sort
        )
    )
# end merge_assets_orderbook_market_states

def assets_to_symbols_orderbook_market_state(
        state: AssetsOrderbookMarketState,
        separator: Optional[str] = None
) -> SymbolsOrderbookMarketState:
    """
    Converts an assets market state into a symbols market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return SymbolsOrderbookMarketState(
        **{
            name: assets_to_symbols_data(
                data=getattr(state, name), separator=separator
            ) for name in OrderbookMarketState.ATTRIBUTES
        }
    )
# end assets_to_symbols_orderbook_market_state

def symbols_to_assets_orderbook_market_state(
        state: SymbolsOrderbookMarketState,
        separator: Optional[str] = None
) -> AssetsOrderbookMarketState:
    """
    Converts a symbols market state into an assets market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return AssetsOrderbookMarketState(
        **{
            name: symbol_to_assets_data(
                data=getattr(state, name), separator=separator
            ) for name in OrderbookMarketState.ATTRIBUTES
        }
    )
# end symbols_to_assets_orderbook_market_state