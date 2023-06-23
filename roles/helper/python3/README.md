Role: opennebula.deploy.helper.python3
======================================

A simple role that installs Python3 on Debian/RedHat-like distros (via BASH script).

Requirements
------------

N/A

Role Variables
--------------

N/A

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: frontend:node
      strategy: linear
      roles:
         - role: opennebula.deploy.helper.python3

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
