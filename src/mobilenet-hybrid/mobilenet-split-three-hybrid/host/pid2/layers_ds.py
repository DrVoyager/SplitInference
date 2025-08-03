from reluLayer import ReluLayer
from convLayer2 import ConvLayer
from batchnormalLayer2 import BatchNormalLayer

class Layers_Ds:
    def __init__(self, nInputNum, nOutputNum, nInputWidth, nStride, fileNum1, fileNum2):
        # The following references assume the existence of ConvLayer, BatchNormalLayer, and ReluLayer in Python.
        # They must be defined similarly to your original code.
        self.m_ConvlayerDw = ConvLayer(fileNum1, nInputNum, nInputNum, nInputWidth, 3, 1, nStride, nInputNum)
        self.m_ConvDwBn = BatchNormalLayer(fileNum1, nInputNum, nInputWidth // nStride)
        self.m_RelulayerDw = ReluLayer(self.m_ConvDwBn.GetOutputSize())

        self.m_ConvlayerSep = ConvLayer(fileNum2, nInputNum, nOutputNum, nInputWidth // nStride, 1, 0)
        self.m_ConvSepBn = BatchNormalLayer(fileNum2, nOutputNum, nInputWidth // nStride)
        self.m_RelulayerSep = ReluLayer(self.m_ConvSepBn.GetOutputSize())

    def __del__(self):
        pass

    def forward(self, pfInput):
        
        self.m_ConvlayerDw.forward(pfInput)
        self.m_ConvDwBn.forward(self.m_ConvlayerDw.GetOutput())
        self.m_RelulayerDw.forward(self.m_ConvDwBn.GetOutput())

        self.m_ConvlayerSep.forward(self.m_RelulayerDw.GetOutput())
        self.m_ConvSepBn.forward(self.m_ConvlayerSep.GetOutput())
        self.m_RelulayerSep.forward(self.m_ConvSepBn.GetOutput())

    def GetOutput(self):
        return self.m_RelulayerSep.GetOutput()
