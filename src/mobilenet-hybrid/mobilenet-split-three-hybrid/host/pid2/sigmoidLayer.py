class SigmoidLayer:
    def __init__(self, nInputSize):
        self.m_nInputSize = nInputSize
        self.m_pfOutput = [0.0] * self.m_nInputSize

    def __del__(self):
        pass

    def forward(self, pfInput):
        import math
        for i in range(self.m_nInputSize):
            self.m_pfOutput[i] = 1.0 / (1.0 + math.exp(-pfInput[i]))

    def GetOutput(self):
        return self.m_pfOutput
