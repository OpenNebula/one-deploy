Role: opennebula.deploy.opennebula.server
=========================================

A role that deploys OpenNebula Frontends in HA mode.

Requirements
------------

N/A

Role Variables
--------------

| Name                | Type   | Default      | Example       | Description                                                                                                     |
|---------------------|--------|--------------|---------------|-----------------------------------------------------------------------------------------------------------------|
| `one_pass`          | `str`  | `null`       | `asd123`      | Use specific password for the `oneadmin` user.                                                                  |
| `force_ha`          | `bool` | `false`      |               | Deploy OpenNebula in HA mode even with a single Frontend.                                                       |
| `unsafe_migrations` | `bool` | `true`       |               | Disable LibVirt's NFS/mountpoint checks.                                                                        |
| `keep_empty_bridge` | `bool` | `true`       |               | Make sure empty network bridges are never removed (from Nodes).                                                 |
| `one_vip`           | `str`  | undefined    | `10.11.12.13` | When OpenNebula is in HA mode it points to the Leader.                                                          |
| `one_vip_if`        | `str`  | undefined    | `eth0`        | NIC device to assign the `one_vip` address to (on Frontends).                                                   |
| `one_vip_cidr`      | `int`  | undefined    | `24`          | CIDR prefix of the subnet `one_vip` is allocated in.                                                            |
| `db_backend`        | `str`  | `MariaDB`    |               |`MariaDB` or `SQLite`.                                                                                           |
| `db_name`           | `str`  | `opennebula` |               | Name of the database/schema used by OpenNebula.                                                                 |
| `db_owner`          | `str`  | `oneadmin`   |               | User used by OpenNebula to access the database.                                                                 |
| `db_password`       | `str`  | `opennebula` |               | Password used by OpenNebula to authenticate the user.                                                           |
| `gate_endpoint`     | `str`  | conditional  | (check below) | An URL used to reach the OneGate endpoint (HTTP).                                                               |
| `admin_pubkey`      | `str`  | loaded       | (check below) | SSH pubkey loaded from `/var/lib/one/.ssh/id_rsa.pub`, provided by the user (as string) or ignored when `null`. |
| `rank`              | `str`  | undefined    | (check below) | Rank scheduler configuration.                                                                                   |
| `drs`               | `str`  | undefined    | (check below) | OpenNebula Distributed Resource Scheduler configuration.                                                        |

Dependencies
------------

- community.general

Example Playbook
----------------

    - hosts: frontend
      vars:
        gate_endpoint: "http://10.11.12.13:5030"
        admin_pubkey: null  # ignore it
        rank:
          DIFFERENT_VNETS: NO

          DEFAULT_SCHED:
            POLICY: 3
            RANK: "- (RUNNING_VMS * 50  + FREE_CPU)"

        drs:
          PREDICTIVE: 0.3
          MEMORY_SYSTEM_DS_SCALE: 0
          DIFFERENT_VNETS: YES
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
