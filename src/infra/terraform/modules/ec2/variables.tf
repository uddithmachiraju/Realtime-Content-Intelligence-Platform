# Variables for EC2 module 

variable "instance_type" {
    description     = "EC2 Instance Type"
    type            = string
}

variable "ami" {
    description     = "AMI ID for the EC2 instance"
    type            = string
}

variable "subnet_id" {
    description     = "Subnet ID where the EC2 instance will be launched"
    type            = string
}

variable "vpc_security_group_ids" {
    description     = "List of VPC Security Group IDs to associate with the EC2 instance"
    type            = list(string)
    default         = []
}

variable "iam_instance_profile_name" {
    description     = "IAM Instance Profile name to attach to the EC2 instance"
    type            = string
    default         = null
}

variable "key_name" {
    description     = "Key pair name to access the EC2 instance"
    type            = string
}

variable "instance_name" {
    description     = "Name tag for the EC2 instance"
    type            = string
}

variable "root_volume_size" {
    description     = "Size of the root EBS volume in GB"
    type            = number
}

variable "environment" {
    description     = "Deployment environment (e.g., dev, staging, prod)"
    type            = string
}

variable "project_name" {
    description     = "Name of the project"
    type            = string
}

variable "application_repo_url" {
    description     = "URL of the application repository to clone"
    type            = string
}