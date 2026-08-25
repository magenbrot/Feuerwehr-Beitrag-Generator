#!/bin/sh
set -e

MEDIA_DIR="/usr/share/nginx/html/media"

# Seed default media on first run (when volume is empty or missing files)
if [ ! -f "${MEDIA_DIR}/.seeded" ]; then
    echo "First run: seeding default media..."
    mkdir -p "${MEDIA_DIR}/templates"
    cp -n /defaults/logo.png "${MEDIA_DIR}/logo.png" 2>/dev/null || true
    cp -n /defaults/templates/*.png "${MEDIA_DIR}/templates/" 2>/dev/null || true
    touch "${MEDIA_DIR}/.seeded"
    echo "Default media seeded. Replace files in ${MEDIA_DIR} to customize."
else
    echo "Media already present, skipping seed."
fi

exec nginx -g 'daemon off;'
