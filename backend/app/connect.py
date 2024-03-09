"""
This module contains a single function that connects 
to the postgreSQL database server
"""
import os
import logging
import psycopg2

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ["POSTGRES_HOST"],
            database=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USR"],
            password=os.environ["POSTGRES_PWD"],
            port=os.environ["POSTGRES_PORT"],
        )
        return conn
    except psycopg2.DatabaseError as error:
        logging.exception("Failed to connect to database")
