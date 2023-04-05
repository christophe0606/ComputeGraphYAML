# Table of content

* [File structure](#File-Structure)
  * [`version:`](#version)
  * [`graph:`](#graph)
    * [`nodes:`](#nodes)
      * [`node:`](#node)
      * [`kind:`](#kind)
      * [`inputs:`](inputs)
        * `input:`
        * `samples:`
        * `type:`
      * [`outputs:`](#outputs)
        * `output:`
        * `samples:`
        * `type:`
    * [`edges:`](#edges)
      * [`src:`](#src)
        * `node:`
        * `output:`
      * [`dst:`](#dst)
        * `node:`
        * `input:`

# File Structure

The table below explains the top-level elements of the yml graph description.

| Keyword              | Description                                                |
| -------------------- | ---------------------------------------------------------- |
| [version:](#version) | Version of the Compute graph YAML format used by this file |
| [graph:](#graph)     | Description of the graph                                   |

## version:

This is a string representing the version of the Compute Graph file format used by the file.

It is using semantic versioning.

## graph:

Description of the graph. It contains the following:

| graph:           | Content                    |
| ---------------- | -------------------------- |
| [nodes:](#nodes) | List of nodes in the graph |
| [edges:](#edges) | List of edges in the graph |

### nodes:

Description of the nodes. It contains the following:

| nodes:              | Content                    |
| ------------------- | -------------------------- |
| [node:](#node)      |                            |
| [kind:](#kind)      |                            |
| [inputs:](#inputs)  | List of nodes in the graph |
| [outputs:](#output) | List of edges in the graph |

#### node:

#### kind:

#### inputs:

| inputs:              | Content                    |
| -------------------- | -------------------------- |
| [input:](#input)     | List of nodes in the graph |
| [samples:](#samples) | List of edges in the graph |
| [type:](#type)       |                            |

#### outputs:

| outputs:             | Content                    |
| -------------------- | -------------------------- |
| [output:](#output)   | List of nodes in the graph |
| [samples:](#samples) | List of edges in the graph |
| [type:](#type)       |                            |

### edges:

Description of the edges. It contains the following:

| edges:       | Content                    |
| ------------ | -------------------------- |
| [src:](#src) | List of nodes in the graph |
| [dst:](#dst) | List of edges in the graph |

#### src:

#### dst: