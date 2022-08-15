#!/usr/bin/python3

import copy
import numpy as np
import time

import config
from launcher import SDLauncher

import vis


def get_coercivity(dm):
  init_hz = -10
  hz = init_hz

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
  c.hz = init_hz  # hack for visualization

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


  launcher = SDLauncher()
  init_res = launcher.run(initial_config, "run/init/")

  restartfiles_history = [init_res.restartfile]
  configs_history = [init_res.config]
  coordfile = init_res.coordfile


  step_config = copy.deepcopy(c)
  step_config.mode = 'S'
  step_config.steps = 30000
  step_config.initmag = 4
  step_config.restartfile = init_res.restartfile
  step_config.temp = 0.00001
  step_config.mseed = 2
  step_config.tseed = 2
  step_config.damping = 0.05

  def equilibrize(conf):
    def is_equilibrium(vals):
      return True
      # determines whether equilibrium is achieved based on detecting a trend in `vals`
      vals = np.array(vals)
      p, cov = np.polyfit(np.arange(len(vals)), vals, 1, cov=True)
      return np.abs(p[0]) < np.sqrt(cov[0][0]) or np.abs(p[0]) < 1e-9  # 1e-9 is negligible

    lookback_window = 10
    magzs = []
    while True:
      res = launcher.run(conf, "run/step/")
      restartfiles_history.append(res.restartfile)
      configs_history.append(copy.deepcopy(res.config))
      # res.restartfile.avg_M()[2] is the average z-component of magnetization
      magzs.append(res.restartfile.avg_M()[2])
      conf.restartfile = res.restartfile
      if len(magzs) > lookback_window and is_equilibrium(magzs[-lookback_window:]):
        break

  while True:
    print("Mz: {}, Hz: {}".format(step_config.restartfile.avg_M()[2], hz))
    step_config.hz = hz
    equilibrize(step_config)
    if step_config.restartfile.avg_M()[2] > 0:
      break

    hz += 1
  vis.anim_mag_overview(init_res.coordfile, restartfiles_history, configs_history, "anim_mag_{}.mp4".format(str(dm)))
  return hz

  # vis.plot_mag(init_res.coordfile, init_res.restartfile, "init_mag.png")

  # for i in range(30):
  #   step_res = launcher.run(step_config, "run/step/")
  #   print(step_res.restartfile.avg_M())
  #   step_config.restartfile = step_res.restartfile
  #   restartfiles.append(step_res.restartfile)


with open("coercivity.txt", "w") as fp:
  # for dm in [0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.72, 0.74, 0.76, 0.78, 0.8, 0.82, 0.84, 0.86, 0.88, 0.9]:
  for dm in [1.8]:
    hz = get_coercivity(dm)
    fp.write("{} {}\n".format(dm, hz))
    fp.flush()