Role: opennebula.deploy.helper.hosts
====================================

A role that populates `/etc/hosts` and sets the hostname.

Requirements
------------

N/A

Role Variables
--------------

| Name              | Type   | Default | Example | Description                                     |
|-------------------|--------|---------|---------|-------------------------------------------------|
| `ensure_hostname` | `bool` | `False` |         | Enforce hostname to match `inventory_hostname`. |
| `ensure_hosts`    | `bool` | `False` |         | Populate `/etc/hosts` with data from inventory. |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: all
      roles:
         - { role: opennebula.deploy.helper.hosts, ensure_hostname: true, ensure_hosts: true }

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
