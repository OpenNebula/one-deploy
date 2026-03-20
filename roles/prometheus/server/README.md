Role: opennebula.deploy.prometheus.server
=========================================

A role that manages the Prometheus and Alertmanager services.

Requirements
------------

N/A

Role Variables
--------------

| Name                   | Type   | Default             | Example       | Description                                   |
|------------------------|--------|---------------------|---------------|-----------------------------------------------|
| `node_hypervisor`      | `str`  | `kvm`               |               | Currently only `kvm` is supported.            |
| `alertmanager_config`  | `str`  | (check below)       |               | Configuration YAML document for Alertmanager. |
| `oneprometheus_limits` | `dict` | (check common role) | (check below) | Define resource limits for systemd units.     |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: frontend
      vars:
        alertmanager_config: |
          ---
          global:
            resolve_timeout: 5m

          route:
            group_by: [alertname]
            group_wait: 1m
            group_interval: 5m
            repeat_interval: 1h
            receiver: discard

          receivers:
            - name: discard

          templates: []

          inhibit_rules:
            - source_match:
                severity: critical
              target_match:
                severity: warning
              equal: [alertname, dev, instance]
        oneprometheus_limits:
          opennebula-alertmanager.service:
            CPUQuota: 25%
            CPUWeight: 150
            MemoryHigh: 128M
            MemoryMax: 256M
          opennebula-exporter.service:
            CPUQuota: 25%
            CPUWeight: 25
            MemoryHigh: 128M
            MemoryMax: 256M
          opennebula-node-exporter.service:
            CPUQuota: 25%
            CPUWeight: 25
            MemoryHigh: 64M
            MemoryMax: 128M
          opennebula-prometheus.service:
            CPUQuota: 100%
            CPUWeight: 100
            MemoryHigh: 1024M
            MemoryMax: 2048M
            IOWeight: 200
            IOReadBandwidthMax: /var/lib/prometheus 50M
            IOWriteBandwidthMax: /var/lib/prometheus 25M
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.repository
        - role: opennebula.deploy.prometheus.server

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
