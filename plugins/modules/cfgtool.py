# -*- coding: utf-8 -*-
# Copyright: OpenNebula Project, OpenNebula Systems
# Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

DOCUMENTATION = r"""
module: cfgtool
short_description: Generic module to run config parsers
description:
  - This module allows for running One and Rc parsers.
options:
  dest:
    description:
      - Filesystem path to config file to be processed.
    type: str
  parser:
    description:
      - Config parser to be used (One or Rc).
    type: str
  operation:
    description:
      - Type of operation to be perfomed inside the file (Match, Get, Put or Drop).
    type: str
  path:
    description:
      - An "ypath" expression (for example `DB/BACKEND`).
    type: str
  value:
    description:
      - Value to put (or match against) inside the file at given path.
    type: str
author:
  - Michal Opala (@sk4zuzu)
"""

EXAMPLES = r"""
- name: Update oned.conf
  opennebula.deploy.cfgtool:
    dest: /etc/one/oned.conf
    parser: One
    operation: Put
    path: DB/BACKEND
    value: '"mysql"'
"""

RETURN = r"""
params:
    description: Input parameters of the module (for reference).
    type: dict
    returned: always
"""


from ansible_collections.opennebula.deploy.plugins.module_utils.cfgtool import (OneParser, RcParser)
from ansible.module_utils.basic import AnsibleModule

import traceback


PARSERS = {
    "One": OneParser,
    "Rc": RcParser,
}

OPERATIONS = {
    "Match": dict(readonly=True, keys=["path", "value"]),
    "Get": dict(readonly=True, keys=["path"]),
    "Put": dict(readonly=False, keys=["path", "value"]),
    "Drop": dict(readonly=False, keys=["path", "value"]),
}


def _run(params):
    try:
        parser_class = PARSERS[params["parser"]]

        with open(params["dest"], "r") as f:
            before = f.read()

        parser = parser_class(before)
        parser.parse()

        operation = params["operation"]
        value = getattr(parser, operation.lower())(*[
            params[k]
            for k in OPERATIONS[operation]["keys"]
        ])

        if OPERATIONS[operation]["readonly"]:
            after = before
        else:
            after = parser.render()
            if before != after:
                with open(params["dest"], "w") as f:
                    f.write(after)
            value = params["value"]

        return dict(
            failed  = False,
            changed = before != after,
            value   = value,
            errors  = [],
        )
    except:
        return dict(
            failed  = True,
            changed = False,
            value   = None,
            errors  = [traceback.format_exc()],
        )


def _main():
    module = AnsibleModule(
        argument_spec = dict(
            dest      = dict(required=True, type="str"),
            parser    = dict(required=True, type="str", choices=list(PARSERS.keys())),
            operation = dict(required=True, type="str", choices=list(OPERATIONS.keys())),
            path      = dict(required=True, type="str"),
            value     = dict(required=False, type="str", default=None),
        ),
    )

    result = _run(module.params)

    module.exit_json(**result, params=module.params)


if __name__ == "__main__":
    _main()
