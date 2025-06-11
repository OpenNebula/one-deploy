# -*- coding: utf-8 -*-
# Copyright: OpenNebula Project, OpenNebula Systems
# Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

DOCUMENTATION = r"""
module: augeas
short_description: Manage configuration files using Augeas lenses
version_added: "1.0"
description:
  - Manage configuration files using Augeas lenses via python-augeas.
options:
  lens:
    description:
      - The Augeas lens to use.
    type: str
    required: true
  file:
    description:
      - The configuration file to manage.
    type: str
    required: true
  command:
    description:
      - The Augeas command to run. Currently only 'set' is supported.
    type: str
    choices: [ set ]
    required: true
  path:
    description:
      - The Augeas path to operate on (relative to the lens root).
    type: str
    required: true
  value:
    description:
      - The value to set at the given path (required for 'set').
    type: str
    required: false
author:
  - Balazs Nemeth (@balazsbme)
"""

EXAMPLES = r"""
- name: Set DEFAULT_CDROM_DEVICE_PREFIX
  augeas:
    lens: oned
    file: /etc/one/oned.conf
    command: set
    path: DEFAULT_CDROM_DEVICE_PREFIX
    value: '"/dev/sr0"'

- name: Configure KVM defaults for RAW
  augeas:
    lens: oned
    file: /etc/one/vmm_exec/vmm_exec_kvm.conf
    command: set
    path: RAW
    value: '"some raw value"'
"""

RETURN = r"""
changed:
    description: Whether any change was made.
    type: bool
    returned: always
old_value:
    description: The previous value at the specified path (if any).
    type: str
    returned: always
new_value:
    description: The value set at the specified path (if any).
    type: str
    returned: always
"""

from ansible.module_utils.basic import AnsibleModule

try:
    import augeas
    HAS_AUGEAS = True
except ImportError:
    HAS_AUGEAS = False

def run_augeas_set(module, lens, file, path, value):
    aug = augeas.Augeas(flags=augeas.Augeas.NO_MODL_AUTOLOAD)
    # Load the lens and file
    aug.set("/augeas/load/{}/lens".format(lens), lens)
    aug.set("/augeas/load/{}/incl".format(lens), file)
    aug.load()
    # Compose the full Augeas path
    root = "/files{}".format(file)
    full_path = root + "/" + path
    old_value = aug.get(full_path)
    changed = old_value != value
    if not module.check_mode and changed:
        aug.set(full_path, value)
        aug.save()
    # Re-read after save (or for check mode)
    new_value = value if changed else old_value
    return changed, old_value, new_value

def main():
    module_args = dict(
        lens=dict(type='str', required=True),
        file=dict(type='str', required=True),
        command=dict(type='str', required=True, choices=['set']),
        path=dict(type='str', required=True),
        value=dict(type='str', required=False, default=None),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if not HAS_AUGEAS:
        module.fail_json(msg="The python-augeas package is required for this module.")

    lens = module.params['lens']
    file = module.params['file']
    command = module.params['command']
    path = module.params['path']
    value = module.params['value']

    if command == 'set':
        if value is None:
            module.fail_json(msg="'value' is required for command 'set'.")
        try:
            changed, old_value, new_value = run_augeas_set(module, lens, file, path, value)
        except Exception as e:
            module.fail_json(msg="Augeas set operation failed: {}".format(e))
        module.exit_json(changed=changed, old_value=old_value, new_value=new_value)
    else:
        module.fail_json(msg="Unsupported command: {}".format(command))

if __name__ == '__main__':
    main()