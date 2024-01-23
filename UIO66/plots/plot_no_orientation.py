import os, sys
import numpy as np
import matplotlib.pyplot as plt
import pickle

sys.path.append('..')
from traj_names import get_traj_names

analysis_no_path = '/home/sc_enigma/Projects/MD_UIO66/analysis/NO_orientation/'

step = np.pi / 40
cnt_steps_theta = int(round(np.pi / step))
cnt_steps_phi = int(round(2.0 * np.pi / step))

def calculate_distribution(orient_data):
    global cnt_steps_theta
    global cnt_steps_phi
    distr = np.zeros((cnt_steps_theta, cnt_steps_phi))  # [theta, phi]
    for rec in orient_data.y:
        distr[int(rec[0] / step) % cnt_steps_theta, int(rec[1] / step) % cnt_steps_phi] += 1
    distr = np.sqrt(distr)
    distr /= np.max(distr)
    return distr

for job_name in get_traj_names():
    if not os.path.exists(f'{analysis_no_path}{job_name}.pickle'):
        continue
    with open(f'{analysis_no_path}{job_name}.pickle', 'rb') as handle:
        orient_data = pickle.load(handle)

    distr = calculate_distribution(orient_data)

    x, y = np.meshgrid(np.linspace(0.0, np.pi * 2.0, cnt_steps_phi), np.linspace(0.0, np.pi, cnt_steps_theta))
    plt.pcolormesh(x, y, distr, cmap='hot')
    plt.xlabel('')
    plt.colorbar()
    plt.xlabel('ϕ, rad')
    plt.ylabel('θ, rad')
    plt.title('Distribution of TEMPO NO vector orientation')
    # plt.show()
    plt.savefig(f'{analysis_no_path}{job_name}.png', dpi=500)
