class GlobalPoolLayer:
    def __init__(self, nOutputNum, nInputWidth):
        self.m_nOutputNum = nOutputNum
        self.m_nInputWidth = nInputWidth
        self.m_nPoolWidth = nInputWidth  # as in the original code
        self.m_nOutputWidth = 1
        self.m_nOutputSize = self.m_nOutputWidth * self.m_nOutputWidth
        self.m_nInputSize = self.m_nInputWidth * self.m_nInputWidth

        # Allocate memory (lists in Python)
        self.m_pfOutput = [0.0] * (self.m_nOutputNum * self.m_nOutputSize)

    def __del__(self):
        # Python GC handles cleanup; placeholder
        pass

    def forward(self, pfInput):
        
        for nOutmapIndex in range(self.m_nOutputNum):
            nOutputIndex = nOutmapIndex * self.m_nOutputSize
            nInputIndexStart = nOutmapIndex * self.m_nInputSize

            fSum = 0.0
            for m in range(self.m_nPoolWidth):
                for n in range(self.m_nPoolWidth):
                    nInputIndex = nInputIndexStart + m * self.m_nInputWidth + n
                    fSum += pfInput[nInputIndex]

            self.m_pfOutput[nOutputIndex] = fSum / float(self.m_nInputSize)

    def GetOutput(self):
        return self.m_pfOutput
