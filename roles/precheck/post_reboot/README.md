Role: opennebula.deploy.precheck.post_reboot
============================================

A role that performs various checks and assertions.

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
      vars:
        kernel_ok_to_reboot: true
        kernel_need_to_reboot: true
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.kernel
        - role: opennebula.deploy.precheck.post_reboot

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
