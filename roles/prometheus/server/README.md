Role: opennebula.deploy.prometheus.server
=========================================

A role that manages the Prometheus and Alertmanager services.

Requirements
------------

N/A

Role Variables
--------------

| Name                                | Type   | Default               | Example       | Description                                        |
|-------------------------------------|--------|-----------------------|---------------|----------------------------------------------------|
| `node_hypervisor`                   | `str`  | `kvm`                 |               | Currently only `kvm` is supported.                 |
| `oneprometheus_config.prometheus`   | `str`  | (check role defaults) |               | Configuration YAML document for Prometheus.        |
| `oneprometheus_config.alertmanager` | `str`  | (check role defaults) |               | Configuration YAML document for Alertmanager.      |
| `oneprometheus_components`          | `dict` | (check common role)   | (check below) | OpenNebula Prometheus stack component definitions. |
| `oneprometheus_limits`              | `dict` | (check common role)   | (check below) | Define resource limits for systemd units.          |
| `oneprometheus_labels`              | `dict` | undefined             | (check below) | Define custom labels.                              |
| `oneprometheus_rules`               | `dict` | (check common role)   | (check below) | Define custom rules.                               |

Dependencies
------------

- ansible.utils
- opennebula.deploy.prometheus.common
- opennebula.deploy.repository
- opennebula.deploy.opennebula.leader

Example Inventory
-----------------

```yaml
all:
  vars:
    oneprometheus_components:
      opennebula-alertmanager: { enabled: false }
      opennebula-lvm-exporter: { enabled: true }
      opennebula-ovs-exporter: { enabled: true }

    oneprometheus_rules:
      # NOTE: Ansible treats YAML values tagged with !unsafe as literal text
      #       and skips Jinja templating for those values.
      host-alerts.yml: !unsafe |
        groups:
          - name: OpenNebulaHosts
            rules:
              - alert: HostExporterDown
                expr: 'up{job="node_exporter"} == 0'
                for: 5m
                annotations:
                  summary: 'Exporter down on {{ $labels.instance }}'
      asd-rules.yml: >-
        {{ lookup('ansible.builtin.file', inventory_dir ~ '/rules/asd-rules.yml') }}

frontend:
  hosts:
    fe01:
      oneprometheus_labels:
        fqdn: fe01.example.com
        location: madrid

node:
  hosts:
    node01:
      oneprometheus_labels:
        fqdn: node01.example.com
        location: madrid
```

Example Playbook
----------------

```yaml
- hosts: frontend
  vars:
    oneprometheus_config:
      alertmanager: |
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
      opennebula-mysql-exporter.service:
        CPUQuota: 25%
        CPUWeight: 25
        MemoryHigh: 128M
        MemoryMax: 256M
      opennebula-node-exporter.service:
        CPUQuota: 25%
        CPUWeight: 25
        MemoryHigh: 64M
        MemoryMax: 128M
      opennebula-ovs-exporter.service:
        CPUQuota: 50%
        CPUWeight: 25
        MemoryHigh: 256M
        MemoryMax: 512M
      opennebula-prometheus.service:
        CPUQuota: 100%
        CPUWeight: 100
        MemoryHigh: 1024M
        MemoryMax: 2048M
        IOWeight: 200
        IOReadBandwidthMax: /var/lib/prometheus 50M
        IOWriteBandwidthMax: /var/lib/prometheus 25M
        storage.tsdb.retention.size: 50GB
        storage.tsdb.retention.time: 30d
      opennebula-smartctl-exporter.service:
        CPUQuota: 25%
        CPUWeight: 25
        MemoryHigh: 128M
        MemoryMax: 256M
  roles:
    - role: opennebula.deploy.helper.facts
    - role: opennebula.deploy.repository
    - role: opennebula.deploy.prometheus.server
```

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
