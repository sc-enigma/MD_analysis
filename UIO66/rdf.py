import os, sys
import mdtraj as md

sys.path.append('../components')
from components.IterLoad import Iterload
from traj_names import get_traj_names

production_path = '/media/sc_enigma/_data/Projects/MD_UIO66/production/'
analysis_rdf_path = '/home/sc_enigma/Projects/MD_UIO66/analysis/rdf/'

def compute_rdf(trajectory, params):
    x, y = md.compute_rdf(trajectory, params['pairs'], r_range=[0.0, 2.0], bin_width=0.005, n_bins=None, periodic=True, opt=True)
    return x, y, []

for job_name in get_traj_names():
    if not os.path.exists(f'{analysis_rdf_path}{job_name}'):
        os.mkdir(f'{analysis_rdf_path}{job_name}')
    traj = f'{production_path}{job_name}/prod/traj_comp.xtc'
    top = f'{production_path}{job_name}/prod/confout.gro'

    if not os.path.exists(traj) or not os.path.exists(top):
        continue

    pairs = {}
    topology = md.load_topology(f'{production_path}{job_name}/prod/confout.gro')
    pairs['tmp_all_uio66_zr'] = topology.select_pairs("resname == TMP",               "resname == UIO and name == Zr")
    pairs['tmp_all_uio66_c1'] = topology.select_pairs("resname == TMP",               "resname == UIO and name == C1")
    pairs['tmp_all_uio66_c2'] = topology.select_pairs("resname == TMP",               "resname == UIO and name == C2")
    pairs['tmp_all_uio66_c3'] = topology.select_pairs("resname == TMP",               "resname == UIO and name == C3")
    pairs['tmp_all_uio66_o1'] = topology.select_pairs("resname == TMP",               "resname == UIO and name == O1")
    pairs['tmp_all_uio66_o3'] = topology.select_pairs("resname == TMP",               "resname == UIO and name == O3")
    pairs['tmp_n_uio66_zr'] = topology.select_pairs(  "resname == TMP and type == N", "resname == UIO and name == Zr")
    pairs['tmp_n_uio66_c1'] = topology.select_pairs(  "resname == TMP and type == N", "resname == UIO and name == C1")
    pairs['tmp_n_uio66_c2'] = topology.select_pairs(  "resname == TMP and type == N", "resname == UIO and name == C2")
    pairs['tmp_n_uio66_c3'] = topology.select_pairs(  "resname == TMP and type == N", "resname == UIO and name == C3")
    pairs['tmp_n_uio66_o1'] = topology.select_pairs(  "resname == TMP and type == N", "resname == UIO and name == O1")
    pairs['tmp_n_uio66_o3'] = topology.select_pairs(  "resname == TMP and type == N", "resname == UIO and name == O3")

    for key in pairs.keys():
        print('rdf', job_name, key)
        output = f'{analysis_rdf_path}{job_name}/{key}'
        params = {}
        params['pairs'] = pairs[key]
        Iterload(traj, top, output, compute_rdf, params)

'''with open('/home/sc_enigma/Projects/MD_UIO66/analysis/rdf/uio66_tempo/tmp_all_uio66_zr.pickle', 'rb') as handle:
    rdf_data = pickle.load(handle)
plt.plot(rdf_data.x, rdf_data.y / rdf_data.cnt_chunk)
plt.show()'''
