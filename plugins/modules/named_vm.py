# -*- coding: utf-8 -*-
# Copyright: OpenNebula Project, OpenNebula Systems
# Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

DOCUMENTATION = r"""
module: named_vm
short_description: Create/destroy a named OpenNebula VM
description:
  - This module can create or destroy a named virtual machine instance in OpenNebula.
  - Optional datablock(s) can be automatically created and attached to the instance.
options:
  name:
    description:
      - Name of the VM in OpenNebula.
    type: str
  state:
    description:
      - Desired VM state C(present) or C(absent).
    choices: ["present", "absent"]
    default: present
    type: str
  template:
    description:
      - VM template definition.
    type: dict
    suboptions:
      name:
        description:
          - Name of an existing VM template.
        type: str
      content:
        description:
          - Extra content merged into the template.
        type: dict
  datablocks:
    description:
      - Datablock defintions (list of dicts).
    type: list
    elements: dict
  auth:
    description:
      - OpenNebula endpoint and credentials.
    type: dict
    suboptions:
      host:
        description:
          - OpenNebula XMLRPC2 endpoint.
        type: str
      user:
        description:
          - Existing OpenNebula user.
        type: str
      pswd:
        description:
          - OpenNebula user's password.
        type: str
author:
  - Michal Opala (@sk4zuzu)
"""

EXAMPLES = r"""
- name: Terminate named_vm1
  opennebula.deploy.named_vm:
    name: named_vm1
    state: absent
    auth:
      host: http://localhost:2633/RPC2
      user: oneadmin
      pswd: opennebula

- name: Instantiate named_vm2 from an existing VM template
  opennebula.deploy.named_vm:
    name: named_vm2
    template:
      name: Alpine Linux 3.17
    auth:
      host: http://localhost:2633/RPC2
      user: oneadmin
      pswd: opennebula

- name: Instantiate named_vm3 from an existing VM template attaching a NIC device (eth0)
  opennebula.deploy.named_vm:
    name: named_vm3
    template:
      name: Alpine Linux 3.17
      content:
        NIC:
          NETWORK: service
    auth:
      host: http://localhost:2633/RPC2
      user: oneadmin
      pswd: opennebula

- name: Instantiate named_vm4 from an existing VM template attaching two 20GiB datablocks
  opennebula.deploy.named_vm:
    name: named_vm4
    template:
      name: Alpine Linux 3.17
    datablocks:
      - PERSISTENT: "NO"
        DATASTORE_ID: 1
        FORMAT: "qcow2"
        DEV_PREFIX: "vd"
        SIZE: 20480
      - PERSISTENT: "NO"
        DATASTORE_ID: 1
        FORMAT: "qcow2"
        DEV_PREFIX: "vd"
        SIZE: 20480
    auth:
      host: http://localhost:2633/RPC2
      user: oneadmin
      pswd: opennebula

- name: Instantiate named_vm5 directly (without VM template)
  opennebula.deploy.named_vm:
    name: named_vm5
    template:
      content:
        CONTEXT:
          NETWORK: "YES"
          SSH_PUBLIC_KEY: "$USER[SSH_PUBLIC_KEY]"
        CPU: "1"
        DISK:
          IMAGE_ID: "2"
        GRAPHICS:
          LISTEN: "0.0.0.0"
          TYPE: vnc
        MEMORY: 1024
        NIC:
          NETWORK: service
    auth:
      host: http://localhost:2633/RPC2
      user: oneadmin
      pswd: opennebula
"""

RETURN = r"""
errors:
    description: List of errors detected during module execution.
    type: list
    elements: str
    returned: always
template:
    description: Dictionary containing final VM template data.
    type: dict
    returned: always
params:
    description: Input parameters of the module (for reference).
    type: dict
    returned: always
"""


from ansible.module_utils.basic import AnsibleModule

import time
import traceback

from ansible_collections.opennebula.deploy.plugins.module_utils.main import (flatten,
                                                                             to_one,
                                                                             get_one,
                                                                             get_vm,
                                                                             get_template,
                                                                             get_datablocks)


def _create_datablocks(params, one):
    if params.get("datablocks") is None:
        return False

    before = {
        image.NAME
        for image in get_datablocks(params, one=one)
    }

    for index, template in enumerate(params["datablocks"]):
        name = "{name:s}-{index:d}".format(**params, index=index)

        if name in before:
            continue

        template["NAME"] = name
        template["TYPE"] = "DATABLOCK"

        one.image.allocate(to_one(template), int(template["DATASTORE_ID"]))

    after = {
        image.NAME
        for image in get_datablocks(params, one=one)
    }

    return before != after


def _create_vm(params, one):
    if params["template"].get("content") is None:
        raise ValueError("template content is undefined")

    _create_datablocks(params, one)

    content = params["template"]["content"]

    content["NAME"] = params["name"]

    # Append datablock(s) if present.
    content["DISK"] = flatten(
        [content.get("DISK", [])] + [
            { "IMAGE_ID": image.ID }
            for image in get_datablocks(params, one=one)
        ],
        extract=True
    )

    one.vm.allocate(to_one(content))
    return True


def _instantiate_template(template, params, one):
    _create_datablocks(params, one)

    content = params["template"].get("content") or {}

    # Append datablock(s) if present.
    content["DISK"] = flatten(
        [template.TEMPLATE.get("DISK", [])] + [
            { "IMAGE_ID": image.ID }
            for image in get_datablocks(params, one=one)
        ],
        extract=True
    )

    one.template.instantiate(template.ID,
                             params["name"],
                             False,
                             to_one(content))
    return True


def _terminate_vm(vm, params, one):
    if vm is None:
        return False

    one.vm.recover(vm.ID, 3)

    # Delete datablock(s) if present.
    for image in get_datablocks(params, one=one):
        for retry in range(10):
            try:
                one.image.delete(image.ID, True)
                break
            except:
                time.sleep(5)

    return True


def _dispatch(params, one):
    vm       = get_vm(params, one=one)
    template = get_template(params, one=one)

    if params["state"] == "present":
        if vm is not None:
            return False
        else:
            if template is None:
                return _create_vm(params, one)
            else:
                return _instantiate_template(template, params, one)

    if params["state"] == "absent":
        if vm is not None:
            return _terminate_vm(vm, params, one)
        else:
            return False


def _main():
    module = AnsibleModule(
        argument_spec = dict(
            name  = dict(required=True, type="str"),
            state = dict(required=False, type="str", choices=["present", "absent"], default="present"),

            template = dict(required=False, type="dict",
                options=dict(
                    name    = dict(required=False, type="str"),
                    content = dict(required=False, type="dict"),
                ),
                required_one_of=[
                    ("name", "content"),
                ],
            ),

            datablocks = dict(required=False, type="list", elements="dict"),

            auth = dict(required=True, type="dict",
                options=dict(
                    host = dict(required=True, type="str"),
                    user = dict(required=True, type="str"),
                    pswd = dict(required=True, type="str"),
                ),
            ),
        ),
        required_if=[
            ("state", "present", ["template"], True),
        ],
    )

    one = get_one(module.params)

    try:
        errors   = []
        changed  = _dispatch(module.params, one)
        instance = get_vm(module.params, one=one)
    except:
        errors   = [traceback.format_exc()]
        changed  = False
        instance = None

    module.exit_json(
        changed  = changed,
        failed   = bool(errors),
        errors   = errors,
        template = dict(instance.TEMPLATE) if instance is not None else None,
        params   = module.params,
    )


if __name__ == "__main__":
    _main()
