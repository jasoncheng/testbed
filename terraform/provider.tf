terraform {
  required_providers {
    aws = {}
  }
}

provider "aws" {
  profile = var.aws_profile
  region = var.aws_region
}

data "aws_ami_ids" "ami" {
  owners      = ["self", "amazon", "099720109477"]
  filter {
    name   = "name"
    values = ["*ubuntu-focal-20.04-amd64-server-20211021*"]
  }
}

data "aws_ami_ids" "ami_centos" {
  owners      = ["self", "amazon", "125523088429"]
  filter {
    name   = "name"
    values = ["*CentOS*"]
  }
}