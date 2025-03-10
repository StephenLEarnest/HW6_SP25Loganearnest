import math
import numpy as np
import random as rnd
from scipy.optimize import fsolve
from Fluid import Fluid

class Pipe:
    def __init__(self, Start='A', End='B', L=100, D=200, r=0.00025, fluid=Fluid()):
        self.startNode = min(Start, End)
        self.endNode = max(Start, End)
        self.length = L
        self.r = r
        self.fluid = fluid
        self.d = D / 1000.0
        self.relrough = self.r / self.d
        self.A = math.pi / 4.0 * self.d ** 2
        self.Q = 10  # L/s
        self.vel = self.V()
        self.reynolds = self.Re()

    def V(self):
        self.vel = (self.Q / 1000) / self.A  # #$JES MISSING CODE$ - Convert L/s to m³/s
        return self.vel

    def Re(self):
        self.reynolds = (self.fluid.rho * self.V() * self.d) / self.fluid.mu  # #$JES MISSING CODE$
        return self.reynolds

    def FrictionFactor(self):
        Re = self.Re()
        rr = self.relrough
        def CB():
            cb = lambda f: 1 / (f ** 0.5) + 2.0 * np.log10(rr / 3.7 + 2.51 / (Re * f ** 0.5))
            result = fsolve(cb, (0.01))
            return result[0]
        def lam():
            return 64 / Re
        if Re >= 4000:
            return CB()
        if Re <= 2000:
            return lam()
        CBff = CB()
        Lamff = lam()
        mean = Lamff + ((Re - 2000) / (4000 - 2000)) * (CBff - Lamff)
        sig = 0.2 * mean
        return rnd.normalvariate(mean, sig)

    def frictionHeadLoss(self):
        g = 9.81
        ff = self.FrictionFactor()
        hl = ff * (self.length / self.d) * (self.V() ** 2) / (2 * g)  # #$JES MISSING CODE$ - Head loss in m
        return hl

    def getFlowHeadLoss(self, s):
        nTraverse = 1 if s == self.startNode else -1
        nFlow = 1 if self.Q >= 0 else -1
        return nTraverse * nFlow * self.frictionHeadLoss()

    def Name(self):
        return self.startNode + '-' + self.endNode

    def oContainsNode(self, node):
        return self.startNode == node or self.endNode == node

    def printPipeFlowRate(self):
        print('The flow in segment {} is {:.4f} m^3/s'.format(self.Name(), self.Q / 1000))  # Convert L/s to m³/s

    def getFlowIntoNode(self, n):
        if n == self.startNode:
            return -self.Q
        return self.Q