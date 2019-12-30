#!/usr/bin/env python
# coding: utf-8

# # Gather Data
# Uses finnhub.io API to gather historical stock data over period of time for items in provided sectors.

# In[ ]:


# API and Data Models
from datetime import datetime
import time
from functools import reduce
import os

import requests


TOKEN = os.environ['FINNHUB_TOKEN']

class StockDay():
    def __init__(self, symbol: str, timestamp: int, opening: float, closing: float, high: float, low: float, volume: float):
        self.symbol = symbol
        self.timestamp = datetime.utcfromtimestamp(timestamp)
        self.opening = opening
        self.closing = closing
        self.high = high
        self.low = low
        self.volume = volume
        
    def __str__(self):
        return "StockDay<symbol={symbol}, timestamp={timestamp}, opening={opening}, closing={closing}, low={low} high={high}, volume={volume}>".format(
            symbol=self.symbol,
            timestamp=self.timestamp.strftime('%Y-%m-%d'),
            opening=self.opening,
            closing=self.closing,
            low=self.low,
            high=self.high,
            volume=self.volume
        )

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

# Caching logic
class memoize():
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}
    
    def __call__(self, *args, **kwargs):
        if args not in self.memo:
            self.memo[args] = self.fn(*args, **kwargs)
        return self.memo[args]

    def reset_cache(self):
        self.memo = {}

@memoize
def get_stock_history(symbol: str, days=7, wait=1):
    """
    https://finnhub.io/docs/api#stock-candles
    """
    r = requests.get('https://finnhub.io/api/v1/stock/candle?symbol={SYMBOL}&token={TOKEN}&resolution=D&count={days}'.format(TOKEN=TOKEN, SYMBOL=symbol, days=days))
    try:
        body = r.json()
        if body["s"] == "ok":
            return StockHistory(symbol, body)
        else:
            return StockHistory(symbol, StockHistory.EMPTY_BODY)
    except:
        if r.status_code == 429:
            # API limiting, so let's wait and retry
            print("API rate limiting... retrying in {wait}".format(wait=wait))
            time.sleep(wait)
            return get_stock_history(symbol=symbol, days=days, wait=min(wait*2, 8))  # exponential backoff
        # if a different error, print out error message
        print(r.status_code, r.text)


# In[ ]:


# Sector Logic
class Sectors:
    XLK = 'xlk'
    XLV = 'xlv'
    XLP = 'xlp'
    XLY = 'xly'
    XLI = 'xli'
    XLU = 'xlu'
    XLB = 'xlb'
    XLE = 'xle'
    XLF = 'xlf'
    XLRE = 'xlre'

def get_sector_stocks(sector: str):
    with open("./sectors/{}.txt".format(sector.lower())) as phile:
        return list(map(str.strip, phile.readlines()))

sectors = [
    Sectors.XLK,
    Sectors.XLV,
    Sectors.XLP,
    Sectors.XLY,
    Sectors.XLI,
    Sectors.XLU,
    Sectors.XLB,
    Sectors.XLE,
    Sectors.XLF,
    Sectors.XLRE,
]


# In[ ]:


# OPTIONAL: reset cache to force re-fetch
get_stock_history.reset_cache()


# In[ ]:


# Get stock data

# Select Timeframe
start = datetime(2019, 1, 1, 0, 0, 0)
end = datetime.now()
days = (end - start).days

# Gather Data from API
sector_stock_histories = {}

for sector in sectors:
    stocks = get_sector_stocks(sector)
    print(sector, len(stocks))
    
    histories = []
    for stock in stocks:
        # NOTE(james.fulford): Tried parallelizing this,
        # performance gains were limited due to rate limiting of API
        # and also a big headache.
        # Don't try to parallelize this again, it isn't worth it
        stock_history = get_stock_history(stock, days=days)
        print(stock_history)
        if len(stock_history.days) > 0:
            histories.append(stock_history)
    sector_stock_histories[sector] = histories    

print("Done.")


# In[ ]:


for sector, history in sector_stock_histories.items():
    print("{}: {}/{}".format(sector, len(history), len(get_sector_stocks(sector))))


# # Trades

# In[ ]:


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

    
def evaluate_trades(trades, histories):
    if len(trades) == 0:
        return None
    net = 0
    total_in = 0
    total_out = 0
    total_unrealized = 0
    for stock_history in histories:
        relevant_trades = list(filter(lambda t: t.symbol == stock_history.symbol, trades))
        if len(relevant_trades) == 0:
            continue

        money_in = reduce(lambda a, x: a + (x.closing_value if x.quantity > 0 else 0), relevant_trades, 0)
        money_out = reduce(lambda a, x: a + (x.closing_value if x.quantity < 0 else 0), relevant_trades, 0)

        current = stock_history.get_current_day_state()

        realized = money_out - money_in
        
        remaining_quantity = reduce(lambda a, x: a + x.quantity, relevant_trades, 0)
        unrealized = current.closing * remaining_quantity

        current_value = realized + unrealized

        # print("{symbol} delta: ${change:.2f} ({percent_change:.1f}%)".format(symbol=stock_history.symbol, change=current_value, percent_change=100 * current_value/money_in))
        
        net += current_value
        total_in += money_in
        total_out += money_out
        total_unrealized += unrealized

    period_roi = net / total_in
    print("\n\t\tROI: {:.2f}% ({} to {})".format(100 * period_roi, start.strftime("%Y/%m/%d"), end.strftime("%Y/%m/%d")))
    # TODO(james.fulford): Fix this, days isn't number of trading days
    # annual_roi = period_roi * (252 / days)
    # print("\t\tAnnualized ROI: {:.2f}%".format(100 * annual_roi))
    # TODO(james.fulford): What should this return?


# ## Strategy

# In[ ]:


def use_buy_n_strategy(n):
    """
    Buy `n` shares of each stock at the start of the period. Hold.
    """
    def buy_n_strategy(histories):
        return [Trade(history.days[0], n) for history in histories]
    return buy_n_strategy

def use_buy_preset_value_strategy(target_value):
    """
    Try to buy `value`-worth of each stock at the start of the period. Hold.
    (Rounds down to whole share)
    """
    def buy_preset_value_strategy(histories):
        trades = []
        for history in histories:
            day = history.days[0]
            quantity = target_value // day.closing
            trades.append(Trade(history.days[0], quantity))
        return trades
    
    buy_preset_value_strategy.__name__ += "({})".format(target_value)
    return buy_preset_value_strategy

# TODO(james.fulford): Collect more days in past for Moving Average reasons
# TODO(james.fulford): Collect higher resolution data (not daily, but hourly or something)
# TODO(james.fulford): Collect earnings data (?)

def use_top_volume_fixed_purchasing(top_n, target_value):
    def top_volume_fixed_purchasing(histories):
        final_records = {}
        for history in histories:
            # move this to stock history class:
            for day in history.days:
                index = day.timestamp.strftime("%Y/%m/%d")
                if index not in final_records:
                    final_records[index] = {}
                
                final_records[index][day.symbol] = day
        
        trades = []

        for timestamp, records_by_symbol in final_records.items():
            records_by_volume = sorted(records_by_symbol.values(), key=lambda d: -d.volume)
            stocks_to_trade = records_by_volume[:top_n]
            
            for stock_day in stocks_to_trade:
                quantity = target_value // stock_day.closing
                trades.append(Trade(stock_day, quantity))

        return trades

    top_volume_fixed_purchasing.__name__ += "(top_n={top_n}, target_value={target_value})".format(top_n=top_n, target_value=target_value)
    return top_volume_fixed_purchasing


# In[ ]:


for strategy in [use_top_volume_fixed_purchasing(3, 1000)]:
    print("{}:\n".format(strategy.__name__))
    for sector, histories in sector_stock_histories.items():
        print("{}:\n".format(sector, ))
        trades = strategy(histories)
        
        today_s = end.strftime("%Y/%m/%d")
        for t in filter(lambda t: t.stock_day.timestamp.strftime("%Y/%m/%d") == today_s, trades):
            print("\t{symbol:4} x {quantity:5}:\t${closing:.2f}\t({volume:.1f}M)".format(
                symbol=t.symbol,
                quantity=int(t.quantity),
                closing=t.stock_day.closing,
                volume=t.stock_day.volume / 1000000,
            ))
        evaluation = evaluate_trades(trades, histories)
        print()


# In[ ]:




