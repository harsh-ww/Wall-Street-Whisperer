import pytest 
from app import create_app
from connect import get_db_connection

# Create app for the test environment
@pytest.fixture()
def test_app():
    testapp = create_app()
    testapp.config['TESTING'] =  True
    yield testapp

# Create client fixture
@pytest.fixture()
def client(test_app):
    return test_app.test_client()

# Create database fixture
@pytest.fixture()
def test_db():

    conn = get_db_connection()
    
    yield conn

    # Close the db after test function
    conn.close()