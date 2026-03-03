Role: opennebula.deploy.helper.kernel
=====================================

A role that updates Linux kernel's cmdline (+ reboot).

Requirements
------------

N/A

Role Variables
--------------

| Name                    | Type   | Default   | Example       | Description                                                        |
|-------------------------|--------|-----------|---------------|--------------------------------------------------------------------|
| `kernel_ok_to_reboot`   | `bool` | `false`   | (check below) | Give consent to reboot.                                            |
| `kernel_need_to_reboot` | `bool` | `false`   |               | Indicate reboot **should** be performed (ie. **try** to force it). |
| `kernel_params`         | `list` | undefined | (check below) | List of kernel params (unverified).                                |
| `kernel_modules`        | `list` | undefined | (check below) | List of kernel modules to be loaded or blacklisted.                |

Dependencies
------------

N/A

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
        kernel_modules:
          - load: kvm-amd
            options: ["nested=1"]
            managed: false  # keep it in the inventory but disabled
          # PCI passthrough
          - load: vfio-pci
          - load: nvgrace-gpu-vfio-pci
          # Disable Nouveau
          - blacklist: nouveau
          # Core NVIDIA driver stack
          - blacklist: nvidia
          - blacklist: nvidia_modeset
          - blacklist: nvidia_drm
          - blacklist: nvidia_uvm
          # Optional / auxiliary NVIDIA modules
          - blacklist: nvidia_vgpu_vfio
          - blacklist: nvidia_peermem
          - blacklist: nvidia_fs
          - blacklist: nvidia_cspmu
          - blacklist: nvidiafb
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.kernel

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
