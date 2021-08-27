from os import name
import re
from src.pipelines.alpha import Alpha
from src.pipelines.dim import Dim
from src.stats import word_list_freq
from models import MODELS
import functools
import json
import time

def apply_task(req):

    data = None
    added_date = None

    if isinstance(req, dict):
        data = json.loads(req['data'])
        added_date = req['added_date']
    else :
        data = json.loads(req)

    text = data['text']
    features = data['features']
    active_models = data['active_models']

    if isinstance(features, list) and len(features) > 0:
        model_to_skips = set(functools.reduce(lambda a, b: a + b, [[source['name'] for source in item['sources']]for item in features]))
    else:
        model_to_skips = set()
        features = []

    for model_class in MODELS:
        if model_class.get_fullname() in active_models and (model_class.force_update == True or model_class.get_fullname() not in model_to_skips):
            print('in')
            model = model_class()
            et = time.process_time()
            model(text, features)
            features.append(
                {'name':'time_to_compute', 
                    'sources': [{
                        'name': model_class.get_fullname(),
                        'type': 'model',
                        'items': [{'label':'ttc', 'value':str(time.process_time()-et)}]
                }]})                        
    word_frequencies = word_list_freq(text)

    return data['id'], {'added_date':added_date, 'features':features, 'word_frequencies':word_frequencies}