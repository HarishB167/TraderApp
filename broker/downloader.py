import datetime
import os

import requests as rqs
import pandas as pd

from . import constants as c, utils

class Downloader:

    def __init__(self) -> None:
        self.broker_data = utils.load_broker_data()        

    def generate_url(self, ticker, interval, fromDate, toDate, user_id):
        return (f"{c.ZERODHA_HISTORICAL_DATA_URL_PREFIX}{ticker}"
               f"/{interval}?{c.ZERODHA_HIST_DT_URL_Q_USER_ID}"
               f"={user_id}&{c.ZERODHA_HIST_DT_URL_Q_OI}="
               f"{c.ZERODHA_HIST_DT_URL_Q_OI_VAL}&"
               f"{c.ZERODHA_HIST_DT_URL_Q_DATE_FROM}={fromDate}&"
               f"{c.ZERODHA_HIST_DT_URL_Q_DATE_TO}={toDate}")

    def timedelta_underlimit_for_interval(self, interval, fromDate, toDate):
        delta = toDate - fromDate
        if delta.days <= c.ZERODHA_INTERVAL_LIMITS_IN_DAYS[interval]:
            return True
        return False

    def download_batch_data(self, ticker, interval, fromDate, toDate):
        user_id = self.broker_data[c.ZERODHA_HIST_DT_URL_Q_USER_ID]
        enctoken = self.broker_data['enctoken']
        fromDate = fromDate.strftime("%Y-%m-%d")
        toDate = toDate.strftime("%Y-%m-%d")

        url = self.generate_url(ticker, interval, fromDate, toDate, user_id)

        headers = {'authorization': f'enctoken {enctoken}'}
        print("Url is : ", url)
        r = rqs.get(url, headers=headers)
        print("r.status_code", r.status_code)
        print("r.json() ",r.json()['status'])
        if r.json()['status'] == 'success':
            if len(r.json()['data']['candles']) == 0:
                return None
            return pd.DataFrame(r.json()['data']['candles'], 
                columns=c.STOCK_DATA_HEADERS).set_index('TIME')
        else:
            print("Print some unknown error occured r.text : ", r.text)
            return None

    def create_path_for_file(self, interval, filename):
        stock_data_dir = os.path.join(c.DATA_FOLDER, c.STOCK_DATA_DIR, interval)
        filename = filename.replace(".csv", "") + ".csv"
        if not os.path.exists(stock_data_dir):
            os.makedirs(stock_data_dir)
        return os.path.join(stock_data_dir, filename)

    def save_df_to_file(self, df, filepath):
        df.to_csv(filepath)
            
    """
    fromDate and toDate should be datetime object
    """
    def download_data(self, ticker, interval, fromDate, toDate, filename_to_save=None):
        if not isinstance(fromDate, datetime.datetime) or not isinstance(toDate, datetime.datetime):
            raise ValueError("One of both date ranges are not a datetime object.")
        if (toDate - fromDate).days <= 0:
            raise ValueError("Date range cannot be 0 or negative.")

        if self.timedelta_underlimit_for_interval(interval, fromDate, toDate):        
            data = self.download_batch_data(ticker, interval, fromDate, toDate)
            filename = filename_to_save if filename_to_save is not None else ticker
            self.save_df_to_file(data, self.create_path_for_file(interval, filename))
            return data
        else:
            limit_days = c.ZERODHA_INTERVAL_LIMITS_IN_DAYS[interval]
            print("Limit days : ", limit_days)
            print("fromDate / toDate", fromDate, "/", toDate)
            last_center_point = None
            center_point = toDate - datetime.timedelta(days=limit_days)
            main_df = None
            while center_point > fromDate:
                current_to_date = toDate if last_center_point is None else last_center_point
                df = self.download_batch_data(ticker, interval, center_point, current_to_date)
                if main_df is None:
                    main_df = df
                else:
                    main_df = pd.concat([df, main_df])
                last_center_point = center_point
                center_point = center_point - datetime.timedelta(days=limit_days)

            df = self.download_batch_data(ticker, interval, fromDate, last_center_point)
            main_df = pd.concat([df, main_df]).drop_duplicates()
            print(main_df.head())
            print(main_df.tail())        
            filename = filename_to_save if filename_to_save is not None else ticker
            self.save_df_to_file(main_df, self.create_path_for_file(interval, filename))
            return main_df
            