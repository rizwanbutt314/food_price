from flask_restful import Resource, reqparse
from flask import jsonify, make_response
import copy
import sqlite3
import re

from common.utils import execute_db_query, parse_request_arguments
from common.constants import BUSINESS_PARAMS


class BusinessList(Resource):
    def get(self):
        request_data = parse_request_arguments(BUSINESS_PARAMS)
        search_params = copy.copy(request_data)
        del search_params['offset']
        del search_params['limit']

        conn = sqlite3.connect("database/businesses.db")
        cur = conn.cursor()
        cur1 = conn.cursor()

        if None in search_params.values() and search_params['load_source'] == "click":
            return make_response(jsonify({
                "error": "Please Fill all filters",
            }), 500)

        if search_params['postcode']:
            postcode_query = """
                SELECT COUNT(*) FROM business WHERE postcode='{0}'
            """.format(request_data['postcode'].upper())
            cur1.execute(postcode_query)
            count = cur1.fetchone()

            if count[0] < 1:
                return make_response(jsonify({
                    "error": "Postcode Invalid",
                }), 500)

        
        init_query = """
                SELECT * FROM business
        """

        where_clause = ""
        # if request_data['type'] == 'category':
        #     if request_data['search']:
        #         where_clause = "WHERE p_category LIKE '%{0}%'".format(request_data['search'])
        #
        # else:
        if request_data['search']:
            search_values = request_data['search'].split(',')
            search_query = []
            for val in search_values:
                search_query.append("p_name LIKE '%{0}%'".format(val))
            search_query = " OR ".join(search_query)
            where_clause = """ WHERE ({0})
                            AND (postcode='{1}') AND (cuisines LIKE '%{2}%')
            """.format(search_query, request_data['postcode'].upper(), request_data['type'])
            
        if where_clause:
            init_query += where_clause

        order_by_query = "ORDER BY rating, p_price"
        limit = request_data['limit'] if request_data['limit'] else 10
        final_query = init_query + order_by_query +  " LIMIT {0}".format(limit)

        cur.execute(final_query)
        rows = cur.fetchall()
        
        all_data = []
        for row in rows:
            all_data.append({
                    'url': row[0],
                    'business_name': row[1],
                    'rating': row[2],
                    'cuisines': row[3],
                    'address': re.sub('[ \t\n]+', ' ', row[4]),
                    'dish_name': row[5],
                    'dish_sub_name': row[6] if row[6] else '---',
                    'dish_category': row[7],
                    'dish_description': row[8],
                    'dish_price': row[9].encode('ascii',errors='ignore'),
                })
            
        return make_response(jsonify({
            "data": all_data,
        }), 200)
