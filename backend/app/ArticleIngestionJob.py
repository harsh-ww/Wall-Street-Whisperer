import schedule
from models.Company import Company
from models.Article import Article
from connect import get_db_connection
import logging
from typing import List, Tuple
from services import NewsService, AnalysisService

INGESTION_FREQUENCY = 24

# gets a list of Company objects for tracked companies

def getTrackedCompanies() -> List[Company]:
    statement = "SELECT CommonName, Exchange, TickerCode FROM company WHERE Tracked=True"
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(statement)
        results = cur.fetchall()
    conn.close()

    return [Company(rt[0], rt[1], rt[2]) for rt in results]

def ingestNewsArticles(companies: List[Company]) -> List[Tuple[Company, Article]]:
    companyArticle = []
    for company in companies:
        articles = NewsService.fetch_news(company, INGESTION_FREQUENCY)
        for article in articles:
            companyArticle.append((company, article))
    return companyArticle

# def saveAnalysedArticles(articles: List[AnalysisService.AnalysedArticle]):
#     conn = get_db_connection()
#     sqlStatement = "INSERT INTO "
#     with conn.cursor() as cur:
#         for article in articles:
#             cur.execute

def job():
    logging.info("Beginning tracked article ingestion pipeline")
    companies = getTrackedCompanies()
    articlesToProcess = ingestNewsArticles(companies)

    processor = AnalysisService.BatchArticleAnalysis(articlesToProcess)

    analysedArticles = processor.processArticlesParallel()

