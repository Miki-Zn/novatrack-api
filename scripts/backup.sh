#!/bin/bash

source .env.prod

BACKUP_DIR="./backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
FILE_NAME="db_backup_$DATE.sql.gz"

mkdir -p $BACKUP_DIR

docker compose -f docker-compose.prod.yml exec -T db pg_dump -U $POSTGRES_USER $POSTGRES_DB | gzip > $BACKUP_DIR/$FILE_NAME

find $BACKUP_DIR -type f -name "*.sql.gz" -mtime +7 -exec rm {} \;