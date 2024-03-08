from flask import Blueprint, jsonify
from connect import get_db_connection
from app import app

tracked_companies_blueprint = Blueprint('tracked_companies_routes', __name__)

@tracked_companies_blueprint.route('/tracked_companies', methods=['GET'])
def get_tracked_companies():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.CompanyID, c.CompanyName, c.TickerCode, c.Exchange
                FROM company c
                INNER JOIN user_follows_company ufc ON c.CompanyID = ufc.CompanyID
            """)
            tracked_companies = [{
                'id': row[0],
                'name': row[1],
                'ticker_code': row[2],
                'exchange': row[3]
            } for row in cur.fetchall()]
        return jsonify(tracked_companies)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

