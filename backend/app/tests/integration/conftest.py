import pytest
import os
os.environ['EMAIL_PASSWORD'] = ''
from app import create_app
from connect import get_db_connection
from testcontainers.postgres import PostgresContainer


postgres = PostgresContainer('postgres:latest')

@pytest.fixture(scope="module", autouse=True)
def setup(request):
    print(os.getcwd())
    postgres.start()

    def teardown():
        postgres.stop()
    
    request.addfinalizer(teardown)

    os.environ['POSTGRES_HOST'] = postgres.get_container_host_ip()
    os.environ['POSTGRES_DB'] = postgres.POSTGRES_DB
    os.environ['POSTGRES_USR'] = postgres.POSTGRES_USER
    os.environ['POSTGRES_PWD'] = postgres.POSTGRES_PASSWORD
    os.environ['POSTGRES_PORT'] = postgres.get_exposed_port(5432)
    setupSchema()

def setupSchema():
    # Loads the database schema in to allow for testing
    with open('../scripts/postgres/schema.sql', 'r') as file:
        sql_script = file.read()

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(sql_script)
        conn.commit()
    conn.close()

@pytest.fixture(scope='function', autouse=True)
def clear_data():
    # Clears data in between each test
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE user_follows_company, company_articles, company_social_posts, article, social_post, web_source, stock_price, company, users CASCADE;")
    conn.close()

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