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

PRINT_DIR = "plot_print/"

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
# sys.path.append("/Volumes/My Passport for Mac/TideB")
timestep = 89

fldrpth = "/Volumes/My Passport for Mac/TideB/"
init_file = "GLX.000001"
# init_file = "GLX.00001"
init_file_num = init_file.split(".")[-1]

# loop start here
past_file_num = init_file_num
next_time_num = str(int(past_file_num) + timestep)

next_file = init_file[: -len(next_time_num)] + next_time_num

filepath = fldrpth + next_file

# for some reason file naming loses a 0 at file 610

# %%
s = pynbody.load(filepath)
s.physical_units()

print("-------PREAMBLE-------")
print(next_file)
print(s.families())
print(s.loadable_keys())
print(s.properties)
print(s.g)
print(s.gas.loadable_keys())
print(s.s)
print(s.star.loadable_keys())
print(s.dm)
print(s.dm.loadable_keys())

t_now = s.properties["time"].in_units("Myr")
timestr = str(np.round(float(t_now), 1))

# %%
pynbody.analysis.angmom.faceon(s)

# bin stuff up radially:
r_enc = "15 kpc"
pp0 = pynbody.analysis.profile.Profile(s, max=r_enc, min="0.01 kpc", type="log", nbins=300)
ppd = pynbody.analysis.profile.Profile(s.dm, max=r_enc, min="0.01 kpc", type="log", nbins=300)
ppg = pynbody.analysis.profile.Profile(s.gas, max=r_enc, min="0.01 kpc", type="log", nbins=300)
pps = pynbody.analysis.profile.Profile(s.stars, max=r_enc, min="0.01 kpc", type="log", nbins=300)

print("------SETUP-DONE------")

# %%
# Some useful plots using pynbody

# Rotation curve
plt.clf()
plt.plot(pp0["rbins"], pp0["v_circ"], label="all")
plt.plot(ppd["rbins"], ppd["v_circ"], label="dark")
plt.plot(pps["rbins"], pps["v_circ"], label="star")
plt.plot(ppg["rbins"], ppg["v_circ"], label="gas")
plt.legend()
plt.xlim(0, 10)
plt.xlabel("$R$ [kpc]")
plt.ylabel("$V_{circ}$ [km/s]")
plt.savefig(PRINT_DIR + "rot_curve.pdf")

# -- Face-on stellar density plot
print("plotting stars")
vmin = 100
vmax = 600
plt.clf()
figS = plt.figure(2)
axS = figS.add_subplot(1, 1, 1)
im_S = sph.image(s.star, qty="rho", width="40 kpc", cmap="bone", subplot=axS, show_cbar=True)
plt.xlabel("$x \\;{\\rm [kpc]}$", fontsize=15)
plt.ylabel("$y \\;{\\rm [kpc]}$", fontsize=15)
axS.annotate(timestr + "Myr", xy=(0.7, 0.9), xycoords="axes fraction", color="white", fontsize=13)
plt.savefig(PRINT_DIR + "stellar_density.pdf")

# -- Face-on gas density plot
print("plotting gas")
vmin = 3e-4
vmax = 8e-2
plt.clf()
figG = plt.figure(1)
axG = figG.add_subplot(1, 1, 1)
imG = sph.image(
    s.gas, qty="rho", width="40 kpc", cmap="pink", units="g cm^-2", show_cbar=True, subplot=axG
)  # proj
plt.xlabel("$x \\;{\\rm [kpc]}$", fontsize=15)
plt.ylabel("$y \\;{\\rm [kpc]}$", fontsize=15)
axG.annotate(timestr + "Myr", xy=(0.7, 0.9), xycoords="axes fraction", color="white", fontsize=13)
plt.savefig(PRINT_DIR + "gas_density.pdf")

# -- Face-on DM density plot
print("plotting DM")
vmin = 5e1
vmax = 1e4
plt.clf()
figD = plt.figure(3)
axD = figD.add_subplot(1, 1, 1)
im_D = sph.image(
    s.dm, qty="rho", width="40 kpc", cmap="inferno", units="Msol pc^-2", show_cbar=True, subplot=axD
)  # proj
plt.xlabel("$x \\;{\\rm [kpc]}$", fontsize=15)
plt.ylabel("$y \\;{\\rm [kpc]}$", fontsize=15)
axD.annotate(timestr + "Myr", xy=(0.7, 0.9), xycoords="axes fraction", color="white", fontsize=13)
plt.savefig(PRINT_DIR + "dm_density.pdf")

print("plotting velocities")
res = 2000
cb = (True, True, True, True)
bx = 12
wx = str(2.0 * bx) + " kpc"
aza = "rho"  # uses a column average

plt.clf()
vmin = -200
vmax = 200
figVr = plt.figure(1)
axVr = figVr.add_subplot(1, 1, 1)
im = sph.image(
    s.star,
    qty="vr",
    width=wx,
    cmap="seismic",
    units="km s^-1",
    show_cbar=cb[0],
    resolution=res,
    log=False,
    vmin=vmin,
    vmax=vmax,
    av_z=aza,
)
plt.xlabel("$x \\;{\\rm [kpc]}$", fontsize=15)
plt.ylabel("$y \\;{\\rm [kpc]}$", fontsize=15)
axVr.annotate(timestr + "Myr", xy=(0.7, 0.9), xycoords="axes fraction", color="black", fontsize=13)
plt.ylim(-10, 10)
plt.savefig(PRINT_DIR + "radial_velocity.pdf")

# -- Face-on projection of Tangential velocity (v_t)
plt.clf()
vmin = 0
vmax = 200
figVt = plt.figure(1)
axVt = figVt.add_subplot(1, 1, 1)
sph.image(
    s.star,
    qty="vphi",
    width=wx,
    cmap="magma",
    show_cbar=cb[0],
    resolution=res,
    log=False,
    units="km s^-1",
    vmin=vmin,
    vmax=vmax,
    av_z=aza,
)
plt.xlabel("$x \\;{\\rm [kpc]}$", fontsize=15)
plt.ylabel("$y \\;{\\rm [kpc]}$", fontsize=15)
axVt.annotate(timestr + "Myr", xy=(0.7, 0.9), xycoords="axes fraction", color="white", fontsize=13)
plt.ylim(-10, 10)
plt.savefig(PRINT_DIR + "tangential_velocity.pdf")

# %%
