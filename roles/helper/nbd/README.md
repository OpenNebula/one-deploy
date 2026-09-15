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
        # NOTE: nbd-client does not load the nbd module itself and only kernels >= 6.12
        #       autoload it (netlink family alias), e.g. Debian 12 needs it loaded explicitly.
        kernel_ok_to_reboot: true
        kernel_modules:
          - load: nbd
        nbd:
          - name: export0
            host: 10.2.11.1
            device: nbd0
            options: port=10809
          - name: export1
            host: 10.2.11.1
            device: nbd1
            options: port=10809
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.kernel # (e.g. Debian 12)
        - role: opennebula.deploy.helper.nbd

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
