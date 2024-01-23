import os, sys
import mdtraj as md
import numpy as np

sys.path.append('../components')
from components.IterLoad import Iterload
from traj_names import get_traj_names

production_path = '/media/sc_enigma/_data/Projects/MD_UIO66/production/'
analysis_water_count_path = '/home/sc_enigma/Projects/MD_UIO66/analysis/water_count/'

def compute_water_count(trajectory, params):
    def is_inside(verts, pt):
        center = np.zeros(3)
        for vert in verts:
            center += vert / len(verts)
        res = True
        for comb in [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]:
            norm = np.cross(verts[comb[1]] - verts[comb[0]], verts[comb[2]] - verts[comb[0]])
            res &= np.dot(norm, pt - verts[comb[0]]) * np.dot(norm, center - verts[comb[0]]) > 0.0
        return res

    x = trajectory.time
    y = np.zeros(len(trajectory.xyz))

    for t_cnt in range(len(trajectory.xyz)):
        verts = [\
            trajectory.xyz[t_cnt][params['edges'][0]], \
            trajectory.xyz[t_cnt][params['edges'][1]], \
            trajectory.xyz[t_cnt][params['edges'][2]], \
            trajectory.xyz[t_cnt][params['edges'][3]]]
        r_w = trajectory.xyz[t_cnt][params['water_ids']]
        for r in r_w:
            if is_inside(verts, r):
                y[t_cnt] += 1

    return x, y, []

for job_name in get_traj_names():
    traj = f'{production_path}{job_name}/prod/traj_comp.xtc'
    top = f'{production_path}{job_name}/prod/confout.gro'

    if not os.path.exists(traj) or not os.path.exists(top):
        continue

    params = {}
    topology = md.load_topology(f'{production_path}{job_name}/prod/confout.gro')
    params['data_type'] = 'DataTPos'
    params['water_ids'] = topology.select("resname == SOL and type == O")

    if job_name == 'uio66_tempo':
        params['edges'] = [0, 1, 2, 3]

    output = f'{analysis_water_count_path}{job_name}'
    Iterload(traj, top, output, compute_water_count, params)

