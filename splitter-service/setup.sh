#!/bin/bash

set -e

echo "Updating package repositories..."
apt-get update

echo "Installing git..."
apt-get install -y git

echo "Cloning GitHub repository to a temporary directory..."
git clone https://github.com/JowiAoun/Audio-Separate.git /tmp/splitter-service

echo "Installing necessary dependencies..."
pip install -r /tmp/splitter-service/requirements.txt

echo "Moving cloned directory to desired location..."
mv /tmp/splitter-service /splitter-service

echo "Cleaning up temporary directory..."
rm -rf /tmp/splitter-service

echo "Starting application..."
python /splitter-service/main.py
