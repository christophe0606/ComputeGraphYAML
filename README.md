# Table of content

* [File structure](#File-Structure)
  * [`version:`](#version)
  * [`graph:`](#graph)
    * [`nodes:`](#nodes)
    * [`edges:`](#edges)
* [Node description](#node-description)
  * [`node:`](#node)
  * [`kind:`](#kind)
  * [`inputs:`](#io-port-description)
  * [`outputs:`](#io-port-description)

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


# File Structure

The table below explains the top-level elements of the yml graph description.

| Keyword                | Description                                                |
| ---------------------- | ---------------------------------------------------------- |
| [`version:`](#version) | Version of the Compute graph YAML format used by this file |
| [`graph:`](#graph)     | Description of the graph                                   |

## `version:`

This is a string representing the version of the Compute Graph file format used by the file.

It is using semantic versioning.

## `graph:`

Description of the graph. It contains the following:

| `graph:`           | Content                    |
| ------------------ | -------------------------- |
| [`nodes:`](#nodes) | List of nodes in the graph |
| [`edges:`](#edges) | List of edges in the graph |

**Examples:**

```yml
version: '1.0'
graph:
  nodes:
  ...
  edges:
  ...
```

### `nodes:`

List of [nodes](#nodes)

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

List of [edges](#edges).

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

| nodes:                       | Content                                  |
| ---------------------------- | ---------------------------------------- |
| [`node:`](#node-description) | The name of the node used to identify it |
| [`kind:`](#kind)             | The category of the node                 |
| [`inputs:`](#inputs)         | List of inputs for this node             |
| [`outputs:`](#output)        | List of outputs for this node            |

#### `node:`

Name of the node. It must be a valid C variable name. It is used to identify the node in the graph and in the generated C code

#### `kind:`

It is the name of the `C++` class template implementing the node. It must be a valid `C++` class name.

#### `inputs:`

List of [inputs](#input-or-output) for the node

#### `outputs:`

List of [outputs](#input-or-output) for the node

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

## Edge description

It contains the following:

| Keyword        | Content                       |
| -------------- | ----------------------------- |
| [`src:`](#src) | Source port for the edge      |
| [`dst:`](#dst) | Destination port for the edge |

**Examples:**

```yml
- src:
      node: source
      output: o
  dst:
      node: processing
      input: i
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

It can also be more complex datatypes defined with a C struct. More complex datatypes have to be define at the beginning of the graph description.