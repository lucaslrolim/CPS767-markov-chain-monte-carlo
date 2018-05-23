from randomWalk import *
import matplotlib.pyplot as plt
import math

max_t = 100
n = 1000
lazy = 0.5

v_grid = []
v_ring = []
v_binaryTree = []

gridGraph = GridGraphRW(n,lazy)
ringGraph = RingGraphRW(n,lazy)
btGraph = BinaryTreeGraphRW(n,lazy)

for t in range(1,max_t):
    v_grid.append(math.log(gridGraph.calculateVariation(t)))
    v_ring.append(math.log(ringGraph.calculateVariation(t)))
    v_binaryTree.append(math.log(btGraph.calculateVariation(t)))

x_axis = []
for i in range(1,max_t):
    x_axis.append(math.log(i))


plt.plot(x_axis,v_grid,'r-',label='GRID')
plt.plot(x_axis,v_ring,'b-',label='RING')
plt.plot(x_axis,v_binaryTree,'g-',label='TREE')
plt.legend()
plt.savefig('variation.png')
