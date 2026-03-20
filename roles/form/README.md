Role: opennebula.deploy.form
============================

A role that manages the OneForm service.

Requirements
------------

N/A

Role Variables
--------------

| Name             | Type  | Default   | Example       | Description                                            |
|------------------|-------|-----------|---------------|--------------------------------------------------------|
| `form_bind_addr` | `str` | `0.0.0.0` |               | Bind/Listen address of the OneForm service.            |
| `leader`         | `str` | undefined | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader. |

Dependencies
------------

- opennebula.deploy.opennebula.leader

Example Playbook
----------------

    - hosts: frontend
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.form

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
