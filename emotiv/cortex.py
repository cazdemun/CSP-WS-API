from lib.cortex import Cortex
import numpy as np
import asyncio
import json
import time

LICENSE_ID = "82a67d9d-b24b-4c11-a470-2868748a876b"

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