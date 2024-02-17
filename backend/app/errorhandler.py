from psycopg2 import DatabaseError
from app import app

# https://flask.palletsprojects.com/en/2.3.x/errorhandling/

@app.errorhandler(DatabaseError)
def handle_db_error():
    return 'Database Error', 500
