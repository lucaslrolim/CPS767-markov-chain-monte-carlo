from slotMachine import * 

class Gambler():
    motivation = 1
    def __init__(self,budget):
        self.wallet = budget
        self.prizesReceived = []
        self.games = 0
        self.loses = 0
        self.moneyLose = []
    def gamesUntilZero(self,machine):
        while(self.wallet > 0 and self.motivation > 0):
            reward = machine.play()
            self.wallet += reward
            self.games += 1
        return self.games
    def play(self,machine,numberOfPlays):
        while(self.games < numberOfPlays and self.wallet > 0):
            reward = machine.play()
            self.wallet += reward
            if(reward > 0):
                self.prizesReceived.append(reward)
            else:
                self.moneyLose.append(reward)
            self.games += 1
        return self.wallet
    def getPrizeHistory(self):
        return self.prizesReceived
    def getWallet(self):
        return self.wallet
    def getBidReturn(self):
        p_win  =  len(self.prizesReceived)  / (len(self.prizesReceived) + len(self.moneyLose))
        if(len(self.prizesReceived) > 0):
            meanPrize = (sum(self.prizesReceived)/len(self.prizesReceived))
        else:
            meanPrize = 0
        if(len(self.moneyLose) > 0):
            meanLoss = (sum(self.moneyLose)/len(self.moneyLose))
        else:
            meanLoss = 0
        bidReturn = p_win * meanPrize  + (1-p_win) * meanLoss
        return bidReturn