import glob
import os
import re
from collections import defaultdict

import hcl
import pytest
from dotted.utils import dot
from python_terraform import Terraform


def pytest_addoption(parser):
    """--terraform-dirの任意オプション"""
    parser.addoption('--terraform-dir', action='store', default='',
                     help='testing environment: active or standby')


@pytest.fixture(scope='session', autouse=True)
def terraform_dir(request):
    """terraform-dirオプション取得用fixture"""
    terraform_dir = request.config.getoption('--terraform-dir')
    # TODO pytest args の取り出し方がわからなかったので暫定的に env へセット
    os.putenv('TERRAFROM_DIR', terraform_dir)
    return terraform_dir


@pytest.fixture(scope='session')
def terraform(terraform_dir):
    return Terraform(working_dir=terraform_dir)


def generate_terraform_fixture(target, scope='function'):
    @pytest.fixture(scope=scope)
    def terraform_fixture(terraform):
        print('terraform_fixture: target={}'.format(target))
        terraform.init()
        terraform.apply(skip_plan=True, target=target)
        code_, out, err_ = terraform.cmd('show')
        return out

    return terraform_fixture


def generate_terraform_function(target):
    def terraform_function(terraform):
        print('terraform_function: target={}'.format(target))
        terraform.init()
        terraform.apply(skip_plan=True, target=target)
        code_, out, err_ = terraform.cmd('show')
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


def pytest_cmdline_preparse(config, args):
    # TODO: どうにかしたい
    dir = ''
    for arg in args:
        m = re.match(r'--terraform-dir=(.*)', arg)
        if m:
            dir = m.groups()[0]

    # --terraform-dir で指定されたディレクトリから *.tf を取得
    tf_files = glob.glob('{terraform_dir}/*.tf'.format(terraform_dir=dir))

    # --terraform-dir で指定されたディレクトリから resource "hogehoge" "fugafuga" {} の定義を取り出す
    resources = defaultdict(lambda: [])
    for tf_file in tf_files:
        # hcl で記述されている .tf を開く
        with open(tf_file, 'r') as f:
            obj = dot(hcl.load(f))

        # resource セクションのみ処理
        if 'resource' in list(obj.keys()):
            terraform_resource = obj.resource
            for resource_key, resource in terraform_resource.items():
                for name, param in resource.items():
                    resources[resource_key].append(name)

    for resource, names in resources.items():
        print(resource, names)
        for name in names:
            inject_terraform_fixture(resource, name)

        inject_terraform_class(resource, names)
