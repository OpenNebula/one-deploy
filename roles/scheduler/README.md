Role: opennebula.deploy.scheduler
================================

A role that configures the OpenNebula scheduler.

Requirements
------------

N/A

Role Variables
--------------

| Name                                  | Type   | Default                                               | Example | Description                                                           |
|---------------------------------------|--------|-------------------------------------------------------|---------|-----------------------------------------------------------------------|
| `sched.solver`                        | `str`  | `CBC`                                                 |         | `CBC` or `GLPK` or `COINMP`                                           |
| `sched.solver_path`                   | `str`  | `/usr/lib/one/python/pulp/solverdir/cbc/linux/64/cbc` |         | Specifies the path to the solver binary                               |
| `sched.place.policy`                  | `str`  | `BALANCE`                                             |         | `BALANCE` or `PACK`                                                   |
| `sched.place.weights`                 | `dict` |                                                       |         | Relative importance of the total CPU and Memory                       |
| `sched.optimize.policy`               | `str`  | `BALANCE`                                             |         | `BALANCE` or `PACK`                                                   |
| `sched.optimize.migration_threshold`  | `int`  | `-1`                                                  |         | Threshold for VMs that can be migrated                                |
| `sched.optimize.weights`              | `dict` |                                                       |         | Relative importance of the CPU, CPU_USAGE, NET, DISK and MEMORY       |
| `sched.predictive`                    | `int`  | `0`                                                   |         | Schedules with current/future resource usage                          |
| `sched.memory_system_ds_scale`        | `int`  | `0`                                                   |         | Scales VM usage of the system DS with memory size                     |
| `sched.different_vnets`               | `str`  | `YES`                                                 |         | If set (YES), NICs go to separate VNs                                 |


Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: frontend
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.scheduler

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
