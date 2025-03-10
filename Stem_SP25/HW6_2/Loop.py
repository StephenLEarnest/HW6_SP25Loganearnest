class Loop:
    def __init__(self, Name='A', Pipes=[]):
        self.name = Name
        self.pipes = Pipes

    def getLoopHeadLoss(self):
        deltaP = 0
        startNode = self.pipes[0].startNode
        for p in self.pipes:
            phl = p.getFlowHeadLoss(startNode)
            deltaP += phl
            startNode = p.endNode if startNode != p.endNode else p.startNode
        return deltaP