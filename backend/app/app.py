from flask import Flask
from connect import get_db_connection
from api_routes import api_routes_blueprint

app = Flask(__name__)
app.register_blueprint(api_routes_blueprint)

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


