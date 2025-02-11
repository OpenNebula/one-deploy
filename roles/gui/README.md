Role: opennebula.deploy.gui
===========================

A role that manages Sunstone and FireEdge services.

Requirements
------------

N/A

Role Variables
--------------

| Name                        | Type   | Default                                   | Example             | Description                                                                    |
|-----------------------------|--------|-------------------------------------------|---------------------|--------------------------------------------------------------------------------|
| `private_fireedge_endpoint` | `str`  | `http://localhost:2616`                   |                     | FireEdge URL used internally in Sunstone / reverse proxies.                    |
| `one_token`                 | `str`  | undefined                                 | `asd123as:123asd12` | OpenNebula Enterprise Edition subscription token.                              |
| `one_fqdn`                  | `str`  | undefined                                 | `nebula.example.io` | Fully qualified domain name of the OpenNebula instance.                        |
| `one_vip`                   | `str`  | undefined                                 | `10.11.12.13`       | When OpenNebula is in HA mode it points to the Leader.                         |
| `ssl.web_server`            | `enum` | `apache`                                  | (check below)       | Enable reverse proxy with SSL termination with Apache2 or nginx over HTTPS/443.|
| `ssl.key`                   | `str`  | `/etc/ssl/private/opennebula-key.pem`     |                     | Private key path on the target Front-end (the file must be readable).          |
| `ssl.certchain`             | `str`  | `/etc/ssl/certs/opennebula-certchain.pem` |                     | Certificate chain path on the target Front-end (the file must be readable).    |
| `ssl.generate_cert`         | `bool` | `false`                                   | `true`              | Generate a CA and a certificate signed by that CA for the reverse proxy.       |

Dependencies
------------

- opennebula.deploy.opennebula.leader
- opennebula.deploy.helper.certs

Example Playbook
----------------

    - hosts: frontend
      vars:
        one_fqdn: "nebula.example.io"
        ssl:
          generate_cert: true
          web_server: nginx
          key: /etc/ssl/private/ssl-cert-snakeoil.key
          certchain: /etc/ssl/certs/ssl-cert-snakeoil.pem
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.gui

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
