import pytest
import os
# Overwrite env vars
os.environ['EMAIL_PASSWORD'] = ''
os.environ['SIMILARWEB_KEY'] = ''
os.environ['PERIGON_KEY'] = ''
from connect import get_db_connection
from testcontainers.postgres import PostgresContainer

from unittest import mock

# Mock the NewsSentiment library - we don't want to install it in CI (because it's massive) or run it in tests (slow) when we can mock the data
# aim of these tests is to test surrounding business logic
NewsSentiment = mock.MagicMock()
mock.patch.dict("sys.modules", NewsSentiment=NewsSentiment).start()



# define the postgres container
postgres = PostgresContainer('postgres:latest')

# fixture to start and stop the postgres container
@pytest.fixture(scope="session", autouse=True)
def setup(request):

    postgres.start()

    def teardown():
        postgres.stop()
        
    # add a finalizer to stop the container
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

@pytest.fixture(scope='function', autouse=False)
def clear_data():
    # Clears data in between each test
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE article, web_source, company, notifications CASCADE;")
        conn.commit()
    conn.close()
