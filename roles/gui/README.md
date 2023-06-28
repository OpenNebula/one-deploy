Role: opennebula.deploy.gui
===========================

A role that manages Sunstone and FireEdge services.

Requirements
------------

N/A

Role Variables
--------------

| Name                       | Type  | Default     | Example             | Description                                                                |
|----------------------------|-------|-------------|---------------------|----------------------------------------------------------------------------|
| `public_fireedge_endpoint` | `str` | conditional | (check below)       | Base URL (domain or IP-based) over which end-users can access the service. |
| `one_token`                | `str` | undefined   | `asd123as:123asd12` | OpenNebula Enterprise Edition subscription token.                          |
| `one_fqdn`                 | `str` | undefined   | `nebula.example.io` | Fully qualified domain name of the OpenNebula instance.                    |
| `one_vip`                  | `str` | undefined   | `10.11.12.13`       | When OpenNebula is in HA mode it points to the Leader.                     |
| `leader`                   | `str` | undefined   | `10.11.12.13`       | When OpenNebula is in HA mode it points to the Leader.                     |

Dependencies
------------

- opennebula.deploy.opennebula.leader

Example Playbook
----------------

    - hosts: frontend
      vars:
        public_fireedge_endpoint: "https://nebula.example.io"
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.repository
        - role: opennebula.deploy.gui

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
