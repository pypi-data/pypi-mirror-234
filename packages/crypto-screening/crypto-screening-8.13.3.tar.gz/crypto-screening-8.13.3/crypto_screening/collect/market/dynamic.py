# dynamic.py

import datetime as dt
from abc import ABCMeta
from typing import (
    Iterable, Dict, Optional, List, Tuple, Union
)

from attrs import define

from represent import represent

from crypto_screening.screeners import BaseScreener
from crypto_screening.collect.market.state import (
    AssetsMarketState, merge_symbols_market_states_data,
    assets_to_symbols_data, assets_market_state_data,
    symbol_to_assets_data, symbols_market_state_data,
    merge_assets_market_states_data, SymbolsMarketState,
    MarketState
)

__all__ = [
    "BaseDynamicMarketState",
    "AssetsDynamicMarketState",
    "SymbolsDynamicMarketState",
    "assets_dynamic_market_state",
    "assets_to_symbols_dynamic_market_state",
    "symbols_dynamic_market_state",
    "symbols_to_assets_dynamic_market_state",
    "merge_symbols_dynamic_market_states",
    "merge_assets_dynamic_market_states"
]

AssetsPrices = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, float]]]]]
SymbolsPrices = Dict[str, Dict[str, List[Tuple[dt.datetime, float]]]]

@define(repr=False, init=False, slots=False)
@represent
class BaseDynamicMarketState(MarketState, metaclass=ABCMeta):
    """
    A class to represent the current market state.

    This class is a base class for containers of structured market data,
    with assets structure.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - attributes:
        The attributes of the data.

    - data:
        The data to store.
    """

    def __init__(
            self,
            screeners: Iterable[BaseScreener],
            data: Union[Dict[str, AssetsPrices], Dict[str, SymbolsPrices]]
    ) -> None:
        """
        Defines the attributes of the market state.

        :param screeners: The screeners of the data.
        :param data: The data to store.
        """

        self.attributes = tuple(set(data.keys()))
        type(self).ATTRIBUTES = {name: name for name in data.keys()}

        for key, value in data.items():
            setattr(self, key, value)
        # end for

        super().__init__(screeners=screeners)
    # end __init__
# end AssetsDynamicMarketState

@define(repr=False, init=False)
@represent
class AssetsDynamicMarketState(BaseDynamicMarketState, AssetsMarketState):
    """
    A class to represent the current market state.

    This class is a base class for containers of structured market data,
    with assets structure.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - attributes:
        The attributes of the data.

    - data:
        The data to store.

    >>> from crypto_screening.collect.market.dynamic import assets_dynamic_market_state
    >>>
    >>> state = assets_dynamic_market_state(...)
    """

    def __init__(
            self,
            screeners: Iterable[BaseScreener],
            data: Dict[str, AssetsPrices]
    ) -> None:
        """
        Defines the attributes of the market state.

        :param screeners: The screeners of the data.
        :param data: The data to store.
        """

        super().__init__(screeners=screeners, data=data)
    # end __init__
# end AssetsDynamicMarketState

@define(repr=False, init=False)
@represent
class SymbolsDynamicMarketState(BaseDynamicMarketState, SymbolsMarketState):
    """
    A class to represent the current market state.

    This class is a base class for containers of structured market data,
    with symbols structure.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - attributes:
        The attributes of the data.

    - data:
        The data to store.

    >>> from crypto_screening.collect.market.dynamic import symbols_dynamic_market_state
    >>>
    >>> state = symbols_dynamic_market_state(...)
    """

    def __init__(
            self,
            screeners: Iterable[BaseScreener],
            data: Dict[str, SymbolsPrices]
    ) -> None:
        """
        Defines the attributes of the market state.

        :param screeners: The screeners of the data.
        :param data: The data to store.
        """

        super().__init__(screeners=screeners, data=data)
    # end __init__
# end SymbolsDynamicMarketState

def assets_dynamic_market_state(
        columns: Iterable[str],
        screeners: Optional[Iterable[BaseScreener]] = None,
        separator: Optional[str] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> AssetsDynamicMarketState:
    """
    Fetches the values and relations between the assets.

    :param columns: The columns of data.
    :param screeners: The price screeners.
    :param separator: The separator of the assets.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    return AssetsDynamicMarketState(
        screeners=screeners,
        data=assets_market_state_data(
            columns={name: name for name in columns},
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )
    )
# end assets_dynamic_market_state

def symbols_dynamic_market_state(
        columns: Iterable[str],
        screeners: Optional[Iterable[BaseScreener]] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> SymbolsDynamicMarketState:
    """
    Fetches the values and relations between the assets.

    :param columns: The columns of data.
    :param screeners: The price screeners.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    return SymbolsDynamicMarketState(
        screeners=screeners,
        data=symbols_market_state_data(
            columns={name: name for name in columns},
            screeners=screeners, length=length, adjust=adjust
        )
    )
# end symbols_dynamic_market_state

def merge_symbols_dynamic_market_states(
        states: Iterable[SymbolsDynamicMarketState],
        attributes: Iterable[str],
        sort: Optional[bool] = True
) -> SymbolsDynamicMarketState:
    """
    Concatenates the states of the market.

    :param attributes: The attributes of data.
    :param states: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    screeners = set()

    for state in states:
        screeners.update(state.screeners)
    # end for

    return SymbolsDynamicMarketState(
        screeners=screeners,
        **merge_symbols_market_states_data(
            states, data={name: {} for name in attributes},
            sort=sort
        )
    )
# end merge_symbols_orderbook_market_states

def merge_assets_dynamic_market_states(
        states: Iterable[AssetsDynamicMarketState],
        attributes: Iterable[str],
        sort: Optional[bool] = True
) -> AssetsDynamicMarketState:
    """
    Concatenates the states of the market.

    :param attributes: The attributes of data.
    :param states: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    screeners = set()

    for state in states:
        screeners.update(state.screeners)
    # end for

    return AssetsDynamicMarketState(
        screeners=screeners,
        **merge_assets_market_states_data(
            states, data={name: {} for name in attributes},
            sort=sort
        )
    )
# end merge_assets_orderbook_market_states

def assets_to_symbols_dynamic_market_state(
        state: AssetsDynamicMarketState,
        attributes: Iterable[str],
        separator: Optional[str] = None
) -> AssetsDynamicMarketState:
    """
    Converts an assets market state into a symbols market state.

    :param attributes: The attributes of data.
    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return AssetsDynamicMarketState(
        **{
            name: assets_to_symbols_data(
                data=getattr(state, name), separator=separator
            ) for name in attributes
        }
    )
# end assets_to_symbols_dynamic_market_state

def symbols_to_assets_dynamic_market_state(
        state: SymbolsDynamicMarketState,
        attributes: Iterable[str],
        separator: Optional[str] = None
) -> SymbolsDynamicMarketState:
    """
    Converts a symbols market state into an assets market state.

    :param attributes: The attributes of data.
    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return SymbolsDynamicMarketState(
        **{
            name: symbol_to_assets_data(
                data=getattr(state, name), separator=separator
            ) for name in attributes
        }
    )
# end symbols_to_assets_dynamic_market_state