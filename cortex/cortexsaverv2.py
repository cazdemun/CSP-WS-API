from datetime import datetime
import sys 
import asyncio
import numpy as np
from lib.cortex import Cortex
import json
import mne
import matplotlib.pyplot as plt
import logging
import math

LICENSE_ID = "82a67d9d-b24b-4c11-a470-2868748a876b"

# put on cortex creds:
# token (generate new one if the other expired)
# appID

# For SOLID principles, we put Cortex as a global variable
# The relative path are execute respecting to root, btw, unless we use the sys path (adn even then)

# check

userid = sys.argv[1]
state = sys.argv[2]
mock = sys.argv[3].lower() == 'true'

args = {
	'userid': userid,
	'state': state,
	'mock': mock,
}

# These can be in config globals
channel_names = [ 'AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4' ]
channel_types = [ 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg' ]
sample_frequency = 128  # in Hertz
montage = 'standard_1005'

mnelogger = logging.getLogger('mne')
mnelogger.setLevel(logging.WARNING)

if len(sys.argv) > 1:
    blah = sys.argv[1]
else:
    blah = 'blah'

# mock data
async def get_data():
	arr = np.random.randint(1000, size = 14)
	arr = arr / (10 ** 8) * 4
	# normalization respecto to emotiv
	arr = (arr * (10 ** 6)) + 4200
	return arr

async def get_data_sine(i, samples):
	t = (128 * 2 * math.pi) / samples
	arr = np.full(14, math.sin(t * i) * 1000)
	arr = arr / (10 ** 8) * 4
	# normalization respec to emotiv
	arr = (arr * (10 ** 6)) + 4200
	return arr

async def init_cortex(creds, mock):
    '''
    cortex.authorize token return should be stored and checked
    cortex.queryheadsets should be also stored, since is the same id
    cortex.create_session and cortex.create_record are still under study, they can remain,
    but hopefully we'll only need cortex.subscribe with the right configuration
    '''
    if mock is True:
        return None

    cortex = Cortex('./cortex/cortex_creds')
    await cortex.authorize(license_id=LICENSE_ID,debit=50)
    await cortex.query_headsets()

    if len(cortex.headsets) < 1:
       raise ValueError(f'No headsets found')

    await cortex.create_session(activate=True,headset_id=cortex.headsets[0])
    await cortex.create_record(title="emotiv raw trial")
    await cortex.subscribe(['eeg'])

    return cortex

async def generate_trial(mock):
	timestamp = datetime.timestamp(datetime.now())
	cortex = await init_cortex('./cortex/cortex_creds',mock)
	trial = None

	if mock is False:
		trial = await cortex.get_data() # connect with cortex
		trial = json.loads(trial)
		trial = trial['eeg'][2:16]
	else:
		trial = await get_data() # mock data

	trial = np.reshape(trial, (14,-1))  

	sample_period = 0.0078125
	sps = int(1 / sample_period)
	seconds = 8
	samples = int(seconds * sps)

	print(f"Start recording ({seconds} seconds)... ")

	for i in range(0,samples):
		sample = None
		if mock is False:
			await asyncio.sleep(sample_period)
			sample = await cortex.get_data() # connect with cortex
			sample = json.loads(sample)
			sample = sample['eeg'][2:16]
		else:
			sample = await get_data() # mock data
			sample = await get_data_sine(i, samples) # mock data

		trial = np.insert(trial, i + 1, sample, axis=1)
		
	print("8 seconds has passed, saving..."
			f"Channels: {len(trial)}"
			f"Shape: {trial.shape}")

	if mock is not True:
		await cortex.close_session()
		return trial, int(timestamp), cortex
	return trial, int(timestamp), None


async def save_trial(mock):
    
    trial, timestamp, cortex = await generate_trial(mock)
    print(trial)
    
    info = mne.create_info(channel_names, sample_frequency, channel_types, montage)
    info['description'] = 'Emotiv EPOC+ dataset obtainer from Cortex API'

    custom_raw = mne.io.RawArray(trial, info)
    file_name = "../data/" + args['userid'] + "_" + args['state'] + "_" + str(timestamp) + "_raw.fif"

    print(f"Output from Python:\n" 
          f"\tUser ID: {userid}\n"
          f"\tState: {state}\n"
          f"\tTimestamp: {timestamp}\n"
          f"\tFile: {file_name}\n")

    custom_raw.save(file_name)

    if mock is False:
        await cortex.close_session()

    return 'sucess'

asyncio.run(save_trial(mock=mock))

# def init():
#   create Cortex object
#   pass as argument to all the other funcitons
#   init
#   generate_trial
#   save file