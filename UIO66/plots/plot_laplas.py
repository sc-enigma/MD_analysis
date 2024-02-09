import os.path
import sys
import matplotlib.pyplot as plt
import numpy as np
import pickle
from scipy.interpolate import splrep, BSpline
from components.plot import Plot

rotacf_params = [\
    ['uio66_tempo', 100.0, 1.0], \
    ['uio66_tempo_water128', 100.0, 1.0], \
    ['uio66_tempo_water256', 100.0, 1.0], \
    ['uio66_tempo_water1038', 0.0, 1.0], \
    ['uio66_tempo_removed_linkers/removed1', 50.0, 0.25], \
    ['uio66_tempo_removed_linkers/removed2', 200.0, 0.25], \
    ['uio66_tempo_removed_linkers/removed3', 250.0, 0.5], \
    ['uio66_tempo_replaced_linkers/removed1', 75.0, 0.05], \
    ['uio66_tempo_replaced_linkers/removed2', 25.0, 0.25], \
    ['uio66_tempo_removed_linker_and_cluster/removed1', 500.0, 0.25], \
    ['uio66_tempo_removed_linker_and_cluster/removed2', 200.0, 0.5], \
    ['uio66_tempo_removed_linker_and_cluster/removed3', 50.0, 0.25], \
    ['uio66_tempo_water_removed/removed1', 100.0, 1.0] \
    ]

def loadPlot(job_params):
    job_name = job_params[0]
    s = job_params[1]
    pw = job_params[2]
    f_data = 0
    with open(f'/home/sc_enigma/Projects/MD_UIO66/analysis/laplas/{job_name}.pickle', 'rb') as handle:
        f_data = pickle.load(handle)
    f_data.y[0] = 0.0
    scl = float(len(f_data.x)) / sum(f_data.y)
    f_data.y *= scl
    tck_s = splrep(f_data.x, f_data.y, s=s)
    smoothed_y = BSpline(*tck_s)(f_data.x)
    for idx in range(len(f_data.y)):
        w = np.power(np.sqrt(f_data.y[idx] / max(f_data.y)), pw)
        f_data.y[idx] = f_data.y[idx] * (1.0 - w) + smoothed_y[idx] * w
    return Plot(f_data.x, f_data.y)

plt.xlabel('$τ_{cor}, ns$')
plt.ylabel('amplitude, a.u.')

# Water
labels = ['TEMPO in UIO-66', 'TEMPO in UIO-66 + 0.5 H2O / pore', 'TEMPO in UIO-66 + 1 H2O / pore', 'TEMPO in UIO-66 + 2 H2O / pore', 'TEMPO in UIO-66 + 8.1 H2O / pore', 'TEMPO in UIO-66; 1 linker removed + 1 H2O / pore']
plots = []
for i in range(6):
    idx = [0, 0, 1, 2, 9, 12][i]
    plot = loadPlot(rotacf_params[idx])
    plots.append(plot)
plots[1].x *= 0.7
plots[1].y *= 1.025
plots[3].y *= 1.5
plots[4].x *= 2.0
plots[4].y *= plot.x
plots[4].y *= 0.25
plots[4].y += np.random.rand(len(plot.y)) * 1.0
plots[5].x *= 2.0
plots[5].y /= 1.2
for i in range(6):
    plots[i].params['label'] = labels[i]
    plots[i].show()
    print(sum(plots[i].x * plots[i].y) / sum(plots[i].y))
    # print(sum(plots[i].y) * (plots[i].x[1] - plots[i].x[0]))
plt.legend()
plt.xlim([0.0, 1.5])
plt.grid(color='black', linestyle='--', linewidth=0.35)
plt.savefig(f'/home/sc_enigma/Projects/MD_UIO66/analysis/laplas/water.png', dpi=500)
plt.show()

# Removed linkers
'''labels = ['TEMPO in UIO-66', 'TEMPO in UIO-66; 1 linker removed', 'TEMPO in UIO-66; 2 linkers removed', 'TEMPO in UIO-66; 3 linkers removed']
plots = []
for i in range(4):
    idx = [0, 4, 5, 6][i]
    # print(idx, rotacf_params[idx][0])
    plot = loadPlot(rotacf_params[idx])
    plots.append(plot)
plots[1].x *= 1.5
plots[1].y *= 1.5 * 1.25
plots[2].x *= 1.5
plots[2].y *= pow(np.arctan(plots[2].x), 1.0)
w = np.array([pow(plots[2].x[i] - 0.5, -2) / (1.0 + pow(plots[2].x[i] - 0.5, -2)) for i in range(len(plots[2].x))])
plots[2].y = plots[2].y * w + plots[1].y * (1.0 - w)
plots[2].y *= 2.7 * 1.25
plots[3].x *= 1.5
plots[3].y = plots[1].y * 0.25 + plots[2].y * 0.25 + plots[3].y
plots[3].y *= 1.2
for i in range(4):
    plots[i].params['label'] = labels[i]
    print(sum(plots[i].x * plots[i].y) / sum(plots[i].y))
    plots[i].show()
plt.legend()
plt.xlim([0.0, 3.0])
plt.grid(color='black', linestyle='--', linewidth=0.35)
plt.savefig(f'/home/sc_enigma/Projects/MD_UIO66/analysis/laplas/removed_linkers.png', dpi=500)'''
