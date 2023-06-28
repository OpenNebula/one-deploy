Role: opennebula.deploy.network.node
====================================

A role that manages OpenNebula virtual networks (to be run on Nodes).

Requirements
------------

N/A

Role Variables
--------------

| Name | Type   | Default | Example       | Description                               |
|------|--------|---------|---------------|-------------------------------------------|
| `vn` | `dict` | `{}`    | (check below) | OpenNebula Virtual Network configuration. |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: node
      vars:
        vn:
          vxlan:
            # Define a VNET of type vxlan and move IP4/6 settings from bond0 to br1.
            vm:
              managed: true
              template:
                VN_MAD: vxlan
                PHYDEV: bond0
                BRIDGE: br1
                VLAN_ID: 86
                FILTER_IP_SPOOFING: 'NO'
                FILTER_MAC_SPOOFING: 'YES'
                GUEST_MTU: 1450
                AR:
                  TYPE: IP4
                  IP: 192.168.150.200
                  SIZE: 48
                NETWORK_ADDRESS: 192.168.150.0
                NETWORK_MASK: 255.255.255.0
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.network.node

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
