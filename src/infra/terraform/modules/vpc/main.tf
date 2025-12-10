

# VPC
resource "aws_vpc" "main" {
    cidr_block = var.vpc_cidr
    enable_dns_hostnames = true 
    enable_dns_support = true

    tags = {
      "Name" = "${var.project_name}-vpc"
    } 
}

# Internet gateway
resource "aws_internet_gateway" "igw" {
    vpc_id = aws_vpc.main.id

    tags = {
      "Name" = "${var.project_name}-igw"
    } 
}


# Public Subnet
resource "aws_subnet" "public" {
    vpc_id            = aws_vpc.main.id
    cidr_block        = var.public_subnet_cidr
    availability_zone = var.availability_zone
    map_public_ip_on_launch = true

    tags = {
      "Name" = "${var.project_name}-public-subnet"
    } 
} 

# Route Table for Public Subnet
resource "aws_route_table" "public_rt" {
    vpc_id = aws_vpc.main.id

    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.igw.id
    }

    tags = {
      "Name" = "${var.project_name}-public-rt"
    } 
}

# Associate Route Table with Public Subnet
resource "aws_route_table_association" "public_rt_assoc" {
    subnet_id      = aws_subnet.public.id
    route_table_id = aws_route_table.public_rt.id
}

# Security Group allowing inbound SSH and HTTP
resource "aws_security_group" "main_sg" {
    name        = "${var.project_name}-sg"
    description = "Main security group"
    vpc_id      = aws_vpc.main.id

    ingress {
        from_port = 80
        to_port   = 80
        protocol  = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
        description = "Allow HTTP"
    }

    ingress {
        from_port = 443
        to_port   = 443
        protocol  = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
        description = "Allow HTTPS"
    }

    ingress {
        from_port = 22
        to_port   = 22
        protocol  = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
        description = "Allow SSH"
    }

    egress {
        from_port = 0
        to_port   = 0
        protocol  = "-1"
        cidr_blocks = ["0.0.0.0/0"]
        description = "Allow all outbound traffic"
    }

    tags = {
      "Name" = "${var.project_name}-sg"
    } 
}