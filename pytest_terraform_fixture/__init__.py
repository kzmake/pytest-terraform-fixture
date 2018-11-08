import re

import pytest
from python_terraform import Terraform


def pytest_addoption(parser):
    """--terraform-dirの任意オプション"""
    parser.addoption('--terraform-dir', action='store', default='',
                     help='testing environment: active or standby')


@pytest.fixture(scope='session')
def terraform_dir(request):
    """terraform-dirオプション取得用fixture"""
    terraform_dir = request.config.getoption('--terraform-dir')
    return terraform_dir


@pytest.fixture(scope='session')
def terraform(terraform_dir):
    return Terraform(working_dir=terraform_dir)


def generate_terraform_fixture(target, scope='function'):
    @pytest.fixture(scope=scope)
    def terraform_fixture(terraform):
        print('terraform_fixture: target={}'.format(target))
        terraform.init()
        code, out, err = terraform.apply(skip_plan=True, target=target)
        print(code, out, err)
        code, out, err = terraform.cmd('show')
        print(code, out, err)
        return out

    return terraform_fixture


def generate_terraform_function(target):
    def terraform_function(terraform):
        print('terraform_function: target={}'.format(target))
        terraform.init()
        code, out, err = terraform.apply(skip_plan=True, target=target)
        print(code, out, err)
        code, out, err = terraform.cmd('show')
        print(code, out, err)
        return out

    return terraform_function


def inject_terraform_fixture(resource, name):
    # terraform 用に target 生成
    target = f"{resource}.{name}"

    # name から動的に fixture 作成
    for scope in ['', 'function', 'class', 'module', 'session']:
        if scope == '':
            scope = 'function'
            suffix = ''
        else:
            suffix = '_{}'.format(scope)
        globals()[name + suffix] = generate_terraform_fixture(target, scope=scope)


def inject_terraform_class(resource, names):
    # staticmethod
    staticmethods = dict()
    for name in names:
        # terraform 用に target 生成
        target = f"{resource}.{name}"
        staticmethods[name] = staticmethod(generate_terraform_function(target))

    # スネークケースからキャメルケースに変更
    clazz = re.sub("_(.)", lambda x: x.group(1).upper(), resource.capitalize())

    # resource から動的に class 作成
    globals()[clazz] = type('class', (object,), staticmethods)


inject_terraform_fixture('nifcloud_instance', 'instance_a')
inject_terraform_fixture('nifcloud_instance', 'instance_b')
inject_terraform_class('nifcloud_instance', ['instance_a', 'instance_b'])

print(globals())
