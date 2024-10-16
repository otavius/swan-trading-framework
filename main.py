
from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from simulation.ma_cross import run_ma_sim
from dateutil import parser 
from infrastructure.collect_data import run_collection
from simulation.ema_macd_start import run_ema_macd
from simulation.ema_macd_mp import run_ema_macd
from stream_example.streamer import run_streamer

if __name__=="__main__":
    api = OandaApi()

    # dfr = parser.parse("2021-04-21T01:00:00Z")
    # dto = parser.parse("2021-04-28T16:00:00Z")

    # df_candles = api.get_candles_df("EUR_USD", granularity="H1", date_from=dfr, date_to=dto)

    # print(df_candles.head())
    # print("")
    # print(df_candles.tail())

    # print(api.fetch_candles("EUR_USD", granularity="D", price="MB"))

    #instrumentCollection.create_file(api.get_account_instruments(), "./data")
    instrumentCollection.load_instruments("./data")
    # run_collection(instrumentCollection, api)
    # instrumentCollection.print_intsruments()
    #run_ma_sim()
    #run_ema_macd(instrumentCollection)
    #run_ema_macd(instrumentCollection)
    # stream_prices(["GBP_JPY", "GBP_USD"])
    run_streamer()

