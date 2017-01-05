#!/usr/bin/env python2

from ansible.module_utils.basic import AnsibleModule


def is_package_installed(module, package_name):
    cmd = ['pipsi', 'list']
    search = '  Package "{}":\n'.format(package_name)
    _, output, _ = module.run_command(cmd, check_rc=False)
    return search in output


def install_package(module, package_name):
    if is_package_installed(module, package_name):
        module.exit_json(
            changed=False,
            msg='package already installed'
        )

    cmd = ['pipsi', 'install', package_name]
    module.run_command(cmd, check_rc=True)

    module.exit_json(
        changed=True,
        msg='installed package'
    )


def remove_package(module, package_name):
    if not is_package_installed(module, package_name):
        module.exit_json(
            changed=False,
            msg='package not installed'
        )

    cmd = ['pipsi', 'uninstall', '--yes', package_name]
    module.run_command(cmd, check_rc=True)

    module.exit_json(
        changed=True,
        msg='removed package'
    )


def main():
    module = AnsibleModule(
        argument_spec={
            'name': {
                'required': True,
            },
            'state': {
                'default': 'present',
                'choices': ['present', 'absent'],
            }
        }
    )
    params = module.params

    if params['state'] == 'present':
        install_package(module, params['name'])
    elif params['state'] == 'absent':
        remove_package(module, params['name'])


if __name__ == '__main__':
    main()
