import os
import numpy as np

class OutputFile:
    def __init__(self, fname=None, dtype=None):
        self.fname = fname
        self.dtype = dtype
        self.data = None
        if fname != None:
            self.load_from_file(fname, dtype)

    def load_from_file(self, fname, dtype):
        self.data = np.genfromtxt(fname, dtype=dtype)

# i, x, y, z, site number, atom type number
class CoordFile(OutputFile):
    def __init__(self, fname=None):
        super().__init__(fname, dtype=[int, float, float, float, int, int])

    def n_atoms(self):
        return self.data.shape[0]

    def coords(self):
        # sort in case i is not in increasing order
        return self.data[self.data[:,0].argsort()][:,1:4]

#  iatom jatom  itype  jtype        r_{ij}^x        r_{ij}^y        r_{ij}^z          J_{ij}        |r_{ij}|
class StructFile(OutputFile):
    def __init__(self, fname=None):
        super().__init__(fname, dtype=[int, int, int, int, float, float, float, float, float])

#Iter           <M>_x           <M>_y           <M>_z             <M>        M_{stdv}
class AveragesFile(OutputFile):
    def __init__(self, fname=None):
        super().__init__(fname, dtype=[int, float, float, float, float, float])

#Iter                 Tot                 Exc                 Ani                  DM                  PD               BiqDM                  BQ                 Dip              Zeeman                 LSF                Chir                Ring                  SA
class EnergyFile(OutputFile):
    def __init__(self, fname=None):
        super().__init__(fname, dtype=[int, float, float, float, float, float, float, float, float, float, float, float, float, float])

class CumuFile(OutputFile):
    def __init__(self, fname=None):
        super().__init__(fname)

#iter   ens   iatom           |Mom|             M_x             M_y             M_z
class MomentsFile(OutputFile):
    def __init__(self, fname=None):
        super().__init__(fname, dtype=[int, int, int, float, float, float, float])

    # return numpy array in shape (ens, iter, iatom)
    def moments(self):
        iters_ens = []
        iters = np.split(self.data, np.unique(self.data['f0'], return_index=True)[1][1:])
        for iter in iters:
            iters_ens.append(np.split(iter, np.unique(iter['f1'], return_index=True)[1][1:]))
        iters_ens = np.array(iters_ens)
        ens_iters = np.transpose(iters_ens, axes=(1, 0, 2))
        return ens_iters