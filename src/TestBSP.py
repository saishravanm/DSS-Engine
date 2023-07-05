import numpy as np
import networkx as nx
import bsp
import matplotlib.pyplot as plt

segments = np.array([
    [[1, 4], [2, 5]],
    [[0, 6], [1, 6]],
    [[0, 6], [0, 3]],
    [[0, 3], [1, 2]],
    [[1, 2], [1, 1]],
    [[1, 1], [0, 1]],
    [[0, 1], [0, 0]],
    [[0, 0], [3, 0]],
    [[3, 0], [3, 1]],
    [[3, 1], [2, 1]],
    [[2, 1], [2, 2]],
    [[2, 2], [3, 3]],
    [[3, 3], [5, 3]],
    [[5, 3], [5, 2]],
    [[5, 2], [6, 2]],
    [[6, 2], [6, 5]],
    [[6, 5], [5, 5]],
    [[5, 5], [5, 4]],
    [[5, 4], [3, 4]],
    [[3, 4], [2, 5]],
    [[2, 5], [1, 5]],
    [[1, 5], [1, 6]],
    
])

tree = bsp.build_tree(segments)

fig = plt.figure(figsize=(8,8))
axis = plt.subplot(2,1,1)
axis.grid()
for segment in segments:
    axis.plot(*(segment.T), "o-", color='k', linewidth=3, markersize=12)

ax2 = plt.subplot(2,1,2)
for _,segments in tree.nodes.data('colinear_segments'):
    print(segments)
    for segment in segments:
        ax2.plot(*(segment.T), "o-", linewidth=3, markersize=12)
        plt.pause(1)

ax2.grid()

ax2.set_xlim(axis.get_xlim())
ax2.set_ylim(axis.get_ylim())
plt.show()
