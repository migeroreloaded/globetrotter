from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type"]}})

@app.route("/")
def home():
    return "Hello, Globetrotter!"

if __name__ == "__main__":
    app.run(debug=True)
