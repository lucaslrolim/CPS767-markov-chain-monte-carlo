from randomWalk import *
import matplotlib.pyplot as plt

states = [10,50,100,300,700,1000,3000,5000,10000]
lazy = 0.5
eps = pow(10,-4)

print("LIST OF STATES: ", states)

GraphMixtureResults = []
objs = [RingGraphRW(states[i],lazy) for i in range(len(states))]
for i in range(len(states)):
    result = objs[i].calculateMixingTime(eps)
    print("i = ",states[i]," mixing time = ",result)
    GraphMixtureResults.append(result)

print(GraphMixtureResults)
x_axis = states
y_axis = GraphMixtureResults
plt.plot(x_axis, y_axis, 'b-')
plt.savefig('ringRandomWalk.png')
