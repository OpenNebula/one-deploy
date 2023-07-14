Role: opennebula.deploy.gate.server
===================================

A role that manages the OneGate service.

Requirements
------------

N/A

Role Variables
--------------

| Name                 | Type   | Default     | Example       | Description                                             |
|----------------------|--------|-------------|---------------|---------------------------------------------------------|
| `gate_bind_addr`     | `str`  | `0.0.0.0`   |               | Bind/Listen address of the OneGate service.             |
| `gate_endpoint`      | `str`  | conditional | (check below) | An URL used to reach the OneGate endpoint (HTTP).       |
| `features.gateproxy` | `bool` | `false`     |               | Indicates if OneGate Proxy service is enabled/disabled. |
| `one_vip`            | `str`  | undefined   | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader.  |
| `leader`             | `str`  | undefined   | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader.  |

Dependencies
------------

- opennebula.deploy.opennebula.leader

Example Playbook
----------------

    - hosts: frontend
      vars:
        gate_endpoint: "http://10.11.12.13:5030"
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.repository
        - role: opennebula.deploy.gate.server

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
