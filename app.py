from flask import Flask, request, render_template
from flask_restful import Resource, Api

#from views.view_home import AppDetail
from views.view_businesslist import BusinessList

app = Flask(__name__)
api = Api(app)

# Routes
#api.add_resource(AppDetail, '/', endpoint="home")
api.add_resource(BusinessList, '/businesses', endpoint="businesses")

@app.route('/')
def result():
   types = ['category', 'name']
   return render_template('index.html', search_type = types)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True, threaded=True)
