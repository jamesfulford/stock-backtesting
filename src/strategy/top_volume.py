from ..trade import Trade
from .util.daily import daily

def use_top_volume_fixed_purchasing(top_n, target_value):
    @daily
    def top_volume_fixed_purchasing(timestamp, records_by_symbol):
        records_by_volume = sorted(records_by_symbol.values(), key=lambda d: -d.volume)
        stocks_to_trade = records_by_volume[:top_n]

        for stock_day in stocks_to_trade:
            quantity = target_value // stock_day.closing
            yield Trade(stock_day, quantity)

    top_volume_fixed_purchasing.__name__ += "(top_n={top_n}, target_value={target_value})".format(top_n=top_n, target_value=target_value)
    return top_volume_fixed_purchasing
