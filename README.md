pytest-terraform-fixture
================

🚀 Description
-----------

`--terraform-dir` で指定したディレクトリにある Terraform で作成されるリソースを動的に pytest の fixture として自動で定義してくれる pluginです

🚀 Install
-------

github から引っ張ってきて。

```sh
pip install pytest-terraform-fixture
```


🚀 Usage
-----

Terraform で作成したいリソースを記述する (ここでは `instance_a` のリソースを定義したとする)
```terraform
provider "nifcloud" {
  access_key = "xxxxx"
  secret_key = "yyyyy"
  region     = "jp-east-1"
  endpoint   = "jp-east-1.conputing.api.nifcloud.com"
}

resource "nifcloud_instance" "instance_a" {
  instance_id             = "hogehogea"
  image_id                = "89"
  key_name                = "ssh_key"
  instance_type           = "large"
  description             = "pytest-terraform"
  availability_zone       = "east-11"
  disable_api_termination = "false"
  ip_type                 = "none"
}
```

pytest で `instance_a` をリソースを使うテストを作成します (自動的に `instance_a` をfixutreとして定義してくれる)

```python
import pytest
from python_terraform import Terraform

def test_terraform_fixture(instance_a):
    # instance_a を作成するテスト
    assert True
```

後は、 `*.tf` のディレクトリを指定して実行
```sh
pytest --terraform-dir={実施したい *.tf をもつディレクトリ}
```

🚀 Requirements
------------

このプロジェクトを実行するには以下が必要です:

* [python](https://www.python.org/) 3.4.+
* [terraform](https://www.terraform.io) 0.11.+

🚀 Contributing
------------

PR歓迎してます

🚀 Support and Migration
---------------------

特に無し

🚀 License
-------

- [MIT License](http://petitviolet.mit-license.org/)
