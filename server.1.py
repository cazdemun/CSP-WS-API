from quart import Quart, websocket, request, jsonify
# from flask import Flask, request, jsonify
# from flask_socketio import SocketIO, emit

from monads.utils import propT, eitherToTask, zipList
from monads.task import Task
from monads.list import List

# import asyncio
# import websockets

import db

app = Quart(__name__)
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'mysecret'
# socketio = SocketIO(app,cors_allowed_origins=['localhost'])
PREFIX = "/api/v2" # https://stackoverflow.com/questions/18967441/add-a-prefix-to-all-flask-routes

@app.route('/')
async def index():
    return 'hello world'

# GET api/v2/daemon/state
@app.route(PREFIX + '/daemon/state')
async def get_state():
    """
    f :: () -> Either(Dict Err, Dict Msg)
    """
    return jsonify(username='cazdemun'), 200


# POST api/v2/users/:userid/tasks 
@app.route(PREFIX + '/users/<string:username>/tasks', methods=['GET', 'POST'])
async def tasks(username : str):
    """
    f :: Request -> Either(Dict Err, Dict Msg)
    """
    if request.method == 'POST':
        json = await request.get_json()
        print(json)
        return zipList(List('usuarios', 'protocolos', 'movimientos'), # collections
                List('username', 'protocol', 'movement').fmap(propT(json))) \
            .fmap(lambda c_n: c_n[1].bind(db.get_id(c_n[0]))) \
            .traverse(Task.of, eitherToTask) \
            .bind(lambda args: db.save_task(*args)) \
            .bind(eitherToTask) \
            .fork(lambda e: (jsonify(error=e), 400), 
                lambda c: (jsonify(msg=c), 201))
    else:
        return jsonify(tasks=[]), 200

@app.websocket('/ws')
async def ws():
    websocket.headers
    while True:
        try:
            data = await websocket.receive()
            await websocket.send(f"Echo {data}")
        except asyncio.CancelledError:
            # Handle disconnect
            raise

# @socketio.on('message')
# def test_disconnect(msg):
#     print(msg)

# async def handleMessage(message, websocket):
#     print(message)
#     await websocket.send(message)

# async def echo(websocket, path):
#   print(f"Someone connected")
#   await websocket.send("Connected to server")
#   try:
#     async for message in websocket:
#       await handleMessage(message, websocket)
#   except:
#     print("Someone disconnected")

if __name__ == '__main__':
    print("Starting server")
    # asyncio.get_event_loop().run_until_complete(websockets.serve(echo, 'localhost', 8765))
    # asyncio.get_event_loop().run_until_complete(app.run(debug=True))
    # asyncio.get_event_loop().run_forever()
    # socketio.run(app, debug=True, log_output= True)
    app.run()