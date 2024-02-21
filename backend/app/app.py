from flask import Flask
from flask import request, jsonify
from connect import get_db_connection
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/example')
def example_database_call():
    sql_query = "SELECT * FROM company"
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(sql_query)

        rows = cur.fetchone()
        print(rows)
    return 'Success'

@app.route('/company', methods=['GET'])
def search_companies():
    
    search_query = request.args.get('query', '')
    sql_query = """
        SELECT CompanyName, TickerCode, Exchange
        FROM company
        WHERE CompanyName ILIKE %s OR TickerCode ILIKE %s
    """
    
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(sql_query, (search_query, search_query))
        rows = cur.fetchall()
        companies = []
        for row in rows:
            companies.append({
                'name': row[0],
                'ticker': row[1],
                'exchange': row[2]
            })
            
    return jsonify(companies)