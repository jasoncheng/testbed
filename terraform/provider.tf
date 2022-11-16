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
  owners      = ["self", "amazon", "125523088429", "374168611083"]
  filter {
    name   = "name"
    values = ["ap-northeast-1 image for x86_64 CentOS_7"]
    # values = ["*centos7-hvm-x86_64-202202282101*"]
  }
}