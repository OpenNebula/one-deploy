Role: opennebula.deploy.helper.facts
====================================

A role to replace/optimize built-in fact gathering.

Requirements
------------

N/A

Role Variables
--------------

| Name           | Type   | Default          | Example | Description                                                  |
|----------------|--------|------------------|---------|--------------------------------------------------------------|
| `facts_subset` | `list` | `[min, network]` |         | Define it to gather only a subset of facts.                  |
| `_force`       | `bool` | undefined        | `true`  | Re-gather facts even if the `setup` fact is already defined. |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: frontend:node
      roles:
         - { role: opennebula.deploy.helper.facts, _force: true }

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
