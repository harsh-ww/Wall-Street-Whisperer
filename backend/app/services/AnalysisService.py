from ..models.Article import Article
from ..models.Company import Company
from NewsSentiment import TargetSentimentClassifier
import re
from ..connect import get_db_connection
import urllib.parse as urlparse
import requests

class AnalysedArticle(Article):
    sentiment = None
    sentimentScore = None
    sitePopularity = None

    def __init__(self, company:Company, article:Article, sentimentLabel: str, sentimentProb: float) -> None:
        super().__init__(article.title, article.sourceURL, article.datePublished, article.sourceName, article.authors, article.image, article.text, article.keywords)
        self.company = company
        self.sentimentLabel = sentimentLabel
        self.sentimentProb = sentimentProb
 

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

    # def fetchAndUpdatePopularity(self, domain):
    #   # https://developers.similarweb.com/reference/global-rank
    #     pass

    # def analyseSourcePopularity(self, sourceURL:str):
    #     # extract domain from source URL
    #     domain = urlparse.urlparse(sourceURL).netloc

    #     query = "SELECT Popularity, PopularityLastFetched from websource WHERE SourceURL LIKE %%%s%%"
    #     conn = get_db_connection()
    #     popularity = -1
    #     with conn.cursor() as cur:
    #         cur.execute(query, [domain])
    #         if cur.rowcount==0:
    #             # new source or last fetched a while ago - call similarweb and update
    #             return None
    #         else:
    #             return cur.fetchone()[0]

    def calculateArticleScore(self):
        pass
                

    def processArticlesParallel(self):
        sentimentAnalysisTargets = []
        for articleTuple in self.articles:
            sentimentAnalysisTargets.append(self.splitArticleTarget(articleTuple[0].name, articleTuple[1].text))

        tsc = TargetSentimentClassifier()
        sentiments = tsc.infer(targets=sentimentAnalysisTargets, batch_size=4)

        # run popularity analysis
        # calculate article score

        analysedArticles = []

        for i, result in enumerate(sentiments):
            analysedArticles.append(AnalysedArticle(self.articles[i][0], self.articles[i][1], result[0]['class_label'], result[0]['class_prob']))

        return analysedArticles