Role: opennebula.deploy.helper.numa
===================================

A role that queries NUMA resources.

Requirements
------------

N/A

Role Variables
--------------

| Name | Type | Default | Description |
|------|------|---------|-------------|
|      |      |         |             |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: node
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.numa

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
