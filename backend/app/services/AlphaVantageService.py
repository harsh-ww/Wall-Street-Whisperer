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


