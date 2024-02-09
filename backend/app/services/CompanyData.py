# Example AV data fetching
# maybe should be replaced with existing library which wraps around https://github.com/RomelTorres/alpha_vantage

import requests
import os
import werkzeug.exceptions as exceptions

API_URL = "https://www.alphavantage.co"
API_KEY = os.environ["ALPHA_KEY"]

class APIError(exceptions.InternalServerError):
    description = 'There was a problem fetching data from an external service'

class CompanyDetails:
    def __init__(self, name) -> None:
        self.name = name



def getCompanyDetails(symbol: str) -> CompanyDetails:
    endpoint = f'{API_URL}/query'
    payload = {'function': 'OVERVIEW', 'symbol': symbol, 'apikey': API_KEY}

    response = requests.get(endpoint, params=payload)

    if response.status_code != 200: 
        raise APIError()
    
    data = response.json()

    return CompanyDetails(data['Name'])