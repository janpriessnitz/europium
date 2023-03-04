#!/usr/bin/python3
from pysd import vis
import os
import numpy as np
from pysd import outputfile
import sys

expdir = sys.argv[1]

coordfile = outputfile.CoordFile(expdir + "/run/coord.EXP_NAME.out")
momfile = outputfile.MomentsFile(expdir + "/run/moment.EXP_NAME.out")

vis.anim_mag_direct_imshow(coordfile,momfile.moments()[0],expdir + "/anim.mp4")