# Deployment Guide

## Server requirements

- Ubuntu 20.04 or Amazon Linux 2023
- 2 vCPU, 4GB RAM minimum
- Docker 24+
- Docker Compose v2

## First time setup on server

    sudo apt update && sudo apt install -y docker.io
    sudo systemctl enable docker && sudo systemctl start docker
    sudo usermod -aG docker $USER
    newgrp docker

    sudo mkdir -p /opt/devops-production-stack
    sudo chown $USER /opt/devops-production-stack
    git clone https://github.com/skaftab-in/devops-production-stack.git /opt/devops-production-stack
    cd /opt/devops-production-stack

    cat > .env << EOF
    POSTGRES_USER=appuser
    POSTGRES_PASSWORD=yourpassword
    POSTGRES_DB=appdb
    DATABASE_URL=postgresql://appuser:yourpassword@postgres:5432/appdb
    REDIS_HOST=redis
    EOF

    docker compose up -d

## Verify deployment

    docker compose ps
    curl http://localhost/health

## Restart strategy

All containers have restart: unless-stopped policy.
On server reboot, Docker daemon starts automatically and brings up all containers.

To manually restart:

    docker compose restart

To redeploy after code change:

    git pull origin main
    docker compose up -d --build

## Logs

    # All services
    docker compose logs -f

    # Specific service
    docker compose logs -f app
    docker compose logs -f nginx

## Firewall setup

    sudo ufw allow 22/tcp
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw enable

## fail2ban setup

    sudo apt install fail2ban
    sudo systemctl enable fail2ban
    sudo systemctl start fail2ban

Default config protects SSH automatically. To protect NGINX:

    sudo cat > /etc/fail2ban/jail.local << EOF
    [nginx-http-auth]
    enabled = true
    port = http,https
    logpath = /var/log/nginx/error.log
    EOF

    sudo systemctl restart fail2ban
