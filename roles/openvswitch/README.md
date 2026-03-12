Role: opennebula.deploy.openvswitch
===================================

A role that **replaces** OS default networking with OVS/DPDK.

Requirements
------------

N/A

Role Variables
--------------

| Name           | Type   | Default               | Example       | Description                              |
|----------------|--------|-----------------------|---------------|------------------------------------------|
| `ovs`          | `dict` | (check role defaults) | (check below) | OVS/DPDK config.                         |
| `ovs_packages` | `dict` | (check role defaults) |               | OVS/DPDK packages grouped per OS distro. |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: node
      vars:
        kernel_ok_to_reboot: true
        kernel_params:
          - default_hugepagesz: "1G"
          - hugepagesz: "1G"
          - hugepages: 3
          - intel_iommu: "on"
        kernel_modules:
          - load: vfio-pci
          - load: vfio_iommu_type1
            options: ["allow_unsafe_interrupts=1"] # for virtio-net-pci devices
        opennebula_repo_pre_enable:
          AlmaLinux:
            extra_rpms:
              '10': [centos-release-nfv-openvswitch]
            config_manager:
              '10': [crb, epel, highavailability, centos-nfv-openvswitch]
          RedHat:
            subscription_manager:
              '9':
                - codeready-builder-for-rhel-9-x86_64-rpms
                - rhel-9-for-x86_64-highavailability-rpms
                - fast-datapath-for-rhel-9-x86_64-rpms
        ovs:
          set:
            - other_config:dpdk-init: 'true'
            - other_config:dpdk-socket-mem: '1024,0'
          iface:
            dpdk-p0:
              set:
                - type: dpdkvhostuserclient
                - options:vhost-server-path: /var/tmp/dpdk-p0
            dpdk-p1:
              set:
                - type: dpdk
                - options:dpdk-devargs: '0000:02:00.0'
            dpdk-p2:
              set:
                - type: dpdk
                - options:dpdk-devargs: '0000:03:00.0'
            eth3: {} # non-DPDK device
          bond:
            bond0:
              ifaces: [dpdk-p1, dpdk-p2]
              mode: active-backup
          br:
            ovsbr0:
              ports: [dpdk-p0, bond0]
              set:
                - datapath_type: netdev
              addrs:
                - cidr: "{{ ansible_default_ipv4.address ~ '/' ~ ansible_default_ipv4.prefix }}"
                  metric: 400
              gw: "{{ ansible_default_ipv4.gateway }}"
              dns: ["{{ ansible_default_ipv4.gateway }}"]
            ovsbr1: # non-DPDK bridge
              ports: [eth3]
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.kernel
        - role: opennebula.deploy.repository
        - role: opennebula.deploy.openvswitch

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
