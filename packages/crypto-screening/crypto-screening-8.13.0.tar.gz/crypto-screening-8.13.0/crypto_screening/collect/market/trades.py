# trades.py

from abc import ABCMeta
import datetime as dt
from typing import (
    Iterable, Dict, Optional, ClassVar, List, Tuple
)

from attrs import define

from represent import represent, Modifiers

import pandas as pd

from crypto_screening.dataset import PRICE, AMOUNT, SIDE

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
    "symbols_trades_market_state",
    "merge_assets_trades_market_states",
    "merge_symbols_trades_market_states",
    "assets_trades_market_state",
    "AssetsTradesMarketState",
    "SymbolsTradesMarketState",
    "symbols_to_assets_trades_market_state",
    "assets_to_symbols_trades_market_state",
    "TRADES_ATTRIBUTES"
]

AssetsPrices = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, float]]]]]
SymbolsPrices = Dict[str, Dict[str, List[Tuple[dt.datetime, float]]]]
AssetsSides = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, str]]]]]
SymbolsSides = Dict[str, Dict[str, List[Tuple[dt.datetime, str]]]]

TRADES_ATTRIBUTES = {
    "amounts": AMOUNT,
    "prices": PRICE,
    "sides": SIDE
}

@define(repr=False)
@represent
class TradesMarketState(MarketState, metaclass=ABCMeta):
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
    __modifiers__.excluded.extend(["amounts", "values", "sides"])

    ATTRIBUTES: ClassVar[Dict[str, str]] = TRADES_ATTRIBUTES
# end OrderbookMarketBase

AssetsMarketData = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, Dict[str, float]]]]]]
AssetsMarketDatasets = Dict[str, Dict[str, Dict[str, pd.DataFrame]]]

@define(repr=False)
@represent
class AssetsTradesMarketState(TradesMarketState, AssetsMarketState):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - amounts:
        The volume of the base asset of each trade.

    - price:
        The price of the base asset in the trade.

    - side:
        The side on the trade.

    >>> from crypto_screening.collect.market.trades import assets_trades_market_state
    >>>
    >>> state = assets_trades_market_state(...)
    """

    amounts: AssetsPrices
    prices: AssetsPrices
    sides: AssetsSides

    def amount(
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
            exchange=exchange, symbol=symbol, data=self.amounts,
            separator=separator, provider=self
        )
    # end amount

    def price(
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
            exchange=exchange, symbol=symbol, data=self.prices,
            separator=separator, provider=self
        )
    # end price

    def side(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, str]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.
        :param separator: The separator of the assets.

        :return: The ask price for the symbol.
        """

        return assets_market_values(
            exchange=exchange, symbol=symbol, data=self.sides,
            separator=separator, provider=self
        )
    # end side

    def in_amounts_prices(
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
            separator=separator, data=self.amounts
        )
    # end in_amounts_prices

    def in_prices_prices(
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
            separator=separator, data=self.prices
        )
    # end in_prices_prices

    def in_sides_prices(
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
            separator=separator, data=self.sides
        )
    # end in_sides_prices
# end AssetsMarketStates

SymbolsMarketData = Dict[str, Dict[str, List[Tuple[dt.datetime, Dict[str, float]]]]]
SymbolsMarketDatasets = Dict[str, Dict[str, pd.DataFrame]]

@define(repr=False)
@represent
class SymbolsTradesMarketState(TradesMarketState, SymbolsMarketState):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - amounts:
        The volume of the base asset of each trade.

    - price:
        The price of the base asset in the trade.

    - side:
        The side on the trade.

    >>> from crypto_screening.collect.market.trades import symbols_trades_market_state
    >>>
    >>> state = symbols_trades_market_state(...)
    """

    amounts: SymbolsPrices
    prices: SymbolsPrices
    sides: SymbolsSides

    def amount(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.amounts,
            provider=self
        )
    # end amount

    def price(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.prices,
            provider=self
        )
    # end price

    def side(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, str]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.sides, provider=self
        )
    # end side

    def in_amounts_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.amounts
        )
    # end in_amounts_prices

    def in_prices_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.prices
        )
    # end in_prices_prices

    def in_sides_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.sides
        )
    # end in_sides_prices
# end SymbolsMarketStates

def assets_trades_market_state(
        screeners: Optional[Iterable[BaseScreener]] = None,
        separator: Optional[str] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> AssetsTradesMarketState:
    """
    Fetches the values and relations between the assets.

    :param screeners: The price screeners.
    :param separator: The separator of the assets.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    return AssetsTradesMarketState(
        screeners=screeners,
        **assets_market_state_data(
            columns=TradesMarketState.ATTRIBUTES,
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )
    )
# end assets_tickers_market_state

def symbols_trades_market_state(
        screeners: Optional[Iterable[BaseScreener]] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> SymbolsTradesMarketState:
    """
    Fetches the values and relations between the assets.

    :param screeners: The price screeners.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    return SymbolsTradesMarketState(
        screeners=screeners,
        **symbols_market_state_data(
            columns=TradesMarketState.ATTRIBUTES, screeners=screeners,
            length=length, adjust=adjust
        )
    )
# end symbols_tickers_market_state

def merge_symbols_trades_market_states(
        states: Iterable[SymbolsTradesMarketState], sort: Optional[bool] = True
) -> SymbolsTradesMarketState:
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

    return SymbolsTradesMarketState(
        screeners=screeners,
        **merge_symbols_market_states_data(
            states, data={
                name: {} for name in TradesMarketState.ATTRIBUTES
            }, sort=sort
        )
    )
# end merge_symbols_tickers_market_states

def merge_assets_trades_market_states(
        states: Iterable[AssetsTradesMarketState], sort: Optional[bool] = True
) -> AssetsTradesMarketState:
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

    return AssetsTradesMarketState(
        screeners=screeners,
        **merge_assets_market_states_data(
            states, data={
                name: {} for name in TradesMarketState.ATTRIBUTES
            }, sort=sort
        )
    )
# end merge_assets_tickers_market_states

def assets_to_symbols_trades_market_state(
        state: AssetsTradesMarketState,
        separator: Optional[str] = None
) -> SymbolsTradesMarketState:
    """
    Converts an assets market state into a symbols market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return SymbolsTradesMarketState(
        **{
            name: assets_to_symbols_data(
                data=getattr(state, name), separator=separator
            ) for name in TradesMarketState.ATTRIBUTES
        }
    )
# end assets_to_symbols_tickers_market_state

def symbols_to_assets_trades_market_state(
        state: SymbolsTradesMarketState,
        separator: Optional[str] = None
) -> AssetsTradesMarketState:
    """
    Converts a symbols market state into an assets market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return AssetsTradesMarketState(
        **{
            name: symbol_to_assets_data(
                data=getattr(state, name), separator=separator
            ) for name in TradesMarketState.ATTRIBUTES
        }
    )
# end symbols_to_assets_tickers_market_state