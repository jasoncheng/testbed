resource "aws_security_group" "sg-all" {
  vpc_id = module.vpc.vpc_id
  name   = "${local.prefix}-sg"
  ingress = [
    {
      from_port        = 0
      to_port          = 65535
      protocol         = "all"
      cidr_blocks      = var.ip_white_list
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      security_groups  = []
      description      = "all public"
      self             = false
    },
    {
      from_port        = 0
      to_port          = 65535
      protocol         = "tcp"
      cidr_blocks      = module.vpc.public_subnets_cidr_blocks
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      security_groups  = []
      description      = "internal"
      self             = false
    },
    # {
    #   from_port        = 9000
    #   to_port          = 9000
    #   protocol         = "tcp"
    #   cidr_blocks      = ["0.0.0.0/0"]
    #   ipv6_cidr_blocks = ["::0/0"]
    #   prefix_list_ids  = []
    #   security_groups  = []
    #   description      = "internal"
    #   self             = false
    # },
    # {
    #   from_port        = 0
    #   to_port          = 65535
    #   protocol         = "tcp"
    #   cidr_blocks      = ["3.112.218.236/32", "54.250.8.78/32"]
    #   ipv6_cidr_blocks = []
    #   prefix_list_ids  = []
    #   security_groups  = []
    #   description      = "internal"
    #   self             = false
    # }
  ]

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "all"
    cidr_blocks      = ["0.0.0.0/0"]
    description      = "outbound"
    ipv6_cidr_blocks = ["::/0"]
    prefix_list_ids  = []
    security_groups  = []
    self             = false
  }
  tags = merge(
    var.tags,
    { Name = "${local.prefix}-sg" }
  )
}