"""
Describes a class that represents companies from 3 exchanges.
"""
from enum import Enum


class StockExchange(Enum):
    NASDAQ = 1
    NYSE = 2
    LSE = 3


class Company:
    def __init__(
        self,
        name,
        exchange: StockExchange,
        ticker="",
    ) -> None:
        self.name = name
        if ticker is not None:
            self.ticker = ticker
        self.exchange = exchange
