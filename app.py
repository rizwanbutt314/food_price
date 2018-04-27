from flask import Flask, request, render_template
from flask_restful import Resource, Api
import sqlite3

from views.view_businesslist import BusinessList


app = Flask(__name__)
api = Api(app)

# Routes
api.add_resource(BusinessList, '/businesses', endpoint="businesses")

@app.route('/')
def result():
   conn = sqlite3.connect("database/businesses.db")
   cur = conn.cursor()
   final_query = """
         SELECT DISTINCT(cuisines) FROM business;
   """
   cur.execute(final_query)
   rows = cur.fetchall()
   all_cuisines = []
   for row in rows:
      all_cuisines.append(str(row[0]).replace(' ', ''))
   all_cuisines = ",".join(all_cuisines)

   all_cuisines = all_cuisines.split(',')
   all_cuisines = list(set(all_cuisines))

   return render_template('index.html', search_type = all_cuisines)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True, threaded=True)
