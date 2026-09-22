Role: opennebula.deploy.opennebula.upgrade
==========================================

A role that upgrades OpenNebula.

Requirements
------------

N/A

Role Variables
--------------

N/A

Dependencies
------------

- `opennebula.deploy.database`
- `opennebula.deploy.repository`
- `opennebula.deploy.opennebula.server`
- `opennebula.deploy.opennebula.leader`

Example Playbook
----------------

    - hosts: frontend:node
      vars:
        one_version: '7.4.1'
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.opennebula.upgrade

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
