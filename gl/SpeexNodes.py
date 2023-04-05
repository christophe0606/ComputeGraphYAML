from cmsisdsp.cg.scheduler import *
import math

class Denoise(GenericNode):
    def __init__(self,name,theType,inLength):
        GenericNode.__init__(self,name)
        self.addInput("i",theType,inLength)
        self.addOutput("o",theType,inLength)

    @property
    def typeName(self):
        return "Denoise"

class Resampler(GenericNode):
    def __init__(self,name,theType,inLength,outLength):
        GenericNode.__init__(self,name)
        self.addInput("i",theType,inLength)
        self.addOutput("o",theType,outLength)

    @property
    def typeName(self):
        return "Resampler"

class EchoCanceller(GenericNode):
    def __init__(self,name,theType,inLength):
        GenericNode.__init__(self,name)
        self.addInput("i",theType,inLength)
        self.addInput("r",theType,inLength)
        self.addOutput("o",theType,inLength)

    @property
    def typeName(self):
        return "EchoCanceller"