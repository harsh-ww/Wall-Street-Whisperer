from flask import Blueprint, request
from services.AlphaVantageService import getCompanyDetails

api_routes_blueprint = Blueprint('api_routes', __name__)

# API endpoint to return company details
@api_routes_blueprint.route('/company', methods = ['GET'])
def company_details():

    symbol = request.args.get('symbol', '')

    details = getCompanyDetails(symbol)

    return details
