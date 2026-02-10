Role: opennebula.deploy.helper.mkfs
===================================

A role that (re-)creates filesystems on specified block devices.

Requirements
------------

N/A

Role Variables
--------------

| Name                | Type   | Default   | Example       | Description                         |
|---------------------|--------|-----------|---------------|-------------------------------------|
| `mkfs_ok_to_wipefs` | `bool` | `false`   | (check below) | Give consent to run `wipefs`.       |
| `mkfs`              | `list` | undefined | (check below) | List of block devices with options. |

Dependencies
------------

- `community.general`

Example Playbook
----------------

    - hosts: node
      vars:
        mkfs_ok_to_wipefs: true
        mkfs:
          - fstype: ext4
            dev: /dev/vdb
            force: true
          - fstype: xfs
            dev: /dev/vdc
            resizefs: true
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.mkfs

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
