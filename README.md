# devops-production-stack

A production-grade deployment of a FastAPI application with PostgreSQL, Redis, and NGINX reverse proxy. Built as part of a DevOps engineering assignment.

## Stack

- FastAPI - REST API backend
- PostgreSQL - persistent storage
- Redis - caching layer
- NGINX - reverse proxy with rate limiting and security headers
- Docker Compose - container orchestration
- GitHub Actions - CI/CD pipeline

## Architecture

    Internet
        |
      NGINX (port 80/443)
        |
      FastAPI (port 8000, internal only)
       /    \
PostgreSQL  Redis
(port 5432) (port 6379)

GitHub push to main -> GitHub Actions -> SSH -> VPS -> docker compose up

## Project Structure

    devops-production-stack/
    app/
        main.py
        requirements.txt
        Dockerfile
    nginx/
        nginx.conf
    .github/
        workflows/
            deploy.yml
    docs/
        ssl-setup.md
        deployment.md
    docker-compose.yml
    backup.sh
    README.md

## Setup and Deployment

### Prerequisites

- Docker and Docker Compose installed on server
- Port 80 open in firewall/security group

### Local setup

    git clone https://github.com/skaftab-in/devops-production-stack.git
    cd devops-production-stack
    cp .env.example .env
    # edit .env with your values
    docker compose up -d

### Production deployment

    # On the server
    git clone https://github.com/skaftab-in/devops-production-stack.git /opt/devops-production-stack
    cd /opt/devops-production-stack
    cp .env.example .env
    # edit .env
    docker compose up -d

## API Endpoints

    GET  /          - root, returns API status
    GET  /health    - health check for all services
    POST /notes     - create a note (stored in PostgreSQL)
    GET  /notes     - list all notes
    POST /cache/{key} - store a value in Redis (TTL 300s)
    GET  /cache/{key} - retrieve a cached value

## CI/CD Pipeline

On every push to main branch, GitHub Actions:
1. SSH into the server
2. Pull latest code
3. Rebuild and restart containers
4. Prune old images

Required GitHub secrets:
- VPS_HOST - server public IP
- VPS_USER - SSH username
- VPS_SSH_KEY - private key

## Backup

Run manually or add to cron:

    chmod +x backup.sh
    ./backup.sh

Cron (runs daily at 2am):

    0 2 * * * /opt/devops-production-stack/backup.sh >> /var/log/backup.log 2>&1

Backups are stored in /opt/backups and retained for 7 days.

## Security

- NGINX rate limiting: 10 requests/second per IP
- Security headers: X-Frame-Options, X-Content-Type-Options, XSS-Protection
- FastAPI port not exposed publicly, only accessible via NGINX
- Environment variables managed via .env file, never committed to git

## SSL

See docs/ssl-setup.md for Let's Encrypt and Cloudflare setup instructions.

## Author

Aftab | DevOps Engineer
GitHub: https://github.com/skaftab-in
