from flask import request, jsonify, Blueprint
import psycopg2
import logging
from connect import get_db_connection
from services.AlphaVantageService import getCompanyDetailsNonUS, getCompanyDetails

untrack_blueprint = Blueprint('untrack', __name__)

# API endpoint to untrack a company
@untrack_blueprint.route('/untrack', methods=['POST'])
def untrack_company():
    data = request.get_json()

    user_id = data.get('user_id')
    company_id = data.get('company_id')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    if not company_id:
        return jsonify({'error': 'Company ID is required'}), 400
    
    conn = get_db_connection()

    with conn.cursor() as cur:
        # Remove the entry from the user_follows_company table
        cur.execute("DELETE FROM user_follows_company WHERE UserID = %s AND CompanyID = %s", (user_id, company_id))
        conn.commit()
        
    conn.close()
    return jsonify({'message': 'Company successfully untracked'}), 200
