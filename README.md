# virlutils

[![Build Status](https://travis-ci.org/CiscoDevNet/virlutils.svg?branch=master)](https://travis-ci.org/CiscoDevNet/virlutils)
[![Coverage Status](https://coveralls.io/repos/github/CiscoDevNet/virlutils/badge.svg?branch=master)](https://coveralls.io/github/CiscoDevNet/virlutils?branch=master)
[![PyPI version](https://badge.fury.io/py/virlutils.svg)](https://badge.fury.io/py/virlutils)

A collection of utilities for interacting with [Cisco VIRL](https://learningnetworkstore.cisco.com/virlfaq/aboutVirl) 1.x or [Cisco Modeling Labs (CML)](https://developer.cisco.com/modeling-labs) v2.0+.

This document describes the new version of virlutils (aka cmlutils) that works with Cisco Modeling Labs v2.0 and higher.  Documentation for working with VIRL/CML 1.x is available [here](README_virl1.md).

## virl up / cml up

`virl` (or `cml`) is a devops style cli which supports the most common VIRL/CML operations.  Adding new ones is easy...

```sh
Usage: cml [OPTIONS] COMMAND [ARGS]...

Options:
  --debug / --no-debug  Print any debugging output.
  --help                Show this message and exit.

Commands:
  clear        clear the current lab ID
  cockpit      opens the Cockpit UI
  command      send a command or config to a node (requires pyATS)
  console      console for node
  definitions  manage image and node definitions
  down         stop a lab
  extract      extract configurations from all nodes in a lab
  generate     generate inv file for various tools
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
  ui           opens the Workbench for the current lab
  up           start a lab
  use          use lab launched elsewhere
  version      version information
  wipe         wipe a lab or nodes within a lab
```

<!-- TOC depthFrom:2 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

-   [Prerequisites](#prerequisites)
-   [Installation](#installation)
-   [Configuration](#configuration)
-   [Usage / Workflows](#usage--workflows)
-   [Development](#local-development)

<!-- /TOC -->

## Prerequisites

-   Python 3.6+ (tested with Python 3.7, 3.8, and 3.9)

## Installation

1.  Clone this repo

    ```sh
    git clone https://github.com/CiscoDevNet/virlutils
    cd virlutils
    ```

2.  Either (2a) use pip, or (2b) use setup.py

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

There really isn't much to configure, just set your CML credentials.  There are a few different ways to accomplish this, pick whichever one works best for you. The options listed below are in the `preferred` order.

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

-   `VIRL_TELNET_COMMAND` - allows the user to customize the telnet command that is called.
    This command will be passed the host/ip information from the running simulation

     Example:

    ```sh
    export VIRL_TELNET_COMMAND="mytelnet {host}"
    ```

-   `VIRL_SSH_COMMAND` - allows the user to customize the ssh command that is called.
    This command will be passed the host/ip as well as the username from the running simulation

    Example:

    ```sh
    export VIRL_SSH_COMMAND="myssh {username}@{host}"
    ```

-   `CML_VERIFY_CERT` - The path to a PEM-encoded certificate file to use to verify the CML controller VM's SSL certificate.  If you do not wish to verify the certificate, set this to "False"

    Example:

    ```sh
    export CML_VERIFY_CERT=/etc/certs/ca_bundle.pem
    ```

-   `CML_CONSOLE_COMMAND` - allows the user to customize the SSH command that is called.

    This command will be passed the CML controller VM IP, the console path of the node, and the CML controller username (**note:** you may have to force a TTY allocation in your SSH command)

    Example:

    ```sh
    export CML_CONSOLE_COMMAND="myssh {user}@{host} {console}"
    ```

-   `CML2_PLUS` - If set in the config or in the environment then virlutils will assume the server is a CML 2+ server and not try and automatically guess its version.  If omitted, then virutils will attempt to automatically determine the CML/VIRL server version

    Example:

    ```sh
    export CML2_PLUS="yes"
    ```

-   `CML_PLUGIN_PATH` - A delimiter-separated list of directories in which to find cmlutils plugins.  See the [plugin documentation](examples/plugins/README.md) for more details.  By default, the `plugins` directory in the current `.virl` directory will be searched.

    Example:

    ```sh
    export CML_PLUGIN_PATH="~/cmlutils/plugins:/opt/cmlutils/plugins"
    ```

### Why so many choices??!?!

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

1.  you can easily use different credentials/servers for various environments
2.  you can customize your lab .yaml files to include different tags, different node configurations, etc.
3.  you have a badass workflow.

```sh
$ cml ls  
Labs on Server
╒════════╤════════════════════════════════╤═════════════════════════╤═════════════════╤═════════╤═════════╤══════════════╕
│ ID     │ Title                          │ Description             │ Status          │   Nodes │   Links │   Interfaces │
╞════════╪════════════════════════════════╪═════════════════════════╪═════════════════╪═════════╪═════════╪══════════════╡
|        |                                |                         |                 |         |         |              |
╘════════╧════════════════════════════════╧═════════════════════════╧═════════════════╧═════════╧═════════╧══════════════╛
$ cd ../test
$ cml ls
Labs on Server
╒════════╤════════════════════════════════╤═════════════════════════╤═════════════════╤═════════╤═════════╤══════════════╕
│ ID     │ Title                          │ Description             │ Status          │   Nodes │   Links │   Interfaces │
╞════════╪════════════════════════════════╪═════════════════════════╪═════════════════╪═════════╪═════════╪══════════════╡
│ 7c2cf3 │ Small Branch Test              │                         │ STARTED         │       9 │       8 │           23 │
╘════════╧════════════════════════════════╧═════════════════════════╧═════════════════╧═════════╧═════════╧══════════════╛
$ cd ../prod
$ cml ls
Running Simulations
╒════════╤════════════════════════════════╤═════════════════════════╤═════════════════╤═════════╤═════════╤══════════════╕
│ ID     │ Title                          │ Description             │ Status          │   Nodes │   Links │   Interfaces │
╞════════╪════════════════════════════════╪═════════════════════════╪═════════════════╪═════════╪═════════╪══════════════╡
│ 7c2cf3 │ Small Branch Prod              │                         │ STARTED         │       9 │       8 │           23 │
╘════════╧════════════════════════════════╧═════════════════════════╧═════════════════╧═════════╧═════════╧══════════════╛
```

## Usage / Workflows

### Basic Workflow

in the absence of better documentation, here's a sample workflow

```sh
[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml ls
Labs on Server
╒════════╤════════════════════════════════╤═════════════════════════╤═════════════════╤═════════╤═════════╤══════════════╕
│ ID     │ Title                          │ Description             │ Status          │   Nodes │   Links │   Interfaces │
╞════════╪════════════════════════════════╪═════════════════════════╪═════════════════╪═════════╪═════════╪══════════════╡
│ 02f6c6 │ CCIE Enterprise Infrastructure │                         │ DEFINED_ON_CORE │      54 │      67 │          216 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 332eab │ Branch Test                    │                         │ DEFINED_ON_CORE │       6 │       5 │           15 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 7c2cf3 │ Small Branch                   │                         │ STOPPED         │       9 │       8 │           23 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ e5afaf │ Dynamic Split Tunnel           │                         │ STOPPED         │      10 │       9 │           36 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 66defd │ Lab at Tue 14:45 PM            │                         │ STOPPED         │       2 │       1 │            6 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ bc518e │ Lab at Wed 21:39 PM            │                         │ STOPPED         │       9 │       1 │           26 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 0e1bb2 │ DFN                            │ German Research Network │ DEFINED_ON_CORE │      51 │      80 │          211 │
╘════════╧════════════════════════════════╧═════════════════════════╧═════════════════╧═════════╧═════════╧══════════════╛

[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml id
Small Branch (ID: 7c2cf3)

[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml up
Lab Small Branch (ID: 7c2cf3) is already set as the current lab
Starting lab Small Branch (ID: 7c2cf3)


[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml ls
Labs on Server
╒════════╤════════════════════════════════╤═════════════════════════╤═════════════════╤═════════╤═════════╤══════════════╕
│ ID     │ Title                          │ Description             │ Status          │   Nodes │   Links │   Interfaces │
╞════════╪════════════════════════════════╪═════════════════════════╪═════════════════╪═════════╪═════════╪══════════════╡
│ 02f6c6 │ CCIE Enterprise Infrastructure │                         │ DEFINED_ON_CORE │      54 │      67 │          216 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 332eab │ Branch Test                    │                         │ DEFINED_ON_CORE │       6 │       5 │           15 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 7c2cf3 │ Small Branch                   │                         │ STARTED         │       9 │       8 │           23 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ e5afaf │ Dynamic Split Tunnel           │                         │ STOPPED         │      10 │       9 │           36 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 66defd │ Lab at Tue 14:45 PM            │                         │ STOPPED         │       2 │       1 │            6 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ bc518e │ Lab at Wed 21:39 PM            │                         │ STOPPED         │       9 │       1 │           26 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 0e1bb2 │ DFN                            │ German Research Network │ DEFINED_ON_CORE │      51 │      80 │          211 │
╘════════╧════════════════════════════════╧═════════════════════════╧═════════════════╧═════════╧═════════╧══════════════╛


[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml nodes
Here is a list of nodes in this lab
╒══════╤════════════════╤════════════════════╤═════════╤══════════╤══════════════════╕
│ ID   │ Label          │ Type               │ State   │ Wiped?   │ L3 Address(es)   │
╞══════╪════════════════╪════════════════════╪═════════╪══════════╪══════════════════╡
│ n0   │ branch-rtr     │ csr1000v           │ BOOTED  │ False    │ 192.168.10.219   │
├──────┼────────────────┼────────────────────┼─────────┼──────────┼──────────────────┤
│ n1   │ Internet       │ external_connector │ BOOTED  │ False    │                  │
├──────┼────────────────┼────────────────────┼─────────┼──────────┼──────────────────┤
│ n2   │ branch-sw      │ iosvl2             │ BOOTED  │ False    │                  │
├──────┼────────────────┼────────────────────┼─────────┼──────────┼──────────────────┤
│ n3   │ client-desktop │ desktop            │ BOOTED  │ False    │                  │
├──────┼────────────────┼────────────────────┼─────────┼──────────┼──────────────────┤
│ n4   │ WAN Link 1     │ wan_emulator       │ BOOTED  │ False    │                  │
├──────┼────────────────┼────────────────────┼─────────┼──────────┼──────────────────┤
│ n5   │ rtr-2          │ iosv               │ BOOTED  │ False    │                  │
├──────┼────────────────┼────────────────────┼─────────┼──────────┼──────────────────┤
│ n8   │ ext-conn-1     │ external_connector │ BOOTED  │ False    │                  │
├──────┼────────────────┼────────────────────┼─────────┼──────────┼──────────────────┤
│ n6   │ trex-0         │ trex               │ BOOTED  │ False    │                  │
├──────┼────────────────┼────────────────────┼─────────┼──────────┼──────────────────┤
│ n7   │ VLAN 10        │ external_connector │ BOOTED  │ False    │                  │
╘══════╧════════════════╧════════════════════╧═════════╧══════════╧══════════════════╛


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
Shutting down lab Small Branch (ID: 7c2cf3).....
SUCCESS

[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml ls
Labs on Server
╒════════╤════════════════════════════════╤═════════════════════════╤═════════════════╤═════════╤═════════╤══════════════╕
│ ID     │ Title                          │ Description             │ Status          │   Nodes │   Links │   Interfaces │
╞════════╪════════════════════════════════╪═════════════════════════╪═════════════════╪═════════╪═════════╪══════════════╡
│ 02f6c6 │ CCIE Enterprise Infrastructure │                         │ DEFINED_ON_CORE │      54 │      67 │          216 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 332eab │ Branch Test                    │                         │ DEFINED_ON_CORE │       6 │       5 │           15 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 7c2cf3 │ Small Branch                   │                         │ STOPPED         │       9 │       8 │           23 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ e5afaf │ Dynamic Split Tunnel           │                         │ STOPPED         │      10 │       9 │           36 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 66defd │ Lab at Tue 14:45 PM            │                         │ STOPPED         │       2 │       1 │            6 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ bc518e │ Lab at Wed 21:39 PM            │                         │ STOPPED         │       9 │       1 │           26 │
├────────┼────────────────────────────────┼─────────────────────────┼─────────────────┼─────────┼─────────┼──────────────┤
│ 0e1bb2 │ DFN                            │ German Research Network │ DEFINED_ON_CORE │      51 │      80 │          211 │
╘════════╧════════════════════════════════╧═════════════════════════╧═════════════════╧═════════╧═════════╧══════════════╛

[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml use --lab-name "Small Branch"

[venv]jclarke@jamahal:~/src/git/virlutils|cmlutils
⇒  cml nodes
Here is a list of nodes in this lab
╒══════╤════════════════╤════════════════════╤═════════╤══════════╤══════════════════╕
│ ID   │ Label          │ Type               │ State   │ Wiped?   │ L3 Address(es)   │
╞══════╪════════════════╪════════════════════╪═════════╪══════════╪══════════════════╡
│ n0   │ branch-rtr     │ csr1000v           │ STOPPED │ False    │                  │
├──────┼────────────────┼────────────────────┼─────────┼──────────┼──────────────────┤
│ n1   │ Internet       │ external_connector │ STOPPED │ False    │                  │
├──────┼────────────────┼────────────────────┼─────────┼──────────┼──────────────────┤
│ n2   │ branch-sw      │ iosvl2             │ STOPPED │ False    │                  │
├──────┼────────────────┼────────────────────┼─────────┼──────────┼──────────────────┤
│ n3   │ client-desktop │ desktop            │ STOPPED │ False    │                  │
├──────┼────────────────┼────────────────────┼─────────┼──────────┼──────────────────┤
│ n4   │ WAN Link 1     │ wan_emulator       │ STOPPED │ False    │                  │
├──────┼────────────────┼────────────────────┼─────────┼──────────┼──────────────────┤
│ n5   │ rtr-2          │ iosv               │ STOPPED │ False    │                  │
├──────┼────────────────┼────────────────────┼─────────┼──────────┼──────────────────┤
│ n8   │ ext-conn-1     │ external_connector │ STOPPED │ False    │                  │
├──────┼────────────────┼────────────────────┼─────────┼──────────┼──────────────────┤
│ n6   │ trex-0         │ trex               │ STOPPED │ False    │                  │
├──────┼────────────────┼────────────────────┼─────────┼──────────┼──────────────────┤
│ n7   │ VLAN 10        │ external_connector │ STOPPED │ False    │                  │
╘══════╧════════════════╧════════════════════╧═════════╧══════════╧══════════════════╛

```

### Inventory Generation

virlutils will generate inventories for various management systems

#### pyATS Testbed Generation

quickly turn your simulations into a testbed file that can be used for pyATS/Genie

```sh
cml generate pyats
```

#### Command and Config Execution

Using the same pyATS framework, `virlutils` can execute CLI EXEC-level (e.g., "show") commands as well as configuration commands on nodes within a lab.  These nodes do not have to be externally reachable or have any IP connectivity.  This is a great way to test operational aspects of a completely isolated topology.  Before using the `command` command you must install pyATS.  You can install pyATS by running `pip install pyats`.

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

#### Ansible Inventory Generation

quickly turn your simulations into an inventory file that can be used to run your playbooks
against.  Both INI and YAML(default) formats are supported by the tool.

```sh
Usage: cml generate ansible [OPTIONS]

  generate ansible inventory

Options:
  -o, --output TEXT   output File name
  --style [ini|yaml]  output format (default is yaml)
  --help              Show this message and exit.
```

The ansible group membership can be controlled by adding the "ansible_group" tag to nodes in your CML labs.  Multiple "ansible_group" tags can be assigned to a single node, and that node will be placed into each Ansible inventory group.

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

**NOTE:** if the ansible_group tag is not specified for a node, that node will not be included during inventory generation.  Additionally, CML needs to know each node's management IP address before it will be placed into the inventory file

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

**NOTE**:  NSO environment is also attempted to be determined using the following environment
variables

-   NSO_HOST
-   NSO_USERNAME
-   NSO_PASSWORD

NSO Configuration Example

```sh
export NSO_HOST=localhost
export NSO_USERNAME=admin
export NSO_PASSWORD=admin
```

#### Tab Completions

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

## Local Development

If you have an idea for a feature you would like to see, we gladly accept pull requests.  To get started developing, simply run the following..

```sh
git clone https://github.com/CiscoDevNet/virlutils
cd virlutils
python setup.py develop
```

### Linting

We use flake 8 to lint our code. Please keep the repository clean by running:

```sh
flake8
```

### Testing

We have some testing implemented, but would love to have better coverage. If you
add a feature, or just feel like writing tests please update the appropriate files
in the `tests` folder.

To run the tests in the `tests` folder, you can simply run `make test` from
the project root.
