#/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation

import pickle

import scipy.optimize

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
  ax21.set_ylim(-1, 1)
  ax21.set_xlabel("t")
  ax22.set_ylabel("M")

  hx = []
  hy = []
  line22 = ax22.plot(hx, hy)
  ax22.set_xlim(0, len(restartfiles))
  ax22.set_ylim(-10, 10)
  ax22.set_xlabel("t")
  ax22.set_ylabel("H")


  # MH curve
  line23 = ax23.plot([], [])
  ax23.set_xlim(-2, 2)
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
    hy.append(config.hz / mRyToTesla)
    line22[0].set_data(hx, hy)
    ax22.set_ylim(np.array(hy).min()-1, np.array(hy).max()+1)

    mhs[hy[-1]] = my[-1]
    mhx = []
    mhy = []
    for k, v in mhs.items():
      mhx.append(k)
      mhy.append(v)

    line23[0].set_data(mhx, mhy)
    ax23.set_xlim(np.array(mhx).min(), np.array(mhx).max())
    ax23.set_ylim(np.array(mhy).min(), np.array(mhy).max())

  anim = animation.FuncAnimation(fig, animate,
                               frames=range(0, int(len(restartfiles))), interval=200)

  FFwriter = animation.FFMpegWriter()
  anim.save(out_fname, writer = FFwriter)

  # HTML(anim.to_jshtml())
  #HTML(anim.to_html5_video())

# plt.show()

def get_E(m, deltaJ, dm, H):
  if dm < 3**(1/2):
    return 6*(1 - m**2)*(deltaJ - 1) - m*H
  else:
    return 6*(1 - m**2)*(deltaJ + 1/2 - np.sqrt(3)/2*dm) - m*H

def get_theor_mag(deltaJ, dm, maxH):
  xs = np.append(np.linspace(-maxH, maxH, 200), np.linspace(maxH, -maxH, 200))
  ys = []
  lastm = [-1]
  for h in xs:
    res = scipy.optimize.minimize(get_E, lastm, args=(deltaJ, dm, h), bounds=[(-1, 1)])
    ys.append(lastm)
    lastm = res.x
  return xs, ys

def plot_hysteresis(restartfiles, configs, out_fname):
  deltaJ = configs[0].pdfile.interactions[0][7]
  dm = abs(configs[0].dmfile.interactions[0][7])
  fig, ax = plt.subplots(1, 1, figsize=(15, 7))
  # MH curve
  # ax.set_xlim(-2, 2)
  ax.set_ylim(-1.1, 1.1)
  ax.set_xlabel("H")
  ax.set_ylabel("M")
  xs = []
  ys = []
  lasth = 0
  lastm = 0
  for i in range(len(restartfiles)):
    if lasth != configs[i].hz/ mRyToTesla:
      xs.append(lasth)
      ys.append(lastm)
    lasth = configs[i].hz / mRyToTesla
    lastm = restartfiles[i].avg_M()[2]
  ax.scatter(xs, ys, color="black")

  # print(xs)

  xs2, ys2 = get_theor_mag(deltaJ, dm, np.abs(xs[1]))
  ax.plot(xs2, ys2, color="red")
  # print(xs, ys)

  plt.title("deltaJ = %.1f, DM = %.1f" % (deltaJ, dm))

  plt.savefig(out_fname)

def plot_hysteresis_from_exp(experiment_file, out_fname):
  with open(experiment_file, "rb") as fp:
    experiment = pickle.load(fp)
  plot_hysteresis(experiment["restartfiles"], experiment["configs"], out_fname)

def anim_mag_from_exp(experiment_file, out_fname):
  with open(experiment_file, "rb") as fp:
    experiment = pickle.load(fp)
  anim_mag_overview(experiment["coordfile"], experiment["restartfiles"], experiment["configs"], out_fname)


def plot_hyst(res, out_fname):
  mRyToTesla = 235.0314 # 1 mRy ~ 235 Tesla for a spin with muB magnetic moment
  config = res['configs'][1]
  hs = [x.hz/mRyToTesla for x in res['configs']]
  ms = [x.avg_M()[2] for x in res['restartfiles']]
  fig = plt.figure()
  plt.plot(hs, ms)
  plt.ylim(-1.1, 1.1)
  plt.title("Hysteresis loop AFM: Jx=-1, Jy=-1, Jz={}, D={}, T={} K".format(config.pdfile.interactions[0][7], config.dmfile.interactions[1][7], config.temp))
  plt.xlabel("H")
  plt.ylabel("M")
  plt.savefig(out_fname)