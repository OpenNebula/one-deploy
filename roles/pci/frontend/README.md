Role: opennebula.deploy.pci.frontend
====================================

A role that handles PCI Passthrough configuration on the Front-end's side.

Requirements
------------

N/A

Role Variables
--------------

| Name                             | Type   | Default | Example | Description                              |
|----------------------------------|--------|---------|---------|------------------------------------------|
| `pci_passthrough_enabled`        | `bool` | `false` |         | Enable/Disable PCI passthrough.          |
| `pci_passthrough_default_filter` | `bool` | `*:*`   |         | Default (global) PCI passthrough filter. |

Dependencies
------------

- opennebula.deploy.opennebula.leader

Example Playbook
----------------

    - hosts: frontend
      roles:
        - role: opennebula.deploy.pci.frontend

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
