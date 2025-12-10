
provider "aws" {
    region = var.aws_region
}

module "IAM" {
    source = "./modules/iam"

    role_name    = var.iam_role_name
    instance_profile_name = "${var.project_name}-instance-profile"
    environment  = var.environment
    project_name = var.project_name
}

module "VPC" {
    source = "./modules/vpc"

    vpc_cidr            = var.vpc_cidr
    public_subnet_cidr  = var.public_subnet_cidr
    availability_zone   = var.availability_zone
    project_name        = var.project_name
}

module "EC2" {
    source = "./modules/ec2"

    instance_type = var.instance_type
    instance_name = var.instance_name
    subnet_id     = module.VPC.public_subnet_id
    vpc_security_group_ids = [module.VPC.security_group_id]
    root_volume_size = var.root_volume_size
    iam_instance_profile_name = module.IAM.instance_profile_name
    ami           = var.ami
    key_name      = var.key_name
    project_name = var.project_name
    environment  = var.environment
}