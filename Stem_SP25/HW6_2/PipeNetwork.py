from scipy.optimize import fsolve
import numpy as np
from Fluid import Fluid
from Node import Node

class PipeNetwork:
    def __init__(self, Pipes=[], Loops=[], Nodes=[], fluid=Fluid()):
        self.loops = Loops
        self.nodes = Nodes
        self.Fluid = fluid
        self.pipes = Pipes

    def findFlowRates(self):
        N = len(self.nodes) + len(self.loops)  # 8 nodes + 3 loops = 11 equations
        Q0 = np.full(N, 10)  # Initial guess
        def fn(q):
            for i in range(len(self.pipes)):
                self.pipes[i].Q = q[i]  # #$JES MISSING CODE$ - Assign flows (L/s)
            L = self.getNodeFlowRates()  # #$JES MISSING CODE$ - Node flows
            L += self.getLoopHeadLosses()  # #$JES MISSING CODE$ - Loop head losses
            return L
        FR = fsolve(fn, Q0)
        for i, p in enumerate(self.pipes):
            p.Q = FR[i]
        return FR

    def getNodeFlowRates(self):
        return [n.getNetFlowRate() for n in self.nodes]

    def getLoopHeadLosses(self):
        return [l.getLoopHeadLoss() for l in self.loops]

    def getPipe(self, name):
        for p in self.pipes:
            if name == p.Name():
                return p

    def getNodePipes(self, node):
        return [p for p in self.pipes if p.oContainsNode(node)]

    def nodeBuilt(self, node):
        return any(n.name == node for n in self.nodes)

    def getNode(self, name):
        for n in self.nodes:
            if n.name == name:
                return n

    def buildNodes(self):
        for p in self.pipes:
            if not self.nodeBuilt(p.startNode):
                self.nodes.append(Node(p.startNode, self.getNodePipes(p.startNode)))
            if not self.nodeBuilt(p.endNode):
                self.nodes.append(Node(p.endNode, self.getNodePipes(p.endNode)))

    def printPipeFlowRates(self):
        for p in self.pipes:
            p.printPipeFlowRate()

    def printNetNodeFlows(self):
        for n in self.nodes:
            print('net flow into node {} is {:.2f}'.format(n.name, n.getNetFlowRate()))

    def printLoopHeadLoss(self):
        for l in self.loops:
            print('head loss for loop {} is {:.2f}'.format(l.name, l.getLoopHeadLoss()))