from .sectors import get_sector_stocks, sectors as default_sectors
from .get_stock_history import get_stock_history

def get_sector_histories(start, end, sectors=default_sectors):
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
            stock_history = get_stock_history(stock, start, end)
            print(stock_history)
            if len(stock_history.days) > 0:
                histories.append(stock_history)
        sector_stock_histories[sector] = histories
    return sector_stock_histories