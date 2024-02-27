from ..models.Article import Article
from ..models.Company import Company
from NewsSentiment import TargetSentimentClassifier
import re
from ..connect import get_db_connection
import tldextract
import requests
import os
import logging
from datetime import datetime, timedelta
from typing import List

SIMILARWEB_API_KEY = os.environ['SIMILARWEB_KEY']

# Class to store data about articles post-analysis
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
 

# Main batch processing class
class BatchArticleAnalysis():

    # constructor to set articles to be analysed
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
            logging.warning(f"No similarweb rank for {domain}")
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
        domain = tldextract.extract(sourceURL).registered_domain

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
            score *= 1.1 * popularityNormalised
        
        return score

    # Main article processing function
    def processArticlesParallel(self) -> List[AnalysedArticle]:
        """
        Performs processing on the articles provided
        """
        
        sentimentAnalysisTargets = []
        cleanedTargets = []
        for articleTuple in self.articles:
            company = articleTuple[0]
            article = articleTuple[1]

            # split article text to allow for sentiment analysis
            target = self.splitArticleTarget(company.name, article.text)

            # Model can't handle text where the target (i.e. company name) doesn't appear in the first 512 chars
            # This is reasonable. If an article about a company doesn't mention it in the first roughly 5 sentences
            # the article probably isn't about the company
            if len(target[0])>512:
                continue

            # add to targets
            sentimentAnalysisTargets.append(target)
            cleanedTargets.append((company, article))

        # classify text using NewsSentiment
        tsc = TargetSentimentClassifier()
        sentiments = tsc.infer(targets=sentimentAnalysisTargets, batch_size=4)


        analysedArticles:list[AnalysedArticle] = []
        # post processing of sentiments to add to list
        for i, result in enumerate(sentiments):
            analysedArticles.append(AnalysedArticle(cleanedTargets[i][0], cleanedTargets[i][1], result[0]['class_label'], result[0]['class_prob']))

        # Analyse source popularity of articles
        for aa in analysedArticles:
            popularity = self.analyseSourcePopularity(aa.sourceURL, aa.sourceName)
            if popularity is not None:
                aa.setPopularity(popularity)
        
        # Score articles based on all factors we have
        for aa in analysedArticles:
            aa.score = self.calculateArticleScore(aa)
            
        return analysedArticles