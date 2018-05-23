import numpy as np
import math
import random as rm

class RandomWalk():
    """Creates a Markov Chain structure and do random walk"""
    def __init__(self,numberOfNodes, lazy = 0):
        self.lazy = lazy
        self.numberOfNodes = numberOfNodes

        self.transitions = []
        self.currentState = 0
        self.stationaryDistribution = []
        self.pi = [0] * numberOfNodes
        self.pi[self.currentState] = 1

        self.states = list(range(numberOfNodes))
        self.generateTransitionMatrix()

    def changeState(self):
        self.currentState = np.random.choice(self.states,replace = True, p = self.transitions[self.currentState])
        self.pi = np.matmul(self.pi, self.transitions)

    def getTransitions(self):
        return self.transitions
    def getStates(self):
        return self.states
    def setCurrentState(self,state):
        self.currentState = state
        self.pi = [0] * self.currentState
        self.pi[self.currentState] = 1
    def getCurrentState(self):
        return self.currentState
    def setStationaryDistribution(self):
        pass
    def getStationaryDistribution(self):
        return self.stationaryDistribution
    def getStateMatrix(self):
        return self.pi

    def calculateVariation(self,time):
        if(self.stationaryDistribution == None):
            print("Please set the stationary distribution first")
            return -1
        t = 0
        while t < time:
            self.changeState()
            variation = 0
            for i in range(len(self.pi)):
                variation += math.fabs (self.stationaryDistribution[i] - self.pi[i])
            variation  = variation/2
            t += 1
        return variation

    def calculateMixingTime(self,eps):
        variation = np.inf 
        mixingTime = 0
        while(variation > eps):
            variation = self.calculateVariation(1)
            mixingTime += 1
        return mixingTime

    def generateTransitionMatrix(self):
        pass

class RingGraphRW(RandomWalk):
    """Random Walk on a ring graph structure"""
    def generateTransitionMatrix(self): 
        for i in range(0,self.numberOfNodes):
            stateTransitions = [0] * self.numberOfNodes
            stateTransitions[i] = self.lazy
            if(i != 0 and i != self.numberOfNodes - 1):
                stateTransitions[i+1] = (1 - self.lazy)/2
                stateTransitions[i-1] = (1 - self.lazy)/2
            elif(i == 0):
                stateTransitions[i+1] = (1 - self.lazy)/2
                stateTransitions[self.numberOfNodes-1] = (1 - self.lazy)/2
            elif(i == self.numberOfNodes - 1):
                stateTransitions[i-1] = (1 - self.lazy)/2
                stateTransitions[0] = (1 - self.lazy)/2
            
            self.transitions.append(stateTransitions)
            self.setStationaryDistribution()

    def setStationaryDistribution(self):
        self.stationaryDistribution = [1.0/self.numberOfNodes] * self.numberOfNodes

class BinaryTreeGraphRW(RandomWalk):
    """Random Walk on a Binary Tree graph structure"""
    def generateTransitionMatrix(self): 
            for i in range(1,self.numberOfNodes+1):
                stateTransitions = [0] * self.numberOfNodes
                stateTransitions[i-1] = self.lazy

                if(i == 1):
                    stateTransitions[1] = (1 - self.lazy)/2
                    stateTransitions[2] = (1 - self.lazy)/2
                elif(i % 2 == 0):
                    j = int(i/2) - 1
                else:
                    j = int((i-1)/2) -1

                if(((2*i)+1) <= self.numberOfNodes and i != 1):
                    stateTransitions[j] = (1 - self.lazy)/3
                    stateTransitions[(2*i) -1] = (1 - self.lazy)/3
                    stateTransitions[(2*i)] = (1 - self.lazy)/3
                elif(((2*i)) <= self.numberOfNodes and i !=1):
                    stateTransitions[j] = (1 - self.lazy)/2
                    stateTransitions[(2*i) -1] = (1 - self.lazy)/2
                elif(i != 1):
                    stateTransitions[j] = (1 - self.lazy)

                self.transitions.append(stateTransitions)
            self.setStationaryDistribution()

    def setStationaryDistribution(self):
        self.stationaryDistribution = []
        for i in range(0,self.numberOfNodes):
            g = -1
            for j in range(self.numberOfNodes):
                if(self.transitions[j][i] > 0):
                    g +=1
            self.stationaryDistribution.append(g/(2*(self.numberOfNodes-1)))

class GridGraphRW(RandomWalk):
    """Random Walk on a Grid graph structure"""
    neighbors = None
    def mapNeightbors(self):
        valid_values = list(range(self.numberOfNodes))
        v = 0
        neighbors = [[] for i in range(self.numberOfNodes)]
        n_rows = int(math.sqrt(self.numberOfNodes))
        rows = []
        for i in range(n_rows):
            r = list(range(v,v+n_rows))
            rows.append(r)
            v = v+n_rows
        for line in rows:
            for element in line:
                if(line.index(element) != 0):
                    neighbors[element].append(line[line.index(element) - 1])
                if (line.index(element) != len(line)-1):
                    neighbors[element].append(line[line.index(element) + 1])
            if(rows.index(line) != 0):
                for element in line:
                    neighbors[element].append(rows[rows.index(line) - 1][line.index(element)])
            if(rows.index(line) != len(rows)-1):
                for element in line:
                    neighbors[element].append(rows[rows.index(line) + 1][line.index(element)])
        print("neighbors set")
        return neighbors

    def generateTransitionMatrix(self):
        neighbors =  self.mapNeightbors()
        self.neighbors = neighbors
        for i in range(0,self.numberOfNodes):
            stateTransitions = [0] * self.numberOfNodes
            stateTransitions[i] = self.lazy
            for j in neighbors[i]:
                stateTransitions[int(j)] = (1 - self.lazy ) / len(neighbors[i])
            self.transitions.append(stateTransitions)
        self.setStationaryDistribution()

    def setStationaryDistribution(self):
        self.stationaryDistribution = []
        g_total = 0
        neighbors = self.neighbors
        for i in range(0,self.numberOfNodes):
            g_total += len(neighbors[i])
        for j in range(self.numberOfNodes):
            self.stationaryDistribution.append(len(neighbors[j])/g_total)

