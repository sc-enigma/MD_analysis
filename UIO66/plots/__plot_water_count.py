import os, sys
import numpy as np
import matplotlib.pyplot as plt
import pickle

analysis_water_count_path = '/home/sc_enigma/Projects/MD_UIO66/analysis/water_count/'

def calculate_rmsd(x, y):
    y = np.array(y)
    average = sum(y) / len(y)
    rmsd = np.sqrt(sum(np.power(y - average, 2)) / len(y))
    return average, rmsd

for job_name in ['uio66_tempo_water128', 'uio66_tempo_water256', 'uio66_tempo_water1038']:
    if not os.path.exists(f'{analysis_water_count_path}{job_name}.pickle'):
        continue
    with open(f'{analysis_water_count_path}{job_name}.pickle', 'rb') as handle:
        data = pickle.load(handle)

    average, rmsd = calculate_rmsd(data.x, data.y)
    print(f'{job_name} average wstercount = {average} rmsd = {rmsd}')

    plt.plot(data.x, data.y, '-k')
    plt.xlabel('t, ps')
    plt.ylabel('water count in pore')
    plt.legend()
    # plt.show()
    plt.savefig(f'{analysis_water_count_path}{job_name}.png', dpi=500)


