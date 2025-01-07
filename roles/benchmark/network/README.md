Role: opennebula.deploy.benchmark.network
=============================

A role that performs a network benchmark (throughput and RTT) between OpenNebula hosts. Throughput is measured using IPerf3, latency is measured using ping.

Requirements
------------

N/A

Role Variables
--------------

| Name                     | Type   | Default            | Example             | Description                                                       |
|--------------------------|--------|--------------------|---------------------|-------------------------------------------------------------------|
| `run_iperf`         | `bool`  | `true`         |                     | Determines whether the throughput tests should be performed.                |
| `run_ping`         | `bool`  | `true`         |                     | Determines whether the RTT tests should be performed.                |
|                          |        |                    |                     |                                                                   |
| `iperf3_port`            | `str`  | `5201` |                     | TCP port where the IPerf3 server will listen.                     |
| `iperf3_test_time`           | `str`  | `10` |                     | Testing time for each Iperf3 test instance, in seconds. |
| `ping_test_time`           | `str`  | `10` |                     | Testing time for each ping test instance, in seconds. |

Dependencies
------------

Example Playbook
----------------

```yaml
- hosts: "{{ node_group | d('node') }}"
  tags: [node]
  collections:
    - opennebula.deploy
  roles:

    - role: helper/facts
      tags: [always]


    - role: helper/cache
      vars:
        update_pkg_cache: true
        unattend_disable: true

    - role: benchmark/network
      vars:
        run_iperf: false
```

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
