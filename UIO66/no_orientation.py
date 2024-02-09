import os, sys
import mdtraj as md
import numpy as np
import numpy.linalg as la

sys.path.append('../components')
from components.IterLoad import Iterload
from traj_names import get_traj_names

def compute_clusters_orient(trajectory, params):
    cluster_ids = params['clusters']

    coord = trajectory.xyz[0]
    r_cl = [sum([coord[atom] for atom in cluster]) / len(cluster) for cluster in cluster_ids]
    center = sum(r_cl) / 4
    dirs = [center - r for r in r_cl]

    for dir in dirs:
        if la.norm(dir) > 0.0:
            dir /= la.norm(dir)
        theta = np.arccos(dir[2])
        if dir[0] > 0:
            phi = np.arctan(dir[1] / dir[0])
        if dir[0] < 0.0:
            phi = np.arctan(dir[1] / dir[0]) + np.pi
        if dir[0] == 0.0:
            if dir[1] > 0.0:
                phi = np.pi * 0.5
            else:
                phi = np.pi * -0.5
        phi += np.pi * 0.5
        print(theta, phi)

def compute_no_orient(trajectory, params):
    no_ids = params['no_ids']

    x = trajectory.time
    y = np.zeros((len(trajectory.xyz), 2))

    for t_cnt in range(len(trajectory.xyz)):
        # NOT USED: r_int = np.transpose(la.inv(basis)).dot(r_no)
        # Coefficients in basis: r = r_int[0] * basis[0] + r_int[1] * basis[1] + r_int[2] * basis[2]

        r_no = trajectory.xyz[t_cnt][no_ids[0]] - trajectory.xyz[t_cnt][no_ids[1]]

        # Polar coordinates
        if la.norm(r_no) > 0.0:
            r_no /= la.norm(r_no)
        theta = np.arccos(r_no[2])
        if r_no[0] > 0:
            phi = np.arctan(r_no[1] / r_no[0])
        if r_no[0] < 0.0:
            phi = np.arctan(r_no[1] / r_no[0]) + np.pi
        if r_no[0] == 0.0:
            if r_no[1] > 0.0:
                phi = np.pi * 0.5
            else:
                phi = np.pi * -0.5
        phi += np.pi * 0.5

        y[t_cnt][0] = theta
        y[t_cnt][1] = phi
    return x, y, []
def mdarun(recalc_all=False):
    production_path = '/media/sc_enigma/_data/Projects/MD_UIO66/production/'
    analysis_no_path = '/home/sc_enigma/Projects/MD_UIO66/analysis/NO_orientation/'

    traj_names = get_traj_names()
    job_cnt = 0
    while job_cnt < len(traj_names):  # exclude processed trajectories
        if not recalc_all and os.path.exists(f'{analysis_no_path}{traj_names[job_cnt]}.pickle'):
            del traj_names[job_cnt]
        else:
            job_cnt += 1

    for job_name in traj_names:
        traj = f'{production_path}{job_name}/prod/traj_comp.xtc'
        top = f'{production_path}{job_name}/prod/confout.gro'

        if not os.path.exists(traj) or not os.path.exists(top):
            continue

        print('NO orientation', job_name)
        topology = md.load_topology(top)
        output = f'{analysis_no_path}{job_name}'
        params = {}
        params['data_type'] = 'DataTPos'
        params['stride'] = 1
        params['no_ids'] = np.array([\
            topology.select("resname == TMP and type == N")[0], \
            topology.select("resname == TMP and type == O")[0]])
        '''params['clusters'] = [              \
            [2601, 2590, 2611, 2621, 2643], \
            [3367, 3378, 3388, 3398, 3416], \
            [306, 319, 343, 365, 354],      \
            [315, 1642, 1633, 1621, 1596]]'''
        Iterload(traj, top, output, compute_no_orient, params)

if __name__ == "__main__":
    mdarun()