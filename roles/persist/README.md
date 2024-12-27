# Persist

## Overview
The `persist` role enables users to fetch facts for specified network resources and store them in a YAML-formatted structure. These host variables can be saved either locally or in a remote data store, acting as a single source of truth (SOT) for network configurations.

## Features
- Fetch structured facts for specified resources.
- Persist gathered facts to local directories or remote SCM repositories.
- Enable centralized and version-controlled storage for network configuration data.

## Variables

| Variable Name        | Default Value | Required | Type | Description                                                   | Example |
|:---------------------|:-------------:|:--------:|:----:|:-------------------------------------------------------------|:-------:|
| `ansible_network_os` | `""`          | no      | str  | Network OS for which the facts are being gathered.            | `"cisco.nxos.nxos"` |
| `data_store`         | `""`          | yes      | dict | Specifies the storage configuration (local or SCM).           | See examples below. |

## Usage
Below are examples demonstrating how to use the `persist` role:

### Example 1: Persist to Local Data Store
In this example, gathered facts are stored in a local directory:

```yaml
- name: Persist network facts to local data store
  hosts: all
  gather_facts: true
  tasks:
    - name: Invoke persist role
      ansible.builtin.include_role:
        name: network.interfaces.persist
      vars:
        ansible_network_os: cisco.nxos.nxos
        data_store:
          local: "~/data/network"
```
Example Output
When the playbook is executed, the persisted facts will be saved in the specified data store in a structured YAML format.

### Example 2: Persist to SCM repository
In this example, gathered facts are stored in a remote Git repository:
```yaml
- name: Persist network facts to SCM repository
  hosts: all
  gather_facts: true
  tasks:
    - name: Invoke persist role
      ansible.builtin.include_role:
        name: network.interfaces.persist
      vars:
        data_store:
          scm:
            parent_directory: "/home/rhel"
            origin:
              url: "{{ gh_scm_url }}"
              token: "{{ gh_token }}"
              user:
                name: "{{ gh_username }}"
                email: "{{ gh_email }}"
```
Example Output
When the playbook is executed, the persisted facts will be saved in the specified data store in a structured YAML format.

## License
GNU General Public License v3.0 or later.
See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information
- Ansible Network Content Team