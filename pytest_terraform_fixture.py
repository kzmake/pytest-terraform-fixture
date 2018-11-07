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


def inject_terraform_fixture(resource, name):
    target = f"{resource}.{name}"
    for scope in ['', 'function', 'class', 'module', 'session']:
        if scope == '':
            scope = 'function'
            suffix = ''
        else:
            suffix = '_{}'.format(scope)

        globals()[name + suffix] = generate_terraform_fixture(target, scope=scope)


inject_terraform_fixture('nifcloud_instance', 'instance_a')
inject_terraform_fixture('nifcloud_instance', 'instance_b')
