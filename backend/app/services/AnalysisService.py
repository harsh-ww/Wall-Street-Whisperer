from models.Article import Article
from models.Company import Company
from NewsSentiment import TargetSentimentClassifier
import re
from connect import get_db_connection
import tldextract
import requests
import os
import logging
from datetime import datetime, timedelta
from typing import List
import time
from services.SummaryService import generateSummary

SIMILARWEB_API_KEY = os.environ['SIMILARWEB_KEY']

# Class to store data about articles post-analysis
class AnalysedArticle(Article):
    sentimentLabel = None
    sentimentProb = None
    sitePopularity = None
    score = 0
    summary = ''

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


    def splitArticleTarget(self, companyName:str, articleText:str) -> tuple[str, str, str]:
        """
        Splits an article text into a tuple of strings with the company entity separated in order to allow targeted sentiment analysis
        """

        # split the article at the company name
        articleTextSplit = re.split(companyName, articleText, 1, re.IGNORECASE) 

        if len(articleTextSplit)<2:
            # company name doesn't appear in text - may not be an exact match. Provide anyway
            return None
            return ("", companyName, articleText)
        
        # compose a 3-tuple with the text before and after the company
        return (articleTextSplit[0], companyName, articleTextSplit[1])
    

    def fetchPopularity(self, domain:str):
        """
        Fetches the popularity of a given domain from similarweb
        """

        # Make a request to SimilarWeb
        endpoint = f"https://api.similarweb.com/v1/similar-rank/{domain}/rank"
        query = {
            'api_key': SIMILARWEB_API_KEY,
        }

        response = requests.get(endpoint, params=query)

        if response.status_code == 404:
            logging.warning(f"No similarweb rank for {domain}")
            return None
        elif response.status_code == 429:
            logging.warning("Too many requests")
            time.sleep(1)
        else:
            if response.status_code != 200:
                logging.error(f'Failed Similarweb fetching. Error {response.status_code} - {response.text} ')
                return None
        
        return response.json()['similar_rank']['rank']

    def updatePopularity(self, domain:str, popularity:int, name:str=None):
        """
        Caches the popularity of a given news site's domain in the database
        """

        insertQuery = "INSERT INTO web_source (SourceName, SourceURL, Popularity, PopularityLastFetched) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING"
        updateQuery = "UPDATE web_source SET Popularity=%s, PopularityLastFetched=%s WHERE SourceURL=%s"
        
        conn = get_db_connection()
        
        with conn.cursor() as cur:

            # New entries supply a name to this function
            if name is not None:
                print("updating source popularity")
                cur.execute(insertQuery, [name, domain, popularity, datetime.now().isoformat()])
            else:
                # existing entries already have a name
                cur.execute(updateQuery, [popularity, datetime.now().isoformat(), domain])
            # save changes
            conn.commit()
        
        conn.close()


    def analyseSourcePopularity(self, sourceURL:str, sourceName:str=None):
        """
        Analyses the popularity of a news source - either uses cached or refetches from SimilarWeb
        """

        # extract domain from source URL - domains have similarweb scores
        domain = tldextract.extract(sourceURL).registered_domain

        query = "SELECT Popularity, PopularityLastFetched from web_source WHERE SourceURL LIKE %s"

        conn = get_db_connection()
        with conn.cursor() as cur:

            # fetch rank from database
            cur.execute(query, [("%" + domain + "%")])
            result = cur.fetchone()

            # Retrieve cached result or refetch
            if result is None:
                # don't have a rank for the current domain - fetch it
                rank = self.fetchPopularity(domain)

                # Error fetching rank
                if rank is None:
                    return None
                
                name = domain if sourceName is None else sourceName

                self.updatePopularity(domain, rank, name)
                
                return rank
            else:
                # cached result exists - check when it was last fetched
                lastFetched = result[1]

                # rank is over a month old - refetch and update db
                if lastFetched < datetime.now() - timedelta(days=30):
                    rank = self.fetchPopularity(domain)
                    if rank is None:
                        return None
                    
                    self.updatePopularity(domain, rank)
                    return rank
                else:
                    # rank was fetched recently - use cached
                    return result[0]


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
        
        # Clean up articles

        sentimentAnalysisTargets = []
        cleanedTargets = []
        for articleTuple in self.articles:
            company = articleTuple[0]
            article = articleTuple[1]
            
            combinedText = article.title + " " + article.text
            # split article text to allow for sentiment analysis
            target = self.splitArticleTarget(company.name, combinedText)
            
            # article is not about target
            if combinedText.count(company.name)<2:
                continue

            # Model can't handle text where the target (i.e. company name) doesn't appear in the first 512 chars
            # This is reasonable. If an article about a company doesn't mention it in the first roughly 5 sentences
            # the article probably isn't about the company
            if target is None or len(target[0])>512:
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

        logging.info("Generating article summaries")
        # Generate article summaries
        # for aa in analysedArticles:
        #     aa.summary = generateSummary(aa.text)
            
        return analysedArticles