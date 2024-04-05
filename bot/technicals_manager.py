import pandas as pd

from models.trade_decision import TradeDecision
from technicals.indicators import BollingerBands

pd.set_option("display.max_columns", None)
pd.set_option("expand_frame_repr", False)
from api.oanda_api import OandaApi
from models.trade_settings import TradeSettings
import constants.account as id


ADDROWS = 20

def apply_signal(row, trade_settings: TradeSettings):
    
    if row.SPREAD <= trade_settings.maxspread and row.GAIN >= trade_settings.mingain:
        if row.mid_c > row.BB_UP and row.mid_o < row.BB_UP:
            return id.SELL
        elif row.mid_c < row.BB_LW and row.mid_o > row.BB_LW:
            return id.BUY
        
    return id.NONE

def apply_stop_loss(row, trade_settings: TradeSettings):
    if row.SIGNAL == id.BUY:
        return row.mid_c - (row.GAIN/ trade_settings.riskreward)
    elif row.SIGNAL == id.SELL:
        return row.mid_c + (row.GAIN / trade_settings.riskreward)
    return 0.0

def apply_take_profit(row):
    if row.SIGNAL == id.BUY:
        return row.mid_c + row.GAIN
    elif row.SIGNAL == id.SELL:
        return row.mid_c - row.GAIN 
    return 0.0  
        
        

def process_candles(df: pd.DataFrame, pair, trade_settings: TradeSettings, log_message):
    
    df.reset_index(drop=True, inplace=True)
    df["PAIR"] = pair
    df["SPREAD"] = df.ask_c - df.bid_c

    
    # make indicator
    df = BollingerBands(df, trade_settings.ma, trade_settings.std)
    df["GAIN"] = abs(df.mid_c - df.BB_MA)
    df["SIGNAL"] = df.apply(apply_signal, axis=1, trade_settings=trade_settings)
    df["TP"] = df.apply(apply_take_profit, axis=1)
    df["SL"] = df.apply(apply_stop_loss, axis=1, trade_settings=trade_settings)
    df["LOSS"] = abs(df.mid_c - df.SL)
    
    log_col = ["PAIR", "time", "mid_c", "mid_o", "SL", "TP", "SPREAD", "GAIN", "LOSS","SIGNAL"]
    log_message(f"process_candles:\n{df[log_col].tail()}", pair)
    
    return df[log_col].iloc[-1]

def fetch_candles(pair, row_count, candle_time, granularity, api: OandaApi, log_message):
    df = api.get_candles_df(pair, count=row_count, granularity=granularity)
    
    if df is None or df.shape[0] == 0:
        log_message("tech_manager fetch_candles failed to get candles", pair)
        return None
    
    # Set for later to re-try 2-3 time to fecth candles 
    if df.iloc[-1].time != candle_time:
        log_message(f"tech_manager fetch_candles{df.iloc[-1].time} not correct", pair)
        return None      
    
    return df 

def get_trade_decision(candle_time, pair, granularity, api: OandaApi, trade_settings: TradeSettings, log_message):
    
    max_rows = trade_settings.ma + ADDROWS
    
    log_message(f"tech_manager: max_rows:{max_rows} candle_time{candle_time} granularity:{granularity}", pair) 
    
    df = fetch_candles(pair, max_rows, candle_time, granularity, api, log_message)
    
    if df is not None:
        last_row = process_candles(df, pair, trade_settings, log_message)
        
        return TradeDecision(last_row)
    return None 