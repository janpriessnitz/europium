#!/usr/bin/env python3

from genericpath import exists
import simulation
import os
import numpy as np

hxprecision = 0.02

i = 0

os.mkdir("phase_boundary_no1")
os.chdir("phase_boundary_no1/")
fp = open("dm_hx.txt", "w")
fp.write("# dm hx_boundary\n")
for dm in np.arange(1.8, 2.3, 0.05):
    minhx = 0
    maxhx = 5

    while maxhx - minhx > hxprecision:
        hx = (maxhx + minhx)/2
        print("\nrunning sim DM {}, HX {}".format(dm, hx))
        d = "run_{}".format(i)
        os.mkdir(d)
        os.chdir(d)
        res = simulation.run_sim(dm, hx, 0)
        os.chdir("../")
        i += 1

        avgM = res.restartfile.avg_M()
        print("got mag {}".format(avgM))
        if avgM[0] > 0.9:
            print("got FM")
            maxhx = hx
        elif avgM[0] < 0.1:
            print("got AFM")
            minhx = hx
        else:
            print("could not determine phase from mag {}".format(avgM))
    hx = (maxhx + minhx)/2
    fp.write("{} {}\n".format(dm, hx))
    
fp.close()