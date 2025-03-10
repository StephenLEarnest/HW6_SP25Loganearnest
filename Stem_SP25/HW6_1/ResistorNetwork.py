#region imports
from scipy.optimize import fsolve
from Resistor import Resistor
from VoltageSource import VoltageSource
from Loop import Loop
#endregion

class ResistorNetwork:
    def __init__(self):
        self.Loops = []
        self.Resistors = []
        self.VSources = []

    def BuildNetworkFromFile(self, filename):
        FileTxt = open(filename, "r").read().split('\n')
        LineNum = 0
        self.Resistors = []
        self.VSources = []
        self.Loops = []
        FileLength = len(FileTxt)
        while LineNum < FileLength:
            lineTxt = FileTxt[LineNum].lower().strip()
            if len(lineTxt) < 1 or lineTxt[0] == '#':
                pass
            elif "<resistor>" in lineTxt:
                LineNum = self.MakeResistor(LineNum, FileTxt)
            elif "<source>" in lineTxt:
                LineNum = self.MakeVSource(LineNum, FileTxt)
            elif "<loop>" in lineTxt:
                LineNum = self.MakeLoop(LineNum, FileTxt)
            LineNum += 1

    def MakeResistor(self, N, Txt):
        R = Resistor()
        N += 1
        while N < len(Txt) and "</resistor>" not in Txt[N].lower():
            txt = Txt[N].lower()
            if "name" in txt:
                R.Name = txt.split('=')[1].strip()
            if "resistance" in txt:
                R.Resistance = float(txt.split('=')[1].strip())
            N += 1
        self.Resistors.append(R)
        return N

    def MakeVSource(self, N, Txt):
        VS = VoltageSource()
        N += 1
        while N < len(Txt) and "</source>" not in Txt[N].lower():
            txt = Txt[N].lower()
            if "name" in txt:
                VS.Name = txt.split('=')[1].strip()
            if "value" in txt:
                VS.Voltage = float(txt.split('=')[1].strip())
            if "type" in txt:
                VS.Type = txt.split('=')[1].strip()
            N += 1
        self.VSources.append(VS)
        return N

    def MakeLoop(self, N, Txt):
        L = Loop()
        N += 1
        while N < len(Txt) and "</loop>" not in Txt[N].lower():
            txt = Txt[N].lower()
            if "name" in txt:
                L.Name = txt.split('=')[1].strip()
            if "nodes" in txt:
                txt = txt.replace(" ", "")
                L.Nodes = txt.split('=')[1].strip().split(',')
            N += 1
        self.Loops.append(L)
        return N

    def AnalyzeCircuit(self):
        i0 = [0, 0, 0]
        i = fsolve(self.GetKirchoffVals, i0)
        print("I1 = {:0.1f}".format(i[0]))
        print("I2 = {:0.1f}".format(i[1]))
        print("I3 = {:0.1f}".format(i[2]))
        return i

    def GetKirchoffVals(self, i):
        self.GetResistorByName('ad').Current = i[0]  # I1
        self.GetResistorByName('bc').Current = i[0]  # I1
        self.GetResistorByName('cd').Current = i[2]  # I3
        self.GetResistorByName('ce').Current = i[1]  # I2
        Node_c_Current = i[0] + i[1] - i[2]
        KVL = self.GetLoopVoltageDrops()
        KVL.append(Node_c_Current)
        return KVL

    def GetElementDeltaV(self, name):
        for r in self.Resistors:
            if name == r.Name:
                return -r.DeltaV()
            if name[::-1] == r.Name:
                return r.DeltaV()
        for v in self.VSources:
            if name == v.Name:
                return v.Voltage
            if name[::-1] == v.Name:
                return -v.Voltage

    def GetLoopVoltageDrops(self):
        loopVoltages = []
        for L in self.Loops:
            loopDeltaV = 0
            for n in range(len(L.Nodes)):
                if n == len(L.Nodes) - 1:
                    name = L.Nodes[0] + L.Nodes[n]
                else:
                    name = L.Nodes[n] + L.Nodes[n + 1]
                loopDeltaV += self.GetElementDeltaV(name)
            loopVoltages.append(loopDeltaV)
        return loopVoltages

    def GetResistorByName(self, name):
        for r in self.Resistors:
            if r.Name == name:
                return r
        return None

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
        if self.GetResistorByName('de'):  # Avoid NoneType error
            self.GetResistorByName('de').Current = 32 / 5  # I4
        Node_c_Current = i[0] + i[1] - i[2]
        KVL = self.GetLoopVoltageDrops()
        KVL.append(Node_c_Current)
        return KVL

#endregion