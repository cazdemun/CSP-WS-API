from lib.cortex import Cortex
import numpy as np
import asyncio
import json
import time

LICENSE_ID = "82a67d9d-b24b-4c11-a470-2868748a876b"

async def get_data():
	arr = np.random.randint(1000, size = 14)
	arr = arr / (10 ** 8) * 4
	arr = (arr * (10 ** 6)) + 4200
	return arr

# wrapper for ws bug
# WARNING! RECURSIVE FUNCTION AHEAD - Include a safeguard limit
async def _get_data(cortex):
  sample = await cortex.get_data()
  sample = json.loads(sample)
  try: 
    sample = sample['eeg'][2:16]
  except:
    print("Not an eeg sample!")
    sample = await _get_data(cortex)
  return sample

async def record_data(seconds, cortex=None):
  sample_period = 0.0078125
  samples_frequency = 128 # sps
  samples = int(seconds * samples_frequency) # 1024 or 64

  record = np.empty((14,1))

  t0 = time.time()
  for i in range(0,samples + 1):
    if cortex is not None:
      await asyncio.sleep(sample_period)
      sample = await _get_data(cortex)
    else:
      sample = await get_data()

    record = np.insert(record, i + 1, sample, axis=1)
  t1 = time.time()
  print(t1 - t0)
  record = np.delete(record, 0, 1)
  return record

  ############################################################################

class Emotiv():
  def __init__(self, credentials):
    self.cortex = Cortex(credentials)
  
  async def open_connection(self):
    print("Opening real Emotiv Connection")
    await self.cortex.authorize(license_id=LICENSE_ID,debit=50)
    await self.cortex.query_headsets()

    if len(self.cortex.headsets) < 1:
      raise ValueError(f'No headsets found')

    await self.cortex.create_session(activate=True,headset_id=self.cortex.headsets[0])

  async def close_connection(self):
    await self.cortex.close()

  async def get_data(self, s):
    await self.cortex.subscribe(['eeg'])
    record = await record_data(s, self.cortex)
    await self.cortex.unsubscribe(['eeg'])
    return record

class Mock():
  def __init__(self, credentials):
    self.cortex = None

  async def open_connection(self):
    self.cortex = None

  async def close_connection(self):
    self.cortex = None

  async def get_data(self, s):
    record = await record_data(s, self.cortex)
    return record