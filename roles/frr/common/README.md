Role: opennebula.deploy.frr.common
==================================

A role that installs Free Range Routing (FRR) software.

Requirements
------------

N/A

Role Variables
--------------

| Name | Type | Default | Example | Description |
|------|------|---------|---------|-------------|

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: router:node
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.frr.common

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
