#!/usr/bin/env python2

from ansible.module_utils.basic import AnsibleModule


def is_package_installed(module, package_name):
    cmd = ['pipsi', 'list']
    search = '  Package "{}":\n'.format(package_name)
    _, output, _ = module.run_command(cmd, check_rc=False)
    return search in output


def install_package(module, package_name, python):
    if is_package_installed(module, package_name):
        module.exit_json(
            changed=False,
            msg='package already installed'
        )

    cmd = ['pipsi', 'install', '--python', python, package_name]

    module.run_command(cmd, check_rc=True)
    module.exit_json(
        changed=True,
        msg='installed package'
    )


def update_package(module, package_name, python):
    if not is_package_installed(module, package_name):
        install_package(module, package_name, python)

    else:
        cmd = ['pipsi', 'upgrade', package_name]
        rc, out, _ = module.run_command(cmd)
        if rc and 'up-to-date' in out:
            module.exit_json(
                changed=False,
                msg='Package up to date'
            )
        elif not rc:
            module.exit_json(
                changed=True,
                msg='upgraded package'
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
                'choices': ['present', 'absent', 'latest'],
            },
            'python': {
                'default': ''
            }
        }
    )
    params = module.params

    if params['state'] == 'present':
        install_package(module, params['name'], params['python'])
    elif params['state'] == 'latest':
        update_package(module, params['name'], params['python'])
    elif params['state'] == 'absent':
        remove_package(module, params['name'])


if __name__ == '__main__':
    main()
