from flask import Flask, request
from flask_restful import Resource, Api

from views.view_home import AppDetail
from views.view_zipcode import ZipCode

app = Flask(__name__)
api = Api(app)

# Routes
api.add_resource(AppDetail, '/', endpoint="home")
api.add_resource(ZipCode, '/zipcode', endpoint="zipcode")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True, threaded=True)