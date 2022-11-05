#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import pickle
import os

for root, dirs, files in os.walk("./"):
  if "experiment.out" in files:
    print("loading {}".format(root + "/experiment.out"))
    with open(root + "/experiment.out", "rb") as fp:
      res = pickle.load(fp)
    # for i in range(5):
    mRyToTesla = 235.0314 # 1 mRy ~ 235 Tesla for a spin with muB magnetic moment
    config = res['configs'][1]
    hs = [x.hx/mRyToTesla for x in res['configs']]
    # hs.extend([h for h in hs[::-1] ])
    ms = [x.avg_M() for x in res['restartfiles']]
    # ms.extend([[-mx, -my, -mz] for mx, my, mz in ms])
    ms = np.array(ms)
    fig = plt.figure()
    plt.plot(hs, ms.T[0], label="Mx")
    plt.plot(hs, ms.T[1], label="My")
    plt.plot(hs, ms.T[2], label="Mz")
    plt.ylim(-1.1, 1.1)
    plt.title("Hysteresis loop FM: D={}, T={} K".format(config.dmfile.interactions[1][7], config.temp))
    plt.xlabel("Hx")
    plt.ylabel("M")
    plt.legend()
    plt.savefig(root+"/hyst.png")
    plt.close(fig)


