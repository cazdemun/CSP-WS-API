# import daemon.daemon
from flask import Flask, request, jsonify

from monads.utils import fromNullable, tryCatch, fromNullableField, eitherToTask
from monads.task import Task
from pymonad import List
from functools import reduce
from toolz import curry

from db import save_task

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

def reducetrace(f, a):
    print(f, a)
    return fn(a).fmap(lambda b, bs: bs + b).amap(f)

List.traverse = lambda self, of, fn: reduce(reducetrace,
    self, of(List()))

# List.traverse = lambda self, of, fn: reduce(lambda f, a: fn(a).fmap(lambda b, bs: bs + b).amap(f),
#     self, of(List()))

# List.traverse = lambda self, of, fn: reduce(lambda f, a: f.fmap(),
#     self, of(List()))

# POST api/v2/users/:userid/tasks 
@app.route(PREFIX + '/users/<string:username>/tasks', methods=['GET', 'POST'])
def tasks(username : str) -> Task:
    if request.method == 'POST':
        print(request.json)

        username : Either[str, str] = fromNullableField(request.json.get('username', None), 'username')
        protocol : Either[str, str] = fromNullableField(request.json.get('protocol', None), 'protocol')
        movement : Either[str, str] = fromNullableField(request.json.get('movement', None), 'movement')

        print(List(username, protocol, movement) + List(username))
        print(List(username, protocol, movement)
                .traverse(Task.of, eitherToTask) \
                .fork(lambda e: print(e), lambda c: print(c)))
        # List(username, protocol, movement) \
        #     .fmap(eitherToTask) \
        #     .traverse(Task.of, lambda x: x) \
        #     .fork(lambda e: print(e),
        #         lambda c: print(c))
        return 'testing'
            # .bind(save_task) \
            # .bind(eitherToTask) \

        # return List(eitherToTask(username) \
        #     .bind(save_task) \
        #     .bind(eitherToTask) \
        #     .fork(lambda e: (jsonify(error=e), 400),
        #         lambda c: (jsonify(msg=c), 201))

    else:
        return jsonify(tasks=[]), 200









        # print(List(username, protocol, movement) + List(username))
        # print(List(username, protocol, movement)
        #         .traverse(Task.of, eitherToTask) \
        #         .fork(lambda e: print(e), lambda c: print(c)))
        # # List(username, protocol, movement) \
        # #     .fmap(eitherToTask) \
        # #     .traverse(Task.of, lambda x: x) \
        # #     .fork(lambda e: print(e),
        # #         lambda c: print(c))
        # return 'testing'
        #     # .bind(save_task) \
        #     # .bind(eitherToTask) \

        # # return List(eitherToTask(username) \
        # #     .bind(save_task) \
        # #     .bind(eitherToTask) \
        # #     .fork(lambda e: (jsonify(error=e), 400),
        # #         lambda c: (jsonify(msg=c), 201))

        
        # # return Task.of(save_task) \
        # #     .bind(lambda x: x) \
        # #     .amap(eitherToTask(username)) \
        # #     .bind(eitherToTask) \
        # #     .fork(lambda e: (jsonify(error=e), 400),
        # #         lambda c: (jsonify(msg=c), 201))