Role: opennebula.deploy.ceph.repository
=======================================

A role that prepares Ceph repository.

Requirements
------------

N/A

Role Variables
--------------

| Name           | Type  | Default  | Example     | Description                                                                               |
|----------------|-------|----------|-------------|-------------------------------------------------------------------------------------------|
| `ceph.repo`    | `str` |          | `community` | Defines type of Ceph repository to use `distro` or `community`. Tasks ignored if not set. |
| `ceph.release` | `str` |          | `tentacle`  | Defines Ceph version to use.                                                              |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: mons:mgrs:osds
      vars:
        ceph:
          repo: distro
          release: squid
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.ceph.repository

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
