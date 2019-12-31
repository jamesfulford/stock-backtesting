from .evaluate_trades import evaluate_trades

def run_strategies(strategies, sector_stock_histories, start, end):
    results = {}

    for strategy in strategies:
        strategy_name = strategy.__name__
        results[strategy_name] = {}

        for sector, histories in sector_stock_histories.items():
            trades = strategy(histories)

            evaluation = evaluate_trades(trades, histories, start, end)
            period_roi = evaluation["period_roi"]
            
            results[strategy_name][sector] = {
                "trades": [t.to_dict() for t in trades],
                "evaluation": evaluation,
                "start": start.strftime("%Y-%m-%d"),
                "end": end.strftime("%Y-%m-%d")
            }
    
    return results