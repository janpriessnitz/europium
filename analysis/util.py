#!/usr/bin/python3


import matplotlib.pyplot as plt
import numpy as np
import matplotlib


def almost_eq(vec1, vec2):
    diff = vec1 - vec2
    return np.sqrt(np.sum(diff*diff)) < 0.001

def get_energy(lattice, size, ham):
    energy = 0
    H = ham['B']
    J1 = ham['J1']
    DM = ham['DM']
    for pos, mom in lattice:
        energy += np.sum(mom*H)
        for pos2, mom2 in lattice:
            relpos = (pos2 - pos) % size
            if np.abs(np.sqrt(np.sum(relpos*relpos)) - 1) < 0.001:
                energy += J1*np.sum(mom*mom2)
                if almost_eq(relpos, np.array([1, 0, 0])) or almost_eq(relpos, np.array([-1/2, np.sqrt(3)/2, 0])) or almost_eq(relpos, np.array([-1/2, -np.sqrt(3)/2, 0])):
                    # print("DM+", pos, pos2, relpos)
                    energy += np.sum(np.array([0, 0, DM])*np.cross(mom, mom2))
                else:
                    # print("DM-", pos, pos2, relpos)
                    energy -= np.sum(np.array([0, 0, DM])*np.cross(mom, mom2))

    return energy

def plot_mag(lattice):
  cmap = matplotlib.cm.get_cmap('bwr')

  xs = []
  ys = []
  csx = []
  csy = []
  csz = []

  nAtoms = len(lattice)
  for i in range(nAtoms):
    x, y, z = lattice[i][0][0:3]
    momx, momy, momz = lattice[i][1][0], lattice[i][1][1], lattice[i][1][2]

    colorx=cmap((momx+1)/2)
    colory=cmap((momy+1)/2)
    colorz=cmap((momz+1)/2)
    xs.append(x)
    ys.append(y)
    csx.append(colorx)
    csy.append(colory)
    csz.append(colorz)

  fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 3.5), dpi=200)


  size = 300/(nAtoms**(1/2))
  # plt.figure(1, figsize=(10,10))
  ax1.scatter(xs, ys, color=csx, s=size)
  ax1.set_title("X")
  # plt.colorbar()

  # plt.figure(2, figsize=(10,10))
  ax2.scatter(xs, ys, color=csy, s=size)
  ax2.set_title("Y")
  # plt.colorbar()


  # plt.figure(3, figsize=(10,10))
  sc3 = ax3.scatter(xs, ys, s=size)
  ax3.set_title("Z")
  sc3.set(color=csz)
  plt.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=matplotlib.colors.Normalize(vmin=-1, vmax=1)))

  # print("showing")
#   plt.savefig(out_fname)
