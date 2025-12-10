
variable "vpc_cidr" {
  description = "CIDR block for VPC"
    type        = string
}

variable "public_subnet_cidr" {
    description = "CIDR block for public subnet"
    type        = string
}

variable "project_name" {
    description = "Name of the project"
    type        = string
}

variable "availability_zone" {
    description = "Availability zone for the subnet"
    type        = string
}