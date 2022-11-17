import time

from bs4 import BeautifulSoup
import requests as rqs

from utils.telegram_bot import TelegramBot


class ChangeDetect:

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'referer': 'https://chartink.com/screener/backtest-intraday-priceaction-snr',
        'x-requested-with': 'XMLHttpRequest'
    }
    cookies = None

    def __init__(self, url, method, data):
        self.url = url
        self.method = method
        self.data = data
        self.telegram_bot = TelegramBot()

    def set_cookies(self):
        url = "https://chartink.com/screener/backtest-intraday-priceaction-snr"
        r = rqs.get(url, headers=self.HEADERS)
        self.cookies = r.cookies.get_dict()
        soup = BeautifulSoup(r.text, features="html.parser")
        self.token = soup.find("meta", {"name":"csrf-token"})['content']
        print("token : ", self.token)
        print("Setting cookies")

    def prepare_headers(self):
        self.HEADERS['x-csrf-token'] = self.token
        return self.HEADERS

    def get_scanned_stocks(self):
        if self.method == "POST":
            r = rqs.post(self.url, data=self.data, headers=self.prepare_headers(), cookies=self.cookies)
            if r.status_code == 200:
                return r.json()['data']
            else:
                print("Error occured : ", r.status_code ," ", r.text)

    def run(self):
        self.set_cookies()
        while True:
            try:
                print("-"*50)
                stocks = self.get_scanned_stocks()
                if len(stocks) > 0:
                    print(stocks)
                    res = ""
                    for stock in stocks:
                        print(stock['nsecode'])
                        res += stock['nsecode'] + ", "

                    message = f"Scanned result : {res}"
                    self.telegram_bot.send_message(message)
            except Exception as e:
                print("Error ocured : ", str(e))
            time.sleep(10)
