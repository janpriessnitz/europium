#!/usr/bin/python3


import matplotlib.pyplot as plt
import numpy as np
import matplotlib


def almost_eq(vec1, vec2):
    diff = vec1 - vec2
    return np.sqrt(np.sum(diff*diff)) < 0.001

def get_energy(lattice, ham):
  energy = 0
  energyH = 0
  energyJ = 0
  energyDM = 0
  H = ham['B']
  J1 = ham['J1']
  DM = ham['DM']
  Jints = 0
  sizey = len(lattice)
  sizex = len(lattice[0])
  for yi in range(sizey):
    for xi in range(sizex):
      mom = lattice[yi][xi]
      energyH += np.sum(mom*H)
      for plusmom in [lattice[yi][(xi+1)%sizex], lattice[(yi+1)%sizey][xi], lattice[(yi-1)%sizey][(xi-1)%sizex]]:
        energyJ += J1*np.sum(mom*plusmom)
        Jints += 1
        energyDM += np.sum(np.array([0, 0, DM])*np.cross(mom, plusmom))
      for minusmom in [lattice[yi][(xi-1)%sizex], lattice[(yi-1)%sizey][xi], lattice[(yi+1)%sizey][(xi+1)%sizex]]:
        energyJ += J1*np.sum(mom*minusmom)
        Jints += 1
        energyDM -= np.sum(np.array([0, 0, DM])*np.cross(mom, minusmom))

  energyH /= sizex*sizey
  energyJ /= sizex*sizey
  energyDM /= sizex*sizey
  # print("J interactions per atom {}".format(Jints/sizex/sizey))
  print("energy: H {}, J {}, DM {}".format(energyH, energyJ, energyDM))

  return energyH + energyJ + energyDM

def plot_mag(lattice):
  x1 = np.array([1, 0, 0])
  x2 = np.array([-1/2, 3**(1/2)/2, 0])

  cmap = matplotlib.cm.get_cmap('bwr')

  xs = []
  ys = []
  csx = []
  csy = []
  csz = []

  size = len(lattice)
  for yi in range(size):
    for xi in range(size):
      x, y, z = xi*x1 + yi*x2
      momx, momy, momz = lattice[yi][xi][0], lattice[yi][xi][1], lattice[yi][xi][2]

      colorx=cmap((momx+1)/2)
      colory=cmap((momy+1)/2)
      colorz=cmap((momz+1)/2)
      xs.append(x)
      ys.append(y)
      csx.append(colorx)
      csy.append(colory)
      csz.append(colorz)

  fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 3.5), dpi=200)


  markersize = 300/(size)
  # plt.figure(1, figsize=(10,10))
  ax1.scatter(xs, ys, color=csx, s=markersize)
  ax1.set_title("X")
  # plt.colorbar()

  # plt.figure(2, figsize=(10,10))
  ax2.scatter(xs, ys, color=csy, s=markersize)
  ax2.set_title("Y")
  # plt.colorbar()


  # plt.figure(3, figsize=(10,10))
  sc3 = ax3.scatter(xs, ys, s=markersize)
  ax3.set_title("Z")
  sc3.set(color=csz)
  plt.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=matplotlib.colors.Normalize(vmin=-1, vmax=1)))

  # print("showing")
#   plt.savefig(out_fname)
