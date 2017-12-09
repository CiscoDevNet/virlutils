# virl_cli

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
```
git clone https://github.com/kecorbin/virl_cli
cd virl_cli
virtualenv venv && source venv/bin/activate
python setup.py install
```

## Configuration

s
```
export VIRL_HOST=1.1.1.1
```

## Usage

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
