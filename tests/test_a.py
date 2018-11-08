import os
import pytest
import re
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
def mod_instance_a(terraform):
    return NifcloudInstance.instance_a(terraform)


def test_terraform_fixture_instance_a(instance_a):
    """Fixture instance_a"""
    assert re.match(r'i-[0-9a-z]{8}', instance_a['id'])


def test_terraform_fixture_instance_b(instance_b):
    """Fixture instance_b"""
    assert re.match(r'i-[0-9a-z]{8}', instance_b['id'])


def test_terraform_fixture_instance_a_scope_function(instance_a_function):
    """Fixture instance_a scope=function"""
    assert re.match(r'i-[0-9a-z]{8}', instance_a_function['id'])


def test_terraform_fixture_instance_a_scope_class(instance_a_class):
    """Fixture instance_a scope=class"""
    assert re.match(r'i-[0-9a-z]{8}', instance_a_class['id'])


def test_terraform_fixture_instance_a_scope_module(instance_a_module):
    """Fixture instance_a scope=module"""
    assert re.match(r'i-[0-9a-z]{8}', instance_a_module['id'])


def test_terraform_fixture_instance_a_scope_session(instance_a_session):
    """Fixture instance_a scope=module"""
    assert re.match(r'i-[0-9a-z]{8}', instance_a_session['id'])


def test_terraform_class_staticmethod(terraform):
    """Class.staticmethod"""
    assert re.match(r'i-[0-9a-z]{8}', NifcloudInstance.instance_a(terraform)['id'])
