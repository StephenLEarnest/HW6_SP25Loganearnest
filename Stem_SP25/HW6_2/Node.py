class Node:
    def __init__(self, Name='a', Pipes=[], ExtFlow=0):
        self.name = Name
        self.pipes = Pipes
        self.extFlow = ExtFlow

    def getNetFlowRate(self):
        Qtot = self.extFlow  # #$JES MISSING CODE$ - Start with external flow (L/s)
        for p in self.pipes:
            Qtot += p.getFlowIntoNode(self.name)
        return Qtot