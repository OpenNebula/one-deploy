Role: opennebula.deploy.helper.iscsi
====================================

A role that attached iSCSI LUNs.

Requirements
------------

N/A

Role Variables
--------------

| Name                | Type   | Description                      |
|---------------------|--------|----------------------------------|
| `iscsi`             | `list` | List of iscsi multipath devices. |
| `iscsi[].name`      | `str`  | Interface name.                  |
| `iscsi[].target`    | `str`  | Target IQN.                      |
| `iscsi[].initiator` | `str`  | Initiator IQN.                   |
| `iscsi[].portal`    | `str`  | Portal (host:port).              |

Dependencies
------------

N/A

Example Playbook
----------------

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

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
