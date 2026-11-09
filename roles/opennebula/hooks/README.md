Role: opennebula.deploy.opennebula.hooks
========================================

A role that manages OpenNebula hooks.

Requirements
------------

N/A

Role Variables
--------------

| Name                          | Type           | Default                       | Description                                                 |
|-------------------------------|----------------|-------------------------------|-------------------------------------------------------------|
| `opennebula_hooks_base_dir`   | `str`          | `/var/lib/one/remotes/hooks/` | Destination directory for hook scripts.                     |
| `opennebula_hooks_defaults`   | `list`         | (check role defaults)         | OpenNebula Hook configuration defaults.                     |
| `opennebula_hooks`            | `list`         | (check role defaults)         | OpenNebula Hook configuration.                              |
| `opennebula_hooks[].template` | `dict`         | `{}`                          | OpenNebula Hook template contents.                          |
| `opennebula_hooks[].source`   | `str` / `null` | `null`                        | Source file / directory to push via `rsync --relative`.     |
| `opennebula_hooks[].managed`  | `bool`         | `true` (effectively)          | When evaluates to `false` then one-deploy ignores the hook. |

Custom scripts are installed in `/var/lib/one/remotes/hooks/` with owner and group `oneadmin` (UID/GID `9869`) and executable mode `0750`.

Dependencies
------------

- ansible.posix

Example Playbook
----------------

    - hosts: frontend
      vars:
        # Ignores all default hooks.
        opennebula_hooks_defaults: []
      roles:
        - role: opennebula.deploy.opennebula.hooks

    - hosts: frontend
      vars:
        opennebula_hooks:
          # Ignores `autostart_host` hook (deployed by default).
          - template: { NAME: autostart_host }
            managed: false

          # Ignores `autostart_vm` hook (deployed by default).
          - template: { NAME: autostart_vm }
            managed: false
      roles:
        - role: opennebula.deploy.opennebula.hooks

    - hosts: frontend
      vars:
        opennebula_hooks:
          # Deploys script from "{{ inventory_dir }}/hooks/custom/notify1.sh".
          # Deploys script to "/var/lib/one/remotes/hooks/custom/notify1.sh".
          # Creates "notify1" hook.
          - template:
              NAME: notify1
              TYPE: state
              RESOURCE: HOST
              STATE: MONITORED
              COMMAND: custom/notify1.sh
              # NOTE: It deletes `ASD` attribute from the existing hook template (during update).
              ASD: null
            source: custom/notify1.sh

          # Deploys script from "/absolute/path/on/controller/custom/notify2.sh".
          # Deploys script to "/var/lib/one/remotes/hooks/custom/notify2.sh".
          # Creates "notify2" hook.
          - template:
              NAME: notify2
              TYPE: state
              RESOURCE: HOST
              STATE: MONITORED
              COMMAND: custom/notify2.sh
            # NOTE: Placement of the /./ marker is significant while using `rsync --relative`.
            #       Please refer to rsync's documentation.
            source: /absolute/path/on/controller/./custom/notify2.sh

          # Reuses "/var/lib/one/remotes/hooks/custom/notify2.sh".
          # Creates "notify3" hook.
          - template:
              NAME: notify3
              TYPE: state
              RESOURCE: HOST
              STATE: MONITORED
              COMMAND: custom/notify2.sh
      roles:
        - role: opennebula.deploy.opennebula.hooks

    - hosts: frontend
      vars:
        opennebula_hooks:
          # Deploys all scripts from "{{ inventory_dir }}/hooks/custom/" (whole directory tree).
          # Deploys all script to "/var/lib/one/remotes/hooks/custom/".
          # Creates "notify1" hook.
          - template:
              NAME: notify1
              TYPE: state
              RESOURCE: HOST
              STATE: MONITORED
              COMMAND: custom/notify1.sh
            source: custom
      roles:
        - role: opennebula.deploy.opennebula.hooks

    - hosts: frontend
      vars:
        opennebula_hooks:
          # Deploys script from "/absolute/path/on/controller/custom/" (whole directory tree).
          # Deploys all script to "/var/lib/one/remotes/hooks/custom/".
          # Creates "notify1" hook.
          - template:
              NAME: notify1
              TYPE: state
              RESOURCE: HOST
              STATE: MONITORED
              COMMAND: custom/notify1.sh
            # NOTE: Placement of the /./ marker is significant while using `rsync --relative`.
            #       Please refer to rsync's documentation.
            source: /absolute/path/on/controller/./custom
      roles:
        - role: opennebula.deploy.opennebula.hooks

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
