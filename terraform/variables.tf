variable "aws_profile" {
  type = string
  default = "default"
}

variable "aws_region" {
  type = string
  default = "ap-northeast-1"
}

variable "instance_type_first" {
  type    = string
  default = "t3.small"
}
variable "instance_type" {
  type    = string
  default = "t3.small"
}

variable "instance_count" {
  default = 2
}

variable "instance_ebs_size" {
  default = 24
}

variable "instance_extra_ebs_size" {
  default = 24
}

variable "tags" {
  type = map(any)
  default = {
    Author = "Jason.SC.Cheng"
    Team = "COD"
    terraform = "true"
  }
}

variable "ip_white_list" {
  type = list(any)
  default = [
    "0.0.0.0/0"
  ]
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "public_subnets" {
  default = [
    "10.0.0.0/26", "10.0.0.64/26"

  ]
}

variable "private_subnets" {
  default = [
    "10.0.0.128/26", "10.0.0.192/26"
  ]
}

variable "other_servers" {
  type = map(any)
  default = {
  }
}