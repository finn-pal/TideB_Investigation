import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pynbody
import pynbody.plot.sph as sph

# from ahfhalotools.objects import Cluster

PRINT_DIR = "test_print/"

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

s = pynbody.load(filepath)
s.physical_units()

pynbody.analysis.angmom.faceon(s)

# bin stuff up radially:
r_enc = "15 kpc"
pp0 = pynbody.analysis.profile.Profile(s, max=r_enc, min="0.01 kpc", type="log", nbins=300)
ppd = pynbody.analysis.profile.Profile(s.dm, max=r_enc, min="0.01 kpc", type="log", nbins=300)
ppg = pynbody.analysis.profile.Profile(s.gas, max=r_enc, min="0.01 kpc", type="log", nbins=300)
pps = pynbody.analysis.profile.Profile(s.stars, max=r_enc, min="0.01 kpc", type="log", nbins=300)

t_now = s.properties["time"].in_units("Myr")
timestr = str(np.round(float(t_now), 1))

# -- Face-on stellar density plot
vmin = 100
vmax = 600
plt.clf()
figS = plt.figure(2)
axS = figS.add_subplot(1, 1, 1)
im_S = sph.image(s.star, qty="rho", width="40 kpc", cmap="bone", subplot=axS, show_cbar=True)
plt.xlabel("$x \\;{\\rm [kpc]}$", fontsize=15)
plt.ylabel("$y \\;{\\rm [kpc]}$", fontsize=15)
axS.annotate(timestr + "Myr", xy=(0.7, 0.9), xycoords="axes fraction", color="white", fontsize=13)
plt.savefig(PRINT_DIR + "stellar_density_testing.pdf")

###################################################################################################
i = 0

print()
print(s.gas.loadable_keys())
print()
print(str(len(s.g)) + " - Gas Particles")
print("----------------------------")

# h = s.halos()
print(s.family_keys())
