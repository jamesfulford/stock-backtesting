from .stock_day import StockDay
from functools import reduce

class StockHistory():
    EMPTY_BODY = {
        't': []
    }

    def __init__(self, symbol, body):
        self.symbol = symbol
        
        self.days = [
            StockDay(
                symbol,
                body["t"][i],
                body["o"][i],
                body["c"][i],
                body["h"][i],
                body["l"][i],
                body["v"][i],
            ) for i in range(len(body["t"]))
        ]
        self.days.sort(key=lambda d: d.timestamp)
    
    def get_current_day_state(self):
        """
        returns StockDay with greatest timestamp
        """
        return reduce(
            lambda m, x: m if m.timestamp > x.timestamp else x,
            self.days
        )
    
    def __str__(self):
        return "StockHistory<{} trading days of {}>".format(len(self.days), self.symbol)

    def __repr__(self):
        return self.__str__()
