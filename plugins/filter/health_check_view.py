from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
    name: health_check_view
    author: Ashwini Mhatre (@amhatre)
    version_added: "1.0.0"
    short_description: Generate the filtered health check dict based on the provided target.
    description:
        - Generate the filtered health check dict based on the provided target.
    options:
      health_facts:
        description: Specify the health check dictionary.
        type: dict
"""

EXAMPLES = r"""
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
            details: False
            checks:
              - name: all_operational_state_up
              - name: min_operational_state_up
                min_count: 1
              - name: all_admin_state_up
              - name: min_admin_state_up
                min_count: 1

# TASK [network.interfaces.run : INTERFACES health checks] ***********************
# task path: /Users/amhatre/ansible-collections/collections/ansible_collections/network/interfaces/roles/run/tasks/includes/health_check.yaml:10
# ok: [10.0.150.231] => {
#     "health_checks": {
#         "all_admin_state_up": {
#             "check_status": "successful",
#             "interfaces_status_summery": {
#                 "admin_down": 0,
#                 "admin_up": 4,
#                 "down": 0,
#                 "total": 4,
#                 "up": 4
#             }
#         },
#         "all_operational_state_up": {
#             "check_status": "successful",
#             "interfaces_status_summery": {
#                 "admin_down": 0,
#                 "admin_up": 4,
#                 "down": 0,
#                 "total": 4,
#                 "up": 4
#             }
#         },
#         "min_admin_state_up": {
#             "check_status": "successful",
#             "interfaces_status_summery": {
#                 "admin_down": 0,
#                 "admin_up": 4,
#                 "down": 0,
#                 "total": 4,
#                 "up": 4
#             }
#         },
#         "min_operational_state_up": {
#             "check_status": "successful",
#             "interfaces_status_summery": {
#                 "admin_down": 0,
#                 "admin_up": 4,
#                 "down": 0,
#                 "total": 4,
#                 "up": 4
#             }
#         }
#     }
# }
# META: role_complete for 10.0.150.231
# META: ran handlers
# META: ran handlers
#
# PLAY RECAP *********************************************************************
# 10.0.150.231               : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

- name: Perform interfaces health checks with details as true
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
            details: true
            checks:
              - name: all_operational_state_up
                ignore_errors: true
              - name: min_operational_state_up
                min_count: 1
                ignore_errors: true
              - name: all_admin_state_up
                ignore_errors: true
              - name: min_admin_state_up
                ignore_errors: true
                min_count: 1

# TASK [network.interfaces.run : INTERFACES health checks] *************************************************************
# [WARNING]: Persistent connection logging is enabled for 10.0.150.115. This will log ALL interactions and WILL NOT
# redact sensitive configuration like passwords. USE WITH CAUTION!
# ok: [10.0.150.115] => {
#     "failed_when_result": false,
#     "health_checks": {
#         "all_admin_state_up": {
#             "check_status": "unsuccessful",
#             "interfaces_status_summery": {
#                 "admin_down": 4,
#                 "admin_up": 4,
#                 "down": 1,
#                 "total": 8,
#                 "up": 3
#             }
#         },
#         "all_operational_state_up": {
#             "check_status": "unsuccessful",
#             "interfaces_status_summery": {
#                 "admin_down": 4,
#                 "admin_up": 4,
#                 "down": 1,
#                 "total": 8,
#                 "up": 3
#             }
#         },
#         "detailed_interface_status_summery": {
#             "interfaces": {
#                 "Bundle-Ether11": {
#                     "admin": "up",
#                     "name": "Bundle-Ether11",
#                     "operational": "down,"
#                 },
#                 "GigabitEthernet0/0/0/0": {
#                     "admin": "up",
#                     "name": "GigabitEthernet0/0/0/0",
#                     "operational": "up,"
#                 },
#                 "GigabitEthernet0/0/0/1": {
#                     "admin": "down",
#                     "name": "GigabitEthernet0/0/0/1",
#                     "operational": "NA"
#                 },
#                 "GigabitEthernet0/0/0/2": {
#                     "admin": "down",
#                     "name": "GigabitEthernet0/0/0/2",
#                     "operational": "NA"
#                 },
#                 "Loopback888": {
#                     "admin": "down",
#                     "name": "Loopback888",
#                     "operational": "NA"
#                 },
#                 "Loopback999": {
#                     "admin": "down",
#                     "name": "Loopback999",
#                     "operational": "NA"
#                 },
#                 "MgmtEth0/RP0/CPU0/0": {
#                     "admin": "up",
#                     "name": "MgmtEth0/RP0/CPU0/0",
#                     "operational": "up,"
#                 },
#                 "Null0": {
#                     "admin": "up",
#                     "name": "Null0",
#                     "operational": "up,"
#                 }
#             }
#         },
#         "min_admin_state_up": {
#             "check_status": "successful",
#             "interfaces_status_summery": {
#                 "admin_down": 4,
#                 "admin_up": 4,
#                 "down": 1,
#                 "total": 8,
#                 "up": 3
#             }
#         },
#         "min_operational_state_up": {
#             "check_status": "successful",
#             "interfaces_status_summery": {
#                 "admin_down": 4,
#                 "admin_up": 4,
#                 "down": 1,
#                 "total": 8,
#                 "up": 3
#             }
#         },
#         "status": "successful"
#     }
# }
#
# PLAY RECAP ***********************************************************************************************************
# 10.0.150.115               : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
#
#

- name: Perform interfaces health checks with ignore_errors as false
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
            details: true
            checks:
              - name: all_operational_state_up
                ignore_errors: false
              - name: min_operational_state_up
                min_count: 1
                ignore_errors: true
              - name: all_admin_state_up
                ignore_errors: true
              - name: min_admin_state_up
                ignore_errors: true
                min_count: 1

#
# TASK [network.interfaces.run : INTERFACES health checks] *************************************************************
# [WARNING]: Persistent connection logging is enabled for 10.0.150.115. This will log ALL interactions and WILL NOT
# redact sensitive configuration like passwords. USE WITH CAUTION!
# fatal: [10.0.150.115]: FAILED! => {
#     "failed_when_result": true,
#     "health_checks": {
#         "all_admin_state_up": {
#             "check_status": "unsuccessful",
#             "interfaces_status_summery": {
#                 "admin_down": 4,
#                 "admin_up": 4,
#                 "down": 1,
#                 "total": 8,
#                 "up": 3
#             }
#         },
#         "all_operational_state_up": {
#             "check_status": "unsuccessful",
#             "interfaces_status_summery": {
#                 "admin_down": 4,
#                 "admin_up": 4,
#                 "down": 1,
#                 "total": 8,
#                 "up": 3
#             }
#         },
#         "detailed_interface_status_summery": {
#             "interfaces": {
#                 "Bundle-Ether11": {
#                     "admin": "up",
#                     "name": "Bundle-Ether11",
#                     "operational": "down,"
#                 },
#                 "GigabitEthernet0/0/0/0": {
#                     "admin": "up",
#                     "name": "GigabitEthernet0/0/0/0",
#                     "operational": "up,"
#                 },
#                 "GigabitEthernet0/0/0/1": {
#                     "admin": "down",
#                     "name": "GigabitEthernet0/0/0/1",
#                     "operational": "NA"
#                 },
#                 "GigabitEthernet0/0/0/2": {
#                     "admin": "down",
#                     "name": "GigabitEthernet0/0/0/2",
#                     "operational": "NA"
#                 },
#                 "Loopback888": {
#                     "admin": "down",
#                     "name": "Loopback888",
#                     "operational": "NA"
#                 },
#                 "Loopback999": {
#                     "admin": "down",
#                     "name": "Loopback999",
#                     "operational": "NA"
#                 },
#                 "MgmtEth0/RP0/CPU0/0": {
#                     "admin": "up",
#                     "name": "MgmtEth0/RP0/CPU0/0",
#                     "operational": "up,"
#                 },
#                 "Null0": {
#                     "admin": "up",
#                     "name": "Null0",
#                     "operational": "up,"
#                 }
#             }
#         },
#         "min_admin_state_up": {
#             "check_status": "successful",
#             "interfaces_status_summery": {
#                 "admin_down": 4,
#                 "admin_up": 4,
#                 "down": 1,
#                 "total": 8,
#                 "up": 3
#             }
#         },
#         "min_operational_state_up": {
#             "check_status": "successful",
#             "interfaces_status_summery": {
#                 "admin_down": 4,
#                 "admin_up": 4,
#                 "down": 1,
#                 "total": 8,
#                 "up": 3
#             }
#         },
#         "status": "unsuccessful"
#     }
# }
#
# PLAY RECAP ***********************************************************************************************************
# 10.0.150.115               : ok=4    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0

"""

RETURN = """
  health_checks:
    description: INTERFACES health checks
    type: dict

"""

from ansible.errors import AnsibleFilterError

ARGSPEC_CONDITIONALS = {}


def _process_health_facts(health_facts):
    """ """
    interface_status_summary = {
        "total": len(health_facts.keys()),
        "up": 0,
        "down": 0,
        "admin_up": 0,
        "admin_down": 0,
    }
    for interface in health_facts.values():

        if "up" in interface.get("admin") or "Up" in interface.get("admin"):
            interface_status_summary["admin_up"] += 1
        else:
            interface_status_summary["admin_down"] += 1

        if "up" in interface.get("operational") or "Up" in interface.get(
            "operational"
        ):
            interface_status_summary["up"] += 1
        elif "down" in interface.get("operational") or "Down" in interface.get(
            "operational"
        ):
            interface_status_summary["down"] += 1
    return interface_status_summary


def health_check_view(*args, **kwargs):
    params = ["health_facts", "target"]
    data = dict(zip(params, args))
    data.update(kwargs)
    if len(data) < 2:
        raise AnsibleFilterError(
            "Missing either 'health facts' or 'other value in filter input,"
            "refer 'network.interfaces.health_check_view' filter plugin documentation for details",
        )

    health_facts = data["health_facts"]
    detailed_health_facts = health_facts
    target = data["target"]
    if "interfaces" in health_facts:
        health_facts = _process_health_facts(health_facts["interfaces"])

    health_checks = {}
    if target["name"] == "health_check":
        h_vars = target.get("vars")
        if h_vars:
            checks = h_vars.get("checks")
            details = h_vars.get("details")
            for i in ["all_operational_state_up", "all_admin_state_up", "min_operational_state_up", "min_admin_state_up"]:
                option, int_dict, status = process_stats(i, health_facts, checks)
                if int_dict:
                    health_checks.update({option: int_dict})
                if status:
                    health_checks.update({"status": status})
        else:
            health_checks = health_facts
    if details:
        health_checks.update({"detailed_interface_status_summery": detailed_health_facts})
    if "status" not in health_checks:
        health_checks['status'] = "successful"
    return health_checks


def process_stats(option, health_facts, checks):
    opr = is_present(checks, option)
    status = None
    int_dict = {}
    if opr:
        if option == "all_admin_state_up":
            check_status = get_admin_status(health_facts, "admin_up")
        elif option == "min_operational_state_up":
            check_status = get_status(health_facts, "min", opr["min_count"])
        elif option == "min_admin_state_up":
            check_status = get_admin_status(health_facts, "min", opr["min_count"])
        else:
            check_status = get_status(health_facts, "up")
        int_dict = {"check_status": check_status}
        int_dict.update({"interfaces_status_summery": health_facts})
        if check_status == "unsuccessful" and not opr.get("ignore_errors"):
            status = 'unsuccessful'
    return option, int_dict, status


def get_status(stats, check, count=None):
    if check in ("up", "down"):
        return "successful" if stats["total"] == stats[check] else "unsuccessful"
    else:
        return "successful" if count <= stats["up"] else "unsuccessful"


def get_admin_status(stats, check, count=None):
    if check in ("admin_up", "admin_down"):
        return "successful" if stats["total"] == stats[check] else "unsuccessful"
    else:
        return "successful" if count <= stats["admin_up"] else "unsuccessful"


def is_present(health_checks, option):
    for item in health_checks:
        if item["name"] == option:
            return item
    return None


class FilterModule(object):
    """health_check_view"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"health_check_view": health_check_view}
