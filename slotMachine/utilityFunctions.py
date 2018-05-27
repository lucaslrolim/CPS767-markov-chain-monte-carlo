from gambler import * 

def estimateExpectedValue(machine,n,budget):
    games = 0
    iteration = 0
    while(iteration < n):
        g_games = Gambler(budget).play(machine)
        games += g_games
        iteration += 1
    return games/n

def estimateVariance(machine,n,budget):
    M1 = 0
    M2 = 0
    iteration = 0 
    while(iteration < n):
        sample = Gambler(budget).gamesUntilZero(machine)
        M1 += sample
        M2 += pow(sample,2)
        iteration += 1
    # removind vies
    variance = (M2 - pow(M1,2)/n) / (n-1) 
    return variance