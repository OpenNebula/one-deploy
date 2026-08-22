Role: opennebula.deploy.infra
=============================

A role that pre-deploys Front-end VMs directly in Libvirt.

Requirements
------------

Pre-installed Libvirt software (in the case of `infra` and `node` groups share hosts, then `opennebula-node-kvm` is pre-installed automatically).

Role Variables
--------------

| Name                                 | Type   | Default            | Example             | Description                                                       |
|--------------------------------------|--------|--------------------|---------------------|-------------------------------------------------------------------|
| `frontend_group`                     | `str`  | `frontend`         |                     | Custom name of the Frontend group in the inventory.               |
| `infra_group`                        | `str`  | `infra`            |                     | Custom name of the Infra group in the inventory.                  |
|                                      |        |                    |                     |                                                                   |
| `runtime_dir`                        | `str`  | `/var/one-deploy/` |                     | Directory used to store QCOW2 and ISO images.                     |
| `os_image_url`                       | `str`  |                    |                     | HTTP(S) link to Debian/RedHat-like image running `one-contextd`.  |
| `os_image_size`                      | `str`  | `20G`              |                     | The size to which one-deploy will **try** to adjust the OS image. |
| `memory_KiB`                         | `str`  | `2097152`          |                     | Memory amount to be set in XML in Libvirt.                        |
| `vnc_max_port`                       | `str`  | `65535`            |                     | Upper limit for VNC ports to start counting-down from.            |
| `passthrough_fs`                     | `list` | `[]`               | (check below)       | Shared HV filesystems to attach to the Front-end VMs.             |
|                                      |        |                    |                     |                                                                   |
| `vcpu_pinned`                        | `str`  |                    | `1-2,4`             | List of isolcpus= ranges (comma-separated).                       |
| `vcpu_static`                        | `str`  | `1`                |                     | VCPU amount to be set in XML in Libvirt.                          |
| `vcpu_shares`                        | `str`  | `200`              |                     | The proportional weighted share (PWS) for the domain.             |
|                                      |        |                    |                     |                                                                   |
| `infra_bridge`                       | `str`  | `br0`              |                     | Pre-defined bridge interface to insert VM NICs to.                |
| `infra_vlan_id`                      | `str`  |                    |                     | Optionally set the VLAN ID for the bridge.                        |
| `dpdk_socket_path`                   | `str`  |                    |                     | Path for existing socket when using OVS with DPDK.                |
|                                      |        |                    |                     |                                                                   |
| `infra_hostname`                     | `str`  |                    | `n1a1`              | Defines on which HV machine the Front-end VM should be deployed.  |
| `infra_xml_variant`                  | `str`  | undefined          | `pinned`            | Defined which domain XML variant will be used in Libvirt.         |
|                                      |        |                    |                     |                                                                   |
| `context.ETH0_DNS`                   | `str`  |                    | `1.1.1.1`           | DNS server.                                                       |
| `context.ETH0_SEARCH_DOMAIN`         | `str`  |                    | `1.1.1.1`           | DNS search domain.                                                |
| `context.ETH0_GATEWAY`               | `str`  |                    | `10.2.50.1`         | Gateway.                                                          |
| `context.ETH0_IP`                    | `str`  |                    | `10.2.50.100`       | IPv4 address to be set on eth0.                                   |
| `context.ETH0_MAC`                   | `str`  |                    | `02:01:0a:02:32:64` | MAC address to be set on eth0 (**MUST** match MAC set in XML.)    |
| `context.ETH0_MASK`                  | `str`  |                    | `255.255.255.0`     | Network mask.                                                     |
| `context.ETH0_NETWORK`               | `str`  |                    | `10.2.50.0`         | Network address.                                                  |
| `context.GROW_FS`                    | `str`  | `/`                |                     | Filesystems to grow.                                              |
| `context.PASSWORD`                   | `str`  | `opennebula`       |                     | Root's password.                                                  |
| `context.SET_HOSTNAME`               | `str`  | name of the FE VM  |                     | Hostname.                                                         |
| `context.SSH_PUBLIC_KEY`             | `str`  |                    | (check below)       | Root's extra authorized keys.                                     |
| `context.START_SCRIPT_BASE64`        | `str`  |                    |                     | Start script (base64-encoded).                                    |

**NOTE**: The `infra_hostname` and `context` dictionary should be set for members of the `frontend` group (please check the `inventory/infra.yml` example).

Dependencies
------------

- `community.libvirt`
- `ansible.posix`

Example Inventory
-----------------

    infra:
      vars:
        os_image_url: https://d24fmfybwxpuhu.cloudfront.net/ubuntu2404-7.2.0-0-20260330.qcow2
        os_image_size: 20G
        memory_KiB: 2097152 # 2 GiB
        infra_xml_variant: pinned
        vcpu_pinned: '1,3'
      hosts:
        u1q20: { ansible_host: 10.3.10.20 }
        u1q30: { ansible_host: 10.3.10.30 }

    frontend:
      vars:
        context:
          ETH0_DNS: 10.3.10.1
          ETH0_GATEWAY: 10.3.10.1
          ETH0_MASK: 255.255.255.0
          ETH0_NETWORK: 10.3.10.0
          ETH0_IP: "{{ ansible_host }}"
          PASSWORD: asd
          SSH_PUBLIC_KEY: |-
            ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIF5ndznuZTNZ8u7FCYKgv6Q3/HUVxnaha3tPDUXPfIIw
      hosts:
        u1q40: { ansible_host: 10.3.10.40, infra_hostname: u1q20 }
        u1q50: { ansible_host: 10.3.10.50, infra_hostname: u1q30 }

    node:
      vars:
        kernel_ok_to_reboot: true
        kernel_params:
          - isolcpus: "1-3,5-7"
          - nohz_full: "1-3,5-7"
          - rcu_nocbs: "1-3,5-7"
          - irqaffinity: "0,4"
          - kthread_cpus: "0,4"
          - systemd.cpu_affinity: "0,4"
          - default_hugepagesz: "1G"
          - hugepages: "0:2,1:2"
          - intel_iommu: "on"
      hosts:
        u1q20: { ansible_host: 10.3.10.20 }
        u1q30: { ansible_host: 10.3.10.30 }

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
