
def print_day_trades(results, day):
    day_s = day.strftime("%Y-%m-%d")

    for strategy_name, sector_result_map in results.items():
        print("{strategy_name}:".format(strategy_name=strategy_name))
        
        sector_pairings = list(sector_result_map.items())
        sector_pairings.sort(key=lambda t: t[1]["evaluation"]["period_roi"])

        for sector, sector_results in sector_pairings:
            print("\t{sector}:".format(sector=sector))

            for t in filter(lambda t: t["stock_day"]["timestamp"] == day_s, sector_results["trades"]):
                print("\t\t- {symbol:4}:\t${closing:.2f}\t({volume:.1f}M)".format(
                    symbol=t["symbol"],
                    closing=t["stock_day"]["closing"],
                    volume=t["stock_day"]["volume"] / 1000000,
                ))
