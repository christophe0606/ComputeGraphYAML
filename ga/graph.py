# Include definitions from the Python package to
# define datatype for the IOs and to have access to the
# Graph class
from cmsisdsp.cg.scheduler import *

# Include definitions from the Python package
from cmsisdsp.cg.scheduler import GenericNode,GenericSink,GenericSource

### Define new types of Nodes 

class ProcessingNode(GenericNode):
    """
    Definition of a ProcessingNode for the graph

    Parameters
    ----------
    name : str
         Name of the C variable identifying this node 
         in the C code
    theType : CGStaticType
            The datatype for the input and output
    inLength : int
             The number of samples consumed by input
    outLength : int 
              The number of samples produced on output
    """
    def __init__(self,name,theType,inLength,outLength):
        GenericNode.__init__(self,name)
        self.addInput("i",theType,inLength)
        self.addOutput("o",theType,outLength)

    @property
    def typeName(self):
        """The name of the C++ class implementing this node"""
        return "ProcessingNode"

class Sink(GenericSink):
    """
    Definition of a Sink node for the graph

    Parameters
    ----------
    name : str
         Name of the C variable identifying this node 
         in the C code
    theType : CGStaticType
            The datatype for the input
    inLength : int
             The number of samples consumed by input
    """
    def __init__(self,name,theType,inLength):
        GenericSink.__init__(self,name)
        self.addInput("i",theType,inLength)

    @property
    def typeName(self):
        """The name of the C++ class implementing this node"""
        return "Sink"

class Source(GenericSource):
    """
    Definition of a Source node for the graph

    Parameters
    ----------
    name : str
         Name of the C variable identifying this node 
         in the C code
    theType : CGStaticType
            The datatype for the output
    outLength : int 
              The number of samples produced on output
    """
    def __init__(self,name,theType,outLength):
        GenericSource.__init__(self,name)
        self.addOutput("o",theType,outLength)

    @property
    def typeName(self):
        """The name of the C++ class implementing this node"""
        return "Source"



# Define the datatype we are using for all the IOs in this
# example
floatType=CType(F32)

# Instantiate a Source node with a float datatype and
# working with packet of 5 samples (each execution of the
# source in the C code will generate 5 samples)
# "source" is the name of the C variable that will identify
# this node
src=Source("source",floatType,5)
# Instantiate a Processing node using a float data type for
# both the input and output. The number of samples consumed
# on the input and produced on the output is 7 each time
# the node is executed in the C code
# "processing" is the name of the C variable that will identify
# this node
processing=ProcessingNode("processing",floatType,7,7)
# Instantiate a Sink node with a float datatype and consuming
# 5 samples each time the node is executed in the C code
# "sink" is the name of the C variable that will identify
# this node
sink=Sink("sink",floatType,5)

# Create a Graph object
the_graph = Graph()

# Connect the source to the processing node
the_graph.connect(src.o,processing.i)
# Connect the processing node to the sink
the_graph.connect(processing.o,sink.i)


