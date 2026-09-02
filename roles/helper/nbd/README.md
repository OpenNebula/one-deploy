Role: opennebula.deploy.helper.nbd
==================================

A role that attaches NBD devices.

Requirements
------------

N/A

Role Variables
--------------

| Name            | Type   | Description          |
|-----------------|--------|----------------------|
| `nbd`           | `list` | List of NBD devices. |
| `nbd[].name`    | `str`  | NBD export name.     |
| `nbd[].host`    | `str`  | NBD server endpoint. |
| `nbd[].device`  | `str`  | NBD device name.     |
| `nbd[].options` | `str`  | NBD options.         |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: node
      vars:
        nbd:
          - name: export0
            host: 10.2.11.1
            device: nbd0
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.nbd

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
