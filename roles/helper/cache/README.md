Role: opennebula.deploy.helper.cache
====================================

A role that updates APT / DNF cache.

Requirements
------------

N/A

Role Variables
--------------

| Name               | Type   | Default | Example                 | Description                                   |
|--------------------|--------|---------|-------------------------|-----------------------------------------------|
| `update_pkg_cache` | `bool` | `false` | `true`                  | Update APT / DNF cache.                       |
| `unattend_disable` | `bool` | `false` | `true`                  | Purges the unattended upgrade service.        |
| `pkg_cache_proxy`  | `str`  | `null`  | `http://10.2.11.1:3142` | Define proxy endpoint (like `apt-cacher-ng`). |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: frontend:node
      roles:
        - { role: opennebula.deploy.helper.cache, update_pkg_cache: true, unattend_disable: true }

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
