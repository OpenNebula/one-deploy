Role: opennebula.deploy.helper.kernel
=====================================

A role that updates Linux kernel's cmdline (+ reboot).

Requirements
------------

N/A

Role Variables
--------------

| Name                  | Type   | Default   | Example       | Description                         |
|-----------------------|--------|-----------|---------------|-------------------------------------|
| `kernel_ok_to_reboot` | `bool` | `false`   | (check below) | Give consent to reboot.             |
| `kernel_params`       | `list` | undefined | (check below) | List of kernel params (unverified). |

Dependencies
------------

- `ansible.utils`

Example Playbook
----------------

    - hosts: node
      vars:
        kernel_ok_to_reboot: true
        kernel_params:
          - hugepagesz: "2M"
          - hugepages: 0
          - hugepagesz: "1G"
          - hugepages: 0
          - intel_iommu: "on"
            managed: false  # keep it in the inventory but disabled
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.kernel

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
