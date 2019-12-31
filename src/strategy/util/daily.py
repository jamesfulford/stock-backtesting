

def by_day(histories):
    day_symbol_map = {}
    for history in histories:
        # move this to stock history class:
        for day in history.days:
            index = day.timestamp.strftime("%Y/%m/%d")
            if index not in day_symbol_map:
                day_symbol_map[index] = {}

            day_symbol_map[index][day.symbol] = day
    
    final_records = list(day_symbol_map.items())
    final_records.sort(key=lambda t: t[0])

    return final_records

def daily(fn):
    """
    Decorator. Useful for going day-by-day.
    """
    def _daily(histories):
        trades = []
        for timestamp, records_by_symbol in by_day(histories):
            trades.extend(list(fn(timestamp, records_by_symbol)))
        return trades
    
    _daily.__name__ = fn.__name__
    _daily.__doc__ = fn.__doc__
    return _daily
