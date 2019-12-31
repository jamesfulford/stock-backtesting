from ..trade import Trade

def use_buy_n_strategy(n):
    """
    Buy `n` shares of each stock at the start of the period. Hold.
    """
    def buy_n_strategy(histories):
        return [Trade(history.days[0], n) for history in histories]
    return buy_n_strategy
