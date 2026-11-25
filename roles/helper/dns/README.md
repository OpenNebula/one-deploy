Role: opennebula.deploy.helper.dns
==================================

A role that configures DNS forwarder (Unbound).

Requirements
------------

N/A

Role Variables
--------------

| Name            | Type   | Default               | Example         | Description                                                     |
|-----------------|--------|-----------------------|-----------------|-----------------------------------------------------------------|
| `dns_resolvers` | `dict` | (check role defaults) |                 | Default configs for DNS resolvers.                              |
| `dns_resolver`  | `str`  | `unbound`             |                 | DNS resolver to use (currently only Unbound is supported).      |
| `dns`           | `list` | `[]`                  |                 | DNS configuration to apply.                                     |
| `dns[].zone`    | `str`  | `.`                   |                 | Specify a zone to add the DNS server to.                        |
| `dns[].server`  | `str`  | undefined             | `1.1.1.1`       | Add DNS server.                                                 |
| `dns[].search`  | `str`  | undefined             | `asd.io`        | Add domain to the `search` directive inside `/etc/resolv.conf`. |
| `dns[].host`    | `str`  | undefined             | `1.2.3.4 h1 h2` | Add local / static DNS hostname (just like /etc/hosts).         |

Dependencies
------------

N/A

Example Playbook
----------------

```yaml
- hosts: frontend:node
  vars:
    dns:
      # root zone
      - server: 10.3.10.1
      - server: 1.1.1.1
      - server: 8.8.8.8
      # asd.io zone
      - { server: 10.3.10.1, zone: asd.io }
      - search: asd.io
      # local data
      - host: 1.2.3.4 h1 h2 h3.asd.lh
      - search: asd.lh
  roles:
    - role: opennebula.deploy.helper.facts
    - role: opennebula.deploy.helper.dns
```

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
