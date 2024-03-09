"""
This module contains all flask routes that get news articles.
"""
from datetime import datetime
from flask import Blueprint, jsonify
from connect import get_db_connection

article_routes_blueprint = Blueprint("article_routes", __name__)


def get_articles_by_ticker_db(ticker: str):
    """
    Returns articles that matches the ticker code of a company
    """

    query = """
            SELECT article.*, web_source.Popularity AS SourcePopularity
            FROM article
            JOIN company_articles ON article.ArticleID = company_articles.ArticleID
            JOIN company ON company_articles.CompanyID = company.CompanyID
            JOIN web_source ON article.SourceID = web_source.SourceID
            WHERE company.TickerCode = %s;
        """

    conn = get_db_connection()
    articles = []
    with conn.cursor() as cur:
        cur.execute(query, [ticker])
        rows = cur.fetchall()
        for row in rows:
            row_dict = dict(zip([column[0] for column in cur.description], row))
            articles.append(row_dict)

    conn.close()
    return articles


@article_routes_blueprint.route("/articles/<ticker>", methods=["GET"])
def get_articles(ticker: str):
    """
    A route that executes the get_articles_by_ticker_db function
    """
    # from_date = request.args.get('from_date')
    articles = get_articles_by_ticker_db(ticker)

    return jsonify(articles)


def get_recent_articles():
    conn = get_db_connection()
    articles = []
    with conn.cursor() as cur:
        cur.execute(
            """WITH Ranked AS (SELECT a.*, ca.companyID, ROW_NUMBER() 
               OVER (PARTITION BY ca.CompanyID ORDER BY a.PublishedDate DESC, ABS(a.overallScore) DESC) 
               AS rn 
               FROM article a 
               INNER JOIN company_articles ca 
               on a.articleID=ca.articleID) 
               SELECT r.*, c.CompanyName 
               FROM Ranked r 
               JOIN company c 
               ON r.companyID=c.companyID 
               ORDER BY rn ASC, PublishedDate DESC 
               LIMIT 6;"""
        )
        rows = cur.fetchall()
        for row in rows:
            row_dict = dict(zip([column[0] for column in cur.description], row))
            articles.append(row_dict)

    return articles


@article_routes_blueprint.route("/recent-articles", methods=["GET"])
def recent_articles():
    # from_date = request.args.get('from_date')
    articles = get_recent_articles()

    return jsonify(articles)


@article_routes_blueprint.route("/featured-article/<ticker>/<date>", methods=["GET"])
def featured_article(ticker, date):
    """
    Get the highest scoring article on a particular date
    """
    date_input = datetime.strptime(
        date, "%Y-%m-%d"
    ).date()  # Convert into a valid date format

    conn = get_db_connection()
    with conn.cursor() as cur:
        query = """
                    SELECT *
                    FROM article 
                    JOIN company_articles ON article.ArticleID = company_articles.ArticleID
                    JOIN company ON company_articles.CompanyID = company.CompanyID
                    WHERE PublishedDate = %s AND TickerCode = %s
                    ORDER BY ABS(OverallScore) DESC
                    LIMIT 1;
                    """

        cur.execute(query, (date_input, ticker))
        article = cur.fetchone()

        if not article:
            return {}

        result = {}
        result["title"] = article[1]
        result["articleurl"] = article[2]
        result["sourceid"] = article[3]
        result["publisheddate"] = article[4]
        result["authors"] = article[5]
        result["imageurl"] = article[6]
        result["sentimentlabel"] = article[7]
        result["sentimentscore"] = article[8]
        result["overallscore"] = article[9]
        result["summary"] = article[10]
        result["keywords"] = article[11]

        return jsonify(result)
