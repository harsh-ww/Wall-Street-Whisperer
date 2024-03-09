import requests
import json 

# Test if user can track a company and if the data is correctly added to database
def test_track(client, test_db):
    common_name = "Amazon"
    ticker_code = "AMZN"

    data = {'common_name': common_name, 'ticker_code': ticker_code}

    # Make a post request to track company
    response = client.post('http://localhost:5000/track',
                            content_type='application/json',
                            data = json.dumps(dict(data)))

    # Test if the post request was successful
    assert response.status_code == 201

    with test_db.cursor() as cur:
        # Check if the data has exactly one row
        cur.execute('SELECT COUNT(*) FROM company WHERE Tracked=True')
        rows_count = cur.fetchone()
        assert rows_count[0] == 1

        # Check if the company data is present in the database
        cur.execute('SELECT CompanyName, TickerCode FROM company LIMIT 1')
        rows = cur.fetchone()
        assert rows[0] == "Amazon.com Inc"
        assert rows[1] == "AMZN"

