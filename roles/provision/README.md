Role: opennebula.deploy.flow
============================

A role that sets up the OneProvision utility.

Requirements
------------

N/A

| Name                        | Type  |                               Default                                            |               Example             |              Description                   |
| --------------------------- | ----- | -------------------------------------------------------------------------------- | --------------------------------- | ------------------------------------------ |
| `terraform_source`          | `str` | https://releases.hashicorp.com/terraform/0.14.7/terraform_0.14.7_linux_amd64.zip | http://mirror.local/terraform.zip | Where to look the terraform zipped binary  |
| `ansible_version_provision` | `str` | 2.15.13                                                                          | `2.18`                            | `ansible-core` pip package version         |



Dependencies
------------

- opennebula.deploy.opennebula.common

Example Playbook
----------------

    - hosts: frontend
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.provision

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
