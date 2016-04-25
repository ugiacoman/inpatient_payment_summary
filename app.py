from flask import Flask, jsonify
from flask import render_template
from flask_sqlalchemy  import *
from sqlalchemy import text
import json

app = Flask(__name__, static_folder='templates/static')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

def sql_count(query):
	sql = text(query)
	result = db.engine.execute(sql)
	names = []
	for row in result:
		names.append(row[0])
	return jsonify(count=str(names[0]))

def sql_select(query):
	sql = text(query)
	result = db.engine.execute(sql)
	features = []
	years = []
	dict_result = {}
	crs = { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }
	for row in result:
		print(row['provider_id'],row['name'], row['longtiude'],row['latitude'])
		feature = '{ "type": "Feature", "properties": { "Primary ID": "%s", "Secondary ID": "%s" }, "geometry": { "type": "Point", "coordinates": [ %f, %f ] } }' % (row['provider_id'],row['name'], row['longtiude'],row['latitude'])
		features.append(feature)
	print(features)		
	result.close()
	return jsonify(type="FeatureCollection",
                   crs=crs,
                   features=features)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/test-count")
def test_count():
	query = sql_count("select count(*) from diagnosis where procedure='039 - EXTRACRANIAL PROCEDURES W/O CC/MCC';")
	return query

@app.route("/test-select")
def test_select():
	query = sql_select("select location.provider_id,name,latitude,longtiude from location,provider where location.provider_id = provider.provider_id;")
	return query	

if __name__ == "__main__":
    app.run(port=12000, debug=True, host= '0.0.0.0')
