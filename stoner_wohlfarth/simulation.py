#!/usr/bin/env python3

import copy
import numpy as np
import time
import sys
import pickle

from pysd import config
from pysd import launcher
from pysd import vis


mRyToTesla = 235.0314 # 1 mRy ~ 235 Tesla for a spin with muB magnetic moment
SDsteps = 1000

def do_flip(dm, temp, Hz):
  c = config.InpsdFile()
  c.size_x = 3
  c.size_y = 3

  c.momfile.moms = [[1, 1, 1.00000, 0.0, 0.0, -1.0]]
  c.initmag = 3

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
  c.hz = Hz*mRyToTesla
  c.m_ens = 3
  
  c.mode = 'S'
  c.steps = SDsteps
  c.damping = 0.05
  c.temp = temp
  c.mseed = int(time.time())
  c.tseed = int(time.time())

  c.do_prnstruct = 1
  c.do_tottraj = 'Y'
  c.tottraj_step = 10
  c.do_cumu = 'Y'
  c.do_avrg = 'Y'
  c.avrg_step = 100
  c.plotenergy = 1


  l = launcher.SDLauncher()
  res = l.run(c, "run/")
  return res

  print(res.momentsfile.data.shape)

  vis.plot_mag(res.coordfile, res.restartfile, "mag.png")


if __name__ == "__main__":
  do_flip(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))