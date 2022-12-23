# Network Interfaces Validated Content

This repository contains the `network.interfaces` Ansible Collection.

## Description

The `network.interfaces` enables user to manage the Interfaces resources independent of platforms and perform INTERFACES health checks.

**Capabilities**
- `Build Brownfield Inventory`: Users want to be able to get the facts for INTERFACES resources and store it as host_vars thus enabling the capability to get facts for all the hosts within the inventory and store facts in a structured format which acts as SOT.
- `INTERFACES Resource Management`: Users want to be able to manage the interfaces,L2 interfaces and L3 interfaces configurations.This also includes the enablement of gathering facts, updating INTERFACE resource host-vars and deploying config onto the appliance.
- `INTERFACES Health Checks`: Users want to be able to perform health checks for INTERFACES resource.These health checks should be able to provide the interfaces admin operational state with necessary details.

### Usage
- This platform agnostic role enables the user to perform INTERFACES health checks.Users can perform following health checks:
       `all_operational_state_up`
       `all_operational_state_down` 
       `min_operational_state_up`
       `all_administratnal_state_up`
       `all_administratnal_state_down` 
       `min_administratnal_state_up`
      
  
- This role enables users to create a runtime brownfield inventory with all the INTERFACES configuration in terms of host vars. These host vars are ansible facts which have been gathered through the *_interfaces, *_l2_interfaces and *_l3_interfaces network resource module.The tasks offered by this role could be observed as below:

### Perform INTERFACES Health Checks
- Health Checks operation fetch the current status INTERFACES operation state health.

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
      actions:
        - name: health_check
          vars:
            details: True
            checks:
              - name: all_operational_state_up
              - name: all_operational_state_down 
              - name: min_operational_state_up
                min_count: 1
              - name: all_administratnal_state_up
              - name: all_administratnal_state_down 
              - name: min_administratnal_state_up
                min_count: 1
```


### Building Brownfield Inventory with Persist
- Persist operation fetch the interfaces,L2 interfaces and L3 interfaces facts and store them as host vars.
- Result of successful Persist operation would be an Inventory directory having facts as host vars acting as SOT
  for operations like deploy, etc.

```yaml
- name: Persist the facts into host vars
  hosts: iosxr
  gather_facts: false
  tasks:
  - name: INTERFACES Manager
    ansible.builtin.include_role:
      name: network.interfaces.run
    vars:
      actions:
        - name: persist
          inventory_directory: './inventory'
```

#### Gather INTERFACES Facts
- Gather operation gathers the running-confguration specific to interfaces, l2-interfaces, l3-interfaces resources.

```yaml
- name: Gather Facts
  hosts: iosxr
  gather_facts: false
  tasks:
  - name: INTERFACES Manager
    ansible.builtin.include_role:
      name: network.interface.run
    vars:
      actions:
        - name: gather
```

#### Deploy INTERFACES Configuration
- Deploy operation will read the facts from the provided/default inventory and deploy the changes on to the appliances.

```yaml
- name: Deploy host vars facts
  hosts: iosxr
  gather_facts: false
  tasks:
  - name: INTERFACES Manager
    include_role:
      name: network.interfaces.run
    vars:
      actions:
        - name: deploy
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
