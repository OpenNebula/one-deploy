Role: opennebula.deploy.network.frontend
========================================

A role that manages OpenNebula virtual networks (to be run on Frontends).

Requirements
------------

N/A

Role Variables
--------------

| Name     | Type   | Default   | Example       | Description                                            |
|----------|--------|-----------|---------------|--------------------------------------------------------|
| `vn`     | `dict` | `{}`      | (check below) | OpenNebula Virtual Network configuration.              |
| `leader` | `str`  | undefined | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader. |

Dependencies
------------

- opennebula.deploy.opennebula.leader

Example Playbook
----------------

    - hosts: frontend
      vars:
        vn:
          bridge:
            # Define a VNET of type bridge using predefined bridge br0.
            service:
              managed: true
              template:
                VN_MAD: bridge
                BRIDGE: br0
                AR:
                  TYPE: IP4
                  IP: 10.11.12.200
                  SIZE: 48
                NETWORK_ADDRESS: 10.11.12.0
                NETWORK_MASK: 255.255.255.0
                GATEWAY: 10.11.12.1
                DNS: 1.1.1.1
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
        - role: opennebula.deploy.network.frontend

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
