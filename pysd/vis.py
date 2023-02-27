#/usr/bin/python3

from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation

mRyToTesla = 235.0314 # 1 mRy ~ 235 Tesla for a spin with muB magnetic moment

def plot_mag(coordfile, restartfile, out_fname):
  cmap = mpl.cm.get_cmap('bwr')
  coords = coordfile.coords()
  ens = 0

  xs, ys, zs = coords.T
  momxs, momys, momzs = restartfile.mag[ens].T[1:]
  csx = cmap((momxs+1)/2)
  csy = cmap((momys+1)/2)
  csz = cmap((momzs+1)/2)

  fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(18, 4), width_ratios=(1, 1, 1, 0.05))
  
  ax1.set_facecolor("lightgrey")
  ax2.set_facecolor("lightgrey")
  ax3.set_facecolor("lightgrey")
  
  ax1.set_xticks([])
  ax1.set_yticks([])
  ax2.set_xticks([])
  ax2.set_yticks([])
  ax3.set_xticks([])
  ax3.set_yticks([])

  ax1.scatter(xs, ys, color=csx, s=5)
  ax1.set_title("Mx")

  ax2.scatter(xs, ys, color=csy, s=5)
  ax2.set_title("My")

  ax3.scatter(xs, ys, color=csz, s=5)
  ax3.set_title("Mz")
  
  mpl.colorbar.ColorbarBase(ax4, cmap=cmap, orientation = 'vertical')

  plt.savefig(out_fname)
  plt.close()

def anim_mag_direct(coordfile, moms, out_fname):
  print("begin anim_mag_direct [{}]".format(datetime.now()))
  cmap = mpl.cm.get_cmap('bwr')
  coords = coordfile.coords()

  xs, ys, zs = coords['x'], coords['y'], coords['z']
 
  momxs, momys, momzs = moms[0]['M_x'], moms[0]['M_y'], moms[0]['M_z']
  csx = cmap((momxs+1)/2)
  csy = cmap((momys+1)/2)
  csz = cmap((momzs+1)/2)

  fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(18, 4), width_ratios=(1, 1, 1, 0.05))
  
  ax1.set_facecolor("lightgrey")
  ax2.set_facecolor("lightgrey")
  ax3.set_facecolor("lightgrey")

  sc1 = ax1.scatter(xs, ys, color=csx, s=5)
  ax1.set_title("Mx")

  sc2 = ax2.scatter(xs, ys, color=csy, s=5)
  ax2.set_title("My")

  sc3 = ax3.scatter(xs, ys, s=5)
  ax3.set_title("Mz")
  
  mpl.colorbar.ColorbarBase(ax4, cmap=cmap, orientation = 'vertical')
  
  def animate_init():
    return (sc1, sc2, sc3)

  def animate(j):
    momxs, momys, momzs = moms[j]['M_x'], moms[j]['M_y'], moms[j]['M_z']
    csx = cmap((momxs+1)/2)
    csy = cmap((momys+1)/2)
    csz = cmap((momzs+1)/2)

    sc1.set(color=csx)
    sc2.set(color=csy)
    sc3.set(color=csz)
    return (sc1, sc2, sc3)

  anim = animation.FuncAnimation(fig, animate, init_func=animate_init,
                                 frames=moms.shape[0], interval=200, blit=True)

  FFwriter = animation.FFMpegWriter()
  anim.save(out_fname, writer = FFwriter)
  print("end anim_mag_direct [{}]".format(datetime.now()))

def anim_mag_direct_imshow(coordfile, moms, out_fname):
  print("begin anim_mag_direct_imshow [{}]".format(datetime.now()))

  cmap = mpl.cm.get_cmap('bwr')
  coords = coordfile.coords()

  # xs, ys, zs = coords['x'], coords['y'], coords['z']
 
  momxs, momys, momzs = moms[0]['M_x'], moms[0]['M_y'], moms[0]['M_z']
  # csx = cmap((momxs+1)/2)
  # csy = cmap((momys+1)/2)
  # csz = cmap((momzs+1)/2)

  L = int(np.sqrt(momxs.shape[0]))

  momxs = momxs.reshape((L, L))
  momys = momys.reshape((L, L))
  momzs = momzs.reshape((L, L))


  fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(18, 4), width_ratios=(1, 1, 1, 0.05))
  
  ax1.set_facecolor("lightgrey")
  ax2.set_facecolor("lightgrey")
  ax3.set_facecolor("lightgrey")
    
  imx = ax1.imshow(momxs, cmap='bwr')
  ax1.set_title("Mx")

  imy = ax2.imshow(momys, cmap='bwr')
  ax2.set_title("My")

  imz = ax3.imshow(momzs, cmap='bwr')
  ax3.set_title("Mz")
  
  mpl.colorbar.ColorbarBase(ax4, cmap=cmap, orientation = 'vertical')
  
  def animate_init():
    return imx, imy, imz

  def animate(j):
    momxs, momys, momzs = moms[j]['M_x'], moms[j]['M_y'], moms[j]['M_z']

    momxs = momxs.reshape((L, L))
    momys = momys.reshape((L, L))
    momzs = momzs.reshape((L, L))

    print("momzs", momzs)

    imx.set_array(momxs)
    imy.set_array(momys)
    imz.set_array(momzs)
    return imx, imy, imz

  anim = animation.FuncAnimation(fig, animate, init_func=animate_init,
                                 frames=moms.shape[0], interval=200)

  FFwriter = animation.FFMpegWriter()
  anim.save(out_fname, writer = FFwriter)
  print("end anim_mag_direct_imshow [{}]".format(datetime.now()))


def anim_mag(coordfile, restartfiles, out_fname):
  cmap = mpl.cm.get_cmap('bwr')

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
  sc1 = ax1.scatter(xs, ys, color=csx, s=10)
  ax1.set_title("X")
  # plt.colorbar()

  # plt.figure(2, figsize=(10,10))
  sc2 = ax2.scatter(xs, ys, color=csy, s=10)
  ax2.set_title("Y")
  # plt.colorbar()


  # plt.figure(3, figsize=(10,10))
  sc3 = ax3.scatter(xs, ys, s=10)
  ax3.set_title("Z")
  sc3.set(color=csz)
  plt.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=mpl.colors.Normalize(vmin=-1, vmax=1)))


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
  cmap = mpl.cm.get_cmap('bwr')

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
  sc1 = ax1.scatter(xs, ys, color=csx, s=10)
  ax1.set_title("X")
  # plt.colorbar()

  # plt.figure(2, figsize=(10,10))
  sc2 = ax2.scatter(xs, ys, color=csy, s=10)
  ax2.set_title("Y")
  # plt.colorbar()

  # plt.figure(3, figsize=(10,10))
  sc3 = ax3.scatter(xs, ys, s=10)
  ax3.set_title("Z")
  sc3.set(color=csz)
  plt.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=mpl.colors.Normalize(vmin=-1, vmax=1)))

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
    my.append(restartfile.avg_M()[0])
    line21[0].set_data(mx, my)
    # ax21.set_ylim(np.array(my).min()-1, np.array(my).max()+1)

    hx.append(j)
    hy.append(config.hx)
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