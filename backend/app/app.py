from flask import Flask
from flask import request, jsonify
from connect import get_db_connection
import pandas as pd
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/example')
def example_database_call():
    try:
        sql_query = "SELECT * FROM company"
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(sql_query)

            rows = cur.fetchone()
            print(rows)
    finally:
        conn.close()
        
    return 'Success'


## [PROJ-11] Setup endpoint to allow searching for company names
@app.route('/company', methods=['GET'])
def search_companies():
    
    search_query = request.args.get('query', '')
    companies = []
    DBcompanies = getFromDB(search_query)
    NASDAQcompanies = getFromNASDAQ(search_query, DBcompanies)
    companies = DBcompanies + NASDAQcompanies

    return jsonify(companies)

def getFromDB(squery):
    try:
        # Create SQL query which uses ILIKE to find companies which match the query
        sql_query = """
            SELECT CompanyName, TickerCode, Exchange
            FROM company
            WHERE CompanyName ILIKE %s OR TickerCode ILIKE %s
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

def getFromNASDAQ(squery, DBcompanies):
    # Read the NASDAQ CSV file into a DataFrame
    nasdaq_df = pd.read_csv('../nasdaq_listed.csv')

    # Filter the DataFrame based on the search query
    filtered_df = nasdaq_df[nasdaq_df['Name'].str.contains(squery, case=False)]

    # Convert the filtered DataFrame to a list of dictionaries
    companies = []
    for index, row in filtered_df.iterrows():
        # don't include comapnies already added by database
        if row['Symbol'] not in [db_company['ticker'] for db_company in DBcompanies]:
            companies.append({
                'name': row['Name'],
                'ticker': row['Symbol'],
                'exchange': 'NASDAQ', # Default to NASDAQ since we're searching in the NASDAQ CSV
                'tracked' : False
                })
        
    return companies
## \\ PROJ-11