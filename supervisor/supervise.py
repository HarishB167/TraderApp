from datetime import datetime, timedelta
import json
import time

import pandas as pd
import requests as rqs

import broker
from utils.telegram_bot import TelegramBot
from utils.stock_id import StockId

class Supervise:

    # OPEN_POSITIONS_URL = "https://hdz-some.free.beeceptor.com/api/get_positions"
    OPEN_POSITIONS_URL = "https://docs.google.com/spreadsheets/u/1/d/1RbDvHxAXZMgkREK_jKEZNHhciVuWp9ubqRr4zD51m10/gviz/tq"

    def get_open_positions(self):
        r = rqs.get(self.OPEN_POSITIONS_URL)
        if r.status_code == 200:
            data = r.text[47:-2]
            data = json.loads(data)
            data = json.loads(data['table']['rows'][0]['c'][0]['v'])
            return data
        else:
            return None

    def get_latest_close_for_stock(self, stock_name):
        stock_id = StockId().get_stock_id_for(stock_name)
        print("Stock id : ", stock_id)
        if stock_id is None:
            print("Unkown error : stock is returned none.")
            return
        data = broker.Downloader().download_batch_data(stock_id, 
                broker.c.ZERODHA_INTERVAL_TYPES["5minute"], 
                datetime.now() - timedelta(days=1), datetime.now())
        return data.tail(1).CLOSE

    

    def check_for_event(self, position, close):
        if position['type'] == 'LONG':
            if position['tp_hit'] == 'FALSE' and position['sl_hit'] == 'FALSE' \
                and close <= float(position['sl']):
                return f"LG : INFO : Stoploss triggered : {position['sl']}"
            if position['tp_hit'] == 'FALSE' and position['sl_hit'] == 'FALSE' \
                and close >= float(position['tp']):
                return f"LG : Action : Target triggered : {position['tp']}"

            if position['tp_hit'] == 'TRUE' and close <= float(position['trail_point_1'])\
                and position['trail_1_hit'] == 'FALSE':
                return f"LG : INFO : Trail point 1 reached : {position['trail_point_1']}"

            if position['trail_1_hit'] == 'TRUE':
                return

            if position['tp_hit'] == 'TRUE' and close >= float(position['trail_point_3'])\
                and position['trail_3_hit'] == 'FALSE':
                return f"LG : Action : Trail point 3 reached : {position['trail_point_3']}"

            if position['trail_3_hit'] == 'TRUE' and close <= float(position['trail_point_2'])\
                and position['trail_2_hit'] == 'FALSE':
                return f"LG : INFO : Trail point 3->2 reached : {position['trail_point_2']}"

            if position['trail_3_hit'] == 'TRUE' and close >= float(position['trail_point_4'])\
                and position['trail_4_hit'] == 'FALSE':
                return f"LG : Action : Trail point 3->4 reached : {position['trail_point_4']}"

            if position['trail_4_hit'] == 'TRUE' and close <= float(position['trail_point_3'])\
                and position['trail_3_hit'] == 'FALSE':
                return f"LG : INFO : Trail point 4->3 reached : {position['trail_point_3']}"

            if position['trail_4_hit'] == 'TRUE' and close >= float(position['trail_point_5'])\
                and position['trail_5_hit'] == 'FALSE':
                return f"LG : P-Action : Trail point 4->5 reached : {position['trail_point_5']}"

            if position['trail_4_hit'] == 'TRUE' and close <= float(position['trail_point_4'])\
                and position['trail_4_hit'] == 'FALSE':
                return f"LG : INFO : Trail point 5->4 reached : {position['trail_point_4']}"
        elif position['type'] == 'SHORT':
            if position['tp_hit'] == 'FALSE' and position['sl_hit'] == 'FALSE' \
                and close >= float(position['sl']):
                return f"LG : Action : Stoploss triggered : {position['sl']}"
            if position['tp_hit'] == 'FALSE' and position['sl_hit'] == 'FALSE' \
                and close <= float(position['tp']):
                return f"LG : Action : Target triggered : {position['tp']}"

            if position['tp_hit'] == 'TRUE' and close >= float(position['trail_point_1'])\
                and position['trail_1_hit'] == 'FALSE':
                return f"LG : INFO : Trail point 1 reached : {position['trail_point_1']}"

            if position['trail_1_hit'] == 'TRUE':
                return

            if position['tp_hit'] == 'TRUE' and close <= float(position['trail_point_3'])\
                and position['trail_3_hit'] == 'FALSE':
                return f"LG : Action : Trail point 3 reached : {position['trail_point_3']}"

            if position['trail_3_hit'] == 'TRUE' and close >= float(position['trail_point_2'])\
                and position['trail_2_hit'] == 'FALSE':
                return f"LG : INFO : Trail point 3->2 reached : {position['trail_point_2']}"

            if position['trail_3_hit'] == 'TRUE' and close <= float(position['trail_point_4'])\
                and position['trail_4_hit'] == 'FALSE':
                return f"LG : Action : Trail point 3->4 reached : {position['trail_point_4']}"

            if position['trail_4_hit'] == 'TRUE' and close >= float(position['trail_point_3'])\
                and position['trail_3_hit'] == 'FALSE':
                return f"LG : INFO : Trail point 4->3 reached : {position['trail_point_3']}"

            if position['trail_4_hit'] == 'TRUE' and close <= float(position['trail_point_5'])\
                and position['trail_5_hit'] == 'FALSE':
                return f"LG : P-Action : Trail point 4->5 reached : {position['trail_point_5']}"

            if position['trail_4_hit'] == 'TRUE' and close >= float(position['trail_point_4'])\
                and position['trail_4_hit'] == 'FALSE':
                return f"LG : INFO : Trail point 5->4 reached : {position['trail_point_4']}"

    def run(self):
        while True:
            positions = self.get_open_positions()
            print("Positions are : ")
            print(positions)

            for position in positions:
                stock = position['stock_name']
                print("Stock : ", stock)

                latest_close = self.get_latest_close_for_stock(stock)
                datetime = pd.to_datetime(latest_close.index.values).strftime('%d-%m-%Y %H:%M:%S').values[0]
                print("Latest close is : ", float(latest_close), datetime)
                event = self.check_for_event(position, float(latest_close))
                if event is not None:
                    TelegramBot().send_message(f"{datetime} {stock} {float(latest_close)} : {event}")
            time.sleep(10)
