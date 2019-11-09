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
USERID = sys.argv[1]
STATE = sys.argv[2]
MOCK = sys.argv[3].lower() == 'true'

channel_names = [ 'AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4' ]
channel_types = [ 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg' ]
sample_frequency = 128  # hertz
montage = 'standard_1005'

mnelogger = logging.getLogger('mne')
mnelogger.setLevel(logging.WARNING)

async def get_data():
	# make this more readable
	arr = np.random.randint(1000, size = 14)
	arr = arr / (10 ** 8) * 4
	arr = (arr * (10 ** 6)) + 4200
	return arr

async def init_cortex(creds):
	'''
	cortex.authorize token return should be stored and checked
	cortex.queryheadsets should be also stored, since is the same id

	cortex.create_session and cortex.create_record are still under study, they can remain,
	but hopefully we'll only need cortex.subscribe with the right configuration
	'''
	if creds is None:
		raise ValueError(f'No credentials found')

	cortex = Cortex(creds)
	await cortex.authorize(license_id=LICENSE_ID,debit=50)
	await cortex.query_headsets()

	if len(cortex.headsets) < 1:
		raise ValueError(f'No headsets found')

	await cortex.create_session(activate=True,headset_id=cortex.headsets[0])
	await cortex.create_record(title="emotiv raw trial")
	await cortex.subscribe(['eeg'])

	return cortex

async def generate_trial(cortex=None):
	sample_period = 0.0078125
	sps = int(1 / sample_period)
	seconds = 8
	samples = int(seconds * sps)

	trial = np.empty((14,1))

	print(f"Start recording... ")

	for i in range(0,samples + 1):
		if cortex is not None:
			await asyncio.sleep(sample_period)
			sample = await cortex.get_data()
			sample = json.loads(sample)
			sample = sample['eeg'][2:16]
		else:  # mock data
			sample = await get_data()

		trial = np.insert(trial, i + 1, sample, axis=1)
	
	trial = np.delete(trial, 0, 1)

	print(f"{seconds} seconds had passed, data generated:\n"
			f"\tChannels: {len(trial)}\n"
			f"\tShape: {trial.shape}")

	return trial

async def save_trial(trial, timestamp):
	info = mne.create_info(channel_names, sample_frequency, channel_types, montage)
	info['description'] = 'Emotiv EPOC+ dataset obtainer from Cortex API'

	custom_raw = mne.io.RawArray(trial, info)

	separator = "_"
	extension = "raw.fif"
	file_name = "./data/" + separator.join([USERID, STATE, str(timestamp), extension])

	print(f"Saving this data:\n" 
			f"\tUser ID: {USERID}\n"
			f"\tState: {STATE}\n"
			f"\tTimestamp: {timestamp}\n"
			f"\tFile: {file_name}\n")

	custom_raw.save(file_name)
	return True

async def execute(mock):
	timestamp = datetime.timestamp(datetime.now())
	if mock is False:
		cortex = await init_cortex('./cortex/cortex_creds')
		trial = await generate_trial(cortex)
		await cortex.close_session()
	else:
		trial = await generate_trial()
	result = await save_trial(trial, int(timestamp))

asyncio.run(execute(mock=MOCK))