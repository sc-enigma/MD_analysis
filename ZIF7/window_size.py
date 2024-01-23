import sys
import numpy as np
import mdtraj as md
import matplotlib.pyplot as plt
import pickle
from numba import njit

sys.path.append('../components')
from components.IterLoad import Iterload

zero_tol = 10e-20
def length(vec):
    return np.sqrt(sum(np.power(vec, 2)))

def normalize(vec):
    global zero_tol
    if length(vec) > zero_tol:
        vec /= length(vec)
    return vec

def normalize_ref(vec, ref=np.array([0.0, 0.0, 1.0])):
    vec = normalize(vec)
    if np.dot(vec, ref) < 0.0:
        vec *= -1.0
    return vec

def vec_angle(vec_a, vec_b):
    global zero_tol
    length_a = length(vec_a)
    length_b = length(vec_b)
    if length_a < zero_tol or length_b < zero_tol:
        return 0.0
    product = np.dot(vec_a, vec_b) / length_a / length_b
    return np.arccos(product)

def compute_linkers_angle(trajectory, params):
    zn_xyz = trajectory.xyz[:, params['zn_ids']]

    y = np.zeros(trajectory.n_frames)
    for t_cnt in range(trajectory.n_frames):
        zn_delta_1 = zn_xyz[t_cnt][0] - zn_xyz[t_cnt][3]
        zn_delta_2 = zn_xyz[t_cnt][1] - zn_xyz[t_cnt][4]
        zn_delta_3 = zn_xyz[t_cnt][2] - zn_xyz[t_cnt][5]
        normal = normalize(
            normalize_ref(np.cross(zn_delta_1, zn_delta_2)) +
            normalize_ref(np.cross(zn_delta_2, zn_delta_3)) +
            normalize_ref(np.cross(zn_delta_3, zn_delta_1)))
        pore_center = (zn_xyz[t_cnt][0] + zn_xyz[t_cnt][1] + zn_xyz[t_cnt][2] +
                       zn_xyz[t_cnt][3] + zn_xyz[t_cnt][4] + zn_xyz[t_cnt][5]) / 6

        for n_cnt in range(len(params['n_ids'])):
            linker_vec = (trajectory.xyz[t_cnt, params['n_ids'][n_cnt][0]] -
                          trajectory.xyz[t_cnt, params['n_ids'][n_cnt][1]])
            vec_to_center = (pore_center - trajectory.xyz[t_cnt, params['n_ids'][n_cnt][1]])
            ang = vec_angle(linker_vec, normal)
            if np.dot(linker_vec, normal) < 0.0:
                ang = np.pi - ang
            if np.dot(vec_to_center, linker_vec) < 0.0:
                ang *= -1.0
            y[t_cnt] += ang / len(params['n_ids'])

    hist_y, hist_x = np.histogram(y, bins=100, range=[-np.pi/2, np.pi/2])
    hist_y = np.append(hist_y, 0)
    return hist_x, hist_y, []

for job_name in ['zif7_tempo_lpA', 'zif7_tempo_npA', 'zif7_tempo_lpB']:
    traj = f'/media/sc_enigma/_data/Projects/MD_ZIF7/production/{job_name}/prod/traj_comp.xtc'
    top = f'/media/sc_enigma/_data/Projects/MD_ZIF7/production/{job_name}/prod/confout.gro'
    output = f'/home/sc_enigma/Projects/MD_ZIF7/analysis/linkers_angle/{job_name}'

    params = {}
    if 'A' in job_name: # START PORE FOR A TRAJECTORY
        params['zn_ids'] = [2276, 2236, 2295, 2191, 2256, 2210]
        params['n_ids'] = [[2290, 2275], [2248, 2255], [2183, 2208], [2270, 2273], [2250, 2294], [2181, 2188]]
        params['data_type'] = 'DataXY'
    Iterload(traj, top, output, compute_linkers_angle, params)


with open('/home/sc_enigma/Projects/MD_ZIF7/analysis/linkers_angle/zif7_tempo_lpA.pickle', 'rb') as handle:
    angle_data = pickle.load(handle)
plt.plot(angle_data.x, angle_data.y / angle_data.cnt_chunk)
plt.show()
