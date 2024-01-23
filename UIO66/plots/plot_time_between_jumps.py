import os, sys
import numpy as np
import matplotlib.pyplot as plt
import pickle
from traj_names import get_traj_names

analysis_no_path = '/home/sc_enigma/Projects/MD_UIO66/analysis/NO_orientation/'
analysis_rotacf_path = '/home/sc_enigma/Projects/MD_UIO66/analysis/rotacf/'
def read_xvg(file_name):
    file = open(file_name, 'r')
    lines = [line.replace('\n', '') for line in file]
    lines = [line for line in lines if len(line) != 0 \
             if line[0] != '@' and line[0] != '#' and line[0] != '&']
    file.close()

    x = [float(line.split()[0]) for line in lines]
    y = [float(line.split()[1]) for line in lines]
    return x, y

def calculate_time_distribution(orient_data):
    prev_quater = [0, 0]
    tau = 0.0
    tau_arr = []
    for rec_cnt in range(1, len(orient_data.y)):
        rec = orient_data.y[rec_cnt]
        quater = [int((rec[0] // (np.pi / 2)) % 2), int((rec[1] // np.pi) % 2)]

        if quater[0] == prev_quater[0] and quater[1] == prev_quater[1]:
            tau += orient_data.x[rec_cnt] - orient_data.x[rec_cnt - 1]
        else:
            if tau > 2.0:
                tau_arr.append(tau)
            prev_quater = quater
            tau = 0.0

    hist, bin_edges = np.histogram(tau_arr, bins=50, range=[0, 500.0])
    hist = np.append(hist, 0.0)
    for i in range(len(hist) - 1):
        hist[i] *= bin_edges[i + 1]
    hist /= np.max(hist)
    return bin_edges, hist

for job_name in get_traj_names():
    if not os.path.exists(f'{analysis_no_path}{job_name}.pickle'):
        continue
    with open(f'{analysis_no_path}{job_name}.pickle', 'rb') as handle:
        orient_data = pickle.load(handle)

    x, y = calculate_time_distribution(orient_data)
    plt.plot(x, y, '-k', label='Time between jumps')
    plt.xlabel('tau, ps')
    plt.ylabel('probability, a. u.')

    x_cor, y_cor = read_xvg(f'{analysis_rotacf_path}N_O/{job_name}.xvg')
    y_cor = np.array(y_cor) / max(y_cor)
    plt.plot(x_cor, y_cor, '-r', label='rotacf')
    plt.legend()
    plt.xlim([0.0, 1000.0])
    plt.ylim([0.0, 0.8])
    # plt.show()
    plt.savefig(f'{analysis_no_path}{job_name}.png', dpi=500)
