Role: opennebula.deploy.pci\_passthrough.frontend
=================================================

A role that handles PCI Passthrough configuration on the nodes side. Currently, the role:
- Creates an udev rule to make sure vfio devices are in the kvm group
- Checks for the existence of the PCI devices defined in the Inventory, per-host
- Uses driverctl to bind the device to the vfio-pci driver
- Retrieves Vendor and DeviceID for the device

Requirements
------------

N/A

Role Variables
--------------

N/A

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: node
      roles:
        - role: opennebula.deploy.pci_passthrough.node

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
