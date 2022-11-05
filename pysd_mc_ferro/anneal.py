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
steps = 30000

def anneal(dm):
  c = config.InpsdFile()
  c.pdfile.interactions = [
  [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
  [1, 1, 0.50000,   0.86603,   0.00000, 1, 1, 1, 0, 0, 0],
  [1, 1, -0.50000,   0.86603,   0.00000, 1, 1, 1, 0, 0, 0],
  [1, 1, -1, 0, 0, 1, 1, 1, 0, 0, 0],
  [1, 1, 0.50000,   -0.86603,   0.00000, 1, 1, 1, 0, 0, 0],
  [1, 1, -0.50000,  -0.86603,   0.00000, 1, 1, 1, 0, 0, 0],
  ]
  c.dmfile.interactions = [
  [1, 1, 1, 0, 0, 0, 0, -dm],
  [1, 1, 0.50000, 0.86603, 0.00000, 0, 0, dm],
  [1, 1, -0.50000, 0.86603, 0.00000, 0, 0, -dm],
  [1, 1, -1, 0, 0, 0, 0, dm],
  [1, 1, 0.50000, -0.86603, 0.00000, 0, 0, dm],
  [1, 1, -0.50000, -0.86603, 0.00000, 0, 0, -dm],
  ]
  c.ip_hz = 0
  c.hz = 0
  c.plotenergy = 1
  c.m_ens = 5

  c.ip_mcanneal.sched = [
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
  [steps, 3],
  [steps, 1],
  [steps, 0.3],
  [steps, 0.1],
  [steps, 0.01],
  [steps, 0.001],
  [steps, 0.0001],
  ]
  c.do_prnstruct = 1
  c.mode = 'S'
  c.steps = steps
  c.temp = 0.00001
  c.mseed = int(time.time())
  c.tseed = int(time.time())

  l = launcher.SDLauncher()
  res = l.run(c, "run/init/")
  with open("experiment.out", "wb") as fp:
    pickle.dump(res, fp)

if __name__ == "__main__":
  anneal(float(sys.argv[1]))