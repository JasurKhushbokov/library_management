# Azure Deployment Instructions for Django Library Management System

## Prerequisites
- Azure VM (Ubuntu 20.04 or 22.04)
- SSH access to VM
- Docker installed on VM
- Domain name (optional)

---

## Step 1: Prepare Your Local Machine

### 1.1 Update .env file for production
```bash
# Edit .env file
nano .env
```

Update these values:
```
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-vm-ip
DB_HOST=db
DB_PASSWORD=strong-password-here
```

---

## Step 2: Build and Save Docker Image

### 2.1 Build the image
```bash
cd library_management
docker build -t library-app:latest .
```

### 2.2 Save image to file
```bash
docker save -o library-app.tar library-app:latest
```

---

## Step 3: Transfer to Azure VM

### 3.1 Copy files to Azure VM
```bash
# Replace with your VM IP and username
scp library-app.tar azureuser@YOUR_VM_IP:~/
scp docker-compose.prod.yml azureuser@YOUR_VM_IP:~/
scp -r media azureuser@YOUR_VM_IP:~/
```

---

## Step 4: Setup Azure VM

### 4.1 SSH into your VM
```bash
ssh azureuser@YOUR_VM_IP
```

### 4.2 Install Docker (if not installed)
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
```

### 4.3 Create .env file on VM
```bash
nano .env
```

Add these contents:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=strong-password
DB_HOST=db
DB_PORT=5432
```

---

## Step 5: Run on Azure VM

### 5.1 Load the Docker image
```bash
docker load -i library-app.tar
```

### 5.2 Start the containers
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 5.3 Check status
```bash
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f
```

---

## Step 6: Access Your Application

- **http://YOUR_VM_IP:8000** - Your application
- **http://YOUR_VM_IP:8000/admin/** - Admin panel

---

## Step 7: Configure Firewall (Optional)

```bash
sudo ufw allow 8000
sudo ufw allow 22
sudo ufw enable
```

---

## Quick Commands for Azure

```bash
# Start
docker-compose -f docker-compose.prod.yml start

# Stop
docker-compose -f docker-compose.prod.yml stop

# Restart
docker-compose -f docker-compose.prod.yml restart

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Update and redeploy
docker-compose -f docker-compose.prod.yml down
# Transfer new files, then:
docker-compose -f docker-compose.prod.yml up -d --build
```

---

## Troubleshooting

### Check if containers are running
```bash
docker ps
```

### Check logs
```bash
docker logs library_web
docker logs library_db
```

### Restart services
```bash
docker-compose -f docker-compose.prod.yml restart
```
