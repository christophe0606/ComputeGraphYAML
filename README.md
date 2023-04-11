# Table of content

* [Introduction](#introduction)
* [YAML for the graph](#yaml-for-the-graph)
  * [`version:`](#version)
  * [`graph:`](#graph)
    * [`options:`](#options)
    * [`structures:`](#structures)
    * [`nodes:`](#nodes)
    * [`edges:`](#edges)
* [Node description](#node-description)
  * [`node:`](#node)
  * [`kind:`](#kind)
  * [`inputs:`](#io-port-description)
  * [`outputs:`](#io-port-description)
  * [`args:`](#args)

* [Edge description](#edge-description)
  * [`src:`](#src)
    * [`node:`](#node)
    * [`output:`](#input-or-output)
  * [`dst:`](#dst)
    * [`node:`](#node)
    * [`input:`](#input-or-output)

* [IO Port description](#io-port-description)
  * [`input:`](#input-or-output) or [`output:`](#input-or-output)
  * [`samples:`](#samples)
  * [`type:`](#type)
* [YAML for the configuration](#yaml-for-the-configuration)
* [version:](#version)

# Introduction

Two kind of YAML files are used for the compute graph. The first kind is the graph description that is:

* Defining the nodes
* The API of the nodes
* The implementation to use for the nodes
* The edges and the related FIFOs

The second kind of file is the configuration file controlling how the code generation is done:

* Describing the API of the scheduler
* Describing if the graph is synchronous or asynchronous
* Defining the name of all the files used and / or generated by the tool

# YAML for the graph

The table below explains the top-level elements of the yml graph description.

| Keyword                | Description                                                |
| ---------------------- | ---------------------------------------------------------- |
| [`version:`](#version) | Version of the Compute graph YAML format used by this file |
| [`graph:`](#graph)     | Description of the graph                                   |

## `graph:`

Description of the graph. It contains the following:

| `graph:`                     |              | Content                                                      |
| ---------------------------- | ------------ | ------------------------------------------------------------ |
| [`options:`](#options)       | Optional     | Option to select some default  C++ class for some nodes and edges |
| [`structures:`](#structures) | Optional     | C struct used in the graph for IO description                |
| [`nodes:`](#nodes)           | **Required** | List of nodes in the graph                                   |
| [`edges:`](#edges)           | **Required** | List of edges in the graph                                   |

**Examples:**

```yml
version: '1.0'
graph:
  nodes:
  ...
  edges:
  ...
```

### `options:`

| `options:`   |          | Content                                                      |
| ------------ | -------- | ------------------------------------------------------------ |
| `FIFO:`      | Optional | Name of the C++ class implementing FIFOs in the C++ generated code. (It can be overridden for each edge of the graph) |
| `Duplicate:` | Optional | `Prefix` of C++ class implementing the implicit `Duplicate` nodes that are introduced to implement one-to-many connections. The C++ class are named `Prefix2` and `Prefix3` (currently limited to 3 outputs for the implicit duplicate nodes. For more outputs you need to introduce explicit duplication nodes in the graph) |

### `structures:`

List of C structs used in the node description.

This entry is optional in the graph description.

**Examples**

```yml
  structures:
    structure1:
      ...
    structure2:
      ...
```

```yml
  structures:
    complex:
      cname: complex
      bytes: 8
    quaternion:
      cname: quaternion
      bytes: 16
```

Each item in the list has following format:

| Keyword  | Description                                              |
| -------- | -------------------------------------------------------- |
| `cname:` | C name of the structure                                  |
| `bytes:` | Size of the structure in bytes as returned by C `sizeof` |

**Examples**

```yml
- structures:
    complex:
      cname: complex
      bytes: 8
```

### `nodes:`

List of [nodes](#node-description)

**Examples:**

```yml
nodes:
  - node: source
    ...
  - node: processing
    ...
  - node: sink
    ...
```

### `edges:`

List of [edges](#edge-description).

**Examples:**

```yml
edges:
  - src:
      node: source
      ...
    dst:
      node: processing
      ...
  - src:
      node: processing
      ...
    dst:
      node: sink
      ...
```

### Node description

 It contains the following:

| nodes:                       |              | Content                                                      |
| ---------------------------- | ------------ | ------------------------------------------------------------ |
| [`node:`](#node-description) | **Required** | Identification of the node.                                  |
| [`kind:`](#kind)             | Optional     | The category of the node (when implemented with a C++ class) |
| [`dsp:`](#dsp)               | Optional     | The CMSIS-DSP function name (when node is a CMSIS-DSP function) |
| [`unary:`](#unary)           | Optional     | Function name for unary function (when node is a pure function with one input and one output) |
| [`binary:`](#binary)         | Optional     | Function name for binary function (when node is a pure function with two inputs and one output) |
| [`inputs:`](#inputs)         | Optional     | List of inputs for this node                                 |
| [`outputs:`](#output)        | Optional     | List of outputs for this node                                |
| [`args:`](#args)             | Optional     |                                                              |

**Examples:**

```yml
- node: processing
    kind: ProcessingNode
    inputs:
    - input: i
      samples: 7
      type: float32_t
    outputs:
    - output: o
      samples: 7
      type: float32_t
```

#### `node:`

Identification of the node. It must be a valid C variable name. It is used to identify the node in the graph and in the generated C code. It must be unique in the graph since it is the only way to identify the node,

#### `kind:`

It is the name of the `C++` class template implementing the node. It must be a valid `C++` class name.

It is optional for `Constant` nodes since those nodes just represent a C variable and don't have a corresponding C implementation.

It is not used for `Dsp`, `Unary` and `Binary` nodes that are mapped to pure C functions. A pure C function has no state and thus do not need a C++ wrapper.

#### `dsp:`

When the node is a CMSIS-DSP function that has no state (a pure function), there is no C++ wrapper. This `dsp:` field is the name of a CMSIS-DSP function (without the prefix and datatype.)

**Examples:**

```yml
  - node: arm_scale_f321
    dsp: scale
    inputs:
    - input: ia
      samples: 160
      type: float32_t
    - input: ib
      samples: 160
      type: float32_t
    outputs:
    - output: o
      samples: 160
      type: float32_t
```

This will be mapped to the CMSIS-DSP function `arm_scale_f32` with header:

```C
  void arm_scale_f32(
  const float32_t * pSrc,
        float32_t scale,
        float32_t * pDst,
        uint32_t blockSize);
```

In this example we can see that the second argument is not an array but a constant. It must thus be connected, in the graph, to a constant node. Connecting it to a normal node would be an error since it would be connected to a FIFO in the generated graph.

By connecting `ib` to a constant node, the `ib` description will just be ignored.

The Python is currently recognizing only a small subset of CMSIS-DSP functions and is not checking if the argument is a constant or array.

The YAML description for a `Dsp` node must ensure that datatypes and number of samples are the same for all IO ports.

#### `unary:`

When the node is a pure function that has no state and only one input / output, there is no C++ wrapper. This `unary:` field is the name of the function. The C function should implement a specific header.

**Examples:**

```yml
  - node: my_scale1
    unary: my_scale
    inputs:
    - input: i
      samples: 160
      type: float32_t
    outputs:
    - output: o
      samples: 160
      type: float32_t
```

**Header for a unary function:**

```C
void unary(
  const float32_t * pSrc,
        float32_t * pDst,
        uint32_t blockSize);
```

#### `binary:`

When the node is a pure function that has no state, two inputs, one output, there is no C++ wrapper. This `binary:` field is the name of the function. The C function should implement a specific header.

**Examples:**

```yml
  - node: my_binary1
    binary: my_binary
    inputs:
    - input: ia
      samples: 160
      type: float32_t
    - input: ib
      samples: 160
      type: float32_t
    outputs:
    - output: o
      samples: 160
      type: float32_t
```

**Header for a binary function:**

```C
void binary(
  const float32_t * pSrcA,
        float32_t * pSrcB,
        float32_t * pDst,
        uint32_t blockSize);
```

The type of an input argument could just be `float32_t` instead of a pointer. In that case, this input must be connected to a constant node in the graph.

#### `inputs:`

List of [inputs](#input-or-output) for the node.

A source node has no inputs. So this item is optional. 

#### `outputs:`

List of [outputs](#input-or-output) for the node.

A sink node has no outputs. So this item is optional.

#### `args:`

The `C++` implementation can have additional arguments in the constructor. Those arguments are defined with this `args:` field that is optional.

| args:                    |          | Content                  |
| ------------------------ | -------- | ------------------------ |
| [`literal:`](#literal)   | Optional | A scalar or string       |
| [`variable:`](#variable) | Optional | The name of a C variable |

**Examples:**

```yml
args:
    - literal: 4
    - literal: testString
    - variable: someVariable
```

The generated C++ constructor call may look like:

```C++
ProcessingNode<float32_t,7,float32_t,5> processing(fifo0,fifo1,4,"testString",someVariable);
```

##### `literal:`

It can be a scalar (int, float) or a string. I will be passed as it is to the API of the `C++` constructor.

##### `variable:`

It is the name of a C variable.

## Edge description

It contains the following:

| Keyword        |              | Content                                                      |
| -------------- | ------------ | ------------------------------------------------------------ |
| [`src:`](#src) | **Required** | Source port for the edge                                     |
| [`dst:`](#dst) | **Required** | Destination port for the edge                                |
| `class:`       | Optional     | Name of the C++ class template implementing this FIFO. The template arguments must be the same than in original FIFO template. The C++ class must inherit from `FIFOBase` |
| `scale:`       | Optional     | Used in asynchronous scheduling only. It is a float used to scale the synchronous FIFO size to have more margin in asynchronous mode. |

**Examples:**

```yml
- src:
      node: source
      output: o
  dst:
      node: processing
      input: i
```

```yml
- src:
      node: sourceOdd
      output: o
  dst:
      node: debug
      input: i
  class: MyFIFO
  scale: 3.0
```

### `src:`

Source port for an edge. It contains the following:

| `src:`                       | Content                                                     |
| ---------------------------- | ----------------------------------------------------------- |
| [`node:`](#node-description) | Source node                                                 |
| `output:`                    | Name of the [Output port](#io-port-description) of the node |

**Examples:**

```yml
- src:
      node: source
      output: o
```

### `dst:`

Destination port for an edge. It contains the following:

| `dst:`           | Content                                                     |
| ---------------- | ----------------------------------------------------------- |
| [`node:`](#node) | Destination node                                            |
| `input:`         | Name of the [Input port](#io-port-description) for the node |

**Examples:**

```yml
dst:
      node: processing
      input: i
```

## IO Port Description

Description of an IO port on a node:

| Keyword                | Content                                |
| ---------------------- | -------------------------------------- |
| `input:` or `output:`  | Name of the IO port.                   |
| [`samples:`](#samples) | Number of samples produced or consumed |
| [`type:`](#type)       | Data type for the samples              |

**Examples:**

```yml
- input: i
  samples: 7
  type: float32_t
```

```yml
- output: o
  samples: 5
  type: float32_t
```

### `input:` or `output:`

Name of the IO port. It must be a valid Python property name that is not already used by the Python root class.

### `samples:`

Number of samples produced on an output or consumed on an input.

In case of an asynchronous scheduling, it represents the ideal or average case.

In case of cyclo-static scheduling, this is a list encoding the sequence of generated values.

**Examples**

```yml
inputs:
    - input: i
      samples: 800
      type: int16_t
```

For cyclo-static scheduling:

```yml
outputs:
    - output: o
      samples:
      - 185
      - 185
      - 185
      - 180
      type: int16_t
```

### `type:`

Data type for the samples. It can be a scalar data type as defined in CMSIS-DSP:

* `float64_t`
* `float32_t`
* `float16_t`
* `q31_t`
* `q15_t`
* `q7_t`
* `uint32_t`
* `uint16_t`
* `uint8_t`
* `sint32_t`
* `sint16_t`
* `sint8_t`

It can also be more complex datatypes defined with a C struct. More complex datatypes have to be define at the beginning of the graph description using the [`structures:`](#structures) field.

## YAML for the configuration

The table below explains the top-level elements of the yml configuration description.

| Keyword                                                      | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [`version:`](#version)                                       | Version of the Compute graph YAML format used by this file   |
| [`schedule-options:`](#schedule-options)                     | Options used for the computation of the synchronous scheduling |
| [`code-generation-options:`](#code-generation-options)       | Common code generation options                               |
| [`c-code-generation-options:`](#c-code-generation-options)   | Options for the C++ code generation                          |
| [`python-code-generation-options:`](#python-code-generation-options) | Options for the Python code generation                       |
| [`graphviz-code-generation-options:`](#graphviz-code-generation-options) | Options for the graphviz generation                          |

### `schedule-options:`

| Keyword                                                      | Description                                              |
| ------------------------------------------------------------ | -------------------------------------------------------- |
| [`memory-optimization:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/SchedOptions.md#memoryoptimization-default--false) | Enable memory optimization                               |
| [`sink-priority:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/SchedOptions.md#sinkpriority-default--true) | Enable sink prioritization                               |
| [`display-fifo-sizes:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/SchedOptions.md#displayfifosizes-default--false) | Display FIFO sizes during schedule computation           |
| [`dump-schedule:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/SchedOptions.md#dumpschedule-default--false) | Dump the schedule at the end of the schedule computation |

### `code-generation-options:`

| Keyword                                                      | Description                                      |
| ------------------------------------------------------------ | ------------------------------------------------ |
| [`debug-limit:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CodegenOptions.md#debuglimit-default--0) | Number of schedule iterations (used for debug)   |
| [`dump-fifo:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CodegenOptions.md#dumpfifo-default--false) | Dump of FIFO content at runtime (used for debug) |
| [`scheduler-name:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CodegenOptions.md#schedname-default--scheduler) | Name of the scheduler function                   |
| [`fifo-prefix:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CodegenOptions.md#prefix-default--) | Prefix for naming FIFO global buffers.           |

### `c-code-generation-options:`

| Keyword                                                      | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [`c-optional-args:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CCodeGen.md#coptionalargs-default--) | Arguments of the C API of the scheduler                      |
| [`code-array:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CCodeGen.md#codearray-default--true) | Don't inline the schedule. Schedule is represented as an array |
| [`switch-case:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CCodeGen.md#switchcase-default--true) | Don't unroll the schedule. Schedule is implemented as a switch / case |
| [`event-recorder:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CCodeGen.md#eventrecorder-default--false) | Enable event recorder calls in the generated schedule        |
| [`custom-c-name:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CCodeGen.md#customcname-default--customh) | Name of the custom include file                              |
| [`post-custom-c-name:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CCodeGen.md#postcustomcname-default--) | Name of a custom include file following all other include files |
| [`generic-node-c-name:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CCodeGen.md#genericnodecname-default--genericnodesh) | Name of the include file containing the generic nodes (part of the pack) |
| [`app-nodes-c-name:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CCodeGen.md#appnodescname-default--appnodesh) | Name of the include file containing the application nodes    |
| [`scheduler-c-file-name:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CCodeGen.md#schedulercfilename-default--scheduler) | Name of the files containing the code for the scheduler and header for the scheduler |
| [`c-api:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CCodeGen.md#capi-default--true) | True when the API of the scheduler is callable from C        |
| [`cmsis-dsp:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CCodeGen.md#cmsisdsp-default--true) | True when CMSIS-DSP headers are included                     |
| [`asynchronous:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CCodeGen.md#asynchronous-default--false) | True when asynchronous mode is enabled                       |
| [`fifo-increase:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CCodeGen.md#fifoincrease-default-0) | In asynchronous mode, increase all FIFO sizes globally       |
| [`async-default-skip:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/CCodeGen.md#asyncdefaultskip-default-true) | Behavior of `Duplicate` nodes in asynchronous mode           |

### `python-code-generation-options:`

| Keyword                                                      | Description                                   |
| ------------------------------------------------------------ | --------------------------------------------- |
| [`py-optional-args:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/PythonGen.md#pyoptionalargs-default--) | Arguments for the Python API of the scheduler |
| [`custom-python-name:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/PythonGen.md#custompythonname-default--custom) | Name of the custom python file                |
| [`app-nodes-python-name:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/PythonGen.md#appnodespythonname-default--appnodes) | Name of the python application node files     |
| [`scheduler-python-file-name:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/PythonGen.md#schedulerpythonfilename-default--sched) | Name of the python scheduler file             |

### `graphviz-code-generation-options:`

| Keyword                                                      | Description                                     |
| ------------------------------------------------------------ | ----------------------------------------------- |
| [`horizontal:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/GraphvizGen.md#horizontal-default--true) | Horizontal layout for the graph                 |
| [`display-fifo-buf:`](https://github.com/ARM-software/CMSIS-DSP/blob/main/ComputeGraph/documentation/GraphvizGen.md#displayfifobuf-default--false) | Display FIFO buffer ID instead of the FIFO size |

## `version:`

This is a string representing the version of the Compute Graph file format used a YAML file.

It is using semantic versioning.