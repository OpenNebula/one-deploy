Role: opennebula.deploy.gate
============================

A role that manages the OneGate service.

Requirements
------------

N/A

Role Variables
--------------

| Name             | Type   | Default     | Example       | Description                                            |
|------------------|--------|-------------|---------------|--------------------------------------------------------|
| `gate_tproxy`    | `list` | `[]`        | (check below) | Transparent proxy configuration.                       |
| `gate_bind_addr` | `str`  | `0.0.0.0`   |               | Bind/Listen address of the OneGate service.            |
| `gate_endpoint`  | `str`  | conditional | (check below) | An URL used to reach the OneGate endpoint (HTTP).      |
| `one_vip`        | `str`  | undefined   | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader. |
| `leader`         | `str`  | undefined   | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader. |

Dependencies
------------

- opennebula.deploy.opennebula.leader

Example Playbook
----------------

    - hosts: frontend
      vars:
        gate_endpoint: "http://169.254.16.9:5030"
        gate_tproxy:
          # OneGate service.
          - :service_port: 5030
            :remote_addr: "{{ one_vip }}"
            :remote_port: 5030
          # Custom service.
          - :service_port: 1234
            :remote_addr: 10.11.12.13
            :remote_port: 4321
            :networks: [vnet_name_or_id]
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.gate

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
