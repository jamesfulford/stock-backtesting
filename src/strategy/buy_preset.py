from ..trade import Trade

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
