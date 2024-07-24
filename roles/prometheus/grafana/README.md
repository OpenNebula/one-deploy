Role: opennebula.deploy.prometheus.grafana
==========================================

A role that manages the Grafana service.

Requirements
------------

N/A

Role Variables
--------------

| Name      | Type   | Default   | Example       | Description                                            |
|-----------|--------|-----------|---------------|--------------------------------------------------------|
| `one_vip` | `str`  | undefined | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader. |
| `leader`  | `str`  | undefined | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader. |

Dependencies
------------

- opennebula.deploy.opennebula.leader

Example Playbook
----------------

    - hosts: grafana
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.prometheus.grafana

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
