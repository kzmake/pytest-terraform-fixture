import os

import pytest
from python_terraform import Terraform

from pytest_terraform_fixture import NifcloudInstance

ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
REGION = os.environ.get("REGION")
SERVICE = os.environ.get("SERVICE")


@pytest.fixture(scope='session')
def terraform(terraform_dir):
    variables = {
        'access_key': ACCESS_KEY,
        'secret_key': SECRET_KEY,
        'region': REGION,
        'service': SERVICE
    }
    return Terraform(working_dir=terraform_dir, variables=variables)


@pytest.fixture(scope='function')
def instance_a_modfixutre(terraform):
    return NifcloudInstance.instance_a(terraform)


def test_terraform_fixture(terraform_dir, instance_a):
    print(terraform_dir, instance_a)
    assert True


def test_terraform_function(terraform_dir, instance_a_modfixutre):
    print(terraform_dir, instance_a_modfixutre)
    assert True
