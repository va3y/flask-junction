from flask import Flask, jsonify, request
import os
from flask_cors import CORS, cross_origin
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle 

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


rf_model = pickle.load(open('./test_model.pickle', 'rb'))



@app.route('/', methods=["POST", "GET"])
@cross_origin()
def index():
    result = rf_model.predict(create_df(request.json))
    return jsonify(result)




import json
import pandas as pd

def flatten_json(nestedjson):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], f"{name}{a}")
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, f"{name}{i}_")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nestedjson)
    return out


def create_df(data):
  flattened_data = [flatten_json(item) for item in data]
  return pd.DataFrame(flattened_data)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
