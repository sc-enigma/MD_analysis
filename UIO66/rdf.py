import os, sys
import mdtraj as md
import numpy as np

sys.path.append('../components')
from components.IterLoad import Iterload
from traj_names import get_traj_names

def compute_rdf(trajectory, params):
    x, y = md.compute_rdf(trajectory, params['pairs'], r_range=[0.0, 2.0], bin_width=0.005, n_bins=None, periodic=True, opt=True)
    return x, y, []

def mdarun(recalc_all=False):
    production_path = '/media/sc_enigma/_data/Projects/MD_UIO66/production/'
    analysis_rdf_path = '/home/sc_enigma/Projects/MD_UIO66/analysis/rdf/'

    traj_names = get_traj_names()
    job_cnt = 0
    while job_cnt < len(traj_names):  # exclude processed trajectories
        if (not recalc_all) and os.path.exists(f'{analysis_rdf_path}{traj_names[job_cnt]}'):
            del traj_names[job_cnt]
        else:
            job_cnt += 1
    '''traj_names = ['uio66_tempo', \
                  'uio66_tempo_removed_linkers/removed1', \
                  'uio66_tempo_removed_linkers/removed2', \
                  'uio66_tempo_replaced_linkers/removed1', \
                  'uio66_tempo_replaced_linkers/removed2']'''

    for job_name in traj_names:
        traj = f'{production_path}{job_name}/prod/traj_comp.xtc'
        top = f'{production_path}{job_name}/prod/confout.gro'

        if not os.path.exists(traj) or not os.path.exists(top):
            continue

        if not os.path.exists(f'{analysis_rdf_path}{job_name}'):
            os.mkdir(f'{analysis_rdf_path}{job_name}')

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
        # pairs['tmp_all_all'] = topology.select_pairs("resname == TMP", "resname != TMP")
        if 'water' in job_name:
            pairs['tmp_all_water_o'] = topology.select_pairs("resname == TMP",               "resname == HOH and type == O")
            pairs['tmp_n_water_o'] = topology.select_pairs(  "resname == TMP and type == N", "resname == HOH and type == O")
        if 'water' in job_name and 'removed' in job_name:
            pairs['tmp_hr_water_o'] = topology.select_pairs(  "resname == UIO and name == HR", "resname == HOH and type == O")

        for key in pairs.keys():
            print('rdf', job_name, key)
            output = f'{analysis_rdf_path}{job_name}/{key}'
            params = {}
            params['pairs'] = pairs[key]
            Iterload(traj, top, output, compute_rdf, params)

if __name__ == "__main__":
    mdarun()
