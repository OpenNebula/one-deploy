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
  actions:
    description:
      - Operations to perform inside the file (Match, Get, Put or Drop).
    type: list
author:
  - Michal Opala (@sk4zuzu)
"""

EXAMPLES = r"""
- name: Update oned.conf
  opennebula.deploy.cfgtool:
    dest: /etc/one/oned.conf
    parser: One
    actions: "{{ item.actions }}"
  no_log: "{{ item.no_log | d(false) }}"
  loop: "{{ _items }}"
  vars:
    _items:
      - actions:
          - put:
              path: [DB, BACKEND]
              value: '"{{ db_backend_types[db_backend] }}"'
          - put:
              path: [DB, SERVER]
              value: '"localhost"'
          - put:
              path: [DB, PORT]
              value: 0
          - put:
              path: [DB, USER]
              value: '"{{ db_owner }}"'
          - put:
              path: [DB, DB_NAME]
              value: '"{{ db_name }}"'
          - put:
              path: [ONEGATE_ENDPOINT]
              value: '"{{ _gate_endpoint }}"'
      - actions:
          - put:
              path: [DB, PASSWD]
              value: '"{{ db_password }}"'
        no_log: true
    _gate_endpoint: >-
      {{ gate_endpoint | d(_default) }}
    _default: >-
      {{ 'http://' ~ (one_vip | d(_host)) ~ ':5030' }}
    _host: >-
      {{ hostvars[federation.groups.frontend[0]].ansible_host }}
  notify:
    - Restart OpenNebula
"""

RETURN = r"""
params:
    description: Input parameters of the module (for reference).
    type: dict
    returned: always
values:
    description: Action results.
    type: list
    returned: always
errors:
    description: Action errors.
    type: list
    returned: always
"""


from ansible_collections.opennebula.deploy.plugins.module_utils.cfgtool import (OneParser, RcParser, YamlParser)
from ansible.module_utils.basic import AnsibleModule

import traceback


PARSERS = {
    "One": OneParser,
    "Rc": RcParser,
    "Yaml": YamlParser,
}

OPERATIONS = {
    "match": dict(readonly=True, keys=["path"]),
    "get": dict(readonly=True, keys=["path"]),
    "put": dict(readonly=False, keys=["path", "value"]),
    "drop": dict(readonly=False, keys=["path"]),
}


def _run(params):
    values, errors = [], []

    try:
        parser_class = PARSERS[params["parser"]]

        with open(params["dest"], "r") as f:
            before = f.read()

        parser = parser_class(before)
        parser.parse()

        readonly = True

        for action in params["actions"]:
            try:
                skip = False
                operation = None

                for k in action.keys():
                    if k == "when":
                        skip = not action[k]
                    elif k in list(OPERATIONS.keys()):
                        operation = k
                    else:
                        raise Exception(f"Unknown action attribute: `{k}'.")

                if skip:
                    continue
                if operation is None:
                    raise Exception("No operation given.")

                readonly = readonly and OPERATIONS[operation]["readonly"]

                values.append(getattr(parser, operation)(*[
                    action[operation][k]
                    for k in OPERATIONS[operation]["keys"]
                ]))
            except:
                errors.append(traceback.format_exc())

        if errors:
            return dict(
                failed  = True,
                changed = False,
                values  = [],
                errors  = errors,
            )

        if readonly:
            after = before
        else:
            after = parser.render()
            if before != after:
                with open(params["dest"], "w") as f:
                    f.write(after)

        return dict(
            failed  = False,
            changed = before != after,
            values  = values,
            errors  = [],
        )
    except:
        errors.append(traceback.format_exc())
        return dict(
            failed  = True,
            changed = False,
            values  = [],
            errors  = errors,
        )


def _main():
    module = AnsibleModule(
        argument_spec = dict(
            dest    = dict(required=True, type="str"),
            parser  = dict(required=True, type="str", choices=list(PARSERS.keys())),
            actions = dict(required=True, type="list", elements="dict"),
        ),
    )

    result = _run(module.params)

    module.exit_json(**result, params=module.params)


if __name__ == "__main__":
    _main()
