from datetime import datetime

class StockDay():
    def __init__(self, symbol: str, timestamp: int, opening: float, closing: float, high: float, low: float, volume: float):
        self.symbol = symbol
        self.timestamp = datetime.utcfromtimestamp(timestamp)
        self.opening = opening
        self.closing = closing
        self.high = high
        self.low = low
        self.volume = volume
        
    def __str__(self):
        return "StockDay<symbol={symbol}, timestamp={timestamp}, opening={opening}, closing={closing}, low={low} high={high}, volume={volume}>".format(
            symbol=self.symbol,
            timestamp=self.timestamp.strftime('%Y-%m-%d'),
            opening=self.opening,
            closing=self.closing,
            low=self.low,
            high=self.high,
            volume=self.volume
        )
    
    def to_dict(self):
        return {
            "symbol": self.symbol,
            "timestamp": self.timestamp.strftime('%Y-%m-%d'),
            "opening": self.opening,
            "closing": self.closing,
            "low": self.low,
            "high": self.high,
            "volume": self.volume,
        }
