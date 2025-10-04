Role: opennebula.deploy.pci\_passthrough.frontend
=================================================

A role that handles PCI Passthrough configuration on the FrontEnd side. Currently, the role:
- Enables monitoring of all PCI devices in FrontEnds.
- Maps PCI devices defined in the Inventory to Vendor:DeviceID format to avoid PCI bus changes after server reboots.
- Filters PCI devices per-host based on the PCI_FILTER host template attribute.

Requirements
------------

N/A

Role Variables
--------------

N/A

Dependencies
------------

- opennebula.deploy.opennebula.leader

Example Playbook
----------------

    - hosts: frontend
      roles:
        - role: opennebula.deploy.pci_passthrough.frontend

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
