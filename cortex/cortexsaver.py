from datetime import datetime
import sys 
import asyncio
import numpy as np
from lib.cortex import Cortex
import json
import mne
import matplotlib.pyplot as plt

LICENSE_ID = "82a67d9d-b24b-4c11-a470-2868748a876b"

# put on cortex creds:
# token (generate new one if the other expired)
# appID

# For SOLID principles, we put Cortex as a global variable
# The relative path are execute respecting to root, btw, unless we use the sys path (adn even then)

# mock data
async def get_data():
    arr = np.random.randint(1000, size = 14)
    arr = arr / 100000000 * 4
    return arr

async def init_cortex(cortex):
    await cortex.authorize(license_id=LICENSE_ID,debit=50)
    await cortex.query_headsets()

    if len(cortex.headsets) < 1:
      return 0

    await cortex.create_session(activate=True, headset_id=cortex.headsets[0])
    await cortex.create_record(title="emotiv raw test 1")
    await cortex.subscribe(['eeg'])

async def generate_trial():
    cortex = Cortex('./cortex/cortex_creds')
    await init_cortex(cortex)
    freq = 0.0078125 # sleep every freq sec 1 / 128
    sps = int(1 / freq) # must be 128 samples per second
    seconds = 8 # graz protocol trial duration
    samples = int(seconds * sps)
    # trial = await get_data() # connect with cortex
    trial = await cortex.get_data() # connect with cortex
    trial = json.loads(trial)
    trial = trial['eeg'][2:16]
    trial = np.reshape(trial, (14,-1))  
    
    now = datetime.now()
    timestamp = datetime.timestamp(now)

    print("Start recording...")
    for i in range(0, samples):
        await asyncio.sleep(freq)
        # temp_data = await get_data()
        temp_data = await cortex.get_data()
        temp_data = json.loads(temp_data)
        temp_data = temp_data['eeg'][2:16]
        # print(temp_data)
        trial = np.insert(trial, i + 1, temp_data, axis=1)

    print("8 seconds has passed, saving...")
    print("Channels: ", len(trial))
    print("Shape: ", trial.shape)
    # await cortex.close_session()
    return trial, int(timestamp), cortex


async def save_trial():
  trial, timestamp, cortex = await generate_trial()
  
  channel_names = [ 'AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4' ]
  channel_types = [ 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg' ]
  sfreq = 128  # in Hertz
  montage = 'standard_1005'

  info = mne.create_info(channel_names, sfreq, channel_types, montage)
  info['description'] = 'Emotiv EPOC+ dataset obtainer from Cortex API'

  custom_raw = mne.io.RawArray(trial, info)
  userid = sys.argv[1]
  state = sys.argv[2]
  # mock_mode = sys.argv[3]

  # should add /data to file name
  file_name = sys.argv[1] + "_" + sys.argv[2] + "_" + str(timestamp) + "_raw.fif"

  print(trial)
  print("Output from Python") 
  print("User ID:", sys.argv[1]) 
  print("State:", sys.argv[2]) 
  print("Timestamp:", timestamp)
  print("File:", file_name)

  custom_raw.save(file_name)
  await cortex.close_session()

asyncio.run(save_trial())

# def init():
#   create Cortex object
#   pass as argument to all the other funcitons
#   init
#   generate_trial
#   save file