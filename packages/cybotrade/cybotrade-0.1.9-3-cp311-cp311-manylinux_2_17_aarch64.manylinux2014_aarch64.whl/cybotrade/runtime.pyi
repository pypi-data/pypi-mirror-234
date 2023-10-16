from typing import Optional
from .models import (
    Position,
    RuntimeConfig,
    OrderParams,
    OrderResponse,
    Performance,
    OrderSize,
)
from .strategy import Strategy

class StrategyTrader:
    config: RuntimeConfig

    async def entry(self, params: OrderParams) -> OrderResponse:
        """
        Enters a trade with the given quantity, do note that this entry function will do
        pyramiding where it closes the existing position if one exists.
        """
    async def exit(
        self, id: str, size: OrderSize, tp: Optional[float], sl: Optional[float]
    ):
        """
        Exit a specific trade by setting take profit and stop loss order.
        """
    async def order(self, params: OrderParams) -> OrderResponse:
        """
        Places an order, do note that this function does not take into account current position,
        it merely executes whatever parameters was given.
        """
    async def cancel(self, id: str) -> OrderResponse:
        """
        Cancels a specific order by its id.
        """
    async def close(self, id: str, size: OrderSize):
        """
        Closes a specific trade with the given quantity. This function closes the trade with market
        order.
        """
    async def close_all(self):
        """
        Close all currently entered trades, do note that this function does not early exits even
        if it failed to close one of the trades, it will continue to close all orders.
        """
    async def get_order_size(self) -> float:
        """
        Get the order quantity in base currency for the given [`OrderSize`] provided to the strategy.
        """
    async def get_current_equity(self) -> float:
        """
        Get the current equity of the running strategy.
        """
    async def get_current_available_balance(self) -> float:
        """
        Get the current available balance of the running strategy.
        """
    async def get_current_wallet_balance(self) -> float:
        """
        Get the current wallet balance of the running strategy.
        """
    async def position(self) -> Position:
        """
        Get the current position of the strategy.
        """
    async def performance(self) -> Performance:
        """
        Calculate and get the current performance of the running strategy.
        """

class Runtime:
    """
    A class representation of the underlying strategy runtime which handle backtest,
    paper trade, live trade.
    """

    @staticmethod
    async def connect(config: RuntimeConfig, strategy: Strategy) -> Runtime:
        """
        Instantiate the `Runtime` class by providing the configurations and a `Strategy`
        class which acts as the event handler.

        Parameters
        ----------
        config : RuntimeConfig
            the configuration for the runtime.
        strategy : Strategy
            the strategy to run within the runtime.

        Returns
        -------
        Runtime
            a Runtime instance

        Raises
        ------
        Exception
            If there is an error creating the runtime.
        """
    async def start(self) -> None:
        """
        Start the runtime and this method ideally will never return under live trade /
        paper trade unless interrupted, however this function will return when the backtest
        finishes.

        Raises
        ------
        Exception
            If there is an error during the runtime.
        """
