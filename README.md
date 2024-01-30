# Ansible Network interfaces
[![CI](https://github.com/redhat-cop/network.interfaces/actions/workflows/tests.yml/badge.svg?branch=main&event=schedule)](https://github.com/redhat-cop/network.interfaces/actions/workflows/tests.yml)[!
[OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/7650/badge)](https://bestpractices.coreinfrastructure.org/projects/7650)

This repository contains the `network.interfaces` Ansible Collection.


## About

- Ansible Network interfaces Collection contains the role that provides a platform-agnostic way of
  managing interfaces protocol/resources. This collection provides the user the capabilities to gather,
  deploy, remediate, configure and perform health checks for network interfaces resources. 

- Network interfaces collection can be used by anyone who is looking to manage and maintain interfaces protocol/resources. This includes system administrators and IT professionals.

## Requirements
- [Requires Ansible](https://github.com/redhat-cop/network.interfaces/blob/main/meta/runtime.yml)
- [Requires Content Collections](https://github.com/redhat-cop/network.interfaces/blob/main/galaxy.yml#L5https://forum.ansible.com/c/news/5/none)
- [Testing Requirements](https://github.com/redhat-cop/network.interfaces/blob/main/test-requirements.txt)
- Users also need to include platform collections as per their requirements. The supported platform collections are:
  - [arista.eos](https://github.com/ansible-collections/arista.eos)
  - [cisco.ios](https://github.com/ansible-collections/cisco.ios)
  - [cisco.iosxr](https://github.com/ansible-collections/cisco.iosxr)
  - [cisco.nxos](https://github.com/ansible-collections/cisco.nxos)
  - [junipernetworks.junos](https://github.com/ansible-collections/junipernetworks.junos)

## Installation
To consume this Validated Content from Automation Hub, the following needs to be added to ansible.cfg:
```
[galaxy]
server_list = automation_hub

[galaxy_server.automation_hub]
url=https://console.redhat.com/api/automation-hub/content/published/
auth_url=https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token
token=<SuperSecretToken>
```

Get the required token from the [Automation Hub Web UI](https://console.redhat.com/ansible/automation-hub/token).

With this configured, simply run the following commands:

```
ansible-galaxy collection install network.base
ansible-galaxy collection install network.interfaces
```

## Use Cases

`Build Brownfield Inventory`:
- Users want to be able to get the facts for INTERFACES resources and store it as host_vars thus enabling the capability to get facts for all the hosts within the inventory and store facts in a structured format that acts as SOT.
  
`interfaces Resource Management`:
- Users want to be able to manage the interfaces, L2 interfaces and L3 interfaces configurations. This also includes the enablement of gathering facts, updating INTERFACE resource host-vars and deploying config onto the appliance.

`Detect Drift and remediate`: This enables users to detect any drift between the provided config and the running config and if required then override the running config.

`interfaces Health Checks`:  Users want to be able to perform health checks for INTERFACES resources. These health checks should be able to provide the interface's admin operational state with the necessary details.

- So in summary this platform-agnostic role enables the user to perform interfaces health checks. Users can perform the following health checks:
      `all_operational_state_up`
       `min_operational_state_up`
       `all_administratnal_state_up`
       `min_administratnal_state_up`
  
This role enables users to create a runtime brownfield inventory with all the INTERFACES configurations in terms of host vars. These host vars are ansible facts that have been gathered through the *_interfaces, *_l2_interfaces and *_l3_interfaces network resource module. The tasks offered by this role could be observed  below:

### Perform interfaces Health Checks
- Health Checks operation fetches the current status of INTERFACES operation state health.

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
      operations:
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


### Building Brownfield Inventory with Persist
- Persist operation fetches the interfaces, L2 interfaces and L3 interfaces facts and stores them as host vars.
- The result of a successful Persist operation would be host_vars having YAML formatted resource facts.
- These host_vars could exist locally or even be published to a remote repository acting as SOT for operations like deploy, remediate, detect, etc.

#### fetch interfaces resource facts and build local data_store.
```yaml
- name: Persist the facts into host vars
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network interfaces Manager
    ansible.builtin.include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: persist
      data_store:
        local: "~/interfaces/network"
```

#### fetch interfaces resource facts and publish persisted host_vars inventory to GitHub repository.
```yaml
- name: Persist the facts into remote data_store which is a GitHub repository
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network interfaces Manager
    ansible.builtin.include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: persist
      persist_empty: false
      data_store:
        scm:
          origin:
            url: "{{ your_github_repo }}"
            token: "{{ github_access_token }}"
            user:
              name: "{{ ansible_github }}"
              email: "{{ your_email@example.com }}"
```

### Display Structured Data with Gather
- gather operation gathers the running configuration specific to interfaces, l2-interfaces and, l3-interfaces resources. resources
  and displays these facts in YAML formatted structures.

```yaml
- name: Display interfaces resources in a structured format
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: interfaces Manager
    ansible.builtin.include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: gather
```

### Deploy interfaces Configuration
- Deploy operation will read the facts from the provided/default or remote inventory and deploy the changes onto the appliances.

#### read host_vars from local data_store and deploy onto the field.
```yaml
- name: Deploy changes
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network interfaces Manager
    ansible.builtin.include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: deploy
      data_store:
        local: "~/interfaces/network"
```

#### retrieve host_cars from the GitHub repository and deploy changes onto the field.
```yaml
- name: retrieve config from GitHub repo and deploy changes
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network interfaces Manager
    ansible.builtin.include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: deploy
      persist_empty: false
      data_store:
        scm:
          origin:
            url: "{{ your_github_repo }}"
            token: "{{ github_access_token }}"
            user:
              name: "{{ ansible_github }}"
              email: "{{ your_email@example.com }}"
```

### Detect configuration drift in interfaces Configuration
- Detect operation will read the facts from the local provided/default inventory and detect if any configuration diff exists w.r.t running-config.

#### detect the config difference between host_vars in local data_store and running-config.

```yaml
- name: Configuration drift detection
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network interfaces Manager
    ansible.builtin.include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: detect
      data_store:
        local: "~/interfaces/network"
```

- Detect operation will read the facts from the GitHub repository inventory and detect if any configuration diff exists w.r.t running-config.

#### detect the config difference between host_vars in local data_store and running-config.
```yaml
- name: Configuration drift detection
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network interfaces Manager
    include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: detect
      data_store:
        scm:
          origin:
            url: "{{ your_github_repo }}"
            token: "{{ github_access_token }}"
            user:
              name: "{{ ansible_github }}"
              email: "{{ your_email@example.com }}"
```

#### Remediate configuration drift in interfaces Configuration
- remediate operation will read the facts from the locally provided/default inventory and remediate if any configuration changes are there on the appliances using the overridden state.

```yaml
- name: Remediate configuration
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network interfaces Manager
    include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: remediate
      data_store:
        local: "~/interfaces/network"
```
- remediate operation will read the facts from the GitHub repository and remediate if any configuration changes are there on the appliances using the overridden state.

```yaml
- name: Remediate configuration
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network interfaces Manager
    include_role:
      name: network.interfaces.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: remediate
      data_store:
        scm:
          origin:
            url: "{{ your_github_repo }}"
            token: "{{ github_access_token }}"
            user:
              name: "{{ ansible_github }}"
              email: "{{ your_email@example.com }}"
```
## Testing

The project uses tox to run `ansible-lint` and `ansible-test sanity`.
Assuming this repository is checked out in the proper structure,
e.g. `collections_root/ansible_collections/network/interfaces`, run:

```shell
  tox -e ansible-lint
  tox -e py39-sanity
```

To run integration tests, ensure that your inventory has a `network_base` group.
Depending on what test target you are running, comment out the host(s).

```shell
[network_hosts]
ios
junos

[ios:vars]
< enter inventory details for this group >

[junos:vars]
< enter inventory details for this group >
```

```shell
  ansible-test network-integration -i /path/to/inventory --python 3.9 [target]
```

## Contributing

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against this repository.

Don't know how to start? Refer to the [Ansible community guide](https://docs.ansible.com/ansible/devel/community/index.html)!

Want to submit code changes? Take a look at the [Quick-start development guide](https://docs.ansible.com/ansible/devel/community/create_pr_quick_start.html).

We also use the following guidelines:

* [Collection review checklist](https://docs.ansible.com/ansible/devel/community/collection_contributors/collection_reviewing.html)
* [Ansible development guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
* [Ansible collection development guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections)

### Code of Conduct
This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Release notes

Release notes are available [here](https://github.com/redhat-cop/network.interfaces/blob/main/CHANGELOG.rst).

## Related information

- [Developing network resource modules](https://github.com/ansible-network/networking-docs/blob/main/rm_dev_guide.md)
- [Ansible Networking docs](https://github.com/ansible-network/networking-docs)
- [Ansible Collection Overview](https://github.com/ansible-collections/overview)
- [Ansible Roles overview](https://docs.ansible.com/ansible/2.9/user_guide/playbooks_reuse_roles.html)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.