#!/bin/bash

set -e

echo "Updating package repositories..."
apt-get update

echo "Installing git..."
apt-get install -y git

echo "Cloning GitHub repository to a temporary directory..."
git clone https://github.com/JowiAoun/Audio-Separate.git /tmp/api-service

echo "Installing necessary dependencies..."
pip install -r /tmp/api-service/requirements.txt

echo "Moving cloned directory to desired location..."
mv /tmp/api-service /api-service

echo "Cleaning up temporary directory..."
rm -rf /tmp/api-service

echo "Starting application..."
python3 -m uvicorn main:app --reload
