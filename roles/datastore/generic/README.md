Role: opennebula.deploy.datastore.generic
=========================================

A role that manages OpenNebula datastores (`generic` mode).

Requirements
------------

N/A

Role Variables
--------------

| Name          | Type   | Default   | Example                                | Description                                                                    |
|---------------|--------|-----------|----------------------------------------|--------------------------------------------------------------------------------|
| `ds.mode`     | `str`  | `ssh`     |                                        | OpenNebula Datastore configuration mode: `ssh`, `shared`, `ceph` or `generic`. |
| `ds.config`   | `dict` | `{}`      | (check below)                          | OpenNebula Datastore configuration for a specifc mode.                         |
| `ds_defaults` | `dict` |           |                                        | Defaults that are merged with user configs.                                    |
| `ceph.pool`   | `str`  | `one`     |                                        | Name of the Ceph pool dedicated to OpenNebula.                                 |
| `ceph.user`   | `str`  | `libvirt` |                                        | Ceph user that is to have access to the OpenNebula's pool.                     |
| `ceph.host`   | `str`  |           | `10.11.12.13 10.11.12.14:1234`         | Space-separated list of IP:PORT pairs of Ceph mons.                            |
| `ceph.uuid`   | `str`  | `null`    | `fd083b60-82ce-518b-a1a7-fc7bda472338` | UUID of the secret that is to keep Ceph key in Libvirt.                        |
| `node_group`  | `str`  | `node`    |                                        | Custom name of the Node group in the inventory.                                |
| `leader`      | `str`  | undefined | `10.11.12.13`                          | When OpenNebula is in HA mode it points to the Leader.                         |

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
