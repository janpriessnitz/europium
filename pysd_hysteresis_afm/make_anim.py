#!/usr/bin/python3

from pysd_package import vis
import pickle
import os
import sys


exp_dir = sys.argv[1]
print("loading {}".format(exp_dir + "/experiment.out"))
with open(exp_dir + "/experiment.out", "rb") as fp:
    res = pickle.load(fp)
vis.plot_hyst(res, exp_dir + "/hysteresis.png")
vis.anim_mag_overview(res['coordfile'], res['restartfiles'], res['configs'], "anim_mag.mp4")



