Role: opennebula.deploy.database
================================

A role that performs initial configuration of the OpenNebula database.

Requirements
------------

N/A

Role Variables
--------------

| Name          | Type  | Default      | Example | Description                                           |
|---------------|-------|--------------|---------|-------------------------------------------------------|
| `db_backend`  | `str` | `MariaDB`    |         | Can be `MariaDB` or `PostgreSQL`.                     |
| `db_name`     | `str` | `opennebula` |         | Name of the database/schema used by OpenNebula.       |
| `db_owner`    | `str` | `oneadmin`   |         | User used by OpenNebula to access the database.       |
| `db_password` | `str` | `opennebula` |         | Password used by OpenNebula to authenticate the user. |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: frontend
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.database

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
