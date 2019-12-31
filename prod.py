#!/usr/bin/env python
# coding: utf-8

# # Gather Data
# Uses finnhub.io API to gather historical stock data over period of time for items in provided sectors.

# In[ ]:


from datetime import datetime

# Select Timeframe
start = datetime(2019, 1, 1, 0, 0, 0)
end = datetime.now()
days = (end - start).days

from src.get_sector_history import get_sector_histories

sector_stock_histories = get_sector_histories(days)

from src.sectors import get_sector_stocks

for sector, history in sector_stock_histories.items():
    print("{}: {}/{}".format(sector, len(history), len(get_sector_stocks(sector))))


# ## Strategy

# In[ ]:


# TODO(james.fulford): Collect more days in past for Moving Average reasons
# TODO(james.fulford): Collect higher resolution data (not daily, but hourly or something)
# TODO(james.fulford): Collect earnings data (?)


# In[ ]:


from src.strategy.top_volume import use_top_volume_fixed_purchasing
from src.evaluate_trades import evaluate_trades

strategies = [
    use_top_volume_fixed_purchasing(3, 1000)
]

for strategy in strategies:
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
        evaluation = evaluate_trades(trades, histories, start, end)
        print()


# In[ ]:




