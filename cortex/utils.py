# graz: 6 sessions, 4 runs, 2 movements, 10 trials
def decode_state(state, cproperty=None, protocol="graz"):
  state = int(state) - 1
  tri, mov, run, ses = 10, 2, 4, 6
  decoded_state = {
    "session": (int(state / int(tri * mov * run)) % ses) + 1,
    "run": (int(state / int(tri * mov)) % run) + 1,
    "movement": (int(state / tri) % mov) + 1,
    "trial": (state % tri) + 1
  }
  if cproperty is not None:
    return decoded_state[cproperty]
  return decoded_state

def decode_filename(filename, cproperty=None):
  user_split = filename.split("_")
  decoded_filename = {
    'userid':user_split[0],
    'state': int(float(user_split[1])),
    'timestamp': int(float(user_split[2]))
  }
  if cproperty is not None:
    return decoded_filename[cproperty]
  return decoded_filename

def decode_state_from_filename(f, cproperty=None):
  decoded_f = decode_filename(f, 'state')
  decoded_s = decode_state(decoded_f)
  if cproperty is not None:
    return decoded_s[cproperty]
  return decoded_s

def create_filename(user):
  extension = "raw.fif"
  filename = "./data/" + "_".join([
    user['userid'], 
    str(user['state']), 
    str(user['timestamp']), 
    extension
  ])
  return filename

def normalize_data(channel):
  channel = (channel - 4200) / 10 ** 6
  return channel