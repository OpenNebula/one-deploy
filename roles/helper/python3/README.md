Role: opennebula.deploy.helper.python3
======================================

A simple role that installs Python3 on Debian/RedHat-like distros (via BASH script).

Requirements
------------

N/A

Role Variables
--------------

| Name                         | Type   | Default               | Example       | Description                                        |
|------------------------------|--------|-----------------------|---------------|----------------------------------------------------|
| `ansible_python_interpreter` | `str`  | `/usr/bin/python3`    | (check below) | Ansible's built-in, please refer to official docs. |
| `python3_os_packages`        | `list` | (check role defaults) | (check below) | Extra python3 OS packages to install.              |
| `python3_pip_packages`       | `list` | (check role defaults) | (check below) | Extra python3 PyPI packages to install.            |

Dependencies
------------

N/A

Example Playbook
----------------

    - hosts: frontend:node
      strategy: linear
      vars:
        ansible_python_interpreter: /usr/bin/python3.11
        python3_os_packages:
          Debian: []
          openSUSE Leap: []
          RedHat: []
          Suse: [python311-pip]
        python3_pip_packages:
          Debian: []
          openSUSE Leap: []
          RedHat: []
          Suse: [ruamel.yaml]
      roles:
        - role: opennebula.deploy.helper.python3 # install interpreter only
        - role: opennebula.deploy.helper.facts   # provide the 'setup' fact
        - role: opennebula.deploy.helper.cache
        - role: opennebula.deploy.helper.python3 # install packages only

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
