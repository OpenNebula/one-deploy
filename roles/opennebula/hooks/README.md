Role: opennebula.deploy.opennebula.hooks
=======================================

Registers the `autostart-host` and `autostart-vm` hooks by default and can add
custom hooks. OpenNebula already supplies the autostart command scripts on
frontends; this role does not copy them.

Role Variables
--------------

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `opennebula_custom_hooks` | list of dictionaries | `[]` | Extra hook templates, each with a unique `NAME`. These extend the two autostart hooks. |
| `opennebula_hook_scripts` | list of `{src, dest}` dictionaries | `[]` | Custom command files to copy from the Ansible controller to every frontend. `dest` is relative to `/var/lib/one/remotes/hooks/`. |

Custom scripts are installed with owner and group `oneadmin` (UID/GID 9869)
and executable mode `0750`. The role creates any subdirectories in `dest`.
Only local frontend hook commands are supported; `REMOTE=YES` scripts must be
distributed to nodes separately.

Example Playbook
----------------

    - hosts: frontend
      collections:
        - opennebula.deploy
      vars:
        opennebula_hook_scripts:
          - src: /path/on/controller/notify.sh
            dest: custom/notify.sh
        opennebula_custom_hooks:
          - NAME: notify-host
            TYPE: state
            COMMAND: custom/notify.sh
            RESOURCE: HOST
            STATE: MONITORED
      roles:
        - role: opennebula/hooks

The role registers hooks from the first frontend in the play; it does not
require an elected leader. It creates a hook only when its name is absent and
does not update or delete existing hooks.
The two autostart hooks are always included, so extra hooks must have distinct
names.

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
