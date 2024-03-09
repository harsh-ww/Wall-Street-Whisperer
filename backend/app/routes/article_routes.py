from flask import Blueprint, jsonify
from connect import get_db_connection


article_routes_blueprint = Blueprint('article_routes', __name__)

def get_articles_by_ticker_db(ticker: str):
        query = """
            SELECT article.*, web_source.Popularity AS SourcePopularity
            FROM article
            JOIN company ON article.CompanyID = company.CompanyID
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
     

@article_routes_blueprint.route('/articles/<ticker>', methods=['GET'])
def get_articles(ticker:str):
        #from_date = request.args.get('from_date')
        articles = get_articles_by_ticker_db(ticker)

        return jsonify(articles)

def get_recent_articles():
    conn = get_db_connection()
    articles = []
    with conn.cursor() as cur:
          cur.execute("WITH Ranked AS (SELECT a.*, ROW_NUMBER() OVER (PARTITION BY a.CompanyID ORDER BY a.PublishedDate DESC, ABS(a.overallScore) DESC) AS rn FROM article a) SELECT r.*, c.CompanyName FROM Ranked r JOIN company c ON r.companyID=c.companyID ORDER BY rn ASC, PublishedDate DESC LIMIT 6;")
          rows = cur.fetchall()
          for row in rows:
                row_dict = dict(zip([column[0] for column in cur.description], row))
                articles.append(row_dict)

    return articles

@article_routes_blueprint.route('/recent-articles', methods=['GET'])
def recent_articles():
        #from_date = request.args.get('from_date')
        articles = get_recent_articles()

        return jsonify(articles)