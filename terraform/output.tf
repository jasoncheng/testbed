output "publicIP" {
  value = ["${aws_instance.instances.*.public_ip}"]
}