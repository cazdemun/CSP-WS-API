import numpy as np
import mne
from mne.io import Raw, RawArray
from pymonad import Monad
from toolz import compose

import sys 
import os
sys.path.append(os.path.join(os.getcwd(), 'monads'))

from task import Task

Task.of(1) \
    .fmap(lambda x: x + 1) \
    .bind(lambda x: Task.of(x + 1)) \
    .fork(lambda e: print('err', e), lambda x: print('success', x))

Task.rejected(1) \
    .fmap(lambda x: x + 1) \
    .bind(lambda x: Task.of(x + 1)) \
    .fork(lambda e: print('err', e), lambda x: print('success', x))


def launchMissiles():
    def fork(rej, res):
        print("launch missiles!")
        res("missile")
    return Task(fork)


app = launchMissiles().fmap(lambda x: x + "!")

app \
    .fmap(lambda x: x + "!") \
    .fork(lambda e: print('err', e), lambda x: print('success', x))

# 13. Use Task for Asynchronous Actions


def rawArrayBuilder() -> RawArray:
    sfreq = 1000  # Sampling frequency
    times = np.arange(0, 10, 0.001)  # Use 10000 samples (10s)

    sin = np.sin(times * 10)  # Multiplied by 10 for shorter cycles
    cos = np.cos(times * 10)
    sinX2 = sin * 2
    cosX2 = cos * 2

    # Numpy array of size 4 X 10000.
    data = np.array([sin, cos, sinX2, cosX2])

    # Definition of channel types and names.
    ch_types = ['mag', 'mag', 'grad', 'grad']
    ch_names = ['sin', 'cos', 'sinX2', 'cosX2']

    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
    return mne.io.RawArray(data, info)


def readRawFile(path: str) -> Task:  # Raw
    def fork(rej, res):
        try:
            res(mne.io.read_raw_fif(path))
        except:
            rej(rawArrayBuilder())
    return Task(fork)


# def fetchRawFile(db, path: string) -> Task: #Raw
#         try:
#             return mne.io.read_raw_fif(path)
#         except expression as identifier:
#             return Raw()

readRawFile("asdf.fif") \
    .fork(lambda e: print('err', e), lambda x: print('success', x))


