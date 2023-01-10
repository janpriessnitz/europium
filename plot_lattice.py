#!/usr/bin/env python3

from pysd import vis
import pickle
import os
import sys


exp_dir = sys.argv[1]

with open(exp_dir + "/experiment.out", "rb") as fp:
    res = pickle.load(fp)
# vis.plot_hyst(res, root + "/hysteresis.png")
vis.plot_mag(res['coordfile'], res['restartfiles'][-1], exp_dir + "/lattice.png")


