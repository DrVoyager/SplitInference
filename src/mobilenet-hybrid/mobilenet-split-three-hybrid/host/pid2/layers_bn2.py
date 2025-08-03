from reluLayer import ReluLayer
from convLayer2 import ConvLayer
from batchnormalLayer2 import BatchNormalLayer

class Layers_Bn:
    def __init__(self, nInputNum, nOutputNum, nInputWidth, nStride, fileNum):
        # These class references presume the existence of ConvLayer, BatchNormalLayer, and ReluLayer in Python,
        # each matching the behavior of your original C++ classes.
        self.m_ConvlayerDw = ConvLayer(fileNum, nInputNum, nOutputNum, nInputWidth, 3, 1, nStride)
        self.m_ConvDwBN = BatchNormalLayer(fileNum, nOutputNum, nInputWidth // nStride)
        self.m_RelulayerDw = ReluLayer(self.m_ConvDwBN.GetOutputSize())

    def __del__(self):
        pass

    def forward(self, pfInput):
        
        self.m_ConvlayerDw.forward(pfInput)
        self.m_ConvDwBN.forward(self.m_ConvlayerDw.GetOutput())
        self.m_RelulayerDw.forward(self.m_ConvDwBN.GetOutput())

    def GetOutput(self):
        return self.m_RelulayerDw.GetOutput()
