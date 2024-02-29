from flask import Blueprint, request, jsonify
from services.AlphaVantageService import getCompanyDetails, companySearch
from connect import get_db_connection
import json


api_routes_blueprint = Blueprint('api_routes', __name__)

# API endpoint to return company details
# company is made unique by its ticker and exchange
# Endpoint modified to `/companies/<:exchange:>/<:ticker:>
@api_routes_blueprint.route('/company/<exchange>/<symbol>', methods = ['GET'])
def company_details(exchange, symbol):
    details = getCompanyDetails(symbol)
    exchange = details.get('Exchange')

    conn = get_db_connection()
    with conn.cursor() as cur:
        # Query database to check if company is tracked
        cur.execute("SELECT * FROM company WHERE Exchange = %s AND TickerCode = %s", (exchange, symbol))
        result = cur.fetchone()
        # If company is tracked, add attributes to the data (eg score)
        if result is not None:
            details['CurrentScore'] = result['CurrentScore']

    conn.close()
        
    return details

## [PROJ-11] Setup endpoint to allow searching for company names
@api_routes_blueprint.route('/company', methods=['GET'])
def search_companies():
    
    search_query = request.args.get('query', '')
    companies = []
    DBcompanies = getFromDB(search_query)
    #NASDAQcompanies = getFromNASDAQ(search_query, DBcompanies)
    otherCompanies = companySearch(search_query)
    dbtickers = [x['ticker'] for x in DBcompanies]
    companiesToReturn = []
    for c in otherCompanies:
        if c['ticker'] not in dbtickers:
            c['tracked'] = False
            companiesToReturn.append(c)

    companies = DBcompanies + companiesToReturn

    return jsonify(companies)

def getFromDB(squery):
    try:
        # Create SQL query which uses ILIKE to find companies which match the query
        sql_query = """
            SELECT CompanyName, TickerCode, Exchange
            FROM company
            WHERE CompanyName ILIKE %%%s%% OR TickerCode ILIKE %%%s%%
        """
        
        # Connect to DB and execute query
        # Create json data for valid companies from DB
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(sql_query, (squery, squery))
            rows = cur.fetchall()
            companies = []
            for row in rows:
                companies.append({
                    'name': row[0],
                    'ticker': row[1],
                    'exchange': row[2],
                    'tracked': True # Only tracked companies will exist in the database
                    })
    finally:
        conn.close()
        
    return companies

@api_routes_blueprint.route('/articles/<id>', methods=['GET'])
def get_articles(id):
        from_date = request.args.get('from_date')
        
        query = """
            SELECT a.* 
            FROM article a
            JOIN company_articles ca ON a.ArticleID = ca.ArticleID
            WHERE ca.CompanyID = %s AND a.PublishedDate >= %s
        """

        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, (id, from_date))
            articles = cur.fetchall()

        conn.close()

        return json.dumps(articles)