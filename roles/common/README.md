Role: opennebula.deploy.common
==============================

A basic role that aggregates global defaults/handlers etc.

Requirements
------------

N/A

Role Variables
--------------

| Name      | Type   | Default   | Example       | Description                                            |
|-----------|--------|-----------|---------------|--------------------------------------------------------|
| `one_vip` | `str`  | first `one_vips` address, otherwise undefined | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader. Explicit values take precedence. |
| `one_vips` | `list` | undefined | see `opennebula/server` | VIP addresses or mappings. Common derives `one_vip` from the first entry if needed. |
| `leader`  | `str`  | undefined | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader. |

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
