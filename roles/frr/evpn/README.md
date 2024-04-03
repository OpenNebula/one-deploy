Role: opennebula.deploy.frr.evpn
================================

A role that configures BGP/EVPN Control Plane (for VXLAN VNETs).

Requirements
------------

N/A

Role Variables
--------------

| Name              | Type   | Default  | Example              | Description                                                      |
|-------------------|--------|----------|----------------------|------------------------------------------------------------------|
| `evpn_as`         | `str`  | `65000`  |                      | BGP Autonomous System ID.                                        |
| `evpn_if`         | `str`  |          | `eth0`               | Network interface used to establish BGP Control Plane.           |
| `evpn_cluster_id` | `str`  |          | `1.2.3.4`            | A cluster is a collection of Route Reflectors and their clients. |
| `evpn_pfxlen`     | `str`  |          | `16`                 | CIDR prefix length of the peer group's subnet.                   |
| `evpn_rr_servers` | `list` |          | `[1.2.3.4, 2.3.4.5]` | List of addresses of Route Reflectors.                           |
| `router_group`    | `str`  | `router` |                      | Custom name of the Router group in the inventory.                |
| `node_group`      | `str`  | `node`   |                      | Custom name of the Node group in the inventory.                  |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: router:node
      vars:
        features: { evpn: true }
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.frr.evpn

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
