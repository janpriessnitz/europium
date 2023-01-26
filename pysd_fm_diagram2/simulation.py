#!/usr/bin/env python3

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

def get_config(dm, hx, hz):
  nSteps = 10000
  init_temp = 500
  fin_temp = 1
  nTemps = 25

  c = config.InpsdFile()
  c.size_x = 90
  c.size_y = 90
  c.exchangefile.interactions = [
    [1, 1, 1, 0, 0, 1],
    [1, 1, 0.50000,   0.86603,   0.00000, 1],
    [1, 1, -0.50000,   0.86603,   0.00000, 1],
    [1, 1, -1, 0, 0, 1],
    [1, 1, 0.50000,   -0.86603,   0.00000, 1],
    [1, 1, -0.50000,  -0.86603,   0.00000, 1],
  ]
  c.symmetry = 0
  c.dmfile.interactions = [
      [1, 1, 1, 0, 0, 0, 0, dm],
      [1, 1, 0.50000, 0.86603, 0.00000, 0, 0, -dm],
      [1, 1, -0.50000, 0.86603, 0.00000, 0, 0, dm],
      [1, 1, -1, 0, 0, 0, 0, -dm],
      [1, 1, 0.50000, -0.86603, 0.00000, 0, 0, -dm],
      [1, 1, -0.50000, -0.86603, 0.00000, 0, 0, dm],
    ]
  c.m_ens = 5
  c.ip_hx = hx
  c.hx = hx
  c.ip_hz = hz
  c.hz = hz

  c.plotenergy = 1

  c.ip_mcanneal.sched = [[nSteps, temp] for temp in np.geomspace(init_temp, fin_temp, num=nTemps)]

  c.do_prnstruct = 1

  c.mseed = int(time.time())
  c.tseed = int(time.time())

  # measurement phase
  c.steps = nSteps
  c.temp = fin_temp
  return c

def run_sim(dm, hx, hz):
  config = get_config(dm, hx*mRyToTesla, hz*mRyToTesla)

  l = launcher.SDLauncher()
  res = l.run(config, "run/")
  restartfiles_history = [res.restartfile]
  configs_history = [res.config]
  coordfile = res.coordfile
  result = {"restartfiles": restartfiles_history, "configs": configs_history, "coordfile": coordfile}
  with open("experiment.out", "wb") as fp:
    pickle.dump(result, fp)

  vis.plot_mag(res.coordfile, res.restartfile, "mag.png")
  return res

if __name__ == "__main__":
  run_sim(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
