from datetime import datetime, timedelta
import requests
import logging
import os
from .exceptions import APIError
from models.Article import Article
from typing import List

API_URL = "https://www.alphavantage.co"
API_KEY = os.environ['AV_KEY']

class CompanyDetails:
    def __init__(self, name) -> None:
        self.name = name

# search for company by keyword
def companySearch(keyword: str) -> str:
    endpoint = f'{API_URL}/query'
    payload = {'function': 'SYMBOL_SEARCH', 'keywords': keyword, 'apikey': API_KEY}
    #use symbol search to convert a string name to relevant ticker
    response = requests.get(endpoint, params=payload)
    if response.status_code != 200: 
        logging.error(f'Failed Company Search... Error {response.json()}')
        raise APIError()
    
    data = response.json()['bestMatches']
    companyData = [] 
    for match in data:
        if match["3. type"] == "Equity":
            newCompany = {
                "symbol": match["1. symbol"],
                "name": match["2. name"],
                "exchange": match["4. region"]
            }
            companyData.append(newCompany)
    return companyData

# get details of a company for non-US region.
def getCompanyDetailsNonUS(symbol:str):
    endpoint = f'{API_URL}/query'
    payload = {'function': 'SYMBOL_SEARCH', 'keywords': symbol, 'apikey': API_KEY}
    # use symbol search to convert a string name to relevant ticker
    # prioritises ticker symbol over anything else
    response = requests.get(endpoint, params=payload)
    if response.status_code != 200: 
        logging.error(f'Failed Company Search... Error {response.json()}')
        raise APIError()

    data = response.json()['bestMatches']
    return {
        "symbol": data[0]["1. symbol"],
        "name": data[0]["2. name"],
        "exchange": data[0]["4. region"],
        "currency": data[0]["8. currency"]
    }
    

def getCompanyDetails(symbol: str) -> CompanyDetails:
    endpoint = f'{API_URL}/query'
    payload = {'function': 'OVERVIEW', 'symbol': symbol, 'apikey': API_KEY}

    response = requests.get(endpoint, params=payload)

    if response.status_code != 200: 
        logging.error(f'Failed AV company details fetching. Error {response.json()}')
        raise APIError()
    
    data = response.json()

    return data

# get news articles for a company
def getCompanyNews(symbol: str, timePeriodHours: int, count:int) -> List[Article]:
    timeFrom = datetime.now() - timedelta(hours=timePeriodHours)

    endpoint = f'{API_URL}/query'
    payload = {
        'function': 'NEWS_SENTIMENT',
        'tickers': symbol,
        'time_from': timeFrom.strftime('%Y%m%dT%H%M'),
        'limit': count,
        'apikey': API_KEY
    }

    response = requests.get(endpoint, params=payload)

    if response.status_code != 200:
        logging.error(f'Failed AV news fetching. Error {response.json()}')
        raise APIError('Problem fetching news articles from AlphaVantage')
    
    data = response.json()

    articles = []

    for articleJson in data['feed']:
        article = Article(
            title=articleJson['title'],
            sourceURL=articleJson['url'],
            datePublished=articleJson['time_published'],
            authors=articleJson['authors'],
            image=articleJson['banner_image'],
            sourceName=articleJson['source']
        )

        articles.append(article)

    return articles

# get current stock price for a company
def getCurrentStockPrice(symbol: str):
    if not symbol:
        return None
    endpoint = f'{API_URL}/query'
    payload = {'function': 'GLOBAL_QUOTE', 'symbol': symbol, 'apikey': API_KEY}

    response = requests.get(endpoint, params=payload)

    if response.status_code != 200: 
        logging.error(f'Failed AV stock price fetching. Error {response.json()}')
        raise APIError()
    
    data = response.json()
    cleanedDict = {}
    for k,v in data['Global Quote'].items():
        if k == '01. symbol':
            continue
        cleanedDict[k[4:]] = v

    return cleanedDict

# get time series data for a company from AlphaVantage
def getTimeSeries(symbol:str, granularity:str):
    if not granularity in ['DAILY', 'WEEKLY', 'MONTHLY']:
        return {}
    
    granularityFunction = {
        'DAILY': 'TIME_SERIES_DAILY',
        'WEEKLY': 'TIME_SERIES_WEEKLY',
        'MONTHLY': 'TIME_SERIES_MONTHLY'
    }
    label = {
        'DAILY': 'Time Series (Daily)',
        'WEEKLY': 'Weekly Time Series',
        'MONTHLY': 'Monthly Time Series'
    }

    endpoint = f'{API_URL}/query'
    payload = {'function': granularityFunction[granularity], 'symbol': symbol, 'apikey': API_KEY}

    response = requests.get(endpoint, params=payload)


    if response.status_code != 200: 
        logging.error(f'Failed AV time series fetching. Error {response.json()}')
        raise APIError()
    
    data = response.json()

    # Invalid symbol supplied
    if label[granularity] not in data:
        return {}
    
    return data[label[granularity]]

