Role: opennebula.deploy.helper.pci
==================================

A role that handles PCI Passthrough / SR-IOV device configuration.

Requirements
------------

N/A

Role Variables
--------------

| Name          | Type   | Default | Example       | Description                     |
|---------------|--------|---------|---------------|---------------------------------|
| `pci_devices` | `list` | `[]`    | (check below) | PCI devices configuration.      |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: node
      vars:
        pci_devices:
          - address: "0000:02:00.0"
            excluded: true
          - address: "0000:03:00.*"
            unlisted: true
            set_name: "asd{0[3]}"
          - vendor: "1af4"
            device: "*"
            class: "0200"
            set_driver: omit # NOTE: 'vfio-pci' is the default, 'omit' skips override altogether
            set_numvfs: max
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.pci

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
