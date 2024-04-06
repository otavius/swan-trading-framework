import json
import threading 
import requests
import pandas as pd
from timeit import default_timer as timer

import constants.account as id
from infrastructure.log_wrapper import LogWrapper
from models.live_api_price import LiveApiPrice 
from stream_example.stream_base import StreamBase

STREAM_URL = f"https://stream-fxpractice.oanda.com/v3"

class PriceStreamer(StreamBase):
    LOG_FREQ = 60
    def __init__(self, shared_prices, price_lock: threading.Lock, price_events):
        super().__init__(shared_prices, price_lock, price_events, "PriceStreamer")
        self.pairs_list = shared_prices.keys()
        self.price_lock = price_lock
        self.price_events = price_events
        self.shared_prices = shared_prices
        self.log = LogWrapper("PriceStreamer")
        print(self.pairs_list)
        
    def fire_new_price_event(self, instrument):
        if self.price_events[instrument].is_set() == False:
            self.price_events[instrument].set()
        
    def update_live_price(self, live_price: LiveApiPrice):
        try:
            self.price_lock.acquire()
            self.shared_prices[live_price.instrument] = live_price
            self.fire_new_price_event(live_price.instrument)
        except Exception as error:
            self.log_message(f"Exception: {error}", error=True)   
        finally:
            self.price_lock.release()
            
    def log_data(self):
        self.log_message("")
        self.log_message(f"\n{pd.DataFrame.from_dict([v.get_dict() for _,v in self.shared_prices.items()])}")

    def run(self):
        
        start = timer() - PriceStreamer.LOG_FREQ + 10
        
        params = dict(
            instruments = ','.join(self.pairs_list)
        )
        
        url = f"{STREAM_URL}/accounts/{id.ACCOUNT_ID}/pricing/stream"
        
        response = requests.get(url, params=params, headers=id.SECURE_HEADER, stream=True)
        
        for price in response.iter_lines():
            if price:
                decode_price = json.loads(price.decode("utf-8"))
                if "type" in decode_price and decode_price["type"] == "PRICE":
                    # print(LiveApiPrice(decode_price).get_dict())
                    self.update_live_price(live_price=(decode_price))
                    if timer() - start > PriceStreamer.LOG_FREQ:
                        print(LiveApiPrice(decode_price).get_dict())
                        #log data
                        self.log_data()
                        start = timer()