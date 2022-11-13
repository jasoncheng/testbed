resource "tls_private_key" "key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "aws_key" {
  key_name   = local.prefix
  public_key = tls_private_key.key.public_key_openssh
  tags       = var.tags
}

resource "local_file" "publicKey" {
  filename = "${local.prefix}.pub"
  content = tls_private_key.key.public_key_openssh
  file_permission = 0600
}

resource "local_file" "pemFile" {
  filename = "${local.key_name}"
  content = tls_private_key.key.private_key_pem
  file_permission = 0600
}