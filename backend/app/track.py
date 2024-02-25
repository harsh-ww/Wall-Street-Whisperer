from flask import Flask, request, jsonify
from connection import get_db_connection
from app import app

# API endpoint to track a company
@app.route('/track', methods=['POST'])
def track_company():
    data = request.get_json()

    ticker_code = data.get('ticker_code')

    if not ticker_code:
        return jsonify({'error': 'Ticker code is required'}), 400

    try:
        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the company already exists
        cur.execute("SELECT * FROM company WHERE TickerCode = %s", (ticker_code,))
        existing_company = cur.fetchone()

        if existing_company:
            return jsonify({'error': 'Company already tracked'}), 400

        # Create a new company
        cur.execute("INSERT INTO company (CompanyName, TickerCode) VALUES (%s, %s) RETURNING CompanyID",
                    (ticker_code, ticker_code))
        new_company_id = cur.fetchone()[0]

        # Save the company to the tracked companies table
        cur.execute("INSERT INTO tracked_company (company_id) VALUES (%s)", (new_company_id,))

        # Commit changes
        conn.commit()
        return jsonify({'message': 'Company successfully tracked'}), 201

    except psycopg2.DatabaseError as error:
        logging.exception("Failed to track company")
        return jsonify({'error': 'Failed to track company'}), 500

    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
