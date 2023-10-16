# cyperf-agent-manager
A simple python script that can ssh into multiple cyperf agents and run some pre-defined commands

[![PyPI - Version](https://img.shields.io/pypi/v/cyperf-agent-manager.svg)](https://pypi.org/project/cyperf-agent-manager)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cyperf-agent-manager.svg)](https://pypi.org/project/cyperf-agent-manager)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)
- [CLI](#cli)
- [Password Override](#password override)
- [Module](#module)

## Installation

```console
pip install cyperf-agent-manager
```

_If `pip` command is not found on your system then use the following commands to install `pip`._

```cosnole
$ wget https://bootstrap.pypa.io/get-pip.py
$ python get-pip.py
```
_If `python` command is also not found then please look for `python3` command. Otherwise install `python3`._

## License

`cyperf-agent-manager` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## CLI
This package installs a command called `cyperf-agent-manager` that is a very thin wrapper over `cyperf_agent_manager` package. This top level commands has many subcommands that can be used to execute different operations on multiple agents at simultaneously.

The command details can be found by running the script with `--help` option, as shown in the following blocks.
```
[PROMPT]:~$ cyperf-agent-manager --help
Usage: cyperf-agent-manager [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  install-build
  reload
  set-controller
  set-test-interface
```
### Installing an agent build on multiple agents
```
[PROMPT]:~$ cyperf-agent-manager install-build --help
Usage: cyperf-agent-manager install-build [OPTIONS]

Options:
  --agent-ips NETWORK ADDRESS LIST
                                  One or more agent names (IP addresses or
                                  hostnames). Use quotation marks (`'` or `"`)
                                  for whitespace (` `) separated values. Other
                                  valid separators are `,`, `;` and `:`.
                                  [required]
  --username TEXT                 A common username for all the agents.
                                  [default: cyperf]
  --override-password             This along with --password option should be
                                  used for non default password.
  --password TEXT                 A common password for all the agents.
  --key-file FILE                 A common key file for opening ssh
                                  connections to all the agents.
  --debian-file-path FILE         Path to the .deb file to be installed.
                                  [required]
  --help                          Show this message and exit.

Example:
========

[PROMPT]:~$ cyperf-agent-manager install-build --agent-ips '10.36.75.69 10.36.75.70' --debian-file-path ./tiger_x86_64_ixos-8.50_ixstack-raw_release_1.0.3.575.deb
>> Connectiong to agent 10.36.75.69
>> Tranferring file ./tiger_x86_64_ixos-8.50_ixstack-raw_release_1.0.3.575.deb to ~/tiger_x86_64_ixos-8.50_ixstack-raw_release_1.0.3.575.deb
>> Connectiong to agent 10.36.75.70
>> Tranferring file ./tiger_x86_64_ixos-8.50_ixstack-raw_release_1.0.3.575.deb to ~/tiger_x86_64_ixos-8.50_ixstack-raw_release_1.0.3.575.deb
>> Connectiong to agent 10.36.75.69
>> Executing command sudo -S -p '' apt install -y ~/tiger_x86_64_ixos-8.50_ixstack-raw_release_1.0.3.575.deb
Reading package lists...
Building dependency tree...
Reading state information...
The following NEW packages will be installed:
  tiger-x86-64-ixos-8.50-ixstack-raw-release-1.0.3.575
0 upgraded, 1 newly installed, 0 to remove and 2 not upgraded.
Need to get 0 B/62.0 MB of archives.
After this operation, 0 B of additional disk space will be used.
Get:1 /home/cyperf/tiger_x86_64_ixos-8.50_ixstack-raw_release_1.0.3.575.deb tiger-x86-64-ixos-8.50-ixstack-raw-release-1.0.3.575 all 1.0.3.575 [62.0 MB]
Selecting previously unselected package tiger-x86-64-ixos-8.50-ixstack-raw-release-1.0.3.575.
(Reading database ... 69919 files and directories currently installed.)
Preparing to unpack .../tiger_x86_64_ixos-8.50_ixstack-raw_release_1.0.3.575.deb ...
Unpacking tiger-x86-64-ixos-8.50-ixstack-raw-release-1.0.3.575 (1.0.3.575) ...
Setting up tiger-x86-64-ixos-8.50-ixstack-raw-release-1.0.3.575 (1.0.3.575) ...
Creating symbolic links
Installing portmanager
  Stopping existing portmanager service.
  Creating symbolic links
  Removing the existing cyperfagentcli auto-completion script
  Ensuring /etc/bash_completion.d/ directory is present in the system

Reusing following configurations from existing configuration
  Broker URL:                  nats://10.36.75.126:30422
  Management Interface:        ens160
  Test Interface:       [auto]
  Hooks:
    pre_diagnostic_collection: /opt/keysight/tiger/active/bin/utilities/01_ipsec_concatenate_key_logs
  Tags:       []

  Removing portmanager database
  Installing portmanager service
  Installing agent-update service
  Starting portmanager service
  Setting stack type ixstack-raw

Parsing config JSON file
schemaFileUri = file:///opt/keysight/tiger/active/bin/portmanager/portmanager-config.json.schema.json configFileUri = file:///etc/portmanager/portmanager-config.json
Restarting portmanager
Stack type set to: ixstack-raw

Portmanager service restarted.

  Starting portmanager service
Installing QAT Engine

	****Installing QAT Engine****>





	***QAT Engine Installation Complete***>





	***installer operation status is Success***>


/

Hook pre_diagnostic_collection is set to /opt/keysight/tiger/active/bin/utilities/01_ipsec_concatenate_key_logs.


Portmanager service restarted.


>> Connectiong to agent 10.36.75.70
>> Executing command sudo -S -p '' apt install -y ~/tiger_x86_64_ixos-8.50_ixstack-raw_release_1.0.3.575.deb
Reading package lists...
Building dependency tree...
Reading state information...
The following NEW packages will be installed:
  tiger-x86-64-ixos-8.50-ixstack-raw-release-1.0.3.575
0 upgraded, 1 newly installed, 0 to remove and 2 not upgraded.
Need to get 0 B/62.0 MB of archives.
After this operation, 0 B of additional disk space will be used.
Get:1 /home/cyperf/tiger_x86_64_ixos-8.50_ixstack-raw_release_1.0.3.575.deb tiger-x86-64-ixos-8.50-ixstack-raw-release-1.0.3.575 all 1.0.3.575 [62.0 MB]
Selecting previously unselected package tiger-x86-64-ixos-8.50-ixstack-raw-release-1.0.3.575.
(Reading database ... 72923 files and directories currently installed.)
Preparing to unpack .../tiger_x86_64_ixos-8.50_ixstack-raw_release_1.0.3.575.deb ...
Unpacking tiger-x86-64-ixos-8.50-ixstack-raw-release-1.0.3.575 (1.0.3.575) ...
Setting up tiger-x86-64-ixos-8.50-ixstack-raw-release-1.0.3.575 (1.0.3.575) ...
Creating symbolic links
Installing portmanager
  Stopping existing portmanager service.
  Creating symbolic links
  Removing the existing cyperfagentcli auto-completion script
  Ensuring /etc/bash_completion.d/ directory is present in the system

Reusing following configurations from existing configuration
  Broker URL:                  nats://10.36.75.126:30422
  Management Interface:        ens160
  Test Interface:       [auto]
  Hooks:
    pre_diagnostic_collection: /opt/keysight/tiger/active/bin/utilities/01_ipsec_concatenate_key_logs
  Tags:       []

  Removing portmanager database
  Installing portmanager service
  Installing agent-update service
  Starting portmanager service
  Setting stack type ixstack-raw

Parsing config JSON file
schemaFileUri = file:///opt/keysight/tiger/active/bin/portmanager/portmanager-config.json.schema.json configFileUri = file:///etc/portmanager/portmanager-config.json
Restarting portmanager
Stack type set to: ixstack-raw

Portmanager service restarted.

  Starting portmanager service
Installing QAT Engine

	****Installing QAT Engine****>





	***QAT Engine Installation Complete***>





	***installer operation status is Success***>


/

Hook pre_diagnostic_collection is set to /opt/keysight/tiger/active/bin/utilities/01_ipsec_concatenate_key_logs.


Portmanager service restarted.


```
### Setting controller IP for multiple agents
```
[PROMPT]:~$ cyperf-agent-manager set-controller --help
Usage: cyperf-agent-manager set-controller [OPTIONS]

Options:
  --agent-ips NETWORK ADDRESS LIST
                                  One or more agent names (IP addresses or
                                  hostnames). Use quotation marks (`'` or `"`)
                                  for whitespace (` `) separated values. Other
                                  valid separators are `,`, `;` and `:`.
                                  [required]
  --username TEXT                 A common username for all the agents.
                                  [default: cyperf]
  --override-password             This along with --password option should be
                                  used for non default password.
  --password TEXT                 A common password for all the agents.
  --key-file FILE                 A common key file for opening ssh
                                  connections to all the agents.
  --controller-ip NETWORK ADDRESS
                                  The IP/Hostname of the CyPerf controller.
                                  [required]
  --help                          Show this message and exit.

Example:
========

[PROMPT]:~$ cyperf-agent-manager set-controller --controller-ip 10.36.75.126 --agent-ips '10.36.75.69 10.36.75.70'
>> Connectiong to agent 10.36.75.69
>> Executing command cyperfagent controller set 10.36.75.126

Controller is set successfully.

Current Configurations
  Controller:           10.36.75.126:30422
  Management Interface: ens160
  Test Interface:       ens192

Please make sure that the URL and interfaces are set correctly for the tests to run.

Portmanager service restarted.

Connecting....Connected


>> Connectiong to agent 10.36.75.70
>> Executing command cyperfagent controller set 10.36.75.126

Controller is set successfully.

Current Configurations
  Controller:           10.36.75.126:30422
  Management Interface: ens160
  Test Interface:       ens192

Please make sure that the URL and interfaces are set correctly for the tests to run.

Portmanager service restarted.

Connecting....Connected

```
### Reloading configuration for multiple agents
```
[PROMPT]:~$ cyperf-agent-manager reload --help
Usage: cyperf-agent-manager reload [OPTIONS]

Options:
  --agent-ips NETWORK ADDRESS LIST
                                  One or more agent names (IP addresses or
                                  hostnames). Use quotation marks (`'` or `"`)
                                  for whitespace (` `) separated values. Other
                                  valid separators are `,`, `;` and `:`.
                                  [required]
  --username TEXT                 A common username for all the agents.
                                  [default: cyperf]
  --override-password             This along with --password option should be
                                  used for non default password.
  --password TEXT                 A common password for all the agents.
  --key-file FILE                 A common key file for opening ssh
                                  connections to all the agents.
  --help                          Show this message and exit.

Example:
========

[PROMPT]:~$ cyperf-agent-manager reload --agent-ips '10.36.75.69 10.36.75.70'
>> Connectiong to agent 10.36.75.69
>> Executing command cyperfagent configuration reload

Current Configurations
  Controller:           10.36.75.126:30422
  Management Interface: ens160
  Test Interface:       ens192

Please make sure that the URL and interfaces are set correctly for the tests to run.

Portmanager service restarted.

Connecting.....Connected


>> Connectiong to agent 10.36.75.70
>> Executing command cyperfagent configuration reload

Current Configurations
  Controller:           10.36.75.126:30422
  Management Interface: ens160
  Test Interface:       ens192

Please make sure that the URL and interfaces are set correctly for the tests to run.

Portmanager service restarted.

Connecting....Connected


```
### Setting test interface for multiple agents
```
[PROMPT]:~$ cyperf-agent-manager set-test-interface --help
Usage: cyperf-agent-manager set-test-interface [OPTIONS]

Options:
  --agent-ips NETWORK ADDRESS LIST
                                  One or more agent names (IP addresses or
                                  hostnames). Use quotation marks (`'` or `"`)
                                  for whitespace (` `) separated values. Other
                                  valid separators are `,`, `;` and `:`.
                                  [required]
  --username TEXT                 A common username for all the agents.
                                  [default: cyperf]
  --override-password             This along with --password option should be
                                  used for non default password.
  --password TEXT                 A common password for all the agents.
  --key-file FILE                 A common key file for opening ssh
                                  connections to all the agents.
  --test-interface TEXT           The name of the interface on the agents
                                  which will be used for test traffic.
                                  [required]
  --help                          Show this message and exit.

Example:
========

[PROMPT]:~$ cyperf-agent-manager set-test-interface --agent-ips '10.36.75.69 10.36.75.70' --test-interface auto
>> Connectiong to agent 10.36.75.69
>> Executing command cyperfagent interface test set auto

Test Interface is set successfully.

Current Configurations
  Controller:           10.36.75.126:30422
  Management Interface: ens160
  Test Interface:       auto (Auto-detected interface is ens192)

Please make sure that the URL and interfaces are set correctly for the tests to run.
Use the following commands to explicitly set the Management and Test interfaces:
  cyperfagent interface management set <Management interface name>
  cyperfagent interface test set <Test interface name>

Portmanager service restarted.


>> Connectiong to agent 10.36.75.70
>> Executing command cyperfagent interface test set auto

Test Interface is set successfully.

Current Configurations
  Controller:           10.36.75.126:30422
  Management Interface: ens160
  Test Interface:       auto (Auto-detected interface is ens192)

Please make sure that the URL and interfaces are set correctly for the tests to run.
Use the following commands to explicitly set the Management and Test interfaces:
  cyperfagent interface management set <Management interface name>
  cyperfagent interface test set <Test interface name>

Portmanager service restarted.


```

## Password Override
Even though CyPerf agents are deployed from official machice images provided CyPerf team, CyPerf can also installed on arbitrary machines. All CyPerf machine images come with a default password. `cyperf-agent-manager` by default tries to connect with that default password. Obviously the default password won't work for arbitrary machines. In those cases the password has to be overriden. The options `--override-password` and `--password` are there for that purpose only but using `--password` directly in CLI is unsafe. In that case the actual password will be visible in plain text. A better option is to use only the `--override-password` option in CLI and then a password prompt will come up. The user will be able to type the password in an invisible way. Please see the example below.
_If a key file is provided using `--key-file` option then `cyperf-agent-manager` will try to open a connection with each agent using the key file first. If authentication fails with the key file then it will try the password._

### Example
```
[PROMPT]:$ cyperf-agent-manager reload --agent-ips '10.36.75.69 10.36.75.70' --override-password
Password [cyperf]:
Repeat for confirmation:
>> Connectiong to agent 10.36.75.69
>> Executing command cyperfagent configuration reload

Current Configurations
  Controller:           10.36.75.126:30422
  Management Interface: ens160
  Test Interface:       auto (Auto-detected interface is ens192)

Please make sure that the URL and interfaces are set correctly for the tests to run.
Use the following commands to explicitly set the Management and Test interfaces:
  cyperfagent interface management set <Management interface name>
  cyperfagent interface test set <Test interface name>

Portmanager service restarted.

Connecting.....Connected


>> Connectiong to agent 10.36.75.70
>> Executing command cyperfagent configuration reload

Current Configurations
  Controller:           10.36.75.126:30422
  Management Interface: ens160
  Test Interface:       auto (Auto-detected interface is ens192)

Please make sure that the URL and interfaces are set correctly for the tests to run.
Use the following commands to explicitly set the Management and Test interfaces:
  cyperfagent interface management set <Management interface name>
  cyperfagent interface test set <Test interface name>

Portmanager service restarted.

Connecting....Connected


```

## Module
The python module installed by this package in `cyperf_agent_manager`. This can be used from a custom python script. Here is a smaple code that uses the `cyperf_agent_manager` module.
```
import cyperf_agent_manager.agent_manager as caMgr

agentIPs     = [ '192.168.0.1', '192.168.0.2' ]
controllerIP = '192.168.100.1'
testIface    = 'ens192'
debFile      = './tiger_x86_64_ixos-8.50_ixstack-raw_release_1.0.3.575.deb'

agentMgr     = caMgr.CyPerfAgentManager(agentIPs)

agentMgr.InstallBuild (debFile)
agentMgr.ControllerSet (controllerIP)
agentMgr.Reload ()
agentMgr.SetTestInterface (testIface)
```
