#!/usr/bin/python3

import subprocess
import sys
import os
import shutil

import vis_tools as vis

def setup_configs():
  shutil.rmtree("run")
  shutil.copytree("config", "run")

def do_interactive():
  while True:
    inp_step = input("next_step (steps temp):\n")
    steps, temp = inp_step.split(" ")

    shutil.copyfile("config/inpsd.dat", "run/inpsd.dat")
    with open("run/inpsd.dat", "a") as fp:
      fp.write("\nmcnstep {}\ntemp {}\n".format(steps, temp))
      if os.path.isfile("run/restart.EuAlOBas.out"):
        fp.write("Initmag 4\nrestartfile restart.EuAlOBas.out\n")
      else:
        fp.write("Initmag 1\n")

    subprocess.run("../../uppasd", cwd="run/", capture_output=True)

    vis.show_traj("run/")

if __name__ == "__main__":
  setup_configs()
  do_interactive()