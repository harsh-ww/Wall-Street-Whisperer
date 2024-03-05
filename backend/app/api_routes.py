from flask import Blueprint, request, jsonify
from services.AlphaVantageService import getCompanyDetails, companySearch, getCompanyDetailsNonUS, getCurrentStockPrice, getTimeSeries
from connect import get_db_connection
import json


api_routes_blueprint = Blueprint('api_routes', __name__)

# API endpoint to return company details
# Companies are made unique by a ticker and exchange. New company searching has unique tickers
@api_routes_blueprint.route('/company/<symbol>', methods = ['GET'])
def company_details(symbol: str):
    stockInfo = getCurrentStockPrice(symbol)
    if not stockInfo:
        return jsonify({'error': 'Ticker does not exist'}), 404

    details = {}
    details['stock'] = stockInfo
    tracked = False

    # Add in additional data if the company is tracked
    conn = get_db_connection()
    with conn.cursor() as cur:
        # Query database to check if company is tracked
        cur.execute("SELECT CompanyName, CurrentScore FROM company WHERE TickerCode = %s", [symbol])
        result = cur.fetchone()
        # If company is tracked, add attributes to the data (eg score)
        if result is not None:
            details['tracked'] = True
            details['score'] = result[1]
            details['name'] = result[0]
            tracked = True
    
    conn.close()

    # Fetch company overview from AlphaVantage
    if "." in symbol:
        if not tracked:
            details = {**details, **getCompanyDetailsNonUS(symbol)}
    else:
        # Fetch company details from AlphaVantage
        details = {**details, **getCompanyDetails(symbol)}

        
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
    print(dbtickers)
    print(otherCompanies)
    companiesToReturn = []
    for c in otherCompanies:
        if c['symbol'] not in dbtickers:
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
            WHERE CompanyName ILIKE %s OR TickerCode ILIKE %s
        """
        searchTerm = '%'+ squery + '%'
        # Connect to DB and execute query
        # Create json data for valid companies from DB
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(sql_query, (searchTerm, searchTerm))
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

@api_routes_blueprint.route('/articles/<ticker>', methods=['GET'])
def get_articles(ticker:str):
        #from_date = request.args.get('from_date')
        
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

        return jsonify(articles)

@api_routes_blueprint.route('/company/<ticker>/timeseries', methods=['GET'])
def get_timeSeries(ticker):
    granularity = request.args.get('granularity') or 'DAILY'
    data = getTimeSeries(ticker, granularity)

    if not data:
        return jsonify({'message': 'Ticker code does not exist, or invalid granularity provided.'}), 404
    
    newData = changeFormat(data)  # Format the data

    return jsonify(newData)

def changeFormat(data): 
    formatted_data = []
    for date, values in data.items():
        formatted_item = {'date': date}
        formatted_item.update(values)
        formatted_data.append(formatted_item)
    reversed_data = formatted_data[::-1]  # Reverse the list so it is in chronological order
    return reversed_data[-30:]  # return the 30 most recent data points
