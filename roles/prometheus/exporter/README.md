Role: opennebula.deploy.prometheus.exporter
===========================================

A role that manages the Prometheus exporters.

Requirements
------------

N/A

Role Variables
--------------

| Name              | Type  | Default | Example | Description                        |
|-------------------|-------|---------|---------|------------------------------------|
| `node_hypervisor` | `str` | `kvm`   |         | Currently only `kvm` is supported. |


Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: node
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
