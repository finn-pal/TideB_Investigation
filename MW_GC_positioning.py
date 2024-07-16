import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table
from matplotlib.patches import Ellipse

t = Table.read("MW_data/orbit_details.csv")

x = np.array(t["x_gc"])
y = np.array(t["y_gc"])
z = np.array(t["z_gc"])

size_lims = 40
ticks = np.linspace(-size_lims, size_lims, 5)

select_min_xy = 25  # kpc
select_min_xz = 3  # kpc

size = 2
lw = 1
zord = 10
ls = "-"
colour = "tab:blue"
flag_colour = "red"

fig, axs = plt.subplots(2, 2, figsize=(8, 8))
plt.subplots_adjust(wspace=0, hspace=0)

axs[0, 1].axis("off")

xy_lim = plt.Circle((0, 0), select_min_xy, fill=False, edgecolor="r", linestyle=ls, linewidth=lw, zorder=zord)

xz_lim = Ellipse(
    xy=(0, 0),
    width=select_min_xy * 2,
    height=select_min_xz * 2,
    fill=False,
    edgecolor="r",
    linestyle=ls,
    linewidth=lw,
    zorder=zord,
)

yz_lim = Ellipse(
    xy=(0, 0),
    width=select_min_xy * 2,
    height=select_min_xz * 2,
    fill=False,
    edgecolor="r",
    linestyle=ls,
    linewidth=lw,
    zorder=zord,
)

rad_xy = (x**2 / (select_min_xy) ** 2) + (y**2 / (select_min_xy) ** 2)
colors_xy = np.array([colour] * len(rad_xy))
colors_xy[np.where(rad_xy <= 1.0)[0]] = flag_colour

# axs[0, 0].scatter(x, y, c=colors_xy, s=size)

rad_xz = (x**2 / (select_min_xy) ** 2) + (z**2 / (select_min_xz) ** 2)
colors_xz = np.array([colour] * len(rad_xz))
colors_xz[np.where(rad_xz <= 1.0)[0]] = flag_colour

# axs[1, 0].scatter(x, z, c=colors_xz, s=size)

rad_yz = (x**2 / (select_min_xy) ** 2) + (y**2 / (select_min_xz) ** 2)
colors_yz = np.array([colour] * len(rad_yz))
colors_yz[np.where(rad_xz <= 1.0)[0]] = flag_colour

# axs[1, 1].scatter(y, z, c=colors_yz, s=size)

axs[0, 0].add_patch(xy_lim)
axs[1, 0].add_patch(xz_lim)
axs[1, 1].add_patch(yz_lim)

for i, ax in enumerate(axs.flat):
    ax.set_xlim(-size_lims, size_lims)
    ax.set_ylim(-size_lims, size_lims)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)

axs[1, 0].set_xlabel("x [kpc]")
axs[1, 1].set_xlabel("y [kpc]")

axs[0, 0].set_ylabel("y [kpc]")
axs[1, 0].set_ylabel("z [kpc]")

axs[0, 0].set_xticklabels([])
axs[1, 1].set_yticklabels([])

axs[1, 0].set_yticks(ticks[:-1])
axs[1, 0].set_xticks(ticks[:-1])

# for i in range(0, len(x)):

# [x + 1 if x >= 45 else x + 5 for x in l]

req_fit = [
    1 if (xc == flag_colour and yc == flag_colour and zc == flag_colour) else 0
    for xc, yc, zc in zip(colors_xy, colors_xz, colors_yz)
]

for i in range(0, len(req_fit)):
    if req_fit[i] == 1:
        axs[0, 0].scatter(x[i], y[i], c=flag_colour, s=size)
        axs[1, 0].scatter(x[i], z[i], c=flag_colour, s=size)
        axs[1, 1].scatter(y[i], z[i], c=flag_colour, s=size)

    else:
        axs[0, 0].scatter(x[i], y[i], c=colour, s=size)
        axs[1, 0].scatter(x[i], z[i], c=colour, s=size)
        axs[1, 1].scatter(y[i], z[i], c=colour, s=size)

plt.text(
    0.5,
    0.5,
    str(len(req_fit)) + " MW GCs" + "\n\n" + str(np.sum(req_fit)) + " MW Disk GCs",
    horizontalalignment="center",
    verticalalignment="center",
    transform=axs[0, 1].transAxes,
)

# https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_performance_verification/ssec_dm_chemical_cartography.html

x_s, y_s, z_s = 8.249, 0, 0.0208
c_s = "green"
s_s = 20

axs[0, 0].scatter(x_s, y_s, marker="*", c=c_s, s=s_s)
axs[1, 0].scatter(x_s, z_s, marker="*", c=c_s, s=s_s)
axs[1, 1].scatter(y_s, z_s, marker="*", c=c_s, s=s_s)

plt.show()
