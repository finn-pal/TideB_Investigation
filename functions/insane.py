import time

import matplotlib.pyplot as plt
import numpy as np
import pynbody
from matplotlib.animation import PillowWriter

start = time.time()

PRINT_DIR = "test_3_print/"
FLDRPTH = "/Volumes/My Passport for Mac/TideB/"

# data loop details
INIT_TIME = 1
TIMESTEP = 1
NUM_TIMESTEP = 20
I_ORD = 3

# plotting details
PLT_XLIM = 25
PLT_YLIM = 25

metadata = dict(title="Test", artist="Loser")
writer = PillowWriter(fps=1, metadata=metadata)

# for some reason file naming loses a 0 at file 610
BASE_FILE = "GLX.000000"
# INIT_FILE = "GLX.000001"
# INIT_FILE = "GLX.00001"
INIT_FILE = BASE_FILE[: -len(str(INIT_TIME))] + str(INIT_TIME)

params = {"font.family": "serif", "mathtext.fontset": "stix"}
plt.rcParams.update(params)

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

# sys.path.append("/Volumes/My Passport for Mac/TideB")
# TIMESTEP_MAX = 89
i = 0

init_file_num = INIT_FILE.split(".")[-1]
next_time_num = init_file_num

fig, ax = plt.subplots()
ax.set_xlim(-PLT_XLIM, PLT_XLIM)
ax.set_ylim(-PLT_YLIM, PLT_YLIM)

ls_pos_plt = []


print("--------- START ---------")

with writer.saving(fig, "pop2.gif", 100):
    while i <= NUM_TIMESTEP:
        next_file = INIT_FILE[: -len(next_time_num)] + next_time_num
        filepath = FLDRPTH + next_file

        # do code looping here
        s = pynbody.load(filepath)
        s.physical_units()
        t_now = s.properties["time"].in_units("Myr")
        timestr = str(np.round(float(t_now), 1))

        i_ord_pos = s[I_ORD]["pos"][0]

        print(str(int(next_time_num)) + " Myr - " + str(i_ord_pos))

        # plot
        pos_plt = ax.scatter(i_ord_pos[0], i_ord_pos[1], c="blue", s=10)
        writer.grab_frame()
        pos_plt.remove()

        # next loop step
        past_file_num = next_time_num
        next_time_num = str(int(past_file_num) + TIMESTEP)
        i = i + 1


print("---------- END ----------")
end = time.time()
print("Runtime " + str(round(end - start, 2)) + " seconds")
