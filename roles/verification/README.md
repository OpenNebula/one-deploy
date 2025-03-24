Role Name
=========

OpenNebula cloud verification role.

Requirements
------------

Ansible inventory, used for the cloud deployment should be used with this playbook

Role Variables
--------------


Example Playbook
----------------

This role should be included into the target playbook, like the following:

  - hosts: "{{ frontend_group | d('frontend') }}"
    roles:
      - role: verification

License
-------

BSD

Author Information
------------------

OpenNebula team
