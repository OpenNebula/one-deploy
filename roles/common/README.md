Role: opennebula.deploy.common
==============================

A basic role that aggregates global defaults/handlers etc.

Requirements
------------

N/A

Role Variables
--------------

| Name                 | Type   | Default   | Example       | Description                                             |
|----------------------|--------|-----------|---------------|---------------------------------------------------------|
| `features.gateproxy` | `bool` | `false`   |               | Indicates if OneGate Proxy service is enabled/disabled. |
| `one_vip`            | `str`  | undefined | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader.  |
| `leader`             | `str`  | undefined | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader.  |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: all
      roles:
        - role: opennebula.deploy.common

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
