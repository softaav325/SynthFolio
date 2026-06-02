# 🚀 Portfolio Deployment Guide for VPS (Ubuntu)

This project is prepared for deployment using Docker and Nginx.

## 1. Server Preparation (VPS)

### Install Docker and Docker Compose
Run the following commands on your server:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose (V2)
sudo apt install -y docker-compose-plugin
```

## 2. Project Deployment

### Cloning and Configuration
```bash
# Clone your repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Create environment variables file
cp .env.example .env
nano .env  # Edit SECRET_KEY and ADMIN_EMAIL
```

### Running Containers
```bash
# Build and run in background mode
sudo docker compose up -d --build
```

## 3. Domain and HTTPS Configuration

### Domain Binding
Point the **A record** of your domain (e.g., `portfolio.example.com`) to your VPS IP address.

### SSL Certificate Installation (Let's Encrypt)
Use Certbot to obtain a free SSL certificate:

```bash
# Install Certbot
sudo apt install -y certbot

# Obtain certificate (replace domain.com with yours)
sudo certbot certonly --standalone -d portfolio.example.com
```

### Configuring HTTPS in Nginx
Edit `nginx.conf` to add redirection from port 80 to 443 and specify the paths to the certificates:

```nginx
server {
    listen 80;
    server_name portfolio.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name portfolio.example.com;

    ssl_certificate /etc/letsencrypt/live/portfolio.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/portfolio.example.com/privkey.pem;
    
    # Other settings from nginx.conf...
}
```
Then restart Nginx: `sudo docker compose restart nginx`

## 4. Useful Commands

- **View logs:** `sudo docker compose logs -f`
- **Restart after code update:** 
  ```bash
  git pull
  sudo docker compose up -d --build
  ```
- **Stop project:** `sudo docker compose down`
