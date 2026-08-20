Role: opennebula.deploy.datastore.generic
=========================================

A role that manages OpenNebula datastores (`generic` mode).

Requirements
------------

N/A

Role Variables
--------------

| Name          | Type   | Default   | Example                                | Description                                                                    |
|---------------|--------|-----------|----------------------------------------|--------------------------------------------------------------------------------|
| `ds.mode`     | `str`  | `ssh`     |                                        | OpenNebula Datastore configuration mode: `ssh`, `shared`, `ceph` or `generic`. |
| `ds.config`   | `dict` | `{}`      | (check below)                          | OpenNebula Datastore configuration for a specifc mode.                         |
| `ds_defaults` | `dict` |           |                                        | Defaults that are merged with user configs.                                    |
| `ceph.pool`   | `str`  | `one`     |                                        | Name of the Ceph pool dedicated to OpenNebula.                                 |
| `ceph.user`   | `str`  | `libvirt` |                                        | Ceph user that is to have access to the OpenNebula's pool.                     |
| `ceph.host`   | `str`  |           | `10.11.12.13 10.11.12.14:1234`         | Space-separated list of IP:PORT pairs of Ceph mons.                            |
| `ceph.uuid`   | `str`  | `null`    | `fd083b60-82ce-518b-a1a7-fc7bda472338` | UUID of the secret that is to keep Ceph key in Libvirt.                        |
| `node_group`  | `str`  | `node`    |                                        | Custom name of the Node group in the inventory.                                |
| `leader`      | `str`  | undefined | `10.11.12.13`                          | When OpenNebula is in HA mode it points to the Leader.                         |

Dependencies
------------

- opennebula.deploy.opennebula.leader

Example Playbook
----------------

Please also check examples from `opennebula.datastores.frontend` and `opennebula.datastore.node` roles.

    # Configure datastores 0, 1 to use 'lvm' driver.

    - hosts: node
      vars:
        iscsi:
          - name: target0
            target: iqn.1970-01.com.example:target0
            initiator: iqn.1970-01.com.example:client0
            portal: 10.2.11.1:3260
          - name: target1
            target: iqn.1970-01.com.example:target1
            initiator: iqn.1970-01.com.example:client1
            portal: 10.2.11.1:3261
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.iscsi

    - hosts: frontend:node
      vars:
        ds:
          mode: generic
          config:
            SYSTEM_DS:
              system:
                template:
                  TYPE: SYSTEM_DS
                  TM_MAD: lvm
                  DISK_TYPE: BLOCK
                  BRIDGE_LIST: "{{ groups.node | map('extract', hostvars, ['ansible_host']) | join(' ') }}"
            IMAGE_DS:
              default:
                device: /dev/mapper/mpatha
                template:
                  TYPE: IMAGE_DS
                  DS_MAD: lvm
                  TM_MAD: lvm
                  DISK_TYPE: BLOCK
                  BRIDGE_LIST: "{{ groups.node | map('extract', hostvars, ['ansible_host']) | join(' ') }}"
                  LVM_THIN_ENABLE: 'YES'
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.datastore

    # Configure datastores 0, 1 to use 'fs_lvm' driver.

    - hosts: node
      vars:
        iscsi:
          - name: target0
            target: iqn.1970-01.com.example:target0
            initiator: iqn.1970-01.com.example:client0
            portal: 10.2.11.1:3260
          - name: target1
            target: iqn.1970-01.com.example:target1
            initiator: iqn.1970-01.com.example:client1
            portal: 10.2.11.1:3261
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.iscsi

    - hosts: frontend:node
      vars:
        fstab:
          - src: 10.2.11.1:/nfs/default
            path: /nfs/default
            fstype: nfs
            opts: rw,relatime,comment=one-deploy
        ds:
          mode: generic
          config:
            SYSTEM_DS:
              system:
                device: /dev/mapper/mpatha
                template:
                  TYPE: SYSTEM_DS
                  TM_MAD: fs_lvm
                  DISK_TYPE: BLOCK
                  BRIDGE_LIST: "{{ groups.node | map('extract', hostvars, ['ansible_host']) | join(' ') }}"
            IMAGE_DS:
              default:
                symlink:
                  src: /nfs/default/
                template:
                  TYPE: IMAGE_DS
                  DS_MAD: fs
                  TM_MAD: fs_lvm
                  DISK_TYPE: BLOCK
                  LVM_THIN_ENABLE: 'YES'
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.fstab
        - role: opennebula.deploy.datastore

    # Configure datastores 0, 1 to use 'fs_lvm_ssh' driver.

    - hosts: node
      vars:
        iscsi:
          - name: target0
            target: iqn.1970-01.com.example:target0
            initiator: iqn.1970-01.com.example:client0
            portal: 10.2.11.1:3260
          - name: target1
            target: iqn.1970-01.com.example:target1
            initiator: iqn.1970-01.com.example:client1
            portal: 10.2.11.1:3261
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.iscsi

    - hosts: frontend:node
      vars:
        ds:
          mode: generic
          config:
            SYSTEM_DS:
              system:
                device: /dev/mapper/mpatha
                template:
                  TYPE: SYSTEM_DS
                  TM_MAD: fs_lvm_ssh
                  DISK_TYPE: BLOCK
                  BRIDGE_LIST: "{{ groups.node | map('extract', hostvars, ['ansible_host']) | join(' ') }}"
            IMAGE_DS:
              default:
                template:
                  TYPE: IMAGE_DS
                  DS_MAD: fs
                  TM_MAD: fs_lvm_ssh
                  DISK_TYPE: BLOCK
                  LVM_THIN_ENABLE: 'YES'
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.datastore

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
