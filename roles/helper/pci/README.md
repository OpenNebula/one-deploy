Role: opennebula.deploy.helper.pci
==================================

A role that handles PCI Passthrough / SR-IOV device configuration.

Requirements
------------

N/A

Role Variables
--------------

| Name                        | Type  | Default   | Example       | Description                                                                  |
|-----------------------------|-------|-----------|---------------|------------------------------------------------------------------------------|
| `pci_devices`               | `list`| `[]`      | (check below) | PCI devices configuration.                                                   |
| `pci_devices[*].excluded`   | `bool`| `false`   | (check below) | Do not process matching PCI devices.                                         |
| `pci_devices[*].unlisted`   | `bool`| `false`   | (check below) | Do not pass matching PCI devices to OpenNebula.                              |
| `pci_devices[*].address`    | `str` | undefined | (check below) | Glob PCI devices by PCI or MAC address.                                      |
| `pci_devices[*].vendor`     | `str` | `*`       | (check below) | Glob PCI devices by PCI Vendor (if address is undefined).                    |
| `pci_devices[*].device`     | `str` | `*`       | (check below) | Glob PCI devices by PCI Device (if address is undefined).                    |
| `pci_devices[*].class`      | `str` | `*`       | (check below) | Glob PCI devices by PCI Class (if address is undefined).                     |
| `pci_devices[*].set_driver` | `str` | `omit`    | (check below) | Use driverctl to override driver (unless "omit").                            |
| `pci_devices[*].set_name`   | `str` | `omit`    | (check below) | Rename device in udev (unless "omit").                                       |
| `pci_devices[*].set_numvfs` | `str` | `0`       | (check below) | Enable Virtual Functions for SR-IOV capable devices (integer >= 0 or "max"). |

Dependencies
------------

N/A

Example Playbook
----------------

    # NOTE: Dicts defined in pci_devices are processed top-to-bottom without merging.

    - hosts: node
      vars:
        pci_devices:
          # Rename virtio-net-pci devices unless configured otherwise later (below).
          - vendor: "1af4"
            device: "*"
            class: "0200"
            # NOTE: 0[0] -> PCI Domain
            #       0[1] -> PCI Bus
            #       0[2] -> PCI Device
            #       0[3] -> PCI Function
            set_name: "asd{0[1]}v{0[3]}"

          # Do not rename "0000:04:00.0" + If it's SR-IOV capable, enable all available VFs.
          - address: "0000:04:00.0"
            set_numvfs: max
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.pci

    - hosts: node
      vars:
        pci_devices:
          # Exclude primary NIC from processing.
          - address: "0000:02:00.0"
            excluded: true

          # Enable 2 VFs and rename them to asd3v1, asd3v2 + Make sure OpenNebula doesn't use them (unlisted <- true).
          - address: "0000:03:00.*"
            set_name: "asd3v{0[3]}"
            unlisted: true
          - address: "0000:03:00.0"
            set_numvfs: 2

          # Enable 2 VFs and rename them to asd4v1, asd4v2 + Make sure OpenNebula does use them (unlisted <- false).
          - address: "0000:04:00.*"
            set_driver: vfio-pci # usual requirement for OpenNebula VMs
            set_name: "asd4v{0[3]}"
          - address: "0000:04:00.0"
            set_numvfs: 2
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.pci

    - hosts: node
      vars:
        pci_devices:
          # Enable all available VFs for all existing Mellanox PFs.
          - vendor: "15b3"
            device: "1015"
            class: "0200"
            set_numvfs: max

          # Rename all existing Mellanox VFs.
          - vendor: "15b3"
            device: "1016"
            class: "0200"
            set_name: "vf{0[2]}{0[3]}"
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.pci

    - hosts: node
      vars:
        pci_devices:
          # Rename and unlist all NICs matching MAC address wildcard.
          - address: "52:54:00:12:3*:*"
            set_name: "unlist{0[1]}v{0[3]}"
            unlisted: true
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.pci

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
