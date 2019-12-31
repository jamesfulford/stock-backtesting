from ..trade import Trade

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
