import json
import os

import requests as rqs

class StockId:

    STOCK_ID_PAIR_URL = "https://hdz-some.free.beeceptor.com/api/get_stocks_list"
    LOCAL_STOCK_ID_FILE = "data/stock_id.json"


    def download_stock_id_data(self):    
        if not os.path.exists("data"):
            os.makedirs("data")
        filepath = os.path.join("data", "stock_id.json")

        r = rqs.get(self.STOCK_ID_PAIR_URL)
        if r.status_code == 200:
            with open(filepath, 'w+') as file:            
                json.dump(r.json(), file, indent=4)
            return r.json()
        return None


    def load_stock_id_file(self, download=False):  
        if os.path.exists("data/stock_id.json"):
            filepath = os.path.join("data", "stock_id.json")
            with open(filepath, 'r') as file:
                data = file.read()
                try:
                    obj = json.loads(data)
                    return obj
                except json.JSONDecodeError:
                    print("Stock id file is not in JSON format.")
                    return None
        elif download:
            return self.download_stock_id_data()
        print("Stock id file doesn't exist.")
        return None

    def get_stock_id_for(self, symbol):
        data = self.load_stock_id_file(download=True)
        if data is not None:
            for row in data:
                if symbol.upper() == row['Stock'].upper():
                    return row['Id']
        return None