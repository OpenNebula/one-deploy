Role: opennebula.deploy.helper.vmdns
====================================

A role that automatically updates /etc/hosts on the RAFT leader.

Requirements
------------

N/A

Role Variables
--------------

| Name           | Type  | Default | Description                                                        |
|----------------|-------|---------|--------------------------------------------------------------------|
| `vmdns_server` | `str` | `null`  | DNS service to configure (currently only `resolved` is supported). |

Dependencies
------------

- ansible.posix

Example Playbook
----------------

    - hosts: frontend
      vars:
        leader_hook: raft/failover.sh
        follower_hook: raft/failover.sh
        vmdns_server: resolved
        prod_env: false
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.vmdns

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
