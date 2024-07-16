import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import PillowWriter

fig = plt.figure()
# lo = plt.scatter([], [])

plt.xlim(-5, 5)
plt.ylim(-5, 5)


def func(x):
    return np.sin(x) * 3


metadata = dict(title="Test", artist="Loser")
writer = PillowWriter(fps=15, metadata=metadata)

xlist = []
ylist = []

with writer.saving(fig, "pop.gif", 100):
    for xval in np.linspace(-5, 5, 100):
        xlist.append(xval)
        ylist.append(func(xval))

        # plt.cla()

        # plt.xlim(-5, 5)
        # plt.ylim(-5, 5)
        sun = plt.scatter(xval, func(xval), c="blue", s=10)

        writer.grab_frame()
        sun.remove()
