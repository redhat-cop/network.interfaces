# Network Interfaces Validated Content

This repository contains the `network.interfaces` Ansible Collection.

## Description

The `network.interfaces` enables user to manage the Interfaces resources independent of platforms and perform INTERFACES health checks.

## Tested with Ansible

Tested with ansible-core 2.13 releases.

## Installation

```
ansible-galaxy collection install git+https://github.com/redhat-cop/network.interfaces
```

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
collections:
- name: https://github.com/redhat-cop/network.interfaces.git
  type: git
  version: main
```

**Capabilities**
- `Build Brownfield Inventory`: Users want to be able to get the facts for INTERFACES resources and store it as host_vars thus enabling the capability to get facts for all the hosts within the inventory and store facts in a structured format which acts as SOT.
- `INTERFACES Resource Management`: Users want to be able to manage the interfaces,L2 interfaces and L3 interfaces configurations.This also includes the enablement of gathering facts, updating INTERFACE resource host-vars and deploying config onto the appliance.
- `INTERFACES Health Checks`: Users want to be able to perform health checks for INTERFACES resource.These health checks should be able to provide the interfaces admin operational state with necessary details.

### Usage
- This platform agnostic role enables the user to perform INTERFACES health checks.Users can perform following health checks:
       `all_operational_state_up`
       `min_operational_state_up`
       `all_administratnal_state_up`
       `min_administratnal_state_up`
      
  
- This role enables users to create a runtime brownfield inventory with all the INTERFACES configuration in terms of host vars. These host vars are ansible facts which have been gathered through the *_interfaces, *_l2_interfaces and *_l3_interfaces network resource module.The tasks offered by this role could be observed as below:

## Perform INTERFACES Health Checks
#### Health Checks operation fetch the current status INTERFACES operation state health.

```yaml
health_checks.yml
---
- name: Perform interfaces health checks
  hosts: iosxr
  gather_facts: false
  tasks:
  - name: INTERFACES Manager
    ansible.builtin.include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.iosxr.iosxr
      actions:
        - name: health_check
          vars:
            details: True
            checks:
              - name: all_operational_state_up
              - name: min_operational_state_up
                min_count: 1
              - name: all_admin_state_up
              - name: min_admin_state_up
                min_count: 1
```


## Building Brownfield Inventory with Persist
#### Persist operation fetch the interfaces,L2 interfaces and L3 interfaces facts and store them as host vars.
##### Result of successful Persist operation would be interfaces facts and publish inventory host_vars to remote repository which will act as SOT for operations like deploy, remediate,detect etc.

```yaml
- name: Persist the facts into host vars
  hosts: iosxr
  gather_facts: false
  tasks:
  - name: Network Interfaces Manager
    ansible.builtin.include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.ios.ios
      actions:
        - name: persist
      data_store:
      scm:  
        origin:
          url: "{{ GH_REPO_URL }}"
          token: "{{ GH_PAT }}"
          user:
            name: ansible_github
            email: ansible@ansible.com
```

## Gather INTERFACES Facts
#### Gather operation gathers the running-confguration specific to interfaces, l2-interfaces, l3-interfaces resources.

```yaml
- name: Gather Facts
  hosts: iosxr
  gather_facts: false
  tasks:
  - name: INTERFACES Manager
    ansible.builtin.include_role:
      name: network.interface.run
    vars:
      ansible_network_os: cisco.iosxr.iosxr
      actions:
        - name: gather
```

## Deploy INTERFACES Configuration
#### Read all host_vars from persisted local inventory and deploy changes to running-config.

```yaml
- name: Deploy host vars facts
  hosts: iosxr
  gather_facts: false
  tasks:
  - name: INTERFACES Manager
    include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.iosxr.iosxr
      actions:
        - name: deploy
      data_store:
        local: "~/backup/network"
```

#### Read provided resources host vars from remote repository and deploy changes to running-config.

```yaml
- name: Deploy host vars facts
  hosts: iosxr
  gather_facts: false
  tasks:
  - name: INTERFACES Manager
    include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.iosxr.iosxr
      actions:
        - name: deploy
      data_store:
        scm:  
          origin:
            url: "{{ GH_REPO_URL }}"
            token: "{{ GH_PAT }}"
            user:
              name: github_username
              email: youremail@example.com
```

## Detect configuration drift in INTERFACES Configuration
#### Detect configuration drift between local host vars and running config. In this action 'overridden' state is used with 'check_mode=True'

```yaml
- name: 
  hosts: iosxr
  gather_facts: false
  tasks:
  - name: INTERFACES Manager
    include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.iosxr.iosxr
      actions:
        - name: detect
      data_store:
        local: "~/backup/network"
```

#### Detect configuration drift between remote host-vars repository and running config. In this action 'overridden' state is used with 'check_mode=True'

```yaml
- name: 
  hosts: iosxr
  gather_facts: false
  tasks:
  - name: INTERFACES Manager
    include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.iosxr.iosxr
      actions:
        - name: detect
      data_store:
        scm:  
          origin:
            url: "{{ GH_REPO_URL }}"
            token: "{{ GH_PAT }}"
            user:
              name: github_username
              email: youremail@example.com
```

## Remediate configuration drift in INTERFACES Configuration
#### Remediate configuration drift between local inventory host-vars and running config for given network resources.
[CAUTION !] This action will override the running-config

```yaml
- name: 
  hosts: iosxr
  gather_facts: false
  tasks:
  - name: INTERFACES Manager
    include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.iosxr.iosxr
      actions:
        - name: remediate
      data_store:
          local: "~/backup/network"
```

#### Remediate configuration drift between remote inventory host-vars and running config for given network resources.
[CAUTION !] This action will override the running-config

```yaml
- name: 
  hosts: iosxr
  gather_facts: false
  tasks:
  - name: INTERFACES Manager
    include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.iosxr.iosxr
      actions:
        - name: remediate
      data_store:
        scm:  
          origin:
            url: "{{ GH_REPO_URL }}"
            token: "{{ GH_PAT }}"
            user:
              name: github_username
              email: youremail@example.com
```
## Configure interface configuration with config action.
#### invoke single operation for provided resource with provided configuration and state for given ansible_network_os

```yaml
- name: 
  hosts: iosxr
  gather_facts: false
  tasks:
  - name: INTERFACES Manager
    include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.iosxr.iosxr
      vars:
      action: configure
      ansible_network_os: cisco.iosxr.iosxr
      config:
        - name: "GigabitEthernet0/0"
          description: "Edited with Configure operation"
      state: merged
```
### Code of Conduct
This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.


## Release notes

Release notes are available [here](https://github.com/redhat-cop/network.interfaces/blob/main/CHANGELOG.rst).

## Licensing

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
