Role: opennebula.deploy.helper.certs
====================================

A simple role that generates a certificate authority (CA) and then a client certificate signed by that CA.

Requirements
------------

N/A

Role Variables
--------------

| Name               | Type   | Default          | Example | Description                                                  |
|--------------------|--------|------------------|---------|--------------------------------------------------------------|
| `certs_path`       | `str`  | `/etc/proxy`     |         | Directory containing the certificates, keys, and CSR         |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: frontend
      roles:
         - role: opennebula.deploy.helper.certs

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
