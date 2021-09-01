from os import name
import re
from src.pipelines.alpha import Alpha
from src.pipelines.dim import Dim
from src.stats import word_list_freq, gather_identity
from models import MODELS
import functools
import json
import time

# TODO : Refactorize
def apply_task(req):
    '''
    Apply all models for project of document
    
    Parameters
    ----------
    req : dict, data of apply or queue_apply request

    Returns
    -------
    id : int, id of document processed.
    result : dict, contain added_date, features and stats
    '''

    data = None
    added_date = None

    # if instance is dict
    if isinstance(req, dict):
        # Load data
        data = json.loads(req['data'])
        # Get added_date
        added_date = req['added_date']
    # if instance nt dict (str)
    else :
        # Load data
        data = json.loads(req)

    # Unpack data
    text = data['text']
    features = data['features']
    active_models = data['active_models']

    # Create list of model to skip, already applied models.
    if isinstance(features, list) and len(features) > 0:
        model_to_skips = set(functools.reduce(lambda a, b: a + b, [[source['name'] for source in item['sources']]for item in features]))
    else:
        model_to_skips = set()
        features = []

    # Iter on models class.
    for model_class in MODELS:
        # If models is in project and model need to by apply 
        if (model_class.get_fullname() in active_models and
            (model_class.force_update == True or model_class.get_fullname() not in model_to_skips)):
            # Load model
            model = model_class('models')
            # Get current time
            et = time.process_time()
            # Apply model
            model(text, features)
            # Add time to compute to model
            features.append(
                {'name':'time_to_compute', 
                    'sources': [{
                        'name': model_class.get_fullname(),
                        'type': 'model',
                        'items': [{'label':'ttc', 'value':str(time.process_time()-et)}]
                }]})                        

    # Generate word_frequencies stats
    stats = {'word_frequencies':word_list_freq(text)}
    # Generate identity stats
    identity = gather_identity(text, features)
    # Add identity if not empty
    if len(identity) > 0:
        stats.update({'identity':identity}) 
    
    # Return result
    return data['id'], {'added_date':added_date, 'features':features, 'stats':stats}