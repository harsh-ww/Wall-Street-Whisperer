import pytest
from app import create_app

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

# Create client fixture
@pytest.fixture()
def client(test_app):
    return test_app.test_client()
