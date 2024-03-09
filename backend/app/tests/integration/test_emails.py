import json
import emails as emails
import datetime

def test_daily_email_follow(client, test_db, test_app_context):
    """
    Test if the company appears in the daily email if it is followed
    """
    # User tracks AMZN company
    common_name = "Amazon"
    ticker_code = "AMZN"

    data = {"common_name": common_name, "ticker_code": ticker_code}

    # Make a post request to track company
    response = client.post(
        "http://localhost:5000/track",
        content_type="application/json",
        data=json.dumps(dict(data)),
    )

    # Check if tracking was successful
    assert response.status_code == 201

    # Check if the correct company name is in the email
    content = emails.daily_email_content()
    assert "Amazon.com" in content

    # Check if the correct date is displayed
    current_date = datetime.datetime.now().date()
    assert str(current_date) in content

    # Check if the email shows no news articles
    assert "There are no news articles for this company today." in content


def test_daily_email_unfollow(client, test_db, test_app_context):
    """
    Test if the company no longer appears in daily emails after 
    the user unfollows a company
    """
    assert True



# import json

# # Test if emails can be sent
# def test_sendemail(client):

#     data = {'recipients':["stockapp220@gmail.com"]}

#     # Make a post request to send email
#     # Email sending is disabled when app.config['TESTING] = True
#     response = client.post('http://localhost:5000/senddailyemail',
#                             content_type='application/json',
#                             data = json.dumps(dict(data)))

#     # Test if the post request was successful
#     assert response.status_code == 201
