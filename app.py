from flask import Flask
from flask import render_template
from flask_sqlalchemy  import *





app = Flask(__name__, static_folder='templates/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:st@localhost/test'
db = SQLAlchemy(app)

class Incident(db.Model):
	incident_id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(100))

	def __init__(self, incident_id, type):
		self.incident_id = incident_id
		self.type = type

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=11000, debug=True, host= '0.0.0.0')
