import os, sys
import mdtraj as md
import numpy as np

sys.path.append('../components')
from components.IterLoad import Iterload
from traj_names import get_traj_names

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

def mdarun():
    production_path = '/media/sc_enigma/_data/Projects/MD_UIO66/production/'
    analysis_water_count_path = '/home/sc_enigma/Projects/MD_UIO66/analysis/water_count/'

    traj_names = get_traj_names()
    job_cnt = 0
    while job_cnt < len(traj_names):  # exclude processed trajectories
        if os.path.exists(f'{analysis_water_count_path}{traj_names[job_cnt]}.pickle'):
            del traj_names[job_cnt]
        else:
            job_cnt += 1

    for job_name in ['uio66_tempo_water1038']: #traj_names:
        traj = f'{production_path}{job_name}/prod/traj_comp.xtc'
        top = f'{production_path}{job_name}/prod/confout.gro'

        if not 'water' in job_name:
            continue
        if not os.path.exists(traj) or not os.path.exists(top):
            continue

        params = {}
        topology = md.load_topology(f'{production_path}{job_name}/prod/confout.gro')
        params['data_type'] = 'DataTPos'
        sel = topology.select("resname != UIO and resname != TMP")
        params['water_ids'] = [sel[3  * i] for i in range(int(len(sel)/3))]

        if job_name == 'uio66_tempo_water128':
            params['edges'] = [343, 3367, 2611, 1651]
        if job_name == 'uio66_tempo_water256':
            params['edges'] = [3367, 2621, 1609, 306]
        if job_name == 'uio66_tempo_water1038':
            params['edges'] = [3407, 1651, 2611, 319]

        output = f'{analysis_water_count_path}{job_name}'
        Iterload(traj, top, output, compute_water_count, params)

