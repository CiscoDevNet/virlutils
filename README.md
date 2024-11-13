# virlutils

[![Build Status](https://travis-ci.org/CiscoDevNet/virlutils.svg?branch=master)](https://travis-ci.org/CiscoDevNet/virlutils)
[![Coverage Status](https://coveralls.io/repos/github/CiscoDevNet/virlutils/badge.svg?branch=master)](https://coveralls.io/github/CiscoDevNet/virlutils?branch=master)
[![PyPI version](https://badge.fury.io/py/virlutils.svg)](https://badge.fury.io/py/virlutils)

A collection of utilities for interacting with [Cisco Modeling Labs (CML)](https://developer.cisco.com/modeling-labs) v2.6+.

## virl up / cml up

`virl` (or `cml`) is a devops style cli which supports the most common VIRL/CML operations. Adding new ones is easy...

```sh
Usage: cml [OPTIONS] COMMAND [ARGS]...

Options:
  --debug / --no-debug  Print any debugging output.
  --help                Show this message and exit.

Commands:
  clear        clear the current lab ID
  cluster      display and manage CML cluster details
  cockpit      opens the Cockpit UI
  command      send a command or config to a node (requires pyATS)
  console      console for node
  definitions  manage image and node definitions
  down         stop a lab
  extract      extract configurations from all nodes in a lab
  generate     generate inv file for various tools
  groups       manage groups
  id           get the current lab title and ID
  license      work with product licensing
  ls           lists running labs and optionally those in the cache
  nodes        get node list for the current lab
  pull         pull topology.yaml from repo
  rm           remove a lab
  save         save lab to a local yaml file
  search       list topologies available via github
  ssh          ssh to a node
  start        start a node
  stop         stop a node
  telnet       telnet to a node
  tmux         console to all nodes using tmux
  ui           opens the Workbench for the current lab
  up           start a lab
  use          use lab launched elsewhere
  users        manage users
  version      version information
  wipe         wipe a lab or nodes within a lab
```

<!-- TOC depthFrom:2 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage / Workflows](#usage--workflows)
- [Contributing](#contributing)

<!-- /TOC -->

## Prerequisites

- Python 3.8+ (tested with Python 3.8, 3.9, 3.10, 3.11 and 3.12)

## Installation

1.Clone this repo

```sh
git clone https://github.com/CiscoDevNet/virlutils
cd virlutils
```

2.Either (2a) use pip, or (2b) use setup.py

2a. Use pip

```sh
pip install cmlutils
```

Or

```sh
pip install virlutils
```

2b. Use setup.py

```sh
python3 -m venv venv
source venv/bin/activate
python setup.py install
```

## Configuration

There really isn't much to configure, just set your CML credentials. There are a few different ways to accomplish this, pick whichever one works best for you. The options listed below are in the `preferred` order.

### .virlrc in working directory

Add a .virlrc to the working directory, this will always be checked first and
is useful when you want to override one or more parameters for a particular project
directory.

The contents would look something like this.

```sh
VIRL_HOST=specialvirlserver.foo.com
```

### environment variables

You can also add them as environment variables. This is useful if you want to override
the global VIRL settings.

```sh
export VIRL_HOST=192.0.2.100
export VIRL_USERNAME=admin
export VIRL_PASSWORD=admin123
```

### .virlrc in your home directory

Configure VIRL credentials globally by putting them in ~/.virlrc the formatting

```sh
VIRL_USERNAME=netadmins
VIRL_PASSWORD=cancodetoo!
```

### Other configuration options

In addition to basic credentials, the following configuration options are supported
using any of the methods mentioned previously

- `VIRL_TELNET_COMMAND` - allows the user to customize the telnet command that is called.
  This command will be passed the host/ip information from the running simulation

  Example:

  ```sh
  export VIRL_TELNET_COMMAND="mytelnet {host}"
  ```

- `VIRL_SSH_COMMAND` - allows the user to customize the ssh command that is called.
  This command will be passed the host/ip as well as the username from the running simulation

  Example:

  ```sh
  export VIRL_SSH_COMMAND="myssh {username}@{host}"
  ```

- `CML_VERIFY_CERT` - The path to a PEM-encoded certificate file to use to verify the CML controller VM's SSL certificate. If you do not wish to verify the certificate, set this to "False"

  Example:

  ```sh
  export CML_VERIFY_CERT=/etc/certs/ca_bundle.pem
  ```

- `CML_CONSOLE_COMMAND` - allows the user to customize the SSH command that is called.

  This command will be passed the CML controller VM IP, the console path of the node, and the CML controller username (**note:** you may have to force a TTY allocation in your SSH command)

  Example:

  ```sh
  export CML_CONSOLE_COMMAND="myssh {user}@{host} {console}"
  ```

- `CML_PLUGIN_PATH` - A delimiter-separated list of directories in which to find cmlutils plugins. See the [plugin documentation](examples/plugins/README.md) for more details. By default, the `plugins` directory in the current `.virl` directory will be searched.

  Example:

  ```sh
  export CML_PLUGIN_PATH="~/cmlutils/plugins:/opt/cmlutils/plugins"
  ```

### Why so many choices??!?

Understanding the precedence allows you to do some pretty cool things.

Assume the following directory structure...

```plain
.
├── dev
│   ├── .virlrc
│   └── topology.yaml
├── prod
│   ├── .virlrc
│   └── topology.yaml
└── test
    ├── .virlrc
    └── topology.yaml

```

This allows three major benefits.

1. you can easily use different credentials/servers for various environments
2. you can customize your lab .yaml files to include different tags, different node configurations, etc.
3. you have a badass workflow.

```sh
$ cml ls
Labs on Server
╒═══════════════╤════════════════════════╤═══════════════╤══════════╤══════════╤═════════╤═════════╤══════════════╕
│ ID            │ Title                  │ Description   │ Owner    │ Status   │   Nodes │   Links │   Interfaces │
╞═══════════════╪════════════════════════╪═══════════════╪══════════╪══════════╪═════════╪═════════╪══════════════╡
│               │                        │               │          │          │         │         │              │
╘═══════════════╧════════════════════════╧═══════════════╧══════════╧══════════╧═════════╧═════════╧══════════════╛
$ cd ../test
$ cml ls
Labs on Server
╒══════════════════════════════════════╤════════════════════════════════╤═════════════════════════════════════════╤══════════╤═════════════════╤═════════╤═════════╤══════════════╕
│ ID                                   │ Title                          │ Description                             │ Owner    │ Status          │   Nodes │   Links │   Interfaces │
╞══════════════════════════════════════╪════════════════════════════════╪═════════════════════════════════════════╪══════════╪═════════════════╪═════════╪═════════╪══════════════╡
│ f25b3881-0d19-4a6d-816f-36d1c663f930 │ Multi Platform Network         │ A sample network built with IOS XE, NX- │ labuser  │ STOPPED         │      14 │      32 │          101 │
│                                      │                                │ OS, IOS XR, and ASA devices.  Includes  │          │                 │         │         │              │
│                                      │                                │ Linux hosts.                            │          │                 │         │         │              │
╘══════════════════════════════════════╧════════════════════════════════╧═════════════════════════════════════════╧══════════╧═════════════════╧═════════╧═════════╧══════════════╛
$ cd ../prod
$ cml ls
Labs on Server
╒══════════════════════════════════════╤════════════════════════════════╤═════════════════════════════════════════╤══════════╤═════════════════╤═════════╤═════════╤══════════════╕
│ ID                                   │ Title                          │ Description                             │ Owner    │ Status          │   Nodes │   Links │   Interfaces │
╞══════════════════════════════════════╪════════════════════════════════╪═════════════════════════════════════════╪══════════╪═════════════════╪═════════╪═════════╪══════════════╡
│ 0fdea012-83b4-4545-8747-c7b8037e5a96 │ Multi Platform Network         │ A sample network built with IOS XE, NX- │ labuser  │ STARTED         │      14 │      32 │          101 │
│                                      │                                │ OS, IOS XR, and ASA devices.  Includes  │          │                 │         │         │              │
│                                      │                                │ Linux hosts.                            │          │                 │         │         │              │
╘══════════════════════════════════════╧════════════════════════════════╧═════════════════════════════════════════╧══════════╧═════════════════╧═════════╧═════════╧══════════════╛
```

## Usage / Workflows

### Basic Workflow

in the absence of better documentation, here's a sample workflow

```sh
[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml ls
Labs on Server
╒══════════════════════════════════════╤════════════════════════════════╤═════════════════════════════════════════╤══════════╤═════════════════╤═════════╤═════════╤══════════════╕
│ ID                                   │ Title                          │ Description                             │ Owner    │ Status          │   Nodes │   Links │   Interfaces │
╞══════════════════════════════════════╪════════════════════════════════╪═════════════════════════════════════════╪══════════╪═════════════════╪═════════╪═════════╪══════════════╡
│ 35c5393b-6037-4c96-86d4-33f96e53a615 │ CCIE Enterprise Infrastructure │                                         │ labuser  │ DEFINED_ON_CORE │      54 │      67 │           216│
├──────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ a5fa67e3-44b9-4b26-8a50-58d471766280 │ Branch Test                    │                                         │ labuser  │ STOPPED         │       6 │       5 │           17 │
├──────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 931b20a1-f0be-4c9f-b7ef-4db96ee77135 │ Small Branch                   │ A small branch network built with CSR1kv│ labuser  │ STOPPED         │      14 │      32 │          101 │
│                                      │                                │ IOSv, IOSvL2. The devices are managed by│          │                 │         │         │              │
│                                      │                                │ NSO.                                    │          │                 │         │         │              │
├──────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 8e8047b6-faf8-4b0a-86ea-c05a0549e4fe │ Dynamic Split Tunnel           │                                         │ labuser  │ STOPPED         │       7 │       9 │           37 │
├──────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 86ef940d-58e8-49d9-b154-22ec714add62 │ Lab at Tue 14:45 PM            │                                         │ labuser  │ STOPPED         │       3 │       2 │           14 │
├──────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ ba9a1282-048f-4914-a419-59c8027afa6a │ DFN                            │ German Research Network                 │ labuser  │ STARTED         │      51 │      80 │          211 │
╘══════════════════════════════════════╧════════════════════════════════╧═════════════════════════════════════════╧══════════╧═════════════════╧═════════╧═════════╧══════════════╛

[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml use --lab-name "Small Branch"

[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml id
Small Branch (ID: 931b20a1-f0be-4c9f-b7ef-4db96ee77135)

[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml up
Lab Small Branch (ID: 931b20a1-f0be-4c9f-b7ef-4db96ee77135) is already set as the current lab
Starting lab Small Branch (ID: 931b20a1-f0be-4c9f-b7ef-4db96ee77135)


[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml ls
Labs on Server
╒══════════════════════════════════════╤════════════════════════════════╤═════════════════════════════════════════╤══════════╤═════════════════╤═════════╤═════════╤══════════════╕
│ ID                                   │ Title                          │ Description                             │ Owner    │ Status          │   Nodes │   Links │   Interfaces │
╞══════════════════════════════════════╪════════════════════════════════╪═════════════════════════════════════════╪══════════╪═════════════════╪═════════╪═════════╪══════════════╡
│ 35c5393b-6037-4c96-86d4-33f96e53a615 │ CCIE Enterprise Infrastructure │                                         │ labuser  │ DEFINED_ON_CORE │      54 │      67 │           216│
├──────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ a5fa67e3-44b9-4b26-8a50-58d471766280 │ Branch Test                    │                                         │ labuser  │ STOPPED         │       6 │       5 │           17 │
├──────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 931b20a1-f0be-4c9f-b7ef-4db96ee77135 │ Small Branch                   │ A small branch network built with CSR1kv│ labuser  │ STARTED         │      14 │      32 │          101 │
│                                      │                                │ IOSv, IOSvL2. The devices are managed by│          │                 │         │         │              │
│                                      │                                │ NSO.                                    │          │                 │         │         │              │
├──────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 8e8047b6-faf8-4b0a-86ea-c05a0549e4fe │ Dynamic Split Tunnel           │                                         │ labuser  │ STOPPED         │       7 │       9 │           37 │
├──────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 86ef940d-58e8-49d9-b154-22ec714add62 │ Lab at Tue 14:45 PM            │                                         │ labuser  │ STOPPED         │       3 │       2 │           14 │
├──────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ ba9a1282-048f-4914-a419-59c8027afa6a │ DFN                            │ German Research Network                 │ labuser  │ STARTED         │      51 │      80 │          211 │
╘══════════════════════════════════════╧════════════════════════════════╧═════════════════════════════════════════╧══════════╧═════════════════╧═════════╧═════════╧══════════════╛


[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml nodes
Here is a list of nodes in this lab
╒══════════════════════════════════════╤════════════════════╤════════════════════╤════════════════╤═════════════════╤══════════╤══════════════════════════════════════╕
│ ID                                   │ Label              │ Type               │ Compute Node   │ State           │ Wiped?   │ L3 Address(es)                       │
╞══════════════════════════════════════╪════════════════════╪════════════════════╪════════════════╪═════════════════╪══════════╪══════════════════════════════════════╡
│ 32135ea1-d6f4-4ae5-94cb-8dfa14c0b758 │ Internet           │ external_connector │ compute-01     │ BOOTED          │ False    │                                      │
├──────────────────────────────────────┼────────────────────┼────────────────────┼────────────────┼─────────────────┼──────────┼──────────────────────────────────────┤
│ e6ed74ef-62bf-4f4c-8fe8-a44fb3bc74c4 │ branch-rtr         │ csr1000v           │ compute-01     │ BOOTED          │ False    │ 192.168.10.129                       │
├──────────────────────────────────────┼────────────────────┼────────────────────┼────────────────┼─────────────────┼──────────┼──────────────────────────────────────┤
│ a01784b1-d11f-4c52-907b-b6ac92d3b8f1 │ branch-sw          │ iosvl2             │ compute-01     │ BOOTED          │ False    │ 192.168.10.143                       │
├──────────────────────────────────────┼────────────────────┼────────────────────┼────────────────┼─────────────────┼──────────┼──────────────────────────────────────┤
│ 84625ab4-53dd-4ff4-8cd1-2a2ef94edc02 │ nso-0              │ nso_ubuntu         │ compute-01     │ BOOTED          │ False    │ 2001:db8:dead:beef:5054:ff:fe11:a168 │
│                                      │                    │                    │                │                 │          │ fe80::5054:ff:fe11:a168              │
├──────────────────────────────────────┼────────────────────┼────────────────────┼────────────────┼─────────────────┼──────────┼──────────────────────────────────────┤
│ 579a9e46-3433-4645-9bad-c84106d9cd54 │ remote-rtr         │ iosv               │ compute-01     │ BOOTED          │ False    │ 192.168.10.137                       │
╘══════════════════════════════════════╧════════════════════╧════════════════════╧════════════════╧═════════════════╧══════════╧══════════════════════════════════════╛

[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml console branch-rtr
admin@192.168.10.214's password:
Connecting to console for
Connected to terminalserver.
Escape character is '^]'.

branch-rtr#
branch-rtr#
branch-rtr#
branch-rtr#


[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml down
Shutting down lab Small Branch (ID: 931b20a1-f0be-4c9f-b7ef-4db96ee77135).....
SUCCESS

[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml ls
Labs on Server
╒══════════════════════════════════════╤════════════════════════════════╤═════════════════════════════════════════╤══════════╤═════════════════╤═════════╤═════════╤══════════════╕
│ ID                                   │ Title                          │ Description                             │ Owner    │ Status          │   Nodes │   Links │   Interfaces │
╞══════════════════════════════════════╪════════════════════════════════╪═════════════════════════════════════════╪══════════╪═════════════════╪═════════╪═════════╪══════════════╡
│ 35c5393b-6037-4c96-86d4-33f96e53a615 │ CCIE Enterprise Infrastructure │                                         │ labuser  │ DEFINED_ON_CORE │      54 │      67 │           216│
├──────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ a5fa67e3-44b9-4b26-8a50-58d471766280 │ Branch Test                    │                                         │ labuser  │ STOPPED         │       6 │       5 │           17 │
├──────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 931b20a1-f0be-4c9f-b7ef-4db96ee77135 │ Small Branch                   │ A small branch network built with CSR1kv│ labuser  │ STOPPED         │      14 │      32 │          101 │
│                                      │                                │ IOSv, IOSvL2. The devices are managed by│          │                 │         │         │              │
│                                      │                                │ NSO.                                    │          │                 │         │         │              │
├──────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 8e8047b6-faf8-4b0a-86ea-c05a0549e4fe │ Dynamic Split Tunnel           │                                         │ labuser  │ STOPPED         │       7 │       9 │           37 │
├──────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 86ef940d-58e8-49d9-b154-22ec714add62 │ Lab at Tue 14:45 PM            │                                         │ labuser  │ STOPPED         │       3 │       2 │           14 │
├──────────────────────────────────────┼────────────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ ba9a1282-048f-4914-a419-59c8027afa6a │ DFN                            │ German Research Network                 │ labuser  │ STARTED         │      51 │      80 │          211 │
╘══════════════════════════════════════╧════════════════════════════════╧═════════════════════════════════════════╧══════════╧═════════════════╧═════════╧═════════╧══════════════╛

[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml nodes
Here is a list of nodes in this lab
╒══════════════════════════════════════╤════════════════════╤════════════════════╤════════════════╤═════════════════╤══════════╤══════════════════════════════════════╕
│ ID                                   │ Label              │ Type               │ Compute Node   │ State           │ Wiped?   │ L3 Address(es)                       │
╞══════════════════════════════════════╪════════════════════╪════════════════════╪════════════════╪═════════════════╪══════════╪══════════════════════════════════════╡
│ 32135ea1-d6f4-4ae5-94cb-8dfa14c0b758 │ Internet           │ external_connector │ compute-01     │ STOPPED         │ False    │                                      │
├──────────────────────────────────────┼────────────────────┼────────────────────┼────────────────┼─────────────────┼──────────┼──────────────────────────────────────┤
│ e6ed74ef-62bf-4f4c-8fe8-a44fb3bc74c4 │ branch-rtr         │ csr1000v           │ compute-01     │ STOPPED         │ False    │                                      │
├──────────────────────────────────────┼────────────────────┼────────────────────┼────────────────┼─────────────────┼──────────┼──────────────────────────────────────┤
│ a01784b1-d11f-4c52-907b-b6ac92d3b8f1 │ branch-sw          │ iosvl2             │ compute-01     │ STOPPED         │ False    │                                      │
├──────────────────────────────────────┼────────────────────┼────────────────────┼────────────────┼─────────────────┼──────────┼──────────────────────────────────────┤
│ 84625ab4-53dd-4ff4-8cd1-2a2ef94edc02 │ nso-0              │ nso_ubuntu         │ compute-01     │ STOPPED         │ False    │                                      │
│                                      │                    │                    │                │                 │          │                                      │
├──────────────────────────────────────┼────────────────────┼────────────────────┼────────────────┼─────────────────┼──────────┼──────────────────────────────────────┤
│ 579a9e46-3433-4645-9bad-c84106d9cd54 │ remote-rtr         │ iosv               │ compute-01     │ STOPPED         │ False    │                                      │
╘══════════════════════════════════════╧════════════════════╧════════════════════╧════════════════╧═════════════════╧══════════╧══════════════════════════════════════╛
```

### Console to All Nodes with tmux

If you are a `tmux` user you can console to all nodes with the following command:

```sh
❯ cml tmux --help
Usage: cml tmux [OPTIONS]

  console to all nodes using tmux

Options:
  --group [panes|windows]  'panes': group all nodes in one window, 'windows':
                           one node per window  [default: panes]
  --help                   Show this message and exit.

❯ cml nodes
Here is a list of nodes in this lab
╒══════════════════════════════════════╤════════════════════╤════════════════════╤════════════════╤═════════╤══════════╤══════════════════╕
│ ID                                   │ Label              │ Type               │ Compute Node   │ State   │ Wiped?   │ L3 Address(es)   │
╞══════════════════════════════════════╪════════════════════╪════════════════════╪════════════════╪═════════╪══════════╪══════════════════╡
│ 5fdb38b6-7ff7-4792-b685-5eeaa41d8865 │ c8v-2              │ cat8000v           │ cml-01         │ BOOTED  │ False    │                  │
├──────────────────────────────────────┼────────────────────┼────────────────────┼────────────────┼─────────┼──────────┼──────────────────┤
│ 7bdedc4a-a196-4ad0-b1f3-888cf77eee8b │ c8v-1              │ cat8000v           │ cml-01         │ BOOTED  │ False    │                  │
├──────────────────────────────────────┼────────────────────┼────────────────────┼────────────────┼─────────┼──────────┼──────────────────┤
│ ab3ee63d-109d-424e-a2c0-7581a61b1d1d │ unmanaged-switch-0 │ unmanaged_switch   │ cml-01         │ BOOTED  │ False    │                  │
├──────────────────────────────────────┼────────────────────┼────────────────────┼────────────────┼─────────┼──────────┼──────────────────┤
│ 9a068ec0-0565-44a0-bf16-8e4690108ac9 │ ext-conn-0         │ external_connector │ cml-01         │ BOOTED  │ False    │                  │
╘══════════════════════════════════════╧════════════════════╧════════════════════╧════════════════╧═════════╧══════════╧══════════════════╛
```

This will create a new tmux session with title "lab name + first 4 lab id chars" (e.g. `PPK-c93a`).
By default, the nodes will be grouped into one window (`cml tmux --group panes`),

```sh
❯  printf '\033]2;%s\033\\' 'c8v-2'
❯  ssh -t admin@cml-01 open /PPK/c8v-2/0
admin@cml-01's password:
Connecting to console for c8v-2
Connected to CML terminalserver.
Escape character is '^]'.

c8v2#
─────────────────────────────────────────────────────────────────────────
❯  printf '\033]2;%s\033\\' 'c8v-1'
❯  ssh -t admin@cml-01 open /PPK/c8v-1/0
admin@cml-01's password:
Connecting to console for c8v-1
Connected to CML terminalserver.
Escape character is '^]'.

c8v1#
 PPK-c93a >> 1 > ssh >                                     < 20:20
```

> Note: the command `printf '\033]2;%s\033\\' 'c8v-2'` is used to set the pane's title see: [tmux man](https://man7.org/linux/man-pages/man1/tmux.1.html#NAMES_AND_TITLES)

if you prefer having one connection per window, use: `cml tmux --group windows`.

```sh
❯  ssh -t admin@cml-01 open /PPK/c8v-2/0
admin@cml-01's password:
Connecting to console for c8v-2
Connected to CML terminalserver.
Escape character is '^]'.

c8v2#














 PPK-c93a >> 1 > c8v-2 >> 2 > c8v-1 >                      < 20:32
```

### Inventory Generation

virlutils will generate inventories for various management systems

#### pyATS Testbed Generation

quickly turn your simulations into a testbed file that can be used for pyATS/Genie

```sh
cml generate pyats
```

#### Command and Config Execution

Using the same pyATS framework, `virlutils` can execute CLI EXEC-level (e.g., "show") commands as well as configuration commands on nodes within a lab. These nodes do not have to be externally reachable or have any IP connectivity. This is a great way to test operational aspects of a completely isolated topology. Before using the `command` command you must install pyATS. You can install pyATS by running `pip install pyats`.

```sh
[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒ cml command "branch-rtr" "show version"
Cisco IOS XE Software, Version 16.11.01b
Cisco IOS Software [Gibraltar], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.11.1b, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
...
```

```sh
[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒ cml command --config "branch-rtr" "snmp-server community notpublic"

```

#### EVE-NG Lab Support

The `cml up` command can convert EVE-NG labs to CML labs on the fly (".unl" to ".yaml" conversion) if you install the
[eve2cml](https://pypi.org/project/eve2cml/) Python package.  With that library package, a command such as
`cml up -f my-lab.unl` will convert `my-lab.unl` to `my-lab.yaml` in the same directory and import it into CML.

#### Ansible Inventory Generation

quickly turn your simulations into an inventory file that can be used to run your playbooks
against. Both INI and YAML(default) formats are supported by the tool.

```sh
Usage: cml generate ansible [OPTIONS]

  generate ansible inventory

Options:
  -o, --output TEXT   output File name
  --style [ini|yaml]  output format (default is yaml)
  --help              Show this message and exit.
```

The ansible group membership can be controlled by adding the "ansible_group" tag to nodes in your CML labs. Multiple "ansible_group" tags can be assigned to a single node, and that node will be placed into each Ansible inventory group.

```yaml
nodes:
  - id: n0
    label: branch-rtr
    node_definition: csr1000v
    tags:
      - ansible_group=mygroup
```

would result in the following inventory entry

```yaml
all:
  children:
    mygroup:
      hosts:
        branch-router:
          ansible_host: 192.0.2.1
```

**NOTE:** if the ansible_group tag is not specified for a node, that node will not be included during inventory generation. Additionally, CML needs to know each node's management IP address before it will be placed into the inventory file

#### Cisco Network Services Orchestrator

You can add/update Network Services Orchestrator with your VIRL simulation.

Usage

```sh
Usage: cml generate nso [OPTIONS]

  generate nso inventory

Options:
  -o, --output TEXT           just dump the payload to file without sending
  --syncfrom / --no-syncfrom  Perform sync-from after updating devices
  --help                      Show this message and exit.
```

output

```sh
Updating NSO....
Enter NSO IP/Hostname: localhost
Enter NSO username: admin
Enter NSO password:
Successfully added CML devices to NSO

```

**NOTE**: NSO environment is also attempted to be determined using the following environment
variables

- NSO_HOST
- NSO_USERNAME
- NSO_PASSWORD

NSO Configuration Example

```sh
export NSO_HOST=localhost
export NSO_USERNAME=admin
export NSO_PASSWORD=admin
```

### User and Group Management

You can manage users and groups too!

#### Users

To manage users you can use the `cml users` command

``` sh
❯ cml users
Usage: cml users [OPTIONS] COMMAND [ARGS]...

  manage users

Options:
  --help  Show this message and exit.

Commands:
  create  Create one or more users (e.g., user1 user2)
  delete  Delete one or more users (e.g., user1 user2)
  ls      List all users on the server.
  update  Update one or more users (e.g., user1 user2)
```

To list users

```sh
❯ cml users ls
╒════════════╤═════════════════╤═════════════╤═════════╤════════════╤════════════════════════╕
│ Username   │ Administrator   │ Full Name   │ Email   │ Groups     │ Labs                   │
╞════════════╪═════════════════╪═════════════╪═════════╪════════════╪════════════════════════╡
│ admin      │ True            │             │         │ users      │ BGP                    │
│            │                 │             │         │ superusers │                        │
├────────────┼─────────────────┼─────────────┼─────────┼────────────┼────────────────────────┤
│ john       │ False           │ Uncle John  │         │ users      │ OSPF                   │
├────────────┼─────────────────┼─────────────┼─────────┼────────────┼────────────────────────┤
│ chuck      │ False           │ Uncle Chuck │         │            │                        │
╘════════════╧═════════════════╧═════════════╧═════════╧════════════╧════════════════════════╛
```

By default, user IDs are not shown, to display them use the `--verbose` or `-v` flag:

```sh
❯ cml users ls --verbose
Users on Server
╒══════════════════════════════════════╤════════════╤═════════════════╤═════════════╤═════════╤════════════╤════════════════════════╕
│ ID                                   │ Username   │ Administrator   │ Full Name   │ Email   │ Groups     │ Labs                   │
╞══════════════════════════════════════╪════════════╪═════════════════╪═════════════╪═════════╪════════════╪════════════════════════╡
│ 00000000-0000-4000-a000-000000000000 │ admin      │ True            │             │         │ users      │ BGP                    │
│                                      │            │                 │             │         │ superusers │                        │
├──────────────────────────────────────┼────────────┼─────────────────┼─────────────┼─────────┼────────────┼────────────────────────┤
│ 9e4e75b4-aaab-47af-9edb-9364460a81ae │ john       │ False           │ Uncle John  │         │ users      │ OSPF                   │
├──────────────────────────────────────┼────────────┼─────────────────┼─────────────┼─────────┼────────────┼────────────────────────┤
│ dcc96fe1-8cba-4227-9aa6-b41d5ff91e3a │ chuck      │ True            │ Uncle Chuck │         │            │                        │
╘══════════════════════════════════════╧════════════╧═════════════════╧═════════════╧═════════╧════════════╧════════════════════════╛
```

You can create one or multiple users. For each user, you will be prompted for the password and confirmation.
Optionally, you can grant admin privileges and add the users to one or more groups.

``` sh
❯ cml users create alice bob --admin --group users --superusers
Enter alice's password:
Re-Enter alice's password:
User alice successfully created
Enter bob's password:
Re-Enter bob's password:
User bob successfully created


❯ cml users ls
╒════════════╤═════════════════╤═════════════╤═════════╤════════════╤════════════════════════╕
│ Username   │ Administrator   │ Full Name   │ Email   │ Groups     │ Labs                   │
╞════════════╪═════════════════╪═════════════╪═════════╪════════════╪════════════════════════╡
│ admin      │ True            │             │         │ users      │ BGP                    │
│            │                 │             │         │ superusers │                        │
├────────────┼─────────────────┼─────────────┼─────────┼────────────┼────────────────────────┤
│ john       │ False           │ Uncle John  │         │ users      │ OSPF                   │
├────────────┼─────────────────┼─────────────┼─────────┼────────────┼────────────────────────┤
│ chuck      │ False           │ Uncle Chuck │         │            │                        │
├────────────┼─────────────────┼─────────────┼─────────┼────────────┼────────────────────────┤
│ alice      │ True            │             │         │ users      │                        │
│            │                 │             │         │ superusers │                        │
├────────────┼─────────────────┼─────────────┼─────────┼────────────┼────────────────────────┤
│ bob        │ True            │             │         │ users      │                        │
│            │                 │             │         │ superusers │                        │
╘════════════╧═════════════════╧═════════════╧═════════╧════════════╧════════════════════════╛
```

You can also update one or more existing users (e.g. removing admin privileges)

``` sh
❯ cml users update alice bob --no-admin --remove-from-all-groups
User alice successfully updated
User bob successfully updated

❯ cml users ls
╒════════════╤═════════════════╤═════════════╤═════════╤════════════╤════════════════════════╕
│ Username   │ Administrator   │ Full Name   │ Email   │ Groups     │ Labs                   │
╞════════════╪═════════════════╪═════════════╪═════════╪════════════╪════════════════════════╡
│ admin      │ True            │             │         │ users      │ BGP                    │
│            │                 │             │         │ superusers │                        │
├────────────┼─────────────────┼─────────────┼─────────┼────────────┼────────────────────────┤
│ john       │ False           │ Uncle John  │         │ users      │ OSPF                   │
├────────────┼─────────────────┼─────────────┼─────────┼────────────┼────────────────────────┤
│ chuck      │ False           │ Uncle Chuck │         │            │                        │
├────────────┼─────────────────┼─────────────┼─────────┼────────────┼────────────────────────┤
│ alice      │ False           │             │         │            │                        │
├────────────┼─────────────────┼─────────────┼─────────┼────────────┼────────────────────────┤
│ bob        │ False           │             │         │            │                        │
╘════════════╧═════════════════╧═════════════╧═════════╧════════════╧════════════════════════╛
```

Check the cli help for more options.

To delete one or multiple users.

``` sh
❯ cml users delete alice bob
User alice successfully deleted
User bob successfully deleted

❯ cml users ls
╒════════════╤═════════════════╤═════════════╤═════════╤════════════╤════════════════════════╕
│ Username   │ Administrator   │ Full Name   │ Email   │ Groups     │ Labs                   │
╞════════════╪═════════════════╪═════════════╪═════════╪════════════╪════════════════════════╡
│ admin      │ True            │             │         │ users      │ BGP                    │
│            │                 │             │         │ superusers │                        │
├────────────┼─────────────────┼─────────────┼─────────┼────────────┼────────────────────────┤
│ john       │ False           │ Uncle John  │         │ users      │ OSPF                   │
├────────────┼─────────────────┼─────────────┼─────────┼────────────┼────────────────────────┤
│ chuck      │ False           │ Uncle Chuck │         │            │                        │
╘════════════╧═════════════════╧═════════════╧═════════╧════════════╧════════════════════════╛
```

#### Groups

To manage groups you can use the `cml groups` command

``` sh
❯ cml groups --help
Usage: cml groups [OPTIONS] COMMAND [ARGS]...

  manage groups

Options:
  --help  Show this message and exit.

Commands:
  create  Create one or more groups (e.g., group1 group2)
  delete  Delete one or more groups (e.g., group1 group2)
  ls      List all groups on the server
  update  Update one or more groups (e.g., group1 group2)
```

To list groups

``` sh
❯ cml groups ls
Groups on Server
╒════════════╤═══════════════╤═════════╤════════════════════════════════════╕
│ Name       │ Description   │ Users   │ Labs                               │
╞════════════╪═══════════════╪═════════╪════════════════════════════════════╡
│ users      │ All Users     │ admin   │ netbox (read_only)                 │
│            │               │ john    │ Multi Platform Network (read_only) │
│            │               │         │ BFD (read_only)                    │
├────────────┼───────────────┼─────────┼────────────────────────────────────┤
│ superusers │ Superusers    │ admin   │                                    │
╘════════════╧═══════════════╧═════════╧════════════════════════════════════╛
```

You can create one or more groups and assign them to multiple labs or members.

``` sh
❯ cml ls
Labs on Server
╒══════════════════════════════════════╤════════════════════════╤═════════════════════════════════════════╤══════════╤══════════╤═════════╤═════════╤══════════════╕
│ ID                                   │ Title                  │ Description                             │ Owner    │ Status   │   Nodes │   Links │   Interfaces │
╞══════════════════════════════════════╪════════════════════════╪═════════════════════════════════════════╪══════════╪══════════╪═════════╪═════════╪══════════════╡
│ ba9a1282-048f-4914-a419-59c8027afa6a │ Quantum IPsec          │                                         │ admin    │ STOPPED  │       5 │       4 │           20 │
├──────────────────────────────────────┼────────────────────────┼─────────────────────────────────────────┼──────────┼──────────┼─────────┼─────────┼──────────────┤
│ 0786b045-aa39-4e98-af01-575b22566cf2 │ Multi-SA HSRP          │                                         │ admin    │ STARTED  │      10 │      13 │           47 │
╘══════════════════════════════════════╧════════════════════════╧═════════════════════════════════════════╧══════════╧══════════╧═════════╧═════════╧══════════════╛

❯ cml groups create --member alice --member bob --member mike --lab ba9a1282-048f-4914-a419-59c8027afa6a read_only --lab 0786b045-aa39-4e98-af01-575b22566cf2 read_write cryptopals
Group cryptopals successfully created

❯ cml groups ls
Groups on Server
╒════════════╤═══════════════╤═════════╤════════════════════════════════════╕
│ Name       │ Description   │ Users   │ Labs                               │
╞════════════╪═══════════════╪═════════╪════════════════════════════════════╡
│ users      │ All Users     │ admin   │ netbox (read_only)                 │
│            │               │ john    │ Multi Platform Network (read_only) │
│            │               │         │ BFD (read_only)                    │
├────────────┼───────────────┼─────────┼────────────────────────────────────┤
│ superusers │ Superusers    │ admin   │                                    │
├────────────┼───────────────┼─────────┼────────────────────────────────────┤
│ cryptopals │               │ alice   │ Quantum IPsec (read_only)          │
│            │               │ bob     │ Multi-SA HSRP (read_write)         │
│            │               │ mike    │                                    │
╘════════════╧═══════════════╧═════════╧════════════════════════════════════╛
```

Similarly, you can update one or more groups and assign them to multiple labs or members.
Also, for both `cml groups create` and `cml groups update` you can assign all labs and/or all users to the groups.

``` sh
❯ cml groups update --add-all-users --add-all-labs read_only users
Group users successfully updated

❯ cml groups ls
Groups on Server
╒════════════╤═══════════════╤══════════╤════════════════════════════════════╕
│ Name       │ Description   │ Users    │ Labs                               │
╞════════════╪═══════════════╪══════════╪════════════════════════════════════╡
│ users      │ All Users     │ admin    │ netbox (read_only)                 │
│            │               │ john     │ Multi Platform Network (read_only) │
│            │               │ alice    │ BFD (read_only)                    │
│            │               │ bob      │ Quantum IPsec (read_only)          │
│            │               │ mike     │ Multi-SA HSRP (read_only)          │
├────────────┼───────────────┼──────────┼────────────────────────────────────┤
│ superusers │ Superusers    │ admin    │                                    │
├────────────┼───────────────┼──────────┼────────────────────────────────────┤
│ cryptopals │               │ alice    │ Quantum IPsec (read_only)          │
│            │               │ bob      │ Multi-SA HSRP (read_write)         │
│            │               │ mike     │                                    │
╘════════════╧═══════════════╧══════════╧════════════════════════════════════╛
```

To delete one ore multiple groups

``` sh
❯ cml groups delete superusers cryptopals
Group superusers successfully deleted
Group cryptopals successfully deleted

❯ cml groups ls
Groups on Server
╒════════╤═══════════════╤══════════╤════════════════════════════════════╕
│ Name   │ Description   │ Users    │ Labs                               │
╞════════╪═══════════════╪══════════╪════════════════════════════════════╡
│ users  │ All Users     │ admin    │ nso-ha (read_only)                 │
│        │               │ john     │ netbox (read_only)                 │
│        │               │ bob      │ Multi Platform Network (read_only) │
│        │               │          │ BFD (read_only)                    │
│        │               │          │ Vodafone-PT (read_only)            │
│        │               │          │ fastapi-ubuntu (read_only)         │
│        │               │          │ upm-quick-test (read_only)         │
│        │               │          │ Quantum IPsec (read_only)          │
│        │               │          │ Multi-SA HSRP (read_only)          │
╘════════╧═══════════════╧══════════╧════════════════════════════════════╛
```

### Tab Completions

```sh
[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml l<tab>
license  ls
```

You can activate VIRL autocompletions by executing the following command

```sh
eval "$(_VIRL_COMPLETE=bash_source virl)"
```

To do the same for the `cml` command, do the following

```sh
eval "$(_CML_COMPLETE=bash_source cml)"
```

zsh users may need to run the following prior

```sh
autoload bashcompinit
bashcompinit
```

And then the following to properly enable completions for zsh

```sh
eval "$(_VIRL_COMPLETE=zsh_source virl)"
eval "$(_CML_COMPLETE=zsh_source cml)"
```

## Contributing

If you have an idea for a feature you would like to see, we gladly accept pull requests. To get started please review the [Contributing Guide](CONTRIBUTING.md)
