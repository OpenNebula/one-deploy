Role: opennebula.deploy.passthrough
=================================

A role that manages passthrough related settings.

Requirements
------------

N/A

Role Variables
--------------

| Name                          | Type   | Default     | Example                             | Description                                |
|-------------------------------|--------|-------------|-------------------------------------|--------------------------------------------|
| `passthrough_iommu_pt`        | `bool` | `false`     |                                     | Ansible/Core version to install (PIP).     |


**Developer note**: Kernel parameter 'iommu=pt' results in a change in dmesg from:
`iommu: Default domain type: Translated`
to
`iommu: Default domain type: Passthrough (set via kernel command line)`.
According to [RedHat virtualization documentation](https://docs.redhat.com/en/documentation/red_hat_virtualization/4.1/html/installation_guide/appe-configuring_a_hypervisor_host_for_pci_passthrough), it provides a slight performance improvement, but it is not truly necessary.
Other sources however mention that the improvement is unnoticeable and that it is at the expense of security/device isolation.

<!-- Developer note: IOMMU also needs 'interrupt remapping' to be enabled for passthrough to work properly.
                This is more likely always enabled by default in the kernel at the same time as IOMMU, but it can be verified with the following command:
                dmesg | grep 'remapping'
                A line like "AMD-Vi: Interrupt remapping enabled" or "DMAR-IR: Enabled IRQ remapping in x2apic mode" should be present.
                The exact present line depends on the CPU vendor, and due to the lack of documentation, we can't contemplate all possible cases.
                If no line about the enablement of remapping is found, it can be enabled by force with:
                echo "options vfio_iommu_type1 allow_unsafe_interrupts=1" > /etc/modprobe.d/iommu_unsafe_interrupts.conf
                update-initramfs -u -k all && reboot
                TODO: Add it only according to a variable -->

Dependencies
------------

Example Playbook
----------------

    - hosts: all
      roles:
        - role: opennebula.deploy.passthrough

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
