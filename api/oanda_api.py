import requests
import json
import constants.account as id
import pandas as pd 
from dateutil import parser
from datetime import datetime as dt 
from infrastructure.instrument_collection import instrumentCollection as ic
from models.open_trade import OpenTrade




class OandaApi:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {id.API_KEY}",
            "Content-Type": "application/json"
        })

    def make_request(self, url, verb="get", code=200, params=None, data=None, headers=None):
        full_url = f"{id.OANDA_URL}/{url}"
        
        if data is not None:
            data = json.dumps(data)
        
        try:
            response = None
            if verb == "get":
                response = self.session.get(full_url, params=params, data=data, headers=headers)
                
            if verb == "post":
                response = self.session.post(full_url, params=params, data=data, headers=headers)

            if verb == "put":
                response = self.session.put(full_url, params=params, data=data, headers=headers)

            if response == None:
                return False, {"error": "verb not found"}

            if response.status_code == code:
                return True, response.json()
            else:
                return False, response.json()

        except Exception as error:
            return False, {"Exception": error}

    def get_account_endpoint(self, ep, data_key):
        url = f"accounts/{id.ACCOUNT_ID}/{ep}"
        ok, data = self.make_request(url)
        if ok == True and data_key in data:
            return data[data_key]
        else:
            print("Error get_account_endpoint()", data)
            return None

    def get_account_summary(self):
        return self.get_account_endpoint("summary", "account")

    def get_account_instruments(self):
        return self.get_account_endpoint("instruments", "instruments")

    def fetch_candles(self, pair_name, count=10, granularity="H1", price="MBA", date_from=None, date_to=None):
        url = f"/instruments/{pair_name}/candles"
        params = dict(
            granularity = granularity,
            price = price
        )

        if date_from is not None and date_to is not None: 
            date_format = "%Y-%m-%dT%H:%M:%SZ"
            params["from"] = dt.strftime(date_from, date_format)
            params["to"] = dt.strftime(date_to, date_format)
        else: 
            params["count"] = count


        ok, data = self.make_request(url, params=params)

        if ok == True and "candles" in data:
            return data['candles']
        else:
            print("Error fetch_candles()", data)
            return None
        

    def get_candles_df(self, pair_name, **kwargs):

        data = self.fetch_candles(pair_name, **kwargs)

        if data is None:
            return None
        if len(data) == 0:
            return pd.DataFrame()
        prices = ['mid', 'bid', 'ask']
        ohlc = ['o', 'h', 'l', 'c']
        
        final_data = []
        for candle in data:
            if candle['complete'] == False:
                    continue
            new_dict = {}
            new_dict['time'] = parser.parse(candle['time'])
            new_dict['volume'] = candle['volume']
        
            for p in prices:
                if p in candle: 
                    for o in ohlc:
                        new_dict[f"{p}_{o}"] = float(candle[p][o])
        
            final_data.append(new_dict)
        df = pd.DataFrame.from_dict(final_data)
        return df
    
    def last_complete_candle(self, pair_name, granularity):
        df = self.get_candles_df(pair_name, granularity=granularity, count=10)
        if df.shape[0] == 0:
            return None
        return df.iloc[-1].time 
                
            
    def place_trade(self, pair_name: str, units: float, direction: int, stop_loss: float=None, take_profit: float=None):
        url = f"accounts/{id.ACCOUNT_ID}/orders"
        
        instrument = ic.instruments_dict[pair_name]
        units = round(units, instrument.trade_units_precision)
        
        if direction == id.SELL:
            units = units * -1
        
        data = dict(
            order=dict(
                units=str(units),
                instrument=pair_name,
                type="MARKET"
            )
        )
        
        if stop_loss is not None:
            stop_loss_dict = dict(price=str(round(stop_loss, instrument.displayprecision)))
            data["order"]["stopLossOnFill"] = stop_loss_dict

        if take_profit is not None:
            take_profit_dict = dict(price=str(round(take_profit, instrument.displayprecision)))
            data["order"]["takeProfitOnFill"] = take_profit_dict
        
        #print(data)
        
        ok, response = self.make_request(url, verb="post", data=data, code=201)
        
        #print(ok, response)
        
        if ok == True and "orderFillTransaction" in response:
            return response["orderFillTransaction"]["id"]
        else:
            return None
        
    def close_trade(self, trade_id):
        url = f"accounts/{id.ACCOUNT_ID}/trades/{trade_id}/close"
        
        ok, _ = self.make_request(url, verb="put", code=200)
        
        if ok == True:
            print(f"Closed {trade_id} successfully")
        else: 
            print(f"Failed to close {trade_id}")
        
        return ok
    
    def get_open_trade(self, trade_id):
        url = f"accounts/{id.ACCOUNT_ID}/trades/{trade_id}"
        ok, response = self.make_request(url)
        
        if ok == True and "trade" in response:
            return OpenTrade(response["trade"])
        
    def get_open_trades(self):
        url = f"accounts/{id.ACCOUNT_ID}/openTrades"
        ok, response = self.make_request(url)
        
        if ok == True and "trades" in response:
            return [OpenTrade(x) for x in response["trades"]]
