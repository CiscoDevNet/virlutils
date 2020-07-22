# Initial Proposal and Plan for CML2 Support
`virlutils` has a wide range of commands for managing network simulations with VIRL or CML 1.x.  

```
Usage: virl [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  console   console for node
  down      stop a virl simulation
  flavors   Manage VIRL Flavors Attributes
  generate  generate inv file for various tools
  id        gets sim id for local environment
  logs      Retrieves log information for the provided simulation
  ls        lists running simulations in the current project
  nodes     get nodes for sim_name
  pull      pull topology.virl from repo
  save      save simulation to local virl file
  search    lists virl topologies available via github
  ssh       ssh to a node
  start     start a node
  stop      stop a node
  swagger   manage local swagger ui server
  telnet    telnet to a node
  up        start a virl simulation
  use       use virl simulation launched elsewhere
  uwm       opens UWM for the sim
  version   version information
  viz       opens live visualization for the sim
```

As plans begin for supporting CML2, here's a breakdown of commands and where they fit into priorities and development. 

## Core Functionality / Highest Priority 
These commands and features would be considered mandatory for an initial functional release of CML2 support.

### `virl up` and `virl down` 
The most basic feature of the CLI is to start and stop simulations. 

* `virl up` 
    * With no arguments should look for and use a `topology.yaml` file and start a new simulation after importing into CML2 
    * Save the lab id on client side for future commands
    * *Possible Feature*: If no `topology.yaml` file found, but a `topology.virl` file found, import a 1.x simulation file to convert
    * `-f` option (file) - provide explicit file for simulation to start 
    * `-n` / `--lab-name` option (name) - provide the friend name of a lab that exists in CML2 lab manager *(2.0 new feature)*
        * Alias for `--sim-name` for backwards compatibility with 1.x.  
    * `--id` option (id) - provide the unique ID of a lab that exists in CML2 lab manager *(2.0 new feature)*
    * `--provision` - Wait for all nodes in simulation to be "ready" before completing command **(post initial release)** 
    
* `virl down` 
    * With no argument, look for client side lab id for lab to manage, stop all nodes in simulation
    * `-n` / `--lab-name` option (name) - provide the friend name of a lab that exists in CML2 lab manager 
        * Alias for `--sim-name` for backwards compatibility with 1.x.  
    * `--id` option (id) - provide the unique ID of a lab that exists in CML2 lab manager *(2.0 new feature)*
    
    **STATUS:** <span style="color: green">Fully implemented as described</span>

### `virl ls` 
List out all labs in Lab Manager for user.  Feature useful to `virl up -n "Lab 1"` 

* Basic command with no arguments just list all labs including ID and Description 

**STATUS:** <span style="color: green">Implemented fully with an additional `--all` option to show images in cache not on the server.</span>

### `virl use` 
Update CLI side "project" to leverage specific simulation/lab from 2.0 server 

* `-n` option (name) - provide the friend name of a lab that exists in CML2 lab manager *(2.0 new feature)*
    * For compatibility with 1.x, consider `-n` should also be positional
* `--id` option (id) - provide the unique ID of a lab that exists in CML2 lab manager *(2.0 new feature)*

**STATUS:** <span style="color: green">Fully implemented as described</span>

### `virl nodes` 
List out all nodes in the "active" or "used" simulation. Details displayed in table should match 1.x as much as possible. 

**STATUS:** <span style="color: green">Fully implemented as described</span>

### `virl console` 
Establish console connection to a specific node. 

* Positional parameter for `node name`
* `virl console` should **not** require the Breakout or other utilities, rather use client "ssh" client to connect through the CML2 terminal server option 
    * If valuable, future releases could leverage breakout for additional capabilities, but shouldn't be a requirement

**STATUS:** <span style="color: green">Fully implemented as described.  Also supports the `--display` option to only show the console information.  Works with a custom SSH command, too.</span>

> Note: Support for `virl ssh` and `virl telnet` should be investigated for future support. But lack of easy method to get a management IP for devices, we can rely on `console` for first release

### `virl start` and `virl stop` 
Method to start and stop individual nodes in a lab. 

* Positional parameter for `node name`

**STATUS:** <span style="color: green">Fully implemented as described</span>

### `virl wipe`
New feature for 2.0 that will wipe the state of a node

* Positional parameter for `node name`
* By default, only works if node is already stopped 
* `--force` - if node is started, stop and wipe 
* By default, command should ask for confirmation before executing. 
* `no-confirm` - don't prompt for confirmation 

**STATUS:** <span style="color: green">Fully implemented as described</span>

## Post Initial Release Features and Commands 
Once the core functionality is operational, work can begin on these features which are very useful for workflows with CML2.0

### `virl generate`
Commands to create a variety of related inventory files and connectors for other functionality. 

* `virl generate ansible`
* `virl generate pyats`
* `virl generate nso`
* `virl generate netbox`  *(2.0 new feature)*
* `virl generate nornir` *(2.0 new feature)*

**STATUS:** <span style="color: gold">Only `ansible`, `pyats`, and `nso` are implemented at this time.</span>

### `virl extract config` *(2.0 new feature)*
Command to extract running configuration from devices and update topology file. 

> Consider alternative to creating new `extract` command.  Maybe place under `generate`

**STATUS** <span style="color: green">`virl extract` has been implemented without the `config` subcommand.  Without any arguments, it extracts all configs from running devices in the current lab.  It also optionally updates the local .yaml lab file cache.</span>

### `virl definition` 
Commands to manage the image and node definitions. 

> Note: These commands replace the `virl flavors` feature for 1.x

* `virl definition node` 
* `virl definition image` 
* Sub-commands
    * `ls` - List 
    * `export` - Download to local computer 
    * `import` - Upload from local computer

**STATUS:** <span style="color: green">Fully implemented as described, plus can import both image files and image definitions</span>

### `~~virl diagnostics`~~ 
~~Set of commands for checking health of CML2.0 server and labs~~ 

* ~~`virl diagnostics lab logs`~~ 
    * ~~Pull logs for running lab~~ 
    * ~~*Note: Command replaces `virl logs` feature for 1.x~~ 
* ~~`virl diagnostic cml logs`~~ 
    * ~~Pull logs from server~~ 

> ~~Many options for future commands to go here to help wtih checking health of server and lab.  Consider it the "show tech" for virlutils~~ 

**STATUS:** <span style="color:red">This is not implementable at this time due to lack of CML APIs.</span>

### `virl save`
Download the `topology.yaml` file for running simulation. 

* Default behavior will use lab name as file name 
* `-f` - Provide new file name
* `--extract-config` - Extract running configuration before downloading

**STATUS:** <span style="color: green">Fully implemented as described</span>

## New Features to Consider for 2.0 
### `virl docs` 
Launch user to different docs for CML2.0 

* virl2-client 
* API Docs 
* Support Docs 
* Official User Guide 

**STATUS:** <span style="color:red">Not implemented at this time</span>

## Commands for Centralized and Shared Labs 
Thought should be given to future options for building shared topologies amoung community. Today the virlfiles GitHub org is used for 1.x, but that's hard to scale. 

Commands like `virl search` relate here.

Things to consider: 

* Code Exchange integration 

## Low Priority Commands from virlutils 1.x 
### `virl pull` 
Connect to Git Repository and Pull down a topology file 

**STATUS:** <span style="color:green">Fully implemented for .yaml files with otherwise identical functionality to VIRL/CML 1.x</span>

### `virl swagger` 
For 1.x this launched a virlutils hosted API doc.  Little used outside of core virlutils devs.  It would be simple to have the command launch user into the CML2.0 servers API Docs.

**STATUS:** <span style="color:red">Not implemented at this time</span>

### `virl uwm` and `virl viz`
For 1.x this would launch user to the UWM web interface for lab.  These interfaces aren't in 2.0, though replacements for these commands could be

* `virl ui`
* `virl cockpit`

**STATUS:** <span style="color:green">Both `cockpit` and `ui` have been implemented to behave like `uwm` and `viz` did for VIRL/CML 1.x</span>