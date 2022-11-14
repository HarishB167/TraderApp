import sys
from datetime import datetime, timedelta

import broker
import ui
import supervisor as sp
import stock_alerts as sa

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


if __name__ == "__main__":
    process_args()

