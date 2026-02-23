Role: opennebula.deploy.helper.ntp
==================================

A role that re-configures NTP (chronyd or timesyncd).

Requirements
------------

N/A

Role Variables
--------------

| Name  | Type   | Default | Example       | Description                 |
|-------|--------|---------|---------------|-----------------------------|
| `ntp` | `list` | `[]`    | (check below) | NTP configuration to apply. |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: frontend:node
      vars:
        ntp:
          - pool: pool.ntp.org
          - server: ntp.icm.edu.pl
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.ntp

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
