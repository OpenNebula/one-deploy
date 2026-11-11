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
| `onehost.template`    | `dict` | `{}`      | (check below) | Host template attributes to add or update.             |

Dependencies
------------

- opennebula.deploy.opennebula.leader
- ansible.posix

Example Playbook
----------------

```yaml
- hosts: node
  roles:
    - role: opennebula.deploy.helper.facts
    - { role: opennebula.deploy.kvm, node_hv: qemu }
```

Set `onehost.template` in a node's inventory variables to manage host attributes:

```yaml
node:
  hosts:
    kvm01:
      ansible_host: 10.11.12.20
      onehost:
        template:
          RESERVED_MEM: 4096
          ISOLCPUS: "2,3"
          # NOTE: It removes existing 'ASD' attribute during the next update.
          ASD: null
```

The attributes are appended to the host template after the host is registered.
Existing attributes outside `onehost.template` are preserved. Use uppercase
attribute names, as OpenNebula returns them in uppercase.

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
