from .stock_day import StockDay

class Trade():
    def __init__(self, stock_day: StockDay, quantity: int = 0):
        self.stock_day = stock_day  # composition over inheritance
        self.quantity = quantity

    def __str__(self):
        return "Trade<{quantity} of {stock_day}>".format(quantity=self.quantity, stock_day=self.stock_day)
    
    def __repr__(self):
        return str(self)
    
    @property
    def symbol(self):
        return self.stock_day.symbol
    
    @property
    def closing_value(self):
        return abs(self.quantity * self.stock_day.closing)
