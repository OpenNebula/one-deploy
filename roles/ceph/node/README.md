Role: opennebula.deploy.ceph.node
=================================

A role that manages Ceph related settings on an OpenNebula Node.

Requirements
------------

N/A

Role Variables
--------------

| Name             | Type   | Default   | Example                                | Description                                                |
|------------------|--------|-----------|----------------------------------------|------------------------------------------------------------|
| `ceph.pool`      | `str`  | `one`     |                                        | Name of the Ceph pool dedicated to OpenNebula.             |
| `ceph.user`      | `str`  | `libvirt` |                                        | Ceph user that is to have access to the OpenNebula's pool. |
| `ceph.uuid`      | `str`  | `null`    | `fd083b60-82ce-518b-a1a7-fc7bda472338` | UUID of the secret that is to keep Ceph key in Libvirt.    |
| `mon_group_name` | `str`  | `mons`    |                                        | Name of the inventory group keeping all Ceph mons.         |

Dependencies
------------

Example Playbook
----------------

    - hosts: node
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.ceph.node

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
