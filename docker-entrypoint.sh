#!/bin/sh
set -e

ASSETS_DIR="/usr/share/nginx/html/assets"

# Seed default assets on first run (when volume is empty or missing files)
if [ ! -f "${ASSETS_DIR}/.seeded" ]; then
    echo "First run: seeding default assets..."
    cp -n /defaults/logo.png "${ASSETS_DIR}/logo.png" 2>/dev/null || true
    mkdir -p "${ASSETS_DIR}/templates"
    cp -n /defaults/templates/*.png "${ASSETS_DIR}/templates/" 2>/dev/null || true
    touch "${ASSETS_DIR}/.seeded"
    echo "Default assets seeded. Replace files in ${ASSETS_DIR} to customize."
else
    echo "Assets already present, skipping seed."
fi

exec nginx -g 'daemon off;'
