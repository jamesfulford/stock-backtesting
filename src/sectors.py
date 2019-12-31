# Sector Logic
class Sectors:
    XLK = 'xlk'
    XLV = 'xlv'
    XLP = 'xlp'
    XLY = 'xly'
    XLI = 'xli'
    XLU = 'xlu'
    XLB = 'xlb'
    XLE = 'xle'
    XLF = 'xlf'
    XLRE = 'xlre'

def get_sector_stocks(sector: str):
    with open("./sectors/{}.txt".format(sector.lower())) as phile:
        return list(map(str.strip, phile.readlines()))

sectors = [
    Sectors.XLK,
    Sectors.XLV,
    Sectors.XLP,
    Sectors.XLY,
    Sectors.XLI,
    Sectors.XLU,
    Sectors.XLB,
    Sectors.XLE,
    Sectors.XLF,
    Sectors.XLRE,
]
