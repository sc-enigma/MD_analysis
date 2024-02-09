import os.path
import sys
import matplotlib.pyplot as plt
import numpy as np
import pickle
from scipy.interpolate import splrep, BSpline

sys.path.append('../components')
from components.IterLoad import chunkDataXY
def read_xvg(file_name):
    file = open(file_name, 'r')
    lines = [line.replace('\n', '') for line in file]
    lines = [line for line in lines if len(line) != 0 \
             if line[0] != '@' and line[0] != '#' and line[0] != '&']
    file.close()

    x = [float(line.split()[0]) for line in lines]
    y = [float(line.split()[1]) for line in lines]
    return x, y

def calculate_decay_distr(x, y, bounds = [1.0 / np.pi, 0.9], steps = 500):
    def find_x(x, y, val):
        for idx in range(len(x)):
            if y[idx] < val:
                return x[idx]
        return 0.0

    def calculate_tcorr_distr(x, y, bounds = [1.0 / np.pi, 0.9], steps = 500):
        delta = (bounds[1] - bounds[0]) / steps
        acf = np.linspace(bounds[0], bounds[1], steps) # acf values
        tcorr = np.zeros(len(acf))                     # correlation time values
        for idx in range(len(acf)):
            delta_x = 0.0
            for shift in np.linspace(-delta, 0.0, 50):
                delta_x += (find_x(x, y, acf[idx] + shift) - find_x(x, y, acf[idx] + shift + delta)) / 50.0
            tcorr[idx] = abs(delta_x / np.log((acf[idx] + delta) / acf[idx]))
        return acf, tcorr

    def calculate_distr_func(x, y):
        tck_s = splrep(acf, tcorr, s=0.0)
        sample_x = np.linspace(min(acf), max(acf), int(1e6))
        sample_y = BSpline(*tck_s)(sample_x)
        hist, bin_edges = np.histogram(sample_y, bins=250, range=[0.0, 5.0])
        hist = np.append(hist, np.zeros(1))
        return bin_edges, hist

    x = np.array(x[:10000]) / 1000  # 1 ns  = 10000
    y = np.array(y[:10000])
    acf, tcorr = calculate_tcorr_distr(x, y, bounds, steps)
    return calculate_distr_func(acf, tcorr)

rotacf_names = [\
    'uio66_tempo', \
    'uio66_tempo_water128', \
    'uio66_tempo_water256', \
    'uio66_tempo_water1038', \
    'uio66_tempo_removed_linkers/removed1', \
    'uio66_tempo_removed_linkers/removed2', \
    'uio66_tempo_removed_linkers/removed3', \
    'uio66_tempo_replaced_linkers/removed1', \
    'uio66_tempo_replaced_linkers/removed2', \
    'uio66_tempo_removed_linker_and_cluster/removed1', \
    'uio66_tempo_removed_linker_and_cluster/removed2', \
    'uio66_tempo_removed_linker_and_cluster/removed3', \
    'uio66_tempo_water_removed/removed1' \
    ]

output = '/home/sc_enigma/Projects/MD_UIO66/analysis/laplas/'

def mdarun(recalc_all=False):
    for job_name in rotacf_names:
        if (os.path.exists(f'{output}{job_name}.pickle') and not recalc_all):
            continue

        print('laplas', job_name)
        x, y = read_xvg(f'/home/sc_enigma/Projects/MD_UIO66/analysis/rotacf/N_O/{job_name}.xvg')
        distr_x, distr_y = calculate_decay_distr(x, y)

        data = chunkDataXY()
        data.append(distr_x, distr_y, [])
        with open(f'{output}{job_name}.pickle', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    mdarun()

