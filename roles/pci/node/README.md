Role: opennebula.deploy.pci.node
================================

A role that handles PCI Passthrough / SR-IOV device configuration on the Node's side.

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

- `opennebula.deploy.helper.pci`

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
            set_driver: omit # NOTE: 'vfio-pci' is the default, 'omit' skips override altogether
            set_numvfs: max
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.pci.node

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
