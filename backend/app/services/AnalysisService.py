from ..models.Article import Article
from ..models.Company import Company
from NewsSentiment import TargetSentimentClassifier
import re
from ..connect import get_db_connection
import urllib.parse as urlparse
import requests
import os
import logging
from datetime import datetime, timedelta
from typing import List

SIMILARWEB_API_KEY = os.environ['SIMILARWEB_KEY']

class AnalysedArticle(Article):
    sentimentLabel = None
    sentimentProb = None
    sitePopularity = None
    score = 0

    def __init__(self, company:Company, article:Article, sentimentLabel: str, sentimentProb: float) -> None:
        super().__init__(article.title, article.sourceURL, article.datePublished, article.sourceName, article.authors, article.image, article.text, article.keywords)
        self.company = company
        self.sentimentLabel = sentimentLabel
        self.sentimentProb = sentimentProb

    def setPopularity(self, popularity:int):
        self.sitePopularity = popularity
 

class BatchArticleAnalysis():

    def __init__(self, articles: list[tuple[Company, Article]]) -> None:
        self.articles = articles


    def splitArticleTarget(self, companyName, articleText) -> tuple[str, str, str]:
        """
        Splits an article text into a tuple of strings with the company entity separated in order to allow targeted sentiment analysis
        """
        # split the article 
        articleTextSplit = re.split(companyName, articleText, 1, re.IGNORECASE) 
        if len(articleTextSplit)<2:
            # company name doesn't appear in text - may not be an exact match. Provide anyway
            return ("", companyName, articleText)
        return (articleTextSplit[0], companyName, articleTextSplit[1])
    
    def fetchPopularity(self, domain:str):
        """
        Fetches the popularity of a given domain from similarweb
        """
        endpoint = f"https://api.similarweb.com/v1/similar-rank/{domain}/rank"
        query = {
            'api_key': SIMILARWEB_API_KEY,
        }

        response = requests.get(endpoint, params=query)

        if response.status_code == 404:
            logging.warn(f"No similarweb rank for {domain}")
            return None
        else:
            if response.status_code != 200:
                logging.error(f'Failed Similarweb fetching. Error {response.status_code} - {response.json()}')
                return None
        
        return response.json()['similar_rank']['rank']

    def updatePopularity(self, domain:str, popularity:int, name:str=None):
        """
        Caches the popularity of a given news site's domain in the database
        """
        insertQuery = "INSERT INTO web_source (SourceName, SourceURL, Popularity, PopularityLastFetched) VALUES (%s, %s, %d, %s) ON CONFLICT DO NOTHING"
        updateQuery = "UPDATE web_source SET Popularity=%d, PopularityLastFetched=%s WHERE SourceURL=%s"
        conn = get_db_connection()
        with conn.cursor() as cur:
            if name is not None:
                cur.execute(insertQuery, [name, domain, popularity, datetime.now().isoformat()])
            else:
                cur.execute(updateQuery, [popularity, datetime.now().isoformat(), domain])


    def analyseSourcePopularity(self, sourceURL:str, sourceName:str=None):
        """
        Analyses the popularity of a news source - either uses cached or refetches from SimilarWeb
        """
        # extract domain from source URL
        domain = urlparse.urlparse(sourceURL).netloc

        query = "SELECT Popularity, PopularityLastFetched from websource WHERE SourceURL LIKE %%%s%%"
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, [domain])

            if cur.rowcount==0:
                # don't have a rank for the current domain
                rank = self.fetchPopularity(domain)
                if rank is None:
                    return None
                name = domain if sourceName is None else sourceName
                self.updatePopularity(domain, rank, name)
                return rank
            else:
                lastFetched = datetime.fromisoformat(cur.fetchone()[1])
                # rank is over a month old - refetch and update db
                if lastFetched < datetime.now() - timedelta(days=30):
                    rank = self.fetchPopularity(domain)
                    if rank is None:
                        return None
                    
                    self.updatePopularity(domain, rank)
                    return rank
                else:
                    # rank was fetched recently - use cached
                    return cur.fetchone()[0]


    # this algorithm is very naive
    def calculateArticleScore(self, article:AnalysedArticle):
        """
        Scoring algorithm for articles
        """
        score = 0
        # handle sentiment
        if article.sentimentLabel == 'negative':
            score -= 100 * article.sentimentProb
        elif article.sentimentLabel == 'positive':
            score += 100 * article.sentimentProb
        else:
            score = 50 * article.sentimentProb

        if article.sitePopularity is not None:
            if article.sitePopularity > 500000:
                # unpopular website, ignore
                return score
            popularityNormalised = 1 - (article.sitePopularity - 1)/(500000)
            # multiply based on popularity of the website
            score *= 1.5 * popularityNormalised
        
        return score


    def processArticlesParallel(self) -> List[AnalysedArticle]:
        """
        Performs processing on the articles provided
        """
        sentimentAnalysisTargets = []
        for articleTuple in self.articles:
            sentimentAnalysisTargets.append(self.splitArticleTarget(articleTuple[0].name, articleTuple[1].text))

        tsc = TargetSentimentClassifier()
        sentiments = tsc.infer(targets=sentimentAnalysisTargets, batch_size=4)

        analysedArticles:list[AnalysedArticle] = []

        for i, result in enumerate(sentiments):
            analysedArticles.append(AnalysedArticle(self.articles[i][0], self.articles[i][1], result[0]['class_label'], result[0]['class_prob']))

        for aa in analysedArticles:
            popularity = self.analyseSourcePopularity(aa.sourceURL, aa.sourceName)
            if popularity is not None:
                aa.setPopularity(popularity)
        
        for aa in analysedArticles:
            aa.score = self.calculateArticleScore(aa)
            
        return analysedArticles