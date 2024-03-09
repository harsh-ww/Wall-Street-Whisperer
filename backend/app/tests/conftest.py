import pytest
import os

os.environ["EMAIL_PASSWORD"] = ""
from connect import get_db_connection
from testcontainers.postgres import PostgresContainer

postgres = PostgresContainer("postgres:latest")


@pytest.fixture(scope="session", autouse=True)
def setup(request):
    postgres.start()

    def teardown():
        postgres.stop()

    request.addfinalizer(teardown)

    os.environ["POSTGRES_HOST"] = postgres.get_container_host_ip()
    os.environ["POSTGRES_DB"] = postgres.POSTGRES_DB
    os.environ["POSTGRES_USR"] = postgres.POSTGRES_USER
    os.environ["POSTGRES_PWD"] = postgres.POSTGRES_PASSWORD
    os.environ["POSTGRES_PORT"] = postgres.get_exposed_port(5432)
    setupSchema()


def setupSchema():
    # Loads the database schema in to allow for testing
    with open("../scripts/postgres/schema.sql", "r") as file:
        sql_script = file.read()

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(sql_script)
        conn.commit()
    conn.close()


@pytest.fixture(scope="function", autouse=False)
def clear_data():
    # Clears data in between each test
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "TRUNCATE TABLE user_follows_company, company_articles, company_social_posts, article, social_post, web_source, stock_price, company, users CASCADE;"
        )
        conn.commit()
    conn.close()
