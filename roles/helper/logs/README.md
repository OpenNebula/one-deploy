Role: opennebula.deploy.helper.logs
===================================

A role that configures logrotate and rsyslog (when available).

Requirements
------------

N/A

Role Variables
--------------

| Name                         | Type   | Default               | Example       | Description                        |
|------------------------------|--------|-----------------------|---------------|------------------------------------|
| `logrotate`                  | `dict` | `{}`                  | (check below) | User config for logrotate subrole. |
| `logrotate_defaults`         | `dict` | (check role defaults) | (check below) |                                    |
| `rsyslog`                    | `dict` | `{}`                  | (check below) | User config for rsyslog subrole.   |
| `rsyslog_defaults`           | `dict` | (check role defaults) | (check below) |                                    |
| `rsyslog_collector.target`   | `str`  | undefined             | (check below) | Destination host to send logs to.  |
| `rsyslog_collector.protocol` | `str`  | `tcp`                 | (check below) | Protcol to use for sending logs.   |
| `rsyslog_collector.port`     | `str`  | `514`                 | (check below) | Destination port to send logs to.  |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: node
      vars:
        logrotate_defaults: {} # disable defaults
        logrotate:
          openvswitch:
            managed: true # can be omitted as it's true by default
            paths:
              - /var/log/openvswitch/*.log
            config:
              - su root root
              - daily
              - rotate 30
              - missingok
              - notifempty
              - compress
              - delaycompress
              - dateext
              - sharedscripts
              - postrotate: |-
                  if [ -d /run/openvswitch ]; then
                    for ctl in /run/openvswitch/*.ctl; do
                      ovs-appctl -t "$ctl" vlog/reopen 2>/dev/null ||:
                    done
                  fi
        rsyslog:
          90-kernel:
            # Replace default path /var/log/kern.log
            config: |
              module(load="imklog")
              kern.info /var/log/asd.log
        # Enable log forwarding
        rsyslog_collector:
          target: 10.11.12.13
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.helper.logs

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
