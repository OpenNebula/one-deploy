Role: opennebula.deploy.helper.fstab
====================================

A role that populates `/etc/fstab` and mounts filesystems.

Requirements
------------

N/A

Role Variables
--------------

| Name             | Type    | Default                          | Example                   | Description                                           |
|------------------|---------|----------------------------------|---------------------------|-------------------------------------------------------|
| `fstab`          | `list`  | `[]`                             |                           | A list of mount definitions.                          |
| `fstab[].src`    | `str`   | undefined                        | `server:/srv/shared`      | Device to be mounted on path.                         |
| `fstab[].path`   | `str`   | undefined                        | `/var/lib/one/datastores` | Path to the mountpoint.                               |
| `fstab[].fstype` | `str`   | undefined                        | `nfs`                     | Filesystem type.                                      |
| `fstab[].opts`   | `str`   | `rw,relatime,comment=one-deploy` |                           | Mount options.                                        |
| `fstab[].owner`  | `str`   | `9869`                           |                           | Name/UID of the user that should own the mountpoint.  |
| `fstab[].group`  | `str`   | `9869`                           |                           | Name/GID of the group that should own the mountpoint. |
| `fstab[].mode`   | `str`   | `u=rwx,g=rx,o=`                  |                           | The permissions the resulting mountpoint should have. |

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
         - role: opennebula.deploy.helper.facts
         - role: opennebula.deploy.helper.fstab

    - hosts: frontend:node
      vars:
        # NOTE: The `/srv` directory is automatically included in AppArmor configs
        #       by the `kvm` role.
        fstab:
          - src: server:/srv/shared
            path: /srv/shared
            fstype: nfs
            opts: rw,relatime,comment=one-deploy
        ds:
          mode: shared
          config:
            mounts:
              - type: system
                path: /srv/shared/system
              - type: image
                path: /srv/shared/image
              - type: file
                path: /srv/shared/file
      roles:
         - role: opennebula.deploy.helper.facts
         - role: opennebula.deploy.helper.fstab
         - role: opennebula.deploy.datastore

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
