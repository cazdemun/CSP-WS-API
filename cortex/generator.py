import os
import asyncio
import sys
sys.path.append(os.path.join(os.getcwd(), 'cortex'))

from emotiv import Mock
import fif
import datetime;

emotiv = Mock('./cortex/cortex_creds')  

USERID = sys.argv[1]
STATE = sys.argv[2]
TS = datetime.datetime.now().timestamp()

user = {
  'userid': USERID,
  'state': STATE,
  'timestamp': int(TS)
}

async def save_trial(user):
  record = await emotiv.get_data(8)
  success = fif.save_trial(record, user)
  shape = ' x '.join(tuple(str(x) for x in record.shape))
  print(f"{{ 'message': 'Shape of record {shape}' }}")

asyncio.run(save_trial(user))