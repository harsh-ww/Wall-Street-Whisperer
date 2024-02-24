from flask import Flask
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


## [PROJ-42] Method to generate suggestions from currently tracked companies
# Returns the IDs of companies to suggest
def generateSuggestions():
    
    SUGGEST_COUNT = 10
    suggestions = []
    
    # Get tracked companies and calculate average score
    sql_query = """
        SELECT AVG(CurrentScore) AS avg_score
        FROM company
        WHERE Tracked = True
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(sql_query)
            avg_score_row = cur.fetchone()
            avg_score = avg_score_row[0] if avg_score_row else 0
    finally:
        conn.close()
    
    # Define the initial score range for suggestions
    initial_score_range = 1.0
    
    # Get suggested companies
    score_range = initial_score_range
    while len(suggestions) < SUGGEST_COUNT and score_range <= 10:  # Maximum score range of 10 to avoid indefinite loop
        sql_query = """
            SELECT CompanyID
            FROM company
            WHERE Tracked = False
            AND CurrentScore BETWEEN %s AND %s
            LIMIT %s
        """
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute(sql_query, (avg_score - score_range, avg_score + score_range, SUGGEST_COUNT))
                rows = cur.fetchall()
                suggestions.extend([row[0] for row in rows])
        finally:
            conn.close()
        
        score_range += 2  # Increase the score range for the next iteration
        
    ## Just ensures too many suggestions aren't returned, although, logically this should never happen
    if len(suggestions) > SUGGEST_COUNT:
        suggestions = suggestions[:SUGGEST_COUNT]
    
    return suggestions

## \\ [PROJ-42]