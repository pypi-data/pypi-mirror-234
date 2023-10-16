import time
import requests
import pandas as pd
from datetime import datetime
from io import StringIO


class KabutanScraper(object):
    global scraper_headers
    scraper_headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
        'Cache-Control': 'no-cache, max-age=0'
    }

    def __init__(self, code):
        self.code = code.upper().replace('.T', '')

    def get_stock_price_by_minutes(self):
        r"""
        Description:
            Get stock price by minute
        """
        url = "https://kabutan.jp/stock/read?c={}&m=4&k=1&{}=".format(self.code, int(time.time() * 1000))
        html = requests.get(url=url, headers=scraper_headers).text
        csvStringIO = StringIO(html)
        df = pd.read_csv(csvStringIO, sep=",", header=None)
        
        df = df.iloc[1:]    # Drop the first row, dummy data

        def convert_to_datetime(date1, date2):
            # Combine the two dates
            combined_date = date2 + date1[-6:]
            
            # Convert to datetime object
            datetime_obj = datetime.strptime(combined_date, "%Y.%m.%d/%H:%M")

            return datetime_obj

        df['date'] = df.apply(lambda x: convert_to_datetime(x[0], x[6]), axis=1)
        df = df.rename(columns={1: 'open',2:'high', 3:'low', 4:'close', 5:'volume'}, inplace=False)
        df= df.drop([0, 6,7,8,9,10,11], axis=1)   # Drop unneeded columns

        # Multiply 0.1 & typecasting(for decimal point is not displayed).
        for col in ['open', 'high', 'low', 'close']:
            df[col] = df[col].astype('int')
            df[[col]] = df[[col]].apply(lambda x: (x * 0.1).astype(float))

        df = df.sort_values(by=['date'])
        df = df.set_index('date')
        return df