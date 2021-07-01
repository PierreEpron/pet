from flask import Flask
from pipelines.alpha import Alpha
from flask import request
from flask_cors import CORS

import functools
import json
from flask import jsonify

MODELS = [Alpha()]

app = Flask(__name__)
CORS(app)

@app.route('/apply', methods=['POST'])
def apply():
    data = json.loads(request.data)
    text = data['text']
    features = data['features']

    if isinstance(features, list) and len(features) > 0:
        model_to_skips = set(functools.reduce(lambda a, b: a + b, [item['name'] for item in features]))
    else:
        model_to_skips = set()
        features = []

    print(features)

    for model in MODELS:
        if model.force_update == True or model.get_fullname() not in model_to_skips:
            model(text, features)

    print(features)

    return app.response_class(
            response= json.dumps(features),
            status=200,
            mimetype='application/json')