Role: opennebula.deploy.infra
=============================

A role that pre-deploys Front-end VMs directly in Libvirt.

Requirements
------------

Pre-installed Libvirt software.

Role Variables
--------------

| Name                     | Type   | Default            | Example             | Description                                                       |
|--------------------------|--------|--------------------|---------------------|-------------------------------------------------------------------|
| `frontend_group`         | `str`  | `frontend`         |                     | Custom name of the Frontend group in the inventory.               |
| `infra_group`            | `str`  | `infra`            |                     | Custom name of the Infra group in the inventory.                  |
|                          |        |                    |                     |                                                                   |
| `runtime_dir`            | `str`  | `/var/one-deploy/` |                     | Directory used to store QCOW2 and ISO images.                     |
| `os_image_url`           | `str`  | (check below)      |                     | HTTP(S) link to Debian/RedHat-like image running `one-contextd`.  |
| `os_image_size`          | `str`  | `20G`              |                     | The size to which one-deploy will **try** to adjust the OS image. |
| `memory_KiB`             | `str`  | `2097152`          |                     | Memory amount to be set in XML in Libvirt.                        |
| `vcpu_static`            | `str`  | `1`                |                     | VCPU amount to be set in XML in Libvirt.                          |
| `vnc_max_port`           | `str`  | `65535`            |                     | Upper limit for VNC ports to start counting-down from.            |
| `infra_bridge`           | `str`  | `br0`              |                     | Pre-defined bridge interface to insert VM NICs to.                |
| `infra_shared_paths`     | `list` | `[]`               | (check below)       | Shared HV filesystems to attach to the Front-end VMs.             |
|                          |        |                    |                     |                                                                   |
| `infra_hostname`         | `str`  |                    | `n1a1`              | Defines on which HV machine the Front-end VM should be deployed.  |
| `context.ETH0_DNS`       | `str`  |                    | `1.1.1.1`           | DNS server.                                                       |
| `context.ETH0_GATEWAY`   | `str`  |                    | `10.2.50.1`         | Gateway.                                                          |
| `context.ETH0_IP`        | `str`  |                    | `10.2.50.100`       | IPv4 address to be set on eth0.                                   |
| `context.ETH0_MAC`       | `str`  |                    | `02:01:0a:02:32:64` | MAC address to be set on eth0 (**MUST** match MAC set in XML.)    |
| `context.ETH0_MASK`      | `str`  |                    | `255.255.255.0`     | Network mask.                                                     |
| `context.ETH0_NETWORK`   | `str`  |                    | `10.2.50.0`         | Network address.                                                  |
| `context.GROW_FS`        | `str`  | `/`                |                     | Filesystems to grow.                                              |
| `context.PASSWORD`       | `str`  | `opennebula`       |                     | Root's password.                                                  |
| `context.SET_HOSTNAME`   | `str`  | name of the FE VM  |                     | Hostname.                                                         |
| `context.SSH_PUBLIC_KEY` | `str`  |                    | (check below)       | Root's extra authorized keys.                                     |

**NOTE**: The `infra_hostname` and `context` dictionary should be set for members of the `frontend` group (please check the `inventory/infra.yml` example).

Dependencies
------------

- `community.libvirt`
- `ansible.posix`

Example Playbook
----------------

    - hosts: infra
      vars:
        os_image_url: https://d24fmfybwxpuhu.cloudfront.net/ubuntu2204-6.10.0-1-20240514.qcow2
        infra_shared_paths:
          - driver_type: virtiofs
            source_dir: /var/lib/one/datastores
            target_dir: /var/lib/one/datastores
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.infra

Example Inventory
-----------------
```yaml
...
infra:
  vars:
    update_pkg_cache: true             # From role helper/cache
    #runtime_dir: /var/one-deploy/     # Where the VM Image is stored
    os_image_url: https://marketplace.opennebula.io//appliance/4562be1a-4c11-4e9e-b60a-85a045f1de05/download/0   # https://d24fmfybwxpuhu.cloudfront.net/ubuntu2204-6.8.1-1-20240131.qcow2
    os_image_size: 100G            # Default: 20G
    memory_KiB: 41943040           # Default 2097152, 2 GiB
    vcpu_static: 1                 # Default 1
    infra_bridge: br_management    # Default: br0
    infra_shared_paths:     # Host-guest shared directories. Useful but usually unnecessary
      - driver_type: virtiofs
        source_dir: /var/lib/one/datastores
        target_dir: /var/lib/one/datastores
  hosts:
    node01: { ansible_host: 192.168.0.41 }
    node02: { ansible_host: 192.168.0.42 }
    node03: { ansible_host: 192.168.0.43 }

frontend:
  vars:
    context:
      ETH0_NETWORK: "192.168.0.0"
      ETH0_MASK: "255.255.255.0"
      ETH0_GATEWAY: "192.168.0.1"
      ETH0_DNS: "8.8.8.8"
      ETH0_IP: "{{ ansible_host }}"
      USERNAME: "myuser"
      PASSWORD: "mypassword"
  hosts:
    fe1: { ansible_host: 192.168.0.11, infra_hostname: node01, ansible_user: root }
    fe2: { ansible_host: 192.168.0.12, infra_hostname: node02, ansible_user: root }
    fe3: { ansible_host: 192.168.0.13, infra_hostname: node03, ansible_user: root }
```


License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
