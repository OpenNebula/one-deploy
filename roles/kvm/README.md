Role: opennebula.deploy.kvm
===========================

A role that manages OpenNebula KVM Nodes/Hosts.

Requirements
------------

N/A

Role Variables
--------------

| Name                  | Type   | Default   | Example       | Description                                            |
|-----------------------|--------|-----------|---------------|--------------------------------------------------------|
| `disable_default_net` | `bool` | `true`    |               | Disable default Libvirt's network.                     |
| `libvirtd_args`       | `str`  | `''`      |               | Overwrite arguments in the `libvirtd` systemd service. |
| `leader`              | `str`  | undefined | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader. |
| `node_hv`             | `str`  | `kvm`     | `qemu`        | Select `kvm` or `qemu` (software-mode) hypervisor.     |

Dependencies
------------

- opennebula.deploy.opennebula.leader
- ansible.posix

Example Playbook
----------------

    - hosts: node
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.repository
        - { role: opennebula.deploy.kvm, node_hv: qemu }

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
