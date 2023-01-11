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
  nSteps = 1000
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

  c.ip_hx = hx
  c.hx = hx  # hack for visualization
  c.plotenergy = 1

  c.ip_mcanneal.sched = [
    [nSteps, 400],
    [nSteps, 350],
    [nSteps, 300],
    [nSteps, 250],
    [nSteps, 200],
    [nSteps, 150],
    [nSteps, 100],
    [nSteps, 50],
    [nSteps, 20],
    [nSteps, 10],
    [nSteps, 5],
    [nSteps, 2],
    [nSteps, 1],
    [nSteps, 0.5],
    [nSteps, 0.2],
    [nSteps, 0.1],
    [nSteps, 0.05],
    [nSteps, 0.02],
    [nSteps, 0.01]]

  c.do_prnstruct = 1

  c.mseed = int(time.time())
  c.tseed = int(time.time())

  # measurement phase
  c.steps = nSteps
  c.temp = 0.01
  return c

def run_sim(dm, hx):
  config = get_config(dm, hx*mRyToTesla)

  l = launcher.SDLauncher()
  res = l.run(config, "run/")
  restartfiles_history = [res.restartfile]
  configs_history = [res.config]
  coordfile = res.coordfile
  result = {"restartfiles": restartfiles_history, "configs": configs_history, "coordfile": coordfile}
  with open("experiment.out", "wb") as fp:
    pickle.dump(result, fp)

  vis.plot_mag(res.coordfile, res.restartfile, "mag.png")

if __name__ == "__main__":
  run_sim(float(sys.argv[1]), float(sys.argv[2]))
