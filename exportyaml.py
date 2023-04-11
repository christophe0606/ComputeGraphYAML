import argparse
from yaml import load, dump
from cmsisdsp.cg.scheduler import *

# Argument is test name:
# For instance:
# python exportyaml.py a
# It will generate ga/ref.yml and ga/config.yml
parser = argparse.ArgumentParser(description='Parse test description')
parser.add_argument('others', nargs=argparse.REMAINDER)

args = parser.parse_args()

if len(args.others)>0:
    testid = args.others[0]
    if testid == 'a':
        from ga.graph import * 
        path = "ga"
    if testid == 'b':
        from gb.graph import * 
        path = "gb"
    if testid == 'c':
        # gc is a Python package so we can't reuse
        # this name
        from gctest.graph import * 
        path = "gctest"
    if testid == 'd':
        from gd.graph import * 
        path = "gd"
    if testid == 'e':
        from ge.graph import * 
        path = "ge"
    if testid == 'f':
        from gf.graph import * 
        path = "gf"
    if testid == 'g':
        from gg.graph import * 
        path = "gg"
    if testid == 'h':
        from gh.graph import * 
        path = "gh"
    if testid == 'i':
        from gi.graph import * 
        path = "gi"
    if testid == 'j':
        from gj.graph import * 
        path = "gj"
    if testid == 'k':
        from gk.graph import * 
        path = "gk"
    if testid == 'l':
        from gl.graph import * 
        path = "gl"
    if testid == 'm':
        from gm.graph import * 
        path = "gm"
else:
   # Include definition of the graph
   from ga.graph import * 
   path = "ga"

class YAMLConstantEdge():
    def __init__(self,src,dst):
        self._src = src
        self._dst = dst

    @property
    def src(self):
        return self._src

    @property
    def dst(self):
        return self._dst

    def yaml(self):
        yaml_desc = {}
        srcNode = self.src
        dstNode = self.dst.owner 

        yaml_desc["src"] = {
          "node": srcNode.name,
        }
        yaml_desc["dst"] = {
          "node": dstNode.nodeID,
          "input":self.dst.name
        }

        return(yaml_desc)


class YAMLEdge():
    def __init__(self,src,dst,fifoClass,fifoScale,fifoDelay,constantEdge):
        self._src = src
        self._dst = dst
        self._fifoClass = fifoClass 
        self._fifoScale = fifoScale
        self._fifoDelay = fifoDelay
        self._constantEdge = constantEdge

    @property
    def src(self):
        return self._src

    @property
    def dst(self):
        return self._dst

    @property
    def fifoClass(self):
        return self._fifoClass

    @property
    def fifoScale(self):
        return self._fifoScale
    

    @property
    def fifoDelay(self):
        return self._fifoDelay

    @property
    def constantEdge(self):
        return self._constantEdge

    def yaml(self):
        yaml_desc = {}
        srcNode = self.src.owner 
        dstNode = self.dst.owner 

        yaml_desc["src"] = {
          "node": srcNode.nodeID,
          "output":self.src.name
        }
        yaml_desc["dst"] = {
          "node": dstNode.nodeID,
          "input":self.dst.name
        }
        if self.fifoClass:
            if self.fifoClass != "FIFO":
               yaml_desc["class"] = self.fifoClass
        if self.fifoScale:
            if self.fifoScale != 1.0:
               yaml_desc["scale"] = self.fifoScale
        if self.fifoDelay:
            yaml_desc["delay"] = self.fifoDelay
        return(yaml_desc)
    
def create_YAML_type(t,structured_datatypes):
    if isinstance(t,CType):
        return(t.ctype)
    else:
       yaml_desc = {}
       yaml_desc["cname"] = t.ctype 
       #yaml_desc["python_name"] = t._python_name
       yaml_desc["bytes"] = t.bytes

       if not t.ctype  in structured_datatypes:
          structured_datatypes[t.ctype] = yaml_desc
       return(t.ctype)

    
def create_YAML_IO(io,structured_datatypes,is_input=False):
    yaml_desc = {}
    if is_input:
       yaml_desc["input"] = io.name 
    else:
       yaml_desc["output"] = io.name 
    if isinstance(io._nbSamples,list):
       yaml_desc["samples"] = list(io.nbSamples)
    else:
       yaml_desc["samples"] = io.nbSamples 
    yaml_desc["type"] = create_YAML_type(io.theType,structured_datatypes)
    
    return(yaml_desc)


class YAMLConstantNode():
    def __init__(self,node):
        self._node = node

    @property
    def node(self):
        return self._node

    def yaml(self):
        res = {}
        res["node"] = self.node.name
        return(res)


class YAMLNode():
    def __init__(self,node,structured_datatypes):
        self._node = node
        self._structured_datatypes = structured_datatypes

    @property
    def node(self):
        return self._node

    @property
    def structured_datatypes(self):
        return self._structured_datatypes
    

    def yaml(self):
        res = {}
        res["node"] = self.node.nodeID
        isDSP = False
        if isinstance(self.node,Dsp):
           cmsisfunc = self.node.nodeName.split("_")
           res["dsp"] = cmsisfunc[1]
           isDSP = True
        elif isinstance(self.node,Unary):
           res["unary"] = self.node.nodeName
        elif isinstance(self.node,Binary):
           res["binary"] = self.node.nodeName
        else:
           res["kind"] = self.node.typeName
        
        inputs = []
        outputs = []
        for i in self.node._inputs:
            io = self.node._inputs[i]
            inputs.append(create_YAML_IO(io,self.structured_datatypes,is_input=True))

        if inputs:
           res["inputs"] = inputs

        for o in self.node._outputs:
            io = self.node._outputs[o]
            outputs.append(create_YAML_IO(io,self.structured_datatypes))

        if outputs:
           res["outputs"] = outputs

        if self.node.schedArgs:
           yaml_args = []
           for arg in self.node.schedArgs:
               if isinstance(arg,ArgLiteral):
                  yaml_args.append({"literal" : arg._name})
               else:
                  yaml_args.append({"variable" : arg._name})
           if len(yaml_args)>0:
              res["args"] = yaml_args
           else:
              print(f"Error parsing args for node {self.node.nodeID}")

        return(res)


def export_graph(graph):
    allNodes = {}
    allEdges = {}
    structured_datatypes = {}
    yaml = {}
    # Parse edges having a constant node as source first
    for edge in graph._constantEdges:
        (src,dst) = edge
        dstNode = dst.owner 
        srcNode = src

        if not srcNode in allNodes:
            allNodes[srcNode] = YAMLConstantNode(srcNode)
        if not dst.owner in allNodes:
            allNodes[dstNode] = YAMLNode(dstNode,structured_datatypes)

        if not edge in allEdges:
           allEdges[edge] = YAMLConstantEdge(src,dst)


    for edge in graph._edges:
        (src,dst) = edge
        fifoClass = None
        fifoScale = None 
        fifoDelay = None
        constantEdge = False

        srcNode = src.owner 
        dstNode = dst.owner 


        if edge in graph._FIFOClasses:
            fifoClass = graph._FIFOClasses[edge]
        if edge in graph._FIFOScale:
            fifoScale = graph._FIFOScale[edge]
        if edge in graph._delays:
            fifoDelay = graph._delays[edge]
        if edge in graph._constantEdges:
            constantEdge = graph._constantEdges[edge]

        if not edge in allEdges:
            allEdges[edge] = YAMLEdge(src,dst,fifoClass,fifoScale,fifoDelay,constantEdge)

        if not srcNode in allNodes:
            allNodes[srcNode] = YAMLNode(srcNode,structured_datatypes)
        if not dst.owner in allNodes:
            allNodes[dstNode] = YAMLNode(dstNode,structured_datatypes)
        
    yaml["version"] = "1.0"

    # Scanning nodes is required to extract the structured datatypes
    nodes = [allNodes[x].yaml() for x in allNodes] 
    edges = [allEdges[x].yaml() for x in allEdges]

    options = None
    if graph.defaultFIFOClass != 'FIFO' or graph.duplicateNodeClassName != "Duplicate":
       options = {}
       if graph.defaultFIFOClass != 'FIFO':
          options['FIFO'] = graph.defaultFIFOClass
       if graph.duplicateNodeClassName != 'Duplicate':
          options['Duplicate'] = graph.duplicateNodeClassName


    if len(structured_datatypes)>0:
        if options:
            yaml["graph"] = {
             "options:" : options,
             "structures" : structured_datatypes,
             "nodes":nodes,
             "edges":edges,
           }
        else:
           yaml["graph"] = {
             "structures" : structured_datatypes,
             "nodes":nodes,
             "edges":edges,
           }
    else:
        if options:
            yaml["graph"] = {
              "options:" : options,
              "nodes":nodes,
              "edges":edges,
            }
        else:
            yaml["graph"] = {
              "nodes":nodes,
              "edges":edges,
            }
   

    return yaml

def export_config(config):
    yaml = {}
    yaml["version"] = 1.0
    default = Configuration()

    schedule_options = {}
    if config.memoryOptimization != default.memoryOptimization:
        schedule_options["memory-optimization"] = config.memoryOptimization

    if config.sinkPriority  != default.sinkPriority :
        schedule_options["sink-priority"] = config.sinkPriority

    if config.displayFIFOSizes   != default.displayFIFOSizes  :
        schedule_options["display-fifo-sizes"] = config.displayFIFOSizes

    if config.dumpSchedule   != default.dumpSchedule  :
        schedule_options["dump-schedule"] = config.dumpSchedule 

    if schedule_options:
        yaml["schedule-options"] = schedule_options 

    code_gen = {}

    if config.debugLimit != default.debugLimit:
        code_gen["debug-limit"] = config.debugLimit  

    if config.dumpFIFO  != default.dumpFIFO :
        code_gen["dump-fifo"] = config.dumpFIFO  

    if config.schedName   != default.schedName  :
        code_gen["scheduler-name"] = config.schedName  


    if config.prefix    != default.prefix   :
        code_gen["fifo-prefix"] = config.prefix   


    if code_gen:
        yaml["code-generation-options"] = code_gen 

    c_code_gen = {}

    if config.cOptionalArgs  != default.cOptionalArgs:
        c_code_gen["c-optional-args"] = config.cOptionalArgs 

    if config.codeArray  != default.codeArray:
        c_code_gen["code-array"] = config.codeArray 

    if config.switchCase  != default.switchCase:
        c_code_gen["switch-case"] = config.switchCase 

    if config.eventRecorder   != default.eventRecorder :
        c_code_gen["event-recorder"] = config.eventRecorder 

    if config.customCName    != default.customCName  :
        c_code_gen["custom-c-name"] = config.customCName 

    if config.postCustomCName     != default.postCustomCName   :
        c_code_gen["post-custom-c-name"] = config.postCustomCName      

    if config.genericNodeCName      != default.genericNodeCName    :
        c_code_gen["generic-node-c-name"] = config.genericNodeCName       

    if config.appNodesCName      != default.appNodesCName    :
        c_code_gen["app-nodes-c-name"] = config.appNodesCName       

    if config.schedulerCFileName != default.schedulerCFileName    :
        c_code_gen["scheduler-c-file-name"] = config.schedulerCFileName

    if config.CAPI  != default.CAPI     :
        c_code_gen["c-api"] = config.CAPI 

    if config.CMSISDSP   != default.CMSISDSP      :
        c_code_gen["cmsis-dsp"] = config.CMSISDSP 

    if config.asynchronous != default.asynchronous      :
        c_code_gen["asynchronous"] = config.asynchronous

    if config.FIFOIncrease  != default.FIFOIncrease       :
        c_code_gen["fifo-increase"] = config.FIFOIncrease 

    if config.asyncDefaultSkip   != default.asyncDefaultSkip        :
        c_code_gen["async-default-skip"] = config.asyncDefaultSkip   

    if c_code_gen:
        yaml["c-code-generation-options"] = c_code_gen 

    python_code_gen = {}
    if config.pyOptionalArgs    != default.pyOptionalArgs         :
        python_code_gen["py-optional-args"] = config.pyOptionalArgs    

    if config.customPythonName     != default.customPythonName          :
        python_code_gen["custom-python-name"] = config.customPythonName     

    if config.appNodesPythonName != default.appNodesPythonName          :
        python_code_gen["app-nodes-python-name"] = config.appNodesPythonName     

    if config.schedulerPythonFileName != default.schedulerPythonFileName           :
        python_code_gen["scheduler-python-file-name"] = config.schedulerPythonFileName      

    if python_code_gen:
        yaml["python-code-generation-options"] = python_code_gen 

    graphviz_code_gen = {}
    if config.horizontal  != default.horizontal            :
        graphviz_code_gen["horizontal"] = config.horizontal       

    if config.displayFIFOBuf   != default.displayFIFOBuf             :
        graphviz_code_gen["display-fifo-buf"] = config.displayFIFOBuf        

    if graphviz_code_gen:
        yaml["graphviz-code-generation-options"] = graphviz_code_gen 

    return(yaml)

graph_yml = export_graph(the_graph)
conf_yaml = export_config(conf)

with open(f"{path}/ref.yml","w") as f:
    print(dump(graph_yml, default_flow_style=False, sort_keys=False),file=f)
    
with open(f"{path}/config.yml","w") as f:
    print(dump(conf_yaml, default_flow_style=False, sort_keys=False),file=f)
    
sched = the_graph.computeSchedule(conf)

sched.ccode(f"{path}/generated",config=conf)
       
with open(f"{path}/test.dot","w") as f:
    sched.graphviz(f)

#print(dump(graph_yml, canonical=True))
#print(dump(graph_yml))