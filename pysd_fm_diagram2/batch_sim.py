#!/usr/bin/env python3

import simulation
import os
import numpy as np

i = 0
for dm in np.arange(1.9, 2.1, 0.05):
    for hx in np.arange(0, 2, 0.02):
        print(dm, hx)
        d = "{}_{}".format(dm, hx)
        os.mkdir(d)
        os.chdir(d)
        print("running exp in {}".format(os.getcwd()))
        simulation.run_sim(dm, hx, 0)
        os.chdir("../")
print(i)