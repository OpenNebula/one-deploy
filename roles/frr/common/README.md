Role: opennebula.deploy.frr.common
==================================

A role that installs Free Range Routing (FRR) software.

Requirements
------------

N/A

Role Variables
--------------

| Name                | Type   | Default       | Example | Description                                          |
|---------------------|--------|---------------|---------|------------------------------------------------------|
| `frr_repo_key_path` | `dict` | (check below) |         | FRR GPG key paths for Debian/RedHat distros.         |
| `frr_repo_key_url`  | `dict` | (check below) |         | FRR GPG key urls for Debian/RedHat distros.          |
| `frr_repo_path`     | `dict` | (check below) |         | FRR repo definition paths for Debian/RedHat distros. |
| `frr_repo_url`      | `dict` | (check below) |         | FRR repo url for Debian/RedHat distros.              |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: router:node
      vars:
        frr_repo_key_path:
          Debian: /etc/apt/trusted.gpg.d/frr.asc
          RedHat: /etc/pki/rpm-gpg/RPM-GPG-KEY-frr

        frr_repo_key_url:
          Debian: https://deb.frrouting.org/frr/keys.asc
          RedHat: https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x7AB8AC624CBA356CB6216D48F66B5A9140673A87

        frr_repo_path:
          Debian: /etc/apt/sources.list.d/frr.list
          RedHat: /etc/yum.repos.d/frr.repo

        frr_repo_url:
          Debian: https://deb.frrouting.org/frr
          RedHat: https://rpm.frrouting.org/repo/el$releasever
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.frr.common

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
