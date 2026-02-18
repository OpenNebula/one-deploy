Role: opennebula.deploy.pci.node
================================

A role that handles PCI Passthrough configuration on the Node's side.

Requirements
------------

N/A

Role Variables
--------------

| Name                      | Type   | Default | Example       | Description                     |
|---------------------------|--------|---------|---------------|---------------------------------|
| `pci_passthrough_enabled` | `bool` | `false` |               | Enable/Disable PCI passthrough. |
| `pci_devices`             | `list` | `[]`    | (check below) | PCI devices configuration.      |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: node
      vars:
        pci_passthrough_enabled: true
        pci_devices:
          - address: "0000:02:00.0"
            excluded: true
          - vendor: "1af4"
            device: "*"
            class: "0200"
            set_driver: virtio-pci
            set_numvfs: max
      roles:
        - role: opennebula.deploy.pci.node

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
