Role: opennebula.deploy.helper.ntp
==================================

A role that re-configures NTP (chronyd or timesyncd).

Requirements
------------

N/A

Role Variables
--------------

| Name             | Type   | Default   | Description                 |
|------------------|--------|-----------|-----------------------------|
| `ntp`            | `list` | `[]`      | NTP configuration to apply. |
| `ntp[].timezone` | `str`  | undefined | Set TZ.                     |
| `ntp[].locale`   | `str`  | undefined | Set Locale variable(s).     |
| `ntp[].pool`     | `str`  | undefined | Add NTP pool(s).            |
| `ntp[].server`   | `str`  | undefined | Add NTP server(s).          |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: frontend:node
      vars:
        ntp:
          - timezone: UTC
          - locale: LC_TIME=C.UTF-8
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
