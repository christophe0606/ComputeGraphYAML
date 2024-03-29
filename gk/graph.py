from cmsisdsp.cg.scheduler import *

### Define new types of Nodes 



class SinkAsync(GenericSink):
    def __init__(self,name,theType,inLength):
        GenericSink.__init__(self,name)
        self.addInput("i",theType,inLength)

    @property
    def typeName(self):
        return "SinkAsync"

class SourceOdd(GenericSource):
    def __init__(self,name,theType,inLength):
        GenericSource.__init__(self,name)
        self.addOutput("o",theType,inLength)

    @property
    def typeName(self):
        return "SourceOdd"

class SourceEven(GenericSource):
    def __init__(self,name,theType,inLength):
        GenericSource.__init__(self,name)
        self.addOutput("o",theType,inLength)

    @property
    def typeName(self):
        return "SourceEven"

class ProcessingOddEven(GenericNode):
    def __init__(self,name,theType,inLength,outLength):
        GenericNode.__init__(self,name)
        self.addInput("ia",theType,inLength)
        self.addInput("ib",theType,inLength)
        self.addOutput("o",theType,outLength)

    @property
    def typeName(self):
        return "ProcessingOddEven"



### Define nodes
dataType=CType(SINT16)
odd=SourceOdd("sourceOdd",dataType,1)
even=SourceEven("sourceEven",dataType,1)

proc=ProcessingOddEven("proc",dataType,1,1)
comp=Unary("compute",dataType,1)

sinka=SinkAsync("sinka",dataType,1)
sinkb=SinkAsync("sinkb",dataType,1)

debug=NullSink("debug",dataType,1)

g = Graph()

# Option to customize the default class
# to use for Duplicate and FIFO
# FIFO class can also be changed in the connect
# function to change the class for a specific
# connection
g.defaultFIFOClass = "FIFO"
g.duplicateNodeClassName = "Duplicate"

g.connect(odd.o,proc.ia)
g.connect(even.o,proc.ib)
# Just for checking duplicate nodes
# with scaling factor are working.
# In practice, all edge of a duplicate nodes
# should have same FIFO size
g.connect(odd.o,debug.i,fifoScale=3.0,fifoClass="MyFIFO")

g.connect(proc.o,comp.i)
g.connect(comp.o,sinka.i)
g.connect(comp.o,sinkb.i)


the_graph = g

conf=Configuration()
conf.debugLimit=10
conf.cOptionalArgs=""

conf.memoryOptimization=True

conf.codeArray = True
conf.switchCase = True

conf.asynchronous = True 

conf.FIFOIncrease = 2.0