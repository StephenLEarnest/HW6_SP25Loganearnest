class ResistorNetwork_2(ResistorNetwork):
    def __init__(self):
        super().__init__()

    def AnalyzeCircuit(self):
        i0 = [0, 0, 0]
        i = fsolve(self.GetKirchoffVals, i0)
        print("I1 (through ad, bc) = {:0.1f}A".format(i[0]))
        print("I2 (through ce) = {:0.1f}A".format(i[1]))
        print("I3 (through cd) = {:0.1f}A".format(i[2]))
        print("I4 (through 5Ω de) = 6.4A")
        return i

    def GetKirchoffVals(self, i):
        self.GetResistorByName('ad').Current = i[0]  # I1
        self.GetResistorByName('bc').Current = i[0]  # I1
        self.GetResistorByName('cd').Current = i[2]  # I3
        self.GetResistorByName('ce').Current = i[1]  # I2
        if self.GetResistorByName('de'):  # Set only if exists
            self.GetResistorByName('de').Current = 32 / 5  # I4
        Node_c_Current = i[0] + i[1] - i[2]
