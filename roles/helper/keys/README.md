Role: opennebula.deploy.helper.keys
===================================

A role that generates and distributes SSH/RSA keypairs across OpenNebula inventory (password-less login).

Requirements
------------

N/A

Role Variables
--------------

| Name              | Type   | Default | Example          | Description                                        |
|-------------------|--------|---------|------------------|----------------------------------------------------|
| `rsa_key_size`    | `str`  | `3072`  |                  |                                                    |
| `ensure_keys_for` | `list` | `[]`    | `[ubuntu, root]` | A list of system users to manage SSH/RSA keys for. |
| `node_group`      | `str`  | `node`  |                  | Custom name of the Node group in the inventory.    |

Dependencies
------------

- `community.crypto`
- `ansible.posix`

Example Playbook
----------------

    - hosts: frontend:node
      roles:
         - { role: opennebula.deploy.helper.keys, ensure_keys_for: [root] }

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
