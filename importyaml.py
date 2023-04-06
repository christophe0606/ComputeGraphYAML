import argparse
from yaml import safe_load, dump

from cmsisdsp.cg.scheduler import *

# Include definitions from the Python package
from cmsisdsp.cg.scheduler import GenericNode,GenericSink,GenericSource

def dataType(s):
    if s == 'float32_t':
        return(CType(F32))

class YamlSource(GenericSource):
    def __init__(self,yaml):
        GenericSource.__init__(self,yaml['node'])
        self._cpp = yaml['kind']
        for o in yaml['outputs']:
            theType = o['type']
            nbSamples = o['samples']
            name = o['output']
        self.addOutput(name,dataType(theType),nbSamples)

    @property
    def typeName(self):
        """The name of the C++ class implementing this node"""
        return (self._cpp)

class YamlSink(GenericSink):
    def __init__(self,yaml):
        GenericSink.__init__(self,yaml['node'])
        self._cpp = yaml['kind']
        for i in yaml['inputs']:
            theType = i['type']
            nbSamples = i['samples']
            name = i['input']
        self.addInput(name,dataType(theType),nbSamples)

    @property
    def typeName(self):
        """The name of the C++ class implementing this node"""
        return (self._cpp)

class YamlNode(GenericNode):
    def __init__(self,yaml):
        GenericNode.__init__(self,yaml['node'])
        self._cpp = yaml['kind']
        for i in yaml['inputs']:
            theType = i['type']
            nbSamples = i['samples']
            name = i['input']
        self.addInput(name,dataType(theType),nbSamples)
        for o in yaml['outputs']:
            theType = o['type']
            nbSamples = o['samples']
            name = o['output']
        self.addOutput(name,dataType(theType),nbSamples)

    @property
    def typeName(self):
        """The name of the C++ class implementing this node"""
        return (self._cpp)


parser = argparse.ArgumentParser(description='Parse test description')
parser.add_argument('others', nargs=argparse.REMAINDER)

args = parser.parse_args()



if len(args.others)>0:
    with open(args.others[0],"r") as f:
        r = safe_load(f)
    if 'graph' in r:
        g = r['graph']
        nodes = {}
        the_graph = Graph()
        if 'nodes' in g:
            for n in g['nodes']:
                name = n['node']
                if 'inputs' in n and 'outputs' in n:
                   nodes[name] = YamlNode(n)
                elif 'inputs' in n:
                   nodes[name] = YamlSink(n)
                elif 'outputs' in n: 
                   nodes[name] = YamlSource(n)
            for e in g['edges']:
                src = nodes[e['src']['node']]
                o = e['src']['output']


                dst = nodes[e['dst']['node']]
                i = e['dst']['input']

                the_graph.connect(src[o],dst[i])

            conf=Configuration()
            
            
            sched = the_graph.computeSchedule(conf)
            print("Schedule length = %d" % sched.scheduleLength)
            print("Memory usage %d bytes" % sched.memory)
            #
            
            
            sched.ccode("generated",config=conf)
            
            with open("test.dot","w") as f:
                sched.graphviz(f)
