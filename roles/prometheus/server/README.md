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
| `prometheus_config`    | `str`  | generated           |               | Complete Prometheus YAML document. When set, replaces the generated default. |
| `prometheus_target_labels` | `dict` | `{compute: {}, control_plane: {}}` | (check below) | Extra labels for discovered targets. |
| `prometheus_rule_files` | `dict` | `{}` | (check below) | Rule file names and YAML documents to create beside `prometheus.yml`. |
| `oneprometheus_limits` | `dict` | (check common role) | (check below) | Define resource limits for systemd units.     |

Dependencies
------------

N/A

Prometheus configuration
------------------------

The role manages `/etc/one/prometheus/prometheus.yml` and writes target files
under `/etc/one/prometheus/inventory/`. The default configuration discovers
node exporters through `compute.yml` and `control-plane.yml`, and uses separate
files for the libvirt, OVS, smartctl, LVM, and MySQL exporters. Optional
exporters are included only when their ports respond during deployment. The
compute target list comes from `onehost list`, so it can include hosts outside
the Ansible `node` group. The control-plane file includes every frontend,
including frontends that are also registered compute hosts. A dual-role host
will be scraped twice by a node exporter job that references both files.
Target files are updated on every run; Prometheus
reloads them through file discovery without a service restart.

For an existing installation, apply the Prometheus server tasks with:

    ansible-playbook -i inventory/prometheus-sm23/hosts.yml playbooks/prometheus-config.yml

To test one frontend first, add `--limit fe01`. A repeat run should report no
changes before applying the playbook to the remaining frontends.

This playbook gathers the required facts, finds the OpenNebula leader, and
configures Prometheus on the frontend group. It runs exporter package and
service setup along with discovery and server configuration; it does not manage
the repository or Alertmanager. The Prometheus package and `promtool` must
already be present on the frontends. Rule files referenced
by `prometheus_config` must either be supplied through `prometheus_rule_files`
or already exist on every targeted frontend. For a frontend whose Prometheus
files were removed, supply all referenced rules through `prometheus_rule_files`
in the inventory. Rule files already present on peer frontends do not satisfy
validation on that host.

Use `prometheus_target_labels.compute` to add labels by OpenNebula host name
(`NAME` in `onehost list`) and `prometheus_target_labels.control_plane` by
Ansible frontend inventory name. Label values are converted to strings.
The generated `role` label can be overridden; `one_host_id` always comes from
OpenNebula. For example:

    prometheus_target_labels:
      compute:
        host01:
          fqdn: host01.example.com
          location: madrid
      control_plane:
        fe01:
          fqdn: fe01.example.com
          location: madrid

Set `prometheus_config` to a complete YAML document to control scrape jobs,
`relabel_configs`, and `metric_relabel_configs`. The role validates it with
`promtool` before replacing the active file. Existing manual changes to
`prometheus.yml` must be moved into this variable before the first run with
this version of the role. The role no longer runs `patch_datasources.rb`.

The document can use Ansible variables, so a frontend-specific external label
can be written as `one_fe_instance: '{{ inventory_hostname }}'`. A complete
Prometheus configuration can also be kept in a plain YAML file and loaded with
`lookup('ansible.builtin.file', ...)`. Rule files can be authored the same way:

    prometheus_config: "{{ lookup('ansible.builtin.file', playbook_dir ~ '/prometheus.yml') }}"
    prometheus_rule_files:
      host-alerts.rules: "{{ lookup('ansible.builtin.file', playbook_dir ~ '/rules/host-alerts.rules') }}"

For example, `rules/host-alerts.rules` can contain ordinary Prometheus YAML:

    groups:
      - name: host_alerts
        rules:
          - alert: HostExporterDown
            expr: 'up{job="node_exporter"} == 0'
            for: 5m
            annotations:
              summary: 'Exporter down on {{ $labels.instance }}'

Rule file keys are destination filenames under `/etc/one/prometheus/`. They
may have any name or extension except `prometheus.yml`; path components are
not allowed. Values may be complete YAML strings read from files or YAML
mappings defined directly in inventory. For mappings, use Ansible's `!unsafe`
tag on Prometheus annotation templates so Ansible leaves `{{ ... }}` expressions
for Prometheus. The `rule_files` entries
in a custom `prometheus_config` must use those destination names; the generated
default configuration includes managed rule files automatically. Each file is
checked with `promtool` before installation, and a change restarts Prometheus. Referencing a rule file
that is neither installed by this variable nor already present on the server
causes Prometheus config validation to fail. Custom scrape jobs may reuse
`compute.yml` and `control-plane.yml` and change the exporter port with
`relabel_configs`. To keep the optional exporter reachability checks, use the
generated `ovs.yml`, `smartctl.yml`, and `lvm.yml` files instead.

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

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
