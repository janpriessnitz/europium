#!/usr/bin/python3

from pysd_package import restartfile
import numpy as np

N = 81
dm = 0.8


r = restartfile.Restartfile()


costheta = 0
sintheta = np.sqrt(1 - costheta**2)
mags = []
for x in range(N):
    for y in range(N):
        phi = 2*np.pi/3*(x + y)
        cosphi = np.cos(phi)
        sinphi = np.sin(phi)
        mags.append([1, sintheta*cosphi, sintheta*sinphi, costheta])

r.mag = [mags]

r.save_to_file("manual.restart")