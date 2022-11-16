# Create Ansible Files

resource "local_file" "ansible_inventory" {
  depends_on = [
    aws_instance.instances
  ]
  content = templatefile("ansible.inventory.ini.j2", {
    all           = aws_instance.instances.*.public_ip,
    prefix        = local.prefix,
    other_servers = var.other_servers,
    size          = length(aws_instance.instances.*.public_ip) + 1,
    os            = var.os
  })
  filename = "../ansible/inventory/${local.prefix}.inv"
}

resource "local_file" "ansible_cfg" {
  depends_on = [
    aws_instance.instances
  ]
  content = templatefile("ansible.cfg.ini.j2", {
    key_name  = "${local.key_name}",
    inventory = "${local.prefix}.inv",
    os        = var.os
  })
  filename = "../ansible/ansible.cfg"
}

resource "local_file" "ansible_groups_vars" {
  depends_on = [
    aws_instance.instances
  ]
  content = templatefile("ansible.group_vars.yml.j2", {
    os        = var.os
  })
  filename = "../ansible/group_vars/${local.prefix}.yml"
}
