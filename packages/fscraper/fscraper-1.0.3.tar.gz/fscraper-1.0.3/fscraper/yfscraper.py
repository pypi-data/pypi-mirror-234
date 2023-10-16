import json
import requests
import pandas as pd
import numpy as np
from datetime import date, datetime
from bs4 import BeautifulSoup
from lxml import etree
from .xpath_table import yahoo_xpath


class YahooFinanceScraper(object):
    global scraper_headers
    scraper_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
        'Cache-Control': 'no-cache, max-age=0'
    }

    def __init__(self, code):
        self.code = code.upper()
        self.statistics_dom = None

    def __get_dom(cls, url):
        html = requests.get(url=url, headers=scraper_headers).text

        soup = BeautifulSoup(html, "html.parser")
        dom = etree.HTML(str(soup))

        return dom

    def get_statistics(self):
        url = "https://finance.yahoo.com/quote/{}/key-statistics?p={}".format(
            self.code, self.code)
        self.statistics_dom = self.__get_dom(
            url=url) if self.statistics_dom is None else self.statistics_dom

        df = pd.DataFrame(index=range(1))
        df.insert(len(df.columns), 'Market Cap (intraday)', self.statistics_dom.xpath(
            yahoo_xpath['Market Cap (intraday)'])[0].text)
        df.insert(len(df.columns), 'Enterprise Value', self.statistics_dom.xpath(
            yahoo_xpath['Enterprise Value'])[0].text)
        df.insert(len(df.columns), 'Trailing P/E',
                  self.statistics_dom.xpath(yahoo_xpath['Trailing P/E'])[0].text)
        df.insert(len(df.columns), 'Forward P/E',
                  self.statistics_dom.xpath(yahoo_xpath['Forward P/E'])[0].text)
        df.insert(len(df.columns), 'PEG Ratio (5 yr expected)', self.statistics_dom.xpath(
            yahoo_xpath['PEG Ratio (5 yr expected)'])[0].text)
        df.insert(len(df.columns), 'Price/Sales (ttm)',
                  self.statistics_dom.xpath(yahoo_xpath['Price/Sales (ttm)'])[0].text)
        df.insert(len(df.columns), 'Price/Book (mrq)',
                  self.statistics_dom.xpath(yahoo_xpath['Price/Book (mrq)'])[0].text)
        df.insert(len(df.columns), 'Enterprise Value/Revenue',
                  self.statistics_dom.xpath(yahoo_xpath['Enterprise Value/Revenue'])[0].text)
        df.insert(len(df.columns), 'Enterprise Value/EBITDA',
                  self.statistics_dom.xpath(yahoo_xpath['Enterprise Value/EBITDA'])[0].text)

        return df.transpose()

    def get_stock_price(self, period: str = '1mo', interval: str = '1d'):
        r"""
        Description:
            Get historical price 
        Parameters:
            period : str(`1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max`)
            interval : str(`1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo`)
        """
        params = dict()
        params['range'] = period
        params['interval'] = interval
        params['events'] = 'div'

        df = YahooFinanceScraper.__construct_price_dataframe(self, params)

        return df

    def get_stock_price2(self, start: str = '', end: str = date.today().strftime('%Y-%m-%d'), interval: str = '1d'):
        r"""
        Description:
            Get history price with specified date. 
        Parameters:
            start: str(`yyyy-mm-dd`)
            end: str(`yyyy-mm-dd`)
            interval : str(`1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo`)
        """
        params = dict()
        params['period1'] = int(datetime.strptime(
            start, "%Y-%m-%d").timestamp())
        params['period2'] = int(datetime.strptime(end, "%Y-%m-%d").timestamp())
        params['interval'] = interval
        params['events'] = 'div'

        df = YahooFinanceScraper.__construct_price_dataframe(self, params)
        return df

    def __construct_price_dataframe(self, params):
        df = pd.DataFrame()

        url = "https://query2.finance.yahoo.com/v8/finance/chart/{}".format(
            self.code)
        html = requests.get(url=url, params=params,
                            headers=scraper_headers).text
        price_json = json.loads(html)

        df['date'] = price_json['chart']['result'][0]['timestamp']
        df['open'] = price_json['chart']['result'][0]['indicators']['quote'][0]['open']
        df['high'] = price_json['chart']['result'][0]['indicators']['quote'][0]['high']
        df['low'] = price_json['chart']['result'][0]['indicators']['quote'][0]['low']
        df['close'] = price_json['chart']['result'][0]['indicators']['quote'][0]['close']
        # Bugs: At specific times, inappropriated values of 'volume' are returned.
        df['volume'] = price_json['chart']['result'][0]['indicators']['quote'][0]['volume']

        # Add dividends if exists.
        try:
            for key, item in price_json['chart']['result'][0]['events']['dividends'].items():
                df.loc[df['date'] == item['date'],
                       'dividends'] = item['amount']
        except KeyError as e:
            df['dividends'] = np.nan
            pass

        df['date'] = df['date'].apply(lambda d: datetime.fromtimestamp(
            int(d)).strftime("%Y-%m-%d %H:%M:%S"))
        df = df.set_index('date')

        return df
