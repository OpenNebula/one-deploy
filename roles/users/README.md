Role: opennebula.deploy.users
========================================

A role that manages OpenNebula users and groups (to be run on Frontends).

Currently:

- A user/group already existing won't be updated.
- Only `core` and `ldap` user drivers are supported.
- If any of the groups that the user must belong to does not exist, the user won't be created and the playbook will fail.

Requirements
------------

N/A

Role Variables
--------------

| Name                | Type   | Default   | Example       | Description                                            |
|---------------------|--------|-----------|---------------|--------------------------------------------------------|
| `usergroups.groups` | `dict` | `{}`      | (check below) | OpenNebula group list.                                 |
| `usergroups.users`  | `dict` | `{}`      | (check below) | OpenNebula user list.                                  |

Dependencies
------------

- opennebula.deploy.opennebula.leader

Example Playbook
----------------

    - hosts: frontend
      vars:
        usergroups:
          groups:
            g1: {}
            g2:
              admin_user: admg2
              admin_password: passwd_admg2
              resources: VM+NET+IMAGE+TEMPLATE+HOST+CLUSTER
          users:
            u1:
              password: testpassword
              groups: g1,g2
            u2:
              driver: ldap
     roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.network.frontend

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
