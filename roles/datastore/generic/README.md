Role: opennebula.deploy.datastore.generic
=========================================

A role that manages OpenNebula datastores (`generic` mode).

Requirements
------------

N/A

Role Variables
--------------

| Name          | Type   | Default   | Example       | Description                                                            |
|---------------|--------|-----------|---------------|------------------------------------------------------------------------|
| `ds.mode`     | `str`  | `ssh`     |               | OpenNebula Datastore configuration mode: `ssh`, `shared` or `generic`. |
| `ds.config`   | `dict` | `{}`      | (check below) | OpenNebula Datastore configuration for a specifc mode.                 |
| `ds_defaults` | `dict` |           |               | Defaults that are merged with user configs.                            |
| `leader`      | `str`  | undefined | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader.                 |

Dependencies
------------

- opennebula.deploy.opennebula.leader

Example Playbook
----------------

Please check examples from `opennebula.datastores.frontend` and `opennebula.datastore.node` roles.

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
