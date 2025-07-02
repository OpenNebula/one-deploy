# -*- coding: utf-8 -*-
# Copyright: OpenNebula Project, OpenNebula Systems
# Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

DOCUMENTATION = r"""
module: augtool
short_description: Generic module to run augtool
description:
  - This module allows for running aritrary augtool scripts.
options:
  cmd:
    description:
      - Commands passed to augtool on stdin in a form of a script.
    type: str
author:
  - Michal Opala (@sk4zuzu)
"""

EXAMPLES = r"""
- name: Ensure augtool is installed (no need for python bindings)
  ansible.builtin.package:
    name: augeas-tools

- name: Update oned.conf with the Oned lens
  opennebula.deploy.augtool:
    cmd: |
      set /augeas/load/Oned/lens Oned.lns
      set /augeas/load/Oned/incl[0] /etc/one/oned.conf
      load
      set /files/etc/one/oned.conf/PORT {{ _oned_port }}
      set /files/etc/one/oned.conf/DB/BACKEND '"mysql"'
      save
      errors
  vars:
    _oned_port: 1234
"""

RETURN = r"""
files:
    description: List of files included in the idempotency management.
    type: list
    elements: str
    returned: always
stdout:
    description: Unaltered output of the augtool (may contain detailed error messages).
    type: str
    returned: always
stderr:
    description: Unaltered error output of the augtool (or Python exceptions).
    type: str
    returned: always
params:
    description: Input parameters of the module (for reference).
    type: dict
    returned: always
"""


from ansible.module_utils.basic import AnsibleModule

import hashlib
import re
import subprocess
import traceback


def _run_augtool(cmds):
    p = subprocess.run(["augtool", "--noload", "--noautoload"],
                       capture_output=True,
                       input="\n".join(cmds).encode("utf-8"))
    return dict(
        stdout = p.stdout.decode("utf-8"),
        stderr = p.stderr.decode("utf-8"),
        failed = p.returncode != 0,
    )


def _extract_files(params):
    return set(
        line.split()[-1]
        for line in params.get("cmd").splitlines()
        if re.match(r"^\s*set\s+/augeas/load/[^/]+/incl", line)
    )


def _compute_cksums(paths):
    def _cksum(path):
        with open(path, "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()
    return set(
        _cksum(path)
        for path in paths
    )


def _apply_commands(params):
    files = _extract_files(params)

    before = _compute_cksums(files)

    cmds = params.get("cmd").splitlines()

    result = _run_augtool(cmds)

    after = _compute_cksums(files)

    return dict(
        failed  = result.get("failed"),
        changed = before != after,
        files   = list(files),
        stdout  = result.get("stdout"),
        stderr  = result.get("stderr"),
    )


def _main():
    module = AnsibleModule(
        argument_spec = dict(
            cmd = dict(required=True, type="str"),
        ),
    )

    try:
        result  = _apply_commands(module.params)
        failed  = result.get("failed")
        changed = result.get("changed")
        files   = result.get("files")
        stdout  = result.get("stdout")
        stderr  = result.get("stderr")
    except:
        failed  = True
        changed = False
        files   = []
        stdout  = ""
        stderr  = traceback.format_exc()

    module.exit_json(
        failed  = failed,
        changed = changed,
        files   = files,
        stdout  = stdout,
        stderr  = stderr,
        params  = module.params,
    )


if __name__ == "__main__":
    _main()
