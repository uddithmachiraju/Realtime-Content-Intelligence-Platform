
# Allocate Elastic IP
resource "aws_eip" "webhook" {
    domain = "vpc"
    instance = var.instance_id
    depends_on = [] 
    tags = {
        Name         = "${var.project_name}-webhook-eip"
        Project      = var.project_name
        Domain       = var.domain_name
        Environment  = terraform.workspace
    }
}

