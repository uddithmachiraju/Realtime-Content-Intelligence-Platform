#!/bin/bash
# This script will configure the awscli tool with provided AWS credentials and default region with no arguments needed.

# set -euo pipefails

# echo "Installing dependecies..."

# poetry lock && poetry install 
# python -m pip install --upgrade pip setuptools wheel --break-system-packages
# cd .devcontainer && pip install -r requirements.txt --break-system-packages

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI is not installed. Please install it."
    exit 1
fi 

# Load .env file if it exists
if [ -f ../.env ]; then
    export $(grep -v '^#' ../.env | xargs)
else
    echo ".env file not found. Please create one with AWS credentials."
    exit 1
fi

# Set AWS credentials and default region
aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
aws configure set default.region "$AWS_DEFAULT_REGION"