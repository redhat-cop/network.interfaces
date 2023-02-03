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
            details: True
            checks:
              - name: any_state_up
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
#         "any_state_up": {
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


"""

RETURN = """
  health_checks:
    description:INTERFACES health checks 
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
        else:
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
            ignore_errors = h_vars.get("ignore_errors")
            details = h_vars.get("details")
            stats = health_facts
            if is_present(checks, "all_operational_state_up"):
                int_dict = {"check_status": get_status(health_facts, "up")}
                int_dict.update({"interfaces_status_summery": stats})
                health_checks["all_operational_state_up"] = int_dict
            if is_present(checks, "all_admin_state_up"):
                int_dict = {
                    "check_status": get_admin_status(health_facts, "admin_up")
                }
                int_dict.update({"interfaces_status_summery": stats})
                health_checks["all_admin_state_up"] = int_dict

            opr = is_present(checks, "min_operational_state_up")
            if opr:
                int_dict = {
                    "check_status": get_status(stats, "min", opr["min_count"])
                }
                int_dict.update({"interfaces_status_summery": stats})
                health_checks["min_operational_state_up"] = int_dict

            opr = is_present(checks, "min_admin_state_up")
            if opr:
                int_dict = {
                    "check_status": get_admin_status(
                        stats, "min", opr["min_count"]
                    )
                }
                int_dict.update({"interfaces_status_summery": stats})
                health_checks["min_admin_state_up"] = int_dict
            opr = is_present(checks, "any_state_up")
            if opr:
                int_oper = get_status(stats, "min", 1)
                int_admin = get_admin_status(stats, "min", 1)
                if int_oper == "successful" or int_admin == "successful":
                    check_status = "successful"
                else:
                    check_status = "unsuccessful"
                int_dict = {
                    "check_status": check_status
                }
                int_dict.update({"interfaces_status_summery": stats})
                health_checks["any_state_up"] = int_dict

        else:
            health_checks = health_facts
    fail_task(health_checks, ignore_errors)

    if details:
        health_checks.update({"detailed_interface_status_summery": detailed_health_facts})
    return health_checks

def fail_task(health_facts, ignore_errors):
    for i in health_facts.values():
        if i.get("check_status") == "unsuccessful" and not ignore_errors:
            raise AnsibleFilterError("Failed to get some health checks")

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
