import requests
import os
import time

from .stock_history import StockHistory

TOKEN = os.environ['FINNHUB_TOKEN']

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
