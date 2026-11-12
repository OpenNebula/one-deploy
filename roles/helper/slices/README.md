Role: opennebula.deploy.helper.slices
=====================================

A role that estimates and asserts CPU / MEM isolation for both FE-VMs and DPDK.

Requirements
------------

N/A

Role Variables
--------------

| Name                          | Type   | Default   | Example | Description                                                |
|-------------------------------|--------|-----------|---------|------------------------------------------------------------|
| `slices_hugepagesz`           | `str`  | `1G`      | `2M`    | Hugepage type to use (mixed types are not supported).      |
| `slices_extra_hugepage_count` | `int`  | `0`       |         | Add extra hugepages for DPDK (distributed evenly).         |
| `slices_extra_cpu_count`      | `int`  | `0`       |         | Add extra CPUs for DPDK (distributed evenly).              |
| `infra_xml_variant`           | `str`  | `default` |         | Defines which domain XML variant will be used for FE-VMs.  |
| `vcpu_pinned`                 | `str`  | empty     | `2-3,5` | Isolated CPUs (specified by CPU ID) to be used for FE-VMs. |
| `ovs`                         | `dict` | empty     |         | OVS/DPDK config.                                           |

Dependencies
------------

- `opennebula.deploy.helper.numa`
- `opennebula.deploy.infra`

Example Playbook
----------------

```yaml
# NOTE: The helper/slices role should produce suggestion like below.
#       User is supposed to start without precise `kernel_params` or `vcpu_pinned`, then
#       follow the suggestion (optionally adjusting it) to add it to the inventory.
#       The underlying OS has to satisfy at least that estimation.
#
# kernel_params:
#   - isolcpus: &claimed '2-5,10-13'
#   - nohz_full: *claimed
#   - rcu_nocbs: *claimed
#   - irqaffinity: &protected '0-1,8-9'
#   - kthread_cpus: *protected
#   - systemd.cpu_affinity: *protected
#   - default_hugepagesz: '2M'
#   - hugepagesz: '2M'
#   - hugepages: '0:2056,1:1032'

- hosts: infra:&node
  vars:
    memory_KiB: 2097152 # 2 GiB
    infra_xml_variant: openvswitch_dpdk # no CPU pinning for FE-VMs, but still uses hugepages
  roles:
    - role: opennebula.deploy.infra

- hosts: node
  vars:
    slices_hugepagesz: 2M
    slices_extra_hugepage_count: 16
    slices_extra_cpu_count: 2

    kernel_ok_to_reboot: true
    kernel_params:
      # >> INSERT THE SUGGESTION HERE <<
      - intel_iommu: 'on'
    kernel_modules:
      - load: vfio-pci
      - load: vfio_iommu_type1
        options: [allow_unsafe_interrupts=1]

    pci_devices:
      - address: '0000:30:00.0'
      - address: '0000:40:00.0'

    ovs:
      set:
        - other_config:dpdk-init: 'true'
        - other_config:dpdk-socket-mem: 'auto' # special value that triggers MEM estimation for DPDK
        - other_config:pmd-cpu-mask: 'auto'    # special value that triggers CPU estimation for DPDK
      iface:
        dpdk-p0:
          set:
            - type: dpdk
            - options:dpdk-devargs: '0000:30:00.0'
        dpdk-p1:
          set:
            - type: dpdk
            - options:dpdk-devargs: '0000:40:00.0'
        dpdk-p2:
          set:
            - type: dpdkvhostuserclient
            - options:vhost-server-path: /var/run/one/vhost-socks/FE-VM.sock
      bond:
        bond0:
          ifaces: [dpdk-p0, dpdk-p1]
          mode: active-backup
      br:
        ovsbr1:
          ports: [bond0, dpdk-p2]
          set:
            - datapath_type: netdev
  roles:
    - role: opennebula.deploy.helper.facts
    - role: opennebula.deploy.helper.slices
```

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
