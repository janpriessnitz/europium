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

def get_ground_state(dm, J, deltaJ):
#   def get_maxH(deltaJ, dm):
#     padding = 1.3
#     if dm < 3**(1/2):
#       return np.abs(6*padding*2*(deltaJ - 1))*mRyToTesla + 10
#     else:
#       return np.abs(6*padding*2*(deltaJ + 1/2 - 3**(1/2)/2*dm))*mRyToTesla + 10

  # maxH = get_maxH(deltaJ, dm)
#   maxH = 40*mRyToTesla
#   init_hz = -maxH

  c = config.InpsdFile()
  c.pdfile.interactions = [
  [1, 1, 1, 0, 0, J, J, deltaJ, 0, 0, 0],
  [1, 1, 0.50000,   0.86603,   0.00000, J, J, deltaJ, 0, 0, 0],
  [1, 1, -0.50000,   0.86603,   0.00000, J, J, deltaJ, 0, 0, 0],
  [1, 1, -1, 0, 0, J, J, deltaJ, 0, 0, 0],
  [1, 1, 0.50000,   -0.86603,   0.00000, J, J, deltaJ, 0, 0, 0],
  [1, 1, -0.50000,  -0.86603,   0.00000, J, J, deltaJ, 0, 0, 0],
  ]
  c.dmfile.interactions = [
  [1, 1, 1, 0, 0, 0, 0, -dm],
  [1, 1, 0.50000, 0.86603, 0.00000, 0, 0, dm],
  [1, 1, -0.50000, 0.86603, 0.00000, 0, 0, -dm],
  [1, 1, -1, 0, 0, 0, 0, dm],
  [1, 1, 0.50000, -0.86603, 0.00000, 0, 0, dm],
  [1, 1, -0.50000, -0.86603, 0.00000, 0, 0, -dm],
  ]
#   c.ip_hz = init_hz
#   c.hz = init_hz  # hack for visualization
  c.plotenergy = 1

  steps = 50000

  initial_config = copy.deepcopy(c)
  initial_config.mseed = int(time.time())
  initial_config.tseed = int(time.time())

  initial_config.ip_mcanneal.sched = [
  [steps, 500],
  [steps, 400],
  [steps, 350],
  [steps, 300],
  [steps, 250],
  [steps, 200],
  [steps, 150],
  [steps, 100],
  [steps, 50],
  [steps, 20],
  [steps, 10],
  [steps, 5],
  [steps, 2],
  [steps, 1],
  [steps, 0.5],
  [steps, 0.2],
  [steps, 0.1]]

  initial_config.do_prnstruct = 1

  initial_config.steps = steps
  initial_config.temp = 0.1


  l = launcher.SDLauncher()
  init_res = l.run(initial_config, "run/init/")

  restartfiles_history = [init_res.restartfile]
  configs_history = [init_res.config]
  coordfile = init_res.coordfile

  result = {"restartfiles": restartfiles_history, "configs": configs_history, "coordfile": coordfile}
  with open("experiment.out", "wb") as fp:
    pickle.dump(result, fp)

if __name__ == "__main__":
  get_ground_state(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))