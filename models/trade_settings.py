class TradeSettings:
    
    def __init__(self, ob, pair):
        self.ma = ob["ma"]
        self.std = ob["std"]
        self.maxspread = ob["maxspread"]
        self.mingain = ob["mingain"]
        self.riskreward = ob["riskreward"]
        
    def __repr__(self):
        return str(vars(self))
    
    @classmethod
    def settings_to_str(cls, settings):
        return_string = "Trade Settings:\n"
        
        for _, v in settings.items():
            return_string += f"{v}\n"
        return_string += "\n"
        
        return return_string