Role: opennebula.deploy.repository
==================================

A role that creates OpenNebula repository configs on Debian/RedHat-like distros.

Requirements
------------

N/A

Role Variables
--------------

| Name          | Type   | Default       | Example             | Description                                                           |
|---------------|--------|---------------|---------------------|-----------------------------------------------------------------------|
| `one_version` | `str`  | `6.6`         |                     | OpenNebula version (CE/EE is decided by the presence of `one_token`). |
| `one_token`   | `str`  | undefined     | `asd123as:123asd12` | OpenNebula Enterprise Edition subscription token.                     |
| `gpg_keys`    | `list` | (check below) |                     | List of GPG keys to download and install.                             |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: frontend:node
      vars:
        # Specify OpenNebula GPG repo key to install.
        gpg_keys:
          - name: opennebula2
            url: https://downloads.opennebula.io/repo/repo2.key
        # Enable OpenNebula EE repo.
        one_token: 'asd123as:123asd12'
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.repository

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
