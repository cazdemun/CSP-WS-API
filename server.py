# import daemon.daemon
from flask import Flask, request, jsonify

from monads.utils import propT, destructure, eitherToTask, zipList
from monads.task import Task
from monads.either import Right
from monads.list import List

import db

# from db import save_task
app = Flask(__name__)
PREFIX = "/api/v2" # https://stackoverflow.com/questions/18967441/add-a-prefix-to-all-flask-routes


@app.route('/')
def hello_world():
    return 'Hello, World!'


# GET api/v2/daemon/state
@app.route(PREFIX + '/daemon/state')
def get_state():
    return jsonify(username='cazdemun'), 200


# POST api/v2/users/:userid/tasks 
@app.route(PREFIX + '/users/<string:username>/tasks', methods=['GET', 'POST'])
def tasks(username : str) -> Task:
    if request.method == 'POST':
        print(request.json)
        return zipList(List('usuarios', 'protocolos', 'movimientos'), # collections
                List('username', 'protocol', 'movement').fmap(propT(request.json))) \
            .fmap(lambda c_n: c_n[1].bind(db.get_id(c_n[0]))) \
            .traverse(Task.of, eitherToTask) \
            .bind(lambda args: db.save_task(*args)) \
            .bind(eitherToTask) \
            .fork(lambda e: (jsonify(error=e), 400), 
                lambda c: (jsonify(msg=c), 201))
    else:
        return jsonify(tasks=[]), 200