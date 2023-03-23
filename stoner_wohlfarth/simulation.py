#!/usr/bin/env python3

import copy
import numpy as np
import time
import sys
import pickle

from pysd import config
from pysd import launcher
from pysd import vis


from matplotlib import pyplot as plt

def plot_energy(res : launcher.Result, out_fname):
  fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 6))
  res.energyfile.data
  Es = res.energyfile.data['tot'][1:]
  JEs = res.energyfile.data['exc'][1:]
  DMEs = res.energyfile.data['dm'][1:]
  Mzs = res.averagesfile.data['M_z'][1:]

  ax1.scatter(Mzs, JEs, label="exc")
  ax2.scatter(Mzs, DMEs, label="DM")
  ax3.scatter(Mzs, JEs + DMEs, label="exc + DM")

  plt.savefig(out_fname)

mRyToTesla = 235.0314 # 1 mRy ~ 235 Tesla for a spin with muB magnetic moment

def do_flip(dm, temp, Hz, SDsteps = 2000):
  c = config.InpsdFile()
  c.size_x = 100
  c.size_y = 100

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
  c.m_ens = 1
  
  c.mode = 'H'
  c.steps = SDsteps
  c.damping = 0.05
  c.temp = temp
  c.mseed = int(time.time())
  c.tseed = int(time.time())

  c.do_prnstruct = 1
  c.do_tottraj = 'Y'
  c.tottraj_step = 10
  c.do_cumu = 'Y'
  c.cumu_step = 10
  c.do_avrg = 'Y'
  c.avrg_step = 10
  c.plotenergy = 1


  l = launcher.SDLauncher()
  res = l.run(c, "run/")

  vis.anim_mag_direct(res.coordfile, res.momentsfile.moments()[0], "mag.mp4")
  # vis.anim_mag_direct_imshow(res.coordfile, res.momentsfile.moments()[0], "mag_imshow.mp4")

  plot_energy(res, "energy.png")

if __name__ == "__main__":
  do_flip(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))