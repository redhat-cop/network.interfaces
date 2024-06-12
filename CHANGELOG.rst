===========================================
Network Interfaces Collection Release Notes
===========================================

.. contents:: Topics

v5.0.0
======

Release Summary
---------------

With this release, the minimum required version of `ansible-core` for this collection is `2.15.0`. The last version known to be compatible with `ansible-core` versions below `2.15` is v4.0.0.

Major Changes
-------------

- Bumping `requires_ansible` to `>=2.15.0`, since previous ansible-core versions are EoL now.

Documentation Changes
---------------------

- Update readme as per the common template.

v4.0.0
======

Release Summary
---------------

Starting from this release, the minimum `ansible-core` version this collection requires is `2.14.0`. The last known version compatible with ansible-core<2.14 is `v3.0.1`.

Major Changes
-------------

- Bumping `requires_ansible` to `>=2.14.0`, since previous ansible-core versions are EoL now.

v3.0.1
======

Bugfixes
--------

- Add health_check support for EOS platform(https://github.com/redhat-cop/network.interfaces/issues/19).

v3.0.0
======

Major Changes
-------------

- Rename role variables to follow the role_name_var variable naming rule for roles.
- Rename variable action as operation, on behalf of ansible-lint var-naming error for reserved Ansible keywords.

Documentation Changes
---------------------

- Added installation steps to the documentation.
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
