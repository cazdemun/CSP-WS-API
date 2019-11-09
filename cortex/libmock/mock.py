'''
The purpose of this mock library is to generate fake-real data.
This means we can create fake movements for the algorithm to work with.
It works almost like a signal generator
'''
import numpy as np

async def get_data():
	arr = np.random.randint(1000, size = 14)
	# random adjustment
	arr = arr / (10 ** 8) * 4
	# emotiv normalization
	arr = (arr * (10 ** 6)) + 4200
	return arr

async def get_data_sine(i, samples):
	t = (128 * 2 * math.pi) / samples
	arr = np.full(14, math.sin(t * i) * 1000)
	arr = arr / (10 ** 8) * 4
	# normalization respec to emotiv
	arr = (arr * (10 ** 6)) + 4200
	return arr