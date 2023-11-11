from flask import Flask, jsonify, request
import os
from flask_cors import CORS, cross_origin
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle 
import joblib

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


rf_model = joblib.load('./finalized_model-4.pickle')



@app.route('/', methods=["POST", "GET"])
@cross_origin()
def index():
    print(22, rf_model)
    input_df = create_df(request.json)[['afe0_m0_0', 'afe0_m0_1', 'afe0_m0_2', 'afe0_m0_3', 'afe0_m0_4', 'afe0_m0_5']]
    print('input_df', input_df)
    result = rf_model.predict(input_df)

    print(result)
    return jsonify(result.tolist())




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

  print(pd.DataFrame(flattened_data))
  return pd.DataFrame(flattened_data)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
