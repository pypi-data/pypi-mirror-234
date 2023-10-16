from typing import List
from datetime import datetime
from .models import Symbol, Candle, Exchange, Interval

class Datahub:
    """
    A class for fetching historical data from exchanges.
    """

    @staticmethod
    async def connect(url: str) -> Datahub:
        """
        Instantiate the `Datahub` class by connecting to the database.

        Parameters
        ----------
        url : str
            the database url for the datahub instance

        Returns
        -------
        Datahub
            a Datahub instance

        Raises
        ------
        Exception
            If there is an error connecting to the datahub instance.
        """
    async def candle(
        self,
        symbol: Symbol,
        interval: Interval,
        exchange: Exchange,
        start_time: datetime,
        end_time: datetime,
    ) -> List[Candle]:
        """
        Fetch historical candles from datahub.

        Parameters
        ----------
        symbol : Symbol
            the trading pair eg. BTC/USDT
        interval : Interval
            the interval for candles eg. 1m
        exchange : Exchange
            the exchange to fetch from eg. bybit_linear
        start_time : str
            the start time for the candle to fetch.
        end_time : str
            the end time for the candle to fetch.

        Returns
        -------
        List[Candle]
            a list of candles.

        Raises
        ------
        Exception
            If there is an error fetching candles from the datahub instance.
        """
