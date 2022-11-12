import requests
import time, base64, hashlib, hmac


def get_user(key: str, api_passphrase: str, api_secret: str, type='main') -> dict:
    """ Returns the user's account information
        Parameters
        ----------
        key : str
            The API key
        api_passphrase : str
            The API passphrase
        api_secret : str
            The API secret
        type : str
            The type of account to get the information from (main, margin or trade). Defaults to main
    """
    BASE_URL = 'https://api.kucoin.com'
    URL = '/api/v1/accounts?type=' + type
    now = str(int(time.time() * 1000))
    str_to_sign = str(now) + 'GET' + '/api/v1/accounts?type=' + type
    signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {'KC-API-KEY': key, 'KC-API-SIGN': signature,
               'KC-API-TIMESTAMP': str(now), 'KC-API-PASSPHRASE': passphrase, 'KC-API-KEY-VERSION': '2'}
    r = requests.get(BASE_URL + URL, headers=headers).json()
    return r


def get_price_of(ticker: str) -> float:
    """
    Returns the current price of a ticker from KuCoin

    Parameters
    ----------
    ticker : str
        The ticker to get the price of
    """
    URL = 'https://api.kucoin.com/api/v1/market/orderbook/level1?symbol='
    r = requests.get(URL + ticker).json()
    return r['data']['price']


def get_price_of_list(tickers):
    """ Returns a list of prices for a list of tickers 

    Parameters
    ----------
    tickers : list
        A list of tickers to get the price of
    """
    prices = {}
    for ticker in tickers:
        prices[ticker] = get_price_of(ticker)
    return prices


def get_24h_stats(ticker: str) -> dict:
    """ Returns the 24h stats for a ticker 

    Parameters
    ----------
    ticker : str
        The ticker to get the 24h stats of
    """
    URL = 'https://api.kucoin.com/api/v1/market/stats?symbol='
    r = requests.get(URL + ticker).json()
    return r['data']


def get_24h_stats_list(tickers: list) -> dict:
    """ Returns the 24h stats for a list of tickers 

    Parameters
    ----------
    tickers : list
        A list of tickers to get the 24h stats of
    """
    stats = {}
    for ticker in tickers:
        stats[ticker] = get_24h_stats(ticker)
    return stats
