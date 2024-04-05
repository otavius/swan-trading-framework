
from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
import time

from models.candle_timing import CandleTiming 
from bot.trade_risk_calculator import get_trade_units
import constants.account as id 

def lm(msg, pair):
    #print(msg,pair)
    pass
    
if __name__== "__main__":
    api = OandaApi()
    instrumentCollection.load_instruments("./data")
    # dd = api.last_complete_candle("EUR_USD", granularity="M5")
    # print(CandleTiming(dd))
    #print(api.get_prices(["GBP_JPY"]))
    
    ### 0.0001 / JPY PAIRS 0.01
    print("AUD_NZD", get_trade_units(api, "AUD_NZD", id.BUY, 0.0055, 30, lm))
    print("GBP_JPY",get_trade_units(api, "GBP_JPY", id.BUY, 0.4, 20, lm))
    print("USD_CAD", get_trade_units(api, "USD_CAD", id.BUY, 0.004, 20, lm))
  
    