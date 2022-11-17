import sys
from datetime import datetime, timedelta

import broker
import ui
import supervisor as sp
import stock_alerts as sa
import chartink_scanner as cs

def process_args():
    print("Program loaded")
    if len(sys.argv) > 1:
        if sys.argv[1] == "login":
            print("Logging in...")
            broker.Login().login()
        if sys.argv[1] == "download":
            print("Downloading")
            toDate = datetime.now()
            fromDate = toDate - timedelta(days = 4510)
            broker.Downloader().download_data("1270529", broker.c.ZERODHA_INTERVAL_TYPES["5minute"], fromDate, toDate, 'ICICIBANK')

        if sys.argv[1] == 'plot':
            print("Plotting")
            filename = "data/stock_data/5minute/ICICIBANK.csv"
            ui.Chart().plot(filename)

        if sys.argv[1] == "supervise":
            print("Supervising")
            sp.Supervise().run()

        if sys.argv[1] == "alert":
            print("Alerting service")
            sa.DataLoader().run()

        if sys.argv[1] == "change":
            print("Website change detect service")
            url = "https://chartink.com/screener/process"
            method = "POST"
            data = {"scan_clause": "( {33619} ( ( {33619} ( [-1] 5 minute close > [-2] 5 minute max( 20 , [0] 5 minute open )"
                        " and [-1] 5 minute close > [-2] 5 minute max( 20 , [0] 5 minute close ) and [-1] 5 minute high > [0]"
                        " 5 minute high and [-1] 5 minute high > [0] 5 minute upper bollinger band( 20 , 1.5 )"
                        " and( {cash} ( [0] 5 minute close <= [-1] 5 minute close and [0] 5 minute close <= [-1] 5 minute open )"
                        " ) ) ) or( {33619} ( [-1] 5 minute close < [-2] 5 minute min( 20 , [0] 5 minute open ) and [-1] 5 minute"
                        " close < [-2] 5 minute min( 20 , [0] 5 minute close ) and [-1] 5 minute low < [0] 5 minute low and [-1]"
                        " 5 minute low < [0] 5 minute lower bollinger band( 20 , 1.5 ) and( {cash} ( [0] 5 minute close >= [-1] 5"
                        " minute close and [0] 5 minute close >= [-1] 5 minute open ) ) ) ) ) )"
            }
            cs.ChangeDetect(url, method, data).run()


if __name__ == "__main__":
    process_args()

