locals {
    ami = var.os == "ubuntu" ? data.aws_ami_ids.ami.ids[0] : data.aws_ami_ids.ami_centos.ids[0]
    prefix = "bd"
    key_name = "${local.prefix}.pem"
}