import json

# Test if emails can be sent
def test_sendemail(client):

    data = {'recipients':["stockapp220@gmail.com"]}

    # Make a post request to send email
    # Email sending is disabled when app.config['TESTING] = True
    response = client.post('http://localhost:5000/senddailyemail',
                            content_type='application/json',
                            data = json.dumps(dict(data)))

    # Test if the post request was successful
    assert response.status_code == 201
