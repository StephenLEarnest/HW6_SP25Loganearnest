import numpy as np
from scipy.interpolate import griddata

class steam:
    def __init__(self, pressure, T=None, x=None, v=None, h=None, s=None, name=None):
        self.p = pressure  # kPa
        self.T = T  # °C
        self.x = x  # Quality
        self.v = v  # m³/kg
        self.h = h  # kJ/kg
        self.s = s  # kJ/(kg·K)
        self.name = name
        self.region = None
        if T is None and x is None and v is None and h is None and s is None:
            return
        else:
            self.calc()

    def calc(self):
        # Load saturated properties (T, P in bar, hf, hg, sf, sg, vf, vg)
        ts, ps, hfs, hgs, sfs, sgs, vfs, vgs = np.loadtxt('saturated_steam.txt', skiprows=1, unpack=True)  # #$JES MISSING CODE$
        # Load superheated properties (T, h, s, P in kPa)
        tcol, hcol, scol, pcol = np.loadtxt('superheated_steam.txt', skiprows=1, unpack=True)  # #$JES MISSING CODE$

        R = 8.314 / (18 / 1000)  # J/(mol·K) / (kg/mol) = kJ/(kg·K)
        Pbar = self.p / 100  # Convert kPa to bar for saturated table

        # Saturated properties at self.p
        Tsat = float(griddata(ps, ts, Pbar))
        hf = float(griddata(ps, hfs, Pbar))
        hg = float(griddata(ps, hgs, Pbar))
        sf = float(griddata(ps, sfs, Pbar))
        sg = float(griddata(ps, sgs, Pbar))
        vf = float(griddata(ps, vfs, Pbar))
        vg = float(griddata(ps, vgs, Pbar))

        self.hf = hf

        # Determine region and properties
        if self.T is not None:
            if self.T > Tsat:
                self.region = 'Superheated'
                self.h = float(griddata((pcol, tcol), hcol, (self.p, self.T)))  # #$JES MISSING CODE$
                self.s = float(griddata((pcol, tcol), scol, (self.p, self.T)))  # #$JES MISSING CODE$
                self.x = 1.0
                TK = self.T + 273.14
                self.v = R * TK / (self.p * 1000)  # Ideal gas approximation
            else:
                self.region = 'Saturated'
                self.x = (self.T - Tsat) / (hg - hf) if self.T < Tsat else 1.0  # Simplified, assuming T < Tsat is rare
                self.h = hf + self.x * (hg - hf)
                self.s = sf + self.x * (sg - sf)
                self.v = vf + self.x * (vg - vf)
        elif self.x is not None:
            self.region = 'Saturated'
            self.T = Tsat
            self.h = hf + self.x * (hg - hf)
            self.s = sf + self.x * (sg - sf)
            self.v = vf + self.x * (vg - vf)
        elif self.h is not None:
            self.x = (self.h - hf) / (hg - hf)
            if self.x <= 1.0:
                self.region = 'Saturated'
                self.T = Tsat
                self.s = sf + self.x * (sg - sf)
                self.v = vf + self.x * (vg - vf)
            else:
                self.region = 'Superheated'
                self.T = float(griddata((pcol, hcol), tcol, (self.p, self.h)))  # #$JES MISSING CODE$
                self.s = float(griddata((pcol, hcol), scol, (self.p, self.h)))  # #$JES MISSING CODE$
        elif self.s is not None:
            self.x = (self.s - sf) / (sg - sf)
            if self.x <= 1.0:
                self.region = 'Saturated'
                self.T = Tsat
                self.h = hf + self.x * (hg - hf)
                self.v = vf + self.x * (vg - vf)
            else:
                self.region = 'Superheated'
                self.T = float(griddata((pcol, scol), tcol, (self.p, self.s)))  # #$JES MISSING CODE$
                self.h = float(griddata((pcol, scol), hcol, (self.p, self.s)))  # #$JES MISSING CODE$

    def print(self):
        print('Name: ', self.name)
        if self.x < 0.0:
            print('Region: compressed liquid')
        else:
            print('Region: ', self.region)
        print('p = {:0.2f} kPa'.format(self.p))
        if self.x >= 0.0:
            print('T = {:0.1f} degrees C'.format(self.T))
        print('h = {:0.2f} kJ/kg'.format(self.h))
        if self.x >= 0.0:
            print('s = {:0.4f} kJ/(kg K)'.format(self.s))
            if self.region == 'Saturated':
                print('v = {:0.6f} m^3/kg'.format(self.v))
                print('x = {:0.4f}'.format(self.x))
        print()