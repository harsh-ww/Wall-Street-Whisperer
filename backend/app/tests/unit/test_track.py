import routes.track_routes as track
from unittest import mock

def test_save_tracked(clear_data):
    result = track.save_tracked_company("IBM", "International Business Machines", "IBM", "NYSE", "USD")
    assert type(result) is int

def test_already_tracked(clear_data):
    track.save_tracked_company("IBM", "International Business Machines", "IBM", "NYSE", "USD")

    isTrackedValid = track.check_already_tracked("IBM")
    isTrackedInvalid = track.check_already_tracked("TSCO.L")
    assert isTrackedValid
    assert not isTrackedInvalid

def mockedAVNonUS(*args, **kwargs):
    if args[0]=='TSCO.LON':
        return {
            "symbol": "TSCO.LON",
            "name": "Tesco PLC",
            "exchange": "United Kingdom",
            "currency": "GBX"
        }
    else:
        return {}

def mockedAVUS(*args, **kwargs):
    if args[0]=='IBM':
        return {'Name': 'International Business Machines', 'Exchange': 'NYSE', 'Currency': 'USD', 'Address': '...'}
    else:
        return {}

class TestGetCompanyInfo:
    @mock.patch('services.AlphaVantageService.getCompanyDetailsNonUS', side_effect=mockedAVNonUS)
    @mock.patch('services.AlphaVantageService.getCompanyDetails', side_effect=mockedAVUS)
    def test_invalid(self, mocked_nonus, mocked_us):
        # Invalid ticker Non-US
        result = track.get_company_info('FAKE.LON')
        assert result is None

        # Invalid ticker US
        result = track.get_company_info('FAKE')
        assert result is None

    @mock.patch('services.AlphaVantageService.getCompanyDetailsNonUS', side_effect=mockedAVNonUS)
    @mock.patch('services.AlphaVantageService.getCompanyDetails', side_effect=mockedAVUS)
    def test_valid(self, mocked_nonus, mocked_us):
        # valid ticker Non-US
        result = track.get_company_info('TSCO.LON')
        assert result == {'name': 'Tesco PLC', 'exchange': 'United Kingdom', 'currency': 'GBX'}

        # valid ticker US
        result = track.get_company_info('IBM')
        assert result == {'name': 'International Business Machines', 'exchange': 'NYSE', 'currency': 'USD'}