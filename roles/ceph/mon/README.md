Role: opennebula.deploy.ceph.mon
================================

A role that manages OpenNebula related settings on a Ceph mon.

Requirements
------------

N/A

Role Variables
--------------

| Name | Type | Default | Example | Description |
|------|------|---------|---------|-------------|
|      |      |         |         |             |

Dependencies
------------

Example Playbook
----------------

    - hosts: mons
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.ceph.mon

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
