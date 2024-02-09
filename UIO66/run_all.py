import os, sys
import mdtraj as md
import pickle
import mdtraj as md
import matplotlib.pyplot as plt
import numpy.linalg as la

sys.path.append('../components')
from components.IterLoad import Iterload
from traj_names import get_traj_names

from rdf import mdarun as run_rdf
from no_orientation import mdarun as run_no_orient
from laplas import mdarun as run_laplas

run_rdf()
run_no_orient()
run_laplas()

