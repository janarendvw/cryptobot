import requests


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
    