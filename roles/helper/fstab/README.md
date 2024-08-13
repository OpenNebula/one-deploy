Role: opennebula.deploy.helper.fstab
====================================

A role that populates `/etc/fstab` and mounts filesystems.

Requirements
------------

N/A

Role Variables
--------------

| Name    | Type   | Default | Example       | Description                  |
|---------|--------|---------|---------------|------------------------------|
| `fstab` | `list` | `[]`    | (check below) | A list of mount definitions. |

Dependencies
------------

- `ansible.posix`

Example Playbook
----------------

    - hosts: frontend:node
      vars:
        fstab:
          - src: server:/var/lib/one/datastores
            path: /var/lib/one/datastores
            fstype: nfs
            opts: rw,relatime,comment=one-deploy
      roles:
         - role: opennebula.deploy.helper.fstab

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
