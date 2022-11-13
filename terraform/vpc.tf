data "aws_availability_zones" "available" {
  state = "available"
}
module "vpc" {
  source          = "terraform-aws-modules/vpc/aws"
  name            = "${local.prefix}-vpc"
  cidr            = "${var.vpc_cidr}"
  public_subnets  = var.public_subnets
  private_subnets = var.private_subnets
  # azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  azs = ["${data.aws_availability_zones.available.names[0]}", "${data.aws_availability_zones.available.names[1]}"]
}
