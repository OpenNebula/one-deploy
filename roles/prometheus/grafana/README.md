Role: opennebula.deploy.prometheus.grafana
==========================================

A role that manages the Grafana service.

Requirements
------------

N/A

Role Variables
--------------

| Name                    | Type   | Default       | Example       | Description                                              |
|-------------------------|--------|---------------|---------------|----------------------------------------------------------|
| `grafana_repo_key_path` | `dict` | (check below) |               | Grafana GPG key paths for Debian/RedHat distros.         |
| `grafana_repo_key_url`  | `dict` | (check below) |               | Grafana GPG key urls for Debian/RedHat distros.          |
| `grafana_repo_path`     | `dict` | (check below) |               | Grafana repo definition paths for Debian/RedHat distros. |
| `grafana_repo_url`      | `dict` | (check below) |               | Grafana repo url for Debian/RedHat distros.              |
| `one_vip`               | `str`  | undefined     | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader.   |
| `leader`                | `str`  | undefined     | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader.   |

Dependencies
------------

- opennebula.deploy.opennebula.leader

Example Playbook
----------------

    - hosts: grafana
      vars:
        grafana_repo_key_path:
          Debian: /etc/apt/trusted.gpg.d/grafana.asc
          RedHat: /etc/pki/rpm-gpg/RPM-GPG-KEY-grafana

        grafana_repo_key_url:
          Debian: https://apt.grafana.com/gpg.key
          RedHat: https://rpm.grafana.com/gpg.key

        grafana_repo_path:
          Debian: /etc/apt/sources.list.d/grafana.list
          RedHat: /etc/yum.repos.d/grafana.repo

        grafana_repo_url:
          Debian: https://apt.grafana.com
          RedHat: https://rpm.grafana.com
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
