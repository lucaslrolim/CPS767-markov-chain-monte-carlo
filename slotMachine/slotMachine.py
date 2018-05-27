import random
import math

class SlotMachine():
    figures = 3
    jackpot = 0
    def __init__(self,reward_function,houseEdge,slots = 3,prizeCriteria = 'eq',bid = 1):
        self.reward_function = reward_function
        self.bid = bid
        self.prizeCriteria = prizeCriteria
        self.states = list(range(1,self.figures+1))
        self.statesCombination = math.factorial(slots)
        self.slots = slots
        self.setPrizes()
        self.setProbabilities(houseEdge)

    def setPrizes(self):
        self.totalPrize = 0
        self.prize = {}
        for figure in self.states:
            self.prize[figure] = self.applyPrizeCriteria(figure)
            self.totalPrize += self.prize[figure]

    def applyPrizeCriteria(self,figure):
        if(self.prizeCriteria == '10x'):
            return figure * 10
        if(self.prizeCriteria == 'eq'):
            return self.bid * 5
            
    def setProbabilities(self,houseEdge):
        mean_prize = -5
        self.probabilityToWin = (houseEdge - mean_prize)/(self.bid - mean_prize)
        self.prizeStatesProb = {}
        for figure in self.states:
            index = len(self.states) + 1 - figure
            self.prizeStatesProb[figure] = self.prize[index]

    def EdgeReward(self):
        u = random.uniform(0, 1)
        if(u < self.probabilityToWin):
            self.jackpot += self.bid
            return -self.bid
        else:
            r_state = random.uniform(0, 1)
            figure = 1 
            s =  self.prizeStatesProb[figure]
            while(s <= self.totalPrize * r_state):
                s += self.prizeStatesProb[figure]
                figure += 1
            self.jackpot -= self.prize[figure]
            return self.prize[figure]

    def getJeckpot(self):
        return self.jackpot

    def generateGame(self):
        sample = []
        for i in range(self.slots):
            u = random.randint(0, self.figures)
            sample.append(self.states[u-1])
        return sample

    def simpleReward(self):
        slotResult = self.generateGame()
        rewardResult = -self.bid
        for figure in slotResult:
            if(slotResult.count(figure) == self.slots):
                rewardResult += figure * 2 * self.bid
                break
            # if(slotResult.count(figure) == self.slots - 1):
            #     rewardResult += figure  * bid
            #     break
        return rewardResult

    def play(self):
        rewardFunction = getattr(self, self.reward_function)
        reward = rewardFunction()
        return reward

class Gambler():
    motivation = 1
    games = 0
    def __init__(self,budget):
        self.wallet = budget
    def gamesUntilZero(self,machine):
        while(self.wallet > 0 and self.motivation > 0):
            reward = machine.play()
            self.wallet += reward
            self.games += 1
        return self.games
    def play(self,machine,numberOfPlays):
        while(self.games < numberOfPlays):
            reward = machine.play()
            self.wallet += reward
            self.games += 1
        return self.wallet
