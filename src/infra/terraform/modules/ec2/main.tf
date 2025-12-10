
resource "aws_instance" "WebSub" {
  ami                         = var.ami
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = var.vpc_security_group_ids
  iam_instance_profile        = var.iam_instance_profile_name
  key_name                    = var.key_name

  # Attach the IAM role to the instance

  root_block_device {
    volume_type             = "gp3"
    volume_size             = var.root_volume_size
    delete_on_termination   = true
  }

  tags = {
    Name        = var.instance_name
    Environment = var.environment
    Project     = var.project_name
  }
  
}