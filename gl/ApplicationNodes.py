from cmsisdsp.cg.scheduler import *

class FarEndSource(GenericSource):
    def __init__(self,name,theType,outLength):
        GenericSource.__init__(self,name)
        self.addOutput("oleft",theType,outLength)
        self.addOutput("oright",theType,outLength)

    @property
    def typeName(self):
        return "FarEndSource"

class EchoModel(GenericNode):
    def __init__(self,name,theType,inLength):
        GenericNode.__init__(self,name)
        self.addInput("f",theType,inLength)
        self.addInput("n",theType,inLength)
        self.addOutput("o",theType,inLength)

    @property
    def typeName(self):
        return "EchoModel"

# Debug source generating a sine
class BackgroundSource(GenericSource):
    def __init__(self,name,theType,outLength):
        GenericSource.__init__(self,name)
        self.addOutput("oleft",theType,outLength)
        self.addOutput("oright",theType,outLength)


    @property
    def typeName(self):
        return "BackgroundSource"