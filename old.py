// var process = spawn('python',["./hello.py", req.query.firstname, req.query.lastname] ); 
// var process = spawn('conda activate',["/c", "python ./cortex/cortexsaver.py charle 12345"] ); 
// var process = spawn('conda activate',["/c", "python ./cortex/cortexsaver.py charle 12345"] ); 
// var process = spawn('cmd.exe', ['/c', 'binder.bat']);

from datetime import datetime
import sys 
import asyncio
import numpy as np

async def get_data():
    arr = np.random.randint(1000, size = 14)
    arr = arr / 100000000 * 4
    return arr

async def generate_trial():
    freq = 0.0078125 # sleep every freq sec 1 / 128
    sps = int(1 / freq) # must be 128 samples per second
    seconds = 8 # graz protocol trial duration
    trial = await get_data() # connect with cortex
    trial = np.reshape(trial, (14,-1))  
    
    now = datetime.now()
    timestamp = datetime.timestamp(now)

    for i in range(0, int(seconds * sps)):
        # await asyncio.sleep(freq)
        temp_data = await get_data()
        trial = np.insert(trial, i + 1, temp_data, axis=1)

    print("8 seconds has passed, saving...")
    print("Channels: ", len(trial))
    print("Shape: ", trial.shape)
    return trial


# loop = asyncio.get_event_loop()
# loop.create_task(generate_trial())
# asyncio.run(do_stuff(cortex))


async def do_stuff():
  trial = await generate_trial()
  


  print(trial)
  print("Output from Python") 
  print("User ID: " + sys.argv[1]) 
  print("Status: " + sys.argv[2]) 
  print("Timestamp: ", int(timestamp))
  print("File: ", sys.argv[1] + "_" + sys.argv[2] + "_" + str(int(timestamp)) + "_raw.fif")

# asyncio.run(do_stuff(cortex))
asyncio.run(do_stuff())

# trial