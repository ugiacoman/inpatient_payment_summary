from flask import Flask
from flask import render_template
from flask_sqlalchemy  import *


app = Flask(__name__, static_folder='templates/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ugiacoma:yourownpassword@db/mapbox_inpatient'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=11000, debug=True, host= '0.0.0.0')
