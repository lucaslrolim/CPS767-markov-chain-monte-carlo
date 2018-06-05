import random
import math
from aliasMethod import *
class SlotMachine():
    jackpot = 0
    def __init__(self,reward_function,houseEdge,figures = 3,prizeCriteria = 'eq',bid = 1, slots = 4):
        self.reward_function = reward_function
        self.bid = bid
        self.prizeCriteria = prizeCriteria
        self.figures = figures
        self.states = list(range(1,figures+1))
        self.statesCombination = math.factorial(slots)
        self.slots = slots
        self.setPrizes()
        self.setProbabilities(houseEdge)
        self.j,self.q = alias_setup(self.prizeStatesProb)
        self.prizesConceived = []
        
    def setPrizes(self):
        self.totalPrize = 0
        self.prize = {}
        for figure in self.states:
            self.prize[figure] = self.applyPrizeCriteria(figure)
            self.totalPrize += self.prize[figure]

    def applyPrizeCriteria(self,figure):
        if(self.prizeCriteria == 'bx'):
            p = 0
            temp = self.figures
            prob = self.figures*(1+self.figures)/2
            for i in (self.states):
                p += i * temp
                temp -= 1
            self.mean_prize = - (1/prob) * p * self.bid
            print('MEAN PRIZE ',self.mean_prize)
            return figure * self.bid
        if(self.prizeCriteria == 'eq'):
            self.mean_prize = - 2 * self.bid
            return 2*self.bid
            
    def setProbabilities(self,houseEdge):
        self.prizeStatesProb = []
        prob = 1 / (self.figures*(1+self.figures)/2)
        index = 1
        for figure in reversed(self.states):
            self.prizeStatesProb.append(figure * prob) 
            index += 1
        self.probabilityToWin = (houseEdge - self.mean_prize)/(self.bid - self.mean_prize)

    def EdgeReward(self):
        u = random.uniform(0, 1)
        if(u < self.probabilityToWin):
            self.jackpot += self.bid
            return -self.bid
        else:
            figure = self.states[alias_draw(self.j,self.q)]
            self.jackpot -= self.prize[figure]
            self.prizesConceived.append(self.prize[figure])
            return self.prize[figure]

    def getJeckpot(self):
        return self.jackpot

    def generateGame(self):
        sample = []
        for i in range(self.slots):
            u = random.randint(0, self.figures)
            sample.append(self.states[u-1])
        return sample

    def play(self):
        rewardFunction = getattr(self, self.reward_function)
        reward = rewardFunction()
        return reward

    def getPrizesConceived(self):
        return self.prizesConceived
        
    def getMeanPrize(self):
        if(len(self.prizesConceived) != 0):
            mp = sum(self.prizesConceived)/len(self.prizesConceived)
        else:
            mp = 0
        return mp
    