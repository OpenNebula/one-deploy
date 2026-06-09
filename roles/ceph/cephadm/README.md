Role: opennebula.deploy.ceph.cephadm
====================================

A role that deploys Ceph cluster via Cephadm.

Requirements
------------

N/A

Role Variables
--------------

| Name                                   | Type   | Default               | Description                                                            |
|----------------------------------------|--------|-----------------------|------------------------------------------------------------------------|
| `mon_group`                            | `str`  | `mon`                 | Custom name of the MON group in the inventory.                         |
| `mgr_group`                            | `str`  | `mgr`                 | Custom name of the MGR group in the inventory.                         |
| `osd_group`                            | `str`  | `osd`                 | Custom name of the OSD group in the inventory.                         |
| `cephadm_conf`                         | `dict` | `{}`                  | A dictionary of key/value pairs to set/rm in Ceph.                     |
| `cephadm_extra_labels`                 | `list` | `[]`                  | A list of labels to additionally apply to hosts in Ceph.               |
| `cephadm_modules`                      | `dict` | (check role defaults) | A structure describing modules (currently only "enable" is supported). |
| `cephadm_bootstrap_spec`               | `str`  | (check role defaults) | Cephadm service spec (yaml) apllied during boostrap.                   |
| `cephadm_bootstrap_spec_host_defaults` | `str`  | (check role defaults) | Default boostrap host spec.                                            |
| `cephadm_spec`                         | `str`  | (check role defaults) | Cephadm service spec (yaml) apllied to the cluster (after boostrap).   |
| `cephadm_spec_host_defaults`           | `str`  | (check role defaults) | Default runtime host spec.                                             |
| `cephadm_spec_mon_defaults`            | `str`  | (check role defaults) | Default runtime MON spec.                                              |
| `cephadm_spec_mgr_defaults`            | `str`  | (check role defaults) | Default runtime MGR spec.                                              |
| `cephadm_spec_osd_defaults`            | `str`  | (check role defaults) | Default runtime OSD spec.                                              |
| `cephadm_spec_prometheus_defaults`     | `str`  | (check role defaults) | Default runtime Prometheus spec.                                       |

Dependencies
------------

N/A

Example Inventory
-----------------

    ceph:
      children:
        ? mon
        ? mgr
        ? osd
      vars:
        # When defined in the `ceph` inventory group, all settings are applied at the "global" level in Ceph.
        cephadm_conf:
          osd_memory_target: '2147483648'

    mon:
      hosts:
        u2q10: { ansible_host: 10.3.12.10 }
        u2q20: { ansible_host: 10.3.12.20 }
        u2q30: { ansible_host: 10.3.12.30 }

    mgr:
      hosts:
        u2q10: { ansible_host: 10.3.12.10 }
        u2q20: { ansible_host: 10.3.12.20 }
        u2q30: { ansible_host: 10.3.12.30 }

    osd:
      vars:
        # When defined in the `osd` inventory group, all settings are applied at the "osd" level in Ceph.
        cephadm_conf:
          osd_memory_target_autotune: 'false'
      hosts:
        u2q40:
          ansible_host: 10.3.12.40
          # When defined on the inventory host, all settings are applied at the host level in Ceph.
          cephadm_conf:
            osd_memory_target: null # NOTE: `null` triggers `ceph config rm` instead of `ceph config set`.
        u2q50:
          ansible_host: 10.3.12.50
          cephadm_conf:
            osd_memory_target: null

Example Playbook
----------------

    - hosts: mon:mgr:osd
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.ceph.repository
        - role: opennebula.deploy.ceph.cephadm

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
