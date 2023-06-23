Role: opennebula.deploy.flow
============================

A role that manages the OneFlow service.

Requirements
------------

N/A

Role Variables
--------------

| Name             | Type  | Default   | Example       | Description                                            |
|------------------|-------|-----------|---------------|--------------------------------------------------------|
| `flow_bind_addr` | `str` | `0.0.0.0` |               | Bind/Listen address of the OneFlow service.            |
| `leader`         | `str` | undefined | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader. |

Dependencies
------------

- opennebula.deploy.opennebula.leader

Example Playbook
----------------

    - hosts: frontend
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.repository
        - role: opennebula.deploy.flow

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
