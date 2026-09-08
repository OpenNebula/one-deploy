Role: opennebula.deploy.helper.fw
=================================

A role that opens TCP/UDP ports.

Requirements
------------

N/A

Role Variables
--------------

| Name                      | Type   | Default           | Description                          |
|---------------------------|--------|-------------------|--------------------------------------|
| `fw_ports`                | `list` | `null` (disabled) | FW configuration to apply.           |
| `fw_ports[].name`         | `str`  | undefined         | Unique name of the rule (required).  |
| `fw_ports[].ports`        | `list` | undefined         | List of ports to open.               |
| `fw_ports[].groups.local` | `list` | undefined         | List of groups to open FW ports on.  |
| `fw_ports[].groups.peers` | `list` | undefined         | List of groups to open FW ports for. |

Dependencies
------------

N/A

Example Playbook
----------------

    # Enable helper/fw, use default rules only.
    - hosts: frontend:node
      vars:
        fw_ports: []
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.fw

    # Enable helper/fw, skip OneXmlRpc rule (please check role defaults).
    - hosts: frontend:node
      vars:
        fw_ports:
          - name: OneXmlRpc
            ports: [2633/tcp]
            groups:
              local: [frontend]
              peers: null # `null` skips the rule
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.fw

    # Enable helper/fw, open custom UDP port on FEs, but allow datagrams only from HVs.
    - hosts: frontend:node
      vars:
        fw_ports:
          - name: CustomPort1
            ports: [1234/udp]
            groups:
              local: [frontend]
              peers: [node]
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.fw

    # Enable helper/fw, open custom TCP port range everywhere for everybody.
    - hosts: frontend:node
      vars:
        fw_ports:
          - name: CustomRange1
            ports: [1234-4321/tcp] # 1234:4321/tcp is also allowed
            groups:
              local: [frontend, node]
              peers: [] # `[]` means "any" or "0.0.0.0"
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.fw

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
