import requests
import time, base64, hashlib, hmac

class Main:
    def auth_request(user, url):
        BASE_URL = 'https://api.kucoin.com'
        now = str(int(time.time() * 1000))
        str_to_sign = str(now) + 'GET' + url
        signature = base64.b64encode(hmac.new(user.secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
        passphrase = base64.b64encode(hmac.new(user.secret.encode('utf-8'), user.passphrase.encode('utf-8'), hashlib.sha256).digest())
        headers = {
            'KC-API-KEY': user.key,
            'KC-API-SIGN': signature,
            'KC-API-TIMESTAMP': str(now),
            'KC-API-PASSPHRASE': passphrase,
            'KC-API-KEY-VERSION': '2'
            }
        r = requests.get(BASE_URL + url, headers=headers).json()
        return r['data']
    
    def request(url):
        BASE_URL = 'https://api.kucoin.com'
        r = requests.get(BASE_URL + url).json()
        return r['data']

class Api_user:
    def __init__(self, key, passphrase, secret):
        self.key = key
        self.passphrase = passphrase
        self.secret = secret


class Market_data:
    def get_user(user, type='main') -> dict:
        """ Returns the user's account information
            Parameters
            ----------
            user: Api_user
                The user to get the account information of
            type : str
                The type of account to get the information from (main, margin or trade). Defaults to main
        """
        url = '/api/v1/accounts?type=' + type
        return Main.auth_request(user, url)

    @staticmethod
    def get_price_of(ticker: str) -> float:
        """
        Returns the current price of a ticker from KuCoin

        Parameters
        ----------
        ticker : str
            The ticker to get the price of
        """
        url = 'https://api.kucoin.com/api/v1/market/orderbook/level1?symbol='
        return Main.request(url + ticker)['price']

    @staticmethod
    def get_price_of_list(tickers):
        """ Returns a list of prices for a list of tickers 

        Parameters
        ----------
        tickers : list
            A list of tickers to get the price of
        """
        prices = {}
        for ticker in tickers:
            prices[ticker] = Market_data.get_price_of(ticker)
        return prices


    def get_24h_stats(ticker: str) -> dict:
        """ Returns the 24h stats for a ticker 

        Parameters
        ----------
        ticker : str
            The ticker to get the 24h stats of
        """
        url = 'https://api.kucoin.com/api/v1/market/stats?symbol='
        return Main.request(url + ticker)['data']


    @staticmethod
    def get_24h_stats_list(tickers: list) -> dict:
        """ Returns the 24h stats for a list of tickers 

        Parameters
        ----------
        tickers : list
            A list of tickers to get the 24h stats of
        """
        stats = {}
        for ticker in tickers:
            stats[ticker] = Market_data.get_24h_stats(ticker)
        return stats
