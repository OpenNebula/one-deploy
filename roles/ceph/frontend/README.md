Role: opennebula.deploy.ceph.frontend
=====================================

A role that manages Ceph related settings on an OpenNebula Frontend.

Requirements
------------

N/A

Role Variables
--------------

| Name         | Type   | Default   | Example                                | Description                                             |
|--------------|--------|-----------|----------------------------------------|---------------------------------------------------------|
| `ceph.uuid`  | `str`  | `null`    | `fd083b60-82ce-518b-a1a7-fc7bda472338` | UUID of the secret that is to keep Ceph key in Libvirt. |
| `node_group` | `str`  | `node`    |                                        | Custom name of the Node group in the inventory.         |

Dependencies
------------

Example Playbook
----------------

    - hosts: frontend
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.ceph.frontend

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
