Role: opennebula.deploy.bastion
===============================

A role that renders local SSH configs (in the inventory dir), then those can be used to access cluster nodes via a SSH jump host (aka bastion).

Requirements
------------

A `ssh-agent` instance running on the Ansible controller's side (possibly).

Role Variables
--------------

| Name             | Type  | Default    | Example       | Description                                                         |
|------------------|-------|------------|---------------|---------------------------------------------------------------------|
| `env_name`       | `str` | undefined  | `nebula3`     | Used to distinguish multiple SSH configs/clusters in the inventory. |
| `bastion_group`  | `str` | `bastion`  |               | Custom name of the Bastion group in the inventory.                  |
| `frontend_group` | `str` | `frontend` |               | Custom name of the Frontend group in the inventory.                 |
| `node_group`     | `str` | `node`     |               | Custom name of the Node group in the inventory.                     |
| `one_vip`        | `str` | undefined  | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader.              |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: bastion
      vars:
        # NOTE: the env_name should normally be defined in your inventory!
        env_name: nebula3
      roles:
        - role: opennebula.deploy.bastion
          delegate_to: localhost
          become: false

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
