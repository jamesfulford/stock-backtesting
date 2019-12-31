from functools import reduce

def evaluate_trades(trades, histories, start, end):
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
