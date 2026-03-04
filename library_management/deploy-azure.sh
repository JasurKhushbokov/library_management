#!/bin/bash
# Deploy Django Library Management System to Azure VM

echo "===== Azure Deployment Script ====="

# Variables - UPDATE THESE before running
AZURE_VM_IP="YOUR_VM_IP"
SSH_USER="azureuser"
PROJECT_NAME="library_management"

# Step 1: Build production image locally
echo "Step 1: Building Docker image..."
docker build -t library-app:latest .

# Step 2: Save image to tar file
echo "Step 2: Saving Docker image..."
docker save -o library-app.tar library-app:latest

# Step 3: Copy image to Azure VM
echo "Step 3: Copying image to Azure VM..."
scp library-app.tar ${SSH_USER}@${AZURE_VM_IP}:~/

# Step 4: SSH into VM and load image
echo "Step 4: Loading image on Azure VM..."
ssh ${SSH_USER}@${AZURE_VM_IP} "
    docker load -i library-app.tar
"

# Step 5: Copy deployment files
echo "Step 5: Copying deployment files..."
scp docker-compose.prod.yml ${SSH_USER}@${AZURE_VM_IP}:~/
scp nginx.conf ${SSH_USER}@${AZURE_VM_IP}:~/
scp .env ${SSH_USER}@${AZURE_VM_IP}:~/
scp -r media ${SSH_USER}@${AZURE_VM_IP}:~/

# Step 6: Run container on Azure VM
echo "Step 6: Starting container on Azure VM..."
ssh ${SSH_USER}@${AZURE_VM_IP} "
    docker-compose -f docker-compose.prod.yml up -d
"

echo "===== Deployment Complete! ====="
echo "Access your app at: http://${AZURE_VM_IP}"
