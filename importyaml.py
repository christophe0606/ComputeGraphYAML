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

# First argument is graph yaml
# Second argument is configuration yaml
# For instance : 
# python importyaml.py ga\ref.yml ga\config.yml
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

def importGraph(r):
    if 'graph' in r:
        g = r['graph']
        nodes = {}
        the_graph = Graph()
        cstruct={} 
        if 'options' in g:
            if 'FIFO' in g['options']:
                the_graph.defaultFIFOClass = g['options']['FIFO']
            if 'Duplicate' in g['options']:
                the_graph.duplicateNodeClassName = g['options']['Duplicate']
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

                delay = None 
                if 'delay' in e:
                    delay = e['delay']

                fifoClass = None 
                fifoScale = 1.0 

                if 'class' in e: 
                    fifoClass = e['class']

                if 'scale' in e:
                    fifoScale = e['scale']

                if o is None:
                   if delay is not None:
                      the_graph.connectWithDelay(src,dst[i],
                        delay,
                        fifoScale=fifoScale,
                        fifoClass=fifoClass)
                   else:
                      the_graph.connect(src,dst[i],
                        fifoScale=fifoScale,
                        fifoClass=fifoClass)
                else:
                   if delay is not None:
                      the_graph.connectWithDelay(src[o],dst[i],
                        delay,
                        fifoScale=fifoScale,
                        fifoClass=fifoClass)
                   else:
                      the_graph.connect(src[o],dst[i],
                        fifoScale=fifoScale,
                        fifoClass=fifoClass)
    return(the_graph)

def importConfig(r):
    conf = Configuration()
    if 'schedule-options' in r:
        so = r['schedule-options']

        if 'memory-optimization' in so:
            conf.memoryOptimization = so['memory-optimization']

        if 'sink-priority' in so:
            conf.sinkPriority = so['sink-priority']

        if 'display-fifo-sizes' in so:
            conf.displayFIFOSizes = so['display-fifo-sizes']

        if 'dump-schedule' in so:
            conf.dumpSchedule = so['dump-schedule']

    if 'code-generation-options' in r:
        co = r['code-generation-options']

        if 'debug-limit' in co:
            conf.debugLimit = co['debug-limit']

        if 'dump-fifo' in co:
            conf.dumpFIFO = co['dump-fifo']

        if 'scheduler-name' in co:
            conf.schedName = co['scheduler-name']

        if 'fifo-prefix' in co:
            conf.prefix = co['fifo-prefix']

    if 'c-code-generation-options' in r:
        cco = r['c-code-generation-options']

        if 'c-optional-args' in cco:
            conf.cOptionalArgs = cco['c-optional-args']

        if 'code-array' in cco:
            conf.codeArray = cco['code-array']

        if 'switch-case' in cco:
            conf.switchCase = cco['switch-case']

        if 'event-recorder' in cco:
            conf.eventRecorder = cco['event-recorder']

        if 'custom-c-name' in cco:
            conf.customCName = cco['custom-c-name']

        if 'post-custom-c-name' in cco:
            conf.postCustomCName = cco['post-custom-c-name']

        if 'generic-node-c-name' in cco:
            conf.genericNodeCName = cco['generic-node-c-name']

        if 'app-nodes-c-name' in cco:
            conf.appNodesCName = cco['app-nodes-c-name']

        if 'scheduler-c-file-name' in cco:
            conf.schedulerCFileName = cco['scheduler-c-file-name']

        if 'c-api' in cco:
            conf.CAPI = cco['c-api']

        if 'cmsis-dsp' in cco:
            conf.CMSISDSP = cco['cmsis-dsp']

        if 'asynchronous' in cco:
            conf.asynchronous = cco['asynchronous']

        if 'fifo-increase' in cco:
            conf.FIFOIncrease = cco['fifo-increase']

        if 'async-default-skip' in cco:
            conf.asyncDefaultSkip = cco['async-default-skip']

    if 'python-code-generation-options' in r:
        pco = r['python-code-generation-options']

        if 'py-optional-args' in pco:
            conf.pyOptionalArgs = pco['py-optional-args']

        if 'custom-python-name' in pco:
            conf.customPythonName = pco['custom-python-name']

        if 'app-nodes-python-name' in pco:
            conf.appNodesPythonName = pco['app-nodes-python-name']

        if 'scheduler-python-file-name' in pco:
            conf.schedulerPythonFileName = pco['scheduler-python-file-name']

        if 'scheduler-python-file-name' in pco:
            conf.schedulerPythonFileName = pco['scheduler-python-file-name']

    if 'graphviz-code-generation-options' in r:
        gco = r['graphviz-code-generation-options']

        if 'horizontal' in gco:
            conf.horizontal = gco['horizontal']

        if 'display-fifo-buf' in gco:
            conf.displayFIFOBuf = gco['display-fifo-buf']


    return(conf)

if len(args.others)>1:
    with open(args.others[0],"r") as f:
        r = safe_load(f)
        the_graph = importGraph(r)

    with open(args.others[1],"r") as f:
        r = safe_load(f)
        conf = importConfig(r)
    
        
    sched = the_graph.computeSchedule(conf)
    print("Schedule length = %d" % sched.scheduleLength)
    print("Memory usage %d bytes" % sched.memory)
        
        
    sched.ccode("generated",config=conf)
        
    with open("test.dot","w") as f:
        sched.graphviz(f)
