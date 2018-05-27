from utilityFunctions import * 
import matplotlib.pyplot as plt

machine  = SlotMachine('simpleReward')

n = pow(10,4)
x_axis = []
y_axis = []
for i in range(1,n):
    estimeted_variace = estimateVariance(machine,n,10)
    x_axis.append(i)
    y_axis.append(estimeted_variace)

plt.plot(x_axis,y_axis,'b-')
plt.savefig('simpleReward.png')
plt.show()

