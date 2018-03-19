# virlutils

A collection of utilities for interacting with [Cisco VIRL](https://learningnetworkstore.cisco.com/virlfaq/aboutVirl)

## Features

### virl up


`virl` is a devops style cli which supports the most common VIRL operations.  Adding new ones is easy...

```
Usage: virl [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  console   console for node
  down      stop a virl simulation
  generate  generate inv file for various tools
  logs      Retrieves log information for the provided...
  ls        lists running simulations in the current...
  nodes     get nodes for sim_name
  save      save simulation to local virl file
  ssh       ssh to a node
  start     start a node
  stop      stop a node
  telnet    telnet to a node
  up        start a virl simulation
  use       use virl simulation launched elsewhere

```

#### Tab Completions


```
➜  test git:(test) virl l<tab>
logs  ls  

```

You can activate VIRL autocompletions by executing the following command

```
eval "$(_VIRL_COMPLETE=source virl)"
```

zsh users may need to run the following prior

```
autoload bashcompinit
bashcompinit
```

### Inventory Generation

virlutils will generate inventories for various management systems

#### pyATS Testbed Generation

quickly turn your simulations into a testbed file that can be used for pyATS/Genie

```
virl generate pyats
```

#### Ansible Inventory Generation

quickly turn your simulations into an inventory file that can be to run your playbooks
against

```
virl generate ansible
```

#### Cisco Network Services Orchestrator - COMING SOON!!

import your virl devices directly into Network services orchestrator, or generate CLI,API templates


```
virl generate nso [optional NSO URL for auto update]
```


<!-- TOC depthFrom:2 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Local Development](#local-development)
- [Testing](#testing)

<!-- /TOC -->

## Installation

1. Clone this repo

```
git clone https://github.com/kecorbin/virl_cli
```

2. Install

### With Pip

```
pip install virlutils
```

### Clone & Install
```
git clone https://github.com/kecorbin/virl_cli
cd virl_cli
virtualenv venv && source venv/bin/activate
python setup.py install
```

## Configuration

There really isn't much to configure, just set your VIRL credentials up.  
There are a few different ways to accomplish this, pick whichever one works best for you,
the options listed below are in the `preferred` order.  


#### .virlrc in working directory

Add a .virlrc to the working directory, this will always be checked first and
is useful when you want to override one or more parameters for a particular project
directory.

The contents would look something like this.

```
VIRL_HOST=specialvirlserver.foo.com
```


#### environment variables
You can also add them as environment variables. This is useful if you want to override
the global VIRL settings.

```
export VIRL_HOST=1.1.1.1
export VIRL_USERNAME=guest
export VIRL_PASSWORD=guest
```

#### .virlrc in your home directory

Configure VIRL credentials globally by putting them in ~/.virlrc the formatting

```
VIRL_USERNAME=netadmins
VIRL_PASSWORD=cancodetoo!
```


### Why so many choices??!?!

Understanding the precedence allows you to do some pretty cool things.

Assume the following directory structure...

```
.
├── dev
│   ├── .virlrc
│   └── topology.virl
├── prod
│   ├── .virlrc
│   └── topology.virl
└── test
    ├── .virlrc
    └── topology.virl

```

This allows three major benefits.  

1. you can easily use different credentials/servers for various environments
2. you can specify environment specific details into your .virl files if you need to. we find
this most useful in the context of out-of-band management networks/gateways and such.
3. you have a badass workflow..

```
(netdevops-demo) ➜  dev git:(test) ✗ virl ls  
Running Simulations
╒══════════════╤══════════╤════════════╤═══════════╕
│ Simulation   │ Status   │ Launched   │ Expires   │
╞══════════════╪══════════╪════════════╪═══════════╡
╘══════════════╧══════════╧════════════╧═══════════╛
(netdevops-demo) ➜  dev git:(test) ✗ cd ../test
(netdevops-demo) ➜  test git:(test) ✗ virl ls
Running Simulations
╒═════════════════════╤══════════╤════════════════════════════╤═══════════╕
│ Simulation          │ Status   │ Launched                   │ Expires   │
╞═════════════════════╪══════════╪════════════════════════════╪═══════════╡
│ test_default_hfMQHh │ ACTIVE   │ 2018-03-18T06:23:05.607199 │           │
╘═════════════════════╧══════════╧════════════════════════════╧═══════════╛
(netdevops-demo) ➜  test git:(test) ✗ cd ../prod
(netdevops-demo) ➜  prod git:(test) ✗ virl ls
Running Simulations
╒═════════════════════╤══════════╤════════════════════════════╤═══════════╕
│ Simulation          │ Status   │ Launched                   │ Expires   │
╞═════════════════════╪══════════╪════════════════════════════╪═══════════╡
│ prod_default_jbdKOW │ ACTIVE   │ 2018-03-18T06:18:04.635601 │           │
╘═════════════════════╧══════════╧════════════════════════════╧═══════════╛
```



### Demo Workflow

in the absence of better documentation, here's a sample workflow


```
(venv) KECORBIN-M-90Y9:virl_cli kecorbin$ virl ls

    Here is a list of all the running nodes

╒═════════════════╤══════════╤════════════════════════════╤═══════════╕
│ Simulation      │ Status   │ Launched                   │ Expires   │
╞═════════════════╪══════════╪════════════════════════════╪═══════════╡
│ topology-CoC73j │ ACTIVE   │ 2017-12-02T14:44:29.209647 │           │
╘═════════════════╧══════════╧════════════════════════════╧═══════════╛
(venv) KECORBIN-M-90Y9:virl_cli kecorbin$ virl up
Launching Simulation from topology.virl
virl_cli-GnMIWY


(venv) KECORBIN-M-90Y9:virl_cli kecorbin$ virl ls

    Here is a list of all the running nodes

╒═════════════════╤══════════╤════════════════════════════╤═══════════╕
│ Simulation      │ Status   │ Launched                   │ Expires   │
╞═════════════════╪══════════╪════════════════════════════╪═══════════╡
│ topology-CoC73j │ ACTIVE   │ 2017-12-02T14:44:29.209647 │           │
├─────────────────┼──────────┼────────────────────────────┼───────────┤
│ virl_cli-GnMIWY │ ACTIVE   │ 2017-12-08T07:35:46.444588 │           │
╘═════════════════╧══════════╧════════════════════════════╧═══════════╛


(venv) KECORBIN-M-90Y9:virl_cli kecorbin$ virl nodes virl_cli-GnMIWY

    Here is a list of all the running nodes

╒═══════════╤══════════╤══════════╤═════════════╤═══════════════════════╕
│ Node      │ Type     │ State    │ Reachable   │ management-protocol   │
╞═══════════╪══════════╪══════════╪═════════════╪═══════════════════════╡
│ iosv-2    │ IOSv     │ BUILDING │ False       │ telnet                │
├───────────┼──────────┼──────────┼─────────────┼───────────────────────┤
│ ~mgmt-lxc │ mgmt-lxc │ ACTIVE   │ True        │ ssh                   │
├───────────┼──────────┼──────────┼─────────────┼───────────────────────┤
│ iosv-1    │ IOSv     │ ACTIVE   │ False       │ telnet                │
╘═══════════╧══════════╧══════════╧═════════════╧═══════════════════════╛


(venv) KECORBIN-M-90Y9:virl_cli kecorbin$ virl console virl_cli-GnMIWY iosv-1
iosv-1
Attempting to connect to console of iosv-1
Trying 10.94.140.41...
Connected to mm-c1-6620.cisco.com.
Escape character is '^]'.

[OK] (elapsed time was 9 seconds)

Building configuration...

telnet> quit
Connection closed.


(venv) KECORBIN-M-90Y9:virl_cli kecorbin$ virl down virl_cli-GnMIWY
Shutting Down Simulation virl_cli-GnMIWY.....SUCCESS
(venv) KECORBIN-M-90Y9:virl_cli kecorbin$ virl ls

    Here is a list of all the running nodes

╒═════════════════╤══════════╤════════════════════════════╤═══════════╕
│ Simulation      │ Status   │ Launched                   │ Expires   │
╞═════════════════╪══════════╪════════════════════════════╪═══════════╡
│ topology-CoC73j │ ACTIVE   │ 2017-12-02T14:44:29.209647 │           │
├─────────────────┼──────────┼────────────────────────────┼───────────┤
│ virl_cli-GnMIWY │ STOP     │ 2017-12-08T07:35:46.444588 │           │
╘═════════════════╧══════════╧════════════════════════════╧═══════════╛

(venv) KECORBIN-M-90Y9:virl_cli kecorbin$ virl ls

    Here is a list of all the running nodes

╒═════════════════╤══════════╤════════════════════════════╤═══════════╕
│ Simulation      │ Status   │ Launched                   │ Expires   │
╞═════════════════╪══════════╪════════════════════════════╪═══════════╡
│ topology-CoC73j │ ACTIVE   │ 2017-12-02T14:44:29.209647 │           │
╘═════════════════╧══════════╧════════════════════════════╧═══════════╛

```
## Local Development

To easily get started, you can run this inside a docker container like so:

```
docker run --rm -it -v "$(pwd):/home" --workdir /home python:2.7 /bin/bash
root@ab89db25addf:/home# python setup.py install
....
root@ab89db25addf:/home# virl
```

### Testing

To run the tests in the `tests` folder, you can simply run `make test` from
the project root.
