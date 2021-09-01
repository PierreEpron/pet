from flask import Flask

from flask import request
from flask_cors import CORS
from flask import Flask, logging as flog

from models import MODELS

from datetime import datetime
import logging
import requests
import json
import os

import redis
from rq import Queue, Connection
from tasks import apply_task

# CONST From .env
API_URL = os.environ.get("API_URL", "http://172.18.0.1:8000/api")
REDIS_URL = os.environ.get("REDIS_URL", "redis://172.19.0.7:6379/0")
WEB_LOG_PATH = os.environ.get('LOG_PATH', 'logs/web_logs.log')

# Create app and unable CORS 
app = Flask(__name__)
CORS(app)

# Setup logger
handler = logging.FileHandler(WEB_LOG_PATH, encoding='utf-8')
logger = app.logger
logger.setLevel(logging.INFO)
wlogger = logging.getLogger("werkzeug")
handler.setFormatter(flog.default_handler.formatter)
logger.addHandler(handler)
logging.getLogger("werkzeug").addHandler(handler)

@app.route('/apply', methods=['POST'])
def apply():
    ''' Apply models on document and return features and stats '''
    # Apply task and unpack result
    _, result = apply_task(request.data)

    # Return result of apply task
    return app.response_class(
            response= json.dumps(result),
            status=200,
            mimetype='application/json')

def apply_success(job, connection, result, *args, **kwargs):
    ''' Handle succes of apply task when queue in REDIS '''
    # Unpack result
    id, result = result
    # Get token for api authentification
    headers = {"Content-Type":"application/json"}
    res = requests.post(f'{API_URL}/token/', json.dumps({'username':'admin', 'password':'1234'}), headers=headers)
    token = res.json()['access']
    headers['Authorization'] = "Bearer " + token
    # Patch document with result
    res = requests.patch(f'{API_URL}/documents/{id}/', json.dumps(result), headers=headers).json()
    if 'msg' in res:
       logger.info(f'apply_succes patch canceled for document {id} : {res["msg"]}')
    else :
       logger.info(f'apply_succes patch succeed for document {id}')

@app.route('/queue-apply', methods=['POST'])
def queue_apply():
    ''' Enqueue apply task on REDIS'''
    # Connect to REDIS
    with Connection(redis.from_url(REDIS_URL)):
        # Get Queue and enqueue new task
        q = Queue()
        task = q.enqueue(
            apply_task, {'added_date': datetime.now().timestamp(), 
            'data':request.data}, job_timeout='15m', on_success=apply_success)
    # Return task id
    return app.response_class(
            response= json.dumps({
                "status": "success",
                "data": {
                    "task_id": task.get_id()
                }
            }),
            status=200,
            mimetype='application/json')

@app.route('/queue-count', methods=['GET'])
def queue_count():
    ''' Retrieve queue count of redis'''
    # Connect to REDIS
    with Connection(redis.from_url(REDIS_URL)):
        # Get queue count
        c = Queue().count
    # Return queue count
    return app.response_class(
        response=json.dumps({'count':c}), 
        status=200, mimetype='application/json')

@app.route('/models-info', methods=['GET'])
def models_info():
    ''' Retrieve informations about models'''
    # Gather models infos
    infos = json.dumps([{"name": model.get_fullname(), "desc": model.desc} for model in MODELS])
    # Return models infos
    return app.response_class(
            response= infos,
            status=200,
            mimetype='application/json')
            