Role: opennebula.deploy.helper.pci
==================================

A role that handles PCI Passthrough / SR-IOV device configuration.

Requirements
------------

N/A

Role Variables
--------------

| Name                        | Type   | Default   | Description                                                                         |
|-----------------------------|--------|-----------|-------------------------------------------------------------------------------------|
| `pci_devices`               | `list` | `[]`      | PCI devices configuration.                                                          |
| `pci_devices[].excluded`    | `bool` | `false`   | Do not process matching PCI devices.                                                |
| `pci_devices[].unguarded`   | `bool` | `false`   | Do not protect matching PCI devices (this may cause primary NIC connectivity loss). |
| `pci_devices[].unlisted`    | `bool` | `true`    | Do not pass matching PCI devices to OpenNebula.                                     |
| `pci_devices[].virtual`     | `bool` | `false`   | Do not fail query on missing virtual devices (SR-IOV).                              |
| `pci_devices[].address`     | `str`  | undefined | Glob PCI devices by PCI or MAC address.                                             |
| `pci_devices[].vendor`      | `str`  | `*`       | Glob PCI devices by PCI Vendor (if address is undefined).                           |
| `pci_devices[].device`      | `str`  | `*`       | Glob PCI devices by PCI Device (if address is undefined).                           |
| `pci_devices[].class`       | `str`  | `*`       | Glob PCI devices by PCI Class (if address is undefined).                            |
| `pci_devices[].set_counter` | `str`  | undefined | Reset the "set_counter" internal counter that can be used with set_name ("{3}").    |
| `pci_devices[].set_driver`  | `str`  | `omit`    | Use driverctl to override driver (unless "omit").                                   |
| `pci_devices[].set_name`    | `str`  | `omit`    | Rename device in udev (unless "omit").                                              |
| `pci_devices[].set_numvfs`  | `str`  | `0`       | Enable Virtual Functions for SR-IOV capable devices (integer >= 0 or "max").        |

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
            # NOTE: 1[0] -> PCI Domain (SR-IOV PF)
            #       1[1] -> PCI Bus (SR-IOV PF)
            #       1[2] -> PCI Device (SR-IOV PF)
            #       1[3] -> PCI Function (SR-IOV PF)
            # NOTE: 2    -> "virtfn" index (SR-IOV VF)
            # NOTE: 3    -> index derived from set_counter
            set_name: "pf{1[1]}{1[2]}vf{2}"

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

          # Enable 2 VFs and rename them to asd3v0, asd3v1 + Make sure OpenNebula doesn't use them (unlisted <- true).
          - address: "0000:03:00.*"
            set_name: "asd3vf{2}"
          - address: "0000:03:00.0"
            set_numvfs: 2

          # Enable 2 VFs and rename them to asd4v0, asd4v1 + Make sure OpenNebula does use them (unlisted <- false).
          - address: "0000:04:00.*"
            unlisted: false
            set_driver: vfio-pci # usual requirement for OpenNebula VMs
            set_name: "asd4vf{2}"
          - address: "0000:04:00.0"
            set_numvfs: 2
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.pci

    - hosts: node
      vars:
        pci_devices:
          # Process primary NIC by disabling its protection (NOTE: in general, this may cause connectivity loss!).
          - address: "0000:02:00.0"
            unguarded: true
            set_name: asd0
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.pci

    - hosts: node
      vars:
        pci_devices:
          # Enable all available VFs of 2 distinct PFs (virtio-net-pci) + rename using single counter.
          - address: '0000:30:00.*'
            set_counter: 0
            set_name: 'vf{3}'
          - address: '0000:40:00.*'
            set_name: 'vf{3}'
          - address: '0000:30:00.0'
            set_numvfs: max
          - address: '0000:40:00.0'
            set_numvfs: max
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.pci

    - hosts: node
      vars:
        pci_devices:
          # Enable all available VFs for all existing Mellanox PFs + rename PFs.
          - vendor: "15b3"
            device: "1015"
            class: "0200"
            set_numvfs: max
            set_name: "pf{0[1]}{0[2]}{0[3]}"

          # Rename all existing Mellanox VFs.
          - vendor: "15b3"
            device: "1016"
            class: "0200"
            virtual: true
            set_name: "pf{1[1]}{1[2]}{1[3]}vf{2}"
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

          # Rename all existing Mellanox VFs using custom counter (starting from 1), then pass them to OpenNebula.
          - vendor: "15b3"
            device: "1016"
            class: "0200"
            virtual: true
            unlisted: false
            set_counter: 1
            set_name: "vf{3}"
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.pci

    - hosts: node
      vars:
        pci_devices:
          # Rename and unlist all NICs matching MAC address wildcard.
          - address: "52:54:00:12:3*:*"
            set_name: "unlist{0[1]}{0{2}}{0[3]}"
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
