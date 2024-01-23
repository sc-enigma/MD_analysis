import sys
import numpy as np
import mdtraj as md
import matplotlib.pyplot as plt
import pickle

class chunkDataXY:
    def __init__(self):
        self.x = np.empty([])
        self.y = np.empty([])
        self.cnt_chunk = 0

    def append(self, x, y, auxiliary):
        if self.cnt_chunk == 0:
            self.x = x
            self.y = y
        else:
            self.x = x
            self.y += y
        self.cnt_chunk += 1

class chunkDataTPos:
    def __init__(self):
        self.x = np.empty([])
        self.y = np.empty([])
        self.cnt_chunk = 0

    def append(self, x, y, auxiliary):
        if self.cnt_chunk == 0:
            self.x = x
            self.y = y
        else:
            self.x = np.append(self.x, x)
            self.y = np.append(self.y, y, axis=0)
        self.cnt_chunk += 1

def Iterload(traj, top, output, func, params):
    if not '.xtc' in traj:
        traj += '.xtc'
    if not '.gro' in top:
        top += '.gro'

    limit = -1
    if 'limit' in params:
        limit = params['limit']
    chunk = 1000
    if 'chunk' in params:
        chunk = params['chunk']
    stride = 10
    if 'stride' in params:
        stride = params['stride']
    data = None
    if 'data_type' in params:
        if params['data_type'] == 'DataTPos':
            data = chunkDataTPos()
    if data == None:
        data = chunkDataXY()

    for trajectory in md.iterload(traj, top=top, chunk=chunk, stride=stride):
        if trajectory.time[-1] / 1000 > limit and limit > 0:
            break
        print(f'{round(trajectory.time[-1] / 1000, 3)} ns')

        x, y, auxiliary = func(trajectory, params)
        data.append(x, y, auxiliary)

        with open(f'{output}.pickle', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)