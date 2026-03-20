Role: opennebula.deploy.prometheus.exporter
===========================================

A role that manages the Prometheus exporters.

Requirements
------------

N/A

Role Variables
--------------

| Name                   | Type   | Default             | Example       | Description                               |
|------------------------|--------|---------------------|---------------|-------------------------------------------|
| `node_hypervisor`      | `str`  | `kvm`               |               | Currently only `kvm` is supported.        |
| `oneprometheus_limits` | `dict` | (check common role) | (check below) | Define resource limits for systemd units. |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: node
      vars:
        oneprometheus_limits:
          opennebula-libvirt-exporter.service:
            CPUQuota: 25%
            CPUWeight: 25
            MemoryHigh: 128M
            MemoryMax: 256M
          opennebula-node-exporter.service:
            CPUQuota: 25%
            CPUWeight: 25
            MemoryHigh: 64M
            MemoryMax: 128M
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.repository
        - role: opennebula.deploy.prometheus.exporter

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
