from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "hello bro"

if __name__ == "__main__":
    app.run()
