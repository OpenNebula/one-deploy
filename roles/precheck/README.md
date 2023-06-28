Role: opennebula.deploy.precheck
================================

A role that performs various checks and assertions.

Requirements
------------

N/A

Role Variables
--------------

N/A

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: frontend:node
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.precheck

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
