class ReluLayer:
    def __init__(self, nInputSize):
        self.m_nInputSize = nInputSize
        self.m_pfOutput = [0.0] * self.m_nInputSize

    def __del__(self):
        pass

    def forward(self, pfInput):
        
        for i in range(self.m_nInputSize):
            if pfInput[i] > 0:
                self.m_pfOutput[i] = pfInput[i]
            else:
                self.m_pfOutput[i] = 0

    def GetOutput(self):
        return self.m_pfOutput
