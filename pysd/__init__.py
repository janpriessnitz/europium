import numpy as np

mRyToTesla = 235.0314 # 1 mRy ~ 235 Tesla for a spin with 1*muB magnetic moment
mRyToKelvin = 157.88766343200544 # 1 mRy ~ 158 K


def fourier(ms, qxs, qys):
    qw, qh = qxs.shape
    qxs = np.reshape(qxs, (qw, qh, 1, 1))
    qys = np.reshape(qys, (qw, qh, 1, 1))
    h, w = ms.shape
    xs = np.arange(w)
    ys = np.arange(h)
    xgrid, ygrid = np.meshgrid(xs, ys)
    xgrid = np.reshape(xgrid, (1, 1, w, h))
    ygrid = np.reshape(ygrid, (1, 1, w, h))
    exps = (xgrid - 0.5*ygrid)*qxs + (0.86603*ygrid)*qys
    # exps = xgrid*Nx + ygrid*Ny
    # print((ms*np.exp(1j*exps)).shape)
    fs = np.sum(ms*np.exp(1j*exps), axis=(2,3))*np.sum(ms*np.exp(-1j*exps), axis=(2,3))/w/w/h/h

    return fs
