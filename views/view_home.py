from flask_restful import Resource
from flask import jsonify, make_response


class AppDetail(Resource):
    def get(self):
        
        return make_response(jsonify({
            "app_name": "Analytics API",
            "app_verison": "1.0",
            "endpoints": {
                            "/zipcode": {
                                            "GET_PARAMS": [
                                                            "limit",
                                                            "offset",
                                                            "group",
                                                            "county",
                                                            "state",
                                                            "msa",
                                                          ]
                                        },
                        }
        }), 200)
