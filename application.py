from flask import Flask, jsonify
from flask import render_template, send_from_directory
from flask_sqlalchemy  import *
from sqlalchemy import text
import json, pygeoj

app = Flask(__name__, static_folder='templates/static')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["CACHE_TYPE"] = "null"
db = SQLAlchemy(app)

from models import *


def sql_count(query):
	sql = text(query)
	result = db.engine.execute(sql)
	names = []
	for row in result:
		names.append(row[0])
	return jsonify(count=str(names[0]))

def sql_geojson(query):
	sql = text(query)
	result = db.engine.execute(sql)
	geojson_dict = {}
	features = []
	years = []
	dict_result = {}
	for row in result:
		primary_id = float(row['avg_total_payments'])
		lat = float(row['latitude'])
		lng = float(row['longitude'])
		feature = { "type": "Feature", "properties": { "Primary ID": primary_id, "Secondary ID": primary_id }, "geometry": { "type": "Point", "coordinates": [ lng, lat ] } }
		features.append(feature)	
	result.close()
	geojson_dict["type"] = "FeatureCollection"
	geojson_dict["crs"] = { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }
	geojson_dict["features"] = features
	return str(geojson_dict).replace("'", '"')

def sql_json(query):
	sql = text(query)
	result = db.engine.execute(sql)
	procedures = {}
	count = 0
	for row in result:
		procedure = str(row).strip("(u'");
		procedure = procedure.strip("',)");
		procedures[count] = procedure
		count += 1
	result.close()
	return jsonify(procedures)

def sql_min(query):
	data = pygeoj.load('templates/static/data/states.geojson')
	sql = text(query)
	result = db.engine.execute(sql)
	for row in result:
		state = 'US.' + str(row['state'].encode("utf-8"))		
		mincost = float(row['min'])
		for feature in data:
			if feature.properties["code_hasc"] == state:
				feature.properties["name"] = "%.2f" % mincost 
	


	data.save('templates/static/data/states.geojson')

	with open('templates/static/data/states.geojson') as f:
		saved = json.load(f)	
	data_json = json.dumps(saved, ensure_ascii=False)

	return data_json

def sql_single_min(query):
	data = pygeoj.load('templates/static/data/states.geojson')
	sql = text(query)
	result = db.engine.execute(sql)
	min_hospital = ""
	for row in result:
		name = row['name'].encode('UTF-8')		
		state = row['state'].encode("utf-8")		
		mincost= float(row['avg_total_payments'])
		min_hospital =  "%s %s %.2f" % (name.decode("utf-8") , state.decode("utf-8"), mincost)
 


	return min_hospital


@app.route("/test-count")
def test_count():
	query = sql_count("select count(*) from diagnosis where procedure='039 - EXTRACRANIAL PROCEDURES W/O CC/MCC';")
	return query

@app.route("/all-locations")
def test_select():
	query = sql_select("select location.provider_id,name,latitude,longitude from location,provider where location.provider_id = provider.provider_id;")
	return query

@app.route("/filter")
def filter():
    return render_template('filter.html')

@app.route('/mincost/<drc>')
def min_cost(drc):
	drc = drc.replace("_","/")
	drc = drc.replace("&"," ")
	query = sql_min("SELECT b.state, min(a.avg_total_payments) FROM diagnosis a, location b WHERE a.procedure = '{}' and b.provider_id = a.provider_id GROUP BY b.state;".format(drc))
	return query

@app.route('/single_mincost/<drc>')
def single_min_cost(drc):
	drc = drc.replace("_","/")
	drc = drc.replace("&"," ")
	query = sql_single_min("select c.name, a.avg_total_payments, b.state from diagnosis a, location b, provider c where a.procedure = '{}' and avg_total_payments = (select min(avg_total_payments) from diagnosis where diagnosis.procedure = '{}') and b.provider_id = a.provider_id and c.provider_id = a.provider_id;".format(drc, drc))
	return query

@app.route('/heat/<drc>')
def heat(drc):
	drc = drc.replace("_","/")
	drc = drc.replace("&"," ")
	query = sql_geojson("SELECT l.latitude, l.longitude, d.avg_total_payments FROM diagnosis d, location l WHERE d.provider_id = l.provider_id and d.procedure = '{}';".format(drc))
	return query	

@app.route('/procedures')
def procedures():
	query = sql_json("select DISTINCT procedure from diagnosis")
	return query	

@app.route('/min/<drc>')
def min(drc):
	return render_template('min_cost.html')	

@app.route("/heatmap/<drc>")
def heatmap(drc):
    return render_template('heatmap.html')    

@app.route("/")
def index():
    return render_template('index.html')    	

if __name__ == "__main__":
    app.run(port=12000, debug=True, host= '0.0.0.0')
