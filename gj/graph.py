from cmsisdsp.cg.scheduler import *

### Define new types of Nodes 

class Node(GenericNode):
    def __init__(self,name,theType,inLength,outLength):
        GenericNode.__init__(self,name)
        self.addInput("ia",theType,inLength)
        self.addInput("ib",theType,inLength)
        self.addOutput("o",theType,outLength)

class Sink(GenericSink):
    def __init__(self,name,theType,inLength):
        GenericSink.__init__(self,name)
        self.addInput("i",theType,inLength)

    @property
    def typeName(self):
        return "Sink"

class Source(GenericSource):
    def __init__(self,name,theType,inLength):
        GenericSource.__init__(self,name)
        self.addOutput("o",theType,inLength)

    @property
    def typeName(self):
        return "Source"

class ProcessingNode(Node):
    @property
    def typeName(self):
        return "ProcessingNode"



### Define nodes
floatType=CType(F32)
src=Source("source",floatType,5)
b=ProcessingNode("filter",floatType,5,5)
sink=Sink("sink",floatType,5)

g = Graph()

g.connect(src.o,b.ia)
g.connect(b.o,sink.i)
# With less than 5, the tool cannot find a possible schedule
# and is generating a DeadLock error
g.connectWithDelay(b.o,b.ib,5)


the_graph = g

conf=Configuration()
