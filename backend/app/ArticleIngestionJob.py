import schedule
from models.Company import Company
from models.Article import Article
from connect import get_db_connection
import logging
from typing import List, Tuple
from services import NewsService, AnalysisService
import tldextract
import requests, json

INGESTION_FREQUENCY = 24
SCORE_THRESHOLD = 50   # An article have to be greater than this score to notify users

# gets a list of Company objects for tracked companies

def getTrackedCompanies() -> List[Company]:
    """
    Gets a list of tracked companies from the database
    """
    query = "SELECT CommonName, Exchange, TickerCode FROM company"
    conn = get_db_connection()

    with conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
    
    conn.close()

    return [Company(rt[0], rt[1], rt[2]) for rt in results]

def ingestNewsArticles(companies: List[Company]) -> List[Tuple[Company, Article]]:
    """
    Gets news articles for a given list of companies
    """

    companyArticle = []
    for company in companies:
        articles = NewsService.fetch_news(company, INGESTION_FREQUENCY)
        for article in articles:
            companyArticle.append((company, article))
    return companyArticle

def saveAnalysedArticles(articles: List[AnalysisService.AnalysedArticle]):
    """"
    Persists analysed articles to the database
    """

    conn = get_db_connection()

    newarticleIDs = []  # A list of important new news articles

    with conn.cursor() as cur:
        for article in articles:
            # get company ID by ticker code
            cur.execute("""SELECT CompanyID FROM company WHERE TickerCode=%s""", [article.company.ticker])
            result = cur.fetchone()
            if result is None:
                # The ticker isn't found in the database
                logging.error(f"Ticker {article.company.ticker} not found")

                # Skip this article and continue with the rest of the batch job
                continue
                
            company_id = result[0]

            # Get source ID
            domain = tldextract.extract(article.sourceURL).registered_domain
            cur.execute("""SELECT SourceID FROM web_source WHERE SourceURL=%s""", [domain])
            result = cur.fetchone()
            if result is None:
                # source hasn't been inserted as site doesn't have a popularity - may have been an error in the process
                cur.execute("""INSERT INTO web_source (SourceName, SourceURL) VALUES (%s, %s) RETURNING SourceID""", [article.sourceName, domain])
                sourceID = cur.fetchone()[0]
            else:
                sourceID = result[0]
            
            # Insert article
                
            # Storing keywords and authors as text for simplicity
            keywordsAsText = str([x['name'] for x in article.keywords]).replace("[","").replace("]", "")
            authorsAsText =  str(article.authors).replace("[","").replace("]", "")

            insertSQL = """
                INSERT INTO article (Title, ArticleURL, SourceID, PublishedDate, Authors, ImageURL, SentimentLabel, SentimentScore, OverallScore, Keywords) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING ArticleID
            """

            cur.execute(insertSQL, [article.title, article.sourceURL, sourceID, article.datePublished, authorsAsText, article.image, article.sentimentLabel, article.sentimentProb, article.score, keywordsAsText])
            
            articleID = cur.fetchone()[0]

            # Link company and article
            cur.execute("""INSERT INTO company_articles (CompanyID, ArticleID) VALUES (%s, %s)""", [company_id, articleID])

            conn.commit()

            # Add the article ID to a list to be notified, if its score exceeds threshold
            if abs(article.score) >= SCORE_THRESHOLD:
                newarticleIDs.append(articleID)

                # Add important articles to the notifications table
                cur.execute("""INSERT INTO notifications (ArticleID) VALUES (%s)""", (articleID,))

    conn.close()

    return newarticleIDs

def job():
    """
    Main job for article ingestion and analysis
    """

    logging.info("Beginning tracked article ingestion pipeline")
    companies = getTrackedCompanies()

    logging.info("Fetching articles for tracked companies")
    articlesToProcess = ingestNewsArticles(companies)

    logging.info("Performing article analysis")
    processor = AnalysisService.BatchArticleAnalysis(articlesToProcess)
    analysedArticles = processor.processArticlesParallel()

    logging.info("Saving analysed articles")
    newartleIDs = saveAnalysedArticles(analysedArticles)


    """
    Job for sending emails 
    """
    if newartleIDs:
        data = {'recipients':["stockapp220@gmail.com"], 'articleList': newartleIDs} #CHANGE

        response = requests.post('http://localhost:5000/sendarticleemail',
                            content_type='application/json',
                            data = json.dumps(dict(data)))
        
        if response.status_code == 201:
            logging.info("Article emails sent successfully.")
        else:
            logging.error("There is an error sending article emails.")

# Run this as a CRON JOB
# schedule.every(INGESTION_FREQUENCY).hours()

if __name__ == "__main__":
    job()