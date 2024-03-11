import requests
from models.Article import Article
import os
from datetime import datetime, timedelta
import logging
from .exceptions import APIError

API_URL = "https://api.goperigon.com/v1/"
API_KEY = os.environ['PERIGON_KEY']

# retrieves news articles related to a given company from the Perigon API
def getCompanyNewsPerigon(companyName: str, timePeriodHours: int, count:int, topSources:bool=False) -> list[Article]:
    # calculate the time from which to fetch news
    timeFrom = datetime.now() - timedelta(hours=timePeriodHours)
    # construct API request
    endpoint = f'{API_URL}/all'
    payload = {
        'companyName': companyName,
        'sortBy': 'relevance',
        'from': timeFrom.strftime('%Y-%m-%d'),
        'size': count,
        'language': 'en',
        'showReprints': False,
        'apiKey': API_KEY
    }
    
    # add option to retrieve articles from top sources
    if topSources:
        payload['sourceGroup'] = 'top100'
    # make request
    response = requests.get(endpoint, params=payload)
    # handle response
    if response.status_code != 200:
        logging.error(f'Failed Perigon news fetching. Error {response.status_code} - {response.json()}')
        raise APIError('Problem fetching news articles from GoPerigon')
    
    data = response.json()
    
    # parse articles from response
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
            keywords=articleJson['keywords'],
            summary=articleJson['summary']
        )

        articles.append(article)

    return articles


