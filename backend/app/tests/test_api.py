# Test if can successfully get company details
def test_company_details(client):

    # Test values
    exchange = 'NASDAQ'
    symbol = 'AMZN'
    invalid = 'ABCDE'

    # Valid symbol
    response = client.get(f'/company/{symbol}')
    # Invalid symbol
    response_invalid = client.get(f'/company/{invalid}')

    data = response.json

    assert response.status_code == 200
    assert data['Name'] == "Amazon.com Inc"
    assert data['Exchange'] == exchange
    assert len(data['Description']) != 0
    assert response_invalid.status_code == 404

# Test if company can be searched
def test_search_companies(client):

    # Test values
    company_name = '3M Company'
    symbol = 'MMM'
    invalid = 'ABCDE'

    # CURRENTLY, I THINK THE COMPANIES GOT FROM DB ARE NOT PROPERLY TESTED.
    # Use code only
    response_code = client.get(f'/company?query={symbol}')
    # Use name only
    response_name = client.get(f'/company?query={company_name}')
    # Not exist
    response_notexist = client.get(f'/company?query={invalid}')

    data_code = response_code.json
    data_name = response_name.json 
    data_notexist = response_notexist.json 

    assert response_code.status_code == 200
    assert response_name.status_code == 200
    assert response_notexist.status_code == 200
    assert any(company['name'] == '3M Company' for company in data_code)
    assert any(company['symbol'] == 'MMM' for company in data_name)
    assert len(data_notexist) == 0

# Test if articles can be retrieved
def test_get_articles(client):
    assert True  # To be implemented when the API service is called

# Test if time series can be retrieved
def test_get_timeSeries(client):

    # Test values
    symbol = 'AMZN'
    invalid = 'ABCDE'

    # Valid symbol
    response = client.get(f'/company/{symbol}/timeseries?granularity=DAILY')
    # Invalid symbol
    response_invalid_s = client.get(f'/company/{invalid}/timeseries?granularity=DAILY')
    # Invalid granularity
    response_invalid_g = client.get(f'/company/{symbol}/timeseries?granularity=TENYEARLY')
    
    data = response.json

    assert response.status_code == 200
    assert len(data) != 0
    assert response_invalid_s.status_code == 404
    assert response_invalid_g.status_code == 404