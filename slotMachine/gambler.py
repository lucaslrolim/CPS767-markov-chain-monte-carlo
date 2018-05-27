from slotMachine import * 

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
