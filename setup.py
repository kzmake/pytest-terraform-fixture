import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


required = [
    "pytest",
    "dotted",
    "python-terraform",
    "pyhcl"
]

setup(
    name='pytest-terraform-fixture',
    version='0.1.2',
    author='Kazuki Iwata',
    author_email='kazu.0516.k0n0f@gmail.com',
    maintainer='Kazuki Iwata',
    maintainer_email='kazu.0516.k0n0f@gmail.com',
    license='MIT',
    url='https://github.com/kzmake/pytest-terraform-fixture',
    description='generate terraform resources to use with pytest',
    long_description=read('README.md'),
    py_modules=['pytest_terraform_fixture'],
    python_requires='>=3.4',
    install_requires=required,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'pterraform-fixture = pytest_terraform_fixture',
        ],
    },
)
