import logging

from typing import List, Dict
from .models import Candle, OrderUpdate, Performance, RuntimeMode, Interval


class Strategy:
    """
    This class is a handler that will be used by the Runtime to handle events such as
    `on_candle_closed`, `on_order_update`, etc. The is a base class and every new strategy
    should be inheriting this class and override the methods.
    """

    logger = logging
    LOG_FORMAT = (
        "%(levelname)s %(name)s %(asctime)-15s %(filename)s:%(lineno)d %(message)s"
    )

    def __init__(
        self,
        log_level: int = logging.INFO,
        handlers: List[logging.Handler] = [],
    ):
        """
        Set up the logger
        """
        if len(handlers) == 0:
            default_handler = logging.StreamHandler()
            default_handler.setFormatter(logging.Formatter(self.LOG_FORMAT))
            handlers.append(default_handler)

        logging.root.setLevel(log_level)
        for handler in handlers:
            logging.root.addHandler(handler)

    async def on_order_update(self, strategy, update: OrderUpdate):
        logging.info(f"Received order update: {update.__repr__()}")

    async def on_candle_closed(
        self, strategy, candle: Candle, candles: Dict[Interval, List[Candle]]
    ):
        # No need to log if it's backtest
        if strategy.config.mode == RuntimeMode.Backtest:
            return

        logging.info(
            f"[{self.__class__.__name__}] {candle.interval} candle for {candle.symbol.base}/{candle.symbol.quote} beginning at {candle.start_time} has closed at {candle.close}. "
            + f"Maintaining a total of {len(candles[candle.interval])} candles"
        )

    async def on_backtest_complete(self, strategy, performance: Performance):
        logging.info(f"[{self.__class__.__name__}] Backtest completed.")
