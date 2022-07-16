#/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation

def plot_mag(coordfile, restartfile, out_fname):
  cmap = matplotlib.cm.get_cmap('bwr')

  xs = []
  ys = []
  csx = []
  csy = []
  csz = []

  nAtoms = len(coordfile.coords)
  ens = 0
  for i in range(nAtoms):
    x, y, z = coordfile.coords[i]
    momx, momy, momz = restartfile.mag[ens][i][1:]
    
    colorx=cmap((momx+1)/2)
    colory=cmap((momy+1)/2)
    colorz=cmap((momz+1)/2)
    xs.append(x)
    ys.append(y)
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
  sc3 = ax3.scatter(xs, ys, s=30)
  ax3.set_title("Z")
  sc3.set(color=csz)
  plt.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=matplotlib.colors.Normalize(vmin=-1, vmax=1)))

  # print("showing")
  plt.savefig(out_fname)

def anim_mag(coordfile, restartfiles, out_fname):
  cmap = matplotlib.cm.get_cmap('bwr')

  xs = []
  ys = []
  csx = []
  csy = []
  csz = []

  nAtoms = len(coordfile.coords)
  ens = 0

  for i in range(nAtoms):
    x, y, z = coordfile.coords[i]
    momx, momy, momz = restartfiles[0].mag[ens][i][1:]
    
    colorx=cmap((momx+1)/2)
    colory=cmap((momy+1)/2)
    colorz=cmap((momz+1)/2)
    xs.append(x)
    ys.append(y)
    csx.append(colorx)
    csy.append(colory)
    csz.append(colorz)

  fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 3))

  # plt.figure(1, figsize=(10,10))
  sc1 = ax1.scatter(xs, ys, color=csx, s=30)
  ax1.set_title("X")
  # plt.colorbar()

  # plt.figure(2, figsize=(10,10))
  sc2 = ax2.scatter(xs, ys, color=csy, s=30)
  ax2.set_title("Y")
  # plt.colorbar()


  # plt.figure(3, figsize=(10,10))
  sc3 = ax3.scatter(xs, ys, s=30)
  ax3.set_title("Z")
  sc3.set(color=csz)
  plt.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=matplotlib.colors.Normalize(vmin=-1, vmax=1)))


  # animation function.  This is called sequentially
  def animate(j):
    restartfile = restartfiles[j]
    for i in range(nAtoms):
      momx, momy, momz = restartfile.mag[ens][i][1:]
      
      colorx=cmap((momx+1)/2)
      colory=cmap((momy+1)/2)
      colorz=cmap((momz+1)/2)
      csx[i] = colorx
      csy[i] = colory
      csz[i] = colorz
    sc1.set(color=csx)
    sc2.set(color=csy)
    sc3.set(color=csz)

  anim = animation.FuncAnimation(fig, animate,
                               frames=int(len(restartfiles)), interval=200)

  FFwriter = animation.FFMpegWriter()
  anim.save(out_fname, writer = FFwriter)

  # HTML(anim.to_jshtml())
  #HTML(anim.to_html5_video())

# plt.show()