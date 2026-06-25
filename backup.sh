#!/bin/bash
set -e

BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"

docker compose exec -T postgres pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" \
  | gzip > "$BACKUP_DIR/pg_backup_$DATE.sql.gz"

docker compose exec -T redis redis-cli BGSAVE
sleep 2
docker cp $(docker compose ps -q redis):/data/dump.rdb "$BACKUP_DIR/redis_$DATE.rdb"

find "$BACKUP_DIR" -name "*.gz" -mtime +7 -delete
find "$BACKUP_DIR" -name "*.rdb" -mtime +7 -delete

echo "Backup complete: $DATE"

