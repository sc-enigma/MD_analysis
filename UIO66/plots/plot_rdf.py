import os, sys
import matplotlib.pyplot as plt
import pickle

sys.path.append('../../components')
from components.plot import Plot
from traj_names import get_traj_names

analysis_rdf_path = '/home/sc_enigma/Projects/MD_UIO66/analysis/rdf/'

rdf_names = [           \
    'tmp_all_uio66_zr', \
    'tmp_all_uio66_c1', \
    'tmp_all_uio66_c2', \
    'tmp_all_uio66_o1', \
    'tmp_all_uio66_o3', \
    'tmp_n_uio66_zr', \
    'tmp_n_uio66_c1', \
    'tmp_n_uio66_c2', \
    'tmp_n_uio66_o1', \
    'tmp_n_uio66_o3']

# Plots for TMP ALL
rdf_data = {}
for job_name in get_traj_names():
    rdf_data[job_name] = {}
    for rdf_name in rdf_names():
        if not os.path.exists(f'{analysis_rdf_path}{job_name}/{rdf_name}.pickle'):
            continue
        with open(f'{analysis_rdf_path}{job_name}/{rdf_name}.pickle', 'rb') as handle:
            f_data = pickle.load(handle)
            rdf_data[job_name][rdf_data] = [f_data.x, f_data.y / f_data.cnt_chunk]

for job_name in get_traj_names():
    plots = []

    if 'tmp_all_uio66_zr' in rdf_data[job_name].keys():
        plots.append(Plot(\
            rdf_data[job_name]['tmp_all_uio66_zr'][0], \
            rdf_data[job_name]['tmp_all_uio66_zr'][1], \
            {'label': 'TEMPO ALL - Zr'}))

    if 'tmp_all_uio66_c1' in rdf_data[job_name].keys() and  \
       'tmp_all_uio66_c2' in rdf_data[job_name].keys() and \
       'tmp_all_uio66_c3' in rdf_data[job_name].keys():
        plots.append(Plot(\
            rdf_data[job_name]['tmp_all_uio66_c1'][0],     \
           (rdf_data[job_name]['tmp_all_uio66_c1'][1] +    \
            rdf_data[job_name]['tmp_all_uio66_c2'][1] +    \
            rdf_data[job_name]['tmp_all_uio66_c3'][1]) / 3,\
            {'label': 'TEMPO ALL - Zr'}))

    if 'tmp_all_uio66_o1' in rdf_data[job_name].keys() and \
       'tmp_all_uio66_o3' in rdf_data[job_name].keys():
        plots.append(Plot( \
            rdf_data[job_name]['tmp_all_uio66_o1'][0],      \
           (rdf_data[job_name]['tmp_all_uio66_o1'][1] +     \
            rdf_data[job_name]['tmp_all_uio66_o3'][1]) / 2, \
            {'label': 'TEMPO ALL - Zr'}))

    for plot in plots:
        plot.show()
    plt.xlim([0.0, 1.0])
    plt.xlabel('r, nm')
    plt.ylabel('g(r)')
    plt.ylim([0.0, 2.0])
    plt.legend()
    plt.savefig(f'{analysis_rdf_path}/{job_name}_all.png', dpi=500)

# Plots for TMP N
for job_name in get_traj_names():
    plots = []

    if 'tmp_n_uio66_zr' in rdf_data[job_name].keys():
        plots.append(Plot(                             \
            rdf_data[job_name]['tmp_n_uio66_zr'][0], \
            rdf_data[job_name]['tmp_n_uio66_zr'][1], \
            {'label': 'TEMPO N - Zr'}))

    if 'tmp_n_uio66_c1' in rdf_data[job_name].keys() and \
        'tmp_n_uio66_c2' in rdf_data[job_name].keys() and \
        'tmp_n_uio66_c3' in rdf_data[job_name].keys():
        plots.append(Plot( \
            rdf_data[job_name]['tmp_n_uio66_c1'][0],       \
            (rdf_data[job_name]['tmp_n_uio66_c1'][1] +     \
             rdf_data[job_name]['tmp_n_uio66_c2'][1] +     \
             rdf_data[job_name]['tmp_n_uio66_c3'][1]) / 3, \
            {'label': 'TEMPO N - C'}))

    if 'tmp_n_uio66_o1' in rdf_data[job_name].keys() and \
        'tmp_n_uio66_o3' in rdf_data[job_name].keys():
        plots.append(Plot( \
            rdf_data[job_name]['tmp_n_uio66_o1'][0],       \
            (rdf_data[job_name]['tmp_n_uio66_o1'][1] +     \
             rdf_data[job_name]['tmp_n_uio66_o3'][1]) / 2, \
            {'label': 'TEMPO N - O'}))

    for plot in plots:
        plot.show()
    plt.xlim([0.0, 1.0])
    plt.xlabel('r, nm')
    plt.ylabel('g(r)')
    plt.ylim([0.0, 2.0])
    plt.legend()
    plt.savefig(f'{analysis_rdf_path}/{job_name}.png', dpi=500)