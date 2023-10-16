from typing import List, Optional
from .models import (
    LocalOrderBookUpdate,
    OrderBookSubscriptionParams,
    Symbol,
    Candle,
    ExchangeConfig,
    Exchange,
    Interval,
)

class MarketCollector:
    """
    A class for fetching live market data from exchanges.
    """

    @staticmethod
    async def connect(exchanges: List[ExchangeConfig]) -> MarketCollector:
        """
        Instantiate the `MarketCollector` class by connecting to one or more exchanges.

        Parameters
        ----------
        exchanges : List[ExchangeConfig]
            the list of exchanges to connect to.

        Returns
        -------
        MarketCollector
            a MarketCollector instance

        Raises
        ------
        Exception
            If there is an error connecting to the exchange.
        """
    async def subscribe_candle(
        self,
        symbol: Symbol,
        interval: Interval,
        exchange: Exchange,
        params: Optional[dict],
    ):
        """
        Subscribe to the live candle updates for the specified exchange.

        Parameters
        ----------
        symbol : str
            the trading pair eg. BTC/USDT
        interval : Interval
            the interval for candles eg. 1m
        exchange : Exchange
            the exchange to fetch from eg. bybit_linear
        params : str
            extra parameters for the subscription.

        Raises
        ------
        Exception
            If there is an error sending subscription message to the exchange.
        """
    async def subscribe_aggregated_order_book(
        self,
        symbol: Symbol,
        depth: int,
        exchanges: List[tuple[Exchange, OrderBookSubscriptionParams]],
    ):
        """
        Subscribe to the aggregated live order book updates for the specified exchanges.

        Parameters
        ----------
        symbol : str
            the trading pair eg. BTC/USDT
        depth : int
            the order book depth for the aggregated order book.
        exchanges : List[tuple[Exchange, OrderBookSubscriptionParams]]
            the exchanges to subscribe to and its corresponding subscription params.

        Raises
        ------
        Exception
            If there is an error sending subscription message to the exchange.
        """
    async def listen_candle(self) -> Candle:
        """
        Listen for the latest candle update.
        NOTE: This function will never yield if there is no active subscriptions.

        Returns
        -------
        Candle
            the latest candle from the exchange.

        Raises
        ------
        Exception
            If there is an error retrieving the latest candle from the exchange.
        """
    async def listen_aggregated_order_book(self) -> List[LocalOrderBookUpdate]:
        """
        Listen for the latest aggregated order book update.
        NOTE: This function will never yield if there is no active subscriptions.

        Returns
        -------
        List[LocalOrderBookUpdate]
            the latest local order book update from the exchanges.

        Raises
        ------
        Exception
            If there is an error retrieving the latest aggregated order book from exchanges.
        """  # noqa: E501
