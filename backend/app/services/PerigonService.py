import requests
from models.Article import Article
import os
from datetime import datetime, timedelta
import logging
from .exceptions import APIError

API_URL = "https://api.goperigon.com/v1/"
API_KEY = os.environ['PERIGON_KEY']

def getCompanyNewsPerigon(companyName: str, timePeriodHours: int, count:int, topSources:bool=False) -> list[Article]:
    timeFrom = datetime.now() - timedelta(hours=timePeriodHours)

    endpoint = f'{API_URL}/all'
    payload = {
        'companyName': companyName,
        'sortBy': 'relevance',
        'from': timeFrom.strftime('%Y-%m-%d'),
        'size': count,
        'language': 'en',
        'apiKey': API_KEY
    }

    if topSources:
        payload['sourceGroup'] = 'top100'

    response = requests.get(endpoint, params=payload)

    if response.status_code != 200:
        logging.error(f'Failed Perigon news fetching. Error {response.status_code} - {response.json()}')
        raise APIError('Problem fetching news articles from GoPerigon')
    
    data = response.json()

    articles = []

    for articleJson in data['articles']:

        article = Article(
            title=articleJson['title'],
            sourceURL=articleJson['url'],
            datePublished=articleJson['pubDate'],
            authors=[x['name'] for x in articleJson['matchedAuthors']],
            image=articleJson['imageUrl'],
            sourceName=articleJson['source']['domain'],
            text=articleJson['content'],
            keywords=articleJson['keywords']
        )

        articles.append(article)

    return articles


