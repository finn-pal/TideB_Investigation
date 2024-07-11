# %%
import glob
import os
import re
import struct
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pynbody
import pynbody.plot as pp
import pynbody.plot.sph as sph
import scipy.interpolate
import scipy.signal

# %%
params = {"font.family": "serif", "mathtext.fontset": "stix"}
matplotlib.rcParams.update(params)

kpc_cgs = 3.08567758e21
G_cgs = 6.67e-8
Mo_cgs = 1.99e33
umass_GizToGas = 1.0  # 1e9Mo
umass = 1.0  # * umass_GizToGas
udist = 1.0  # kpc
uvel = np.sqrt(G_cgs * umass * Mo_cgs / (udist * kpc_cgs)) / 1e5
# uvel = 207.402593435
udens = umass * Mo_cgs / (udist * kpc_cgs) ** 3.0
utime = np.sqrt(1.0 / (udens * G_cgs))
sec2myr = 60.0 * 60.0 * 24.0 * 365.0 * 1e6

# %%
