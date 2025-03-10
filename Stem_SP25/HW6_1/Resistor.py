class Resistor:
    def __init__(self, R=1.0, i=0.0, name='ab'):
        self.Resistance = R  # Assign resistance
        self.Current = i     # Assign current
        self.Name = name     # Assign name
        # Note: self.DeltaV() is a method, not an attribute; no assignment needed here

    def DeltaV(self):
        self.V = self.Current * self.Resistance
        return self.V