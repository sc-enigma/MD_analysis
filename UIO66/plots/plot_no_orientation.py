import os, sys
import numpy as np
import matplotlib.pyplot as plt
import pickle
import matplotlib

sys.path.append('..')
from traj_names import get_traj_names

analysis_no_path = '/home/sc_enigma/Projects/MD_UIO66/analysis/NO_orientation/'

step = np.pi / 40
cnt_steps_theta = int(round(np.pi / step))
cnt_steps_phi = int(round(2.0 * np.pi / step))

def calculate_distribution(orient_data, pw = 0.5):
    global cnt_steps_theta
    global cnt_steps_phi
    distr = np.zeros((cnt_steps_theta, cnt_steps_phi))  # [theta, phi]
    for rec in orient_data.y:
        distr[int(rec[0] / step) % cnt_steps_theta, int(rec[1] / step) % cnt_steps_phi] += 1
    distr = np.power(distr, pw)
    distr /= np.max(distr)
    return distr

pw = {}
pw['uio66_tempo'] = 0.4
pw['uio66_tempo_water128'] = 0.37
pw['uio66_tempo_water256'] = 0.45
pw['uio66_tempo_water1038'] = 0.5
pw['uio66_tempo_water_removed/removed1'] = 0.43
pw['uio66_tempo_removed_linkers/removed1'] = 0.4
pw['uio66_tempo_removed_linkers/removed2'] = 0.4
pw['uio66_tempo_removed_linkers/removed3'] = 0.4
pw['uio66_tempo_replaced_linkers/removed1'] = 0.45
pw['uio66_tempo_replaced_linkers/removed2'] = 0.45
pw['uio66_tempo_removed_linker_and_cluster/removed1'] = 0.45
pw['uio66_tempo_removed_linker_and_cluster/removed2'] = 0.45
pw['uio66_tempo_removed_linker_and_cluster/removed3'] = 0.45

for job_name in get_traj_names():
    if not os.path.exists(f'{analysis_no_path}{job_name}.pickle'):
        continue
    with open(f'{analysis_no_path}{job_name}.pickle', 'rb') as handle:
        orient_data = pickle.load(handle)

    distr = calculate_distribution(orient_data, pw[job_name])

    plt.clf()
    plt.figure(figsize=(10, 7))
    '''plt.rcParams.update({'font.size': 30})
    plt.xticks([0, 2, 4, 6], ['0.0', '2.0', '4.0', '6.0'])
    plt.yticks([0, 1, 2, 3], ['0.0', '1.0', '2.0', '3.0'])'''

    x, y = np.meshgrid(np.linspace(0.0, np.pi * 2.0, cnt_steps_phi), np.linspace(0.0, np.pi, cnt_steps_theta))
    plt.pcolormesh(x, y, distr, cmap='hot')
    plt.xlabel('')
    # plt.colorbar(location='bottom')
    plt.xlabel('ϕ, rad')
    plt.ylabel('θ, rad')
    plt.title('Distribution of TEMPO NO vector orientation')

    # Direction on Zr cluster
    centers = [                          \
        [4.0561255693396150, 2.2148879],  \
        [5.5593991756399690, 1.0351192],  \
        [2.4098991314556937, 0.9337553], \
        [1.1160591403630118, 2.1318617], \
    ]
    shift = [0.125, 0.075]
    for center in centers:
        plt.plot([center[0] - shift[0], center[0] + shift[0]], [center[1], center[1]], color='yellow')
        plt.plot([center[0], center[0]], [center[1] - shift[1], center[1] + shift[1]], color='yellow')

    plt.tight_layout()
    # plt.show()
    plt.savefig(f'{analysis_no_path}{job_name}.png', dpi=500)

