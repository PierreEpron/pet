from flask import Flask
from src.pipelines.alpha import Alpha
from src.pipelines.dim import Dim
from flask import request
from flask_cors import CORS
from src.stats import word_list_freq

import functools
import json

MODELS = [Alpha(), Dim()]

app = Flask(__name__)
CORS(app)

@app.route('/apply', methods=['POST'])
def apply():
    data = json.loads(request.data)
    text = data['text']
    features = data['features']
    active_models = data['active_models']


    if isinstance(features, list) and len(features) > 0:
        model_to_skips = set(functools.reduce(lambda a, b: a + b, [item['name'] for item in features]))
    else:
        model_to_skips = set()
        features = []

    for model in MODELS:
        if model.name in active_models and (model.force_update == True or model.get_fullname() not in model_to_skips):
            model(text, features)
    
    word_frequencies = word_list_freq(text)
    return app.response_class(
            response= json.dumps({'features':features,'word_frequencies':word_frequencies}),
            status=200,
            mimetype='application/json')

@app.route('/models-info', methods=['GET'])
def models_info():
    return app.response_class(
            response= json.dumps([{"name": model.name, "desc": model.desc} for model in MODELS]),
            status=200,
            mimetype='application/json')
            