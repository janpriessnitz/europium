#!/usr/bin/python3

import copy
import numpy as np
import time
import sys
import pickle

from pysd import config
from pysd import launcher
from pysd import vis


mRyToTesla = 235.0314 # 1 mRy ~ 235 Tesla for a spin with muB magnetic moment
nPoints = 100

def get_hyst(dm, temp):
#   def get_maxH(deltaJ, dm):
#     padding = 1.3
#     if dm < 3**(1/2):
#       return np.abs(6*padding*2*(deltaJ - 1))*mRyToTesla + 10
#     else:
#       return np.abs(6*padding*2*(deltaJ + 1/2 - 3**(1/2)/2*dm))*mRyToTesla + 10

  # maxH = get_maxH(deltaJ, dm)
  maxH = 2*mRyToTesla
  init_h = -maxH

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
      [1, 1, 0.50000, 0.86603, 0.00000, 0, 0, -dm],
      [1, 1, -0.50000, 0.86603, 0.00000, 0, 0, dm],
      [1, 1, -1, 0, 0, 0, 0, -dm],
      [1, 1, 0.50000, -0.86603, 0.00000, 0, 0, -dm],
      [1, 1, -0.50000, -0.86603, 0.00000, 0, 0, dm],
    ]

  c.ip_hx = init_h
  c.hx = init_h  # hack for visualization
  c.plotenergy = 1

  initial_config = copy.deepcopy(c)
  initial_config.ip_mcanneal.sched = [
  [10000, 400],
  [10000, 350],
  [10000, 300],
  [10000, 250],
  [10000, 200],
  [10000, 150],
  [10000, 100],
  [10000, 50],
  [10000, 20],
  [10000, 10]]

  while initial_config.ip_mcanneal.sched[-1][1] > temp:
    initial_config.ip_mcanneal.sched.append([10000, initial_config.ip_mcanneal.sched[-1][1]/2])

  initial_config.do_prnstruct = 1

  l = launcher.SDLauncher()
  init_res = l.run(initial_config, "run/init/")

  restartfiles_history = [init_res.restartfile]
  configs_history = [init_res.config]
  coordfile = init_res.coordfile

  step_config = copy.deepcopy(c)
  step_config.mode = 'S'
  step_config.steps = 20000
  step_config.initmag = 4
  step_config.restartfile = init_res.restartfile
  step_config.temp = temp
  step_config.mseed = 2
  step_config.tseed = 2

  for hx in np.linspace(-maxH, maxH, 40):
    print("\nhx: {}".format(hx))
    step_config.hx = hx
    res = l.run(step_config, "run/step/")
    restartfiles_history.append(res.restartfile)
    configs_history.append(copy.deepcopy(res.config))
    step_config.restartfile = res.restartfile

    print("M: {}".format(restartfiles_history[-1].avg_M()))

  result = {"restartfiles": restartfiles_history, "configs": configs_history, "coordfile": coordfile}
  with open("experiment.out", "wb") as fp:
    pickle.dump(result, fp)

if __name__ == "__main__":
  get_hyst(float(sys.argv[1]), float(sys.argv[2]))