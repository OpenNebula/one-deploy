Role: opennebula.deploy.gui
===========================

A role that manages Sunstone and FireEdge services.

Requirements
------------

N/A

Role Variables
--------------

| Name                        | Type   | Default                                   | Example             | Description                                                                 |
|-----------------------------|--------|-------------------------------------------|---------------------|-----------------------------------------------------------------------------|
| `private_fireedge_endpoint` | `str`  | `http://localhost:2616`                   |                     | FireEdge URL used internally in Sunstone / reverse proxies (Passenger).     |
| `public_fireedge_endpoint`  | `str`  | conditional                               | (check below)       | Base URL (domain or IP-based) over which end-users can access the service.  |
| `one_token`                 | `str`  | undefined                                 | `asd123as:123asd12` | OpenNebula Enterprise Edition subscription token.                           |
| `one_fqdn`                  | `str`  | undefined                                 | `nebula.example.io` | Fully qualified domain name of the OpenNebula instance.                     |
| `one_vip`                   | `str`  | undefined                                 | `10.11.12.13`       | When OpenNebula is in HA mode it points to the Leader.                      |
| `leader`                    | `str`  | undefined                                 | `10.11.12.13`       | When OpenNebula is in HA mode it points to the Leader.                      |
| `features.passenger`        | `bool` | `false`                                   | (check below)       | Enable Passenger/Apache2 high-performance Sunstone.                         |
| `apache2_http.managed`      | `bool` | `true`                                    | (check below)       | Enable Passenger/Apache2 over HTTP/80.                                      |
| `apache2_https.managed`     | `bool` | `false`                                   | (check below)       | Enable Passenger/Apache2 over HTTPS/443.                                    |
| `apache2_https.key`         | `str`  | `/etc/ssl/private/opennebula-key.pem`     |                     | Private key path on the target Front-end (the file must be readable).       |
| `apache2_https.certchain`   | `str`  | `/etc/ssl/certs/opennebula-certchain.pem` |                     | Certificate chain path on the target Front-end (the file must be readable). |

Dependencies
------------

- opennebula.deploy.opennebula.leader

Example Playbook
----------------

    - hosts: frontend
      vars:
        public_fireedge_endpoint: "https://nebula.example.io"
        one_fqdn: "nebula.example.io"
        features:
          passenger: true # enable Passenger/Apache2 Sunstone
        apache2_http:
          managed: false # disable plain HTTP
        apache2_https:
          managed: true # enable HTTPS with the default key and certchain
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
