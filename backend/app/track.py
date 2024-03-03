from flask import Flask, request, jsonify, Blueprint
import psycopg2
import logging
from connect import get_db_connection
from services.AlphaVantageService import getCompanyDetailsNonUS, getCompanyDetails

track_blueprint = Blueprint('track', __name__)

# API endpoint to track a company
@track_blueprint.route('/track', methods=['POST'])
def track_company():
    data = request.get_json()

    user_id = data.get('user_id')
    ticker_code = data.get('ticker_code')
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    if not ticker_code:
        return jsonify({'error': 'Ticker code is required'}), 400
    
    conn = get_db_connection()

    with conn.cursor() as cur:
        cur = conn.cursor()

        # Check if the company exists in the company table
        cur.execute("SELECT CompanyID FROM company WHERE TickerCode = %s", (ticker_code,))
        company_id_result = cur.fetchone()

        if not company_id_result:
            return jsonify({'error': 'Company does not exist'}), 400

        company_id = company_id_result[0]

        # Check if the user is already following the company
        cur.execute("SELECT * FROM user_follows_company WHERE UserID = %s AND CompanyID = %s", (user_id, company_id))
        existing_follow = cur.fetchone()

        if existing_follow:
            return jsonify({'error': 'User already follows this company'}), 400
        
        name = ''
        # get official name
        if "." in ticker_code:
            details = getCompanyDetailsNonUS(ticker_code)
            if not details:
                return jsonify({'error': 'Ticker code does not exist'}), 400
            name = details['name']
        else:
            details = getCompanyDetails(ticker_code)
            if not details:
                return jsonify({'error': 'Ticker code does not exist'}), 400
            name = details['Name']

        # Save the company to the user_follows_company table
        cur.execute("INSERT INTO user_follows_company (UserID, CompanyID) VALUES (%s, %s)", (user_id, company_id))
        
        conn.commit()
        conn.close()
        return jsonify({'message': 'Company successfully tracked'}), 201


