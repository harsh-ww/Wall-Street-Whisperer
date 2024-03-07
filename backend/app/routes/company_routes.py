from flask import Blueprint, request, jsonify
from services.AlphaVantageService import getCompanyDetails, companySearch, getCompanyDetailsNonUS, getCurrentStockPrice, getTimeSeries
from connect import get_db_connection

company_routes_blueprint = Blueprint('company_routes', __name__)

def get_company_details_db(ticker:str):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT CompanyName, CurrentScore FROM company WHERE TickerCode = %s", [ticker])
        result = cur.fetchone()

    conn.close()

    if result is not None:
        return {
            'tracked': True,
            'score': result[1],
            'name': result[0],
        }
    else:
        return {}
# API endpoint to return company details
# Companies are made unique by a ticker and exchange. New company searching has unique tickers
@company_routes_blueprint.route('/company/<ticker>', methods = ['GET'])
def company_details(ticker: str):
    # Get current stock price
    stockInfo = getCurrentStockPrice(ticker)
    
    if not stockInfo:
        return jsonify({'error': 'Ticker does not exist'}), 404

    details = {}
    details['stock'] = stockInfo
    tracked = False

    # Get company info from database
    db_details = get_company_details_db(ticker)
    if db_details != {}:
        tracked = True
    details = {**details, **db_details}

    # Fetch company overview from AlphaVantage
    if "." in ticker:
        if not tracked:
            details = {**details, **getCompanyDetailsNonUS(ticker)}
    else:
        # Fetch company details from AlphaVantage
        details = {**details, **getCompanyDetails(ticker)}

        
    return details

## [PROJ-11] Setup endpoint to allow searching for company names
@company_routes_blueprint.route('/company', methods=['GET'])
def search_companies():
    
    search_query = request.args.get('query', '')
    if not search_query:
        return []

    companies = []

    # Get companies from DB
    DBcompanies = search_companies_db(search_query)

    # Get companies from AV search
    otherCompanies = companySearch(search_query)

    # Eliminate duplicates and set tracked=False on non-tracked
    dbtickers = [x['ticker'] for x in DBcompanies]
    companiesToReturn = []
    for c in otherCompanies:
        if c['symbol'] not in dbtickers:
            c['tracked'] = False
            companiesToReturn.append(c)

    companies = DBcompanies + companiesToReturn

    return jsonify(companies)

def search_companies_db(ticker):

    # Create SQL query which uses ILIKE to find companies which match the query
    sql_query = """
        SELECT CompanyName, TickerCode, Exchange
        FROM company
        WHERE CompanyName ILIKE %s OR TickerCode ILIKE %s
    """
    searchTerm = '%'+ ticker + '%'
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
    
    conn.close()
        
    return companies

@company_routes_blueprint.route('/company/<ticker>/timeseries', methods=['GET'])
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
