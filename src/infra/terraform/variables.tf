# AWS Region variable
variable "aws_region" {
    description     = "AWS region to deploy resources in"
    type            = string
}

variable "environment" {
    description     = "The environment for resource deployment (e.g., dev, staging, prod)"
    type            = string
}

variable "project_name" {
    description     = "The name of the project for resource tagging"
    type            = string
}

# Variables for EC2 module
variable "instance_name" {
    description     = "Name of the EC2 instance"
    type            = string
}

variable "instance_type" {
    description     = "EC2 Instance Type"
    type            = string
    default         = "t2.micro"
}

variable "ami" {
    description     = "AMI ID for the EC2 instance"
    type            = string
}

variable "key_name" {
    description     = "Key pair name for the EC2 instance"
    type            = string
}

variable "root_volume_size" {
    description     = "Size of the root EBS volume in GB"
    type            = number
}

# Variable for IAM Role name
variable "iam_role_name" {
    description     = "IAM Role name to attach to the EC2 instance"
    type            = string
}

# Variables for VPC module
variable "vpc_cidr" {
    description = "CIDR block for VPC"
    type        = string
}

variable "public_subnet_cidr" {
    description = "CIDR block for public subnet"
    type        = string
}

variable "availability_zone" {
    description = "Availability zone for the subnet"
    type        = string
}