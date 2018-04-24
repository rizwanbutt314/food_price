from constants import *

import psycopg2
from urlparse import urlparse
from flask_restful import reqparse


def make_db_connection():
    try:
        url = urlparse(DATABASE_URI)
        conn = psycopg2.connect(
            dbname=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        cursor = conn.cursor()
        return conn, cursor
    except psycopg2.DatabaseError:
        print("Connection Failed to database")
        return None, None


def execute_db_query(query):
    conn, cursor = make_db_connection()
    cursor.execute(query)
    db_data = cursor.fetchall()
    conn.close()
    return db_data


def map_request_params(params_list):
    parser = reqparse.RequestParser()
    for param in params_list:
        parser.add_argument(param)

    return parser.parse_args()


def parse_request_arguments(view_params):
    parsed_params = map_request_params(view_params)
    return parsed_params
