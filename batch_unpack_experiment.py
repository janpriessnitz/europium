#!/usr/bin/python3

import os
import pickle

for root, dirs, files in os.walk("./"):
  if "experiment.out" in files:
    output_dir = root + "/uppasd_out/"
    print("unpacking {} into ".format(root + "/experiment.out", output_dir))
    with open(root + "/experiment.out", "rb") as fp:
      res = pickle.load(fp)
    os.makedirs(output_dir, exist_ok=True)
    init_dir = output_dir+"/init/"
    os.makedirs(init_dir, exist_ok=True)
    res['configs'][0].save_all_configs(init_dir)
    res['restartfiles'][0].save_to_file(init_dir+"/restart.out")
    for i in range(1, len(res['configs'])):
        step_dir = output_dir+"/step_{}".format(i)
        os.makedirs(step_dir, exist_ok=True)
        res['configs'][i].save_all_configs(step_dir)
        res['restartfiles'][i].save_to_file(step_dir+"/restart.out")


