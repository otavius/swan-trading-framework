class TradeDecision:
    
    def __init__(self, row):
        self.gain = row.GAIN
        self.signal =  row.SIGNAL
        self.stop_loss = row.SL 
        self.take_profit  = row.TP
        self.pair = row.PAIR
        
    def __repr__(self) -> str:
        return f"TradeDecision(): {self.pair} dir:{self.signal} gain:{self.gain:.4f} stoploss:{self.stop_loss:.4f} takeprofit:{self.take_profit:.4f}"