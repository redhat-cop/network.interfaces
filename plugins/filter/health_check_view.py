from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
    name: health_check_view
    author: Rohit Thakur (@rohitthakur2590)
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
- set_fact:
   "health_facts":{
   "down_peer_count":"",
   "group_count":"",
   "neighbors":[
      {
         "msg_rcvd":3839,
         "msg_sent":3834,
         "path":{
            "memory_usage":168,
            "total_entries":2
         },
         "peer":"12.0.0.1",
         "peer_as":500,
         "peer_state":"1",
         "total_memory":776
      },
      {
         "msg_rcvd":0,
         "msg_sent":0,
         "path":{
            "memory_usage":168,
            "total_entries":2
         },
         "peer":"23.0.0.1",
         "peer_as":500,
         "peer_state":"Idle",
         "total_memory":776
      }
   ],
   "peer_count":""
}

- set_fact:
    "action": {
   "name":"health_check",
   "vars":{
      "checks":[
         {
            "name":"all_neighbors_up"
         },
         {
            "name":"all_neighbors_down"
         },
         {
            "min_count":1,
            "name":"min_neighbors_up"
         }
      ]
   }
} 

- name: Get final list of parameters
  register: result
  set_fact:
    final_params: "{{ health_facts|health_check_view(action) }}"

# TASK [Target list] **********************************************************
# ok: [localhost] => {
#     "msg": {
#         "actionable": [
#             "2",
#             "4"
#         ],
#         "unsupported": []
#     }
# }
"""

RETURN = """
  health_checks:
    description: INTERFACE health checks 
    type: dict

"""

from ansible.errors import AnsibleFilterError

ARGSPEC_CONDITIONALS = {}

def _process_health_facts(health_facts):
    """

    """
    interface_status_summary = {
        "total": len(health_facts.keys()),
        "up": 0,
        "down": 0,
        "admin_up": 0,
        "admin_down": 0
    }
    for interface in health_facts.values():
        if "up" in interface.get("admin") or "Up" in interface.get("admin"):
            interface_status_summary["admin_up"]+=1
        else:
            interface_status_summary["admin_down"] += 1

        if "up" in interface.get("operational") or "Up" in interface.get("operational"):
            interface_status_summary["up"]+=1
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
    target = data["target"]
    if "interfaces" in health_facts:
        health_facts = _process_health_facts(health_facts["interfaces"])

    health_checks = {}
    if target['name'] == 'health_check':
        h_checks = target.get('vars')
        if h_checks:
            checks = h_checks.get('checks')
            stats = health_facts
            health_checks.update({"interfaces_summery":stats})
            if is_present(checks, 'all_operational_state_up'):
                int_dict = {'check_status': get_status(health_facts, 'up')}
                health_checks['all_operational_state_up'] = int_dict

            if is_present(checks, 'all_operational_state_down'):
                int_dict = {'check_status': get_status(health_facts, 'down')}
                health_checks['all_operational_state_down'] = int_dict
            if is_present(checks, 'all_administratnal_state_up'):
                int_dict = {'check_status': get_admin_status(health_facts, 'admin_up')}
                health_checks['all_administratnal_state_up'] = int_dict

            if is_present(checks, 'all_administratnal_state_down'):
                int_dict = {'check_status': get_admin_status(health_facts, 'admin_down')}
                health_checks['all_administratnal_state_down'] = int_dict

            opr = is_present(checks, 'min_operational_state_up')
            if opr:
                int_dict = {'check_status': get_status(stats, 'min', opr['min_count'])}
                health_checks['min_operational_state_up'] = int_dict

            opr = is_present(checks, 'min_administratnal_state_up')
            if opr:
                int_dict = {'check_status': get_admin_status(stats, 'min', opr['min_count'])}
                health_checks['min_administratnal_state_up'] = int_dict
        else:
            health_checks = health_facts
    return health_checks


def get_status(stats, check, count=None):
    if check in ('up', 'down'):
        return 'successful' if stats['total'] == stats[check] else 'failed'
    else:
        return 'successful' if count <= stats['up'] else 'failed'

def get_admin_status(stats, check, count=None):
    if check in ('admin_up', 'admin_down'):
        return 'successful' if stats['total'] == stats[check] else 'failed'
    else:
        return 'successful' if count <= stats['admin_up'] else 'failed'


def is_present(health_checks, option):
    for item in health_checks:
        if item['name'] == option:
            return item
    return None


class FilterModule(object):
    """health_check_view"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"health_check_view": health_check_view}