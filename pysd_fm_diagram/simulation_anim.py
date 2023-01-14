#!/usr/bin/python3

# Reproducing https://arxiv.org/pdf/2206.09060.pdf

import copy
import numpy as np
import time
import sys
import pickle

from pysd import config
from pysd import launcher
from pysd import vis


mRyToTesla = 235.0314 # 1 mRy ~ 235 Tesla for a spin with muB magnetic moment

def get_config(dm, hx):
  nSteps = 2000
  c = config.InpsdFile()
  c.size_x = 90
  c.size_y = 90
  c.symmetry = 0
  c.exchangefile.interactions = [
    [1, 1, 1, 0, 0, 1],
    [1, 1, -1, 0, 0, 1],
    [1, 1, 0.5, -0.86603, 0, 1],
    [1, 1, -0.5, 0.86603, 0, 1],
    [1, 1, 0.5, 0.86603, 0, 1],
    [1, 1, -0.5, -0.86603, 0, 1],
    ]


  c.dmfile.interactions = [
      [1, 1, 1, 0, 0, 0, 0, dm],
      [1, 1, 0.50000, 0.86603, 0.00000, 0, 0, dm],
      [1, 1, -0.50000, 0.86603, 0.00000, 0, 0, dm],
      [1, 1, -1, 0, 0, 0, 0, dm],
      [1, 1, 0.50000, -0.86603, 0.00000, 0, 0, dm],
      [1, 1, -0.50000, -0.86603, 0.00000, 0, 0, dm],
    ]

  # Old
  # c.dmfile.interactions = [
  #   [1, 1, 1, 0, 0, 0, 0, -dm],
  #   [1, 1, 0.50000, 0.86603, 0.00000, 0, 0, dm],
  #   [1, 1, -0.50000, 0.86603, 0.00000, 0, 0, -dm],
  #   [1, 1, -1, 0, 0, 0, 0, dm],
  #   [1, 1, 0.50000, -0.86603, 0.00000, 0, 0, dm],
  #   [1, 1, -0.50000, -0.86603, 0.00000, 0, 0, -dm],
  #   ]

  c.hx = hx  # hack for visualization

  c.do_prnstruct = 1

  c.mseed = int(time.time())
  c.tseed = int(time.time())

  # measurement phase
  c.steps = nSteps
  c.temp = 0.01
  return c

def run_sim(dm, hx):
  config = get_config(dm, hx*mRyToTesla)
  restartfiles_history = []
  configs_history = []
  l = launcher.SDLauncher()
  temps = np.geomspace(400, 1, num=30)
  for t in temps:
    config.temp = t
    res = l.run(config, "run/")
    config.restartfile = res.restartfile
    config.initmag = 4
    restartfiles_history.append(res.restartfile)
    configs_history.append(res.config)
    coordfile = res.coordfile
  result = {"restartfiles": restartfiles_history, "configs": configs_history, "coordfile": coordfile}
  with open("experiment.out", "wb") as fp:
    pickle.dump(result, fp)

  vis.plot_mag(res.coordfile, res.restartfile, "mag.png")
  vis.anim_mag(res.coordfile, restartfiles_history, "anim_mag.mp4")

if __name__ == "__main__":
  run_sim(float(sys.argv[1]), float(sys.argv[2]))
