Role: opennebula.deploy.lxc
===========================

A role that manages OpenNebula LXC Nodes/Hosts.

Requirements
------------

N/A

Role Variables
--------------

| Name      | Type   | Default   | Example       | Description                                            |
|-----------|--------|-----------|---------------|--------------------------------------------------------|
| `leader`  | `str`  | undefined | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader. |
| `node_hv` | `str`  | undefined | `lxc`         | Select `lxc` hypervisor.                               |

Dependencies
------------

- opennebula.deploy.opennebula.leader
- ansible.posix

Example Playbook
----------------

    - hosts: node
      roles:
        - role: opennebula.deploy.helper.facts
        - { role: opennebula.deploy.lxc, node_hv: lxc }

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
