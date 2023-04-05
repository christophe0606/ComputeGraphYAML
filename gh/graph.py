import numpy as np 

from cmsisdsp.cg.scheduler import *


class Processing(GenericNode):
    def __init__(self,name,outLength):
        GenericNode.__init__(self,name)
        self.addInput("i",CType(Q15),outLength)
        self.addOutput("o",CType(Q15),outLength)

    @property
    def typeName(self):
        return "Processing"


BUFSIZE=128
### Define nodes
src=VHTSource("src",BUFSIZE,0)
processing=Processing("proc",BUFSIZE)
sink=VHTSink("sink",BUFSIZE,0)


g = Graph()

g.connect(src.o, processing.i)
g.connect(processing.o, sink.i)



the_graph = g