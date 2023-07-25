===========================================
Network Interfaces Collection Release Notes
===========================================

.. contents:: Topics


v3.0.1
======

Documentation Changes
---------------------

- Added installation steps to the documentation.

v3.0.0
======

Major Changes
-------------

- Rename role variables to follow the role_name_var variable naming rule for roles.
- Rename variable action as operation, on behalf of ansible-lint var-naming error for reserved Ansible keywords.

Documentation Changes
---------------------

- Fix misspelled words in README, and fix examples.

v2.0.0
======

Major Changes
-------------

- Enable scm based operations(https://github.com/redhat-cop/network.interfaces/issues/7)

Bugfixes
--------

- Fix issue in 'health_check' action.

Documentation Changes
---------------------

- Update README with collection installation commands.

v1.0.0
======

Major Changes
-------------

- Add Network INTERFACES role.

Documentation Changes
---------------------

- Add docs for Remediate and Detect action.
- Fix collection name in galaxy.yaml.
