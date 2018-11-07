variable "access_key" {}
variable "secret_key" {}
variable "region" {}
variable "service" {}

variable "zone" {
  type = "map"

  default = {
    east-11 = "east-11"
    east-12 = "east-12"
    west-11 = "west-11"
  }
}

variable "image_id" {
  type = "map"

  default = {
    centos67   = "89"
    ubuntu1804 = "168"
  }
}

variable "instance_type" {
  default = "small"
}

variable "key_name" {
  default = "itsshkey"
}
