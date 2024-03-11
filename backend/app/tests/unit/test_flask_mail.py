"""
Unit test to test the functionality of flask mail
"""
import pytest
from app import create_app
from flask_mail import Mail, Message

# Create app for the test environment
@pytest.fixture()
def test_app():
    testapp = create_app()
    testapp.config['TESTING'] =  True
    yield testapp

# Create the app context
@pytest.fixture()
def test_app_context(test_app):
    with test_app.app_context():
        yield

def test_send_email(test_app, test_app_context):
    """
    Test if flask mail works by creating a test mail
    """
    mail = Mail(test_app)

    # Send mail
    with mail.record_messages() as outbox:
        msg_title = "TestSubject"
        msg = Message(msg_title, recipients = ['stockapp220@gmail.com'])
        
        mail.send(msg)

    # Check if the correct email is sent
    assert len(outbox) == 1
    assert outbox[0].subject == "TestSubject"