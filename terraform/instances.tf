resource "nifcloud_instance" "instance_a" {
  name                    = "hogehogea"
  image_id                = "${var.image_id["centos67"]}"
  key_name                = "${var.key_name}"
  instance_type           = "${var.instance_type}"
  description             = "pytest-terraform"
  availability_zone       = "${var.zone["east-11"]}"
  disable_api_termination = "false"
  ip_type                 = "none"
}

resource "nifcloud_instance" "instance_b" {
  name                    = "hogehogeb"
  image_id                = "${var.image_id["ubuntu1804"]}"
  key_name                = "${var.key_name}"
  instance_type           = "${var.instance_type}"
  description             = "pytest-terraform"
  availability_zone       = "${var.zone["east-11"]}"
  disable_api_termination = "false"
  ip_type                 = "none"
}
