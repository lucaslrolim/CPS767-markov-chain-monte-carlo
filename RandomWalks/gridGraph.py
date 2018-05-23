from randomWalk import *
import matplotlib.pyplot as plt

states = [9,49,100,289,729,1000,1024,2048, 4096,8192]
lazy = 0.5
eps = pow(10,-4)

print("LIST OF STATES: ", states)

GraphMixtureResults = []
objs = [GridGraphRW(states[i],lazy) for i in range(len(states))]
for i in range(len(states)):
    result = objs[i].calculateMixingTime(eps)
    print("i = ",states[i]," mixing time = ",result)
    GraphMixtureResults.append(result)

print(GraphMixtureResults)
x_axis = states
y_axis = GraphMixtureResults
plt.plot(x_axis, y_axis, 'b-')
plt.savefig('gridRandomWalk.png')