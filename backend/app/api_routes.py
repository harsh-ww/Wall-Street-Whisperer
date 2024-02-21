from flask import Blueprint, request
import requests

api_routes_blueprint = Blueprint('api_routes', __name__)
api_key = 'RH7EG7YN7BPG9V7Z'

# Use the API to get information of ALL companies in JSON format.
@api_routes_blueprint.route('/company', methods = ['GET'])
def company():
    symbol = request.args.get('symbol')  # Query string ?symbol={}
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}'
    r = requests.get(url)
    data = r.json()

    return data
