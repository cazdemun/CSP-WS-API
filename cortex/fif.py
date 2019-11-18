import mne
import logging
import utils
from os import getcwd, listdir
from os.path import isfile, join

DATA_PATH = join(getcwd(), "data")

mnelogger = logging.getLogger('mne')
mnelogger.setLevel(logging.WARNING)

CHANNEL_NAMES = [ 'AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4' ]
SAMPLE_FREQUENCY = 128  # hertz
CHANNEL_TYPES = [ 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg' ]
MONTAGE = 'standard_1005'

def add_annotations(trial, filename):
	state = utils.decode_state_from_filename(filename)
	movement = state['movement']
	movement_annotations = mne.Annotations(onset=[0, 4], duration=[4, 4], description=['T0', 'T' + str(movement)])
	trial.set_annotations(movement_annotations)
	return trial

def save_trial(trial, user):
  filename = utils.create_filename(user)
  info = mne.create_info(CHANNEL_NAMES, SAMPLE_FREQUENCY, CHANNEL_TYPES, MONTAGE)
  info['description'] = 'Emotiv EPOC+ dataset obtainer from Cortex API'

  custom_raw = mne.io.RawArray(trial, info)
  custom_raw = add_annotations(custom_raw, filename)
  custom_raw.save(filename)
  return True

########################################################

def get_session(userid):
  '''
  In the best case scenario, the matrix is
    raw: channels x time
    14 x ( 1025 * 80 )
    epochs: epochs x channels x time[window]
    80 x 14 x (4.5 * 128)

    Divisions by 80 are hardcoded from graz
  '''
  # info from data saved
  info = {
    'userid': userid,
    'len': 0,
    'last_state': 0,
    'session_for_training': 0,
    'current_session': 0,
    'current_session_percentage': 0.0
  }

  all_files = get_files()
  user_files = filter_by_user(all_files, userid)
  info['len'] = len(user_files)

  if len(user_files) < 10:
    info['current_session_percentage'] = len(user_files) / 80
    return None, None, info

  # sorted_user_files = sort_files(user_files)
  # last_file = sorted_user_files[len(sorted_user_files) - 1]
  # info['last_state'] = utils.decode_filename(last_file, 'state')

  last_session_completed = int(len(user_files) / 80)
  last_session_completed = last_session_completed
  current_session = last_session_completed + 1
  info['current_session'] = current_session

  if (last_session_completed is 0):
    info['current_session_percentage'] = len(user_files) / 80
    session_files = filter_by_session(user_files, 1)
    info['session_for_training'] = 1
  else:
    session_files = filter_by_session(user_files, current_session)
    info['current_session_percentage'] = len(session_files) / 80
    session_files = filter_by_session(user_files, last_session_completed)
    info['session_for_training'] = last_session_completed
    
  # feedback is separated from training for now
  # last_session = (int(last_session / 2) * 2) + 1

  raw = pack_session(session_files)
  events, _ = mne.events_from_annotations(raw, event_id=dict(T1=2, T2=3))
  tmin, tmax = -1., 3.5
  event_id = dict(hands=2, feet=3)
  epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True,
                  baseline=None, preload=True)
  epochs_train = epochs.copy().crop(tmin=1., tmax=2.)
  labels = epochs.events[:, -1] - 2

  data = epochs_train.get_data()
  return data, labels, info

def pack_session(session_files,input_type='trial'):
  pack = []
  for t in session_files:
    t = join(DATA_PATH, t)   
    raw = mne.io.read_raw_fif(t)
    raw.load_data()
    raw.apply_function(utils.normalize_data)
    pack.append(raw)
  raw = mne.io.concatenate_raws(pack)
  return raw

def get_files():
  files = [f for f in listdir(DATA_PATH) if isfile(join(DATA_PATH, f))]
  filenames = [f for f in files if ".fif" in f]
  return filenames

def filter_by_user(filenames, userid):
  filtered = [f.split("_") for f in filenames]
  filtered = [f for f in filtered if f[0] == userid]
  filtered = ["_".join(f) for f in filtered]
  return filtered

def filter_by_session(filenames, session):
  filtered = [f for f in filenames if utils.decode_state_from_filename(f, 'session') == session]
  return filtered