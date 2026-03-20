Role: opennebula.deploy.prometheus.grafana
==========================================

A role that manages the Grafana service.

Requirements
------------

N/A

Role Variables
--------------

| Name                   | Type   | Default             | Example       | Description                                            |
|------------------------|--------|---------------------|---------------|--------------------------------------------------------|
| `one_vip`              | `str`  | undefined           | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader. |
| `leader`               | `str`  | undefined           | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader. |
| `oneprometheus_limits` | `dict` | (check common role) | (check below) | Define resource limits for systemd units.              |

Dependencies
------------

- opennebula.deploy.opennebula.leader

Example Playbook
----------------

    - hosts: grafana
      vars:
        oneprometheus_limits:
          grafana-server.service:
            CPUQuota: 100%
            CPUWeight: 100
            MemoryHigh: 1024M
            MemoryMax: 2048M
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.repository
        - role: opennebula.deploy.prometheus.grafana

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
