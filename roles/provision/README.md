Role: opennebula.deploy.provision
=================================

A role that sets up the OneProvision utility.

Requirements
------------

N/A

Role Variables
--------------

| Name                          | Type  | Default       | Example                             | Description                                |
|-------------------------------|-------|---------------|-------------------------------------|--------------------------------------------|
| `provision_ansible_version`   | `str` | `2.15.13`     |                                     | Ansible/Core version to install (PIP).     |
| `provision_terraform_version` | `str` | `0.14.7`      |                                     | Terraform version to install.              |
| `provision_terraform_url`     | `str` | (check below) | `http://mirror.local/terraform.zip` | Where to look the terraform zipped binary. |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: frontend
      vars:
        provision_terraform_url: >-
          https://releases.hashicorp.com/terraform/0.14.7/terraform_0.14.7_linux_amd64.zip
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.provision

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
