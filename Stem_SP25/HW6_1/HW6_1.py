#region imports
from ResistorNetwork import ResistorNetwork, ResistorNetwork_2
#endregion

def main():
    print("Network 1:")
    Net = ResistorNetwork()
    Net.BuildNetworkFromFile("ResistorNetwork.txt")
    try:
        IVals = Net.AnalyzeCircuit()
        print("Network 1 currents:", IVals)
    except Exception as e:
        print(f"Error in Network 1: {e}")

    print("\nNetwork 2:")
    Net_2 = ResistorNetwork_2()
    try:
        Net_2.BuildNetworkFromFile("ResistorNetwork_2.txt")
        print("Network 2 file loaded successfully")
        IVals_2 = Net_2.AnalyzeCircuit()
        print("Network 2 currents:", IVals_2)
    except Exception as e:
        print(f"Error in Network 2: {e}")

if __name__ == "__main__":
    main()