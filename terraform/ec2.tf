resource "aws_instance" "instances" {
  count         = var.instance_count + 1
  ami           = local.ami
  instance_type = count.index == 0 ? var.instance_type_first : var.instance_type
  key_name      = aws_key_pair.aws_key.key_name
  subnet_id     = module.vpc.public_subnets[0]
  monitoring    = false
  root_block_device {
    volume_size = var.instance_ebs_size
    tags = merge(
      var.tags,
      { Name = "${local.prefix}-wrk${count.index + 1}-ebs" }
    )
  }
  vpc_security_group_ids = [aws_security_group.sg-all.id]
  tags = merge(
    var.tags,
    { Name = "${local.prefix}${count.index + 1}" }
  )

}

resource "aws_ebs_volume" "ebs" {
  count             = var.instance_count + 1
  availability_zone = data.aws_availability_zones.available.names[0]
  size              = var.instance_extra_ebs_size
}

resource "aws_volume_attachment" "ebs_att" {
  count        = var.instance_count + 1
  device_name  = "/dev/sdh"
  volume_id    = aws_ebs_volume.ebs[count.index].id
  instance_id  = aws_instance.instances[count.index].id
  force_detach = true
}
