from utilityFunctions import * 
import random


machine  = SlotMachine('EdgeReward',0,5,'bx',1)

## N players playing 10 times on a 0.1 house advantage machine
n_players = pow(10,5)
budget = 100
players = [Gambler(budget) for i in range(n_players)]
for g in players:
    u  = random.randint(0, budget)
    g.play(machine,10)

jp = machine.getJeckpot()
print('Jackpot', jp)
print('ERROR', jp/(n_players*10) )

sumPrize = 0
prizesLen = 0 

print("MEAN PRIZE: ", machine.getMeanPrize())

