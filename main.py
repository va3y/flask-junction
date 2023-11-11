from flask import Flask, jsonify
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route('/')
@cross_origin()
def index():
    return jsonify({"Choo Choo ": "Welcome to cross origin Flask app 🚅"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
