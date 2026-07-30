Role: opennebula.deploy.helper.online
=====================================

A role that waits for SSH connectivity (no python required).

Requirements
------------

N/A

Role Variables
--------------

| Name             | Type  | Default        | Description                                     |
|------------------|-------|----------------|-------------------------------------------------|
| `online_timeout` | `int` | `0` (disabled) | Number of seconds to wait for SSH connectivity. |
| `online_delay`   | `int` | `5`            | Number of seconds to wait between retries.      |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: all
      vars:
        online_timeout: 120
      roles:
        - role: opennebula.deploy.helper.online

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
