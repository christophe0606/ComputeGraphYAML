import argparse
from yaml import safe_load, dump

from cmsisdsp.cg.scheduler import *

# Include definitions from the Python package
from cmsisdsp.cg.scheduler import GenericNode,GenericSink,GenericSource

def dataType(s,cstruct):
    if s == 'float64_t':
        return(CType(F64))
    if s == 'float32_t':
        return(CType(F32))
    if s == 'float16_t':
        return(CType(F16))
    if s == 'q31_t':
        return(CType(Q31))
    if s == 'q15_t':
        return(CType(Q15))
    if s == 'q7_t':
        return(CType(Q7))
    if s == 'uint32_t':
        return(CType(UINT32))
    if s == 'uint16_t':
        return(CType(UINT16))
    if s == 'uint8_t':
        return(CType(UINT8))
    if s == 'int32_t':
        return(CType(SINT32))
    if s == 'int16_t':
        return(CType(SINT16))
    if s == 'int8_t':
        return(CType(SINT8))
    if s in cstruct:
        return(cstruct[s])

class YamlSource(GenericSource):
    def __init__(self,yaml,cstruct):
        GenericSource.__init__(self,yaml['node'])
        self._cpp = yaml['kind']
        for o in yaml['outputs']:
            theType = o['type']
            nbSamples = o['samples']
            name = o['output']
            self.addOutput(name,dataType(theType,cstruct),nbSamples)

    @property
    def typeName(self):
        """The name of the C++ class implementing this node"""
        return (self._cpp)

class YamlSink(GenericSink):
    def __init__(self,yaml,cstruct):
        GenericSink.__init__(self,yaml['node'])
        self._cpp = yaml['kind']
        for i in yaml['inputs']:
            theType = i['type']
            nbSamples = i['samples']
            name = i['input']
            self.addInput(name,dataType(theType,cstruct),nbSamples)

    @property
    def typeName(self):
        """The name of the C++ class implementing this node"""
        return (self._cpp)

class YamlNode(GenericNode):
    def __init__(self,yaml,cstruct):
        GenericNode.__init__(self,yaml['node'])
        self._cpp = yaml['kind']
        for i in yaml['inputs']:
            theType = i['type']
            nbSamples = i['samples']
            name = i['input']
            self.addInput(name,dataType(theType,cstruct),nbSamples)
        for o in yaml['outputs']:
            theType = o['type']
            nbSamples = o['samples']
            name = o['output']
            self.addOutput(name,dataType(theType,cstruct),nbSamples)

    @property
    def typeName(self):
        """The name of the C++ class implementing this node"""
        return (self._cpp)

def mkUnaryNode(yaml,cstruct):
    name = yaml['unary']
    firstInput = yaml['inputs'][0]
    theType = dataType(firstInput['type'],cstruct)
    nbSamples = firstInput['samples']

    return(Unary(name,theType,nbSamples))

def mkBinaryNode(yaml,cstruct):
    name = yaml['binary']
    firstInput = yaml['inputs'][0]
    theType = dataType(firstInput['type'],cstruct)
    nbSamples = firstInput['samples']

    return(Binary(name,theType,nbSamples))

def mkDspNode(yaml,cstruct):
    name = yaml['dsp']
    firstInput = yaml['inputs'][0]
    theType = dataType(firstInput['type'],cstruct)
    nbSamples = firstInput['samples']

    return(Dsp(name,theType,nbSamples))


parser = argparse.ArgumentParser(description='Parse test description')
parser.add_argument('others', nargs=argparse.REMAINDER)

args = parser.parse_args()

def processArguments(node,n):
    if 'args' in n:
        for k in n['args']:
            if 'literal' in k:
                node.addLiteralArg(k['literal'])
            if 'variable' in k:
                node.addVariableArg(k['variable'])

def importYaml(r):
    if 'graph' in r:
        g = r['graph']
        nodes = {}
        the_graph = Graph()
        cstruct={} 
        if 'structures' in g:
            for c in g['structures']:
                name = g['structures'][c]['cname']
                size = g['structures'][c]['bytes']
                cstruct[c]=CStructType(name,size)
        if 'nodes' in g:
            for n in g['nodes']:
                name = n['node']
                if 'inputs' in n and 'outputs' in n:
                   if 'kind' in n:
                       nodes[name] = YamlNode(n,cstruct)
                   if 'unary' in n: 
                       nodes[name] = mkUnaryNode(n,cstruct)
                   if 'binary' in n: 
                       nodes[name] = mkBinaryNode(n,cstruct)
                   if 'dsp' in n: 
                       nodes[name] = mkDspNode(n,cstruct)
                   processArguments(nodes[name],n)
                elif 'inputs' in n:
                   nodes[name] = YamlSink(n,cstruct)
                   processArguments(nodes[name],n)
                elif 'outputs' in n: 
                   nodes[name] = YamlSource(n,cstruct)
                   processArguments(nodes[name],n)
                else:
                   nodes[name] = Constant(name)
            for e in g['edges']:
                src = nodes[e['src']['node']]
                o = None
                if 'output' in e['src']:
                    o = e['src']['output']

                dst = nodes[e['dst']['node']]
                i = e['dst']['input']

                if o is None:
                   the_graph.connect(src,dst[i])
                else:
                   the_graph.connect(src[o],dst[i])
    return(the_graph)

if len(args.others)>0:
    with open(args.others[0],"r") as f:
        r = safe_load(f)
        the_graph = importYaml(r)
    
        conf=Configuration()
        
        
        sched = the_graph.computeSchedule(conf)
        print("Schedule length = %d" % sched.scheduleLength)
        print("Memory usage %d bytes" % sched.memory)
        #
        
        
        sched.ccode("generated",config=conf)
        
        with open("test.dot","w") as f:
            sched.graphviz(f)
