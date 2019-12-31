def print_roi(results):
    for strategy_name, sector_result_map in results.items():
        print("{strategy_name}:".format(strategy_name=strategy_name))
        
        sector_pairings = list(sector_result_map.items())
        sector_pairings.sort(key=lambda t: t[1]["evaluation"]["period_roi"])

        for sector, sector_results in sector_pairings:
            print("\t{sector}: {roi:.2f}".format(sector=sector, roi=100 * sector_results["evaluation"]["period_roi"]))
