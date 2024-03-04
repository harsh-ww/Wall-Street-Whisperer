import os
os.environ['AV_KEY'] = ''

import services.AlphaVantageService as av
from services.exceptions import APIError
import pytest
import requests
from unittest import mock



def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    # Mock responses
    if kwargs['params']['function'] == 'SYMBOL_SEARCH' and kwargs['params']['keywords']== 'Tesco':
        return MockResponse({"bestMatches":[{"1. symbol":"TSCO.LON","2. name":"Tesco PLC","3. type":"Equity","4. region":"United Kingdom","5. marketOpen":"08:00","6. marketClose":"16:30","7. timezone":"UTC+01","8. currency":"GBX","9. matchScore":"0.7273"},{"1. symbol":"TSCDF","2. name":"Tesco plc","3. type":"Equity","4. region":"United States","5. marketOpen":"09:30","6. marketClose":"16:00","7. timezone":"UTC-04","8. currency":"USD","9. matchScore":"0.7143"},{"1. symbol":"TSCDY","2. name":"Tesco plc","3. type":"Equity","4. region":"United States","5. marketOpen":"09:30","6. marketClose":"16:00","7. timezone":"UTC-04","8. currency":"USD","9. matchScore":"0.7143"},{"1. symbol":"TCO2.FRK","2. name":"TESCO PLC ADR/1 LS-05","3. type":"Equity","4. region":"Frankfurt","5. marketOpen":"08:00","6. marketClose":"20:00","7. timezone":"UTC+02","8. currency":"EUR","9. matchScore":"0.5455"},{"1. symbol":"TCO0.FRK","2. name":"TESCO PLC LS-0633333","3. type":"Equity","4. region":"Frankfurt","5. marketOpen":"08:00","6. marketClose":"20:00","7. timezone":"UTC+02","8. currency":"EUR","9. matchScore":"0.5455"}]}, 200)
    elif kwargs['params']['function'] == 'SYMBOL_SEARCH' and kwargs['params']['keywords']== 'BA':
        return MockResponse({"bestMatches":[{"1. symbol":"BA","2. name":"Boeing Company","3. type":"Equity","4. region":"United States","5. marketOpen":"09:30","6. marketClose":"16:00","7. timezone":"UTC-04","8. currency":"USD","9. matchScore":"1.0000"},{"1. symbol":"BAB","2. name":"INVESCO TAXABLE MUNICIPAL BOND ETF ","3. type":"ETF","4. region":"United States","5. marketOpen":"09:30","6. marketClose":"16:00","7. timezone":"UTC-04","8. currency":"USD","9. matchScore":"0.8000"},{"1. symbol":"BA.LON","2. name":"BAE Systems plc","3. type":"Equity","4. region":"United Kingdom","5. marketOpen":"08:00","6. marketClose":"16:30","7. timezone":"UTC+01","8. currency":"GBX","9. matchScore":"0.6667"},{"1. symbol":"BABA","2. name":"Alibaba Group Holding Ltd","3. type":"Equity","4. region":"United States","5. marketOpen":"09:30","6. marketClose":"16:00","7. timezone":"UTC-04","8. currency":"USD","9. matchScore":"0.6667"},{"1. symbol":"BA3.FRK","2. name":"Brooks Automation Inc","3. type":"Equity","4. region":"Frankfurt","5. marketOpen":"08:00","6. marketClose":"20:00","7. timezone":"UTC+02","8. currency":"EUR","9. matchScore":"0.5714"},{"1. symbol":"BAAPX","2. name":"BlackRock Aggressive GwthPrprdPtfInvstrA","3. type":"Mutual Fund","4. region":"United States","5. marketOpen":"09:30","6. marketClose":"16:00","7. timezone":"UTC-04","8. currency":"USD","9. matchScore":"0.5714"},{"1. symbol":"BAAAAX","2. name":"Building America Strategy Port CDA USD Ser 21/1Q MNT CASH","3. type":"Mutual Fund","4. region":"United States","5. marketOpen":"09:30","6. marketClose":"16:00","7. timezone":"UTC-04","8. currency":"USD","9. matchScore":"0.5000"},{"1. symbol":"BAAAFX","2. name":"Building America Strgy Portf CDA USD Ser 2022/2Q MNT CASH","3. type":"Mutual Fund","4. region":"United States","5. marketOpen":"09:30","6. marketClose":"16:00","7. timezone":"UTC-04","8. currency":"USD","9. matchScore":"0.5000"},{"1. symbol":"BAB3.LON","2. name":"Leverage Shares 3x Alibaba ETP Securities","3. type":"ETF","4. region":"United Kingdom","5. marketOpen":"08:00","6. marketClose":"16:30","7. timezone":"UTC+01","8. currency":"USD","9. matchScore":"0.5000"},{"1. symbol":"BAAX39.SAO","2. name":"Ishares Msci All Country Asia Ex Japan ETF","3. type":"ETF","4. region":"Brazil/Sao Paolo","5. marketOpen":"10:00","6. marketClose":"17:30","7. timezone":"UTC-03","8. currency":"BRL","9. matchScore":"0.3636"}]}, 200)
    elif kwargs['params']['function'] == 'TIME_SERIES_DAILY':
        return MockResponse({"Meta Data":{"1. Information":"Daily Prices (open, high, low, close) and Volumes","2. Symbol":"IBM","3. Last Refreshed":"2024-03-01","4. Output Size":"Compact","5. Time Zone":"US/Eastern"},"Time Series (Daily)":{"2024-03-01":{"1. open":"185.4900","2. high":"188.3800","3. low":"185.1800","4. close":"188.2000","5. volume":"4018354"},"2024-02-29":{"1. open":"186.1500","2. high":"186.8495","3. low":"184.6900","4. close":"185.0300","5. volume":"6458487"},"2024-02-28":{"1. open":"184.6300","2. high":"185.3700","3. low":"183.5500","4. close":"185.3000","5. volume":"3216345"}}}, 200)
    elif kwargs['params']['function'] == 'TIME_SERIES_WEEKLY':
        return MockResponse({"Meta Data":{"1. Information":"Weekly Prices (open, high, low, close) and Volumes","2. Symbol":"IBM","3. Last Refreshed":"2024-03-01","4. Time Zone":"US/Eastern"},"Weekly Time Series":{"2024-03-01":{"1. open":"185.6000","2. high":"188.3800","3. low":"182.6200","4. close":"188.2000","5. volume":"21955379"},"2024-02-23":{"1. open":"187.6400","2. high":"188.7700","3. low":"178.7500","4. close":"185.7200","5. volume":"17487852"},"2024-02-16":{"1. open":"185.9000","2. high":"188.9500","3. low":"182.2600","4. close":"187.6400","5. volume":"21745006"}}}, 200)
    elif kwargs['params']['function'] == 'TIME_SERIES_MONTHLY':
        return MockResponse({"Meta Data":{"1. Information":"Monthly Prices (open, high, low, close) and Volumes","2. Symbol":"IBM","3. Last Refreshed":"2024-03-01","4. Time Zone":"US/Eastern"},"Monthly Time Series":{"2024-03-01":{"1. open":"185.4900","2. high":"188.3800","3. low":"185.1800","4. close":"188.2000","5. volume":"4018354"},"2024-02-29":{"1. open":"183.6300","2. high":"188.9500","3. low":"178.7500","4. close":"185.0300","5. volume":"88679550"},"2024-01-31":{"1. open":"162.8300","2. high":"196.9000","3. low":"157.8850","4. close":"183.6600","5. volume":"128121557"}}}, 200)
    elif kwargs['params']['function'] == 'GLOBAL_QUOTE' and kwargs['params']['symbol']=='IBM':
        return MockResponse({"Global Quote":{"01. symbol":"IBM","02. open":"185.4900","03. high":"188.3800","04. low":"185.1800","05. price":"188.2000","06. volume":"4018354","07. latest trading day":"2024-03-01","08. previous close":"185.0300","09. change":"3.1700","10. change percent":"1.7132%"}}, 200)
    return MockResponse(None, 404)

class TestCompanySearch:
    """Test companySearch function"""

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_structure(self, mocked_get):
        """Test the structure of the data returned is as expected"""
        # Test structure of data returned
        results = av.companySearch("Tesco")

        assert len(results)==5

        for r in results:
            assert 'symbol' in r
            assert 'name' in r
            assert 'exchange' in r

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_filtering(self, mocked_get):
        """Test that non-equity funds are removed from results"""
        # Testing Equity Filtering
        results = av.companySearch("BA")
        assert len(results)==4
        expectedSymbols = ['BA', 'BA.LON', 'BABA', 'BA3.FRK']
        actualSymbols = [r['symbol'] for r in results]
        for symbol in expectedSymbols:
            assert symbol in actualSymbols

class TestGetTimeSeries:
    """Test getTimeSeries function"""

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_invalidGranularity(self, mocked_get):
        """Test empty with invalid granularity"""
        # Invalid granularity
        result = av.getTimeSeries('TSCO.L', 'YEARLY')
        assert not bool(result)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_granularity(self, mocked_get):
        """Test all valid granularities successfully return data"""
        # This tests that the granularity conversion is working correctly

        # Daily
        result = av.getTimeSeries('IBM', 'DAILY')
        assert len(result)==3
        assert '2024-03-01' in result

        # Weekly
        result = av.getTimeSeries('IBM', 'WEEKLY')
        assert len(result)==3
        assert '2024-02-16' in result

        # Monthly
        result = av.getTimeSeries('IBM', 'MONTHLY')
        assert len(result)==3
        assert '2024-01-31' in result

class TestGetCurrentStockPrice:
    """Test the getCurrentStockPrice function"""

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def testInvalidSymbol(self, mocked_get):
        with pytest.raises(APIError):
            av.getCurrentStockPrice("MADEUPSYMBOL12")

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def testValidSymbol(self, mocked_get):
        # Test the data cleaning
        result = av.getCurrentStockPrice("IBM")
        assert result['price']=='188.2000'

class TestGetCompanyDetailsNonUS:
    """Test the getCompanyDetailsNonUS function"""

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def testStructure(self, mocked_get):
        actual = av.getCompanyDetailsNonUS("BA")
        expected = {
            "symbol": "BA",
            "name": "Boeing Company",
            "exchange": "United States",
            "currency": "USD"
        }
        assert actual == expected
