Role: opennebula.deploy.opennebula.server
=========================================

A role that deploys OpenNebula Frontends in HA mode.

Requirements
------------

N/A

Role Variables
--------------

| Name                | Type   | Default       | Example       | Description                                                                                                     |
|---------------------|--------|---------------|---------------|-----------------------------------------------------------------------------------------------------------------|
| `one_pass`          | `str`  | `null`        | `asd123`      | Use specific password for the `oneadmin` user.                                                                  |
| `force_ha`          | `bool` | `false`       |               | Deploy OpenNebula in HA mode even with a single Frontend.                                                       |
| `unsafe_migrations` | `bool` | `true`        |               | Disable LibVirt's NFS/mountpoint checks.                                                                        |
| `keep_empty_bridge` | `bool` | `true`        |               | Make sure empty network bridges are never removed (from Nodes).                                                 |
| `one_vip`           | `str`  | undefined     | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader.                                                          |
| `one_vip_if`        | `str`  | undefined     | `eth0`        | NIC device to assign the `one_vip` address to (on Frontends).                                                   |
| `one_vip_cidr`      | `int`  | undefined     | `24`          | CIDR prefix of the subnet `one_vip` is allocated in.                                                            |
| `leader_hook`       | `str`  | `raft/vip.sh` |               | Define RAFT leader VIP handler.                                                                                 |
| `follower_hook`     | `str`  | `raft/vip.sh` |               | Define RAFT follower VIP handler.                                                                               |
| `db_backend`        | `str`  | `MariaDB`     |               |`MariaDB` or `SQLite`.                                                                                           |
| `db_name`           | `str`  | `opennebula`  |               | Name of the database/schema used by OpenNebula.                                                                 |
| `db_owner`          | `str`  | `oneadmin`    |               | User used by OpenNebula to access the database.                                                                 |
| `db_password`       | `str`  | `opennebula`  |               | Password used by OpenNebula to authenticate the user.                                                           |
| `gate_endpoint`     | `str`  | conditional   | (check below) | An URL used to reach the OneGate endpoint (HTTP).                                                               |
| `admin_pubkey`      | `str`  | loaded        | (check below) | SSH pubkey loaded from `/var/lib/one/.ssh/id_rsa.pub`, provided by the user (as string) or ignored when `null`. |
| `sched_rank`        | `dict` | undefined     | (check below) | Rank scheduler configuration.                                                                                   |
| `oned_conf`         | `dict` | undefined     | (check below) | Extra `/etc/one/oned.conf` settings, keys are "/"-separated paths, values inserted verbatim (quote strings).  |
| `kvm_conf`          | `dict` | undefined     | (check below) | Extra `/etc/one/vmm_exec/vmm_exec_kvm.conf` settings (same format as `oned_conf`).                             |
| `kvmrc`             | `dict` | undefined     | (check below) | Extra `/var/lib/one/remotes/etc/vmm/kvm/kvmrc` shell variables (flat `NAME: value`, `null` unsets).            |
| `sched_drs`         | `dict` | undefined     | (check below) | OpenNebula Distributed Resource Scheduler configuration.                                                        |
| `auth.default`      | `str`  | `null`        |               | Pick default auth mechanism (currently only `ldap` is supported in one-deploy).                                 |
| `auth.ldap.config`  | `dict` | `{}`          | (check below) | LDAP authentication config (/etc/one/auth/ldap_auth.conf).                                                      |
| `auth.ldap.mapping` | `dict` | `{}`          | (check below) | LDAP authentication group mapping (manually defined).                                                           |

> **Note:** Typed variables (`gate_endpoint`, `sched_rank`, `sched_drs`, `auth.*`, ...) are used where
> one-deploy derives, validates or converts values. The generic `oned_conf`, `kvm_conf` and `kvmrc` dicts are
> a verbatim pass-through for anything else: for the OpenNebula-template style files (`oned_conf`, `kvm_conf`)
> keys are "/"-separated paths into the file and strings must carry their own quotes
> (`LOG_CALL_FORMAT: '"Req:%i ..."'`); `kvmrc` is a shell rc file, so keys are plain variable names and
> values are written as-is. A `null` value drops the attribute (or the whole vector). Prefer the typed variable when one exists, settings they manage are rejected in the generic dicts.

Dependencies
------------

- community.general

Example Playbook
----------------

    - hosts: frontend
      vars:
        gate_endpoint: "http://10.11.12.13:5030"
        admin_pubkey: null  # ignore it

      # LDAP authentication with manually defined group mappings.
      auth:
        default: ldap
        ldap:
          config:
            :order: [dirsrv]
            dirsrv:
              :user: cn=admin,dc=sk4zuzu,dc=eu
              :password: asd123
              :host: 10.3.10.1
              :base: dc=sk4zuzu,dc=eu
              :rfc2307bis: true
              :group_field: memberOf
              :mapping_generate: false
              :mapping_filename: dirsrv.yaml
          mapping:
            dirsrv:
              cn=users,ou=groups,dc=sk4zuzu,dc=eu: 1

        oned_conf:
          MANAGER_TIMER: 10
          MONITORING_INTERVAL_DATASTORE: 20
          LOG/DEBUG_LEVEL: 5
          LOG_CALL_FORMAT: '"Req:%i UID:%u IP:%A %m invoked %l5000"'
          HOOK_LOG_CONF/LOG_RETENTION: 200
          RAFT/ELECTION_TIMEOUT_MS: 7000
          RAFT/BROADCAST_TIMEOUT_MS: 800
          DEFAULT_COST: null # drop the setting
        kvm_conf:
          DISK/DRIVER: '"qcow2"'
          DISK/CACHE: '"writethrough"'
        kvmrc:
          CLEANUP_MEMORY_ON_START: 'yes'
        sched_rank:
          DIFFERENT_VNETS: false

          DEFAULT_SCHED:
            POLICY: 3
            RANK: "- (RUNNING_VMS * 50  + FREE_CPU)"

        sched_drs:
          PREDICTIVE: 0.3
          MEMORY_SYSTEM_DS_SCALE: 0
          DIFFERENT_VNETS: true
          DEFAULT_SCHED:
            SOLVER: "CBC"
            SOLVER_PATH: "/usr/lib/one/python/pulp/solverdir/cbc/linux/64/cbc"

          PLACE:
            POLICY: "PACK"

          OPTIMIZE:
            POLICY: "BALANCE"
            MIGRATION_THRESHOLD: 10
            WEIGHTS:
              CPU_USAGE: 0.2
              CPU: 0.2
              MEMORY: 0.4
              DISK: 0.1
              NET: 0.1

      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.database
        - role: opennebula.deploy.opennebula.server

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
