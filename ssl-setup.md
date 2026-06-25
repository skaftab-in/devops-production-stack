# SSL Setup

## With a domain name

Install certbot and obtain a certificate:

    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d yourdomain.com

Certbot will automatically update the nginx config. Certificates auto-renew via a systemd timer.

## nginx.conf update for SSL

    server {
        listen 80;
        server_name yourdomain.com;
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com;

        ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location / {
            proxy_pass http://app:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

## Without a domain (self-signed for testing)

    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
      -keyout nginx/ssl/selfsigned.key \
      -out nginx/ssl/selfsigned.crt \
      -subj "/C=IN/ST=Maharashtra/L=Mumbai/O=Webvory/CN=localhost"

Mount the certs in docker-compose and reference them in nginx.conf.

## Cloudflare integration

Point your domain to the server IP in Cloudflare DNS.
Set SSL mode to Full (strict) in Cloudflare dashboard.
Cloudflare handles the public-facing SSL and proxies to your server.
