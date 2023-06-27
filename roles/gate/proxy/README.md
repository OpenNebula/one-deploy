Role: opennebula.deploy.gate.proxy
==================================

A role that manages the OneGate Proxy service.

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

    - hosts: node
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.repository
        - role: opennebula.deploy.gate.proxy

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
