import os

import pytest
from dotenv import load_dotenv, find_dotenv
from python_terraform import Terraform

load_dotenv(find_dotenv())

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


def test_terraform_fixture(terraform_dir, instance_a):
    print(terraform_dir, instance_a)
