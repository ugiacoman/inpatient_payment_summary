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
	names = []
	years = []
	for row in result:
		names.append(row[0])
		years.append(row[1])
	return jsonify(provider_id=str(names[0]),year=str(row[1]))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/test-count")
def test_count():
	query = sql_count("select count(*) from diagnosis where procedure='039 - EXTRACRANIAL PROCEDURES W/O CC/MCC';")
	return query

@app.route("/test-select")
def test_select():
	query = sql_select("select provider_id,year from diagnosis where procedure='039 - EXTRACRANIAL PROCEDURES W/O CC/MCC';")
	return query	

if __name__ == "__main__":
    app.run(port=12000, debug=True, host= '0.0.0.0')
