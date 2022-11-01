#!/usr/bin/python3

from pysd_package import vis
import pickle
import os

for root, dirs, files in os.walk("./"):
  if "experiment.out" in files:
    print("loading {}".format(root + "/experiment.out"))
    with open(root + "/experiment.out", "rb") as fp:
      res = pickle.load(fp)
    # for i in range(5):
    vis.plot_hyst(res, root + "/hysteresis.png")



