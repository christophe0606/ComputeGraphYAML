import argparse
from yaml import load, dump

parser = argparse.ArgumentParser(description='Parse test description')
parser.add_argument('others', nargs=argparse.REMAINDER)

args = parser.parse_args()

if len(args.others)>0:
    testid = args.others[0]
    if testid == 'a':
        from ga.graph import * 
    if testid == 'b':
        from gb.graph import * 
    if testid == 'c':
        # gc is a Python package so we can't reuse
        # this name
        from gctest.graph import * 
    if testid == 'd':
        from gd.graph import * 
    if testid == 'e':
        from ge.graph import * 
    if testid == 'f':
        from gf.graph import * 
    if testid == 'g':
        from gg.graph import * 
    if testid == 'h':
        from gh.graph import * 
    if testid == 'i':
        from gi.graph import * 
    if testid == 'j':
        from gj.graph import * 
    if testid == 'k':
        from gk.graph import * 
    if testid == 'l':
        from gl.graph import * 
else:
   # Include definition of the graph
   from ga.graph import * 

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
          "constant":True
        }
        yaml_desc["dst"] = {
          "node": dstNode.nodeName,
          "input":self.dst._name
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
          "node": srcNode.nodeName,
          "output":self.src._name
        }
        yaml_desc["dst"] = {
          "node": dstNode.nodeName,
          "input":self.dst._name
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
       yaml_desc["input"] = io._name 
    else:
       yaml_desc["output"] = io._name 
    if isinstance(io._nbSamples,list):
       yaml_desc["samples"] = list(io._nbSamples)
    else:
       yaml_desc["samples"] = io._nbSamples 
    yaml_desc["type"] = create_YAML_type(io._theType,structured_datatypes)
    
    return(yaml_desc)


class YAMLConstantNode():
    def __init__(self,node):
        self._node = node

    @property
    def node(self):
        return self._node

    def yaml(self):
        res = {}
        res["name"] = self._node.name
        res["constant"] = True
        return(res)


class YAMLNode():
    def __init__(self,node,structured_datatypes):
        self._node = node
        self._structured_datatypes = structured_datatypes

    @property
    def node(self):
        return self._node

    def yaml(self):
        res = {}
        res["node"] = self._node._nodeName
        res["kind"] = self._node.typeName
        
        inputs = []
        outputs = []
        for i in self._node._inputs:
            io = self._node._inputs[i]
            inputs.append(create_YAML_IO(io,self._structured_datatypes,is_input=True))

        if inputs:
           res["inputs"] = inputs

        for o in self._node._outputs:
            io = self._node._outputs[o]
            outputs.append(create_YAML_IO(io,self._structured_datatypes))

        if outputs:
           res["outputs"] = outputs

        if self._node.schedArgs:
           yaml_args = []
           for arg in self._node.schedArgs:
               if isinstance(arg,ArgLiteral):
                  yaml_args.append({"literal" : arg._name})
               else:
                  yaml_args.append({"variable" : arg._name})
           if len(yaml_args)>0:
              res["args"] = yaml_args
           else:
              print(f"Error parsing args for node {self._node._nodeName}")

        return(res)


def export(graph):
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
        
    yaml["version"] = 1.0

    # Scanning nodes is required to extract the structured datatypes
    nodes = [allNodes[x].yaml() for x in allNodes] 
    edges = [allEdges[x].yaml() for x in allEdges]

    if len(structured_datatypes)>0:
        yaml["graph"] = {
          "structures" : structured_datatypes,
          "nodes":nodes,
          "edges":edges,
        }
    else:
        yaml["graph"] = {
          "nodes":nodes,
          "edges":edges,
        }
   

    return yaml


res = export(the_graph)

print(dump(res, default_flow_style=False, sort_keys=False))
#print(dump(res, canonical=True))
#print(dump(res))