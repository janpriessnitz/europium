#/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib


def show_traj(run_dir, exp_name="EuAlOBas", ens=0):
  coordfile = run_dir + "/coord."+exp_name+".out"
  restartfile = run_dir + "/restart."+exp_name+".out"
  coord = np.genfromtxt(coordfile)
  moms = np.genfromtxt(restartfile)

  cmap = matplotlib.cm.get_cmap('bwr')

  xs = []
  ys = []
  csx = []
  csy = []
  csz = []

  nAtoms = len(coord)

  for i in range(nAtoms):
    x0, y0 = coord[int(i)-1][1:3]
    momx, momy, momz = moms[int(i)-1 + nAtoms*ens][4:]
    colorx=cmap((momx+1)/2)
    colory=cmap((momy+1)/2)
    colorz=cmap((momz+1)/2)
    xs.append(x0)
    ys.append(y0)
    csx.append(colorx)
    csy.append(colory)
    csz.append(colorz)

  fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 3))

  # plt.figure(1, figsize=(10,10))
  ax1.scatter(xs, ys, color=csx, s=30)
  ax1.set_title("X")
  # plt.colorbar()

  # plt.figure(2, figsize=(10,10))
  ax2.scatter(xs, ys, color=csy, s=30)
  ax2.set_title("Y")
  # plt.colorbar()


  # plt.figure(3, figsize=(10,10))
  ax3.scatter(xs, ys, color=csz, s=30)
  ax3.set_title("Z")
  plt.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=matplotlib.colors.Normalize(vmin=-1, vmax=1)))

  # print("showing")
  plt.show()