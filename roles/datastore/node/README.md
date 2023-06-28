Role: opennebula.deploy.datastore.node
======================================

A role that manages OpenNebula datastores (to be run on Nodes).

Requirements
------------

N/A

Role Variables
--------------

| Name        | Type   | Default   | Example       | Description                                                            |
|-------------|--------|-----------|---------------|------------------------------------------------------------------------|
| `ds.mode`   | `str`  | `ssh`     |               | OpenNebula Datastore configuration mode: `ssh`, `shared` or `generic`. |
| `ds.config` | `dict` | `{}`      | (check below) | OpenNebula Datastore configuration for a specifc mode.                 |
| `leader`    | `str`  | undefined | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader.                 |

Dependencies
------------

- opennebula.deploy.opennebula.leader
- opennebula.deploy.network.simple
- opennebula.deploy.network.generic

Example Playbook
----------------

    - hosts: node
      vars:
        # Configure OpenNebula to use "shared" image and system datastores.
        # Create symlinks accordingly.
        ds:
          mode: shared
          config:
            mounts:
              - type: system
                path: /opt/nfs/system/
              - type: image
                path: /opt/nfs/default/
              - type: file
                path: /opt/nfs/files/
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.datastore.node

    - hosts: node
      vars:
        # Configure OpenNebula to use "shared" image and system datastores.
        # Create new datastores and symlinks accordingly.
        ds:
          mode: generic
          config:
            SYSTEM_DS:
              system:
                enabled: false
              system1:
                id: 100
                managed: true
                enabled: true
                symlink:
                  groups: [node]
                  src: /opt/nfs1/100/
                template: &template
                  TYPE: SYSTEM_DS
                  TM_MAD: shared
                  BRIDGE_LIST: "{{ groups.node | map('extract', hostvars, ['ansible_host']) | join(' ') }}"
              system2:
                id: 101
                managed: true
                enabled: true
                symlink:
                  groups: [node]
                  src: /opt/nfs2/101/
                template: *template
              system3:
                id: 102
                managed: true
                enabled: true
                symlink:
                  groups: [node]
                  src: /opt/nfs3/102/
                template: *template
            IMAGE_DS:
              default:
                symlink: { src: /opt/nfs0/1/ }
                template:
                  TM_MAD: shared
            FILE_DS:
              files:
                symlink: { src: /opt/nfs0/2/ }
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.datastore.node

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
