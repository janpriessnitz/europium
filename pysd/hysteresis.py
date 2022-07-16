#!/usr/bin/python3

import copy
import numpy as np

import config
import launcher

import vis

init_hz = -10
dm = 0

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
c.ip_hz = init_hz

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
[10000, 10],
[10000, 3],
[10000, 1],
[10000, 0.3],
[10000, 0.1],
]
initial_config.do_prnstruct = 1


launcher = launcher.SDLauncher()
init_res = launcher.run(initial_config, "run/init/")

restartfiles = [init_res.restartfile]

step_config = copy.deepcopy(c)
step_config.mode = 'S'
step_config.steps = 1000
step_config.initmag = 4
step_config.restartfile = init_res.restartfile
step_config.hz = 0.5
# step_config.temp = 10000

vis.plot_mag(init_res.coordfile, init_res.restartfile, "init_mag.png")

for i in range(30):
  step_res = launcher.run(step_config, "run/step/")
  print(step_res.restartfile.avg_M())
  step_config.restartfile = step_res.restartfile
  restartfiles.append(step_res.restartfile)


vis.anim_mag(init_res.coordfile, restartfiles, "anim_mag.mp4")