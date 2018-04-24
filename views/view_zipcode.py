from flask_restful import Resource, reqparse
from flask import jsonify, make_response
import copy
import decimal

from common.utils import execute_db_query, parse_request_arguments
from common.constants import ZIPCODE_PARAMS


class ZipCode(Resource):
    def get(self):
        request_data = parse_request_arguments(ZIPCODE_PARAMS)
        search_params = copy.copy(request_data)
        del search_params['offset']
        del search_params['limit']
        schema_setting = """
                SET search_path TO "location-prioritization";
        """
        init_query = """
                SELECT  {0}
                FROM us_households t_hh 
                FULL JOIN mosaic_group mg 
                    ON t_hh.mosaic_group_id = mg.mosaic_group_id 
                FULL JOIN us_zipcode zc 
                    ON t_hh.zipcode_id::integer = zc.zipcode_id
                FULL JOIN us_county cy
                    ON t_hh.county_id = cy.county_id
                FULL JOIN us_state st
                    ON t_hh.state_id = st.state_id
                FULL JOIN us_cbsa msa
                    ON t_hh.msa_id = msa.cbsa_id
        """

        query_data_columns = """zc.zipcode as zipcode, cy.county_name as county, 
                        st.state_name as state, t_hh.households as households, 
                        mg.mosaic_group_name as group"""

        query_count_columns = """DISTINCT ON (t_hh.us_household_id) t_hh.households as household"""

        where_clause = list()
        if any(search_params.values()):
            if request_data['group']:
                where_clause.append("(mg.mosaic_group_name ILIKE '{0}%')".format(request_data['group']))

            if request_data['state']:
                where_clause.append("(st.state_name ILIKE '{0}%')".format(request_data['state']))

            if request_data['msa']:
                where_clause.append("(msa.cbsa_name ILIKE '{0}%')".format(request_data['msa']))

            if request_data['county']:
                where_clause.append("(cy.county_name ILIKE '{0}%')".format(request_data['county']))

            where_clause = "WHERE"+ " AND ".join(where_clause)

        if where_clause:
            init_query += where_clause

        offfset = request_data['offset'] if request_data['offset'] else 0
        limit = request_data['limit'] if request_data['limit'] else 50
        limit_offset_query = """OFFSET {0} LIMIT {1};""".format(offfset, limit)

        final_data_query = schema_setting + init_query.format(query_data_columns) + limit_offset_query

        query_count_wrapper = schema_setting + """
                SELECT COUNT(*), sum(household), (SELECT sum(households) FROM us_households) as total FROM({0}) rizwan
        """.format(init_query.format(query_count_columns))

        try:
            query_data = execute_db_query(final_data_query)
            query_count = execute_db_query(query_count_wrapper)
        except Exception as error:
            return make_response(jsonify({
                "error": "Error while running SQL query",
                "errorrr": str(error),
                "query": str(query_count_wrapper)
            }), 500)

        result = list()
        for q_data in query_data:
            result.append({
                'zipcode': q_data[0],
                'county': q_data[1],
                'state': q_data[2],
                'households': q_data[3],
                'group': q_data[4],
            })
            
        try:
            households_percent = ((decimal.Decimal(str(query_count[0][1]))/decimal.Decimal(str(query_count[0][2])))*100).quantize(decimal.Decimal("0.01"), decimal.ROUND_HALF_DOWN)
        except:
            households_percent = 0
            
        return make_response(jsonify({
            "data": result,
            "total_count": query_count[0][0],
            "total_households": query_count[0][1] if query_count[0][1] else 0,
            "households_percent": float(households_percent),
        }), 200)
