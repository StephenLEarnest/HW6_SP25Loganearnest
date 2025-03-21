from Fluid import Fluid
from Pipe import Pipe
from Loop import Loop
from PipeNetwork import PipeNetwork

def main():
    water = Fluid(mu=0.00089, rho=1000)  # #$JES MISSING CODE$
    roughness = 0.00025
    PN = PipeNetwork()  # #$JES MISSING CODE$
    PN.pipes.append(Pipe('a', 'b', 250, 300, roughness, water))
    PN.pipes.append(Pipe('a', 'c', 100, 200, roughness, water))
    PN.pipes.append(Pipe('b', 'e', 100, 200, roughness, water))
    PN.pipes.append(Pipe('c', 'd', 125, 200, roughness, water))
    PN.pipes.append(Pipe('c', 'f', 100, 150, roughness, water))
    PN.pipes.append(Pipe('d', 'e', 125, 200, roughness, water))
    PN.pipes.append(Pipe('d', 'g', 100, 150, roughness, water))
    PN.pipes.append(Pipe('e', 'h', 100, 150, roughness, water))
    PN.pipes.append(Pipe('f', 'g', 125, 250, roughness, water))
    PN.pipes.append(Pipe('g', 'h', 125, 250, roughness, water))
    PN.buildNodes()
    PN.getNode('a').extFlow = 60
    PN.getNode('d').extFlow = -30
    PN.getNode('f').extFlow = -15
    PN.getNode('h').extFlow = -15
    PN.loops.append(Loop('A', [PN.getPipe('a-b'), PN.getPipe('b-e'), PN.getPipe('d-e'), PN.getPipe('c-d'), PN.getPipe('a-c')]))
    PN.loops.append(Loop('B', [PN.getPipe('c-d'), PN.getPipe('d-g'), PN.getPipe('f-g'), PN.getPipe('c-f')]))
    PN.loops.append(Loop('C', [PN.getPipe('d-e'), PN.getPipe('e-h'), PN.getPipe('g-h'), PN.getPipe('d-g')]))
    PN.findFlowRates()
    PN.printPipeFlowRates()
    print()
    print('Check node flows:')
    PN.printNetNodeFlows()
    print()
    print('Check loop head loss:')
    PN.printLoopHeadLoss()

if __name__ == "__main__":
    main()