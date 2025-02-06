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
| `pki.base`         | `str`  | `/etc/proxy`     |         | Base directory for PKI files                                 |
| `pki.dirs.key`     | `str`  | `key`            |         | Subdirectory for storing private keys                        |
| `pki.dirs.crt`     | `str`  | `crt`            |         | Subdirectory for storing certificates                        |
| `pki.dirs.csr`     | `str`  | `csr`            |         | Subdirectory for storing certificate signing requests        |
| `pki.ca.key`       | `str`  | `ca.key`         |         | Filename of the CA private key                               |
| `pki.ca.crt`       | `str`  | `ca.crt`         |         | Filename of the CA certificate                               |
| `pki.ca.csr`       | `str`  | `ca.csr`         |         | Filename of the CA certificate signing request               |
| `pki.client.key`   | `str`  | `client.key`     |         | Filename of the client private key                           |
| `pki.client.crt`   | `str`  | `client.crt`     |         | Filename of the client certificate                           |
| `pki.client.csr`   | `str`  | `client.csr`     |         | Filename of the client certificate signing request           |
| `pki.certchain`    | `str`  | `certchain.crt`  |         | Filename of the full certificate chain                       |

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
