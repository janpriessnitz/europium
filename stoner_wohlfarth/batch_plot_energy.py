#!/usr/bin/python3

import os
import matplotlib.pyplot as plt
import numpy as np


def plot_energy(rundir, out_fname):
    DM, temp, Hfield = rundir.split("/")[0].split("_")

    fig, ((ax11, ax12), (ax21, ax22)) = plt.subplots(2, 2, figsize=(12, 8))

    energydata = np.genfromtxt(rundir + "/totenergy.EXP_NAME.out")
    averagedata = np.genfromtxt(rundir + "/averages.EXP_NAME.out")
    Es = energydata[1:,1]
    JEs = energydata[1:,2]
    DMEs = energydata[1:,4]
    Mzs = averagedata[1:-1,3]

    plt.suptitle("Mz flip - energy - DM={}, T={} K, external_H={}".format(DM, temp, Hfield))

    ax11.scatter(Mzs, JEs, label="exchange")
    ax11.set_xlabel("Mz")
    ax11.set_ylabel("E")
    ax11.legend()
    
    ax12.scatter(Mzs, DMEs, label="DM")
    ax12.set_xlabel("Mz")
    ax12.set_ylabel("E")
    ax12.legend()
    
    ax21.scatter(Mzs, JEs + DMEs, label="exchange + DM")
    ax21.set_xlabel("Mz")
    ax21.set_ylabel("E")
    ax21.legend()

    ax22.scatter(Mzs, Es, label="exchange + DM + Hfield")    
    ax22.set_xlabel("Mz")
    ax22.set_ylabel("E")
    ax22.legend()

    plt.tight_layout()

    plt.savefig(out_fname)
    plt.close()

for d in os.listdir("."):
    rundir = d + "/run"
    print(d)
    plot_energy(rundir, d + "/energy.png")