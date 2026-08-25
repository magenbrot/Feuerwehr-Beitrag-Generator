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

# Generate templates manifest (JSON list of available template images)
TEMPLATES_DIR="${MEDIA_DIR}/templates"
MANIFEST="${TEMPLATES_DIR}/manifest.json"

if [ -d "${TEMPLATES_DIR}" ]; then
    MANIFEST_ENTRIES=""
    for ext in png jpg jpeg webp gif PNG JPG JPEG WEBP GIF; do
        for filepath in "${TEMPLATES_DIR}"/*.${ext}; do
            [ -f "$filepath" ] || continue
            filename=$(basename "$filepath")
            name="${filename%.*}"
            path="/media/templates/${filename}"
            if [ -z "$MANIFEST_ENTRIES" ]; then
                MANIFEST_ENTRIES="  {\"name\": \"$name\", \"path\": \"$path\"}"
            else
                MANIFEST_ENTRIES="$MANIFEST_ENTRIES
  {\"name\": \"$name\", \"path\": \"$path\"}"
            fi
        done
    done

    if [ -n "$MANIFEST_ENTRIES" ]; then
        printf '[\n%s\n]\n' "$MANIFEST_ENTRIES" > "${MANIFEST}"
    else
        echo "[]" > "${MANIFEST}"
    fi
    echo "Generated templates manifest: ${MANIFEST}"
fi

exec nginx -g 'daemon off;'
