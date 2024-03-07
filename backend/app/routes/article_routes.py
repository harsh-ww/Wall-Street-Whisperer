from flask import Blueprint, jsonify
from connect import get_db_connection


article_routes_blueprint = Blueprint('article_routes', __name__)

def get_articles_by_ticker_db(ticker: str):
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
     

@article_routes_blueprint.route('/articles/<ticker>', methods=['GET'])
def get_articles(ticker:str):
        #from_date = request.args.get('from_date')
        articles = get_articles_by_ticker_db(ticker)

        return jsonify(articles)