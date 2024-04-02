class Instrument:

    def __init__(self, name, ins_type, display_name,
        pip_location, trade_units_precision, margin_rate, display_precision):
            self.name = name
            self.ins_type = ins_type
            self.display_name = display_name
            self.pip_location = pow(10, pip_location)
            self.trade_units_precision = trade_units_precision
            self.margin_rate = float(margin_rate)
            self.displayprecision = display_precision


    def __repr__(self):
        return str(vars(self))

    @classmethod
    def from_api_object(cls, ob):
        return Instrument(
            ob["name"],
            ob["type"],
            ob["displayName"],
            ob["pipLocation"],
            ob["tradeUnitsPrecision"],
            ob["marginRate"],
            ob["displayPrecision"]
        )
