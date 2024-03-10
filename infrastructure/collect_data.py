import pandas as pd 
import datetime as dt 
from dateutil import parser
from infrastructure.instrument_collection import InstrumentCollection
from api.oanda_api import OandaApi

CANDLE_COUNT = 3000

INCREMENTS = {
    "M5" : 5 * CANDLE_COUNT,
    "H1" : 60 * CANDLE_COUNT,
    "H4" : 240 * CANDLE_COUNT
}

def save_file(final_df: pd.DataFrame, file_prefix, granularity, pair):
    file_name = f"{file_prefix}{pair}_{granularity}.pkl"
    final_df.drop_duplicates(subset=["time"], inplace=True)
    final_df.sort_values(by="time", inplace=True)
    final_df.reset_index(drop=True, inplace=True)
    final_df.to_pickle(file_name)
    print(f"*** {pair} {granularity} {final_df.time.min()} {final_df.time.max()} ---> {final_df.shape[0]} candles ***")

def fetch_candles(pair, granularity, date_from: dt.datetime, date_to: dt.datetime, api: OandaApi):
    # goes straight to the api 
    attempts = 0

    while attempts < 3:
        candles_df = api.get_candles_df(pair, granularity=granularity, date_from=date_from, date_to=date_to)
        if candles_df is not None:
            break

        attempts += 1

    if candles_df is not None and candles_df.empty == False:
        return candles_df
    else: 
        return None

def collect_data(pair, granularity, date_from, date_to,file_prefix, api: OandaApi):
    time_step = INCREMENTS[granularity]
    end_date = parser.parse(date_to)
    from_date = parser.parse(date_from)

    candle_dfs = []

    to_date =  from_date

    while to_date < end_date:
        to_date = from_date + dt.timedelta(minutes=time_step)
        if to_date > end_date:
            to_date = end_date

        candles = fetch_candles(pair, granularity, from_date, to_date, api)

        if candles is not None:
            candle_dfs.append(candles)
            print(f"{pair} {granularity} {to_date} {from_date} ---> {candles.shape[0]} candles loaded")            
        else:
            print(f"{pair} {granularity} {to_date} {from_date} ---> NO CANLDES")

        from_date = to_date

    if len(candle_dfs) > 0:
        final_df = pd.concat(candle_dfs)
        save_file(final_df, file_prefix, granularity, pair)
    else:
        print(f"{pair} {granularity} ---> NO DATA SAVED")


def run_collection(ic: InstrumentCollection, api:OandaApi):
    our_curr = ["AUD", "CAD", "JPY", "GBP", "USD", "EUR", "NZD", "CHF"]
    for p1 in our_curr:
        for p2 in our_curr:
            pair = f"{p1}_{p2}"
            if pair in ic.instruments_dict.keys():
                for granularity in ["M5","H1", "H4"]:
                    print(pair, granularity)
                    collect_data(
                        pair, 
                        granularity,
                        "2016-01-01T00:00:00Z",
                        "2023-12-31T00:00:00Z",
                        "./data/",
                        api
                    )
