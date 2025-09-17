#!/bin/bash
set -e  # exit if any command fails

# Ensure ec2-user owns the project folder
sudo chown -R ec2-user:ec2-user /home/ec2-user/backend
cd /home/ec2-user/backend

# Go to project directory (adjust if needed)
cd /home/ec2-user/backend

# Ensure Python 3 and pip are installed
sudo yum update -y
sudo yum install -y python3 python3-pip

# Create venv if it doesn’t exist
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
