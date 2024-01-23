import os, sys
import mdtraj as md
import numpy as np
import numpy.linalg as la

sys.path.append('../components')
from components.IterLoad import Iterload
from traj_names import get_traj_names

production_path = '/media/sc_enigma/_data/Projects/MD_UIO66/production/'
analysis_no_path = '/home/sc_enigma/Projects/MD_UIO66/analysis/rdf/'
def compute_orient(trajectory, params):
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
        phi = np.arctan(r_no[1] / r_no[0])
        if r_no[0] < 0.0:
            phi += np.pi
        phi += np.pi * 0.5

        y[t_cnt][0] = theta
        y[t_cnt][1] = phi
    return x, y, []

for job_name in get_traj_names():
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
    Iterload(traj, top, output, compute_orient, params)

'''with open('/home/sc_enigma/Projects/MD_UIO66/analysis/NO_orientation/uio66_tempo.pickle', 'rb') as handle:
    orient_data = pickle.load(handle)
plt.plot(orient_data.y[:, 0], orient_data.y[:, 1])
plt.xlim([0.0, np.pi])
plt.ylim([0.0, 2.0 * np.pi])
plt.show()'''
