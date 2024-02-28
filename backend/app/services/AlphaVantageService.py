# Example AV data fetching
# maybe should be replaced with existing library which wraps around https://github.com/RomelTorres/alpha_vantage

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


def companySearch(keyword: str) -> str:
    endpoint = f'{API_URL}/query'
    payload = {'function': 'SYMBOL_SEARCH', 'keywords': keyword, 'apikey': API_KEY}
    #use symbol search to convert a string name to relevant ticker
    #Note -> prioritises ticker symbol over anything else so popular companies may not be the first response... e.g. searching "apple" does not have Apple Inc as first response, -> in which case you must input Apple%20Inc to specify the name with %20 being space
    response = requests.get(endpoint, params=payload)
    if response.status_code != 200: 
        logging.error(f'Failed Company Search... Error {response.json()}')
        raise APIError()
    
    data = response.json()
    #NEW -> get the first n matches
    #MAke sure that the type is Equity
    #IF it is london region, make it United Kingdom
    #return all such relevant data in a json to be read by the company info...
    companyData = [] #returning new json array
    for match in data:
        if match["3. type"] == "Equity":
            newCompany = {
                "symbol": match["1. symbol"],
                "name": match["2. name"],
                "matchScore": match["9. matchScore"]
            }
            if match["4. region"] == "United Kingdom":
                newCompany["symbol"] += ".LON"
            companyData.append(newCompany)
    return companyData



def getCompanyDetails(symbol: str) -> CompanyDetails:
    endpoint = f'{API_URL}/query'
    payload = {'function': 'OVERVIEW', 'symbol': symbol, 'apikey': API_KEY}

    response = requests.get(endpoint, params=payload)

    if response.status_code != 200: 
        logging.error(f'Failed AV company details fetching. Error {response.json()}')
        raise APIError()
    
    data = response.json()

    return data

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


