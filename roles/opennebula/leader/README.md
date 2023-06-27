Role: opennebula.deploy.opennebula.leader
=========================================

A role that detects the Leader.

Requirements
------------

N/A

Role Variables
--------------

| Name              | Type   | Default    | Example       | Description                                               |
|-------------------|--------|------------|---------------|-----------------------------------------------------------|
| `frontend_group`  | `str`  | `frontend` |               | Custom name of the Frontend group in the inventory.       |
| `one_vip`         | `str`  | undefined  | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader.    |
| `ping_port`       | `int`  | `22`       |               | TCP port to check while detecting the Leader.             |
| `force_ha`        | `bool` | `false`    |               | Deploy OpenNebula in HA mode even with a single Frontend. |


Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: frontend:node
      tasks:
        - ansible.builtin.include_role:
            name: opennebula.deploy.opennebula.leader
          when: leader is undefined

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
