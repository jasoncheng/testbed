locals {
    ami = data.aws_ami_ids.ami.ids[0]
    prefix = "bd"
    key_name = "${local.prefix}.pem"
}