from flask import Flask
from flask import render_template

app = Flask(__name__, static_folder='templates/static')

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
