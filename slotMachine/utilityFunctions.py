from gambler import * 
from copy import deepcopy
def estimateExpectedValue(machine,n,budget):
    games = 0
    iteration = 0
    while(iteration < n):
        g_games = Gambler(budget).gamesUntilZero(machine)
        games += g_games
        iteration += 1
    return games/n

def estimateVariance(machineOBJ,n,budget):
    M1 = 0
    M2 = 0
    iteration = 0
    variance = 0
    while(iteration < n):
        machine =  deepcopy(machineOBJ)
        sample = Gambler(budget).gamesUntilZero(machine)
        M1 += sample
        M2 += pow(sample,2)
        iteration += 1
    variance = ((M2 - pow(M1,2)/n) / (n-1)) / n
    mean = M1/n
    return variance,mean
    
def bidReturn(machineOBJ,n,budget,games):
    bidreturn = []
    for i in range(n):
        machine =  deepcopy(machineOBJ)
        gambler = Gambler(budget)
        gambler.play(machine,games)
        bidreturn.append(gambler.getBidReturn())
    return bidreturn

def estimateVarianceMeanPrize(machineOBJ,n,budget = pow(10,20)):
    M1 = 0
    M2 = 0
    variance = 0
    p = 0
    for iteration in range(n):
        machine =  deepcopy(machineOBJ)
        g = Gambler(budget).play(machine,n)
        sample = machine.getMeanPrize()
        if(sample > 0):
            p += 1
        M1 += sample
        M2 += pow(sample,2)
    if (M1 > 0 ):     
        variance = ((M2 - pow(M1,2)/p) / (p-1)) / p
        mean = M1/p
        return variance,mean
    else:
        return 10 , 0

def gamblersWallet(machineOBJ,players,budget,games):
    iteration = 0
    wallets = []
    while (iteration < players):
        machine =  deepcopy(machineOBJ)
        g = Gambler(budget)
        g.play(machine,games)
        wallets.append(g.getWallet())
        iteration += 1
    return wallets