import os, sys
import matplotlib.pyplot as plt
import pickle

sys.path.append('../../components')
from components.plot import Plot
sys.path.append('..')
from traj_names import get_traj_names

analysis_rdf_path = '/home/sc_enigma/Projects/MD_UIO66/analysis/rdf/'

rdf_names = [           \
    'tmp_all_uio66_zr', \
    'tmp_all_uio66_c1', \
    'tmp_all_uio66_c2', \
    'tmp_all_uio66_c3', \
    'tmp_all_uio66_o1', \
    'tmp_all_uio66_o3', \
    'tmp_all_water_o',  \
    'tmp_n_uio66_zr',   \
    'tmp_n_uio66_c1',   \
    'tmp_n_uio66_c2',   \
    'tmp_n_uio66_c3',   \
    'tmp_n_uio66_o1',   \
    'tmp_n_uio66_o3',   \
    'tmp_n_water_o']

rdf_data = {}
for job_name in get_traj_names():
    rdf_data[job_name] = {}
    for rdf_name in rdf_names:
        if not os.path.exists(f'{analysis_rdf_path}{job_name}/{rdf_name}.pickle'):
            print(f'ERROR {analysis_rdf_path}{job_name}/{rdf_name}.pickle DOES NOT EXIST')
            continue
        with open(f'{analysis_rdf_path}{job_name}/{rdf_name}.pickle', 'rb') as handle:
            f_data = pickle.load(handle)
            rdf_data[job_name][rdf_name] = [f_data.x, f_data.y / f_data.cnt_chunk]

# Plots for TMP ALL
'''for job_name in get_traj_names():
    plt.clf()
    plots = []

    if 'tmp_all_uio66_zr' in rdf_data[job_name].keys():
        plots.append(Plot(\
            rdf_data[job_name]['tmp_all_uio66_zr'][0], \
            rdf_data[job_name]['tmp_all_uio66_zr'][1], \
            {'label': 'TEMPO ALL - UIO66 Zr'}))

    if 'tmp_all_uio66_c1' in rdf_data[job_name].keys() and  \
       'tmp_all_uio66_c2' in rdf_data[job_name].keys() and \
       'tmp_all_uio66_c3' in rdf_data[job_name].keys():
        plots.append(Plot(\
            rdf_data[job_name]['tmp_all_uio66_c1'][0],     \
           (rdf_data[job_name]['tmp_all_uio66_c1'][1] +    \
            rdf_data[job_name]['tmp_all_uio66_c2'][1] +    \
            rdf_data[job_name]['tmp_all_uio66_c3'][1]) / 3,\
            {'label': 'TEMPO ALL - UIO66 C'}))

    if 'tmp_all_uio66_o1' in rdf_data[job_name].keys() and \
       'tmp_all_uio66_o3' in rdf_data[job_name].keys():
        plots.append(Plot( \
            rdf_data[job_name]['tmp_all_uio66_o1'][0],      \
           (rdf_data[job_name]['tmp_all_uio66_o1'][1] +     \
            rdf_data[job_name]['tmp_all_uio66_o3'][1]) / 2, \
            {'label': 'TEMPO ALL - UIO66 O'}))

    if 'tmp_all_water_o' in rdf_data[job_name].keys():
        plots.append(Plot( \
            rdf_data[job_name]['tmp_all_water_o'][0], \
            rdf_data[job_name]['tmp_all_water_o'][1], \
            {'label': 'TEMPO ALL - WATER O'}))

    if len(plots) == 0:
        continue
    for plot in plots:
        plot.show()
    plt.xlim([0.0, 1.5])
    plt.xlabel('r, nm')
    plt.ylabel('g(r)')
    plt.ylim([0.0, 2.0])
    plt.legend()
    plt.savefig(f'{analysis_rdf_path}/{job_name}_all.png', dpi=500)

# Plots for TMP N
for job_name in get_traj_names():
    plt.clf()
    plots = []

    if 'tmp_n_uio66_zr' in rdf_data[job_name].keys():
        plots.append(Plot(                             \
            rdf_data[job_name]['tmp_n_uio66_zr'][0], \
            rdf_data[job_name]['tmp_n_uio66_zr'][1], \
            {'label': 'TEMPO N - UIO66 Zr'}))

    if 'tmp_n_uio66_c1' in rdf_data[job_name].keys() and \
        'tmp_n_uio66_c2' in rdf_data[job_name].keys() and \
        'tmp_n_uio66_c3' in rdf_data[job_name].keys():
        plots.append(Plot( \
            rdf_data[job_name]['tmp_n_uio66_c1'][0],       \
            (rdf_data[job_name]['tmp_n_uio66_c1'][1] +     \
             rdf_data[job_name]['tmp_n_uio66_c2'][1] +     \
             rdf_data[job_name]['tmp_n_uio66_c3'][1]) / 3, \
            {'label': 'TEMPO N - UIO66 C'}))

    if 'tmp_n_uio66_o1' in rdf_data[job_name].keys() and \
        'tmp_n_uio66_o3' in rdf_data[job_name].keys():
        plots.append(Plot( \
            rdf_data[job_name]['tmp_n_uio66_o1'][0],       \
            (rdf_data[job_name]['tmp_n_uio66_o1'][1] +     \
             rdf_data[job_name]['tmp_n_uio66_o3'][1]) / 2, \
            {'label': 'TEMPO N - UIO66 O'}))

    if 'tmp_n_water_o' in rdf_data[job_name].keys():
        plots.append(Plot( \
            rdf_data[job_name]['tmp_n_water_o'][0], \
            rdf_data[job_name]['tmp_n_water_o'][1], \
            {'label': 'TEMPO N - WATER O'}))

    if len(plots) == 0:
        continue
    for plot in plots:
        plot.show()
    plt.xlim([0.0, 1.5])
    plt.ylim([0.0, 5.0])
    plt.xlabel('r, nm')
    plt.ylabel('g(r)')
    plt.legend()
    plt.savefig(f'{analysis_rdf_path}/{job_name}.png', dpi=500)'''

# Plots for TMP ALL local density
'''plots_dens = []
for job_name in [get_traj_names()[i] for i in [0, 1, 2, 3, 4, 13]]: # [0, 1, 2, 3] [0, 4, 5, 6] [0, 7, 8, 9] [0, 10, 11, 12]
    plt.clf()

    # LOCAL DENSITY
    # O1        O3        C2          C3         C1         Zr         H1
    # 0.2859    0.0915    0.1073      0.2144     0.1071     0.4060     0.0179
    if  'tmp_all_uio66_zr' in rdf_data[job_name].keys() and \
        'tmp_all_uio66_c1' in rdf_data[job_name].keys() and \
        'tmp_all_uio66_c2' in rdf_data[job_name].keys() and \
        'tmp_all_uio66_c3' in rdf_data[job_name].keys() and \
        'tmp_all_uio66_o1' in rdf_data[job_name].keys() and \
        'tmp_all_uio66_o3' in rdf_data[job_name].keys():

        density = \
            rdf_data[job_name]['tmp_all_uio66_zr'][1] * 0.4060 + \
            rdf_data[job_name]['tmp_all_uio66_c1'][1] * 0.1071 + \
            rdf_data[job_name]['tmp_all_uio66_c2'][1] * 0.1073 + \
            rdf_data[job_name]['tmp_all_uio66_c3'][1] * 0.2144 + \
            rdf_data[job_name]['tmp_all_uio66_o1'][1] * 0.2859 + \
            rdf_data[job_name]['tmp_all_uio66_o3'][1] * 0.0915
        plots_dens.append(Plot( \
            rdf_data[job_name]['tmp_n_uio66_o1'][0], \
            density,
            {'label': job_name}))

for plot in plots_dens:
    plot.show()
plt.xlim([0.0, 1.5])
plt.xlabel('r, nm')
plt.ylabel('$ρ(r)_{loc}, g/cm_{-3}$')
plt.ylim([0.0, 2.0])
plt.legend()
plt.savefig(f'{analysis_rdf_path}/dens.png', dpi=500)'''

plots_dens = []
for job_name in ['uio66_tempo', \
                  'uio66_tempo_removed_linkers/removed1', \
                  'uio66_tempo_removed_linkers/removed2', \
                  'uio66_tempo_replaced_linkers/removed1', \
                  'uio66_tempo_replaced_linkers/removed2']:
    rdf_name = 'tmp_all_all'
    plt.clf()
    with open(f'{analysis_rdf_path}{job_name}/{rdf_name}.pickle', 'rb') as handle:
        f_data = pickle.load(handle)

    plots_dens.append(Plot( \
        f_data.x, \
        f_data.y / f_data.cnt_chunk * 1.23,
        {'label': job_name}))

for plot in plots_dens:
    plot.show()
plt.xlim([0.0, 1.5])
plt.xlabel('r, nm')
plt.ylabel('$ρ(r)_{loc}, g/cm_{-3}$')
plt.ylim([0.0, 2.0])
plt.legend()
plt.savefig(f'{analysis_rdf_path}/dens.png', dpi=500)