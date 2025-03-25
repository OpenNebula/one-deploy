Role: opennebula.deploy.repository
==================================

A role that creates various package repository configs on Debian/RedHat-like distros.

Requirements
------------

N/A

Role Variables
--------------

| Name                            | Type   | Default       | Example             | Description                                                           |
|---------------------------------|--------|---------------|---------------------|-----------------------------------------------------------------------|
| `one_version`                   | `str`  | `6.8`         | `6.8.3`             | OpenNebula version (CE/EE is decided by the presence of `one_token`). |
| `one_token`                     | `str`  | undefined     | `asd123as:123asd12` | OpenNebula Enterprise Edition subscription token.                     |
| `repos_enabled`                 | `list` | (check below) | `[frr]`             | Enable installation of specific repos.                                |
|                                 |        |               |                     |                                                                       |
| `ceph_repo_force_trusted`       | `bool` | `false`       |                     | Disable Ceph GPG / SSL repo verification.                             |
| `ceph_repo_key_path`            | `dict` |               |                     | Ceph GPG key paths for Debian/RedHat distros.                         |
| `ceph_repo_key_url`             | `dict` |               |                     | Ceph GPG key urls for Debian/RedHat distros.                          |
| `ceph_repo_path`                | `dict` |               |                     | Ceph repo definition paths for Debian/RedHat distros.                 |
| `ceph_repo_url`                 | `dict` |               |                     | Ceph repo url for Debian/RedHat distros.                              |
|                                 |        |               |                     |                                                                       |
| `frr_repo_force_trusted`        | `bool` | `false`       |                     | Disable FRR GPG / SSL repo verification.                              |
| `frr_repo_key_path`             | `dict` |               |                     | FRR GPG key paths for Debian/RedHat distros.                          |
| `frr_repo_key_url`              | `dict` |               |                     | FRR GPG key urls for Debian/RedHat distros.                           |
| `frr_repo_path`                 | `dict` |               |                     | FRR repo definition paths for Debian/RedHat distros.                  |
| `frr_repo_url`                  | `dict` |               |                     | FRR repo url for Debian/RedHat distros.                               |
|                                 |        |               |                     |                                                                       |
| `grafana_repo_force_trusted`    | `bool` | `false`       |                     | Disable Grafana GPG / SSL repo verification.                          |
| `grafana_repo_key_path`         | `dict` |               |                     | Grafana GPG key paths for Debian/RedHat distros.                      |
| `grafana_repo_key_url`          | `dict` |               |                     | Grafana GPG key urls for Debian/RedHat distros.                       |
| `grafana_repo_path`             | `dict` |               |                     | Grafana repo definition paths for Debian/RedHat distros.              |
| `grafana_repo_url`              | `dict` |               |                     | Grafana repo url for Debian/RedHat distros.                           |
|                                 |        |               |                     |                                                                       |
| `opennebula_repo_force_trusted` | `bool` | `false`       |                     | Disable OpenNebula GPG / SSL repo verification.                       |
| `opennebula_repo_key_path`      | `dict` |               |                     | OpenNebula GPG key paths for Debian/RedHat distros.                   |
| `opennebula_repo_key_url`       | `dict` |               |                     | OpenNebula GPG key urls for Debian/RedHat distros.                    |
| `opennebula_repo_path`          | `dict` |               |                     | OpenNebula repo definition paths for Debian/RedHat distros.           |
| `opennebula_repo_url`           | `dict` |               | (check below)       | OpenNebula repo url for Debian/RedHat distros.                        |
| `opennebula_repo_pre_enable`    | `dict` |               | (check below)       | Definition of DNF repos to pre-enable in RedHat-like distros.         |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: frontend:node
      vars:
        repos_enabled: [ceph, frr, grafana, opennebula] # defaults

        # Enable OpenNebula EE repo.
        one_token: 'asd123as:123asd12'

        # Enable only 'epel' and 'crb' DNF repos in Alma Linux 9
        opennebula_repo_pre_enable:
          AlmaLinux:
            config_manager:
              '9': [epel, crb]

        # Use custom / local / insecure OpenNebula repo.
        opennebula_repo_force_trusted: true
        opennebula_repo_url:
          RedHat: http://10.11.12.13/repo/6.8/AlmaLinux/
          Ubuntu: http://10.11.12.13/repo/6.8/Ubuntu/22.04/
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.repository

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
