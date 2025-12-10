
# EC2 Module Outputs
output "instance_id" {
    description = "The ID of the EC2 instance"
    value       = module.EC2.instance_id
}

output "private_ip" {
    description = "The private IP address of the EC2 instance"
    value       = module.EC2.private_ip
}

output "public_ip" {
    description = "The public IP address of the EC2 instance"
    value       = module.EC2.public_ip
}

output "instance_arn" {
    description = "The ARN of the EC2 instance"
    value       = module.EC2.instance_arn
}


# IAM Module Outputs
output "role_arn" {
    description = "The ARN of the IAM role"
    value       = module.IAM.role_arn
}

output "role_name" {
    description = "The name of the IAM role"
    value       = module.IAM.role_name
}

# VPC Module Outputs
output "vpc_id" {
    description = "The ID of the VPC"
    value       = module.VPC.vpc_id
}

output "public_subnet_id" {
    description = "The ID of the public subnet"
    value       = module.VPC.public_subnet_id
}

output "security_group_id" {
    description = "The ID of the security group"
    value       = module.VPC.security_group_id
}

output "internet_gateway_id" {
    description = "The ID of the internet gateway"
    value       = module.VPC.internet_gateway_id
}

# Elastic IP Module Outputs
output "elastic_ip_address" {
    description = "The Elastic IP address"
    value       = module.elastic_ip.elastic_ip
}

output "elastic_ip_allocation_id" {
    description = "The Elastic IP allocation ID"
    value       = module.elastic_ip.allocation_id
}

output "elastic_ip_association_id" {
    description = "The Elastic IP association ID"
    value       = module.elastic_ip.association_id
}