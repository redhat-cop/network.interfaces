network.interfaces.health_checks
================================

The role enables user to perform `network.interfaces` health checks.

Users would be able to perform health checks for INTERFACES resources. These health checks should be able to provide the interface's admin operational state with the necessary details.

### Supported Health Checks:
- all_operational_state_up: Verifies if all interfaces are up.
- min_operational_state_up: Checks if a minimum number of interfaces are up.
- all_administratnal_state_up: Checks if all administrative interfaces are up.
- min_administratnal_state_up: Summarizes the overall interfaces status, including metrics like state, messages sent/received, and protocol version.

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
      name: network.interfaces.health_checks
    vars:
      ansible_network_os: cisco.iosxr.iosxr
      interfaces_health_check:
        name: health_check
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

## License
GNU General Public License v3.0 or later.
See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information
- Ansible Network Content Team