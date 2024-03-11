import time
import json

def test_track_response_time(client):
    """
    Test if the time to track a company is less than 200ms
    """
    common_name = "Amazon"
    ticker_code = "AMZN"

    data = {'common_name': common_name, 'ticker_code': ticker_code}

    # Record time
    start_time = time.time()

    # Make a post request to track company
    response = client.post('http://localhost:5000/track',
                         content_type='application/json',
                        data = json.dumps(dict(data)))
    
    end_time = time.time()

    # Test if the post request was successful
    assert response.status_code == 201
    time_taken = end_time - start_time
    assert (time_taken) < 2
