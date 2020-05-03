import asyncio
import websockets
import json
import os

import sys
sys.path.append(os.path.join(os.getcwd(), 'cortex'))

from emotiv import Emotiv, Mock
from classifier import Classifier
import fif

# ws://localhost:8765/
# conda activate
# python daemon/daemon.py

async def info_model(ws):
  info = classifier.info
  print(json.dumps(info))
  await ws.send(f'{json.dumps(info)}')

async def train_model(ws, user):
  info = classifier.train(user['userid'])
  print(json.dumps(info))
  await ws.send(f'{json.dumps(info)}')

async def predict_movement(ws, user):
  record = await emotiv.get_data(0.5)
  movement = classifier.predict(record, user['userid'])
  await ws.send(f'{{ "movement": {movement} }}')

async def save_trial(ws, user):
  record = await emotiv.get_data(8)
  success = fif.save_trial(record, user)
  shape = ' x '.join(tuple(str(x) for x in record.shape))
  await ws.send(f'{{ "message": "Shape of record {shape}" }}')

async def handleMessage(message, websocket):
  message = json.loads(message)
  action = message['action']
  # print(f"Starting action {action}", flush=True)
  if action == "save":
    user = {
      'userid': message['userid'],
      'state': message['state'],
      'timestamp': message['timestamp']
    }
    asyncio.get_event_loop().create_task(save_trial(websocket, user))
    await websocket.send(f'{{ "message": "I\'m saving {user}" }}')
  elif action == "predict":
    user = {
      'userid': message['userid']
    }
    asyncio.get_event_loop().create_task(predict_movement(websocket, user))
    await websocket.send(f'{{ "message": "I\'m predicting" }}')
  elif action == "train":
    user = {
      'userid': message['userid']
    }
    asyncio.get_event_loop().create_task(train_model(websocket, user))
    await websocket.send(f'{{ "message": "I\'m training {user}" }}')
  elif action == "info":
    asyncio.get_event_loop().create_task(info_model(websocket))
    await websocket.send(f'{{ "message": "Sending classifier info" }}')

async def echo(websocket, path):
  print(f"Someone connected", flush=True)
  await websocket.send("Connected to daemon (current user info sent)")
  try:
    async for message in websocket:
      await handleMessage(message, websocket)
  except:
    print("Someone disconnected")

# User logger
print("Loading user data")
classifier = Classifier()
info = classifier.train("charls")
print(json.dumps(info))

emotiv = Mock('./cortex/cortex_creds')  
print("Starting emotiv", flush=True)
if len(sys.argv) < 2:
  print("Mode argument missing, mock connection initiating")
  emotiv = Mock('./cortex/cortex_creds')  
elif sys.argv[1] == "cortex":
  emotiv = Emotiv('./cortex/cortex_creds')  
elif sys.argv[1] == "mock":
  print("Mock connection initiated")
  emotiv = Mock('./cortex/cortex_creds')  
else:
  print("Invalid mode argument")
# Not sure of side effects
asyncio.get_event_loop().run_until_complete(emotiv.open_connection())

print("Starting daemon", flush=True)
asyncio.get_event_loop().run_until_complete(websockets.serve(echo, 'localhost', 8765))
asyncio.get_event_loop().run_forever()