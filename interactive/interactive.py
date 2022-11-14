#!/usr/bin/python3

import subprocess
import sys
import os
import shutil
import time

import pysd

from pysd import config, launcher, vis

mRyToTesla = 235.0314 # 1 mRy ~ 235 Tesla for a spin with muB magnetic moment


def get_config(dm, hx):
  nSteps = 20000
  c = config.InpsdFile()
  c.size_x = 150
  c.size_y = 150
  c.pdfile.interactions = [
      [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
      [1, 1, 0.50000,   0.86603,   0.00000, 1, 1, 1, 0, 0, 0],
      [1, 1, -0.50000,   0.86603,   0.00000, 1, 1, 1, 0, 0, 0],
      [1, 1, -1, 0, 0, 1, 1, 1, 0, 0, 0],
      [1, 1, 0.50000,   -0.86603,   0.00000, 1, 1, 1, 0, 0, 0],
      [1, 1, -0.50000,  -0.86603,   0.00000, 1, 1, 1, 0, 0, 0],
    ]


  c.dmfile.interactions = [
      [1, 1, 1, 0, 0, 0, 0, dm],
      [1, 1, 0.50000, 0.86603, 0.00000, 0, 0, dm],
      [1, 1, -0.50000, 0.86603, 0.00000, 0, 0, dm],
      # [1, 1, -1, 0, 0, 0, 0, dm],
      # [1, 1, 0.50000, -0.86603, 0.00000, 0, 0, dm],
      # [1, 1, -0.50000, -0.86603, 0.00000, 0, 0, dm],
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

  c.hx = hx*mRyToTesla  # hack for visualization
  c.plotenergy = 1

  c.do_prnstruct = 1

  c.mseed = int(time.time())
  c.tseed = int(time.time())

  # measurement phase
  c.steps = nSteps
  c.temp = 0.001
  return c

def setup_configs():
  shutil.rmtree("run")
  shutil.copytree("config", "run")

def do_interactive(dm, hx):
  config = get_config(dm, hx)
  restartfiles_history = []
  configs_history = []
  while True:
    inp_step = input("next_step (steps temp):\n")
    steps, temp = inp_step.split(" ")

    config.steps = int(steps)
    config.temp = float(temp)

    l = launcher.SDLauncher()
    res = l.run(config, "run/")
    restartfiles_history.append(res.restartfile)
    configs_history.append(res.config)
    coordfile = res.coordfile
    vis.plot_mag(res.coordfile, res.restartfile, "mag.png")

    config.initmag = 4
    config.restartfile = res.restartfile
    config.mseed = int(time.time())
    config.tseed = int(time.time())


  result = {"restartfiles": restartfiles_history, "configs": configs_history, "coordfile": coordfile}
  with open("experiment.out", "wb") as fp:
    pickle.dump(result, fp)
  vis.anim_mag(coordfile, restartfiles_history, "anim.mp4")

if __name__ == "__main__":
  do_interactive(float(sys.argv[1]), float(sys.argv[2]))