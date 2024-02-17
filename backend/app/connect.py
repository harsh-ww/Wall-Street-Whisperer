import psycopg2
import os
import logging

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ['POSTGRES_HOST'],
            database=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USR'],
            password=os.environ['POSTGRES_PWD']
        )
        return conn
    except(psycopg2.DatabaseError) as error:
        logging.exception("Failed to connect to database")
