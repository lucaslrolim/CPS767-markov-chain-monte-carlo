from utilityFunctions import * 
import random


machine  = SlotMachine('EdgeReward',0.1,4,'bx',1)

## N players playing 10 times on a 0.1 house advantage machine
n_players = pow(10,4)
budget = 10
players = [Gambler(budget) for i in range(n_players)]
for g in players:
    g.play(machine,budget)

jp = machine.getJeckpot()
print("TOTAL BIDS ", n_players * budget )
print('Jackpot', jp, "   % of bids: ",(jp/(n_players * budget)))
print('ERROR', jp/(n_players*10) )

sumPrize = 0
prizesLen = 0 

print("MEAN PRIZE: ", machine.getMeanPrize())

