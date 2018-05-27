from utilityFunctions import * 

budget = 40
g = Gambler(budget)

machine  = SlotMachine('EdgeReward',0.1)

n = pow(10,4)
print(g.play(machine,10))
print(machine.getJeckpot())
#print('Variance: ', estimateVariance(machine,n,budget))
