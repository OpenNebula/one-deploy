Role: opennebula.deploy.network.common
======================================

A role that aggregates common network defaults/handlers/tasks etc.

Requirements
------------

N/A

Role Variables
--------------

| Name | Type   | Default | Example       | Description                               |
|------|--------|---------|---------------|-------------------------------------------|
| `vn` | `dict` | `{}`    | (check below) | OpenNebula Virtual Network configuration. |

Dependencies
------------

N/A

Example Playbook
----------------

Please check roles `opennebula.deploy.network.frontend` and `opennebula.deploy.network.node`.

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
