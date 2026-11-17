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
| `dns[].server`  | `str`  | undefined             |                 | Add DNS server(s).                                              |
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
      - server: 10.3.10.1
      - server: 1.1.1.1
      - server: 8.8.8.8
      - search: asd.io
      - host: 1.2.3.4 h1 h2 h3.asd.io
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
