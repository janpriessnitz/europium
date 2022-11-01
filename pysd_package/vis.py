#/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation

mRyToTesla = 235.0314 # 1 mRy ~ 235 Tesla for a spin with muB magnetic moment

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

def anim_mag_overview(coordfile, restartfiles, configs, out_fname):
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

  fig, ((ax1, ax2, ax3), (ax21, ax22, ax23)) = plt.subplots(2, 3, figsize=(15, 7))

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

  mx = []
  my = []
  line21 = ax21.plot([], [])
  ax21.set_xlim(0, len(restartfiles))
  ax21.set_ylim(-1.1, 1.1)
  ax21.set_xlabel("t")
  ax21.set_ylabel("M")

  hx = []
  hy = []
  line22 = ax22.plot(hx, hy)
  ax22.set_xlim(0, len(restartfiles))
  ax22.set_ylim(-10, 10)
  ax22.set_xlabel("t")
  ax22.set_ylabel("H")


  # MH curve
  line23 = ax23.plot([], [])
  # ax23.set_xlim(-2, 2)
  ax23.set_ylim(-1.1, 1.1)
  ax23.set_xlabel("H")
  ax23.set_ylabel("M")
  mhs = {}

  plt.tight_layout()

  # animation function.  This is called sequentially
  def animate(j):
    restartfile = restartfiles[j]
    config = configs[j]
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

    mx.append(j)
    my.append(restartfile.avg_M()[2])
    line21[0].set_data(mx, my)
    # ax21.set_ylim(np.array(my).min()-1, np.array(my).max()+1)

    hx.append(j)
    hy.append(config.hz)
    line22[0].set_data(hx, np.array(hy)/mRyToTesla)
    ax22.set_ylim((np.array(hy).min()-1)/mRyToTesla, (np.array(hy).max()+1)/mRyToTesla)

    mhs[hy[-1]] = my[-1]
    mhx = []
    mhy = []
    for k, v in mhs.items():
      mhx.append(k)
      mhy.append(v)

    line23[0].set_data(np.array(mhx)/mRyToTesla, mhy)
    ax23.set_xlim(np.array(mhx).min()/mRyToTesla, np.array(mhx).max()/mRyToTesla)
    # ax23.set_ylim(np.array(mhy).min(), np.array(mhy).max())

  anim = animation.FuncAnimation(fig, animate,
                               frames=int(len(restartfiles)), interval=200)

  return anim
  # FFwriter = animation.FFMpegWriter()
  # anim.save(out_fname, writer = FFwriter)

  # HTML(anim.to_jshtml())
  #HTML(anim.to_html5_video())

# plt.show()

def plot_hyst(res):
  hs = [x.hz for x in res['configs']]
  ms = [x.avg_M()[2] for x in res['restartfiles']]
  fig = plt.figure()
  plt.scatter(hs, ms)
  plt.savefig("hysteresis.png")