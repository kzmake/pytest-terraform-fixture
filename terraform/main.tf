provider "nifcloud" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region     = "${var.region}"
  endpoint   = "${var.region}.${var.service}.api.nifcloud.com"
}
